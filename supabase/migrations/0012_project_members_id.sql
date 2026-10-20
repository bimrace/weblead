-- ============================================================================
-- BIMRACE Lead Engine — 0012 project_members gets an id
--
-- crm.fn_audit records each changed row's "id" in audit_logs.record_id (NOT
-- NULL). project_members used a composite key (project_id, user_id) and had
-- no id, so every team change failed and rolled back. Found by the portal
-- end-to-end test. The composite primary key is unchanged; id is an extra
-- unique identifier. Idempotent.
-- ============================================================================
alter table crm.project_members add column if not exists id uuid not null default gen_random_uuid();
do $$ begin
  alter table crm.project_members add constraint project_members_id_key unique (id);
exception when duplicate_object or duplicate_table then null; end $$;
