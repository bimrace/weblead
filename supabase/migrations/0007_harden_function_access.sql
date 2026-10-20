-- ============================================================================
-- BIMRACE Lead Engine — 0007 harden function access (Supabase advisor findings)
--
-- crm.fn_find_duplicate(email, phone) is SECURITY DEFINER and was executable by
-- anon through /rest/v1/rpc/fn_find_duplicate. Given an email it returns the
-- matching lead id, which lets anyone test whether an address is in the CRM.
-- It is only ever called from inside crm.fn_process_submission (itself SECURITY
-- DEFINER, running as the owner), so no client role needs EXECUTE on it.
--
-- crm.fn_touch_updated_at had a role-mutable search_path.
-- Idempotent: REVOKE and ALTER FUNCTION ... SET are safe to re-run.
-- ============================================================================

revoke execute on function crm.fn_find_duplicate(citext, text) from public, anon, authenticated;

alter function crm.fn_touch_updated_at() set search_path = crm, public;
