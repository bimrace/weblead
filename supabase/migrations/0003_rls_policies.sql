-- ============================================================================
-- BIMRACE Lead Engine — 0003 Row Level Security
--
-- Principle: anonymous visitors may INSERT one row into crm.enquiry_submissions
-- and nothing else. They cannot SELECT it back, cannot read any CRM table, and
-- cannot reach crm.leads at all — so no public request can set a status, an
-- owner or a score. Everything internal requires an authenticated staff user.
--
-- There is deliberately no "authenticated can select everything" policy.
-- ============================================================================

-- Supabase creates these roles; guard for local testing.
do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'anon')
    then create role anon nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticated')
    then create role authenticated nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'service_role')
    then create role service_role nologin bypassrls; end if;
end $$;

grant usage on schema crm to anon, authenticated, service_role;

-- Default deny: no blanket table grants to anon.
revoke all on all tables in schema crm from anon;
revoke all on all sequences in schema crm from anon;

grant select, insert, update, delete on all tables in schema crm to authenticated;
grant usage, select on all sequences in schema crm to authenticated;
grant all on all tables in schema crm to service_role;
grant all on all sequences in schema crm to service_role;
grant all on all functions in schema crm to service_role;

-- The one public write path.
grant insert on crm.enquiry_submissions to anon;
grant usage, select on sequence crm.lead_number_seq to anon;

-- Reference data the public forms need to render dropdowns.
grant select on crm.service_categories, crm.services, crm.countries to anon;

-- Enable RLS everywhere.
do $$
declare t text;
begin
  for t in select tablename from pg_tables where schemaname = 'crm' loop
    execute format('alter table crm.%I enable row level security;', t);
    execute format('alter table crm.%I force row level security;', t);
  end loop;
end $$;
-- service_role bypasses RLS by design; it is used only by Edge Functions.

-- ------------------------------------------------------ public intake -----
drop policy if exists anon_insert_submission on crm.enquiry_submissions;
create policy anon_insert_submission on crm.enquiry_submissions
  for insert to anon with check (true);
-- No SELECT / UPDATE / DELETE policy for anon: a submitted enquiry cannot be
-- read back or altered by the public.

drop policy if exists staff_read_submission on crm.enquiry_submissions;
create policy staff_read_submission on crm.enquiry_submissions
  for select to authenticated using (crm.is_staff());

-- --------------------------------------------------- public reference -----
drop policy if exists public_read_services on crm.services;
create policy public_read_services on crm.services
  for select to anon, authenticated using (is_active);

drop policy if exists public_read_categories on crm.service_categories;
create policy public_read_categories on crm.service_categories
  for select to anon, authenticated using (is_active);

drop policy if exists public_read_countries on crm.countries;
create policy public_read_countries on crm.countries
  for select to anon, authenticated using (true);

-- ---------------------------------------------------------- app_users -----
drop policy if exists users_read_self on crm.app_users;
create policy users_read_self on crm.app_users
  for select to authenticated using (id = auth.uid() or crm.is_staff());

drop policy if exists users_admin_write on crm.app_users;
create policy users_admin_write on crm.app_users
  for all to authenticated using (crm.is_admin()) with check (crm.is_admin());
-- Note: a user cannot change their own role — only an admin can, and the
-- change is captured by the audit trigger.

-- --------------------------------------------------------------- leads -----
drop policy if exists leads_read on crm.leads;
create policy leads_read on crm.leads
  for select to authenticated using (
    case crm.current_role()
      when 'admin' then true
      when 'business_development' then true
      when 'bim_manager' then true
      when 'sales' then assigned_to = auth.uid() or assigned_to is null
      when 'project_manager' then status in ('won','negotiation','proposal_sent')
      when 'viewer' then true
      else false end);

drop policy if exists leads_update on crm.leads;
create policy leads_update on crm.leads
  for update to authenticated
  using (crm.can_write_lead(id)) with check (crm.can_write_lead(id));

drop policy if exists leads_insert on crm.leads;
create policy leads_insert on crm.leads
  for insert to authenticated with check (crm.is_staff());

drop policy if exists leads_delete on crm.leads;
create policy leads_delete on crm.leads
  for delete to authenticated using (crm.is_admin());

-- ------------------------------------------ organizations and contacts -----
drop policy if exists orgs_read on crm.organizations;
create policy orgs_read on crm.organizations
  for select to authenticated using (crm.is_staff() or crm.current_role() = 'viewer');
drop policy if exists orgs_write on crm.organizations;
create policy orgs_write on crm.organizations
  for all to authenticated using (crm.is_staff()) with check (crm.is_staff());

drop policy if exists contacts_read on crm.contacts;
create policy contacts_read on crm.contacts
  for select to authenticated using (crm.is_staff() or crm.current_role() = 'viewer');
drop policy if exists contacts_write on crm.contacts;
create policy contacts_write on crm.contacts
  for all to authenticated using (crm.is_staff()) with check (crm.is_staff());

-- ---------------------------------------- lead-scoped child collections -----
-- Each inherits the visibility of its parent lead, so a sales user who cannot
-- see a lead also cannot see its notes, tasks, files or history.
do $$
declare t text;
begin
  foreach t in array array['lead_notes','lead_tasks','communications','attachments',
                           'lead_status_history','lead_score_history','lead_assignments',
                           'lead_services']
  loop
    execute format($p$
      drop policy if exists %1$s_read on crm.%1$s;
      create policy %1$s_read on crm.%1$s for select to authenticated
        using (exists (select 1 from crm.leads l where l.id = %1$s.lead_id));
      drop policy if exists %1$s_write on crm.%1$s;
      create policy %1$s_write on crm.%1$s for all to authenticated
        using (crm.can_write_lead(lead_id)) with check (crm.can_write_lead(lead_id));
    $p$, t);
  end loop;
end $$;

-- activities may be lead-scoped or organization-scoped
drop policy if exists activities_read on crm.activities;
create policy activities_read on crm.activities
  for select to authenticated using (
    (lead_id is not null and exists (select 1 from crm.leads l where l.id = activities.lead_id))
    or (lead_id is null and crm.is_staff()));
drop policy if exists activities_write on crm.activities;
create policy activities_write on crm.activities
  for insert to authenticated with check (crm.is_staff());

-- ------------------------------------------------ proposals & projects -----
drop policy if exists proposals_read on crm.proposals;
create policy proposals_read on crm.proposals
  for select to authenticated using (crm.is_staff() or crm.current_role() = 'viewer');
drop policy if exists proposals_write on crm.proposals;
create policy proposals_write on crm.proposals
  for all to authenticated
  using (crm.current_role() in ('admin','sales','business_development'))
  with check (crm.current_role() in ('admin','sales','business_development'));

drop policy if exists proposal_items_all on crm.proposal_items;
create policy proposal_items_all on crm.proposal_items
  for all to authenticated
  using (exists (select 1 from crm.proposals p where p.id = proposal_id))
  with check (exists (select 1 from crm.proposals p where p.id = proposal_id));

drop policy if exists projects_read on crm.projects;
create policy projects_read on crm.projects
  for select to authenticated using (crm.is_staff() or crm.current_role() = 'viewer');
drop policy if exists projects_write on crm.projects;
create policy projects_write on crm.projects
  for all to authenticated
  using (crm.current_role() in ('admin','project_manager','business_development'))
  with check (crm.current_role() in ('admin','project_manager','business_development'));

-- ------------------------------------------------------- configuration -----
do $$
declare t text;
begin
  foreach t in array array['lead_sources','lost_reasons','campaigns',
                           'lead_scoring_rules','lead_routing_rules','app_settings']
  loop
    execute format($p$
      drop policy if exists %1$s_read on crm.%1$s;
      create policy %1$s_read on crm.%1$s for select to authenticated
        using (crm.is_staff() or crm.current_role() = 'viewer');
      drop policy if exists %1$s_admin on crm.%1$s;
      create policy %1$s_admin on crm.%1$s for all to authenticated
        using (crm.is_admin()) with check (crm.is_admin());
    $p$, t);
  end loop;
end $$;

-- Admin-managed reference tables that the public also reads.
drop policy if exists services_admin on crm.services;
create policy services_admin on crm.services for all to authenticated
  using (crm.is_admin()) with check (crm.is_admin());
drop policy if exists categories_admin on crm.service_categories;
create policy categories_admin on crm.service_categories for all to authenticated
  using (crm.is_admin()) with check (crm.is_admin());

-- ----------------------------------------------------------- audit log -----
-- Readable by admin only, and never editable by anyone through the API.
drop policy if exists audit_read on crm.audit_logs;
create policy audit_read on crm.audit_logs
  for select to authenticated using (crm.is_admin());
revoke insert, update, delete on crm.audit_logs from authenticated, anon;
-- Rows arrive only through the SECURITY DEFINER audit trigger.

-- ------------------------------------------------------ function grants ----
revoke all on function crm.fn_score_lead(uuid, text) from public, anon;
revoke all on function crm.fn_route_lead(uuid) from public, anon;
revoke all on function crm.fn_convert_lead_to_project(uuid, text) from public, anon;
revoke all on function crm.fn_dashboard_metrics() from public, anon;

grant execute on function crm.fn_dashboard_metrics() to authenticated;
grant execute on function crm.fn_convert_lead_to_project(uuid, text) to authenticated;
grant execute on function crm.current_role() to authenticated;
grant execute on function crm.is_admin() to authenticated;
grant execute on function crm.is_staff() to authenticated;
grant execute on function crm.can_write_lead(uuid) to authenticated;

-- Future tables in this schema keep the same default posture.
alter default privileges in schema crm grant select, insert, update, delete on tables to authenticated;
alter default privileges in schema crm grant all on tables to service_role;
