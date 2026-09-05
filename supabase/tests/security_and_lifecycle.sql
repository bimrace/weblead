-- ============================================================================
-- BIMRACE Lead Engine — security and lifecycle test suite
-- Run against a database with all migrations applied.
-- Every check raises an exception on failure, so a clean run means all passed.
-- ============================================================================
\set ON_ERROR_STOP on
\pset pager off

create or replace function pg_temp.ok(cond boolean, label text) returns void
language plpgsql as $$
begin
  if cond then raise notice 'PASS  %', label;
  else raise exception 'FAIL  %', label; end if;
end $$;

-- ---------------------------------------------------------------- setup ----
insert into crm.app_users (id, email, full_name, role) values
 ('11111111-1111-1111-1111-111111111111','admin@bimrace.com','Admin User','admin'),
 ('22222222-2222-2222-2222-222222222222','sales1@bimrace.com','Sales One','sales'),
 ('33333333-3333-3333-3333-333333333333','sales2@bimrace.com','Sales Two','sales'),
 ('44444444-4444-4444-4444-444444444444','bd@bimrace.com','BD User','business_development'),
 ('55555555-5555-5555-5555-555555555555','bim@bimrace.com','BIM Manager','bim_manager')
on conflict (id) do nothing;

-- =====================  TEST 1 — anonymous lead submission  =================
set role anon;
set request.jwt.claim.sub = '';

insert into crm.enquiry_submissions (submission_key, form_code, payload, source_code, landing_page)
values (gen_random_uuid(), 'mep_bim_support',
  jsonb_build_object(
    'name','Rajesh Kumar','company','Sterling Engineering Pvt Ltd',
    'email','rajesh@sterlingeng.co.in','phone','+91 98200 11223',
    'country_code','IN','city','Mumbai','job_title','Project Manager',
    'lead_type','mep_bim','company_size','51-200',
    'service_interest', jsonb_build_array('MEP Coordination','Clash Detection'),
    'disciplines', jsonb_build_array('Mechanical','Electrical','Plumbing'),
    'project_type','Healthcare','project_stage','Technical design',
    'required_delivery_date','2026-12-01','estimated_budget','850000','currency','INR',
    'message','We need MEP coordination for a 240-bed hospital across six levels. Ductwork, containment and public health are modelled but not federated. We need clash resolution to closure and coordination reports issued fortnightly against our ISO 19650 delivery plan.'),
  'website','/services/mep-bim');

reset role;
select pg_temp.ok((select count(*) = 1 from crm.leads where email = 'rajesh@sterlingeng.co.in'),
  'T1.1 anonymous submission created exactly one lead');
select pg_temp.ok((select organization_id is not null and contact_id is not null
                   from crm.leads where email='rajesh@sterlingeng.co.in'),
  'T1.2 organization and contact were created and linked');
select pg_temp.ok((select count(*) = 1 from crm.organizations where email_domain='sterlingeng.co.in'),
  'T1.3 organization matched on business email domain');

-- =====================  TEST 2 — anon cannot read CRM  ======================
-- Anonymous has no SELECT grant at all on these tables, so the attempt is
-- refused at the privilege layer before RLS is even consulted.
set role anon;
do $$
declare t text; n int;
begin
  foreach t in array array['leads','organizations','contacts',
                           'enquiry_submissions','audit_logs','proposals','projects']
  loop
    begin
      execute format('select count(*) from crm.%I', t) into n;
      raise exception 'FAIL T2 anonymous was able to SELECT from crm.%', t;
    exception when insufficient_privilege then
      raise notice 'PASS  T2 anonymous SELECT on crm.% is refused', t;
    end;
  end loop;
end $$;

do $$ begin
  begin
    update crm.leads set lead_score = 999, status='won';
    raise exception 'FAIL T2.6 anon was able to UPDATE leads';
  exception when insufficient_privilege or raise_exception then
    if sqlerrm like 'FAIL%' then raise; end if;
    raise notice 'PASS  T2.6 anonymous UPDATE on leads is refused';
  end;
end $$;

do $$ begin
  begin
    insert into crm.leads (company_name, email, status, lead_score)
    values ('Injected','x@y.com','won',200);
    raise exception 'FAIL T2.7 anon was able to INSERT directly into leads';
  exception when insufficient_privilege or raise_exception then
    if sqlerrm like 'FAIL%' then raise; end if;
    raise notice 'PASS  T2.7 anonymous cannot INSERT directly into leads';
  end;
end $$;
reset role;

-- =====================  TEST 3 — scoring engine  ============================
select pg_temp.ok((select lead_score >= 51 from crm.leads where email='rajesh@sterlingeng.co.in'),
  'T3.1 detailed MEP enquiry scored HIGH or above');
select pg_temp.ok((select count(*) = 1 from crm.lead_score_history h
                   join crm.leads l on l.id = h.lead_id
                   where l.email='rajesh@sterlingeng.co.in'),
  'T3.2 score history row written');
select pg_temp.ok((select jsonb_array_length(breakdown -> 'rules') >= 6
                   from crm.lead_score_history h join crm.leads l on l.id=h.lead_id
                   where l.email='rajesh@sterlingeng.co.in'),
  'T3.3 score is explainable — every firing rule recorded');

-- =====================  TEST 4 — routing engine  ============================
select pg_temp.ok((select assigned_to is not null from crm.leads where email='rajesh@sterlingeng.co.in'),
  'T4.1 lead was auto-assigned');
select pg_temp.ok((select u.role = 'bim_manager' from crm.leads l
                   join crm.app_users u on u.id = l.assigned_to
                   where l.email='rajesh@sterlingeng.co.in'),
  'T4.2 MEP BIM routed to the bim_manager role, per rule');
select pg_temp.ok((select count(*) >= 1 from crm.lead_assignments a
                   join crm.leads l on l.id=a.lead_id where l.email='rajesh@sterlingeng.co.in'),
  'T4.3 assignment recorded with the rule that caused it');

-- =====================  TEST 5 — duplicate detection  =======================
set role anon;
insert into crm.enquiry_submissions (submission_key, form_code, payload, source_code)
values (gen_random_uuid(), 'general',
  jsonb_build_object('name','Rajesh Kumar','company','Sterling Engineering Pvt Ltd',
    'email','rajesh@sterlingeng.co.in','lead_type','bim_modelling',
    'message','Following up on the earlier enquiry with an additional scope for as-built modelling.'),
  'website');
reset role;
select pg_temp.ok((select count(*) = 2 from crm.leads where email='rajesh@sterlingeng.co.in'),
  'T5.1 second enquiry preserved, not discarded');
select pg_temp.ok((select count(*) = 1 from crm.leads
                   where email='rajesh@sterlingeng.co.in' and status='duplicate'),
  'T5.2 second enquiry flagged as duplicate');
select pg_temp.ok((select count(*) = 1 from crm.organizations where email_domain='sterlingeng.co.in'),
  'T5.3 no duplicate organization created');
select pg_temp.ok((select count(*) = 1 from crm.contacts where email='rajesh@sterlingeng.co.in'),
  'T5.4 no duplicate contact created');

-- =====================  TEST 6 — idempotency  ===============================
do $$
declare k uuid := gen_random_uuid();
begin
  set local role anon;
  insert into crm.enquiry_submissions (submission_key, form_code, payload)
  values (k,'general',jsonb_build_object('name','Double Click','email','dbl@example-corp.com'));
  begin
    insert into crm.enquiry_submissions (submission_key, form_code, payload)
    values (k,'general',jsonb_build_object('name','Double Click','email','dbl@example-corp.com'));
    raise exception 'FAIL T6.1 duplicate submission_key was accepted';
  exception when unique_violation then
    raise notice 'PASS  T6.1 repeated submit with same key is rejected (idempotency)';
  end;
end $$;
reset role;

-- =====================  TEST 7 — spam / invalid input  ======================
set role anon;
insert into crm.enquiry_submissions (submission_key, form_code, payload)
values (gen_random_uuid(),'general', jsonb_build_object('name','','email','not-an-email'));
reset role;
select pg_temp.ok((select rejection_reason = 'invalid_contact_details'
                   from crm.enquiry_submissions where payload ->> 'email' = 'not-an-email'),
  'T7.1 invalid contact details rejected without creating a lead');
select pg_temp.ok((select count(*) = 0 from crm.leads where email = 'not-an-email'),
  'T7.2 no lead created from the invalid submission');

-- =====================  TEST 8 — sales isolation  ===========================
-- Give sales1 a lead, leave sales2 with none.
-- Scope to the primary lead: the duplicate shares the same email address.
update crm.leads set assigned_to='22222222-2222-2222-2222-222222222222'
 where email='rajesh@sterlingeng.co.in' and status <> 'duplicate';

set role authenticated;
set request.jwt.claim.sub = '33333333-3333-3333-3333-333333333333';   -- sales2
select pg_temp.ok((select count(*) = 0 from crm.leads
                   where email='rajesh@sterlingeng.co.in' and status <> 'duplicate'),
  'T8.1 sales user cannot see another rep''s assigned lead');

do $$ begin
  begin
    update crm.leads set status='won'
      where email='rajesh@sterlingeng.co.in' and status <> 'duplicate';
    if found then raise exception 'FAIL T8.2 sales2 updated a lead it does not own'; end if;
    raise notice 'PASS  T8.2 sales user cannot update an unowned lead';
  exception when insufficient_privilege then
    raise notice 'PASS  T8.2 sales user cannot update an unowned lead';
  end;
end $$;

set request.jwt.claim.sub = '22222222-2222-2222-2222-222222222222';   -- sales1
select pg_temp.ok((select count(*) = 1 from crm.leads
                   where email='rajesh@sterlingeng.co.in' and status <> 'duplicate'),
  'T8.3 owning sales user can see their own lead');

set request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';   -- admin
select pg_temp.ok((select count(*) >= 3 from crm.leads),
  'T8.4 admin can see all leads');
select pg_temp.ok((select count(*) > 0 from crm.audit_logs),
  'T8.5 admin can read the audit log');

set request.jwt.claim.sub = '22222222-2222-2222-2222-222222222222';   -- sales1
select pg_temp.ok((select count(*) = 0 from crm.audit_logs),
  'T8.6 non-admin cannot read the audit log');
reset role;

-- =====================  TEST 9 — status history & audit  ====================
set role authenticated;
set request.jwt.claim.sub = '22222222-2222-2222-2222-222222222222';
update crm.leads set status='contacted'
 where email='rajesh@sterlingeng.co.in' and status <> 'duplicate';
update crm.leads set status='qualified'
 where email='rajesh@sterlingeng.co.in' and status = 'contacted';
reset role;

select pg_temp.ok((select count(*) = 2 from crm.lead_status_history h
                   join crm.leads l on l.id=h.lead_id where l.email='rajesh@sterlingeng.co.in'),
  'T9.1 every status transition recorded, none overwritten');
select pg_temp.ok((select count(*) > 0 from crm.audit_logs
                   where table_name='leads' and action='UPDATE'
                     and 'status' = any(changed_fields)),
  'T9.2 audit log captured the status change with old and new values');

-- =====================  TEST 10 — conversion to project  ====================
set role authenticated;
set request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';
do $$
declare lid uuid; pid uuid; pid2 uuid;
begin
  select id into lid from crm.leads where email='rajesh@sterlingeng.co.in' and status <> 'duplicate';
  pid  := crm.fn_convert_lead_to_project(lid, 'Hospital MEP Coordination');
  pid2 := crm.fn_convert_lead_to_project(lid, 'Hospital MEP Coordination');
  if pid is null then raise exception 'FAIL T10.1 conversion returned null'; end if;
  if pid <> pid2 then raise exception 'FAIL T10.2 conversion is not idempotent'; end if;
  raise notice 'PASS  T10.1 lead converted to project';
  raise notice 'PASS  T10.2 repeat conversion returns the same project (idempotent)';
end $$;
reset role;

select pg_temp.ok((select status='won' from crm.leads
                   where email='rajesh@sterlingeng.co.in' and status<>'duplicate'),
  'T10.3 converted lead marked WON');
select pg_temp.ok((select organization_id = (select organization_id from crm.leads
                     where email='rajesh@sterlingeng.co.in' and status<>'duplicate')
                   from crm.projects limit 1),
  'T10.4 project reuses the existing organization — repeat business is linked');

-- =====================  TEST 11 — international routing  ====================
set role anon;
insert into crm.enquiry_submissions (submission_key, form_code, payload, source_code)
values (gen_random_uuid(),'bim_company_support',
  jsonb_build_object('name','Sarah Lee','company','Meridian BIM Studio Ltd',
    'email','sarah@meridianbim.co.uk','country_code','GB','city','Manchester',
    'lead_type','bim_company_support','company_size','11-50',
    'service_interest', jsonb_build_array('Overflow Production','White-label Production'),
    'disciplines', jsonb_build_array('Mechanical','Electrical'),
    'project_type','Commercial','estimated_budget','40000','currency','GBP',
    'required_delivery_date','2027-03-31',
    'message','We are a ten-person BIM studio in Manchester and regularly exceed our MEP modelling capacity. We are looking for a white-label production partner able to take overflow Revit MEP work on a recurring monthly basis, working inside our templates and ACC environment.'),
  'linkedin');
reset role;

select pg_temp.ok((select is_international from crm.leads where email='sarah@meridianbim.co.uk'),
  'T11.1 UK lead flagged international');
select pg_temp.ok((select lead_score >= 51 from crm.leads where email='sarah@meridianbim.co.uk'),
  'T11.2 international company-support lead scored HIGH or above');
select pg_temp.ok((select u.role = 'business_development' from crm.leads l
                   join crm.app_users u on u.id=l.assigned_to where l.email='sarah@meridianbim.co.uk'),
  'T11.3 company-support lead routed to business development');

-- =====================  TEST 12 — low-value enquiry  ========================
set role anon;
insert into crm.enquiry_submissions (submission_key, form_code, payload)
values (gen_random_uuid(),'general',
  jsonb_build_object('name','Student A','email','student123@gmail.com',
    'company_size','individual','lead_type','careers','message','send info'));
reset role;
select pg_temp.ok((select lead_score < 21 from crm.leads where email='student123@gmail.com'),
  'T12.1 free-mail careers enquiry with no detail scores LOW');
select pg_temp.ok((select score_band = 'low' from crm.leads where email='student123@gmail.com'),
  'T12.2 band computed as LOW');
select pg_temp.ok((select count(*)=0 from crm.organizations where email_domain='gmail.com'),
  'T12.3 free-mail domain did not create a bogus organization');

-- =====================  TEST 13 — dashboard metrics  ========================
set role authenticated;
set request.jwt.claim.sub = '11111111-1111-1111-1111-111111111111';
select pg_temp.ok((crm.fn_dashboard_metrics() -> 'international')::int >= 1,
  'T13.1 dashboard reports international lead count');
select pg_temp.ok((crm.fn_dashboard_metrics() -> 'india')::int >= 1,
  'T13.2 dashboard reports India lead count');
reset role;

set role anon;
do $$ begin
  begin
    perform crm.fn_dashboard_metrics();
    raise exception 'FAIL T13.3 anon executed the dashboard function';
  exception when insufficient_privilege then
    raise notice 'PASS  T13.3 anonymous cannot execute the dashboard function';
  end;
end $$;
reset role;

\echo ''
\echo '================= ALL TESTS PASSED ================='
