-- ============================================================================
-- BIMRACE Lead Engine — 0002 functions, triggers and the intake pipeline
-- Additive only. All functions use CREATE OR REPLACE.
-- ============================================================================

-- ------------------------------------------------------ role helpers ------
-- SECURITY DEFINER so RLS on app_users cannot recurse when a policy calls it.
create or replace function crm.current_role()
returns crm.app_role
language sql stable security definer set search_path = crm, public as $$
  select coalesce(
    (select role from crm.app_users where id = auth.uid() and is_active),
    'viewer'::crm.app_role);
$$;

create or replace function crm.is_admin() returns boolean
language sql stable security definer set search_path = crm, public as $$
  select exists (select 1 from crm.app_users
                 where id = auth.uid() and is_active and role = 'admin');
$$;

create or replace function crm.is_staff() returns boolean
language sql stable security definer set search_path = crm, public as $$
  select exists (select 1 from crm.app_users
                 where id = auth.uid() and is_active
                   and role in ('admin','sales','business_development',
                                'project_manager','bim_manager'));
$$;

-- Can this user act on this lead? Admin and BD see everything; sales sees
-- what they own or what is unassigned in the queue; others read-only elsewhere.
create or replace function crm.can_write_lead(p_lead_id uuid) returns boolean
language sql stable security definer set search_path = crm, public as $$
  select case crm.current_role()
    when 'admin' then true
    when 'business_development' then true
    when 'sales' then exists (
      select 1 from crm.leads l
      where l.id = p_lead_id
        and (l.assigned_to = auth.uid() or l.assigned_to is null))
    when 'project_manager' then exists (
      select 1 from crm.leads l where l.id = p_lead_id and l.status = 'won')
    else false
  end;
$$;

-- --------------------------------------------------------- housekeeping ---
create or replace function crm.fn_touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;

do $$
declare t text;
begin
  foreach t in array array['app_users','organizations','contacts','leads',
                           'lead_notes','lead_tasks','proposals','projects']
  loop
    execute format(
      'drop trigger if exists trg_touch_%1$s on crm.%1$s;
       create trigger trg_touch_%1$s before update on crm.%1$s
       for each row execute function crm.fn_touch_updated_at();', t);
  end loop;
end $$;

-- ------------------------------------------------------- scoring engine ---
-- Reads crm.lead_scoring_rules, evaluates each active rule against the lead,
-- and records every rule that fired with its points. Nothing is opaque: the
-- breakdown is stored so any score can be explained after the fact.
create or replace function crm.fn_score_lead(p_lead_id uuid, p_reason text default 'engine')
returns int language plpgsql security definer set search_path = crm, public as $$
declare
  l            crm.leads%rowtype;
  r            record;
  v            text;
  matched      boolean;
  total        int := 0;
  breakdown    jsonb := '[]'::jsonb;
  band         crm.score_band;
  prev_score   int;
  prev_band    crm.score_band;
begin
  select * into l from crm.leads where id = p_lead_id;
  if not found then return null; end if;
  prev_score := l.lead_score; prev_band := l.score_band;

  for r in select * from crm.lead_scoring_rules where is_active order by sort_order, code loop
    -- Resolve the field from the lead row as text.
    execute format('select ($1).%I::text', r.field) into v using l;

    matched := case r.operator
      when 'present'  then v is not null and btrim(v) <> '' and v <> '{}'
      when 'absent'   then v is null or btrim(v) = '' or v = '{}'
      when 'eq'       then v = r.value
      when 'neq'      then v is distinct from r.value
      when 'gt'       then v is not null and v ~ '^-?\d+(\.\d+)?$' and v::numeric >  r.value::numeric
      when 'gte'      then v is not null and v ~ '^-?\d+(\.\d+)?$' and v::numeric >= r.value::numeric
      when 'lt'       then v is not null and v ~ '^-?\d+(\.\d+)?$' and v::numeric <  r.value::numeric
      when 'lte'      then v is not null and v ~ '^-?\d+(\.\d+)?$' and v::numeric <= r.value::numeric
      when 'in'       then v = any (string_to_array(r.value, ','))
      when 'contains' then v is not null and position(lower(r.value) in lower(v)) > 0
      when 'matches'  then v is not null and v ~* r.value
      else false end;

    if matched then
      total := total + r.points;
      breakdown := breakdown || jsonb_build_object(
        'code', r.code, 'label', r.label, 'points', r.points,
        'field', r.field, 'operator', r.operator, 'value', r.value);
    end if;
  end loop;

  total := greatest(-100, least(200, total));
  band := case
    when total >= 76 then 'hot'
    when total >= 51 then 'high'
    when total >= 21 then 'medium'
    else 'low' end::crm.score_band;

  update crm.leads set lead_score = total, score_band = band where id = p_lead_id;

  insert into crm.lead_score_history
    (lead_id, previous_score, new_score, previous_band, new_band, breakdown, computed_by)
  values (p_lead_id, prev_score, total, prev_band, band,
          jsonb_build_object('rules', breakdown, 'total', total), p_reason);

  insert into crm.activities (lead_id, activity_type, summary, detail)
  values (p_lead_id, 'lead_scored',
          format('Scored %s (%s)', total, band),
          jsonb_build_object('rules', breakdown));

  return total;
end $$;

-- ------------------------------------------------------- routing engine ---
create or replace function crm.fn_route_lead(p_lead_id uuid)
returns uuid language plpgsql security definer set search_path = crm, public as $$
declare
  l       crm.leads%rowtype;
  r       crm.lead_routing_rules%rowtype;
  target  uuid;
begin
  select * into l from crm.leads where id = p_lead_id;
  if not found then return null; end if;

  for r in select * from crm.lead_routing_rules where is_active order by priority, code loop
    if (r.match_lead_type is null or r.match_lead_type = l.lead_type)
   and (r.match_country_in is null or l.country_code = any (r.match_country_in))
   and (r.match_international is null or r.match_international = l.is_international)
   and (r.match_min_score is null or l.lead_score >= r.match_min_score)
    then
      target := r.assign_to_user;
      if target is null and r.assign_to_role is not null then
        -- least-loaded active user holding the required role
        select u.id into target
        from crm.app_users u
        left join crm.leads x on x.assigned_to = u.id
             and x.status not in ('won','lost','spam','duplicate','not_qualified')
        where u.role = r.assign_to_role and u.is_active
        group by u.id order by count(x.id) asc, u.created_at asc limit 1;
      end if;

      if target is not null then
        update crm.leads
           set assigned_to = target, assigned_at = now(),
               priority = coalesce(r.set_priority, priority)
         where id = p_lead_id;

        insert into crm.lead_assignments (lead_id, assigned_to, rule_code, reason)
        values (p_lead_id, target, r.code, r.label);

        insert into crm.activities (lead_id, activity_type, summary, detail)
        values (p_lead_id, 'lead_assigned', format('Assigned by rule %s', r.code),
                jsonb_build_object('rule', r.code, 'assigned_to', target));
        return target;
      end if;
    end if;
  end loop;

  insert into crm.activities (lead_id, activity_type, summary)
  values (p_lead_id, 'lead_unrouted', 'No routing rule matched — left in general queue');
  return null;
end $$;

-- ------------------------------------------- status history + timestamps --
create or replace function crm.fn_lead_status_change()
returns trigger language plpgsql security definer set search_path = crm, public as $$
begin
  if new.status is distinct from old.status then
    insert into crm.lead_status_history (lead_id, from_status, to_status, changed_by)
    values (new.id, old.status, new.status, auth.uid());

    insert into crm.activities (lead_id, actor_id, activity_type, summary)
    values (new.id, auth.uid(), 'status_changed',
            format('Status %s to %s', old.status, new.status));

    if new.status = 'won' and new.converted_at is null then new.converted_at := now(); end if;
    if new.status = 'lost' and new.lost_at is null then new.lost_at := now(); end if;
  end if;

  if new.assigned_to is distinct from old.assigned_to and new.assigned_to is not null then
    insert into crm.lead_assignments (lead_id, assigned_to, assigned_by, reason)
    values (new.id, new.assigned_to, auth.uid(), 'manual');
  end if;
  return new;
end $$;

drop trigger if exists trg_lead_status on crm.leads;
create trigger trg_lead_status before update on crm.leads
for each row execute function crm.fn_lead_status_change();

-- ------------------------------------------------------------ audit log ---
create or replace function crm.fn_audit()
returns trigger language plpgsql security definer set search_path = crm, public as $$
declare
  old_j jsonb; new_j jsonb; changed text[];
begin
  old_j := case when tg_op in ('UPDATE','DELETE') then to_jsonb(old) end;
  new_j := case when tg_op in ('INSERT','UPDATE') then to_jsonb(new) end;

  if tg_op = 'UPDATE' then
    select array_agg(key) into changed
    from jsonb_each(new_j) n
    where n.value is distinct from (old_j -> n.key);
    if changed is null then return new; end if;   -- nothing actually changed
  end if;

  insert into crm.audit_logs
    (table_name, record_id, action, actor_id, changed_fields, old_values, new_values)
  values (tg_table_name,
          coalesce((new_j ->> 'id'), (old_j ->> 'id')),
          tg_op, auth.uid(), changed, old_j, new_j);

  return coalesce(new, old);
end $$;

do $$
declare t text;
begin
  foreach t in array array['leads','organizations','contacts','proposals',
                           'projects','app_users','lead_scoring_rules','lead_routing_rules']
  loop
    execute format(
      'drop trigger if exists trg_audit_%1$s on crm.%1$s;
       create trigger trg_audit_%1$s after insert or update or delete on crm.%1$s
       for each row execute function crm.fn_audit();', t);
  end loop;
end $$;

-- ------------------------------------------------- deduplication helper ---
create or replace function crm.fn_find_duplicate(p_email citext, p_phone text)
returns uuid language sql stable security definer set search_path = crm, public as $$
  select id from crm.leads
  where (p_email is not null and email = p_email)
     or (p_phone is not null and btrim(p_phone) <> '' and phone = p_phone)
  order by created_at desc limit 1;
$$;

-- ------------------------------------------------- the intake pipeline ----
-- Runs on insert into enquiry_submissions. This is the single path public data
-- takes into the CRM: validate, link or create organization + contact, create
-- the lead, score it, route it. Nothing here trusts the payload for internal
-- fields — status, score and owner are always set by the engine.
create or replace function crm.fn_process_submission()
returns trigger language plpgsql security definer set search_path = crm, public as $$
declare
  p            jsonb := new.payload;
  v_email      citext := nullif(lower(btrim(p ->> 'email')), '');
  v_domain     citext;
  v_company    text   := nullif(btrim(p ->> 'company'), '');
  v_name       text   := nullif(btrim(p ->> 'name'), '');
  v_phone      text   := nullif(btrim(p ->> 'phone'), '');
  v_country    char(2):= upper(nullif(btrim(p ->> 'country_code'), ''));
  v_org        uuid;
  v_contact    uuid;
  v_lead       uuid;
  v_source     uuid;
  v_dup        uuid;
  free_domains text[] := array['gmail.com','yahoo.com','outlook.com','hotmail.com',
                               'live.com','icloud.com','aol.com','proton.me','protonmail.com'];
begin
  -- minimum viable enquiry
  if v_email is null or v_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' or v_name is null then
    update crm.enquiry_submissions
       set rejection_reason = 'invalid_contact_details',
           processed = true, processed_at = now()
     where id = new.id;
    return null;
  end if;

  v_domain := split_part(v_email::text, '@', 2);

  -- Existing lead from the same person? Keep the enquiry, do not create a
  -- second customer record.
  v_dup := crm.fn_find_duplicate(v_email, v_phone);

  -- organization: match on business domain, else on name
  if v_domain is not null and not (v_domain::text = any (free_domains)) then
    select id into v_org from crm.organizations where email_domain = v_domain;
  end if;
  if v_org is null and v_company is not null then
    select id into v_org from crm.organizations
    where normalized_name = lower(btrim(v_company)) limit 1;
  end if;
  if v_org is null and (v_company is not null or v_domain is not null) then
    insert into crm.organizations (name, email_domain, website, country_code, city, company_size)
    values (coalesce(v_company, v_domain::text),
            case when v_domain::text = any (free_domains) then null else v_domain end,
            nullif(btrim(p ->> 'website'), ''), v_country,
            nullif(btrim(p ->> 'city'), ''),
            coalesce(nullif(p ->> 'company_size',''), 'unknown')::crm.company_size)
    returning id into v_org;
  end if;

  -- contact
  select id into v_contact from crm.contacts where email = v_email;
  if v_contact is null then
    insert into crm.contacts (organization_id, full_name, email, phone, job_title,
                              country_code, linkedin_url)
    values (v_org, v_name, v_email, v_phone, nullif(btrim(p ->> 'job_title'),''),
            v_country, nullif(btrim(p ->> 'linkedin_url'),''))
    returning id into v_contact;
  else
    update crm.contacts
       set organization_id = coalesce(organization_id, v_org),
           phone = coalesce(phone, v_phone),
           job_title = coalesce(job_title, nullif(btrim(p ->> 'job_title'),''))
     where id = v_contact;
  end if;

  select id into v_source from crm.lead_sources
   where code = coalesce(new.source_code, 'website');

  insert into crm.leads (
    organization_id, contact_id, source_id, submission_id, lead_type,
    country_code, region, city, timezone,
    company_name, contact_name, email, phone, website, job_title, industry, company_size,
    service_interest, disciplines, software, project_type, project_location, project_stage,
    required_lod, required_standards, deliverables, project_size, existing_model,
    team_size_required, estimated_budget, currency,
    project_start_date, required_delivery_date, message,
    status, duplicate_of)
  values (
    v_org, v_contact, v_source, new.id, nullif(btrim(p ->> 'lead_type'), ''),
    v_country, nullif(btrim(p ->> 'region'),''), nullif(btrim(p ->> 'city'),''),
    nullif(btrim(p ->> 'timezone'),''),
    v_company, v_name, v_email, v_phone, nullif(btrim(p ->> 'website'),''),
    nullif(btrim(p ->> 'job_title'),''), nullif(btrim(p ->> 'industry'),''),
    coalesce(nullif(p ->> 'company_size',''), 'unknown')::crm.company_size,
    case when p ? 'service_interest' then
      array(select jsonb_array_elements_text(p -> 'service_interest')) end,
    case when p ? 'disciplines' then
      array(select jsonb_array_elements_text(p -> 'disciplines')) end,
    case when p ? 'software' then
      array(select jsonb_array_elements_text(p -> 'software')) end,
    nullif(btrim(p ->> 'project_type'),''), nullif(btrim(p ->> 'project_location'),''),
    nullif(btrim(p ->> 'project_stage'),''), nullif(btrim(p ->> 'required_lod'),''),
    case when p ? 'required_standards' then
      array(select jsonb_array_elements_text(p -> 'required_standards')) end,
    case when p ? 'deliverables' then
      array(select jsonb_array_elements_text(p -> 'deliverables')) end,
    nullif(btrim(p ->> 'project_size'),''),
    case when p ? 'existing_model' then (p ->> 'existing_model')::boolean end,
    nullif(p ->> 'team_size_required','')::int,
    nullif(p ->> 'estimated_budget','')::numeric,
    upper(nullif(btrim(p ->> 'currency'),''))::char(3),
    nullif(p ->> 'project_start_date','')::date,
    nullif(p ->> 'required_delivery_date','')::date,
    nullif(btrim(p ->> 'message'),''),
    case when v_dup is not null then 'duplicate' else 'new' end::crm.lead_status,
    v_dup)
  returning id into v_lead;

  insert into crm.activities (lead_id, organization_id, activity_type, summary, detail)
  values (v_lead, v_org, 'lead_created',
          format('Enquiry received via %s', new.form_code),
          jsonb_build_object('form', new.form_code, 'source', new.source_code,
                             'utm_source', new.utm_source, 'utm_campaign', new.utm_campaign,
                             'landing_page', new.landing_page));

  if v_dup is not null then
    insert into crm.activities (lead_id, activity_type, summary, detail)
    values (v_dup, 'duplicate_enquiry',
            'Same contact submitted another enquiry',
            jsonb_build_object('new_lead', v_lead));
  end if;

  perform crm.fn_score_lead(v_lead, 'intake');
  if v_dup is null then perform crm.fn_route_lead(v_lead); end if;

  update crm.enquiry_submissions
     set lead_id = v_lead, processed = true, processed_at = now()
   where id = new.id;
  return null;
end $$;

-- AFTER INSERT, not BEFORE: the lead carries a foreign key back to the
-- submission, so the submission row has to exist before the lead is created.
drop trigger if exists trg_process_submission on crm.enquiry_submissions;
create trigger trg_process_submission after insert on crm.enquiry_submissions
for each row execute function crm.fn_process_submission();

-- ------------------------------------------------- lead -> project ---------
create or replace function crm.fn_convert_lead_to_project(p_lead_id uuid, p_name text default null)
returns uuid language plpgsql security definer set search_path = crm, public as $$
declare l crm.leads%rowtype; v_project uuid;
begin
  if not crm.can_write_lead(p_lead_id) then
    raise exception 'not authorised to convert this lead';
  end if;
  select * into l from crm.leads where id = p_lead_id;
  if not found then raise exception 'lead not found'; end if;
  if l.organization_id is null then raise exception 'lead has no organization'; end if;

  select id into v_project from crm.projects where lead_id = p_lead_id;
  if v_project is not null then return v_project; end if;   -- idempotent

  insert into crm.projects (organization_id, primary_contact_id, lead_id, name,
                            disciplines, deliverables, scope_summary, currency, status)
  values (l.organization_id, l.contact_id, l.id,
          coalesce(p_name, coalesce(l.project_type, 'Project') || ' — ' || coalesce(l.company_name,'Client')),
          l.disciplines, l.deliverables, l.message, coalesce(l.currency,'INR'), 'planned')
  returning id into v_project;

  update crm.leads set status = 'won', converted_at = now() where id = p_lead_id;

  insert into crm.activities (lead_id, organization_id, actor_id, activity_type, summary, detail)
  values (p_lead_id, l.organization_id, auth.uid(), 'project_created',
          'Lead converted to project', jsonb_build_object('project_id', v_project));
  return v_project;
end $$;

-- --------------------------------------------------- dashboard metrics ----
-- One round trip for the dashboard rather than a dozen count queries.
create or replace function crm.fn_dashboard_metrics()
returns jsonb language sql stable security definer set search_path = crm, public as $$
  select case when not crm.is_staff() then '{}'::jsonb else jsonb_build_object(
    'new_today',      (select count(*) from crm.leads where created_at >= current_date),
    'new_this_week',  (select count(*) from crm.leads where created_at >= date_trunc('week', now())),
    'open',           (select count(*) from crm.leads
                       where status not in ('won','lost','spam','duplicate','not_qualified')),
    'hot',            (select count(*) from crm.leads where score_band = 'hot'
                       and status not in ('won','lost','spam','duplicate')),
    'qualified',      (select count(*) from crm.leads where status = 'qualified'),
    'proposals_open', (select count(*) from crm.proposals
                       where status in ('sent','viewed','negotiation')),
    'followups_due',  (select count(*) from crm.lead_tasks
                       where status = 'pending' and due_at::date <= current_date),
    'followups_overdue', (select count(*) from crm.lead_tasks
                       where status = 'pending' and due_at < now() - interval '1 day'),
    'won',            (select count(*) from crm.leads where status = 'won'),
    'lost',           (select count(*) from crm.leads where status = 'lost'),
    'india',          (select count(*) from crm.leads where country_code = 'IN'),
    'international',  (select count(*) from crm.leads where is_international),
    'by_status',      (select coalesce(jsonb_object_agg(status, n), '{}'::jsonb)
                       from (select status, count(*) n from crm.leads group by status) s),
    'by_type',        (select coalesce(jsonb_object_agg(coalesce(lead_type,'unspecified'), n), '{}'::jsonb)
                       from (select lead_type, count(*) n from crm.leads group by lead_type) t),
    'by_country',     (select coalesce(jsonb_object_agg(coalesce(country_code,'??'), n), '{}'::jsonb)
                       from (select country_code, count(*) n from crm.leads group by country_code) c),
    'by_source',      (select coalesce(jsonb_object_agg(coalesce(s.name,'Unknown'), n), '{}'::jsonb)
                       from (select source_id, count(*) n from crm.leads group by source_id) l
                       left join crm.lead_sources s on s.id = l.source_id)
  ) end;
$$;
