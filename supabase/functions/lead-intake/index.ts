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

const cors = {
  "Access-Control-Allow-Origin": Deno.env.get("ALLOWED_ORIGIN") ?? "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const json = (body: unknown, status = 200) =>
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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";

  try {
    const raw = await req.text();
    if (raw.length > MAX_BYTES) return json({ error: "payload_too_large" }, 413);
    if (rateLimited(ip)) return json({ error: "rate_limited" }, 429);

    const body = JSON.parse(raw);
    const { submission_key, form_code, payload, turnstile_token, ...attribution } = body;

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

    return json({ ok: true, id: data.id });
  } catch (err) {
    console.error("intake_unhandled", err);
    return json({ error: "unexpected_error" }, 500);
  }
});
