-- ============================================================================
-- BIMRACE Lead Engine — 0008 edge-function-only public access
--
-- Until now the publishable (anon) key could INSERT into
-- crm.enquiry_submissions and upload to the enquiry-files bucket directly,
-- which bypassed the lead-intake Edge Function's rate limiting, honeypot,
-- size limit and IP hashing. The website now sends every submission through
-- Edge Functions, which write with server-side credentials.
--
-- After this migration the anon role holds no privileges on the crm schema
-- and no storage write policy. Authenticated staff access is unchanged
-- (policies in 0003 / 0005). Idempotent: REVOKE and DROP POLICY IF EXISTS.
-- ============================================================================

-- Direct table access for anonymous callers: none.
revoke insert on crm.enquiry_submissions from anon;
revoke usage, select on sequence crm.lead_number_seq from anon;
revoke select on crm.service_categories, crm.services, crm.countries from anon;
revoke all on all tables in schema crm from anon;
revoke all on all sequences in schema crm from anon;
revoke all on all functions in schema crm from anon;
revoke usage on schema crm from anon;

-- Keep future objects closed to anon by default.
alter default privileges in schema crm revoke all on tables from anon;
alter default privileges in schema crm revoke all on sequences from anon;
alter default privileges in schema crm revoke execute on functions from anon;

drop policy if exists anon_insert_submission on crm.enquiry_submissions;

-- Direct storage uploads for anonymous callers: none. Files will be uploaded
-- through a signed upload URL issued by an Edge Function instead.
drop policy if exists "anon upload enquiry files" on storage.objects;
