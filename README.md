# BIMRACE Lead Engine

**Deploying or changing the site? Start with [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** — one-time setup, CI/CD pipeline, everyday workflow and rollback.

Website + lead capture + CRM on Supabase. No framework and no runtime
dependencies beyond `supabase-js` loaded from a CDN in the console. The public
site is generated from `_source/` by a single Python script with no third-party
packages; `site/` is its committed output and is what gets deployed.

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
_source/             THE SITE SOURCE — edit here, never in site/
  build.py           generator: head, nav, footer, page registry, sitemap, robots
  _services.py       9 service page contents — follows the service catalogue (Excel)
  _catalogue.py      GENERATED from the catalogue workbook — do not hand-edit
  generate_catalogue.py  regenerate _catalogue.py (needs openpyxl; build.py does not)
  _industries.py     8 original sector page contents
  _industries_public_transport.py  public & government and transportation sector pages
  _services_design.py  MEP engineering design pages (catalogue PKG-05)
  _projects.py       published case studies (data-driven; see docs/DEPLOYMENT.md)
  _locations.py      7 market page contents
  _mcp.py            the MCP for Revit page
  _legal.py          privacy, terms, cookies
  style.css          design system (one file, token-driven)
  script.js          diagrams and behaviour (vanilla, no dependencies)
  lead-capture.js    public form handler + attribution
  audit.py           SEO / a11y / link build audit — run before every deploy
  audit_css.py       unstyled classes and dead CSS
  audit_js.py        JavaScript smoke test
supabase/
  migrations/     0001–0007, apply in order
  functions/      lead-intake Edge Function (optional hardening layer)
  tests/          security_and_lifecycle.sql — 33 assertions
  config.toml
web/
  config.example.js   copy to config.js and fill in
  crm/                internal operations console
site/                 GENERATED OUTPUT — do not hand-edit, build.py overwrites it
docs/
  seo-architecture.md            URL structure, schema, linking, attribution
  search-console-readiness.md    setup steps and what is already satisfied
```

---

## Services follow the catalogue

The nine service pages, the Services menu, the services hub (`engineering.html`)
and the enquiry form's "What do you need" list all follow
`BIMRACE_Building_Sector_Service_Catalogue.xlsx`. After editing the workbook:

```bash
cd _source
python generate_catalogue.py "C:/path/to/BIMRACE_Building_Sector_Service_Catalogue.xlsx"
python build.py --install
```

Retired service URLs (`mep-engineering-services`, `bim-automation-services`,
`construction-support-bim`) 301 to their replacements via `RETIRED` in
`_services.py`. The form's option values are `crm.leads.lead_type` codes;
migration `0006` registers them for scoring and routing.

## Sector coverage

Ten sector pages under `/industries/`, matching the catalogue's Building Types sheet:

| Sector | URL | Catalogue availability |
|---|---|---|
| Commercial & offices | `/industries/commercial.html` | Phase 1 |
| Residential & mixed use | `/industries/residential.html` | Phase 1 |
| Healthcare | `/industries/healthcare.html` | Phase 1 / project-specific |
| Hospitality | `/industries/hospitality.html` | Phase 1 |
| Retail | `/industries/retail.html` | Phase 1 |
| Education (institutional) | `/industries/education.html` | Phase 1 |
| **Public & government** | `/industries/public-government.html` | Phase 1 |
| Industrial & warehousing | `/industries/industrial.html` | Conditional |
| **Transportation buildings** | `/industries/transportation.html` | Conditional — building services only |
| Data centres | `/industries/data-centres.html` | Conditional |

The public & government and transportation pages use optional sector blocks in
`build.py` (building types with an illustrative SVG section, priorities, typical
deliverables, a five-step process, an explicit scope boundary and an on-page
enquiry form). The form is the shared `enquiry_form()` used by the contact page,
with the Sector field pre-filled, so submissions go through the same
`lead-intake` Edge Function into `crm.enquiry_submissions`. Sector pages that do
not define those keys render exactly as before.

## Building the site

`site/` is generated. Editing it directly works until the next build, then the
change disappears — so edit `_source/` and rebuild.

```bash
cd _source
python build.py --install      # regenerate and copy over site/
python audit.py --strict       # 0 errors required before deploy
python audit_css.py            # unstyled classes / dead CSS
python audit_js.py --strict    # JS smoke test
```

`audit.py` is the gate. It fails on broken internal links, duplicate or missing
titles, descriptions or canonicals, wrong canonicals, missing or multiple `h1`,
heading-level skips, `img` without `alt`, invalid JSON-LD, any rating or review
key in structured data, orphan pages, a CTA whose `?service=` value has no
matching option on the enquiry form, and any disagreement between the built
pages and `sitemap.xml`. It currently reports **0 errors, 0 warnings** across 45
pages.

### After deploying

`netlify.toml` is read automatically. **Amplify is not** — it reads neither
`netlify.toml` nor `_redirects`, so two files have to be pasted into the console
once, and again whenever the rules change:

- `site/amplify-redirects.json` → App settings → Rewrites and redirects
- `site/amplify-headers.yml` → App settings → Custom headers (YAML, not JSON)

Until that is done the 301s are not live on the host that actually serves the
site. See `docs/search-console-readiness.md`.

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
`0004_seed_reference_data` → `0005_storage_policies` → `0006_catalogue_service_lines` → `0007_harden_function_access`

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

All public submissions go through the `lead-intake` Edge Function. Since migration
0008 the anon key has no table or storage privileges, so there is no direct
database path to switch on.

---

## 3. Deploy the Edge Function (required)

```bash
supabase secrets set SUPABASE_SERVICE_ROLE_KEY=<rotated key>
supabase secrets set TURNSTILE_SECRET=<cloudflare secret>   # optional
supabase secrets set IP_SALT=<random string>
supabase functions deploy lead-intake --no-verify-jwt
```
(`SUPABASE_SERVICE_ROLE_KEY` is injected automatically on hosted projects.) The
GitHub Action `Deploy Supabase` does this on every merge that touches `supabase/`.

---

## 4. Deploy the site

Run `python _source/build.py --install` first, then drag the `site/` folder onto
Netlify (`index.html` is at its root). The CRM in `web/crm/` is a separate deploy — put it on its own private Netlify site with
password protection, or a subdomain such as `ops.bimrace.com`. **Do not publish
the console on the public marketing domain.**

### AWS Amplify auto-deploy

The repository includes `amplify.yml` for the `main` branch. In the Amplify app,
add these environment variables before enabling auto-builds:

```text
SUPABASE_URL=https://aknvdryanbtqqadssboc.supabase.co
SUPABASE_ANON_KEY=sb_publishable_RPzPdpDEi0tBavMYUuL7gw_1cLafQkK
USE_EDGE_FUNCTION=true
```

### Live backend status (project `aknvdryanbtqqadssboc`)

- Migrations 0001–0007 applied (`npx supabase db push --linked`).
- `crm` schema exposed to the API (`supabase/config.toml` → `npx supabase config push`).
- `lead-intake` Edge Function deployed with `--no-verify-jwt`; `IP_SALT` secret set.
  Its CORS headers now allow `authorization`, which the form sends — without that,
  browsers blocked every submission through the function.
- Verified end to end: browser form → Edge Function → `crm.enquiry_submissions`
  → trigger → scored lead. Anonymous reads of leads are refused.
- Remaining: create your CRM admin user (section 1, "Create your first user"),
  and optionally set `ALLOWED_ORIGIN=https://bimrace.com` and `TURNSTILE_SECRET`
  with `npx supabase secrets set` before launch.

Each build generates the ignored `site/config.js` from those values. The anon key
is safe for browser use; never add the Supabase service role key to Amplify
environment variables used by this frontend.

In Amplify, open **App settings → Environment variables → Manage variables**, add
both names for the `main` branch, save, then choose **Redeploy this version** for
the failed deployment. The build log should show the config-generation command
completing before the artifact upload begins.

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
- **No analytics and no Search Console.** Neither is installed. The cookie
  policy currently says so truthfully; installing analytics makes that page
  inaccurate, so update it in the same change. Search Console setup is written
  up step by step in `docs/search-console-readiness.md`.
- **No case studies, no client logos, no testimonials, no project counts.**
  None have been released and verified. `projects.html` publishes the five
  measurement rules they will follow when they exist, and the sector and market
  pages state explicitly that they describe capability rather than history.
- **No MCP server for Revit.** `/technology/mcp-for-revit.html` explains the
  architecture and says in its first paragraph that it has not been built. If
  that changes, that page changes with it.
- **Virus scanning** has an `attachments.scan_status` column and is designed for,
  but no scanner is connected.
