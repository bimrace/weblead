-- ============================================================================
-- BIMRACE Lead Engine — 0001 core schema
--
-- ADDITIVE ONLY. Every object uses IF NOT EXISTS. There is no DROP, no TRUNCATE
-- and no ALTER that removes a column, so this migration cannot damage existing
-- data in the project. It is safe to run against a database already in use.
--
-- All objects live in the `crm` schema so they cannot collide with anything
-- already present in `public`.
-- ============================================================================

create schema if not exists crm;

create extension if not exists "pgcrypto";   -- gen_random_uuid()
create extension if not exists "citext";     -- case-insensitive email

-- ---------------------------------------------------------------- enums ----
do $$ begin
  create type crm.app_role as enum
    ('admin','sales','business_development','project_manager','bim_manager','viewer');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.lead_status as enum
    ('new','contacted','qualifying','qualified','discovery','scope_defined',
     'proposal_required','proposal_sent','negotiation','won','lost',
     'on_hold','not_qualified','spam','duplicate');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.lead_priority as enum ('low','normal','high','urgent');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.score_band as enum ('low','medium','high','hot');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.comm_direction as enum ('inbound','outbound');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.comm_channel as enum
    ('email','phone','whatsapp','meeting','web_form','linkedin','other');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.task_status as enum
    ('pending','completed','skipped','cancelled');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.proposal_status as enum
    ('draft','internal_review','sent','viewed','negotiation','accepted','rejected','expired');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.project_status as enum
    ('planned','active','on_hold','completed','cancelled');
exception when duplicate_object then null; end $$;

do $$ begin
  create type crm.company_size as enum
    ('individual','1-10','11-50','51-200','201-1000','1000+','unknown');
exception when duplicate_object then null; end $$;

-- ------------------------------------------------------------ app users ----
-- Mirrors auth.users. Role lives here, never on the JWT claims the client
-- controls, so a user cannot escalate their own privileges.
create table if not exists crm.app_users (
  id            uuid primary key,
  email         citext not null,
  full_name     text,
  role          crm.app_role not null default 'viewer',
  is_active     boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ------------------------------------------------------- reference data ----
create table if not exists crm.lead_sources (
  id          uuid primary key default gen_random_uuid(),
  code        text unique not null,
  name        text not null,
  is_active   boolean not null default true,
  sort_order  int not null default 0
);

create table if not exists crm.service_categories (
  id          uuid primary key default gen_random_uuid(),
  code        text unique not null,
  name        text not null,
  description text,
  is_active   boolean not null default true,
  sort_order  int not null default 0
);

create table if not exists crm.services (
  id          uuid primary key default gen_random_uuid(),
  category_id uuid references crm.service_categories(id) on delete restrict,
  code        text unique not null,
  name        text not null,
  is_active   boolean not null default true,
  sort_order  int not null default 0
);

create table if not exists crm.lost_reasons (
  id          uuid primary key default gen_random_uuid(),
  code        text unique not null,
  name        text not null,
  is_active   boolean not null default true
);

create table if not exists crm.countries (
  code        char(2) primary key,
  name        text not null,
  region      text,
  is_target   boolean not null default false,
  currency    char(3),
  default_tz  text
);

-- ----------------------------------------------------------- campaigns ----
create table if not exists crm.campaigns (
  id          uuid primary key default gen_random_uuid(),
  code        text unique not null,
  name        text not null,
  channel     text,
  started_on  date,
  ended_on    date,
  is_active   boolean not null default true,
  created_at  timestamptz not null default now()
);

-- ------------------------------------------------------- organizations ----
create table if not exists crm.organizations (
  id              uuid primary key default gen_random_uuid(),
  name            text not null,
  normalized_name text generated always as (lower(btrim(name))) stored,
  email_domain    citext,
  website         text,
  country_code    char(2) references crm.countries(code),
  region          text,
  city            text,
  timezone        text,
  industry        text,
  company_size    crm.company_size not null default 'unknown',
  org_type        text,                       -- e.g. contractor, consultant, bim_company
  notes           text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

-- One organization per email domain, but only when a domain is known.
create unique index if not exists organizations_email_domain_key
  on crm.organizations (email_domain) where email_domain is not null;

-- ------------------------------------------------------------ contacts ----
create table if not exists crm.contacts (
  id              uuid primary key default gen_random_uuid(),
  organization_id uuid references crm.organizations(id) on delete set null,
  full_name       text not null,
  email           citext not null,
  phone           text,
  job_title       text,
  linkedin_url    text,
  country_code    char(2) references crm.countries(code),
  timezone        text,
  is_primary      boolean not null default false,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create unique index if not exists contacts_email_key on crm.contacts (email);

-- ------------------------------------------------- public intake table ----
-- Anonymous visitors write here and nowhere else. They cannot reach `leads`
-- directly, so no public request can set a score, an owner or a status.
create table if not exists crm.enquiry_submissions (
  id                uuid primary key default gen_random_uuid(),
  submission_key    uuid not null,              -- client-generated; idempotency
  form_code         text not null,              -- which form was used
  payload           jsonb not null,             -- raw, exactly as submitted
  -- attribution, captured server-side where possible
  source_code       text,
  utm_source        text,
  utm_medium        text,
  utm_campaign      text,
  utm_content       text,
  utm_term          text,
  landing_page      text,
  referrer          text,
  user_agent        text,
  ip_hash           text,                       -- hashed, never the raw address
  -- processing
  processed         boolean not null default false,
  processed_at      timestamptz,
  lead_id           uuid,
  rejection_reason  text,
  created_at        timestamptz not null default now()
);

create unique index if not exists enquiry_submissions_key
  on crm.enquiry_submissions (submission_key);

-- --------------------------------------------------------------- leads ----
create sequence if not exists crm.lead_number_seq start 1000;

create table if not exists crm.leads (
  id                    uuid primary key default gen_random_uuid(),
  lead_number           text unique not null
                        default 'BR-L-' || lpad(nextval('crm.lead_number_seq')::text, 6, '0'),
  organization_id       uuid references crm.organizations(id) on delete set null,
  contact_id            uuid references crm.contacts(id) on delete set null,
  source_id             uuid references crm.lead_sources(id) on delete set null,
  campaign_id           uuid references crm.campaigns(id) on delete set null,
  submission_id         uuid references crm.enquiry_submissions(id) on delete set null,

  -- classification
  lead_type             text,                   -- service_category code
  status                crm.lead_status not null default 'new',
  priority              crm.lead_priority not null default 'normal',
  qualification_status  text,

  -- geography
  country_code          char(2) references crm.countries(code),
  region                text,
  city                  text,
  timezone              text,
  is_international      boolean generated always as
                        (country_code is not null and country_code <> 'IN') stored,

  -- denormalised contact snapshot (what they actually typed, kept verbatim)
  company_name          text,
  contact_name          text,
  email                 citext,
  phone                 text,
  website               text,
  job_title             text,
  industry              text,
  company_size          crm.company_size not null default 'unknown',

  -- requirement
  service_interest      text[],
  disciplines           text[],
  software              text[],
  project_type          text,
  project_location      text,
  project_stage         text,
  required_lod          text,
  required_standards    text[],
  deliverables          text[],
  project_size          text,
  existing_model        boolean,
  team_size_required    int,
  estimated_budget      numeric(14,2),
  currency              char(3),
  project_start_date    date,
  required_delivery_date date,
  message               text,

  -- scoring and ownership
  lead_score            int not null default 0,
  score_band            crm.score_band not null default 'low',
  assigned_to           uuid references crm.app_users(id) on delete set null,
  assigned_at           timestamptz,

  -- lifecycle timestamps
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  first_response_at     timestamptz,
  last_contacted_at     timestamptz,
  next_follow_up_at     timestamptz,
  converted_at          timestamptz,
  lost_at               timestamptz,
  lost_reason_id        uuid references crm.lost_reasons(id) on delete set null,
  duplicate_of          uuid references crm.leads(id) on delete set null,

  constraint leads_score_range check (lead_score between -100 and 200)
);

create table if not exists crm.lead_services (
  lead_id     uuid not null references crm.leads(id) on delete cascade,
  service_id  uuid not null references crm.services(id) on delete cascade,
  primary key (lead_id, service_id)
);

-- --------------------------------------------------- history and events ----
create table if not exists crm.lead_status_history (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references crm.leads(id) on delete cascade,
  from_status   crm.lead_status,
  to_status     crm.lead_status not null,
  changed_by    uuid references crm.app_users(id) on delete set null,
  reason        text,
  changed_at    timestamptz not null default now()
);

create table if not exists crm.lead_score_history (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references crm.leads(id) on delete cascade,
  previous_score int,
  new_score     int not null,
  previous_band crm.score_band,
  new_band      crm.score_band not null,
  breakdown     jsonb not null,   -- every rule that fired, and why
  computed_by   text not null default 'engine',
  computed_at   timestamptz not null default now()
);

create table if not exists crm.lead_assignments (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references crm.leads(id) on delete cascade,
  assigned_to   uuid references crm.app_users(id) on delete set null,
  assigned_by   uuid references crm.app_users(id) on delete set null,
  rule_code     text,
  reason        text,
  assigned_at   timestamptz not null default now()
);

create table if not exists crm.activities (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid references crm.leads(id) on delete cascade,
  organization_id uuid references crm.organizations(id) on delete cascade,
  actor_id      uuid references crm.app_users(id) on delete set null,
  activity_type text not null,        -- lead_created, scored, assigned, note_added…
  summary       text not null,
  detail        jsonb,
  occurred_at   timestamptz not null default now()
);

create table if not exists crm.lead_notes (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references crm.leads(id) on delete cascade,
  author_id     uuid references crm.app_users(id) on delete set null,
  body          text not null,
  is_internal   boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create table if not exists crm.lead_tasks (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid not null references crm.leads(id) on delete cascade,
  title         text not null,
  detail        text,
  owner_id      uuid references crm.app_users(id) on delete set null,
  due_at        timestamptz not null,
  status        crm.task_status not null default 'pending',
  priority      crm.lead_priority not null default 'normal',
  completed_at  timestamptz,
  created_by    uuid references crm.app_users(id) on delete set null,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create table if not exists crm.communications (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid references crm.leads(id) on delete cascade,
  contact_id    uuid references crm.contacts(id) on delete set null,
  direction     crm.comm_direction not null,
  channel       crm.comm_channel not null,
  subject       text,
  body          text,
  actor_id      uuid references crm.app_users(id) on delete set null,
  provider_id   text,                 -- id returned by the sending provider
  delivered     boolean,              -- only true when the provider confirmed
  occurred_at   timestamptz not null default now(),
  created_at    timestamptz not null default now()
);

create table if not exists crm.attachments (
  id            uuid primary key default gen_random_uuid(),
  lead_id       uuid references crm.leads(id) on delete cascade,
  project_id    uuid,
  storage_path  text not null unique,  -- private bucket key
  file_name     text not null,
  mime_type     text not null,
  byte_size     bigint not null,
  checksum      text,
  scan_status   text not null default 'pending',   -- pending|clean|infected|skipped
  uploaded_by   uuid references crm.app_users(id) on delete set null,
  uploaded_at   timestamptz not null default now(),
  constraint attachments_size_limit check (byte_size <= 52428800)  -- 50 MB
);

-- ------------------------------------------------- proposals & projects ----
create sequence if not exists crm.proposal_number_seq start 100;

create table if not exists crm.proposals (
  id              uuid primary key default gen_random_uuid(),
  proposal_number text unique not null
                  default 'BR-P-' || lpad(nextval('crm.proposal_number_seq')::text, 5, '0'),
  lead_id         uuid references crm.leads(id) on delete set null,
  organization_id uuid references crm.organizations(id) on delete set null,
  project_id      uuid,
  version         int not null default 1,
  status          crm.proposal_status not null default 'draft',
  currency        char(3) not null default 'INR',
  subtotal        numeric(14,2) not null default 0,
  discount        numeric(14,2) not null default 0,
  tax             numeric(14,2) not null default 0,
  total           numeric(14,2) generated always as (subtotal - discount + tax) stored,
  valid_until     date,
  sent_at         timestamptz,
  decided_at      timestamptz,
  created_by      uuid references crm.app_users(id) on delete set null,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create table if not exists crm.proposal_items (
  id            uuid primary key default gen_random_uuid(),
  proposal_id   uuid not null references crm.proposals(id) on delete cascade,
  service_id    uuid references crm.services(id) on delete set null,
  description   text not null,
  quantity      numeric(12,2) not null default 1,
  unit          text,
  unit_price    numeric(14,2) not null default 0,
  line_total    numeric(14,2) generated always as (quantity * unit_price) stored,
  sort_order    int not null default 0
);

create sequence if not exists crm.project_number_seq start 100;

create table if not exists crm.projects (
  id              uuid primary key default gen_random_uuid(),
  project_number  text unique not null
                  default 'BR-J-' || lpad(nextval('crm.project_number_seq')::text, 5, '0'),
  organization_id uuid references crm.organizations(id) on delete restrict,
  primary_contact_id uuid references crm.contacts(id) on delete set null,
  lead_id         uuid references crm.leads(id) on delete set null,
  proposal_id     uuid references crm.proposals(id) on delete set null,
  name            text not null,
  status          crm.project_status not null default 'planned',
  disciplines     text[],
  deliverables    text[],
  scope_summary   text,
  contract_value  numeric(14,2),
  currency        char(3) default 'INR',
  start_date      date,
  end_date        date,
  manager_id      uuid references crm.app_users(id) on delete set null,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

-- ------------------------------------------------------- configuration ----
create table if not exists crm.lead_scoring_rules (
  id            uuid primary key default gen_random_uuid(),
  code          text unique not null,
  label         text not null,
  points        int not null,
  -- Declarative condition, evaluated by crm.fn_score_lead. Kept as data so the
  -- business can retune scoring without a code deploy.
  field         text not null,
  operator      text not null,   -- present|absent|eq|neq|gt|gte|lt|lte|in|contains|matches
  value         text,
  is_active     boolean not null default true,
  sort_order    int not null default 0,
  constraint scoring_operator_valid check (operator in
    ('present','absent','eq','neq','gt','gte','lt','lte','in','contains','matches'))
);

create table if not exists crm.lead_routing_rules (
  id            uuid primary key default gen_random_uuid(),
  code          text unique not null,
  label         text not null,
  priority      int not null default 100,   -- lower runs first
  match_lead_type    text,
  match_country_in   text[],
  match_international boolean,
  match_min_score    int,
  assign_to_role     crm.app_role,
  assign_to_user     uuid references crm.app_users(id) on delete set null,
  set_priority       crm.lead_priority,
  is_active     boolean not null default true
);

create table if not exists crm.app_settings (
  key           text primary key,
  value         jsonb not null,
  description   text,
  updated_at    timestamptz not null default now()
);

-- ----------------------------------------------------------- audit log ----
create table if not exists crm.audit_logs (
  id            bigserial primary key,
  table_name    text not null,
  record_id     text not null,
  action        text not null,       -- INSERT | UPDATE | DELETE
  actor_id      uuid,
  changed_fields text[],
  old_values    jsonb,
  new_values    jsonb,
  occurred_at   timestamptz not null default now()
);

-- ------------------------------------------------------------- indexes ----
-- Chosen for the queries the CRM actually runs: pipeline board, my-leads,
-- follow-ups due, dashboard counters and dedupe lookups.
create index if not exists leads_status_idx           on crm.leads (status);
create index if not exists leads_assigned_status_idx  on crm.leads (assigned_to, status);
create index if not exists leads_created_at_idx       on crm.leads (created_at desc);
create index if not exists leads_score_idx            on crm.leads (lead_score desc);
create index if not exists leads_country_idx          on crm.leads (country_code);
create index if not exists leads_international_idx    on crm.leads (is_international);
create index if not exists leads_org_idx              on crm.leads (organization_id);
create index if not exists leads_contact_idx          on crm.leads (contact_id);
create index if not exists leads_source_idx           on crm.leads (source_id);
create index if not exists leads_type_idx             on crm.leads (lead_type);
create index if not exists leads_email_idx            on crm.leads (email);
-- Partial: the follow-up queue only ever looks at leads that are still open.
create index if not exists leads_followup_due_idx     on crm.leads (next_follow_up_at)
  where next_follow_up_at is not null
    and status not in ('won','lost','spam','duplicate','not_qualified');

create index if not exists activities_lead_time_idx   on crm.activities (lead_id, occurred_at desc);
create index if not exists notes_lead_idx             on crm.lead_notes (lead_id, created_at desc);
create index if not exists tasks_owner_due_idx        on crm.lead_tasks (owner_id, due_at)
  where status = 'pending';
create index if not exists tasks_lead_idx             on crm.lead_tasks (lead_id);
create index if not exists comms_lead_time_idx        on crm.communications (lead_id, occurred_at desc);
create index if not exists status_hist_lead_idx       on crm.lead_status_history (lead_id, changed_at desc);
create index if not exists score_hist_lead_idx        on crm.lead_score_history (lead_id, computed_at desc);
create index if not exists submissions_unprocessed_idx on crm.enquiry_submissions (created_at)
  where processed = false;
create index if not exists contacts_org_idx           on crm.contacts (organization_id);
create index if not exists audit_record_idx           on crm.audit_logs (table_name, record_id, occurred_at desc);
create index if not exists attachments_lead_idx       on crm.attachments (lead_id);
create index if not exists proposals_lead_idx         on crm.proposals (lead_id);
create index if not exists projects_org_idx           on crm.projects (organization_id);
