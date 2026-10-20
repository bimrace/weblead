// ============================================================================
// BIMRACE — lead-intake Edge Function
//
// Optional hardened entry point in front of crm.enquiry_submissions. The site
// works without it (anon INSERT + RLS is already safe), but routing traffic
// through here adds rate limiting, payload size limits, Turnstile verification
// and IP hashing, none of which a browser can be trusted to do.
//
// Deploy:  supabase functions deploy lead-intake --no-verify-jwt
// Secrets: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, TURNSTILE_SECRET (optional)
// ============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const MAX_BYTES = 24_000;
const WINDOW_MS = 60 * 60 * 1000;   // 1 hour
const MAX_PER_IP = 5;

const hits = new Map<string, number[]>();

// ALLOWED_ORIGINS is a comma-separated list (e.g. "https://bimrace.com,https://www.bimrace.com")
// because the site answers on both hosts. ALLOWED_ORIGIN (single value) is still honoured.
// Unset means "*", which is how local testing works.
const allowed = (Deno.env.get("ALLOWED_ORIGINS") ?? Deno.env.get("ALLOWED_ORIGIN") ?? "*")
  .split(",").map((o) => o.trim()).filter(Boolean);

function corsFor(req: Request) {
  const origin = req.headers.get("origin") ?? "";
  const allowOrigin = allowed.includes("*") ? "*" : allowed.includes(origin) ? origin : allowed[0];
  return {
    "Access-Control-Allow-Origin": allowOrigin,
    // lead-capture.js sends Authorization (the publishable key); browsers refuse
    // the request unless the preflight explicitly allows that header.
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

// Per-request: headers are built from this request's Origin, never shared state,
// so concurrent requests cannot see each other's CORS headers.
const responder = (cors: Record<string, string>) => (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "content-type": "application/json" },
  });

async function sha256(text: string) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function rateLimited(ip: string) {
  const now = Date.now();
  const list = (hits.get(ip) ?? []).filter((t) => now - t < WINDOW_MS);
  list.push(now);
  hits.set(ip, list);
  return list.length > MAX_PER_IP;
}

async function turnstileOk(token: string | undefined, ip: string) {
  const secret = Deno.env.get("TURNSTILE_SECRET");
  if (!secret) return true;               // not configured — skip
  if (!token) return false;
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  body.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify",
    { method: "POST", body });
  const d = await r.json();
  return d.success === true;
}

const BUCKET = "enquiry-files";
const MAX_ATTACHMENTS = 5;

// deno-lint-ignore no-explicit-any
async function linkAttachments(db: any, key: string, submissionId: string, items: unknown[]) {
  const prefix = `incoming/${key}`;
  const { data: sub } = await db.schema("crm").from("enquiry_submissions")
    .select("lead_id").eq("id", submissionId).single();
  const leadId = sub?.lead_id ?? null;          // null when the submission was rejected
  if (!leadId) return 0;

  const { data: objects, error } = await db.storage.from(BUCKET).list(prefix, { limit: 50 });
  if (error || !objects) { console.error("attachment_list_failed", error); return 0; }
  // deno-lint-ignore no-explicit-any
  const byName = new Map<string, any>(objects.map((o: any) => [o.name, o]));

  let linked = 0;
  for (const item of items) {
    // deno-lint-ignore no-explicit-any
    const path = typeof (item as any)?.path === "string" ? (item as any).path : "";
    if (!path.startsWith(prefix + "/") || path.includes("..")) continue;
    const obj = byName.get(path.slice(prefix.length + 1));
    if (!obj) continue;                          // never uploaded
    const size = Number(obj.metadata?.size ?? 0);
    if (!size || size > 52428800) continue;
    const { error: insErr } = await db.schema("crm").from("attachments").insert({
      lead_id: leadId,
      storage_path: path,
      file_name: String((item as any).file_name ?? obj.name).slice(0, 200),
      mime_type: String(obj.metadata?.mimetype ?? "application/octet-stream"),
      byte_size: size,
    });
    if (insErr && insErr.code !== "23505") console.error("attachment_insert_failed", insErr);
    else linked++;
  }
  return linked;
}

Deno.serve(async (req) => {
  const cors = corsFor(req);
  const json = responder(cors);
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";

  try {
    const raw = await req.text();
    if (raw.length > MAX_BYTES) return json({ error: "payload_too_large" }, 413);
    if (rateLimited(ip)) return json({ error: "rate_limited" }, 429);

    const body = JSON.parse(raw);
    const { submission_key, form_code, payload, turnstile_token, attachments, ...attribution } = body;

    if (!submission_key || !form_code || typeof payload !== "object") {
      return json({ error: "invalid_request" }, 400);
    }
    // Honeypot: a real browser leaves this empty.
    if (payload.company_website_hp) return json({ ok: true, id: null });

    if (!(await turnstileOk(turnstile_token, ip))) {
      return json({ error: "verification_failed" }, 403);
    }

    // service_role is used ONLY here, server-side. It never reaches the browser.
    const db = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
      { auth: { persistSession: false } },
    );

    const { data, error } = await db
      .schema("crm")
      .from("enquiry_submissions")
      .insert({
        submission_key,
        form_code,
        payload,
        source_code: attribution.source_code ?? "website",
        utm_source: attribution.utm_source ?? null,
        utm_medium: attribution.utm_medium ?? null,
        utm_campaign: attribution.utm_campaign ?? null,
        utm_content: attribution.utm_content ?? null,
        utm_term: attribution.utm_term ?? null,
        landing_page: attribution.landing_page ?? null,
        referrer: attribution.referrer ?? null,
        user_agent: req.headers.get("user-agent")?.slice(0, 400) ?? null,
        ip_hash: await sha256(ip + (Deno.env.get("IP_SALT") ?? "bimrace")),
      })
      .select("id")
      .single();

    if (error) {
      // 23505 = unique_violation on submission_key: the same submit arrived
      // twice. Treat as success so a double click never shows an error.
      if (error.code === "23505") return json({ ok: true, duplicate: true });
      console.error("intake_insert_failed", error);
      return json({ error: "storage_failed" }, 500);   // never leak DB detail
    }

    // Link files uploaded through lead-upload. Only paths inside this
    // submission's own folder are accepted, each must exist in storage, and
    // size and type come from storage metadata rather than from the browser.
    let linked = 0;
    if (Array.isArray(attachments) && attachments.length) {
      linked = await linkAttachments(db, String(submission_key).toLowerCase(), data.id,
                                     attachments.slice(0, MAX_ATTACHMENTS));
    }

    return json({ ok: true, id: data.id, attachments: linked });
  } catch (err) {
    console.error("intake_unhandled", err);
    return json({ error: "unexpected_error" }, 500);
  }
});
