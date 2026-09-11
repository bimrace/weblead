#!/usr/bin/env python3
"""
BIMRACE — build audit.

Run after build.py. Fails loudly on the defects that are cheap to introduce and
expensive to find in Search Console three weeks later: broken internal links,
duplicate titles or descriptions, wrong canonicals, missing or multiple H1s,
invalid JSON-LD, orphan pages, images without alt text, and any mismatch between
what was built and what the sitemap claims.

    python audit.py          # report
    python audit.py --strict # exit 1 on any error (use in CI)
"""
import collections, html, json, pathlib, re, sys, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
SITE = "https://bimrace.com"

errors, warnings, notes = [], [], []


def err(p, m):
    errors.append(f"{p}: {m}")


def warn(p, m):
    warnings.append(f"{p}: {m}")


pages = {p.relative_to(DIST).as_posix(): p.read_text(encoding="utf-8")
         for p in sorted(DIST.rglob("*.html"))}

# Redirect stubs: noindex, canonical pointing at the target, no OG block.
REDIRECTS = {k for k, v in pages.items() if 'http-equiv="refresh"' in v}
assets = {p.relative_to(DIST).as_posix() for p in DIST.rglob("*") if p.is_file()}

print(f"auditing {len(pages)} pages\n" + "=" * 74)

# ---------------------------------------------------------------- helpers --
TAG = re.compile(r"<[^>]+>")
def text_of(s):
    return html.unescape(TAG.sub(" ", s))


def meta(doc, name=None, prop=None):
    pat = (rf'<meta name="{name}" content="(.*?)">' if name
           else rf'<meta property="{prop}" content="(.*?)">')
    m = re.search(pat, doc, re.S)
    return m.group(1) if m else None


titles, descs, canons = {}, {}, {}
linked_to = collections.Counter()

for path, doc in pages.items():
    noindex = 'name="robots" content="noindex' in doc
    redirect = path in REDIRECTS

    # ---- title ----------------------------------------------------------
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    if not t:
        err(path, "no <title>")
    else:
        title = html.unescape(t.group(1)).strip()
        if len(title) > 70:
            warn(path, f"title is {len(title)} chars (Google truncates near 60)")
        if not noindex:
            titles.setdefault(title, []).append(path)
        if title.count("BIMRACE") > 1:
            err(path, "brand repeated in title")

    # ---- description ----------------------------------------------------
    d = meta(doc, name="description")
    if not d:
        err(path, "no meta description")
    else:
        desc = html.unescape(d).strip()
        if not (70 <= len(desc) <= 190):
            warn(path, f"description is {len(desc)} chars (aim 120-165)")
        if not noindex:
            descs.setdefault(desc, []).append(path)

    # ---- canonical ------------------------------------------------------
    c = re.search(r'<link rel="canonical" href="(.*?)">', doc)
    if not c:
        err(path, "no canonical")
    else:
        expect = f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"
        if redirect:
            # A redirect stub must canonicalise to its target, never to itself.
            if c.group(1) == expect:
                err(path, "redirect stub canonicalises to itself")
        else:
            if c.group(1) != expect:
                err(path, f"canonical is {c.group(1)}, expected {expect}")
            canons.setdefault(c.group(1), []).append(path)

    # ---- Open Graph -----------------------------------------------------
    for prop in ("og:title", "og:description", "og:image", "og:url"):
        if not meta(doc, prop=prop) and not redirect:
            err(path, f"missing {prop}")
    ogu = meta(doc, prop="og:url")
    if ogu and c and ogu != c.group(1):
        err(path, "og:url does not match canonical")

    # ---- headings -------------------------------------------------------
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", doc, re.S)
    if len(h1s) != 1 and not redirect:
        err(path, f"{len(h1s)} <h1> elements (expected exactly 1)")
    elif h1s and not text_of(h1s[0]).strip():
        err(path, "empty <h1>")

    levels = [int(m) for m in re.findall(r"<h([1-4])[ >]", doc)]
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            warn(path, f"heading level jumps h{a} -> h{b}")
            break

    # ---- images ---------------------------------------------------------
    for tag in re.findall(r"<img\b[^>]*>", doc):
        if 'alt="' not in tag:
            err(path, "img without alt attribute")

    # ---- inline SVG needs a label when it is not decorative -------------
    for tag in re.findall(r'<svg\b[^>]*>', doc):
        if 'role="img"' in tag and "aria-label" not in tag:
            err(path, "svg role=img without aria-label")
        if 'role="img"' not in tag and 'aria-hidden' not in tag and 'class="dia"' not in tag:
            warn(path, "svg is neither labelled nor aria-hidden")

    # ---- JSON-LD --------------------------------------------------------
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            err(path, f"invalid JSON-LD: {e}")
            continue
        if "@context" not in data or "@type" not in data:
            err(path, "JSON-LD missing @context or @type")
        def scan(node, path_=path):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in ("aggregateRating", "review", "reviews", "ratingValue",
                             "reviewCount", "ratingCount", "award"):
                        err(path_, f"JSON-LD carries {k} - no verified ratings, "
                                   "reviews or awards exist")
                    if k == "@type" and v in ("Review", "AggregateRating"):
                        err(path_, f"JSON-LD declares @type {v}")
                    scan(v, path_)
            elif isinstance(node, list):
                for v in node:
                    scan(v, path_)
        scan(data)

    # ---- links ----------------------------------------------------------
    for attr, href in re.findall(r'\b(href|src)="([^"]+)"', doc):
        if href.startswith(("http", "mailto:", "tel:", "data:", "#")):
            continue
        if not href.startswith("/"):
            err(path, f"relative {attr} survived rewriting: {href}")
            continue
        target = href.lstrip("/").split("#")[0].split("?")[0]
        if target == "":
            target = "index.html"
        if target not in assets:
            err(path, f"broken link -> {href}")
        else:
            linked_to[target] += 1
            # A page that links to a noindex page in body content is usually a
            # mistake; the two we have are deliberate and excluded below.
            tdoc = pages.get(target, "")
            if ('name="robots" content="noindex' in tdoc
                    and target not in {"thank-you.html", "404.html",
                                       "project-template.html", "capabilities.html"}):
                warn(path, f"links to a noindex page: {href}")

# ---------------------------------------------------------------- global --
for t, ps in titles.items():
    if len(ps) > 1:
        err("GLOBAL", f"duplicate title across {ps}: {t!r}")
for d, ps in descs.items():
    if len(ps) > 1:
        err("GLOBAL", f"duplicate description across {ps}")
for c, ps in canons.items():
    if len(ps) > 1:
        err("GLOBAL", f"duplicate canonical {c} on {ps}")

# ---- CTA service prefill -------------------------------------------------
# Every contextual CTA carries ?service=<lead_type> to pre-select the enquiry
# form. A value with no matching <option> fails silently: the visitor sees an
# unselected dropdown and the lead arrives unclassified, with nothing logged.
form_values = set(re.findall(r'<option value="([a-z_]+)"', pages.get("contact.html", "")))
prefills = set()
for doc in pages.values():
    prefills |= set(re.findall(r"contact\.html\?service=([a-z_]+)", doc))
for v in sorted(prefills - form_values):
    err("GLOBAL", f"CTA prefills ?service={v}, which is not an option on the enquiry form")

# ---- sitemap vs reality --------------------------------------------------
sm = ET.fromstring((DIST / "sitemap.xml").read_text(encoding="utf-8"))
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
sitemap_urls = [u.text for u in sm.findall(".//s:loc", ns)]
if len(sitemap_urls) != len(set(sitemap_urls)):
    err("sitemap.xml", "duplicate <loc>")

sitemap_paths = set()
for u in sitemap_urls:
    if not u.startswith(SITE):
        err("sitemap.xml", f"URL outside the site: {u}")
        continue
    rel = u[len(SITE):].lstrip("/") or "index.html"
    sitemap_paths.add(rel)
    if rel not in pages:
        err("sitemap.xml", f"lists a page that was not built: {u}")
    elif 'name="robots" content="noindex' in pages[rel]:
        err("sitemap.xml", f"lists a noindex page: {u}")

robots = (DIST / "robots.txt").read_text(encoding="utf-8")
for line in robots.splitlines():
    if line.lower().startswith("disallow:"):
        blocked = line.split(":", 1)[1].strip().lstrip("/")
        if blocked and blocked in sitemap_paths:
            err("robots.txt", f"disallows a URL that is in the sitemap: /{blocked}")
if f"Sitemap: {SITE}/sitemap.xml" not in robots:
    err("robots.txt", "does not reference the sitemap")
for ext in (".css", ".js", ".svg", ".png"):
    if f"Disallow: /*{ext}" in robots or f"Disallow: *{ext}" in robots:
        err("robots.txt", f"blocks {ext} — breaks rendering for the crawler")

# ---- orphans -------------------------------------------------------------
for path in pages:
    if path in ("index.html", "404.html", "project-template.html") or path in REDIRECTS:
        continue
    if 'name="robots" content="noindex' in pages[path]:
        continue
    if linked_to[path] == 0:
        err(path, "orphan — no internal page links to it")
    elif linked_to[path] < 2:
        notes.append(f"{path}: only one inbound internal link")

# ---- indexable count -----------------------------------------------------
indexable = [p for p, d in pages.items() if 'content="noindex' not in d]
notes.append(f"{len(indexable)} indexable pages, {len(sitemap_paths)} in sitemap")
if set(indexable) != sitemap_paths:
    diff = set(indexable) ^ sitemap_paths
    err("GLOBAL", f"indexable pages and sitemap disagree: {sorted(diff)}")

# ---- deployed folder vs generator ---------------------------------------
# site/ is the committed artefact Amplify publishes. If someone edits _source/
# and forgets --install, the generator and the deployed site disagree and
# nobody finds out until a page is wrong in production. Catch it here.
import hashlib
SITE_DIR = ROOT.parent / "site"
if SITE_DIR.exists():
    def digest(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()
    ignore = {"config.js"}          # environment-specific, generated at deploy
    stale = []
    for f in DIST.rglob("*"):
        if f.is_dir():
            continue
        rel = f.relative_to(DIST).as_posix()
        if rel in ignore:
            continue
        t_ = SITE_DIR / rel
        if not t_.exists():
            stale.append(f"missing from site/: {rel}")
        elif digest(f) != digest(t_):
            stale.append(f"differs from site/: {rel}")
    for f in SITE_DIR.rglob("*"):
        if f.is_file() and not (DIST / f.relative_to(SITE_DIR)).exists():
            stale.append(f"orphaned in site/: {f.relative_to(SITE_DIR).as_posix()}")
    if stale:
        err("DEPLOY", f"site/ is out of date with the generator "
                      f"({len(stale)} file(s)) - run: python build.py --install")
        for x in stale[:8]:
            notes.append(f"  {x}")
    else:
        notes.append("site/ matches the generator output")

# ---------------------------------------------------------------- report --
for label, items in (("ERROR", errors), ("WARN", warnings), ("NOTE", notes)):
    if items:
        print(f"\n{label} ({len(items)})")
        for i in items:
            print(f"  {label:<5} {i}")

print("\n" + "=" * 74)
print(f"{len(errors)} errors, {len(warnings)} warnings")
if errors and "--strict" in sys.argv:
    sys.exit(1)
