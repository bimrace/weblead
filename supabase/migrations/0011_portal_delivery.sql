-- ============================================================================
-- BIMRACE Lead Engine — 0011 portal: contracts and project delivery
--
-- Adds the delivery side of the business to the CRM:
--   lead -> proposal -> CONTRACT -> PROJECT -> stages, milestones,
--   deliverables (the catalogue handover checklist), tasks and team.
--
-- Access model (RLS):
--   admin                       everything
--   business_development        contracts read/write; projects read/write
--   project_manager, bim_manager  projects and delivery read/write; contracts read
--   sales                       contracts read
--   engineer                    ONLY projects they are a member of; read delivery
--                               data there and update deliverables/tasks assigned
--                               to them. No leads, contacts, proposals, contracts.
--   viewer                      read-only projects and delivery
-- Every table is audited by crm.fn_audit. Additive and idempotent.
-- ============================================================================

-- -------------------------------------------------------- project stage -----
alter table crm.projects add column if not exists stage text not null default 'kickoff';
alter table crm.projects add column if not exists health text not null default 'on_track';
alter table crm.projects add column if not exists progress int not null default 0;
alter table crm.projects add column if not exists building_type text;
alter table crm.projects add column if not exists location text;
alter table crm.projects add column if not exists package_code text;      -- catalogue PKG-0x
alter table crm.projects add column if not exists design_responsibility boolean not null default false;
do $$ begin
  alter table crm.projects add constraint projects_stage_valid check (stage in
    ('kickoff','inputs_review','design','modelling','coordination','qa_qc','issued','handover','closed'));
exception when duplicate_object then null; end $$;
do $$ begin
  alter table crm.projects add constraint projects_health_valid check (health in ('on_track','at_risk','blocked'));
exception when duplicate_object then null; end $$;
do $$ begin
  alter table crm.projects add constraint projects_progress_valid check (progress between 0 and 100);
exception when duplicate_object then null; end $$;

-- ------------------------------------------------------------ contracts -----
create sequence if not exists crm.contract_number_seq start 100;

create table if not exists crm.contracts (
  id               uuid primary key default gen_random_uuid(),
  contract_number  text unique not null
                   default 'BR-C-' || lpad(nextval('crm.contract_number_seq')::text, 5, '0'),
  title            text not null check (char_length(title) between 3 and 200),
  organization_id  uuid references crm.organizations(id) on delete restrict,
  lead_id          uuid references crm.leads(id) on delete set null,
  proposal_id      uuid references crm.proposals(id) on delete set null,
  project_id       uuid references crm.projects(id) on delete set null,
  contract_type    text not null default 'fixed_fee'
                   check (contract_type in ('fixed_fee','time_and_materials','retainer','framework')),
  status           text not null default 'draft'
                   check (status in ('draft','sent','signed','active','completed','terminated')),
  value            numeric(14,2) check (value is null or value >= 0),
  currency         char(3) not null default 'INR',
  design_responsibility boolean not null default false,  -- PKG-05: design is in scope
  scope_summary    text,
  payment_terms    text,
  signed_date      date,
  start_date       date,
  end_date         date,
  document_path    text,          -- signed PDF in private storage, optional
  created_by       uuid references crm.app_users(id) on delete set null default auth.uid(),
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  constraint contracts_dates check (end_date is null or start_date is null or end_date >= start_date)
);
create index if not exists contracts_project_idx on crm.contracts (project_id);
create index if not exists contracts_status_idx on crm.contracts (status);

-- ------------------------------------------------------- project team -----
create table if not exists crm.project_members (
  project_id   uuid not null references crm.projects(id) on delete cascade,
  user_id      uuid not null references crm.app_users(id) on delete cascade,
  project_role text not null default 'engineer'
               check (project_role in ('project_manager','bim_manager','lead_engineer','engineer',
                                       'modeller','coordinator','reviewer')),
  added_at     timestamptz not null default now(),
  primary key (project_id, user_id)
);
create index if not exists project_members_user_idx on crm.project_members (user_id);

-- --------------------------------------------------------- milestones -----
create table if not exists crm.project_milestones (
  id             uuid primary key default gen_random_uuid(),
  project_id     uuid not null references crm.projects(id) on delete cascade,
  name           text not null check (char_length(name) between 2 and 200),
  due_date       date,
  status         text not null default 'pending' check (status in ('pending','in_progress','done')),
  invoice_amount numeric(14,2) check (invoice_amount is null or invoice_amount >= 0),
  invoiced       boolean not null default false,
  sort_order     int not null default 0,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);
create index if not exists milestones_project_idx on crm.project_milestones (project_id);

-- -------------------------------------------------------- deliverables -----
-- Categories follow the catalogue Handover Checklist.
create table if not exists crm.project_deliverables (
  id           uuid primary key default gen_random_uuid(),
  project_id   uuid not null references crm.projects(id) on delete cascade,
  name         text not null check (char_length(name) between 2 and 200),
  category     text not null default 'drawing_package'
               check (category in ('native_model','federated_model','drawing_package',
                                   'schedules_quantities','clash_report','design_documentation',
                                   'qa_report','revision_register','exchange_files','handover_note',
                                   'calculations','other')),
  discipline   text,
  status       text not null default 'not_started'
               check (status in ('not_started','in_progress','in_review','issued','approved','rejected')),
  revision     text,
  due_date     date,
  issued_at    timestamptz,
  assignee_id  uuid references crm.app_users(id) on delete set null,
  notes        text,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create index if not exists deliverables_project_idx on crm.project_deliverables (project_id);
create index if not exists deliverables_assignee_idx on crm.project_deliverables (assignee_id);

-- --------------------------------------------------------------- tasks -----
create table if not exists crm.project_tasks (
  id           uuid primary key default gen_random_uuid(),
  project_id   uuid not null references crm.projects(id) on delete cascade,
  deliverable_id uuid references crm.project_deliverables(id) on delete set null,
  title        text not null check (char_length(title) between 2 and 300),
  description  text,
  status       text not null default 'todo' check (status in ('todo','in_progress','blocked','done')),
  priority     text not null default 'normal' check (priority in ('low','normal','high','urgent')),
  assignee_id  uuid references crm.app_users(id) on delete set null,
  due_date     date,
  created_by   uuid references crm.app_users(id) on delete set null default auth.uid(),
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create index if not exists tasks_project_idx on crm.project_tasks (project_id);
create index if not exists tasks_assignee_idx on crm.project_tasks (assignee_id);

-- ------------------------------------------------------------ helpers -----
create or replace function crm.can_manage_delivery() returns boolean
language sql stable security definer set search_path = crm, public as $$
  select crm.current_role() in ('admin','project_manager','bim_manager','business_development');
$$;

create or replace function crm.is_project_member(p_project_id uuid) returns boolean
language sql stable security definer set search_path = crm, public as $$
  select exists (select 1 from crm.project_members m
                 join crm.app_users u on u.id = m.user_id and u.is_active
                 where m.project_id = p_project_id and m.user_id = auth.uid());
$$;

-- Read access to a project's delivery data.
create or replace function crm.can_read_project(p_project_id uuid) returns boolean
language sql stable security definer set search_path = crm, public as $$
  select crm.is_staff() or crm.current_role() = 'viewer' or crm.is_project_member(p_project_id);
$$;

-- ----------------------------------------- timestamps, audit, privileges -----
do $$
declare t text;
begin
  foreach t in array array['contracts','project_milestones','project_deliverables','project_tasks']
  loop
    execute format('drop trigger if exists trg_%1$s_touch on crm.%1$s;
                    create trigger trg_%1$s_touch before update on crm.%1$s
                    for each row execute function crm.fn_touch_updated_at();', t);
  end loop;
  foreach t in array array['contracts','project_members','project_milestones',
                           'project_deliverables','project_tasks']
  loop
    execute format('drop trigger if exists trg_%1$s_audit on crm.%1$s;
                    create trigger trg_%1$s_audit after insert or update or delete on crm.%1$s
                    for each row execute function crm.fn_audit();', t);
    execute format('alter table crm.%1$s enable row level security;', t);
    execute format('grant select, insert, update, delete on crm.%1$s to authenticated;', t);
    execute format('grant all on crm.%1$s to service_role;', t);
    execute format('revoke all on crm.%1$s from anon;', t);
  end loop;
end $$;
grant usage, select on sequence crm.contract_number_seq to authenticated, service_role;
grant execute on function crm.can_manage_delivery(), crm.is_project_member(uuid),
                          crm.can_read_project(uuid) to authenticated;
revoke execute on function crm.can_manage_delivery(), crm.is_project_member(uuid),
                           crm.can_read_project(uuid) from anon, public;

-- -------------------------------------------------------------- policies -----
-- Projects: engineers additionally see the projects they belong to.
drop policy if exists projects_member_read on crm.projects;
create policy projects_member_read on crm.projects
  for select to authenticated using (crm.is_project_member(id));
drop policy if exists projects_write on crm.projects;
create policy projects_write on crm.projects
  for all to authenticated
  using (crm.can_manage_delivery()) with check (crm.can_manage_delivery());

-- Contracts: commercial roles only.
drop policy if exists contracts_read on crm.contracts;
create policy contracts_read on crm.contracts for select to authenticated
  using (crm.current_role() in ('admin','business_development','project_manager','sales'));
drop policy if exists contracts_write on crm.contracts;
create policy contracts_write on crm.contracts for all to authenticated
  using (crm.current_role() in ('admin','business_development'))
  with check (crm.current_role() in ('admin','business_development'));

-- Team.
drop policy if exists members_read on crm.project_members;
create policy members_read on crm.project_members for select to authenticated
  using (crm.can_read_project(project_id));
drop policy if exists members_write on crm.project_members;
create policy members_write on crm.project_members for all to authenticated
  using (crm.can_manage_delivery()) with check (crm.can_manage_delivery());

-- Milestones: managers write, project readers read.
drop policy if exists milestones_read on crm.project_milestones;
create policy milestones_read on crm.project_milestones for select to authenticated
  using (crm.can_read_project(project_id));
drop policy if exists milestones_write on crm.project_milestones;
create policy milestones_write on crm.project_milestones for all to authenticated
  using (crm.can_manage_delivery()) with check (crm.can_manage_delivery());

-- Deliverables and tasks: managers write everything; an engineer may update
-- the rows assigned to them on projects they belong to.
drop policy if exists deliverables_read on crm.project_deliverables;
create policy deliverables_read on crm.project_deliverables for select to authenticated
  using (crm.can_read_project(project_id));
drop policy if exists deliverables_manage on crm.project_deliverables;
create policy deliverables_manage on crm.project_deliverables for all to authenticated
  using (crm.can_manage_delivery()) with check (crm.can_manage_delivery());
drop policy if exists deliverables_assignee_update on crm.project_deliverables;
create policy deliverables_assignee_update on crm.project_deliverables for update to authenticated
  using (assignee_id = auth.uid() and crm.is_project_member(project_id))
  with check (assignee_id = auth.uid() and crm.is_project_member(project_id));

drop policy if exists tasks_read on crm.project_tasks;
create policy tasks_read on crm.project_tasks for select to authenticated
  using (crm.can_read_project(project_id));
drop policy if exists tasks_manage on crm.project_tasks;
create policy tasks_manage on crm.project_tasks for all to authenticated
  using (crm.can_manage_delivery()) with check (crm.can_manage_delivery());
drop policy if exists tasks_member_insert on crm.project_tasks;
create policy tasks_member_insert on crm.project_tasks for insert to authenticated
  with check (crm.is_project_member(project_id));
drop policy if exists tasks_assignee_update on crm.project_tasks;
create policy tasks_assignee_update on crm.project_tasks for update to authenticated
  using (assignee_id = auth.uid() and crm.is_project_member(project_id))
  with check (assignee_id = auth.uid() and crm.is_project_member(project_id));

-- Engineers need to see colleagues' names on their projects.
drop policy if exists users_project_peers on crm.app_users;
create policy users_project_peers on crm.app_users for select to authenticated
  using (exists (select 1 from crm.project_members a
                 join crm.project_members b on b.project_id = a.project_id
                 where a.user_id = auth.uid() and b.user_id = crm.app_users.id));

-- ------------------------------------------------------ dashboard metrics -----
create or replace function crm.fn_delivery_metrics() returns jsonb
language sql stable security definer set search_path = crm, public as $$
  select case when not (crm.can_manage_delivery() or crm.current_role() = 'engineer') then null else
  jsonb_build_object(
    'projects_active',  (select count(*) from crm.projects p where p.status = 'active'
                          and (crm.can_manage_delivery() or crm.is_project_member(p.id))),
    'projects_at_risk', (select count(*) from crm.projects p where p.health <> 'on_track'
                          and p.status in ('planned','active')
                          and (crm.can_manage_delivery() or crm.is_project_member(p.id))),
    'deliverables_due_7d', (select count(*) from crm.project_deliverables d
                          where d.status not in ('issued','approved') and d.due_date <= current_date + 7
                          and (crm.can_manage_delivery() or crm.is_project_member(d.project_id))),
    'my_open_tasks',    (select count(*) from crm.project_tasks t
                          where t.assignee_id = auth.uid() and t.status <> 'done'),
    'contracts_signed_value', case when crm.current_role() in ('admin','business_development')
                          then (select coalesce(sum(value),0) from crm.contracts
                                where status in ('signed','active','completed')) end
  ) end;
$$;
grant execute on function crm.fn_delivery_metrics() to authenticated;
revoke execute on function crm.fn_delivery_metrics() from anon, public;
