# BIMRACE Lead Engine

Website + lead capture + CRM on Supabase. No framework, no build step, no runtime
dependencies beyond `supabase-js` loaded from a CDN in the console.

---

## ⚠ Do this first: rotate your service role key

A `service_role` key was shared in plaintext during this work. That key bypasses
every RLS policy and grants full read/write/delete on the whole database.

**Supabase Dashboard → Settings → API → rotate the `service_role` key.**

The rotated key goes into Edge Function secrets only. It must never appear in
`/web`, in `config.js`, in a repository, or in any file served to a browser.
The anon key is different: it is *designed* to be public and is constrained by
the RLS policies in migration `0003`.

---

## What is in this package

```
supabase/
  migrations/     0001–0005, apply in order
  functions/      lead-intake Edge Function (optional hardening layer)
  tests/          security_and_lifecycle.sql — 33 assertions
  config.toml
web/
  config.example.js   copy to config.js and fill in
  lead-capture.js     public form handler
  crm/                internal operations console
site/                 the public marketing site (already built)
```

---

## 1. Apply the database migrations

The migrations are **additive only**. Every object uses `IF NOT EXISTS`, there is
no `DROP`, no `TRUNCATE` and no column removal, and everything lives in a new
`crm` schema. They cannot damage data already in `public`.

**Supabase CLI (recommended):**
```bash
supabase link --project-ref YOUR_PROJECT_REF
supabase db push
```

**Or paste each file into the SQL editor, in order:**
`0001_core_schema` → `0002_functions_triggers` → `0003_rls_policies` →
`0004_seed_reference_data` → `0005_storage_policies`

Then expose the schema to the API: **Settings → API → Exposed schemas** — add `crm`.

### Create your first user
Create the user in **Authentication → Users**, then run:
```sql
insert into crm.app_users (id, email, full_name, role)
values ('<the auth user uuid>', 'you@bimrace.com', 'Your Name', 'admin');
```
A user with no `app_users` row defaults to `viewer` and can see nothing sensitive.
Roles: `admin`, `sales`, `business_development`, `project_manager`, `bim_manager`, `viewer`.

### Verify it worked
```sql
-- as anon this must fail; as admin it must return rows
select count(*) from crm.leads;
select crm.fn_dashboard_metrics();
```

---

## 2. Configure the front end

```bash
cp web/config.example.js site/config.js
```
Fill in `supabaseUrl` and `supabaseAnonKey`. Copy the same file to `web/crm/config.js`
(the console loads `../config.js`, so place it one level above `crm/`).

`useEdgeFunction: false` posts directly to `crm.enquiry_submissions` — already safe,
because anon holds INSERT and nothing else. Set it to `true` after deploying the
Edge Function to add rate limiting, Turnstile and IP hashing.

---

## 3. Deploy the Edge Function (optional)

```bash
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<rotated key>
supabase secrets set TURNSTILE_SECRET=<cloudflare secret>   # optional
supabase secrets set IP_SALT=<random string>
supabase functions deploy lead-intake --no-verify-jwt
```
Then set `useEdgeFunction: true` in `config.js`.

---

## 4. Deploy the site

Drag the `site/` folder onto Netlify (`index.html` is at its root). The CRM in
`web/crm/` is a separate deploy — put it on its own private Netlify site with
password protection, or a subdomain such as `ops.bimrace.com`. **Do not publish
the console on the public marketing domain.**

---

## How a lead flows

```
form submit → crm.enquiry_submissions (the ONLY table anon can write)
            → AFTER INSERT trigger fn_process_submission
              ├─ validate email and name, else reject and stop
              ├─ match or create organization (business domain, then name)
              ├─ match or create contact
              ├─ detect duplicates by email or phone
              ├─ create the lead (status/score/owner set by the engine, never by input)
              ├─ fn_score_lead   → writes lead_score_history with every rule that fired
              └─ fn_route_lead   → assigns by rule to the least-loaded holder of a role
```

Public input can never set `status`, `lead_score`, `assigned_to` or `priority`:
those columns are not writable by anon on any table it can reach.

### Scoring
Rules live in `crm.lead_scoring_rules` as **data**, not code. Edit points,
add rules or disable them without a deploy. Bands: `low` 0–20, `medium` 21–50,
`high` 51–75, `hot` 76+. Every calculation writes a breakdown to
`crm.lead_score_history`, and the lead detail screen shows exactly which rules
fired and for how many points — no score is unexplainable.

### Routing
Rules live in `crm.lead_routing_rules`, matched in `priority` order. Rules target
a **role**, and the engine picks the least-loaded active holder of it — so nobody's
name is hard-coded and staff changes need no code change.

---

## Security model

| Actor | Can do |
|---|---|
| anon | INSERT one row into `crm.enquiry_submissions`; SELECT active services/categories/countries; upload to `enquiry-files/incoming/` |
| anon | **Cannot** read leads, organizations, contacts, submissions, audit logs, proposals or projects — refused at the privilege layer, before RLS |
| sales | Read/update leads assigned to them or unassigned; notes, tasks, communications on those leads |
| business_development | All leads; proposals |
| bim_manager | All leads, read-oriented |
| project_manager | Won/late-stage leads; projects |
| viewer | Read-only reference and pipeline visibility |
| admin | Everything, including the audit log and configuration |

There is deliberately no "authenticated can select everything" policy. Roles are
stored in `crm.app_users`, not in JWT claims the client controls, so a user cannot
escalate their own privileges. Role changes are captured by the audit trigger.

Files go to a **private** bucket. Anonymous users can upload but have no SELECT
policy, so an uploaded file cannot be retrieved by guessing its URL. Staff read
via short-lived signed URLs.

---

## Testing

```bash
psql "$DATABASE_URL" -f supabase/tests/security_and_lifecycle.sql
```
33 assertions covering anonymous submission, RLS refusal on seven tables,
anon UPDATE/INSERT rejection, scoring, explainability, routing, duplicate
detection, idempotency, invalid input, cross-user isolation, status history,
audit capture, idempotent project conversion, international routing, low-value
scoring and dashboard authorisation. A clean run prints `ALL TESTS PASSED`.

These were executed against PostgreSQL 16 during development — all 33 pass.

---

## What was deliberately not built

Being explicit so you can plan the next phase:

- **Email sending is not wired up.** The architecture is in place (`app_settings`
  toggles, `communications` table), but no provider is connected. The system never
  records that an email was sent unless a provider actually confirms it.
- **Proposals and projects are foundations**, not a full quoting or PM module —
  tables, numbering, statuses and conversion exist; the UI does not.
- **The CRM console covers** dashboard, leads, pipeline, lead detail, notes,
  follow-ups and conversion. Organizations, contacts, proposals, campaigns,
  analytics and settings screens are not built; the data model supports them.
- **Realtime is not enabled.** Add it per-table when there is a second concurrent
  user; it adds nothing today.
- **Virus scanning** has an `attachments.scan_status` column and is designed for,
  but no scanner is connected.
