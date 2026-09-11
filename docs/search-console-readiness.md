# Google Search Console — readiness and setup

**Search Console is not configured.** Nobody has connected this property. This
document is what to do, and what the site already satisfies so that you are not
debugging the site while you are debugging the console.

---

## Part 1 — What the build already guarantees

Verified by `_source/audit.py`, which reports **0 errors, 0 warnings** across 45
pages and fails the build if any of the following stops being true.

| Check | State | How it is enforced |
|---|---|---|
| Crawlable HTML, no JS required to read content | Pass | Static HTML; JS only adds diagrams and form behaviour |
| `robots.txt` present and reachable | Pass | Generated; references the sitemap absolutely |
| CSS / JS / images not blocked | Pass | Audit fails if a rendering-critical type is disallowed |
| Sitemap present, canonical URLs only | Pass | Generated from the build registry |
| Sitemap contains no noindex, no redirect, no 404 | Pass | Audit cross-checks sitemap against built pages |
| Every indexable page in the sitemap | Pass | Audit fails if the two sets differ |
| Self-referencing canonical on every indexable page | Pass | One code path; audit verifies the exact string |
| No accidental `noindex` | Pass | Exactly 4 noindex pages, all intended, none in the sitemap |
| Unique `<title>` per page | Pass | Audit fails on duplicates |
| Unique meta description per page | Pass | Audit fails on duplicates |
| Exactly one `<h1>` per page | Pass | Audit fails otherwise |
| No heading-level skips | Pass | Audit warns; currently zero |
| Open Graph complete, `og:url` == canonical | Pass | Audit verifies |
| Valid JSON-LD, no fabricated ratings or reviews | Pass | Audit parses every block and rejects rating keys |
| No broken internal links | Pass | Audit resolves every href against the built file set |
| No orphan pages | Pass | Audit fails if an indexable page has no inbound link |
| Branded, useful 404 | Pass | `/404.html`, noindex, links to every main section |
| Mobile viewport and responsive layout | Pass | Breakpoints at 1240 / 1080 / 980 / 560 |
| `img` alt text | Pass | Audit fails on any `img` without `alt` |

### Not yet satisfied — these need a person

| Item | Owner action |
|---|---|
| HTTPS on the live domain | Confirm the Amplify domain has a valid certificate and that `http://` redirects to `https://` |
| One canonical host | Decide `bimrace.com` **or** `www.bimrace.com` and 301 the other. Canonicals are currently written to the apex, so the apex is the choice unless you change `SITE` in `_source/build.py` |
| Redirect rules live | Paste `site/amplify-redirects.json` into Amplify (see below) — Amplify does not read `netlify.toml` |
| Security headers live | Paste `site/amplify-headers.yml` into Amplify |
| Search Console property | Not created |

---

## Part 2 — Before you touch Search Console

### 2.1 Apply the Amplify redirect rules

`amplify.yml` is what deploys this site, and Amplify reads neither
`netlify.toml` nor `_redirects`. Until this is done, `/capabilities.html` — a
previously published URL — resolves only via a meta refresh, which passes less
signal than a 301 and looks like a soft 404.

1. Amplify console → the app → **App settings → Rewrites and redirects**
2. **Open text editor**
3. Paste the contents of `site/amplify-redirects.json`
4. Save

### 2.2 Apply the security headers

Same console, **App settings → Custom headers → Edit**, paste
`site/amplify-headers.yml`. That editor takes YAML, not JSON.

This sets HSTS, `X-Content-Type-Options`, `Referrer-Policy`,
`Permissions-Policy`, a Content-Security-Policy and cache headers. Verify
afterwards that the About page photograph still loads — it is served from
Supabase Storage and the CSP allows `https://*.supabase.co` for `img-src`
specifically because of it.

### 2.3 Confirm both files are reachable

```
https://bimrace.com/robots.txt      -> 200, text/plain
https://bimrace.com/sitemap.xml     -> 200, XML, 41 <url> entries
https://bimrace.com/capabilities.html -> 301 to /engineering.html
https://bimrace.com/nonexistent     -> 404 (not 200 with a 404 page)
```

That last one matters. A host that serves the 404 page with a 200 status
creates a soft-404 for every mistyped URL, and Search Console will report it as
a crawl problem rather than as a missing page.

---

## Part 3 — Set up the property

### 3.1 Create a Domain property

Use **Domain**, not URL-prefix. A Domain property covers `http`, `https`, the
apex and every subdomain in one place, which means you do not later discover
that half the data was going to a property you forgot about.

1. [search.google.com/search-console](https://search.google.com/search-console)
   → **Add property** → **Domain** → `bimrace.com`
2. Google returns a TXT record. Add it at the DNS provider for `bimrace.com`
   (Route 53 if the domain is managed in AWS; otherwise wherever the nameservers
   point).
3. Wait for propagation — usually minutes, occasionally an hour — then
   **Verify**.

If DNS access is genuinely unavailable, fall back to an HTML file uploaded to
`site/` — but note it will be deleted by the next `build.py --install`, because
that step removes files the generator did not produce. Add it to the `keep` set
in `build.py` if you go that route.

### 3.2 Submit the sitemap

**Indexing → Sitemaps** → enter `sitemap.xml` → Submit.

Expect "Success" and 41 discovered URLs. "Couldn't fetch" almost always means
DNS has not propagated or the deploy has not run — not that the file is wrong.

### 3.3 Request indexing for the priority pages

Do not submit all 41. Use **URL Inspection → Request indexing** on the pages
that matter most, roughly five a day:

```
/
/engineering.html
/services/mep-engineering-services.html
/services/bim-coordination-clash-detection.html
/technology/mcp-for-revit.html
/locations.html
/locations/usa.html
/locations/uk.html
/industries.html
/contact.html
```

The rest will be found through internal links and the sitemap. Manual
submission is a nudge, not a requirement, and does not affect ranking.

---

## Part 4 — What to look at, and when

### Week 1

- **Page indexing** — "Discovered, not indexed" is normal for a new site and
  means wait. "Crawled, not indexed" on a cluster page means Google found the
  content thin or duplicative; read that page again with that in mind.
- **Sitemaps** — discovered count should be 41.
- **URL Inspection → Test live URL** on one service page and one market page.
  Check the rendered HTML contains the body copy. It will; the site is static.
- **Enhancements → Breadcrumbs** and **FAQ** should start appearing.

### Weeks 2–6

- **Performance → Queries.** Ignore position at this stage; look at *which*
  queries appear at all. The first real signal is whether the cluster terms —
  "MEP BIM services", "BIM coordination", "MCP for Revit", country-qualified
  variants — show impressions.
- **Core Web Vitals.** Needs 28 days of field data before it reports anything.
  A static site with one stylesheet, two deferred scripts and no images above
  the fold should pass; if it does not, the Google Fonts request is the first
  thing to look at.

### Ongoing

- **Page indexing**, monthly. Any page dropping out is a signal, not noise.
- **Manual actions** and **Security issues**, monthly. Both should be empty.
- **Removals**, never — unless something was published in error.

---

## Part 5 — The queries worth tracking

The site is built around these clusters. Track them from the start so that six
months of data exists when someone asks whether this worked.

**Service intent**
`mep bim services` · `mep engineering outsourcing` · `bim coordination services`
· `clash detection services` · `revit mep modelling` · `revit family creation`
· `bim automation services` · `shop drawing services mep` ·
`builders work drawings`

**Sector intent**
`healthcare mep bim` · `data centre bim coordination` ·
`hotel mep bim services` · `retail fit out bim`

**Market intent**
`mep engineering services usa` · `bim services uk` · `mep bim dubai` ·
`bim outsourcing saudi arabia` · `revit services australia`

**Differentiator intent — low volume, highest value**
`mcp for revit` · `model context protocol revit` · `ai for revit` ·
`ai bim automation` · `ai assisted mep coordination`

That last group is why the MCP page exists. It will not produce volume. It is
likely to produce the enquiries worth having, and it is the term set where
being correct rather than enthusiastic is an actual competitive position.

---

## Part 6 — Also worth doing

- **Bing Webmaster Tools.** Ten minutes, imports directly from Search Console,
  and Bing is what several AI assistants read.
- **Analytics.** None is installed, and the cookie policy currently states that
  truthfully. Installing any analytics makes that page inaccurate and will
  likely require a consent banner — update the policy in the same change, not
  afterwards.
- **Re-run the audit after every content change:**
  ```bash
  cd _source && python build.py --install && python audit.py --strict
  ```
