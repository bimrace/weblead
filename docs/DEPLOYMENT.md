# BIMRACE — Deployment and CI/CD guide

## How the pipeline works

```
 you edit _source/ ──► python build.py --install ──► git push (branch) ──► Pull Request
                                                                              │
                                                     GitHub Actions: CI ◄─────┘
                                                     build + audit.py --strict + audit_css
                                                                              │ green
                                                                              ▼
                                                                     merge into main
                                     ┌────────────────────────────────────────┴───────────────┐
                                     ▼                                                        ▼
                     AWS Amplify (webhook)                              GitHub Actions: Deploy Supabase
                     builds config.js from env vars,                    (only if supabase/** changed)
                     publishes site/ to bimrace.com                     migrations + lead-intake function
```

| Part | Tool | Trigger |
|---|---|---|
| CI | `.github/workflows/ci.yml` | every push and pull request |
| Website deploy | AWS Amplify | push/merge to `main` |
| Database + Edge Function deploy | `.github/workflows/supabase-deploy.yml` | `supabase/**` changes on `main`, or manual |

---

## One-time setup (do these once, in order)

### Step 1 — Amplify environment variables
Amplify → your app → **Hosting → Environment variables → Manage variables**, branch `main`:

| Variable | Value |
|---|---|
| `SUPABASE_URL` | `https://aknvdryanbtqqadssboc.supabase.co` |
| `SUPABASE_ANON_KEY` | `sb_publishable_RPzPdpDEi0tBavMYUuL7gw_1cLafQkK` |
| `USE_EDGE_FUNCTION` | `true` (optional; forms always use the Edge Function) |

Save, then **Deployments → Redeploy this version**.
Check: open `https://bimrace.com/config.js` — it must show `aknvdryanbtqqadssboc`.

### Step 2 — Amplify redirects
Amplify does not read `netlify.toml`. Amplify → **Hosting → Rewrites and redirects → Manage → Open text editor**,
replace everything with the contents of `site/amplify-redirects.json`, save.
Check: `https://bimrace.com/services/mep-engineering-services.html` redirects to `/engineering.html`.
Repeat whenever `amplify-redirects.json` changes in a commit.

### Step 3 — Amplify custom headers
Amplify → **Hosting → Custom headers → Edit**, paste `site/amplify-headers.yml`, save.
This applies the security headers (CSP, HSTS, X-Frame-Options).

### Step 4 — Supabase token for GitHub Actions
1. Create a token: https://supabase.com/dashboard/account/tokens → **Generate new token** → name it `github-actions-weblead`.
2. Store it in GitHub (run in a terminal, paste the token when asked):
   ```
   gh secret set SUPABASE_ACCESS_TOKEN --repo bimrace/weblead
   ```
3. The project id variable (not secret):
   ```
   gh variable set SUPABASE_PROJECT_ID --repo bimrace/weblead --body aknvdryanbtqqadssboc
   ```

### Step 5 — Protect production
GitHub → repo **Settings → Environments → production** → add yourself under **Required reviewers**.
Database migrations then wait for your approval before running.

### Step 6 — Protect main
GitHub → **Settings → Branches → Add branch ruleset** (or classic rule) for `main`:
- Require a pull request before merging
- Require status checks to pass → select **Build and audit**
- Block force pushes

### Step 7 — Lock the enquiry endpoint to your domain
```
npx supabase secrets set ALLOWED_ORIGINS="https://bimrace.com,https://www.bimrace.com"
```
Optional anti-spam (Cloudflare Turnstile): `npx supabase secrets set TURNSTILE_SECRET=...` — the site's form
must then send `turnstile_token`; ask before enabling, because the front end needs the widget added.

### Step 8 — CRM admin user
1. Supabase → **Authentication → Users → Add user** (your email + password).
2. Supabase → **SQL editor**:
   ```sql
   insert into crm.app_users (id, email, full_name, role)
   select id, email, 'Somnath Baste', 'admin' from auth.users where email = 'YOUR_EMAIL';
   ```
3. The staff portal is in `portal/` and deploys as its own Amplify app (Step 9) —
   never on the public bimrace.com domain.

---

### Step 9 — Staff portal at portal.bimrace.com
1. Amplify → **Create new app** → GitHub → `bimrace/weblead`, branch `main`. Amplify reads the
   repository's `amplify.yml`; keep it.
2. Environment variables for this app:
   `APP_TARGET` = `portal`, `SUPABASE_URL` = `https://aknvdryanbtqqadssboc.supabase.co`,
   `SUPABASE_ANON_KEY` = the publishable key. Never the secret key — the build refuses it.
3. Custom headers for this app (Hosting → Custom headers):
   ```yaml
   customHeaders:
     - pattern: "**"
       headers:
         - key: "X-Robots-Tag"
           value: "noindex, nofollow, noarchive"
         - key: "X-Frame-Options"
           value: "DENY"
         - key: "X-Content-Type-Options"
           value: "nosniff"
         - key: "Referrer-Policy"
           value: "strict-origin-when-cross-origin"
         - key: "Strict-Transport-Security"
           value: "max-age=31536000; includeSubDomains"
         - key: "Cache-Control"
           value: "no-cache, must-revalidate"
   ```
4. Domain management → Add domain `bimrace.com` → subdomain `portal` → this app. Add the CNAME
   record Amplify shows at your DNS provider.
5. Supabase auth redirect URLs are already set from `supabase/config.toml` (`[auth]`), applied
   with `npx supabase config push`.
6. Sign in as admin → **Team** → create accounts. Each person gets a temporary password (shown once)
   and must set their own at first sign-in.

## Everyday workflow (every change)

```bash
git checkout main && git pull
git checkout -b update/short-description

# edit files in _source/ (never edit site/ by hand)
cd _source
python build.py --install        # regenerates site/
python audit.py --strict         # must say 0 errors
cd ..

git add -A
git commit -m "Describe the change"
git push -u origin update/short-description
gh pr create --fill               # opens a pull request; CI runs
```
When CI is green, merge the pull request. Amplify publishes within a few minutes.

**Publishing a project (case study):** get the client's written permission, then add an entry to
`_source/_projects.py` (copy `EXAMPLE`, set `"client_released": True`, optional image in
`_source/projects/`). Rebuild — the page appears at `/projects/<slug>.html`, on the Projects page
and in the sitemap. The build refuses unreleased entries and outcome figures without a measurement basis.

**Changing services:** edit the Excel workbook, then
`python _source/generate_catalogue.py "path/to/BIMRACE_Building_Sector_Service_Catalogue.xlsx"` and rebuild.

**Changing the database:** add a new file `supabase/migrations/0008_description.sql` (never edit applied
migrations). Merging it to main runs *Deploy Supabase*, which waits for your approval (Step 5).

---

## Rollback

| What broke | How to roll back |
|---|---|
| Website | Amplify → Deployments → pick the last good build → **Redeploy this version**; then `git revert <commit>` and merge |
| Edge Function | `git revert` the function change and merge (redeploys), or deploy the previous version locally |
| Database | Write a new forward migration that undoes the change; Supabase → Database → Backups for disaster recovery |

## Checks after every deploy
- `https://bimrace.com/` loads, Services menu opens
- `https://bimrace.com/config.js` points at `aknvdryanbtqqadssboc`
- Submit a test enquiry on `/contact.html` with email `qa-test@example.com`, confirm it in the CRM, delete it
