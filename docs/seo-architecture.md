# BIMRACE — SEO architecture

The state of the site as built, and the reasoning behind each decision. Written
so that whoever changes it next can tell what was deliberate.

---

## 1. Where the URLs are

41 indexable pages. Existing URLs were not moved — every page that was live
before this work is still at the same address, so nothing that was indexed has
been invalidated.

```
/                                       home
/platform.html                          intelligence stack        ─┐
/intelligence.html                      BIM as data                │ platform
/automation.html                        AI & automation            │ cluster
/technology/mcp-for-revit.html          MCP for Revit              │
/digital-twin.html                      digital twin              ─┘

/engineering.html                       services hub              ─┐
/services/mep-engineering-services.html                            │
/services/hvac-bim-services.html                                   │
/services/electrical-bim-services.html                             │ service
/services/plumbing-public-health-bim.html                          │ cluster
/services/fire-protection-bim-services.html                        │ (10)
/services/bim-coordination-clash-detection.html                    │
/services/bim-modelling-documentation.html                         │
/services/revit-services.html                                      │
/services/bim-automation-services.html                             │
/services/construction-support-bim.html                           ─┘

/industries.html                        sector hub                ─┐
/industries/commercial.html                                        │
/industries/residential.html                                       │
/industries/healthcare.html                                        │ sector
/industries/data-centres.html                                      │ cluster
/industries/industrial.html                                        │ (8)
/industries/hospitality.html                                       │
/industries/education.html                                         │
/industries/retail.html                                           ─┘

/locations.html                         international hub         ─┐
/locations/usa.html                                                │
/locations/uk.html                                                 │
/locations/uae.html                                                │ market
/locations/saudi-arabia.html                                       │ cluster
/locations/australia.html                                          │ (7)
/locations/canada.html                                             │
/locations/europe.html                                            ─┘

/projects.html  /technology.html  /about.html  /contact.html
/privacy.html   /terms.html       /cookies.html
```

Not indexable, by design and by tag: `/thank-you.html`, `/404.html`,
`/project-template.html`, `/capabilities.html` (a redirect stub).

### Why the hubs kept their old names

`engineering.html` is the services hub and `industries.html` the sector hub,
even though their children live under `/services/` and `/industries/`. Moving
them to `/services/` and `/industries/` would have been tidier and would have
required 301s on two of the site's strongest existing URLs. The URL path does
not have to mirror the breadcrumb for Google to understand the hierarchy — the
breadcrumb markup and the internal linking do that — so the tidiness was not
worth the risk. Directory-form requests are redirected anyway (see §6).

### Why `.html` was kept

Extensionless URLs would be cleaner. Getting them on this stack means either
directory-per-page (`/services/hvac/index.html`) or host rewrite rules, and
either way every existing indexed URL needs a 301. The gain is cosmetic; the
risk is real. If it is ever done, do it as one deliberate migration with a
complete redirect map, not incrementally.

---

## 2. Metadata

One code path builds every `<head>`: `head()` in `_source/build.py`. There is
no page that sets its own title, description or canonical by hand, so the
failure modes that produce `BIMRACE | BIMRACE | BIMRACE` are structurally
impossible.

Every indexable page has a unique title, a unique description and a
self-referencing canonical. `audit.py` fails the build if any of those is
duplicated, missing or wrong.

**Title pattern** — intent, then qualifier, then brand, kept under ~65
characters so Google does not truncate the half that does the work:

```
MEP Engineering & BIM Services | BIMRACE
HVAC Design & Ductwork BIM Services | BIMRACE
BIM Coordination & Clash Detection | BIMRACE
Healthcare MEP & BIM Services | BIMRACE
MEP Engineering & BIM Services for the USA | BIMRACE
MCP for Revit | Model Context Protocol | BIMRACE
```

Location is in the title only on location pages. Forcing a country name into
every title produces a set of titles that compete with each other.

**Descriptions** are 120–170 characters, written as a reason to click rather
than as a keyword list.

---

## 3. Structured data

| Schema | Where | Note |
|---|---|---|
| `Organization` | home | Name, legal name, founder, contact, `knowsAbout`. No ratings, no awards. |
| `ItemList` of `Service` | home, engineering | The five capability groups. |
| `Service` | each of the 10 service pages | With `areaServed` matching the markets that actually have a page. |
| `BreadcrumbList` | every page below the root | Generated from the same list that renders the visible breadcrumb. |
| `FAQPage` | home, 10 services, 8 sectors, 7 markets, locations hub, MCP | Generated from the same list that renders the visible FAQ, so markup and page cannot disagree. |

**Not used, deliberately:**

- `LocalBusiness` — it asserts a servable physical location. BIMRACE has one
  office, in India, and the location pages exist precisely to say there are no
  others. Adding `LocalBusiness` per market would contradict the page body.
- `AggregateRating` / `Review` — there are no verified reviews. `audit.py`
  fails the build if either key ever appears in any JSON-LD block.
- `Product`, `Offer` — nothing on this site is a product for sale, and the
  platform page says so explicitly.

---

## 4. International SEO

**No hreflang, on purpose.** hreflang declares that two URLs are the same
content for different languages or regions. There is one language and one
version of every page here. A self-referencing `hreflang="en"` would be valid
and would communicate nothing; a set of fabricated `en-us` / `en-gb` variants
pointing at the same document would be worse than nothing. If genuinely
localised versions are ever produced — different currency, different code
basis, different contact route — add hreflang at that point and not before.

What is done instead:

- `og:locale: en` and `<html lang="en">`.
- Seven market pages, each with content that is genuinely different: standards
  basis, approval route, working-hours overlap, collaboration model, typical
  engagements, and a licensure statement specific to that jurisdiction.
- `areaServed` on the `Service` schema naming the markets that have a page.
- Internal links from every market page to the services and sectors relevant to
  that market, and from the services hub to all seven markets.

**The honesty constraint is load-bearing.** Every market page opens with a
block stating that BIMRACE has no office, no registered entity and no
professional licensure in that market, and names the licence that would be
required — PE by state in the US, chartered status in the UK, an emirate trade
licence in the UAE, Saudi Council of Engineers registration, state registration
in Australia, provincial P.Eng in Canada, member-state qualification in Europe.
This is also the strongest available differentiator in a category where
implying local presence is close to standard practice.

---

## 5. Sitemap

`/sitemap.xml`, generated from the build registry. Every page that calls
`page()` with `index=True` appends itself; the sitemap is that list minus the
noindex set. A page therefore cannot be forgotten by the sitemap, and the
sitemap cannot list a page that was never built. `audit.py` asserts both
directions and fails if they disagree.

- Canonical URLs only, absolute, `https://bimrace.com`.
- `<lastmod>` is the build date, which is accurate: every page is regenerated
  on every build.
- No `<priority>` and no `<changefreq>`. Google ignores both. A file full of
  values nobody reads is a file nobody keeps accurate.
- No redirects, no 404s, no noindex pages, no duplicates.

**A sitemap index is not needed yet.** The limits are 50,000 URLs and 50 MB
uncompressed; this is 41 URLs. If the site ever passes a few hundred — a case
study library, an insights archive — split by cluster
(`/sitemaps/services.xml`, `/sitemaps/locations.xml`, …) behind
`/sitemap-index.xml`. Doing it now would add moving parts for no benefit.

---

## 6. robots.txt and redirects

`/robots.txt` allows everything public. It disallows only `/thank-you.html`,
`/project-template.html` and `/_source/` — all three also carry `noindex`, and
none is in the sitemap. Nothing blocks CSS, JS, SVG or images: blocking them
breaks rendering for the crawler and costs more than it protects. `audit.py`
fails the build if a disallowed path ever appears in the sitemap, or if a
rendering-critical file type is ever blocked.

Redirects are generated in **two formats from one list**, because the previous
configuration had them only in `netlify.toml` while `amplify.yml` is what
actually deploys the site — so the 301s written for the platform restructure
were live on a host nobody uses and absent on the host in production.

- `netlify.toml` — read automatically.
- `amplify-redirects.json` — **must be pasted** into
  Amplify → App settings → Rewrites and redirects. Amplify reads no file for
  this.
- `amplify-headers.yml` — same, for the security headers. YAML, because that is what the custom-headers editor takes.

| From | To | Status |
|---|---|---|
| `/capabilities`, `/capabilities.html` | `/engineering.html` | 301 |
| `/services`, `/services/` | `/engineering.html` | 301 |
| `/industries/` | `/industries.html` | 301 |
| `/locations/` | `/locations.html` | 301 |
| `/technology/` | `/technology.html` | 301 |
| anything else | `/404.html` | 404 |

---

## 7. Internal linking

Designed rather than incidental. Orphan pages are the default failure mode of a
site that grows by adding landing pages, and `audit.py` fails the build if any
indexable page has no inbound internal link.

```
home ──► engineering.html ──► 10 service pages ──┬──► sibling services
                          └─► 7 market pages     ├──► relevant sectors
                                                 └──► contact?service=…

industries.html ──► 8 sector pages ──┬──► the 3-4 services that matter there
                                     ├──► locations.html
                                     └──► contact

locations.html ──► 7 market pages ──┬──► relevant services
                                    ├──► relevant sectors
                                    ├──► the other 4 markets
                                    └──► contact

platform.html ──► intelligence / automation / mcp-for-revit / digital-twin
mcp-for-revit ──► bim-automation-services, revit-services, automation,
                  intelligence, platform#status, digital-twin
```

The footer carries the full inventory — six services plus the hub, all eight
sectors, all seven markets — and is generated from the same lists that build
the pages, so it cannot link to a page that does not exist or omit one that
does.

---

## 8. Content clusters

| Cluster | Hub | Supporting |
|---|---|---|
| MEP engineering | `/services/mep-engineering-services.html` | HVAC, electrical, public health, fire protection |
| BIM delivery | `/engineering.html` | coordination & clash, modelling & documentation, Revit, construction support |
| AI + BIM | `/platform.html` | intelligence, automation, **MCP for Revit**, digital twin, BIM automation |
| Sectors | `/industries.html` | 8 building types |
| Markets | `/locations.html` | 7 territories |

Each service page carries a section the competition does not have: **what the
appointment does not include**. It is a conversion asset before it is an SEO
one — a scope boundary at enquiry stage is information, and the same boundary
at month three is a dispute — but it also produces genuinely distinct content
per page, which is what keeps ten service pages out of doorway-page territory.

---

## 9. The MCP for Revit page

The highest-intent, lowest-competition term available to this business, and the
one easiest to destroy by overclaiming.

The page ranks on being correct rather than on being enthusiastic: what the
protocol is, why Revit is a hard target (main-thread API context, transactions,
no headless mode for interactive documents, model size against context window,
non-determinism against engineering liability), what the read boundary is and
why it is architectural, the six security questions to ask any vendor including
BIMRACE, and a three-line statement of where BIMRACE actually is.

It opens by saying BIMRACE has not built one. That is the first paragraph, not
a footnote, and the `Roadmap` badge is on the navigation entry.

---

## 10. Lead attribution

The question this answers: **which SEO page generates real business**, not
which page gets traffic.

Captured as first-class columns on `crm.enquiry_submissions`:
`source_code`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`,
`utm_term`, `landing_page`, `referrer`.

Captured inside `payload.__journey` (jsonb — no schema migration required):
`submitted_from` (the page the form was sent from), `page_path` (the route
through the site this session, capped at 12), `page_title`, `screen`, `tz`,
`language`, `at`.

First touch is written once and never overwritten; last touch updates every
visit, so original attribution survives a later campaign click.

Every contextual CTA on a service page carries `?service=<lead_type>`, which
pre-selects the enquiry form's service field. The visitor does not re-state
what they were reading when they decided to enquire, and the lead arrives
classified.

Useful query once there are leads:

```sql
select payload -> '__journey' ->> 'submitted_from' as page,
       count(*)                                    as enquiries,
       count(*) filter (where l.score_band in ('high','hot')) as qualified
from crm.enquiry_submissions s
left join crm.leads l on l.submission_id = s.id
where s.processed and s.rejection_reason is null
group by 1
order by qualified desc, enquiries desc;
```

---

## 11. Keeping it true

```bash
cd _source
python build.py --install     # regenerate and deploy into site/
python audit.py --strict      # exits 1 on any defect
python audit_css.py           # unstyled classes and dead CSS
```

`audit.py` currently reports **0 errors, 0 warnings** across 45 pages. Wire it
into CI before the next content change — it is only worth having if it runs
without being remembered.
