// ============================================================================
// BIMRACE — staff-admin Edge Function (portal user management)
//
// Admin-only operations that need the secret key, which must never reach a
// browser:
//   list_users                       -> staff with role, status, last sign-in
//   create_user  {email, full_name, role}   -> temporary password (shown once)
//   set_role     {user_id, role}
//   set_active   {user_id, active}
//   reset_password {user_id}         -> new temporary password (shown once)
//
// No email is required: Supabase's built-in mailer only reaches project team
// members, so accounts are created with a temporary password that the admin
// shares privately. The portal forces a password change on first sign-in.
//
// Security: deployed WITH JWT verification. The caller's token is resolved to
// a user and must belong to an active crm.app_users admin. Every change is
// written to crm.audit_logs by the table triggers.
// ============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const ROLES = ["admin", "sales", "business_development", "project_manager",
               "bim_manager", "engineer", "viewer"];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

const allowed = (Deno.env.get("PORTAL_ORIGINS") ??
                 "https://portal.bimrace.com,http://localhost:3200")
  .split(",").map((o) => o.trim()).filter(Boolean);

function corsFor(req: Request) {
  const origin = req.headers.get("origin") ?? "";
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

const responder = (cors: Record<string, string>) => (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "content-type": "application/json" } });

function tempPassword() {
  const alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#%*";
  const bytes = crypto.getRandomValues(new Uint8Array(18));
  return Array.from(bytes, (b) => alphabet[b % alphabet.length]).join("");
}

Deno.serve(async (req) => {
  const cors = corsFor(req);
  const json = responder(cors);
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } });
  const crm = db.schema("crm");

  // ---- who is calling? ------------------------------------------------------
  const token = (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
  const { data: who, error: whoErr } = await db.auth.getUser(token);
  if (whoErr || !who?.user) return json({ error: "not_authenticated" }, 401);
  const { data: me } = await crm.from("app_users").select("id, role, is_active")
    .eq("id", who.user.id).maybeSingle();
  if (!me || !me.is_active || me.role !== "admin") return json({ error: "forbidden" }, 403);

  try {
    const body = await req.json();
    const action = String(body.action ?? "");

    if (action === "list_users") {
      const { data: staff, error } = await crm.from("app_users")
        .select("id, email, full_name, role, is_active, created_at").order("created_at");
      if (error) throw error;
      const { data: authUsers } = await db.auth.admin.listUsers({ perPage: 1000 });
      const seen = new Map((authUsers?.users ?? []).map((u) => [u.id, u.last_sign_in_at]));
      return json({ users: (staff ?? []).map((s) => ({ ...s, last_sign_in_at: seen.get(s.id) ?? null })) });
    }

    if (action === "create_user") {
      const email = String(body.email ?? "").trim().toLowerCase();
      const full_name = String(body.full_name ?? "").trim().slice(0, 120);
      const role = String(body.role ?? "");
      if (!EMAIL_RE.test(email) || full_name.length < 2 || !ROLES.includes(role)) {
        return json({ error: "invalid_input" }, 400);
      }
      const password = tempPassword();
      const { data: created, error } = await db.auth.admin.createUser({
        email, password, email_confirm: true,
        user_metadata: { full_name, must_change_password: true },
      });
      if (error || !created?.user) {
        return json({ error: /already/i.test(error?.message ?? "") ? "email_exists" : "create_failed" }, 409);
      }
      const { error: insErr } = await crm.from("app_users")
        .insert({ id: created.user.id, email, full_name, role });
      if (insErr) {
        await db.auth.admin.deleteUser(created.user.id);          // keep auth and CRM in step
        return json({ error: "create_failed" }, 500);
      }
      return json({ ok: true, user_id: created.user.id, temporary_password: password });
    }

    const userId = String(body.user_id ?? "");
    if (!/^[0-9a-f-]{36}$/i.test(userId)) return json({ error: "invalid_input" }, 400);
    if (userId === me.id && action !== "reset_password") {
      return json({ error: "cannot_change_own_access" }, 400);   // avoid locking out the last admin
    }

    if (action === "set_role") {
      const role = String(body.role ?? "");
      if (!ROLES.includes(role)) return json({ error: "invalid_input" }, 400);
      const { error } = await crm.from("app_users").update({ role }).eq("id", userId);
      if (error) throw error;
      return json({ ok: true });
    }

    if (action === "set_active") {
      const active = body.active === true;
      const { error } = await crm.from("app_users").update({ is_active: active }).eq("id", userId);
      if (error) throw error;
      // A deactivated user is also banned at the auth layer, so existing
      // sessions cannot refresh.
      await db.auth.admin.updateUserById(userId, { ban_duration: active ? "none" : "876000h" });
      return json({ ok: true });
    }

    if (action === "reset_password") {
      const password = tempPassword();
      const { data: u } = await db.auth.admin.getUserById(userId);
      const { error } = await db.auth.admin.updateUserById(userId, {
        password, user_metadata: { ...(u?.user?.user_metadata ?? {}), must_change_password: true },
      });
      if (error) throw error;
      return json({ ok: true, temporary_password: password });
    }

    return json({ error: "unknown_action" }, 400);
  } catch (err) {
    console.error("staff_admin_failed", err);
    return json({ error: "unexpected_error" }, 500);
  }
});
