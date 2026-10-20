// ============================================================================
// BIMRACE — lead-upload Edge Function
//
// Issues a one-time signed upload URL so a visitor can attach drawings or
// models to an enquiry without holding any storage privilege themselves
// (anon has none since migration 0008).
//
//   POST { submission_key, file_name, mime_type, byte_size }
//   ->   { path, token, signed_url }
//
// The file lands in the PRIVATE enquiry-files bucket under
// incoming/<submission_key>/<random>-<safe name>. lead-intake later links the
// uploaded paths to the lead after checking they exist under that same prefix.
//
// Deploy: supabase functions deploy lead-upload --no-verify-jwt
// ============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const BUCKET = "enquiry-files";
const MAX_BYTES = 50 * 1024 * 1024;            // matches the bucket and table limit
const MAX_FILES_PER_SUBMISSION = 5;
const WINDOW_MS = 60 * 60 * 1000;
const MAX_URLS_PER_IP = 20;

// Extension decides the stored content type, so a visitor cannot label an
// executable as a PDF. Everything here is a document or model format.
const TYPES: Record<string, string> = {
  pdf: "application/pdf", png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg",
  webp: "image/webp", zip: "application/zip", dwg: "image/vnd.dwg",
  dxf: "application/dxf", ifc: "model/ifc", rvt: "application/octet-stream",
  nwd: "application/octet-stream", nwc: "application/octet-stream",
};

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const hits = new Map<string, number[]>();
const perSubmission = new Map<string, number>();

const allowed = (Deno.env.get("ALLOWED_ORIGINS") ?? Deno.env.get("ALLOWED_ORIGIN") ?? "*")
  .split(",").map((o) => o.trim()).filter(Boolean);

function corsFor(req: Request) {
  const origin = req.headers.get("origin") ?? "";
  const allowOrigin = allowed.includes("*") ? "*" : allowed.includes(origin) ? origin : allowed[0];
  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

const responder = (cors: Record<string, string>) => (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "content-type": "application/json" },
  });

function rateLimited(ip: string) {
  const now = Date.now();
  const list = (hits.get(ip) ?? []).filter((t) => now - t < WINDOW_MS);
  list.push(now);
  hits.set(ip, list);
  return list.length > MAX_URLS_PER_IP;
}

function safeName(name: string) {
  const base = name.split(/[\\/]/).pop() ?? "file";
  return base.normalize("NFKD").replace(/[^A-Za-z0-9._-]+/g, "_").replace(/_+/g, "_").slice(-120);
}

Deno.serve(async (req) => {
  const cors = corsFor(req);
  const json = responder(cors);
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() ?? "unknown";
  try {
    const raw = await req.text();
    if (raw.length > 2_000) return json({ error: "payload_too_large" }, 413);
    if (rateLimited(ip)) return json({ error: "rate_limited" }, 429);

    const { submission_key, file_name, byte_size } = JSON.parse(raw);
    if (typeof submission_key !== "string" || !UUID_RE.test(submission_key)) {
      return json({ error: "invalid_request" }, 400);
    }
    if (typeof file_name !== "string" || !file_name.trim()) return json({ error: "invalid_request" }, 400);
    const size = Number(byte_size);
    if (!Number.isFinite(size) || size <= 0 || size > MAX_BYTES) {
      return json({ error: "file_too_large", max_bytes: MAX_BYTES }, 413);
    }
    const name = safeName(file_name);
    const ext = name.includes(".") ? name.split(".").pop()!.toLowerCase() : "";
    const contentType = TYPES[ext];
    if (!contentType) return json({ error: "file_type_not_allowed", allowed: Object.keys(TYPES) }, 415);

    const used = perSubmission.get(submission_key) ?? 0;
    if (used >= MAX_FILES_PER_SUBMISSION) return json({ error: "too_many_files" }, 429);
    perSubmission.set(submission_key, used + 1);

    // Secret key used only here, server-side. It never reaches the browser.
    const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
      { auth: { persistSession: false } });
    const path = `incoming/${submission_key.toLowerCase()}/${crypto.randomUUID().slice(0, 8)}-${name}`;
    const { data, error } = await db.storage.from(BUCKET).createSignedUploadUrl(path);
    if (error || !data) {
      console.error("signed_upload_failed", error);
      return json({ error: "storage_failed" }, 500);
    }
    return json({ path, token: data.token, signed_url: data.signedUrl, content_type: contentType });
  } catch (err) {
    console.error("upload_unhandled", err);
    return json({ error: "unexpected_error" }, 500);
  }
});
