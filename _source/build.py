#!/usr/bin/env python3
"""
BIMRACE — MEP engineering and BIM site generator.

One source of truth for the head, navigation, CTA band and footer, so those
blocks cannot drift between pages. Run `python build.py`, then copy dist/ over
site/ (or run `python build.py --install`).

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    Every capability claim rendered by this generator carries a status
    badge from B(): live / dev / road / demo. If a claim cannot be given
    one honestly, it does not go on the site. The legend is published at
    platform.html#status so a reader can hold us to it.
"""
import datetime, json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "dist"
sys.path.insert(0, str(ROOT))
from _legal import PRIVACY, TERMS, COOKIES              # noqa: E402

SITE   = "https://bimrace.com"
EMAIL  = "info@bimrace.com"
PHONE  = "+91 75079 58364"
TEL    = "+917507958364"
ENTITY = "BIMRACE PVT LTD"
THEME  = "#F2F5F8"

WORD_D = re.search(r'<path d="(.*?)"', (ROOT / "logo.svg").read_text(), re.S).group(1)
WORD_TF = "scale(0.3333333) translate(0,306) scale(0.25,-0.25)"


# ============================================================================
#  status badges — the honesty system
# ============================================================================
BADGE = {
    "live": ("b--live", "Live"),
    "dev":  ("b--dev",  "In development"),
    "road": ("b--road", "Roadmap"),
    "demo": ("b--demo", "Demo data"),
}


def B(kind, label=None):
    cls, text = BADGE[kind]
    return f'<span class="b {cls}">{label or text}</span>'


# --------------------------------------------------------------- navigation --
# Two menus, both grouped. A visitor who arrives knowing they need HVAC design
# has to reach it from the top bar without reading anything else first, so the
# service menu lists the disciplines under their ordinary names. An entry with no
# href renders as a group heading rather than a link.
SERVICES_MENU = [
    (None, "MEP engineering", None, None),
    ("services/mep-engineering-services.html", "MEP engineering",
     "All four disciplines designed as one connected system.", "live"),
    ("services/hvac-bim-services.html", "HVAC design",
     "Heating, ventilation and air-conditioning systems, ductwork and equipment.", "live"),
    ("services/electrical-bim-services.html", "Electrical design",
     "Power, lighting, containment and LV distribution.", "live"),
    ("services/plumbing-public-health-bim.html", "Plumbing &amp; public health",
     "Water supply, drainage and public health systems.", "live"),
    ("services/fire-protection-bim-services.html", "Fire protection",
     "Sprinkler, detection and suppression systems.", "live"),
    (None, "BIM services", None, None),
    ("services/bim-modelling-documentation.html", "BIM modelling &amp; documentation",
     "Discipline models, with drawings and schedules taken from the model.", "live"),
    ("services/revit-services.html", "Revit MEP",
     "Templates, families, MEP authoring and parameter schemas.", "live"),
    ("services/bim-coordination-clash-detection.html", "MEP coordination &amp; clash detection",
     "Federated models, clearance checks and issues tracked to closure.", "live"),
    ("services/construction-support-bim.html", "Construction support",
     "Shop drawings, builders work and as-built models.", "live"),
    (None, "Digital engineering", None, None),
    ("services/bim-automation-services.html", "BIM automation",
     "Automated model checking, quantities and documentation.", "live"),
    ("automation.html", "AI-assisted workflows",
     "Where automation drafts, and where the engineer signs.", "dev"),
    ("technology/mcp-for-revit.html", "MCP for Revit",
     "Connecting AI assistants to model data through a governed protocol.", "road"),
    ("engineering.html", "All services",
     "Every service group and deliverable in one place.", None),
]

TECHNOLOGY_MENU = [
    ("technology.html", "BIM standards &amp; QA",
     "How we model, and the checks a deliverable passes before issue.", None),
    ("intelligence.html", "BIM intelligence",
     "Treating the model as an engineering database, not a drawing.", "live"),
    ("automation.html", "AI &amp; automation",
     "Automated checking and drafting, with an engineer accountable for the output.", "dev"),
    ("technology/mcp-for-revit.html", "MCP for Revit",
     "Connecting AI assistants to model data through a governed protocol.", "road"),
    ("digital-twin.html", "Digital twin",
     "What a twin actually requires, and what we have not built.", "road"),
    ("platform.html", "Capability status",
     "Live, in development or roadmap — published so you can audit it.", None),
]

NAV = [
    ("engineering.html", "Services",             SERVICES_MENU),
    ("industries.html",  "Industries",           None),
    ("projects.html",    "Projects",             None),
    ("technology.html",  "BIM &amp; Technology", TECHNOLOGY_MENU),
    ("insights.html",    "Insights",             None),
    ("about.html",       "About",                None),
    ("contact.html",     "Contact",              None),
]


def head(title, desc, slug, extra=""):
    canon = f"{SITE}/" if slug == "index" else f"{SITE}/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{THEME}">
<meta name="color-scheme" content="light">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">

<meta property="og:type" content="website">
<meta property="og:locale" content="en">
<meta property="og:site_name" content="BIMRACE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">

<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<svg class="svg-defs" aria-hidden="true" focusable="false"><defs>
  <g id="wm" fill="currentColor" transform="{WORD_TF}"><path d="{WORD_D}"/></g>
</defs></svg>
"""


def chrome(active):
    caret = ('<svg viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" '
             'stroke="currentColor" stroke-width="1.6"/></svg>')
    items = []
    for href, label, sub in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if sub:
            mid = "menu-" + re.sub(r"[^a-z]", "", label.lower())[:6]
            rows = []
            for a, t, d, st in sub:
                if a is None:                    # a group heading, not a link
                    rows.append(f'          <li class="submenu__h">{t}</li>')
                else:
                    rows.append(
                        f'          <li><a href="{a}"><span class="t">{t}'
                        f'{(" " + B(st)) if st else ""}</span>'
                        f'<span class="d">{d}</span></a></li>')
            links = "\n".join(rows)
            grouped = any(a is None for a, _, _, _ in sub)
            cls = " submenu--cols" if grouped else (" submenu--wide" if len(sub) > 6 else "")
            items.append(f"""      <li class="has-menu" data-open="false">
        <button type="button" aria-expanded="false" aria-controls="{mid}">{label}{caret}</button>
        <ul class="submenu{cls}" id="{mid}">
{links}
        </ul>
      </li>""")
        else:
            items.append(f'      <li><a href="{href}"{cur}>{label}</a></li>')
    nav_items = "\n".join(items)

    return f"""
<header class="nav">
  <div class="shell nav__in">
    <a class="brand" href="index.html" aria-label="BIMRACE — home">
      <svg class="brand__logo" viewBox="0 0 876 102" role="img" aria-label="BIMRACE"><use href="#wm"/></svg>
      <span class="brand__sub">MEP &amp; BIM<br>Engineering</span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav__links" id="nav-links">
{nav_items}
        <li class="nav__cta"><a href="contact.html">Discuss your project</a></li>
      </ul>
    </nav>
    <button class="nav__toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
"""


CTA = f"""
<section class="cta">
  <div class="shell cta__in">
    <div>
      <p class="eyebrow">Engineering enquiry</p>
      <h2>Tell us about your project.</h2>
      <p>Send a scope, a drawing set or an information requirement. You will get a technical
      response on approach, disciplines and deliverables — from an engineer, not a sales desk.</p>
      <div class="cta__actions">
        <a class="btn btn--primary btn--lg" href="contact.html">Discuss your project</a>
        <a class="btn btn--ghost btn--lg" href="engineering.html">Explore our services</a>
      </div>
    </div>
    <dl class="cta__side">
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
      <dt>Response</dt><dd>Within two working days</dd>
      <dt>Reaches</dt><dd>Somnath Baste, Founder</dd>
    </dl>
  </div>
</section>
"""


def footer():
    return f"""
<footer class="foot">
  <div class="shell">
    <div class="foot__top">
      <div class="foot__brand">
        <svg class="foot__logo" viewBox="0 0 876 102" role="img" aria-label="BIMRACE"><use href="#wm"/></svg>
        <p class="foot__tagline">MEP engineering and BIM services for complex building projects
        — design, modelling, coordination and documentation.</p>
        <p class="foot__entity">{ENTITY}</p>
        <p class="foot__contact">
          Somnath Baste, Founder<br>
          <a class="foot__link" href="tel:{TEL}">{PHONE}</a><br>
          <a class="foot__link" href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
      <div class="foot__cols">
        <nav class="foot__col" aria-labelledby="f-svc"><h2 id="f-svc">Services</h2><ul>
{foot_links(SERVICES_FOOT)}
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-plat"><h2 id="f-plat">BIM &amp; technology</h2><ul>
          <li><a href="technology.html">BIM standards &amp; QA</a></li>
          <li><a href="intelligence.html">BIM intelligence</a></li>
          <li><a href="automation.html">AI &amp; automation</a></li>
          <li><a href="technology/mcp-for-revit.html">MCP for Revit</a></li>
          <li><a href="digital-twin.html">Digital twin</a></li>
          <li><a href="platform.html#status">Capability status</a></li>
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-ind"><h2 id="f-ind">Industries</h2><ul>
{foot_links(INDUSTRIES_FOOT)}
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-loc"><h2 id="f-loc">Where we work</h2><ul>
{foot_links(LOCATIONS_FOOT)}
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-co"><h2 id="f-co">Company</h2><ul>
          <li><a href="about.html">About</a></li>
          <li><a href="engineering.html">All services</a></li>
          <li><a href="projects.html">Projects</a></li>
          <li><a href="insights.html">Insights</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-leg"><h2 id="f-leg">Legal</h2><ul>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="terms.html">Terms of Use</a></li>
          <li><a href="cookies.html">Cookie Policy</a></li>
        </ul></nav>
      </div>
    </div>
    <div class="foot__rule" aria-hidden="true"></div>
    <div class="foot__bottom">
      <p>© 2026 Bimrace Pvt Ltd. All rights reserved.</p>
      <p class="foot__meta">MEP engineering · BIM modelling · Coordination · Documentation</p>
    </div>
  </div>
</footer>

<script src="config.js"></script>
<script src="script.js" defer></script>
<script src="lead-capture.js" defer></script>
</body>
</html>
"""


# ----------------------------------------------------------------- routing --
# Pages are authored with bare relative hrefs ("engineering.html#mep") because
# that is how the content reads. They are rewritten to root-relative on the way
# out, which is the only thing that lets a page live in /services/ and still
# resolve the same link. Do not hand-write a leading slash in page content.
REL_HREF = re.compile(r'\b(href|src)="(?!/|#|https?:|mailto:|tel:|data:)([^"]*)"')

# The build registry. Every indexable page appends itself here, and the sitemap
# is generated from it — so a new page cannot be forgotten by the sitemap, and
# the sitemap cannot list a page that was never built.
REGISTRY = []


def page(slug, title, desc, body, active, cta=True, extra="", index=True, cta_block=None):
    html = head(title, desc, slug, extra) + chrome(active) + '\n<main id="main">\n' + body \
        + '\n</main>\n' + ((cta_block or CTA) if cta else "") + footer()
    html = REL_HREF.sub(lambda m: f'{m.group(1)}="/{m.group(2)}"', html)
    out = OUT / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    if index:
        REGISTRY.append("" if slug == "index" else f"{slug}.html")
    return slug


def phero(crumbs, h1, lede, meta=None):
    trail = '\n'.join(
        f'        <a href="{h}">{t}</a><span aria-hidden="true">/</span>' if h
        else f'        <span aria-current="page">{t}</span>' for t, h in crumbs)
    m = ""
    if meta:
        m = '<dl class="phero__meta">' + "".join(
            f"<dt>{k}</dt><dd>{v}</dd>" for k, v in meta) + "</dl>"
    return f"""<section class="phero">
  <div class="shell phero__in">
    <div>
      <nav class="crumb" aria-label="Breadcrumb">
{trail}
      </nav>
      <h1>{h1}</h1>
      <p class="phero__lede">{lede}</p>
    </div>
    <div>{m}</div>
  </div>
</section>"""


def breadcrumb_ld(items):
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             "item": f"{SITE}/{u}" if u else f"{SITE}/"}
            for i, (n, u) in enumerate(items)]
    }, indent=2) + '</script>\n')


def strip_tags(s):
    """Schema values are plain text. Badges and entities do not belong in JSON-LD."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).replace("&amp;", "&") \
        .replace("&mdash;", "—").replace("&rarr;", "→").replace("&hellip;", "…").strip()


def faq_ld(pairs):
    """FAQPage from the same list that renders the visible FAQ block. The two
    cannot disagree, because there is only one source."""
    return ('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                        "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                       for q, a in pairs]
    }, indent=2) + '</script>\n')


def service_ld(name, desc, url, area=None, service_type=None):
    d = {"@context": "https://schema.org", "@type": "Service",
         "name": strip_tags(name), "description": strip_tags(desc),
         "url": f"{SITE}/{url}",
         "provider": {"@type": "Organization", "name": "BIMRACE",
                      "url": SITE + "/", "email": EMAIL}}
    if service_type:
        d["serviceType"] = service_type
    if area:
        d["areaServed"] = [{"@type": "Country", "name": a} for a in area]
    return '<script type="application/ld+json">' + json.dumps(d, indent=2) + '</script>\n'


def faq_block(pairs, title="Questions we are asked at enquiry stage",
              eyebrow="FAQ", lede=None):
    """A <details> list. No JavaScript, keyboard-operable for free, and the
    answer text is in the DOM for a crawler whether or not it is open."""
    rows = "\n".join(
        f"""      <details class="faq__i">
        <summary>{q}</summary>
        <div class="faq__a"><p>{a}</p></div>
      </details>""" for q, a in pairs)
    l = f'      <p class="sec-lede">{lede}</p>\n' if lede else ""
    return f"""
<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="sec-title">{title}</h2>
{l}    </header>
    <div class="faq">
{rows}
    </div>
  </div>
</section>"""


def related_block(title, links, eyebrow="Related"):
    """Deliberate internal linking. Every leaf page points sideways to its
    siblings and up to its cluster hub — orphan pages are the default failure
    mode of a site that grows by adding landing pages."""
    items = "\n".join(
        f'      <a class="rel__i" href="{h}"><span class="rel__t">{t}</span>'
        f'<span class="rel__d">{d}</span></a>' for h, t, d in links)
    return f"""
<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">{eyebrow}</p>
      <h2 class="sec-title">{title}</h2>
    </header>
    <div class="rel">
{items}
    </div>
  </div>
</section>"""


def cta_band(heading, body, primary=("contact.html", "Discuss your project"),
             secondary=("engineering.html", "See what is delivered"), prefill=None):
    """A contextual conversion band. The prefill parameter carries the enquiry
    form's service selection through the query string, so a visitor arriving
    from the HVAC page does not have to re-state why they are here."""
    ph = primary[0] + (f"?service={prefill}" if prefill else "")
    return f"""
<section class="cta">
  <div class="shell cta__in">
    <div>
      <p class="eyebrow">Engineering enquiry</p>
      <h2>{heading}</h2>
      <p>{body}</p>
      <div class="cta__actions">
        <a class="btn btn--primary btn--lg" href="{ph}">{primary[1]}</a>
        <a class="btn btn--ghost btn--lg" href="{secondary[0]}">{secondary[1]}</a>
      </div>
    </div>
    <dl class="cta__side">
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
      <dt>Response</dt><dd>Within two working days</dd>
      <dt>Reaches</dt><dd>Somnath Baste, Founder</dd>
    </dl>
  </div>
</section>
"""


# ============================================================================
#  shared content blocks
# ============================================================================

STATUS_LEGEND = f"""
    <div class="badge-legend">
      <div>{B('live')}
        <p>Delivered on client appointments today. If you appoint us this week, this is what
        arrives.</p></div>
      <div>{B('dev')}
        <p>Being built now and used internally on our own delivery. Not a released product, not
        licensable, and no date is committed.</p></div>
      <div>{B('road')}
        <p>Intended direction. Not built. Published so the architecture is legible, not so it can
        be sold.</p></div>
      <div>{B('demo')}
        <p>Simulated content shown on this website for illustration. Not a client project, not a
        real measurement.</p></div>
    </div>"""


STACK_LAYERS = [
    ("01", "BIM DATA", "live", "The structured engineering record",
     "Models authored so their data is queryable from the outset — parameters populated during "
     "authoring rather than retro-fitted before handover. This layer is a service you can appoint "
     "today, and it is the precondition for every layer above it.",
     [("Revit", "mech"), ("IFC", "mech"), ("Parameters", ""), ("Families", ""), ("Systems", ""),
      ("Geometry", ""), ("Schedules", ""), ("Quantities", ""), ("Classification", "")]),

    ("02", "ENGINEERING INTELLIGENCE", "live", "Discipline knowledge encoded as rules",
     "What a competent engineer checks, written down as rule sets a machine can apply — clearances, "
     "sizing bands, system logic, access requirements, standards. This is the layer most BIM "
     "providers do not have, because it needs engineers rather than modellers.",
     [("HVAC", "elec"), ("Plumbing", "plumb"), ("Fire protection", "struct"),
      ("Electrical", "elec"), ("Public health", "plumb"), ("Hydraulic", "plumb"),
      ("Loads", ""), ("Clearances", "")]),

    ("03", "AI ENGINE", "dev", "Reading the model and reasoning about it",
     "Extraction of elements, parameters, systems and relationships as structured data, then "
     "pattern and anomaly detection over it. In development and used internally on our own "
     "delivery. It proposes; it does not decide.",
     [("Model understanding", "mech"), ("Pattern detection", "mech"), ("Rule reasoning", ""),
      ("Anomaly detection", ""), ("Risk classification", ""), ("Prioritisation", "")]),

    ("04", "AUTOMATION ENGINE", "live", "Execution of what has been validated",
     "The repetitive production and checking work, run as scripted and parametric routines. This "
     "has been live in our delivery since before we called it a platform — Dynamo, custom checking "
     "tools and data routines are how the work already gets done.",
     [("Parameter updates", "mech"), ("Model checking", "mech"), ("Documentation", ""),
      ("Schedules", ""), ("Data extraction", ""), ("Reports", ""), ("QA routines", "")]),

    ("05", "ENGINEERING OUTPUT", "live", "What actually leaves the building",
     "Coordinated models, drawings, schedules, quantities and reports — issued through a common "
     "data environment with the correct status codes, signed by a named engineer who is accountable "
     "for them.",
     [("Coordinated BIM", "mech"), ("Calculations", ""), ("Drawings", ""), ("Schedules", ""),
      ("BOQ", ""), ("QA reports", ""), ("Compliance", ""), ("Project data", "")]),
]


def stack_block(compact=False):
    rows = []
    for n, name, status, sub, desc, tags in STACK_LAYERS:
        chips = "".join(
            f'<span class="tag{" tag--" + c if c else ""}">{t}</span>' for t, c in tags)
        rows.append(f"""      <article class="layer" tabindex="0">
        <div class="layer__in">
          <div class="layer__n">LAYER {n}<b>{name}</b></div>
          <div>
            <h3>{sub}</h3>
            <p class="layer__d">{desc}</p>
            <p style="margin-top:14px">{B(status)}</p>
          </div>
          <div class="layer__tags">{chips}</div>
        </div>
      </article>""")
    flow = '\n      <p class="stack__flow">DATA FLOWS UP · ACCOUNTABILITY FLOWS DOWN</p>\n'
    return '    <div class="stack">\n' + ("\n" + flow).join(rows) + "\n    </div>"


AGENTS = [
    ("BIM Analyst", "dev",
     "Reads a model and answers structured questions about what is in it — element counts by "
     "system, parameter completeness, where a given family is used and how systems connect.",
     "Federated model, project parameter schema",
     "Resolve elements to systems, then systems to disciplines",
     "Structured model inventory with element IDs"),
    ("Coordination", "dev",
     "Tests the federated model against clearance, access and zoning rules, then classifies what it "
     "finds by discipline, severity and who has to move.",
     "Federated model, clearance and zoning rule set",
     "Geometric test, then classify by cause rather than by count",
     "Prioritised issue list, grouped by responsible discipline"),
    ("MEP Engineering", "road",
     "Assists with sizing, load and system-performance checks by reading design parameters off the "
     "model instead of re-entering them into a spreadsheet.",
     "System parameters, design criteria, equipment schedule",
     "Apply sizing and load rules to the as-modelled network",
     "Calculation sheet reconciled against the model"),
    ("QA / QC", "dev",
     "Runs the project rule set over the model before issue — naming, classification, parameter "
     "completeness, view and sheet organisation, status codes.",
     "Model, project rule set, level of information need",
     "Test every rule, then cluster failures to find the root cause",
     "QA report with an element ID against every finding"),
    ("Documentation", "dev",
     "Handles the repetitive parts of drawing and schedule production that are fully determined by "
     "the model, so engineers spend their time on the parts that are not.",
     "Model, sheet standard, drawing register",
     "Derive views and schedules from model state",
     "Draft sheets and schedules for engineer review"),
    ("Quantity", "dev",
     "Extracts and classifies quantities directly from model geometry and parameters, with the "
     "measurement rule visible for each line.",
     "Model, classification system, measurement rules",
     "Measure from geometry, classify, reconcile against schedules",
     "Structured quantity export with traceable lines"),
    ("Design Optimisation", "road",
     "Evaluates design alternatives against stated engineering criteria — routing options, "
     "equipment selections, spatial strategies — and shows the trade-offs.",
     "Design intent, constraints, evaluation criteria",
     "Generate options, score against criteria, expose trade-offs",
     "Ranked options with the reasoning shown"),
    ("Project Intelligence", "road",
     "Turns model and project data into decisions a project manager can act on — where change is "
     "concentrating, which systems are unstable, what is not converging.",
     "Model history, issue tracker, delivery plan",
     "Correlate model change against programme and issues",
     "Project signals with the underlying evidence attached"),
]

AGENT_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10" '
              'stroke-linecap="round"/></svg>')


def agents_block():
    cards = []
    for name, status, desc, i, r, o in AGENTS:
        cards.append(f"""      <article class="agent">
        <div class="agent__top">
          <span class="agent__ico">{AGENT_ICON}</span>
          {B(status)}
        </div>
        <h3>{name} Agent</h3>
        <p class="agent__d">{desc}</p>
        <dl class="agent__io">
          <div><dt>Input</dt><dd>{i}</dd></div>
          <div><dt>Reasoning</dt><dd>{r}</dd></div>
          <div><dt>Output</dt><dd>{o}</dd></div>
        </dl>
      </article>""")
    return '    <div class="agents">\n' + "\n".join(cards) + "\n    </div>"


CHAIN = """
    <div class="chain">
      <div><p class="chain__n">01 INPUT</p><h3>Model and rules</h3>
        <p>Structured model data plus the engineering rule set that governs it.</p></div>
      <div><p class="chain__n">02 REASON</p><h3>Analysis</h3>
        <p>Resolve relationships, test against rules, detect what does not fit.</p></div>
      <div><p class="chain__n">03 VALIDATE</p><h3>Engineering rules</h3>
        <p>Findings checked against discipline criteria, not just geometry.</p></div>
      <div><p class="chain__n">04 AUTOMATE</p><h3>Execution</h3>
        <p>Validated actions run as routines. Drafts, never silent model edits.</p></div>
      <div><p class="chain__n">05 APPROVE</p><h3>Engineer signs</h3>
        <p>A named engineer accepts, amends or rejects. Nothing issues without this.</p></div>
    </div>"""


FLOWS = [
    ("01", "Model QA", "live",
     "The standards pass that has to happen before every issue, run as a rule set instead of a "
     "person opening views one at a time.",
     ["Parameter validation", "Naming checks", "Family audit", "System integrity"],
     "QA report with an element ID against every finding, and failures clustered so you fix the "
     "template rather than 241 elements."),
    ("02", "Clash intelligence", "live",
     "Clash detection produces a number. Clash intelligence produces a decision — what actually "
     "conflicts, why, and whose model has to move.",
     ["Detect", "Classify", "Prioritise", "Route"],
     "Issue list grouped by cause and responsible discipline, with clearance and access failures "
     "separated from true hard clashes."),
    ("03", "Engineering calculations", "live",
     "Sizing and load calculations driven from model parameters rather than re-keyed into a "
     "spreadsheet that then drifts from the model.",
     ["Read", "Calculate", "Validate", "Report"],
     "Calculation output reconciled against the as-modelled network, so the two cannot silently "
     "disagree."),
    ("04", "Documentation", "live",
     "Drawings and schedules derived from model state, so a model change and a drawing change are "
     "the same event.",
     ["Model", "Extract", "Generate", "Review"],
     "Draft sheets and schedules ready for engineering review, with the model as the single "
     "source."),
    ("05", "Quantity intelligence", "live",
     "Quantities measured from geometry and parameters, classified, and traceable back to the "
     "elements they came from.",
     ["Measure", "Classify", "Reconcile", "Export"],
     "Structured quantity export where every line can be traced to the elements behind it."),
    ("06", "Design automation", "dev",
     "Generating model content from engineering intent and rules — routing, supports, penetrations "
     "and repeated typologies.",
     ["Intent", "Rules", "Generate", "Validate"],
     "Generated content presented for engineering acceptance. In development; used on our own "
     "delivery, not offered as a product."),
]


def flows_block():
    cards = []
    for n, name, status, desc, seq, out in FLOWS:
        chips = ' <i>&rarr;</i> '.join(f"<span>{s}</span>" for s in seq)
        cards.append(f"""      <article class="flow">
        <div class="flow__top"><span class="flow__n">{n}</span>{B(status)}</div>
        <h3>{name}</h3>
        <p>{desc}</p>
        <div class="flow__seq">{chips}</div>
        <p class="flow__out"><b>Output</b>{out}</p>
      </article>""")
    return '    <div class="flows">\n' + "\n".join(cards) + "\n    </div>"


MATRIX = [
    ("eng", "01", "Engineering", "Building services engineering with real discipline depth. This is "
     "the layer that makes the rest defensible.", [
        ("MEP engineering", "live"), ("HVAC and ductwork", "live"),
        ("Public health and drainage", "live"), ("Fire protection", "live"),
        ("Electrical distribution", "live"), ("Engineering calculations", "live"),
        ("Equipment selection", "live"), ("System analysis", "live"),
     ], "engineering.html#mep"),
    ("bim", "02", "BIM", "Model authoring, coordination and documentation — structured so the data "
     "inside is usable, not only viewable.", [
        ("BIM modelling", "live"), ("BIM coordination", "live"),
        ("Clash detection", "live"), ("Model QA / QC", "live"),
        ("Documentation", "live"), ("Quantity extraction", "live"),
        ("Revit and IFC exchange", "live"), ("CDE and delivery", "live"),
     ], "engineering.html#modelling"),
    ("int", "03", "Intelligence", "The layer we are building. Automation is a service category "
     "here, not a footnote on a modelling proposal.", [
        ("Design automation", "dev"), ("Engineering automation", "live"),
        ("Model intelligence", "dev"), ("Automated QA rule sets", "live"),
        ("AI engineering agents", "dev"), ("Generative workflows", "road"),
        ("Digital twin", "road"), ("Predictive engineering", "road"),
     ], "automation.html"),
]


def matrix_block():
    cols = []
    for cls, n, name, desc, items, href in MATRIX:
        lis = "\n".join(f'          <li>{t} {B(s)}</li>' for t, s in items)
        cols.append(f"""      <div class="mcol mcol--{cls}">
        <div class="mcol__h">
          <p class="mcol__n">CATEGORY {n}</p>
          <h3>{name}</h3>
          <p>{desc}</p>
        </div>
        <ul class="mcol__b">
{lis}
        </ul>
        <div class="mcol__f"><a class="card__more" href="{href}">Scope detail &rarr;</a></div>
      </div>""")
    return '    <div class="matrix">\n' + "\n".join(cols) + "\n    </div>"


MATURITY = [
    ("01", "Digital BIM", "on", "Structured models replace drawings as the source of truth.",
     "Standard practice"),
    ("02", "BIM automation", "on", "Rules and scripts take over repetitive production and checking.",
     "Where we deliver"),
    ("03", "AI-assisted engineering", "part",
     "Model data is read and reasoned over to support engineering decisions.",
     "In development"),
    ("04", "AI engineering agents", "part",
     "Defined workflows run end to end, drafting output for engineering approval.",
     "Partially, internally"),
    ("05", "Engineering intelligence", "", "BIM, AI, automation and project data connected as one "
     "system across a portfolio.", "Direction, not a claim"),
]


def maturity_block():
    cells = []
    for n, name, state, desc, pos in MATURITY:
        cls = " mat__l--on" if state == "on" else (" mat__l--part" if state == "part" else "")
        cells.append(f"""      <div class="mat__l{cls}">
        <p class="mat__n">LEVEL {n}</p>
        <h3>{name}</h3>
        <p>{desc}</p>
        <p class="mat__pos">{pos}</p>
      </div>""")
    return '    <div class="mat">\n' + "\n".join(cells) + "\n    </div>"


CONSOLE = f"""
    <div class="panel" id="console">
      <div class="panel__bar">
        <span><b>BIMRACE</b> / ENGINEERING INTELLIGENCE CONSOLE</span>
        <span>{B('demo', 'Simulated')}</span>
      </div>
      <div class="console">
        <div class="console__l">
          <dl class="console__meta">
            <div><dt>Project</dt><dd>DEMO_PROJECT_01</dd></div>
            <div><dt>Model</dt><dd>MEP_COORDINATION_R04</dd></div>
            <div><dt>Query</dt><dd id="console-query">&nbsp;</dd></div>
          </dl>
          <div class="console__grid" id="console-metrics"></div>
        </div>
        <div>
          <div class="log" id="console-log" aria-live="polite" aria-label="Simulated analysis log"></div>
        </div>
      </div>
      <div class="console__act">
        <button type="button" data-scenario="fire" aria-pressed="false">Fire protection coordination</button>
        <button type="button" data-scenario="chw" aria-pressed="false">Chilled water system</button>
        <button type="button" data-scenario="qa" aria-pressed="false">Model QA pass</button>
      </div>
      <div class="panel__foot">
        <span>SIMULATED SESSION — NO MODEL IS CONNECTED TO THIS PAGE</span>
        <span>FIGURES ARE FABRICATED FOR ILLUSTRATION</span>
      </div>
    </div>"""


CASE_ANATOMY = f"""
      <article class="case">
        <div class="case__h">
          <div>
            <p class="case__k">Case study anatomy</p>
            <h3>Every published case study will answer these six questions, in this order.</h3>
          </div>
          {B('live', 'Structure fixed')}
        </div>
        <div class="case__b">
          <div class="case__c"><h3>01 Project</h3>
            <ul><li>Building type and size</li><li>Location and jurisdiction</li>
            <li>Stage at appointment</li><li>Project team</li></ul></div>
          <div class="case__c"><h3>02 Challenge</h3>
            <p>The problem in the client's terms &mdash; what was slow, repetitive, unreliable or
            unresolvable at the scale of the project.</p></div>
          <div class="case__c"><h3>03 Our scope</h3>
            <ul><li>Disciplines engineered</li><li>Modelling and coordination scope</li>
            <li>Level of information need</li><li>What stayed with others</li></ul></div>
          <div class="case__c"><h3>04 Approach</h3>
            <ul><li>How the systems were designed</li><li>How the model was structured</li>
            <li>What was automated, and what was not</li><li>Where the engineer reviewed</li></ul></div>
          <div class="case__c"><h3>05 Deliverables</h3>
            <ul><li>Drawings and schedules issued</li><li>Models and formats handed over</li>
            <li>Reports and issue records</li><li>Dates and revisions</li></ul></div>
          <div class="case__c case__c--impact"><h3>06 Outcome</h3>
            <p>Measured against a stated baseline, with the measurement method named. Where a number
            cannot be verified, the case study will say so rather than estimate one.</p></div>
        </div>
        <div class="case__f">Failures and dead ends will be published alongside successes. A case
        study library with no failures in it is a brochure.</div>
      </article>"""


# ============================================================================
#  HOME
# ============================================================================
# The homepage answers five questions in order: what this company is, what it
# does, who it does it for, what you actually receive, and what to do next.
# Everything that explains *how* the work is done — the intelligence stack, the
# agents, the automation flows, the console — lives on platform.html,
# automation.html, intelligence.html and engineering.html, which is where a
# visitor who has decided they care about the method will go looking. Repeating
# those sections here is what made the old homepage unreadable: it opened with
# the method and never stated the business.

SERVICE_GROUPS = [
    ("MEP engineering", "mep",
     "We design the building services: heating and cooling, power and lighting, "
     "water and drainage, and fire protection.",
     [("services/hvac-bim-services.html", "HVAC design",
       "Heating, ventilation and air-conditioning, ductwork and plant."),
      ("services/electrical-bim-services.html", "Electrical design",
       "Power, lighting, containment and LV distribution."),
      ("services/plumbing-public-health-bim.html", "Plumbing &amp; public health",
       "Water supply, drainage and public health systems."),
      ("services/fire-protection-bim-services.html", "Fire protection",
       "Sprinkler, detection and suppression systems.")]),
    ("BIM services", "bim",
     "We build and coordinate the models those systems live in, and produce the "
     "drawings and schedules from them.",
     [("services/bim-modelling-documentation.html", "BIM modelling &amp; documentation",
       "Discipline models, drawings and schedules."),
      ("services/revit-services.html", "Revit MEP",
       "Templates, families, authoring and parameter schemas."),
      ("services/bim-coordination-clash-detection.html", "MEP coordination &amp; clash detection",
       "Federated models, clearance checks, issues to closure."),
      ("services/construction-support-bim.html", "Construction support",
       "Shop drawings, builders work and as-built models.")]),
    ("Digital engineering", "digital",
     "Where it saves an engineer time, we automate the repetitive parts of the "
     "work above. An engineer still signs the result.",
     [("services/bim-automation-services.html", "BIM automation",
       "Automated model checking, quantities and documentation."),
      ("automation.html", "AI-assisted workflows",
       "Analysis that drafts findings for an engineer to accept or reject."),
      ("technology/mcp-for-revit.html", "MCP for Revit",
       "Connecting AI assistants to model data through a governed protocol.")]),
]


def service_groups_block():
    """The three service groups, each a heading a non-specialist can parse and a
    short list of the disciplines under it. This is the section that has to pass
    the ten-second test for a visitor who arrived knowing they need HVAC."""
    out = []
    for name, gid, lede, rows in SERVICE_GROUPS:
        links = "\n".join(
            f'        <a class="sgrp__i" href="{h}"><span class="sgrp__t">{t}</span>'
            f'<span class="sgrp__d">{d}</span></a>' for h, t, d in rows)
        out.append(f"""    <div class="sgrp" id="{gid}">
      <div class="sgrp__head">
        <h3>{name}</h3>
        <p>{lede}</p>
      </div>
      <div class="sgrp__list">
{links}
      </div>
    </div>""")
    return '  <div class="sgrps">\n' + "\n".join(out) + "\n  </div>"


AUDIENCES = [
    ("Architects",
     "You need an MEP strategy that respects the design, and services that fit "
     "the ceiling and riser space you have actually allowed for.",
     "We design the systems and model them into your building so the "
     "coordination problems surface on screen rather than on site."),
    ("Contractors",
     "You need coordinated MEP information before you build, not a model that "
     "disagrees with the drawings you were issued.",
     "We coordinate the disciplines, resolve the clashes and issue drawings and "
     "schedules taken from the model that produced them."),
    ("Developers",
     "You need the building services designed and coordinated in a way that "
     "supports your programme and your cost plan.",
     "We deliver the design and the model as one package, so a change in the "
     "design is visible in the quantities rather than discovered later."),
    ("Engineering consultants",
     "You need overflow capacity, or BIM production depth, without losing "
     "control of the engineering.",
     "We work to your standards and templates as an extension of your team, and "
     "your engineer remains the one who signs."),
]


def audience_block():
    rows = "\n".join(
        f"""      <article class="aud">
        <h3>{n}</h3>
        <p class="aud__p"><b>What you need.</b> {need}</p>
        <p class="aud__d"><b>What we do.</b> {does}</p>
      </article>""" for n, need, does in AUDIENCES)
    return '    <div class="auds">\n' + rows + "\n    </div>"


DELIVERS = [
    ("Design", "MEP engineering design",
     "Load calculations, system selection, sizing and layouts for mechanical, "
     "electrical, public health and fire protection."),
    ("Model", "BIM and Revit modelling",
     "Discipline models authored to the level of detail the stage needs, with "
     "the data in them rather than bolted on afterwards."),
    ("Coordinate", "MEP coordination and clash detection",
     "Federated models, clash and clearance checking, and a tracked route from "
     "an issue being raised to it being closed."),
    ("Document", "Drawings, schedules and reports",
     "Deliverables generated from the coordinated model, so the drawing and the "
     "model cannot tell you two different things."),
    ("Optimise", "Automation and AI-assisted checking",
     "Repetitive checking and take-off run automatically. An engineer reviews "
     "and signs the output."),
]


def delivers_block():
    rows = "\n".join(
        f"""      <div class="dlv">
        <span class="dlv__n">0{i + 1}</span>
        <div>
          <p class="dlv__k">{k}</p>
          <h3>{t}</h3>
          <p class="dlv__d">{d}</p>
        </div>
      </div>""" for i, (k, t, d) in enumerate(DELIVERS))
    return '    <div class="dlvs">\n' + rows + "\n    </div>"


HOME_INDUSTRIES = [
    ("industries/commercial.html", "Commercial &amp; offices",
     "Landlord and tenant services, risers, and fit-out coordination."),
    ("industries/residential.html", "Residential &amp; mixed use",
     "Repeatable apartment services, risers and shared plant."),
    ("industries/healthcare.html", "Healthcare",
     "Medical gas, ventilation regimes and resilience requirements."),
    ("industries/hospitality.html", "Hospitality",
     "Guest comfort, acoustic separation and back-of-house plant."),
    ("industries/industrial.html", "Industrial &amp; warehousing",
     "Large-span distribution, process loads and fire protection."),
    ("industries/data-centres.html", "Data centres",
     "Cooling strategy, power resilience and containment density."),
]


def home_industries_block():
    rows = "\n".join(
        f'      <a class="rel__i" href="{h}"><span class="rel__t">{t}</span>'
        f'<span class="rel__d">{d}</span></a>' for h, t, d in HOME_INDUSTRIES)
    return '    <div class="rel">\n' + rows + "\n    </div>"


HOME_REGIONS = [
    ("North America", [("locations/usa.html", "United States"),
                       ("locations/canada.html", "Canada")]),
    ("Europe", [("locations/uk.html", "United Kingdom"),
                ("locations/europe.html", "Europe")]),
    ("Middle East", [("locations/uae.html", "United Arab Emirates"),
                     ("locations/saudi-arabia.html", "Saudi Arabia")]),
    ("Asia-Pacific", [("locations/australia.html", "Australia")]),
]


def home_regions_block():
    rows = []
    for region, places in HOME_REGIONS:
        links = " ".join(
            f'<a href="{h}">{t}</a>' for h, t in places)
        rows.append(f"""          <div class="reg">
            <p class="reg__k">{region}</p>
            <p class="reg__v">{links}</p>
          </div>""")
    return '        <div class="regs">\n' + "\n".join(rows) + "\n        </div>"


HOME = f"""
<section class="hero">
  <div class="hero__bg" aria-hidden="true"></div>
  <div class="shell hero__in">
    <div class="hero__copy">
      <p class="hero__tag hero__tag--plain">MEP engineering &amp; BIM consulting <span>&middot;</span> serving project teams worldwide</p>
      <h1 class="hero__title">MEP engineering and BIM services for complex building projects</h1>
      <p class="hero__lede">BIMRACE designs building services &mdash; heating and cooling, power,
      water and fire protection &mdash; and delivers them as coordinated BIM models, drawings and
      schedules for architects, contractors, developers and engineering teams.</p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="contact.html">Discuss your project</a>
        <a class="btn btn--ghost btn--lg" href="engineering.html">Explore our services</a>
      </div>
      <div class="hero__facts" aria-label="What we do">
        <div class="hero__fact"><span>Design</span><strong>MEP engineering</strong></div>
        <div class="hero__fact"><span>Model</span><strong>BIM &amp; Revit</strong></div>
        <div class="hero__fact"><span>Coordinate</span><strong>Clash detection</strong></div>
        <div class="hero__fact"><span>Document</span><strong>Drawings &amp; schedules</strong></div>
      </div>
    </div>

  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">What we do</p>
      <h2 class="sec-title">We design building services, and we deliver them as coordinated models</h2>
      <p class="sec-lede">Every building needs heating, ventilation, power, water and fire
      protection. Those systems have to fit the building, work together and be documented well
      enough to construct. BIMRACE does the engineering and the BIM that gets that right.</p>
    </header>
{service_groups_block()}
    <p class="tiny" style="margin-top:28px">Not sure which of these you need?
    <a href="contact.html" style="color:var(--sig)">Describe the project</a> and we will tell you
    what the scope should be.</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Who we work with</p>
      <h2 class="sec-title">Who we work with, and what we take off their plate</h2>
      <p class="sec-lede">The reason you would appoint us differs by where you sit on the project.
      Find yourself below.</p>
    </header>
{audience_block()}
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">What you receive</p>
      <h2 class="sec-title">Design &rarr; Model &rarr; Coordinate &rarr; Document</h2>
      <p class="sec-lede">Five steps, in the order they happen on a project. Each one produces
      something you can hold us to.</p>
    </header>
{delivers_block()}
  </div>
</section>

<section class="section">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow">Plain english</p>
      <h2 class="sec-title">What does BIM actually mean?</h2>
      <p class="sec-lede">Building Information Modelling is a way of representing a building and its
      systems digitally, so that the architect, the engineers and the construction team can
      coordinate the information before and during construction &mdash; rather than discovering
      that two systems want the same space once the ceiling is being installed.</p>
      <p class="lede" style="margin-top:22px">In practice it means the ducts, cables, pipes and
      sprinkler mains exist as real objects with real sizes in a shared model, instead of lines on
      separate drawings that nobody has laid over one another. A clash is something you can see and
      fix on screen for the cost of an hour. The same clash found on site costs considerably more.</p>
      <p class="lede" style="margin-top:16px">BIMRACE&rsquo;s role is to do the MEP engineering
      <em>and</em> author that model, so the design decisions and the model agree with each other by
      construction rather than by correction.</p>
      <a class="btn btn--ghost" style="margin-top:30px" href="technology.html">How we model, and to which standards</a>
    </div>
    <div>
      <div class="panel">
        <div class="panel__bar">
          <span><b>BIM</b> / WHY IT MATTERS</span>
        </div>
        <div class="panel__body">
          <div class="spec spec--tight">
            <div class="spec__row"><div class="spec__k"><b>Without a coordinated model</b></div>
              <div class="spec__v">Each discipline draws separately. Conflicts are found by a person
              comparing drawings, or by a contractor on site. Quantities are counted by hand.</div></div>
            <div class="spec__row"><div class="spec__k"><b>With one</b></div>
              <div class="spec__v">The systems occupy real space in a shared model. Conflicts are
              tested before issue. Drawings and schedules come out of the model that was
              coordinated, so they agree with it.</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Sectors</p>
      <h2 class="sec-title">Where we work</h2>
      <p class="sec-lede">The engineering is the same discipline in every sector; the constraints
      and the statutory requirements are not. These are the building types we work on most.</p>
    </header>
{home_industries_block()}
    <a class="btn btn--ghost" style="margin-top:30px" href="industries.html">All sectors</a>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Proof</p>
      <h2 class="sec-title">What we have published, and what we have not</h2>
      <p class="sec-lede">No client has released a case study yet, so there are none on this site.
      Rather than fill the gap with stock imagery and numbers nobody can check, here is the
      structure every published project will follow &mdash; and you can ask for a walkthrough of
      live work at enquiry stage.</p>
    </header>
{CASE_ANATOMY}
    <p class="tiny" style="margin-top:26px">This site publishes no client logos, no project counts
    and no testimonials, because none have been earned and verified yet.
    <a href="projects.html" style="color:var(--sig)">See the projects page</a>.</p>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Why BIMRACE</p>
      <h2 class="sec-title">Stated as things you can check at enquiry stage</h2>
      <p class="sec-lede">Adjectives are free. These are claims you can test in a conversation,
      which is when you should test them.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">01<b>MEP depth, not MEP as an add-on</b></div>
        <div class="spec__v">Building services are the centre of the practice. Mechanical,
        electrical, public health and fire protection are treated as connected systems with real
        spatial constraints, not as coloured tubes in an architectural model.</div></div>
      <div class="spec__row"><div class="spec__k">02<b>Engineering and BIM from one team</b></div>
        <div class="spec__v">The people authoring the model are the people who sized the systems in
        it. You are not managing a design consultant and a modelling bureau who each blame the
        other for the coordination.</div></div>
      <div class="spec__row"><div class="spec__k">03<b>Information-first modelling</b></div>
        <div class="spec__v">Parameters are populated while the model is authored, not retro-fitted
        before handover. It is unglamorous, and it is the reason schedules and automated checks can
        be trusted later.</div></div>
      <div class="spec__row"><div class="spec__k">04<b>Standards-aligned by default</b></div>
        <div class="spec__v">Naming, status codes, federation and delivery are structured to
        ISO&nbsp;19650 principles on every appointment, not only where a client mandates it. We are
        not certified to it and do not claim to be.</div></div>
      <div class="spec__row"><div class="spec__k">05<b>Automation drafts, engineers decide</b></div>
        <div class="spec__v">No routine writes to a live model, closes an issue or issues a
        deliverable. A named engineer accepts, amends or rejects every automated output, and their
        name goes on it.</div></div>
      <div class="spec__row"><div class="spec__k">06<b>Published capability status</b></div>
        <div class="spec__v">Anything on this site that is in development or on the roadmap is
        labelled as such. If you find a claim here we cannot demonstrate at enquiry stage, that is a
        defect and we want to hear about it.</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split split--mid split--rev">
    <div>
      <div class="panel">
        <div class="panel__bar"><span><b>DELIVERY</b> / WORLDWIDE</span></div>
        <div class="panel__body">
{home_regions_block()}
        </div>
      </div>
    </div>
    <div>
      <p class="eyebrow">International delivery</p>
      <h2 class="sec-title">Serving project teams worldwide</h2>
      <p class="sec-lede">BIMRACE works remotely with project teams across North America, Europe,
      the Middle East and Asia-Pacific, to the code and drawing conventions of the project&rsquo;s
      own jurisdiction.</p>
      <p class="lede" style="margin-top:22px">We have one office, in India, and we say so plainly:
      the delivery model is a remote engineering team working to your standards and your programme,
      with overlap arranged around your working day. There are no overseas branches behind the
      pages below.</p>
      <a class="btn btn--ghost" style="margin-top:30px" href="locations.html">How remote delivery works</a>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Engineering + BIM + AI</p>
      <h2 class="sec-title">Automation and AI support the engineering. They do not replace it.</h2>
      <p class="sec-lede">BIMRACE is building internal workflows that connect engineering data, BIM
      models and AI-assisted checking. They make the work faster and more consistent. The business
      is still MEP engineering, BIM coordination and design delivery, and a named engineer is
      accountable for every output. Each capability below is labelled with what it actually is
      today.</p>
    </header>
    <div class="g4">
      <article class="card"><h3>Automated model checking {B('live')}</h3>
        <p>Naming, parameters, clearances and sizing bands tested across the whole model rather than
        the parts someone had time to open.</p>
        <a class="card__more" href="services/bim-automation-services.html">BIM automation</a></article>
      <article class="card"><h3>AI-assisted analysis {B('dev')}</h3>
        <p>Model information read to flag coordination risks and anomalies for an engineer to
        evaluate. It drafts findings; it does not resolve them.</p>
        <a class="card__more" href="automation.html">AI &amp; automation</a></article>
      <article class="card"><h3>MCP for Revit {B('road')}</h3>
        <p>A governed protocol for connecting AI assistants to model data, so a question about the
        model can be asked in words.</p>
        <a class="card__more" href="technology/mcp-for-revit.html">MCP for Revit</a></article>
      <article class="card"><h3>Digital twin {B('road')}</h3>
        <p>A twin needs a model, asset data, live data, engineering rules and analytics. We deliver
        the first two, and structure models so the rest stays possible.</p>
        <a class="card__more" href="digital-twin.html">What a twin requires</a></article>
    </div>
    <p class="tiny" style="margin-top:26px">The full picture, layer by layer, with what is running
    at each one: <a href="platform.html" style="color:var(--sig)">capability status</a>.</p>
  </div>
</section>
"""


# ============================================================================
#  PLATFORM
# ============================================================================
PLATFORM = f"""
{phero([("Home", "index.html"), ("Platform", None)],
       "The BIMRACE intelligence stack",
       "Five layers between an engineering question and an engineering answer. Three are delivered "
       "today, one is in development, and this page publishes the difference along with the legend "
       "we use to describe it.",
       [("Layers", "05"), ("Live today", "01 · 02 · 04 · 05"), ("In development", "03 — AI engine"),
        ("Roadmap", "Digital twin · Generative")])}

<section class="section section--flush" id="status">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Capability status</p>
      <h2 class="sec-title">The legend, published so you can audit us against it</h2>
      <p class="sec-lede">Every capability claim on this website carries one of these four states.
      They appear beside individual line items, not only beside sections, because a section-level
      badge is how vague claims hide.</p>
    </header>
{STATUS_LEGEND}
    <div class="note note--sig" style="max-width:none">
      <p><strong>What this rules out.</strong> No feature on this site is offered for licence. No
      date is committed for anything marked in development or roadmap. Nothing described as an
      agent operates without engineering review. If a page ever contradicts this paragraph, this
      paragraph is correct and the page is a defect.</p>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">The stack</p>
      <h2 class="sec-title">What runs at each layer</h2>
      <p class="sec-lede">Read bottom-up as data and top-down as accountability: model data feeds
      the layers above it, and the engineer at the top is answerable for everything below.</p>
    </header>
{stack_block()}
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Product architecture</p>
      <h2 class="sec-title">How a query becomes an engineering output</h2>
      <p class="sec-lede">The architecture we are building toward. Components are marked with their
      real state below the diagram — several of them are ordinary engineering practice rather than
      software, and that is deliberate.</p>
    </header>
    <div class="panel">
      <div class="panel__bar">
        <span><b>ARCHITECTURE</b> / ORCHESTRATION MODEL</span>
        <span>{B('dev', 'Target architecture')}</span>
      </div>
      <div class="panel__body">
        <svg class="dia" id="platform-svg" viewBox="0 0 900 470" role="img"
          aria-label="Architecture diagram: an orchestration layer connecting Revit and IFC model
          sources, engineering rules, calculation, project data, automation, engineer validation and
          engineering output."></svg>
      </div>
    </div>
    <div class="spec" style="margin-top:var(--s4)">
      <div class="spec__row"><div class="spec__k">Component<b>Model source — Revit / IFC</b>{B('live')}</div>
        <div class="spec__v">Reading models and their data is core delivery work today. Structured
        export, parameter management and IFC exchange are live services.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Engineering rule sets</b>{B('live')}</div>
        <div class="spec__v">Project and practice rules encoded as checkable definitions. Live in
        our QA and coordination workflows now, applied through scripted routines.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Calculation</b>{B('live')}</div>
        <div class="spec__v">Engineering calculation is a delivered service. Driving it from model
        parameters rather than re-keyed spreadsheets is live for some workflows.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Automation engine</b>{B('live')}</div>
        <div class="spec__v">Parametric and scripted routines for production, checking and data
        extraction. This layer predates the platform framing — it is how the work is done.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Model understanding and reasoning</b>{B('dev')}</div>
        <div class="spec__v">Extraction of elements, parameters, systems and relationships as
        structured data, with pattern and anomaly detection over it. In development, used
        internally, not released.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Orchestration</b>{B('dev')}</div>
        <div class="spec__v">Routing a query to the right rules, calculations and routines, and
        recording what was done. Partially built; today a person sequences most of it.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Natural-language query</b>{B('road')}</div>
        <div class="spec__v">Asking questions of model and engineering data in plain English. Not
        built. Shown in the console demonstration on the homepage as a concept only.</div></div>
      <div class="spec__row"><div class="spec__k">Component<b>Engineer validation</b>{B('live')}</div>
        <div class="spec__v">Not software. A named engineer reviews and signs. This is the one
        component we have no intention of automating.</div></div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Maturity model</p>
      <h2 class="sec-title">Where this practice actually sits</h2>
      <p class="sec-lede">A five-level model of AEC engineering maturity, with our honest position
      marked. We deliver at levels one and two, and are working inside three and four. Level five
      is a direction, not a position we hold.</p>
    </header>
{maturity_block()}
    <div class="note" style="max-width:none">
      <p><strong>On level claims.</strong> Every vendor in this sector places itself at the top of
      whichever maturity model it publishes. Ours puts us in the middle, because that is where we
      are. Ask us to demonstrate a level-three or level-four workflow at enquiry stage — that is a
      reasonable request and we will show you the internal tooling rather than a slide.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow">Accountability</p>
      <h2 class="sec-title">AI accelerates engineering. Engineers remain accountable for engineering decisions.</h2>
      <p class="sec-lede">This is not a disclaimer bolted to the bottom of the page. It is a
      structural constraint that shapes what we build and what we refuse to build.</p>
      <p class="lede" style="margin-top:22px">A routine that silently edits a live model removes the
      one thing that makes an engineering deliverable worth anything: a person who is answerable for
      it. So our automation drafts, proposes and reports. It does not commit.</p>
      <p class="lede" style="margin-top:16px">The practical consequence is that our workflows are
      slower than a fully autonomous system would be, and defensible in a way that one would not
      be. That is the trade we have chosen deliberately.</p>
    </div>
    <div>
      <ol class="steps">
        <li class="is-human"><span class="steps__k">Engineer</span><h3>States the intent</h3>
          <p>A scope, a question or a rule set. The engineering judgement about what matters happens
          here, before any automation runs.</p></li>
        <li class="is-ai"><span class="steps__k">System</span><h3>Reads and reasons</h3>
          <p>Model data is resolved, rules applied, anomalies detected and findings classified by
          cause rather than counted.</p></li>
        <li class="is-ai"><span class="steps__k">System</span><h3>Drafts output</h3>
          <p>A report, a schedule, a quantity export or proposed model content — in a reviewable
          state, never written directly to the live model.</p></li>
        <li class="is-human"><span class="steps__k">Engineer</span><h3>Validates</h3>
          <p>Accepts, amends or rejects. Rejections are fed back into the rule set, which is how the
          system gets better rather than more confident.</p></li>
        <li class="is-human"><span class="steps__k">Engineer</span><h3>Issues and signs</h3>
          <p>Through the CDE with the correct status code, under a named person's accountability.</p></li>
      </ol>
    </div>
  </div>
</section>
"""


# ============================================================================
#  BIM INTELLIGENCE
# ============================================================================
INTELLIGENCE = f"""
{phero([("Home", "index.html"), ("Platform", "platform.html"), ("BIM Intelligence", None)],
       "Your BIM model is an engineering database",
       "Turning BIM from a project deliverable into an intelligent engineering data layer — and the "
       "modelling discipline that has to happen first for any of it to be possible.",
       [("Layer", "01 — BIM data"), ("Status", "Live"), ("Depends on", "Information-first authoring"),
        ("Enables", "Automated checking · Analytics")])}

<section class="section section--flush">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow">BIM as data</p>
      <h2 class="sec-title">Information is not the same as intelligence</h2>
      <p class="sec-lede">A model already holds nearly everything a project team needs to know. The
      difficulty is that it holds it passively — stored, opened and interpreted by hand, one view at
      a time.</p>
      <p class="lede" style="margin-top:22px">Move from model coordination to model intelligence and
      the model stops being a thing you look at and becomes a thing you can ask. Element counts by
      system, parameter completeness, clearance failures, quantities with traceable lines — all of
      it is already in there.</p>
      <p class="lede" style="margin-top:16px">BIM is structured engineering context. AI is the
      reasoning layer over it. Automation is the execution layer. None of the second two work if the
      first one is not disciplined.</p>
    </div>
    <div>
      <svg class="dia" id="data-svg" viewBox="0 0 900 610" role="img"
        aria-label="Network diagram: a central BIM model containing structured data, linked to geometry,
        parameters, systems, equipment, relationships, quantities, specifications and spatial data."></svg>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">What a model holds</p>
      <h2 class="sec-title">Ten kinds of information, only one of which is geometry</h2>
      <p class="sec-lede">The 3D view is the least interesting thing in a well-authored model. Each
      of these is queryable if it was populated during authoring, and effectively lost if it
      was not.</p>
    </header>
    <div class="g4">
      <article class="card"><p class="card__k">01</p><h3>Geometry</h3>
        <p>Shape, position and extent. The part everyone sees, and the part automated checking uses
        least.</p></article>
      <article class="card"><p class="card__k">02</p><h3>Parameters</h3>
        <p>Sizes, ratings, flows, loads, materials and classification codes carried on the element
        itself rather than in a document beside it.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Systems</h3>
        <p>Which elements belong to which network, and how the network is bounded. This is what makes
        "check the chilled water system" a resolvable instruction.</p></article>
      <article class="card"><p class="card__k">04</p><h3>Equipment</h3>
        <p>Plant, terminals and devices with their performance data attached, so a schedule and a
        model cannot disagree.</p></article>
      <article class="card"><p class="card__k">05</p><h3>Relationships</h3>
        <p>Connectivity, hosting and containment. The structure that lets an analysis follow a run
        from source to terminal rather than treating it as loose pipes.</p></article>
      <article class="card"><p class="card__k">06</p><h3>Quantities</h3>
        <p>Measurable from geometry and parameters, with the measurement rule visible for each
        line.</p></article>
      <article class="card"><p class="card__k">07</p><h3>Specifications</h3>
        <p>What the element must be, alongside what it currently is. The gap between the two is
        exactly what a compliance check reads.</p></article>
      <article class="card"><p class="card__k">08</p><h3>Spatial information</h3>
        <p>Rooms, zones, voids and clearances. Most coordination failures are spatial rather than
        geometric — the parts do not collide, they just cannot be installed or maintained.</p></article>
      <article class="card"><p class="card__k">09</p><h3>Design intent</h3>
        <p>The criteria the design was meant to satisfy, held against the model so drift is
        detectable rather than discovered on site.</p></article>
      <article class="card"><p class="card__k">10</p><h3>Status and provenance</h3>
        <p>Revision, suitability code, author and issue state. Without this the other nine cannot be
        trusted at any particular moment.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">The precondition</p>
      <h2 class="sec-title">Information-first modelling, and why it cannot be added later</h2>
      <p class="sec-lede">Two models can look identical in a viewer and be completely different
      assets. This is the least marketable thing BIMRACE does and the reason the rest works.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Practice<b>Parameters populated during authoring</b>{B('live')}</div>
        <div class="spec__v">Data is entered as the element is placed, not swept up in a
        pre-handover exercise where 4,000 elements get a plausible value in an afternoon. Retro-fitted
        data is unreliable data, and automated checking over unreliable data is worse than no
        checking because it is confident.</div></div>
      <div class="spec__row"><div class="spec__k">Practice<b>Naming and classification as a rule set</b>{B('live')}</div>
        <div class="spec__v">Conventions defined before authoring starts and enforced by routine
        rather than by review. A machine can only group and query what is named consistently.</div></div>
      <div class="spec__row"><div class="spec__k">Practice<b>Systems modelled as systems</b>{B('live')}</div>
        <div class="spec__v">Connected networks with real system assignment, not disconnected
        geometry that happens to line up. Without this, no analysis can follow an index run or size
        a branch against its upstream.</div></div>
      <div class="spec__row"><div class="spec__k">Practice<b>Model health maintained continuously</b>{B('live')}</div>
        <div class="spec__v">Warnings, unplaced and duplicated elements, worksets, links and shared
        coordinates checked as an ongoing routine. A model that has degraded quietly for six months
        cannot be analysed reliably.</div></div>
      <div class="spec__row"><div class="spec__k">Practice<b>Level of information need agreed first</b>{B('live')}</div>
        <div class="spec__v">What "complete" means for an object at a given milestone, defined
        before authoring. This is what makes a completeness check a factual test rather than an
        opinion.</div></div>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>The uncomfortable version.</strong> If a model was not authored this way, no
      intelligence layer will rescue it. The honest options are to remodel, to accept a narrower set
      of checks that geometry alone supports, or to fix the data as a defined piece of work with its
      own scope. We will tell you which of those applies at enquiry stage rather than after
      appointment.</p>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Data governance</p>
      <h2 class="sec-title">Model integrity, and what happens to your data</h2>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">01</p><h3>Your model stays yours</h3>
        <p>Client models are worked on inside the appointing party's environment where one exists.
        We do not train anything on client model data, and we do not retain it beyond the
        appointment without a written instruction.</p></article>
      <article class="card"><p class="card__k">02</p><h3>Checks are traceable</h3>
        <p>Every automated finding carries the element ID it came from and the rule that produced
        it. A finding you cannot trace is a finding you cannot act on or dispute.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Rules are visible</h3>
        <p>The rule sets applied to your project are stated, not hidden inside a tool. If a check
        fires, you can see the definition that fired it and argue with it.</p></article>
      <article class="card"><p class="card__k">04</p><h3>No silent writes</h3>
        <p>No routine modifies a live model without an engineer accepting the change. Drafts are
        produced in a reviewable state.</p></article>
      <article class="card"><p class="card__k">05</p><h3>Status codes respected</h3>
        <p>Suitability and revision state govern what may be used for what. Automation reads status;
        it does not change it.</p></article>
      <article class="card"><p class="card__k">06</p><h3>Confidentiality by default</h3>
        <p>NDAs signed before drawings are shared, as a matter of course rather than on request.
        Nothing is published as a case study without written release.</p></article>
    </div>
  </div>
</section>
"""


# ============================================================================
#  AI & AUTOMATION
# ============================================================================
AUTOMATION = f"""
{phero([("Home", "index.html"), ("Platform", "platform.html"), ("AI &amp; Automation", None)],
       "AI &rarr; Reason &rarr; Validate &rarr; Automate &rarr; Engineer approves",
       "What the intelligence layer actually does, which workflows it runs today, and exactly where "
       "a person has to sign before anything leaves the building.",
       [("Live workflows", "05"), ("In development", "Agents · Design automation"),
        ("Roadmap", "NL query · Optimisation"), ("Autonomous", "None, by design")])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">The workflow</p>
      <h2 class="sec-title">From engineering intent to engineering output</h2>
      <p class="sec-lede">Ten stages, drawn as one line so the hand-off points are visible. The
      amber nodes are people — the brief at the start and the sign-off at the end. Everything
      between them is machinery that reports to them.</p>
    </header>
    <div class="panel">
      <div class="panel__bar">
        <span><b>PIPELINE</b> / INTENT TO OUTPUT</span>
        <span class="panel__dot"><i></i>DATA FLOW</span>
      </div>
      <div class="panel__body">
        <svg class="dia" id="pipe-svg" viewBox="0 42 1200 120" role="img"
          aria-label="Ten-stage pipeline: engineering intent, interpretation, BIM model, calculation,
          rule engine, analysis, automation, QA and QC, engineer approval, output. Engineering intent
          and engineer approval are marked as human stages."></svg>
      </div>
      <div class="panel__foot">
        <span>AMBER NODES ARE HUMAN STAGES</span>
        <span>NO STAGE IS SKIPPED BY AUTOMATION</span>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Worked example</p>
      <h2 class="sec-title">"Check the chilled water system."</h2>
      <p class="sec-lede">One sentence from an engineer. Here is every step between that sentence
      and a report they can act on — including the two places the system stops and asks.</p>
    </header>
    <div class="split">
      <div>
        <ol class="steps">
          <li class="is-human"><span class="steps__k">Engineer</span><h3>States the query</h3>
            <p>"Check the chilled water system on R04." The scope, the model and the standard being
            applied are established by a person who knows why it matters.</p></li>
          <li class="is-ai"><span class="steps__k">System</span><h3>Resolves the system</h3>
            <p>Reads the federated model, identifies the chilled water network, and separates it
            from adjacent services by system assignment rather than by colour.</p></li>
          <li class="is-ai"><span class="steps__k">System</span><h3>Reads the engineering data</h3>
            <p>Equipment, terminals, pipe segments, diameters, design flows, insulation and
            valve positions — off the elements, not off a spreadsheet.</p></li>
          <li class="is-ai"><span class="steps__k">System</span><h3>Applies engineering rules</h3>
            <p>Sizing bands against flow, velocity limits, index-run pressure drop, clearance and
            access to plant, isolation and drain-down provision.</p></li>
          <li class="is-ai"><span class="steps__k">System</span><h3>Detects abnormal conditions</h3>
            <p>A DN150 branch carrying flow sized for DN200 upstream. Four segments with no design
            flow parameter. A failing index run. Each finding carries its element ID and the rule
            that fired.</p></li>
          <li class="is-ai"><span class="steps__k">System</span><h3>Drafts the report</h3>
            <p>Findings grouped by cause and severity, with the parameter values that produced them,
            and an explicit list of what could not be determined from the model.</p></li>
          <li class="is-human"><span class="steps__k">Engineer</span><h3>Reviews and decides</h3>
            <p>Confirms the real findings, discards the false ones, and decides what changes. False
            positives go back into the rule set — that feedback is the actual product.</p></li>
        </ol>
      </div>
      <div>
        <div class="note note--sig">
          <p><strong>Why this is stronger than "AI makes engineering faster."</strong> Every step
          above names a real artefact: a system assignment, a parameter, a rule, an element ID. A
          claim that names artefacts can be checked. A claim that names a feeling cannot.</p>
        </div>
        <div class="note" style="margin-top:20px">
          <p><strong>What the system does not do.</strong> It does not resize the pipe. It does not
          close the finding. It does not update the model or the drawing. It does not decide whether
          a marginal velocity is acceptable on this project — that is an engineering judgement with
          a name attached to it.</p>
        </div>
        <p class="tiny" style="margin-top:22px">The corresponding scripted run is shown in the
        console demonstration on the homepage. That console is simulated; this description is of the
        workflow as designed. Model reading and rule application are in development and used
        internally; the engineering review step is how we already work.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Engineering agents</p>
      <h2 class="sec-title">Eight defined workflows, four of which exist</h2>
      <p class="sec-lede">An agent is a workflow with a named input, an explicit rule set, a
      reasoning step and an output an engineer signs. It is not a personality and it is not a chat
      window.</p>
    </header>
{CHAIN}
{agents_block()}
    <div class="note note--sig" style="max-width:none">
      <p><strong>Read the badges.</strong> Four of these are in development and used internally on
      our own delivery. Four are roadmap — architecturally coherent, not built. None run
      unattended, and none are offered for licence.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Engineering console</p>
      <h2 class="sec-title">What an engineering query looks like when the model can answer</h2>
      <p class="sec-lede">A simulated session, shown because describing this is worse than showing
      it. Every figure below is fabricated and nothing here is connected to a model.</p>
    </header>
{CONSOLE}
    <p class="viz__cap" style="margin-top:14px">{B('demo')} Note the last line of every run: the
    system holds for engineering review. That is the design, not a limitation of the demo.</p>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">What we automate</p>
      <h2 class="sec-title">Six workflows, five of them running on live appointments</h2>
    </header>
{flows_block()}
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Accountability</p>
      <h2 class="sec-title">Where automation stops</h2>
      <p class="sec-lede">A short, deliberately boring list. It is the part of an AI engineering
      proposition that most sites leave out, and the part a technical buyer actually needs.</p>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">Never</p><h3>Writes to a live model</h3>
        <p>Generated or amended content is produced in a reviewable state for an engineer to accept.
        No routine commits geometry to a shared model on its own authority.</p></article>
      <article class="card"><p class="card__k">Never</p><h3>Closes an issue</h3>
        <p>Findings are raised, classified and prioritised. Closing one is a decision with a
        consequence, so a person makes it and their name is against it.</p></article>
      <article class="card"><p class="card__k">Never</p><h3>Issues a deliverable</h3>
        <p>Nothing reaches a common data environment with a suitability code without a named
        engineer issuing it.</p></article>
      <article class="card"><p class="card__k">Never</p><h3>Changes a status code</h3>
        <p>Automation reads suitability and revision state. It does not promote a container from
        work-in-progress to shared.</p></article>
      <article class="card"><p class="card__k">Never</p><h3>Settles an engineering judgement</h3>
        <p>Whether a marginal result is acceptable on this project, with this client, under this
        standard, is not a computation. It is the job.</p></article>
      <article class="card"><p class="card__k">Never</p><h3>Trains on your model</h3>
        <p>Client model data is not used to train anything. It is worked on for the appointment and
        not retained beyond it without written instruction.</p></article>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>The trade this implies.</strong> These constraints make our workflows slower than a
      fully autonomous system would be. They also make the output defensible, which is the only
      state in which an engineering deliverable has value. We are not planning to relax them.</p>
    </div>
  </div>
</section>
"""


# ============================================================================
#  DIGITAL TWIN
# ============================================================================
DIGITAL_TWIN = f"""
{phero([("Home", "index.html"), ("Platform", "platform.html"), ("Digital Twin", None)],
       "What a digital twin actually requires",
       "Five inputs, of which we deliver two today. This page exists to be precise about the "
       "distance between a well-structured model and a twin, because that distance is routinely "
       "misrepresented in this sector.",
       [("Status", "Roadmap"), ("Delivered today", "Model + asset data"),
        ("Not built", "Live data · Analytics"), ("Committed dates", "None")])}

<section class="section section--flush">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow eyebrow--plain">Definition {B('road')}</p>
      <h2 class="sec-title">A 3D model on a web page is not a digital twin</h2>
      <p class="sec-lede">It is a viewer. A twin is a model bound to asset data, fed by live data
      from the building, governed by engineering rules and read by analytics that produce operational
      decisions. Remove any one of those five and the word does not apply.</p>
      <p class="lede" style="margin-top:22px">BIMRACE delivers the first two inputs today: models
      structured to carry asset information, and the asset data itself, produced as a handover
      deliverable. The live-data and analytics layers are roadmap.</p>
      <p class="lede" style="margin-top:16px">We publish this distinction because "digital twin" is
      currently applied to almost anything with a 3D view, and a client who buys a twin and receives
      a viewer has been mis-sold something expensive.</p>
    </div>
    <div>
      <div class="panel">
        <div class="panel__bar">
          <span><b>COMPOSITION</b> / TWIN INPUTS</span>
          <span>{B('road')}</span>
        </div>
        <div class="panel__body">
          <svg class="dia" id="twin-svg" viewBox="20 20 716 372" role="img"
            aria-label="Composition diagram: BIM model and asset data feeding a digital twin as live
            inputs, with live telemetry, engineering rules and analytics shown as not yet built."></svg>
        </div>
        <div class="panel__foot">
          <span>SOLID CONNECTORS: DELIVERED TODAY</span>
          <span>FAINT CONNECTORS: NOT BUILT</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">The five inputs</p>
      <h2 class="sec-title">What each one is, and whether we have it</h2>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Input 01<b>BIM model</b>{B('live')}</div>
        <div class="spec__v">Geometry and structured data, authored so that asset information can be
        carried on the elements rather than in a separate register that immediately drifts. This is
        core delivery work and a service you can appoint today.</div></div>
      <div class="spec__row"><div class="spec__k">Input 02<b>Asset data</b>{B('live')}</div>
        <div class="spec__v">Equipment registers, specifications, serial and location data,
        maintenance attributes — structured against the model rather than delivered as a folder of
        PDFs. Handover information packaging is a live capability.</div></div>
      <div class="spec__row"><div class="spec__k">Input 03<b>Live data</b>{B('road')}</div>
        <div class="spec__v">Telemetry from BMS, meters and sensors, bound to the model elements
        that generate it. Not built. This requires integration work with the operator's systems that
        we have not undertaken on a live asset.</div></div>
      <div class="spec__row"><div class="spec__k">Input 04<b>Engineering rules</b>{B('dev')}</div>
        <div class="spec__v">Design intent expressed as thresholds a system can test against —
        the same rule sets we are building for design-stage checking, applied to operational data.
        In development for design; not yet applied operationally.</div></div>
      <div class="spec__row"><div class="spec__k">Input 05<b>Analytics</b>{B('road')}</div>
        <div class="spec__v">Reading the combination over time to produce operational decisions.
        Not built. Everything below is what this layer would be for, described as a concept.</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow eyebrow--plain">Applications {B('road')}</p>
      <h2 class="sec-title">What this would be for</h2>
      <p class="sec-lede">Described as concepts, because that is what they are. None of the
      following is a capability BIMRACE offers today, and none should be read as one.</p>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">01</p><h3>Energy optimisation</h3>
        <p>Comparing measured consumption against design intent per system and per zone, so drift is
        attributable to a plant item rather than to the building in general.</p></article>
      <article class="card"><p class="card__k">02</p><h3>Asset monitoring</h3>
        <p>Equipment condition and runtime read against the register, with the model providing the
        location and service context.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Predictive maintenance</h3>
        <p>Intervention scheduled from observed behaviour and duty rather than from a fixed calendar
        that ignores how hard the plant has actually worked.</p></article>
      <article class="card"><p class="card__k">04</p><h3>System performance</h3>
        <p>As-operating performance measured against as-designed criteria, which is the check that
        almost never happens after handover.</p></article>
      <article class="card"><p class="card__k">05</p><h3>Occupancy intelligence</h3>
        <p>Actual use against designed capacity, informing both operation and the brief for the next
        project.</p></article>
      <article class="card"><p class="card__k">06</p><h3>Operational analytics</h3>
        <p>Portfolio-level patterns across assets — which designs perform, which repeat the same
        failures, and what should change upstream.</p></article>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>What we will do today.</strong> Model and structure your asset so that a twin
      remains possible later — correct classification, asset parameters populated during authoring,
      clean system assignment and a handover data structure that an operational platform can
      actually ingest. That is real, deliverable work, and it is the part most projects get wrong in
      a way that is expensive to fix afterwards.</p>
      <p>What we will not do is sell you a model viewer and call it a twin.</p>
    </div>
  </div>
</section>
"""


# ============================================================================
#  ENGINEERING (replaces the old capabilities page)
# ============================================================================
CAPS = [
    ("modelling", "01", "BIM Modelling &amp; Documentation", "live",
     "Discipline models authored to an agreed level of information need, with drawings and schedules "
     "derived from the model rather than drafted separately. Model setup, templates, shared "
     "coordinates and naming conventions are established before authoring starts — which is what "
     "makes the data usable later.",
     ["Architectural modelling", "Structural modelling", "MEP modelling",
      "General arrangement drawings", "Sections, elevations and details",
      "Door, room and equipment schedules", "Family and content creation",
      "Model templates and standards setup"]),
    ("mep", "02", "MEP Engineering", "live",
     "Building services modelled as connected systems, routed against the spatial and access "
     "constraints they must satisfy. Sizing and performance data are held on the elements, so the "
     "model can be interrogated rather than only viewed — this is the discipline depth the "
     "intelligence layer depends on.",
     ["HVAC and ductwork distribution", "Plant room layouts",
      "Electrical distribution and containment", "Lighting and small power",
      "Public health and drainage", "Domestic water services",
      "Fire protection and sprinklers", "Equipment schedules and data"]),
    ("coordination", "03", "BIM Coordination", "live",
     "Federated models assembled from all contributing disciplines, with clashes tracked to closure "
     "and each decision recorded. The output is a resolved model and an auditable issue history, "
     "not a raw clash count — a number nobody can act on.",
     ["Federated model assembly", "Clash detection and rule sets",
      "Clash resolution and re-testing", "Coordination issue tracking",
      "Services zoning strategy", "Clearance and maintenance access checks",
      "Coordination reports", "Coordination workshop support"]),
    ("automation", "04", "Design &amp; Engineering Automation", "live",
     "Automation applied to repetitive production and checking, and model data managed as a "
     "deliverable in its own right. This is a service category rather than an add-on: it is quoted, "
     "scoped and delivered as work, and it is where the intelligence stack meets an appointment.",
     ["Parametric and computational workflows", "Automated model checking routines",
      "Parameter and data management", "Model auditing and health checks",
      "Data export and reporting", "Common data environment structure",
      "Naming and classification automation", "Digital delivery packaging"]),
    ("construction", "05", "Construction Support", "live",
     "Model-derived output produced for the people installing the work, at the detail and tolerance "
     "installation actually requires rather than at the level a design model happens to hold.",
     ["Shop and fabrication drawings", "Spool and prefabrication drawings",
      "Builders work and penetration drawings", "Bracket and support layouts",
      "As-built and record models", "Quantity take-off and schedules",
      "Site query support", "Handover information packaging"]),
]


def caps_block():
    rows = []
    for anchor, n, name, status, desc, items in CAPS:
        lis = "\n".join(f"          <li>{i}</li>" for i in items)
        rows.append(f"""      <div class="spec__row" id="{anchor}">
        <div class="spec__k">Capability {n}<b>{name}</b>{B(status)}</div>
        <div class="spec__v">{desc}
          <ul class="spec__list">
{lis}
          </ul>
        </div>
      </div>""")
    return '    <div class="spec">\n' + "\n".join(rows) + "\n    </div>"


ENGINEERING = f"""
{phero([("Home", "index.html"), ("Engineering", None)],
       "Engineering depth is what makes the intelligence defensible",
       "MEP engineering, BIM delivery and automation, defined by what is produced and issued rather "
       "than by which software is opened. Every line carries its capability status.",
       [("Categories", "Engineering · BIM · Intelligence"), ("Disciplines", "M · E · P · FP · S · A"),
        ("Standard", "ISO 19650 aligned"), ("Delivery", "India studio, remote international")])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Service architecture</p>
      <h2 class="sec-title">Three categories, not a list of twenty services</h2>
      <p class="sec-lede">Automation sits alongside engineering and BIM as a category of its own,
      because that is how it is scoped and priced here — not as a paragraph at the end of a
      modelling proposal.</p>
    </header>
{matrix_block()}
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Scope detail</p>
      <h2 class="sec-title">What is actually produced and issued</h2>
      <p class="sec-lede">Every capability below lists its deliverables. Any of them can be
      appointed on their own or combined; nothing here depends on buying the intelligence layer.</p>
    </header>
{caps_block()}
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Appointment models</p>
      <h2 class="sec-title">How engagements are usually structured</h2>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">01</p><h3>Package delivery</h3>
        <p>A defined scope with a fixed deliverable list and programme — a discipline model, a
        coordination package, a drawing set. Priced against the deliverable.</p></article>
      <article class="card"><p class="card__k">02</p><h3>Team extension</h3>
        <p>Modelling and engineering capacity inside your team and your environment, working to your
        standards and your BEP, for a defined period.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Coordination appointment</h3>
        <p>Federation, clash resolution and coordination management across contributing disciplines,
        with the issue history as a deliverable in its own right.</p></article>
      <article class="card"><p class="card__k">04</p><h3>Automation engagement</h3>
        <p>A defined workflow automated for your team — a QA rule set, a quantity routine, a
        documentation pipeline — delivered as tooling plus the engineering behind it.</p></article>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Tooling</p>
      <h2 class="sec-title">Deliverables are defined by the information required, not by an application</h2>
      <p class="sec-lede">Where a project mandates a toolchain, we work in it.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Authoring<b>Model production</b></div>
        <div class="spec__v">Revit · AutoCAD · discipline-specific MEP authoring tools</div></div>
      <div class="spec__row"><div class="spec__k">Coordination<b>Federation and review</b></div>
        <div class="spec__v">Navisworks · federated model review and clash workflows</div></div>
      <div class="spec__row"><div class="spec__k">Automation<b>Routines and checking</b></div>
        <div class="spec__v">Dynamo · scripted routines · custom checking and data tools built
        in-house</div></div>
      <div class="spec__row"><div class="spec__k">Exchange<b>Interoperability</b></div>
        <div class="spec__v">IFC · COBie-style data exports · common data environments</div></div>
    </div>
    <p class="tiny" style="margin-top:22px">Software names are the property of their respective
    owners and are listed to describe working practice. No partnership, certification or
    endorsement is implied.</p>
  </div>
</section>
"""


# ============================================================================
#  INDUSTRIES
# ============================================================================
INDS = [
    ("01", "Commercial &amp; offices",
     "Fit-out and core-and-shell coordination, ceiling void congestion, tenant variation.",
     "High element count, repeated coordination cycles — automated QA pays back fastest here."),
    ("02", "Residential &amp; mixed use",
     "Repeatable unit typologies, riser coordination and high documentation volume.",
     "Repetition is the ideal condition for design automation and rule-based checking."),
    ("03", "Healthcare",
     "Dense services, strict clearance and access requirements, demanding validation.",
     "Clearance and maintenance-access rules matter more than hard clashes."),
    ("04", "Data centres",
     "High-density mechanical and electrical distribution with tight tolerance coordination.",
     "Parameter completeness and sizing consistency are the dominant risk."),
    ("05", "Industrial &amp; warehousing",
     "Long-span structures, process services and fire protection routing.",
     "Fire protection coordination against structure is the recurring conflict."),
    ("06", "Hospitality",
     "Back-of-house services, guest-room repetition and finish-critical coordination.",
     "Room typology repetition suits generated content and automated checking."),
    ("07", "Education",
     "Phased delivery, standardised room types and ventilation-led services.",
     "Phasing makes model status and revision discipline critical."),
    ("08", "Retail",
     "Landlord and tenant interfaces, rapid fit-out programmes, shopfront coordination.",
     "Short programmes reward automated documentation over manual production."),
]

INDUSTRIES = f"""
{phero([("Home", "index.html"), ("Industries", None)],
       "Where coordination difficulty actually sits",
       "Sectors differ less in the software used than in services density, clearance tolerance and "
       "validation expectation. These are the building types our discipline mix is set up for, and "
       "where automation earns its place.",
       [("Sectors", "08"), ("Basis", "Discipline mix and workflow"),
        ("Not claimed", "Sector-specific project history")])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Sector capability</p>
      <h2 class="sec-title">Services density, not building type, sets the difficulty</h2>
      <p class="sec-lede">Two buildings of identical size can be an order of magnitude apart in
      coordination effort. What varies is how much plant is in the ceiling, how tight the clearance
      requirement is, and how much of the checking has to be evidenced.</p>
    </header>
    <div class="inds">
{chr(10).join(f'''      <article class="ind">
        <p class="ind__n">{n}</p>
        <div><h3>{t}</h3></div>
        <div><p>{d}</p><p class="tiny" style="margin-top:8px">{a}</p></div>
      </article>''' for n, t, d, a in INDS)}
    </div>
    <div class="note" style="max-width:none">
      <p><strong>What this page does and does not say.</strong> It describes the building types our
      disciplines and workflows suit. It does not claim completed projects in each sector, and there
      are no sector case studies on this site yet because none have been released for publication.</p>
      <p>The second line under each sector is where automation is most useful in that building type
      — a statement about workflow, not about work we have already delivered there.</p>
    </div>
  </div>
</section>
"""


# ============================================================================
#  PROJECTS
# ============================================================================
PROJECTS = f"""
{phero([("Home", "index.html"), ("Projects", None)],
       "Case studies structured around the engineering problem",
       "Published as clients release them. Until then, the documentation structure every entry will "
       "follow is set out in full below — including the parts most case studies omit.",
       [("Published", "None yet"), ("Structure", "Fixed, five parts"),
        ("Numbers", "Verified or absent"), ("Failures", "Published too")])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Project evidence</p>
      <h2 class="sec-title">Nothing here is invented</h2>
      <p class="sec-lede">It is common in this sector to show unattributed renders, borrowed
      imagery and round numbers with no method behind them. This page does none of that. Three
      positions are held open, and they stay empty until a client releases the work.</p>
    </header>
{CASE_ANATOMY}
    <div class="g3" style="margin-top:var(--s4)">
      <div class="slot"><p class="slot__k">Position 01 — reserved</p>
        <h3>MEP coordination case study</h3>
        <p>A coordination appointment documented against the five-part structure above, with the
        automated checking workload separated from the manual review workload.</p></div>
      <div class="slot"><p class="slot__k">Position 02 — reserved</p>
        <h3>Automation engagement</h3>
        <p>A workflow automated for a client team, with the baseline it was measured against stated
        and the parts that stayed manual explained.</p></div>
      <div class="slot"><p class="slot__k">Position 03 — reserved</p>
        <h3>Model data and QA</h3>
        <p>An information-first modelling appointment, showing what became queryable as a result and
        what checking that enabled.</p></div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Measurement</p>
      <h2 class="sec-title">How impact will be stated</h2>
      <p class="sec-lede">The rules we are committing to in advance, so that when numbers do appear
      here they mean something.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Rule 01<b>Every number names its baseline</b></div>
        <div class="spec__v">"40% faster" is meaningless without saying faster than what, measured
        how, over what scope. Any figure published here will carry all three.</div></div>
      <div class="spec__row"><div class="spec__k">Rule 02<b>Automated and manual effort separated</b></div>
        <div class="spec__v">If a routine did the checking and an engineer did the review, the case
        study says how much of each. Blending them inflates the automation claim.</div></div>
      <div class="spec__row"><div class="spec__k">Rule 03<b>False positives reported</b></div>
        <div class="spec__v">Automated checking produces findings that turn out to be wrong. The
        rate is a property of the rule set and will be stated, because a checker with an unstated
        false-positive rate cannot be evaluated.</div></div>
      <div class="spec__row"><div class="spec__k">Rule 04<b>What did not work is included</b></div>
        <div class="spec__v">Approaches that were abandoned, rules that had to be rewritten and
        checks that could not be automated will appear in the case study. A library with no failures
        in it is a brochure.</div></div>
      <div class="spec__row"><div class="spec__k">Rule 05<b>Client release in writing</b></div>
        <div class="spec__v">Nothing is published without written permission, including
        anonymised work. If a client prefers anonymity, the sector and scale are described and the
        name is not.</div></div>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>If you are evaluating us right now</strong> and want evidence rather than a
      structure, ask at enquiry stage. We will walk through the internal tooling, the rule sets and
      the QA output on a live workflow directly — under NDA, on a call, with the actual screens.
      That is a better test than a case study we wrote about ourselves.</p>
    </div>
  </div>
</section>
"""


# ============================================================================
#  TECHNOLOGY / STANDARDS
# ============================================================================
TECHNOLOGY = f"""
{phero([("Home", "index.html"), ("Standards", None)],
       "Standards, information management and QA",
       "ISO 19650 information management, the artefacts that govern an appointment, and the checks "
       "applied before anything is issued. This is the discipline the intelligence layer is built "
       "on top of.",
       [("Framework", "ISO 19650 series"), ("Artefacts", "EIR · BEP · MIDP · CDE · LOIN"),
        ("Certification", "None claimed"), ("QA checks", "Six categories")])}

<section class="section section--flush" id="standards">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Information standards</p>
      <h2 class="sec-title">Structured to ISO 19650</h2>
      <p class="sec-lede">ISO 19650 is the international standard series for managing information
      using BIM across the life cycle of built assets. BIMRACE structures delivery around its
      principles by default, on every appointment.</p>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">Part 1</p><h3>Concepts and principles</h3>
        <p>Defines the core terms, roles and the information delivery cycle, including expectations
        for a common data environment, status codes and approval.</p></article>
      <article class="card"><p class="card__k">Part 2</p><h3>Delivery phase</h3>
        <p>The part most referenced in day-to-day practice. Covers information management during
        design and construction, and the artefacts that govern it.</p></article>
      <article class="card"><p class="card__k">Part 3</p><h3>Operational phase</h3>
        <p>Information management during operation and maintenance, and the transition from a
        project information model to an asset information model.</p></article>
      <article class="card"><p class="card__k">Part 4</p><h3>Information exchange</h3>
        <p>Process and decision criteria for individual information exchanges, including quality
        criteria for what is handed over.</p></article>
      <article class="card"><p class="card__k">Part 5</p><h3>Security-minded management</h3>
        <p>Applies where the sensitivity of the information requires protection — relevant to
        government, defence and critical infrastructure assets.</p></article>
      <article class="card"><p class="card__k">Part 6</p><h3>Health and safety information</h3>
        <p>The most recent addition to the series, covering the structuring of health and safety
        information.</p></article>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>On certification.</strong> BIMRACE structures its delivery to align with ISO 19650
      principles. This is a statement of working method, not a claim of third-party certification to
      the standard. Where a project requires certified parties, we will say so at enquiry stage
      rather than after appointment.</p>
    </div>
  </div>
</section>

<section class="section section--raise" id="methodology">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Working artefacts</p>
      <h2 class="sec-title">The documents that govern an appointment</h2>
      <p class="sec-lede">These are the instruments that make information delivery auditable. They
      are agreed before authoring begins — and they are also what an automated check is checking
      against.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">EIR<b>Exchange Information Requirements</b></div>
        <div class="spec__v">What the appointing party needs, when, in what format and to what level
        of information need. Everything downstream is measured against this.</div></div>
      <div class="spec__row"><div class="spec__k">BEP<b>BIM Execution Plan</b></div>
        <div class="spec__v">How the delivery team will meet those requirements — model structure,
        federation strategy, naming, coordinates, software and responsibilities.</div></div>
      <div class="spec__row"><div class="spec__k">MIDP / TIDP<b>Information delivery plans</b></div>
        <div class="spec__v">The master and task-level schedules that say who issues which
        container, at which milestone, in which state.</div></div>
      <div class="spec__row"><div class="spec__k">CDE<b>Common Data Environment</b></div>
        <div class="spec__v">The single source for project information, with status codes controlling
        whether a container is work in progress, shared, published or archived.</div></div>
      <div class="spec__row"><div class="spec__k">LOIN<b>Level of Information Need</b></div>
        <div class="spec__v">Defines what "complete" means for an object at a given milestone —
        geometry, alphanumeric data and documentation. It is the successor to inconsistent LOD usage
        and removes most of the ambiguity that caused. It is also what turns a completeness check
        into a factual test rather than an opinion.</div></div>
    </div>
  </div>
</section>

<section class="section" id="quality">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Quality assurance</p>
      <h2 class="sec-title">What gets checked before anything is issued</h2>
      <p class="sec-lede">Six categories, run as rule sets rather than as a person opening views one
      at a time. The routines are live; the reasoning layer that clusters failures by root cause is
      in development.</p>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">01</p><h3>Model health {B('live')}</h3>
        <p>File size and performance, warnings, unplaced and duplicated elements, worksets, links and
        shared coordinate integrity.</p></article>
      <article class="card"><p class="card__k">02</p><h3>Standards compliance {B('live')}</h3>
        <p>Naming, classification, view and sheet organisation, parameter completeness against the
        agreed level of information need.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Geometric accuracy {B('live')}</h3>
        <p>Origin and orientation, level and grid alignment, discipline model alignment, tolerance
        against the coordination datum.</p></article>
      <article class="card"><p class="card__k">04</p><h3>Data completeness {B('live')}</h3>
        <p>Required parameters populated, schedules reconciling, exported data validating against the
        exchange requirement.</p></article>
      <article class="card"><p class="card__k">05</p><h3>Coordination status {B('live')}</h3>
        <p>Open clashes reviewed, resolutions re-tested, decisions recorded against a tracked issue
        list with an owner.</p></article>
      <article class="card"><p class="card__k">06</p><h3>Issue readiness {B('live')}</h3>
        <p>Correct status code and revision, correct formats, deliverable list reconciled against the
        delivery plan before upload.</p></article>
    </div>
  </div>
</section>

<section class="section section--raise" id="methodology-flow">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Delivery methodology</p>
      <h2 class="sec-title">A defined route from requirement to deliverable</h2>
      <p class="sec-lede">Requirements are agreed before modelling starts, and every deliverable is
      checked against them before it is issued.</p>
    </header>
    <div class="pipe">
      <div class="pipe__s pipe__s--human"><p class="pipe__n">STAGE 01</p><h3>Define</h3>
        <p>Confirm information requirements, scope, disciplines and level of information need.</p></div>
      <div class="pipe__s pipe__s--human"><p class="pipe__n">STAGE 02</p><h3>Plan</h3>
        <p>Execution plan, model structure, naming, shared coordinates and delivery programme.</p></div>
      <div class="pipe__s"><p class="pipe__n">STAGE 03</p><h3>Model</h3>
        <p>Discipline authoring to the agreed standard, with data populated as the model is built.</p></div>
      <div class="pipe__s"><p class="pipe__n">STAGE 04</p><h3>Coordinate</h3>
        <p>Federate, resolve clashes and record decisions against a tracked issue list.</p></div>
      <div class="pipe__s pipe__s--ai"><p class="pipe__n">STAGE 05</p><h3>Validate</h3>
        <p>Automated rule sets plus engineering review, against the plan, before anything is
        issued.</p></div>
      <div class="pipe__s pipe__s--human"><p class="pipe__n">STAGE 06</p><h3>Deliver</h3>
        <p>Issue through the common data environment with the agreed formats and status codes.</p></div>
    </div>
  </div>
</section>
"""


# ============================================================================
#  ABOUT
# ============================================================================
ABOUT = f"""
{phero([("Home", "index.html"), ("About", None)],
       "An engineering practice that builds its own tools",
       "BIMRACE was established around one idea: engineering information that is accurate enough to "
       "rely on and structured enough to be used automatically. The tooling exists because the "
       "engineering demanded it, not the other way round.",
       [("Entity", ENTITY), ("Founded by", "Somnath Baste"),
        ("Base", "India, remote international delivery"), ("Claims", "Status-badged throughout")])}

<section class="section section--flush">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow">The practice</p>
      <h2 class="sec-title">A focused engineering practice, not a volume drafting shop</h2>
      <p class="sec-lede">BIMRACE produces building information that holds up under interrogation:
      models whose data is reliable, coordination whose decisions are recorded, and deliverables that
      reconcile with each other.</p>
      <p class="lede" style="margin-top:22px">The automation followed from that. Once information is
      structured and reliable, a large share of routine checking stops needing a person to do it by
      hand — and the engineers get their attention back for the parts that actually require
      judgement. That is the whole thesis, and it is why the AI layer here is built by the same
      people who do the engineering rather than bought in and pointed at a model.</p>
      <p class="lede" style="margin-top:16px">It is a young practice. This site is structured so you
      can tell exactly how young, and exactly which parts of it are real.</p>
    </div>
    <div>
      <div class="thesis">
        <div><b>Discipline</b><span>MEP engineering at the centre, not bolted onto architectural modelling.</span></div>
        <div><b>Method</b><span>Information-first authoring, so the data can be queried later.</span></div>
        <div><b>Tooling</b><span>Built in-house, by the engineers who use it.</span></div>
        <div><b>Standard</b><span>ISO 19650 aligned by default. Not certified, and not claimed.</span></div>
        <div><b>Accountability</b><span>A named engineer signs every deliverable.</span></div>
      </div>
      <div class="note note--sig" style="margin-top:22px">
        <p><strong>Why the badges exist.</strong> The distance between what a company can do and what
        its website says it can do is the most expensive thing in this sector — it wastes the
        client's procurement time and destroys trust at the first technical conversation. Publishing
        capability status costs us some early enthusiasm and saves everyone the conversation where it
        turns out the platform is a slide deck.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Leadership</p>
      <h2 class="sec-title">Founder</h2>
    </header>
    <div class="founder">
      <div>
        <p class="quote">"Engineering data should not only be stored in models — it should become
        intelligent, useful and actionable. That is a modelling discipline problem before it is an
        AI problem, which is why we start there."</p>
        <p class="lede" style="margin-top:26px"><strong style="color:var(--text)">Somnath Baste</strong>
        — Founder, BIMRACE. Enquiries about scope, standards, automation or delivery method reach the
        founder directly rather than a sales function.</p>
        <p class="lede" style="margin-top:18px">If you want to test whether the intelligence layer
        described on this site is real, ask for a working session. We will show the internal tooling,
        the rule sets and the QA output on a live workflow, under NDA. That is a more useful hour
        than a capability presentation.</p>
        <div class="hero__actions" style="margin-top:32px">
          <a class="btn btn--primary" href="contact.html">Discuss your project</a>
          <a class="btn btn--ghost" href="tel:{TEL}">{PHONE}</a>
        </div>
      </div>
      <div>
        <div class="founder__frame">
          <span class="founder__fallback" aria-hidden="true"
            style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:34px;color:var(--text-4)">SB</span>
          <img class="founder__photo"
            src="https://rhksfmwmqiwzwsiiuhng.supabase.co/storage/v1/object/public/somnathprofilepic/SAM.jpg"
            alt="Portrait of Somnath Baste, Founder of BIMRACE"
            width="800" height="1000" loading="lazy" decoding="async"
            style="position:relative;z-index:1;display:block;width:100%;height:100%;object-fit:cover;object-position:center 22%;filter:grayscale(1) contrast(1.04)">
        </div>
        <p class="founder__cap">SOMNATH BASTE · FOUNDER</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="global">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Global delivery</p>
      <h2 class="sec-title">How remote appointments actually run</h2>
      <p class="sec-lede">BIMRACE operates from India and delivers remotely. Working practices are
      set up for distributed teams rather than adapted to them.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Environment<b>Inside your environment</b></div>
        <div class="spec__v">We work inside the appointing party's common data environment where one
        exists, to your naming, status codes and BEP. Where one does not exist, we provide a
        structured environment and hand it over at the end.</div></div>
      <div class="spec__row"><div class="spec__k">Rhythm<b>Defined issue rhythm</b></div>
        <div class="spec__v">Agreed issue points rather than ad-hoc uploads, so the coordination
        cycle is predictable across time zones and nobody is waiting on an unannounced model.</div></div>
      <div class="spec__row"><div class="spec__k">Hours<b>Working-hours overlap</b></div>
        <div class="spec__v">IST sits within a workable overlap of European and Asia-Pacific hours,
        with an established handover window for North American teams.</div></div>
      <div class="spec__row"><div class="spec__k">Language<b>English-language delivery</b></div>
        <div class="spec__v">Documentation, model data and correspondence in English, to the
        conventions of the appointing party's region.</div></div>
    </div>
    <p class="tiny" style="margin-top:22px">BIMRACE operates as a single India-based studio. We do
    not claim overseas offices.</p>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Positioning</p>
      <h2 class="sec-title">What we will not claim</h2>
      <p class="sec-lede">A short list, because in this sector the absence of these claims is itself
      informative — particularly on a site that uses the words AI and automation as much as this one
      does.</p>
    </header>
    <div class="g2">
      <div class="card">
        <p class="card__k">Not claimed</p>
        <h3>Track record we have not earned</h3>
        <p>No client logos, no project counts, no headcount, no revenue figures, no awards and no
        testimonials — because none of those have been earned and verified yet. When they are, they
        will appear with attribution.</p>
      </div>
      <div class="card">
        <p class="card__k">Not claimed</p>
        <h3>Certification we do not hold</h3>
        <p>We align delivery to ISO 19650 principles, which is a different and checkable statement
        from certification. If your procurement requires certified parties, we will tell you at
        enquiry stage rather than after appointment.</p>
      </div>
      <div class="card">
        <p class="card__k">Not claimed</p>
        <h3>An AI product you can buy</h3>
        <p>The intelligence layer is internal software in development. It is not a released product,
        it is not licensable, and no feature or date on this site is a commitment. Everything marked
        roadmap is not built.</p>
      </div>
      <div class="card">
        <p class="card__k">Not claimed</p>
        <h3>Autonomous engineering</h3>
        <p>Nothing here runs without engineering review. Any vendor in this sector claiming
        autonomous engineering decisions is describing a liability structure that does not exist.</p>
      </div>
    </div>
  </div>
</section>
"""


# ============================================================================
#  INSIGHTS
# ============================================================================
INSIGHT_ENTRIES = [
    ("What BIM actually changes on a project",
     "engineering.html", "See what is delivered",
     ["A model is not a deliverable in itself. What changes is where conflicts are found. "
      "Without a coordinated model, a duct and a cable tray competing for the same 300mm is "
      "found by a person comparing two drawings, or by an installer on site with the ceiling "
      "grid already up. With one, it is found by a clash test before the drawings are issued.",
      "That is the whole economic argument, and it is why BIM is worth the authoring discipline "
      "it demands. The saving is not in the modelling. It is in the rework that does not happen."]),
    ("Why MEP is the hardest part to coordinate",
     "services/bim-coordination-clash-detection.html", "MEP coordination &amp; clash detection",
     ["Architecture and structure are largely fixed early and move slowly. Building services are "
      "the opposite: four disciplines competing for the same ceiling void and the same risers, "
      "each with its own gradient, clearance, access and statutory constraints, and each still "
      "changing while the others are being drawn.",
      "Ductwork needs depth and cannot be casually rerouted. Drainage needs fall and therefore "
      "cannot be moved vertically at all without consequences. Sprinkler coverage is governed by "
      "spacing rules. Cable containment needs maintenance access. Coordinating MEP is mostly the "
      "work of deciding, system by system, which of those constraints yields."]),
    ("Level of detail is a scope decision, not a quality one",
     "services/bim-modelling-documentation.html", "BIM modelling &amp; documentation",
     ["Asking for the most detailed model available is usually the wrong instinct. Detail costs "
      "time to author and time to change, and a model detailed beyond the decisions the stage is "
      "making is slower to coordinate without being more useful.",
      "The question worth agreeing at appointment is what decisions the model has to support at "
      "each stage, and then authoring to that. A concept-stage model that establishes riser sizes "
      "and plant space is doing its job. The same model with every bracket in it is not better; "
      "it is more expensive and harder to move."]),
    ("What to ask for so the data is usable later",
     "technology.html", "BIM standards &amp; QA",
     ["Two models can look identical and be worth very different amounts. The difference is "
      "whether the information was put in during authoring or added under deadline pressure "
      "before handover.",
      "If you want schedules, quantities or automated checks to be trustworthy, ask for the "
      "naming convention, the parameter schema and the QA checks before authoring starts, not "
      "at handover. Retro-fitting data into a finished model is the most expensive way to get it, "
      "and it is where most of the disappointment with BIM comes from."]),
    ("Where AI genuinely helps, and where it does not",
     "automation.html", "AI &amp; automation",
     ["Automated checking is real and useful now. Testing naming, parameters, clearances and "
      "sizing bands across an entire model is repetitive, rule-based and exhaustive work &mdash; "
      "which is exactly what a machine is better at than a person with a deadline.",
      "Deciding what to do about a finding is not that. Rerouting a main to resolve a clearance "
      "failure is an engineering judgement with liability attached, and it depends on things the "
      "model does not contain. So automation drafts findings here and an engineer accepts, amends "
      "or rejects them. Any supplier telling you the decision is automated is describing a "
      "product that does not exist yet."]),
    ("How remote delivery works without losing control",
     "locations.html", "International delivery",
     ["Offshore engineering support fails for two reasons: the standards were never agreed, and "
      "nobody arranged the overlap. Both are fixable at appointment.",
      "Working to your templates, your naming convention and your drawing conventions from the "
      "first day removes most of it. Arranging deliberate overlap with your working day &mdash; "
      "and putting one named engineer on the other end of it rather than a rotating pool &mdash; "
      "removes most of the rest. We have one office, in India, and the model is a remote team "
      "working to your standards, not a branch network."]),
]


def insight_block(entries):
    out = []
    for i, (title, href, label, paras) in enumerate(entries):
        body = "\n".join(f"        <p>{t}</p>" for t in paras)
        out.append(f"""    <article class="ins">
      <p class="ins__n">{i + 1:02d}</p>
      <div class="ins__b">
        <h2>{title}</h2>
{body}
        <a class="card__more" href="{href}">{label}</a>
      </div>
    </article>""")
    return '  <div class="inss">\n' + "\n".join(out) + "\n  </div>"


INSIGHTS_FAQS = [
    ("Do I need to understand BIM to work with BIMRACE?",
     "No. You need to tell us what the building is, what stage it is at and what you need out of "
     "it. We will tell you what the scope should be in ordinary language, and what you will "
     "receive. The modelling standard is our problem to get right, not yours to specify."),
    ("Can you work to our templates and standards?",
     "Yes, and it is the normal case. We work inside client templates, naming conventions and "
     "drawing standards as an extension of your team. Where you do not have them, we will "
     "propose a structure aligned to ISO 19650 principles and agree it before authoring starts."),
    ("Is MEP design and BIM modelling one appointment or two?",
     "It can be either. Some clients appoint us for the engineering design and the model "
     "together, which is where most of the value is because the decisions and the model cannot "
     "disagree. Others already have a design and need the modelling, coordination or "
     "documentation done properly. Both are normal."),
    ("What do you need from us to quote?",
     "Architectural drawings or a model, the stage, the building type and location, and what you "
     "need delivered. If a scope document exists, send that. If it does not, describe the problem "
     "and we will draft the scope."),
]

INSIGHTS = f"""
{phero([("Home", "index.html"), ("Insights", None)],
       "Insights",
       "Plain answers to the questions that the jargon in this sector tends to hide &mdash; what "
       "BIM changes, why MEP coordination is hard, what to ask for so the data is usable, and "
       "where AI genuinely helps.",
       [("Written for", "Architects, contractors, developers and project teams"),
        ("Assumes", "No prior knowledge of BIM or Revit")])}

<section class="section">
  <div class="shell">
{insight_block(INSIGHT_ENTRIES)}
  </div>
</section>
{faq_block(INSIGHTS_FAQS, title="Questions we are asked before an appointment",
           eyebrow="FAQ")}
"""


# ============================================================================
#  CONTACT
# ============================================================================
CONTACT = f"""
{phero([("Home", "index.html"), ("Contact", None)],
       "Tell us about your project",
       "Tell us the scope, or the workflow you are tired of doing by hand. You will get a technical "
       "response from an engineer — approach, disciplines, deliverables, and an honest read on what "
       "is realistically automatable.",
       [("Reaches", "Somnath Baste, Founder"), ("Response", "Within two working days"),
        ("NDA", "Signed before drawings are shared"), ("Not sent", "A brochure")])}

<section class="section section--flush">
  <div class="shell split">
    <div>
      <p class="eyebrow">Project enquiry</p>
      <h2 class="sec-title">Tell us about the project</h2>
      <p class="sec-lede">The more specific the scope, the more useful the response. If you have a
      drawing set, an EIR or a BEP, say so and we will ask for it under NDA.</p>

      <!-- Field names are the contract with crm.enquiry_submissions. Do not
           rename them without migrating the Supabase schema and lead-capture.js. -->
      <form class="form" id="enquiry-form" data-lead-form="project_enquiry" novalidate
            style="margin-top:var(--s4)">
        <p class="hp"><label>Do not fill this in
          <input name="company_website_hp" tabindex="-1" autocomplete="off"></label></p>

        <div class="field"><label for="f-name">Name <span class="req" aria-hidden="true">*</span></label>
          <input id="f-name" name="name" type="text" autocomplete="name" data-required required>
          <p class="err" data-for="f-name" role="alert"></p></div>

        <div class="field"><label for="f-company">Company <span class="req" aria-hidden="true">*</span></label>
          <input id="f-company" name="company" type="text" autocomplete="organization" data-required required>
          <p class="err" data-for="f-company" role="alert"></p></div>

        <div class="field"><label for="f-email">Business email <span class="req" aria-hidden="true">*</span></label>
          <input id="f-email" name="email" type="email" autocomplete="email" data-required required>
          <p class="err" data-for="f-email" role="alert"></p>
          <p class="hint" data-free-mail-hint hidden>A company address reaches us faster and helps us
          identify the project. A personal address is still fine.</p></div>

        <div class="field"><label for="f-phone">Telephone</label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel">
          <p class="err" data-for="f-phone" role="alert"></p></div>

        <div class="field"><label for="f-service">What do you need</label>
          <select id="f-service" name="lead_type">
            <option value="">Select&hellip;</option>
            <option value="mep_bim">MEP engineering / MEP BIM</option>
            <option value="bim_modelling">BIM modelling &amp; documentation</option>
            <option value="bim_coordination">BIM coordination</option>
            <option value="automation">Design &amp; engineering automation</option>
            <option value="bim_consulting">Model QA, data &amp; ISO 19650</option>
            <option value="bim_company_support">BIM company support (overflow / white-label)</option>
            <option value="resource_support">Staff / resource support</option>
            <option value="bim_training">Training</option>
            <option value="general">Not sure yet &mdash; want to discuss</option>
          </select></div>

        <div class="field"><label for="f-country">Country</label>
          <input id="f-country" name="country_code" type="text" maxlength="2"
                 placeholder="IN, GB, AE&hellip;" style="text-transform:uppercase"></div>

        <div class="field"><label for="f-stage">Project stage</label>
          <select id="f-stage" name="project_stage">
            <option value="">Select&hellip;</option>
            <option>Concept / feasibility</option><option>Developed design</option>
            <option>Technical design</option><option>Construction</option>
            <option>Handover / as-built</option>
          </select></div>

        <div class="field"><label for="f-sector">Sector</label>
          <input id="f-sector" name="industry" type="text" placeholder="e.g. healthcare, data centre"></div>

        <div class="field field--full"><label for="f-location">Project location</label>
          <input id="f-location" name="project_location" type="text" placeholder="City, country"></div>

        <div class="field field--full"><label for="f-msg">Scope, disciplines and programme <span class="req" aria-hidden="true">*</span></label>
          <textarea id="f-msg" name="message" data-required data-minlen="20" required
            placeholder="Building type, size, disciplines, stage, level of information need, programme, and any workflow you would like automated."></textarea>
          <p class="err" data-for="f-msg" role="alert"></p></div>

        <!-- Progressive qualification. Everything below is optional and closed by
             default: a longer form qualifies better and converts worse, so the
             detail is available to anyone who wants to give it and costs nothing
             to anyone who does not. Field names map to crm.leads columns via
             fn_process_submission; do not rename without migrating. -->
        <details class="form__more field--full">
          <summary>Add project detail &mdash; optional, and it makes the reply more useful</summary>
          <div class="form__more-in">
            <div class="field"><label for="f-role">Your role</label>
              <input id="f-role" name="job_title" type="text" autocomplete="organization-title"
                     placeholder="e.g. BIM manager, project engineer"></div>

            <div class="field"><label for="f-type">Project type</label>
              <input id="f-type" name="project_type" type="text"
                     placeholder="e.g. new build, fit-out, refurbishment"></div>

            <div class="field"><label for="f-size">Approximate project size</label>
              <select id="f-size" name="project_size">
                <option value="">Select&hellip;</option>
                <option>Under 5,000 m&sup2;</option>
                <option>5,000 &ndash; 20,000 m&sup2;</option>
                <option>20,000 &ndash; 100,000 m&sup2;</option>
                <option>Over 100,000 m&sup2;</option>
                <option>Multiple buildings / programme</option>
                <option>Not a building &mdash; workflow or automation</option>
              </select></div>

            <div class="field"><label for="f-due">Required delivery date</label>
              <input id="f-due" name="required_delivery_date" type="date"></div>

            <fieldset class="field field--full choices">
              <legend>Disciplines involved</legend>
              <label><input type="checkbox" name="disciplines" value="Mechanical"> Mechanical</label>
              <label><input type="checkbox" name="disciplines" value="Electrical"> Electrical</label>
              <label><input type="checkbox" name="disciplines" value="Public health"> Public health</label>
              <label><input type="checkbox" name="disciplines" value="Fire protection"> Fire protection</label>
              <label><input type="checkbox" name="disciplines" value="Structural"> Structural</label>
              <label><input type="checkbox" name="disciplines" value="Architectural"> Architectural</label>
            </fieldset>

            <fieldset class="field field--full choices">
              <legend>Is there an existing model?</legend>
              <label><input type="radio" name="existing_model" value="true"> Yes</label>
              <label><input type="radio" name="existing_model" value="false"> No</label>
            </fieldset>
          </div>
        </details>

        <div class="form__foot">
          <p class="tiny" style="max-width:44ch">By sending this enquiry you agree to our
          <a href="privacy.html" style="color:var(--text-2)">Privacy Policy</a>. We use these
          details only to respond to your enquiry, and we will not add you to a mailing list.</p>
          <button class="btn btn--primary btn--lg" type="submit">Send enquiry</button>
        </div>
        <p class="form-status" data-form-status hidden></p>
      </form>

      <div class="form-success" data-form-success hidden tabindex="-1" style="margin-top:24px">
        <p class="eyebrow">Enquiry received</p>
        <h3 style="font-size:22px">Thank you &mdash; we have your enquiry.</h3>
        <p class="lede" style="margin-top:12px">It has been logged and routed to the right person.
        We respond within two working days. If it is urgent, call
        <a href="tel:{TEL}" style="color:var(--sig)">{PHONE}</a>.</p>
      </div>
    </div>

    <div>
      <div class="panel">
        <div class="panel__bar"><span><b>DIRECT</b> / ENGINEERING</span><span class="panel__dot"><i></i>OPEN</span></div>
        <div class="panel__body">
          <dl class="cta__side" style="border:0;padding:0;background:none">
            <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
            <dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
            <dt>Reaches</dt><dd>Somnath Baste, Founder</dd>
            <dt>Response</dt><dd>Within two working days</dd>
          </dl>
        </div>
      </div>

      <div class="note" style="margin-top:24px">
        <p><strong>What happens next.</strong> Your enquiry reaches the founder, not a sales queue.
        You get a technical reply on approach, disciplines and deliverables — and where we think a
        workflow is not worth automating, we will say that too.</p>
      </div>
      <div class="note" style="margin-top:18px">
        <p><strong>NDAs.</strong> We sign before drawings or models are shared, as a matter of
        course. Send yours or ask for ours.</p>
      </div>
      <div class="note note--sig" style="margin-top:18px">
        <p><strong>Evaluating the intelligence layer?</strong> Ask for a working session instead of a
        proposal. We will screen-share the internal tooling, the rule sets and real QA output on a
        live workflow. Anything marked <em>in development</em> on this site can be demonstrated;
        anything marked <em>roadmap</em> cannot, and we will not pretend otherwise.</p>
      </div>
    </div>
  </div>
</section>
"""


THANKYOU = f"""
<section class="section section--flush">
  <div class="shell shell--narrow">
    <div class="form-success" style="padding:40px 42px">
      <p class="eyebrow">Enquiry received</p>
      <h1 class="sec-title">Thank you — we have your enquiry.</h1>
      <p class="sec-lede">It has reached the founder directly. You will get a technical response
      within two working days: approach, disciplines, deliverables and an honest read on what is
      realistically automatable in what you have described.</p>
      <p class="lede" style="margin-top:20px">If it is urgent, call <a href="tel:{TEL}"
        style="color:var(--sig)">{PHONE}</a> or reply to the confirmation email with the drawing
        set.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="index.html">Back to home</a>
        <a class="btn btn--ghost" href="engineering.html">Explore our services</a>
      </div>
    </div>
  </div>
</section>
"""


NOTFOUND = """
<section class="nf">
  <div class="shell">
    <p class="nf__code">ERROR 404 — CONTAINER NOT FOUND</p>
    <h1>This page is not in the model.</h1>
    <p>The link is wrong, or the page has moved. The pages below are the current structure.</p>
    <div class="nf__links">
      <a class="btn btn--primary" href="index.html">Home</a>
      <a class="btn btn--ghost" href="engineering.html">Services</a>
      <a class="btn btn--ghost" href="industries.html">Industries</a>
      <a class="btn btn--ghost" href="contact.html">Discuss your project</a>
    </div>
  </div>
</section>
"""


PROJECT_TEMPLATE = f"""
<section class="section section--flush">
  <div class="shell">
    <h1 class="sec-title" style="margin-bottom:24px">Case study template</h1>
    <h2 class="eyebrow" style="margin-bottom:12px">How to use this file</h2>
    <div class="note" style="max-width:none;margin-bottom:48px">
      <p><strong>This is the case study template.</strong> Duplicate this file, rename it
      (for example <code>project-riverside-hospital.html</code>), replace every highlighted
      placeholder, update the title and meta description in the <code>&lt;head&gt;</code>, link it
      from <code>projects.html</code>, and add the URL to <code>sitemap.xml</code>. Delete this
      note before publishing.</p>
      <p><strong>Do not publish a number you cannot evidence.</strong> If a figure has no measured
      baseline, delete the line rather than estimating. The measurement rules are published on the
      projects page and this template exists to enforce them.</p>
    </div>

    <article class="case">
      <div class="case__h">
        <div>
          <p class="case__k"><span class="fill">Sector</span> · <span class="fill">Scale</span> ·
          <span class="fill">Stage</span></p>
          <h3><span class="fill">One sentence stating the engineering problem, not the building name</span></h3>
        </div>
        {B('live', 'Client released')}
      </div>
      <div class="case__b">
        <div class="case__c"><h3>01 Problem</h3>
          <p><span class="fill">What was slow, repetitive, unreliable or unresolvable at this
          project's scale. In the client's terms.</span></p></div>
        <div class="case__c"><h3>02 BIM data</h3>
          <ul><li><span class="fill">Element count</span></li>
          <li><span class="fill">Disciplines and systems</span></li>
          <li><span class="fill">Level of information need</span></li>
          <li><span class="fill">Exchange formats</span></li></ul></div>
        <div class="case__c"><h3>03 Intelligence</h3>
          <ul><li><span class="fill">What was read from the model</span></li>
          <li><span class="fill">Which rules were applied</span></li>
          <li><span class="fill">What the analysis found</span></li>
          <li><span class="fill">What it could not determine</span></li></ul></div>
        <div class="case__c"><h3>04 Automation</h3>
          <ul><li><span class="fill">Steps automated</span></li>
          <li><span class="fill">Steps kept manual, and why</span></li>
          <li><span class="fill">Engineer review point</span></li>
          <li><span class="fill">False-positive rate</span></li></ul></div>
        <div class="case__c case__c--impact"><h3>05 Impact</h3>
          <p><span class="fill">Measured against a stated baseline, with the method named. Delete
          this block entirely if no figure can be evidenced.</span></p></div>
      </div>
      <div class="case__f"><span class="fill">What did not work, what was abandoned, what had to be
      rewritten.</span></div>
    </article>
  </div>
</section>
"""


# ============================================================================
#  SERVICE / INDUSTRY / LOCATION CLUSTERS
#  Content lives in _services.py, _industries.py and _locations.py. This
#  section is layout only — if a page reads thin, the fix is in the content
#  module, not here.
# ============================================================================
# Aliased on import: build.py already uses INDUSTRY_PAGES for the sector hub page
# body, and a silent rebind would be a very confusing bug to find.
from _services import SERVICES as SERVICE_PAGES, SERVICE_BY_SLUG        # noqa: E402
from _industries import INDUSTRIES as INDUSTRY_PAGES, INDUSTRY_BY_SLUG  # noqa: E402
from _locations import LOCATIONS as LOCATION_PAGES, LOCATION_BY_SLUG    # noqa: E402
import _mcp                                               # noqa: E402

# Footer link inventory — built from the same lists that build the pages, so
# the footer cannot point at a page that does not exist or omit one that does.
SERVICES_FOOT = [(f"services/{s['slug']}.html", s["nav"]) for s in SERVICE_PAGES[:6]] + \
                [("engineering.html", "All services")]
INDUSTRIES_FOOT = [(f"industries/{i['slug']}.html", i["nav"]) for i in INDUSTRY_PAGES]
LOCATIONS_FOOT = [(f"locations/{l['slug']}.html", l["nav"]) for l in LOCATION_PAGES] + \
                 [("locations.html", "How we work remotely")]


def foot_links(pairs):
    return "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t in pairs)


def prose(blocks):
    """Two-column argument blocks. Long-form prose in a single measure reads
    better than a card grid, and these are arguments rather than features."""
    return "\n".join(f"""    <div class="argu">
      <h3>{h}</h3>
      <p>{p}</p>
    </div>""" for h, p in blocks)


def spec_rows(rows, kicker="Deliverable"):
    return "\n".join(f"""      <div class="spec__row">
        <div class="spec__k">{kicker}<b>{n}</b></div>
        <div class="spec__v">{d}</div>
      </div>""" for n, d in rows)


def badged_rows(rows, kicker="Automation"):
    return "\n".join(f"""      <div class="spec__row">
        <div class="spec__k">{kicker}<b>{n}</b>{B(s)}</div>
        <div class="spec__v">{d}</div>
      </div>""" for n, s, d in rows)


def step_cards(steps):
    return "\n".join(f"""      <article class="flow">
        <div class="flow__top"><span class="flow__n">{n}</span></div>
        <h3>{t}</h3>
        <p>{d}</p>
      </article>""" for n, t, d in steps)


def bullets(items):
    return "\n".join(f"        <li>{i}</li>" for i in items)


def rel_for(service_slugs=(), industry_slugs=(), location_slugs=(), extra=()):
    out = []
    for s in service_slugs:
        v = SERVICE_BY_SLUG[s]
        out.append((f"services/{v['slug']}.html", strip_tags(v["nav"]), strip_tags(v["lede"])[:104] + "…"))
    for s in industry_slugs:
        v = INDUSTRY_BY_SLUG[s]
        out.append((f"industries/{v['slug']}.html", strip_tags(v["nav"]), strip_tags(v["lede"])[:104] + "…"))
    for s in location_slugs:
        v = LOCATION_BY_SLUG[s]
        out.append((f"locations/{v['slug']}.html", strip_tags(v["nav"]),
                    strip_tags(v["lede"])[:104] + "…"))
    return out + list(extra)


# --------------------------------------------------------------- service --
def service_page(s):
    slug = s["slug"]
    url = f"services/{slug}.html"
    body = f"""
{phero([("Home", "index.html"), ("Engineering", "engineering.html"), (strip_tags(s["nav"]), None)],
       s["h1"], s["lede"], s["meta"])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">{s["eyebrow"]}</p>
      <h2 class="sec-title">The engineering position</h2>
    </header>
    <div class="argu__set">
{prose(s["position"])}
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Deliverables</p>
      <h2 class="sec-title">What is actually produced and issued</h2>
      <p class="sec-lede">Any of these can be appointed on their own or combined. Nothing here
      depends on buying the intelligence layer, which is not for sale in any case.</p>
    </header>
    <div class="spec">
{spec_rows(s["delivers"])}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">How it runs</p>
      <h2 class="sec-title">The sequence, and why it is in this order</h2>
      <p class="sec-lede">Sequence is not a formality on this kind of work. Most of the expensive
      rework we are asked to fix was produced by doing step four before step two.</p>
    </header>
    <div class="flows">
{step_cards(s["process"])}
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell split">
    <div>
      <p class="eyebrow">What we need to start</p>
      <h2 class="sec-title">The inputs that decide whether a start is a real start</h2>
      <p class="sec-lede">Missing any of these is survivable. Not knowing which of them are missing
      is not, so we establish it at enquiry stage rather than at forty per cent.</p>
      <ul class="spec__list" style="margin-top:22px">
{bullets(s["inputs"])}
      </ul>
      <a class="btn btn--ghost" style="margin-top:30px" href="contact.html?service={s['prefill']}">Send us what you have</a>
    </div>
    <div>
      <p class="eyebrow">Automation</p>
      <h2 class="sec-title">Where automation applies to this work</h2>
      <p class="sec-lede">Every line carries its real status. Three of the four states on this site
      mean "not yet", and we use them.</p>
      <div class="spec" style="margin-top:22px">
{badged_rows(s["autos"])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Scope boundary</p>
      <h2 class="sec-title">What this appointment does not include</h2>
      <p class="sec-lede">Published because a scope boundary discovered at month three is a dispute,
      and the same boundary stated at enquiry stage is just information.</p>
    </header>
    <div class="note" style="max-width:none">
      <ul class="spec__list">
{bullets(s["nots"])}
      </ul>
    </div>
  </div>
</section>
{faq_block(s["faqs"])}
{related_block("Where this connects", s["related"])}
"""
    ld = (breadcrumb_ld([("Home", ""), ("Services", "engineering.html"),
                         (strip_tags(s["nav"]), url)])
          + service_ld(strip_tags(s["h1"]), s["desc"], url,
                       area=["United States", "United Kingdom", "United Arab Emirates",
                             "Saudi Arabia", "Australia", "Canada", "India"],
                       service_type=strip_tags(s["eyebrow"]))
          + faq_ld(s["faqs"]))
    page(f"services/{slug}", s["title"], s["desc"], body, "engineering.html", extra=ld,
         cta_block=cta_band(
             f"Talk to an engineer about {strip_tags(s['nav']).lower()}.",
             "Send a scope, a drawing set or the workflow you want this applied to. You will get a "
             "technical response on approach, disciplines, deliverables and what is realistically "
             "automatable — from an engineer, not a sales desk.",
             primary=("contact.html", "Discuss your project"),
             secondary=("engineering.html", "See all engineering services"),
             prefill=s["prefill"]))


# -------------------------------------------------------------- industry --
def industry_page(i):
    slug = i["slug"]
    url = f"industries/{slug}.html"
    svc_links = "\n".join(
        f'        <li><a href="services/{x}.html">{strip_tags(SERVICE_BY_SLUG[x]["nav"])}</a></li>'
        for x in i["services"])
    body = f"""
{phero([("Home", "index.html"), ("Industries", "industries.html"), (strip_tags(i["nav"]), None)],
       i["h1"], i["lede"], i["meta"])}

<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">{i["eyebrow"]}</p>
      <h2 class="sec-title">What makes coordination hard in this sector</h2>
    </header>
    <div class="argu__set">
{prose(i["profile"])}
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Difficulty drivers</p>
      <h2 class="sec-title">Where the effort actually goes</h2>
      <p class="sec-lede">Services density and constraint tightness set coordination effort far more
      than floor area does. These are the drivers that dominate here.</p>
    </header>
    <div class="spec">
{spec_rows(i["drivers"], kicker="Driver")}
    </div>
    <div class="note" style="max-width:none">
      <p><strong>Leading discipline.</strong> {i["lead_disc"]}</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div>
      <p class="eyebrow">Information requirements</p>
      <h2 class="sec-title">What the model has to be able to answer here</h2>
      <p class="sec-lede">Level of information need is a sector-specific question. These are the
      requirements that are characteristic of this building type rather than generic to BIM.</p>
      <ul class="spec__list" style="margin-top:22px">
{bullets(i["info_req"])}
      </ul>
    </div>
    <div>
      <p class="eyebrow">Automation</p>
      <h2 class="sec-title">Where automation earns its place here</h2>
      <p class="sec-lede">Not everywhere, and not equally. Each line carries its real status.</p>
      <div class="spec" style="margin-top:22px">
{badged_rows(i["autos"], kicker="Applies")}
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell split">
    <div>
      <p class="eyebrow">Services</p>
      <h2 class="sec-title">The capabilities that matter most here</h2>
      <ul class="spec__list" style="margin-top:22px">
{svc_links}
      </ul>
      <a class="btn btn--ghost" style="margin-top:30px" href="engineering.html">All engineering services</a>
    </div>
    <div>
      <div class="note" style="max-width:none">
        <p><strong>What this page does and does not say.</strong> It describes the discipline mix,
        the coordination character and the workflow fit for this building type. It does not claim
        completed projects in the sector.</p>
        <p>This site publishes no client logos, no project counts and no testimonials, because none
        have been released and verified yet. If you want evidence rather than a description at
        enquiry stage, ask for a working session — we will screen-share the rule sets and live QA
        output under NDA. <a href="projects.html" style="color:var(--sig)">The projects page</a>
        explains the measurement rules we have committed to in advance.</p>
      </div>
    </div>
  </div>
</section>
{faq_block(i["faqs"])}
{related_block("Where this connects",
               rel_for(service_slugs=i["services"][:3],
                       extra=[("industries.html", "All sectors",
                               "Where coordination difficulty sits across the eight building types "
                               "our discipline mix suits."),
                              ("locations.html", "International delivery",
                               "How remote delivery is actually run, market by market.")]))}
"""
    ld = (breadcrumb_ld([("Home", ""), ("Industries", "industries.html"),
                         (strip_tags(i["nav"]), url)]) + faq_ld(i["faqs"]))
    page(f"industries/{slug}", i["title"], i["desc"], body, "industries.html", extra=ld,
         cta_block=cta_band(
             f"Discuss a {strip_tags(i['nav']).lower()} project.",
             "Send the scope, the stage and the disciplines. You will get a technical response on "
             "approach, deliverables and where automation is and is not worth applying on a project "
             "of this type.",
             secondary=("industries.html", "Compare sectors")))


# -------------------------------------------------------------- location --
def location_page(l):
    slug = l["slug"]
    url = f"locations/{slug}.html"
    svc_links = "\n".join(
        f'        <li><a href="services/{x}.html">{strip_tags(SERVICE_BY_SLUG[x]["nav"])}</a></li>'
        for x in l["services"])
    sec_links = "\n".join(
        f'        <li><a href="industries/{x}.html">{strip_tags(INDUSTRY_BY_SLUG[x]["nav"])}</a></li>'
        for x in l["sectors"])
    body = f"""
{phero([("Home", "index.html"), ("Locations", "locations.html"), (strip_tags(l["nav"]), None)],
       l["h1"], l["lede"], l["meta"])}

<section class="section section--flush">
  <div class="shell">
    <div class="note note--sig" style="max-width:none">
      <p><strong>Read this before anything else on the page.</strong> BIMRACE is an India-based
      engineering practice delivering remotely. We do not have an office, a registered entity or
      professional licensure in {strip_tags(l["nav"])}, and this page does not imply that we do.</p>
      <ul class="spec__list" style="margin-top:14px">
{bullets(l["honest"])}
      </ul>
      <p style="margin-top:14px">This section exists because implying local presence is the most
      common form of dishonesty in this sector's international marketing, and it is cheap to tell
      and expensive to be caught in.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">{l["eyebrow"]}</p>
      <h2 class="sec-title">What is actually different about working here</h2>
    </header>
    <div class="argu__set">
{prose(l["intro"])}
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Standards basis</p>
      <h2 class="sec-title">What the engineering is written to</h2>
      <p class="sec-lede">General industry context, not legal advice and not a claim of
      accreditation. Which of these applies to your project is a fact we ask for rather than
      assume — assuming it is a common and expensive failure in offshore work.</p>
    </header>
    <div class="spec">
{spec_rows(l["standards"], kicker="Basis")}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div>
      <p class="eyebrow">Working hours</p>
      <h2 class="sec-title">The overlap, stated specifically enough to hold us to</h2>
      <p class="sec-lede">{l["overlap"]}</p>
    </div>
    <div>
      <p class="eyebrow">Collaboration model</p>
      <h2 class="sec-title">How the appointment actually runs</h2>
      <div class="spec" style="margin-top:22px">
{spec_rows(l["model"], kicker="Model")}
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Typical engagements</p>
      <h2 class="sec-title">What teams in this market actually appoint us for</h2>
    </header>
    <div class="spec">
{spec_rows(l["typical"], kicker="Engagement")}
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div>
      <p class="eyebrow">Services</p>
      <h2 class="sec-title">Relevant capabilities</h2>
      <ul class="spec__list" style="margin-top:22px">
{svc_links}
      </ul>
      <a class="btn btn--ghost" style="margin-top:24px" href="engineering.html">All engineering services</a>
    </div>
    <div>
      <p class="eyebrow">Sectors</p>
      <h2 class="sec-title">Relevant building types</h2>
      <ul class="spec__list" style="margin-top:22px">
{sec_links}
      </ul>
      <a class="btn btn--ghost" style="margin-top:24px" href="industries.html">All sectors</a>
    </div>
  </div>
</section>
{faq_block(l["faqs"], title=f"Working with BIMRACE from {strip_tags(l['nav'])}",
           lede="The licensure question is answered first, because it is the one that decides "
                "whether the rest of the conversation is worth having.")}
{related_block("Where this connects",
               rel_for(location_slugs=[x["slug"] for x in LOCATION_PAGES if x["slug"] != slug][:4],
                       extra=[("locations.html", "International delivery",
                               "How remote delivery is run, and the boundary we hold in every "
                               "market."),
                              ("about.html", "About BIMRACE",
                               "Who this is, where it is, and what it does not claim to be.")]),
               eyebrow="Other markets")}
"""
    ld = (breadcrumb_ld([("Home", ""), ("Locations", "locations.html"),
                         (strip_tags(l["nav"]), url)]) + faq_ld(l["faqs"]))
    page(f"locations/{slug}", l["title"], l["desc"], body, "locations.html", extra=ld,
         cta_block=cta_band(
             f"Discuss a project in {strip_tags(l['nav'])}.",
             "Send the scope, the standards basis and the stage. You will get a technical response "
             "from an engineer — including an honest read on where our remote model fits your "
             "project and where it does not.",
             secondary=("locations.html", "How remote delivery works")))


# ------------------------------------------------------------ locations hub --
def locations_hub():
    cards = "\n".join(f"""      <a class="hub__i" href="locations/{l['slug']}.html">
        <span class="hub__t">{l['nav']}</span>
        <span class="hub__d">{strip_tags(l['lede'])}</span>
        <span class="hub__m">{strip_tags(l['meta'][1][0])}: {strip_tags(l['meta'][1][1])}</span>
      </a>""" for l in LOCATION_PAGES)
    body = f"""
{phero([("Home", "index.html"), ("Locations", None)],
       "International delivery, and the boundary we hold in every market",
       "BIMRACE is an India-based engineering practice working remotely with project teams "
       "internationally. These pages set out the standards basis, the working overlap and the "
       "collaboration model per market — and state, on every one of them, that we hold no local "
       "office and no local licensure.",
       [("Based", "India"), ("Offices elsewhere", "None"),
        ("Licensure elsewhere", "None"), ("Markets described", str(len(LOCATION_PAGES)))])}

<section class="section section--flush">
  <div class="shell">
    <div class="note note--sig" style="max-width:none">
      <p><strong>The one thing worth saying before the rest.</strong> Every market page on this site
      begins by stating that BIMRACE has no office, no registered entity and no professional
      licensure in that market. That is not a disclaimer we were forced into — it is the position,
      and it determines the only delivery model we offer: engineering and BIM production behind
      your licensed engineer, consultant or practitioner of record.</p>
      <p>The alternative — an offshore provider implying local presence and local sign-off — is
      common, cheap to claim and impossible to honour. If a competitor's location page does not tell
      you where their engineers are licensed, that is the question to ask them.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Markets</p>
      <h2 class="sec-title">Where we work, and what differs</h2>
      <p class="sec-lede">These pages exist because the standards basis, the approval route and the
      practical working overlap genuinely differ by market. They are not the same page with a
      country name substituted, and if one of them reads that way it is a defect.</p>
    </header>
    <div class="hub">
{cards}
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Delivery model</p>
      <h2 class="sec-title">How remote engineering delivery is actually run</h2>
      <p class="sec-lede">The failure modes of offshore delivery are well known and largely
      avoidable. These are the ones we design against.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">01<b>A fixed handover, not an expectation of overlap</b></div>
        <div class="spec__v">Where the time difference is large, we agree a daily handover time and
        a written note of what progressed, what is blocked and what needs a decision. An overlap
        nobody has scheduled is not an overlap, and "we're flexible" is how two teams end up waiting
        for each other.</div></div>
      <div class="spec__row"><div class="spec__k">02<b>Your standards, your environment</b></div>
        <div class="spec__v">We work inside your templates, your BEP and your CDE wherever they
        exist, so the deliverable arrives usable rather than requiring a translation step. Where
        there is no standard, we apply ours and hand over the documentation for it.</div></div>
      <div class="spec__row"><div class="spec__k">03<b>Rule sets instead of supervision</b></div>
        <div class="spec__v">Consistency across a distributed team is not achievable by watching
        people. It is achievable by writing the check down and running it on every model, every
        time. This is the single largest reason our remote delivery holds together at
        volume.</div></div>
      <div class="spec__row"><div class="spec__k">04<b>Your engineer of record, always</b></div>
        <div class="spec__v">Statutory sign-off, authority submission and professional
        responsibility sit with your licensed engineer, consultant or practitioner. We produce the
        engineering and BIM deliverables that go into that; we never imply we can replace
        it.</div></div>
      <div class="spec__row"><div class="spec__k">05<b>NDA before drawings</b></div>
        <div class="spec__v">Signed as a matter of course before any model or drawing set is shared.
        Send yours or ask for ours.</div></div>
      <div class="spec__row"><div class="spec__k">06<b>A named person, not a queue</b></div>
        <div class="spec__v">Enquiries reach the founder directly. On an appointment, a named
        engineer is accountable for what we issue, and their name is on it.</div></div>
    </div>
  </div>
</section>
{faq_block([
 ("Do you have offices outside India?",
  "No. BIMRACE is an India-based practice and every market page on this site says so explicitly. "
  "We do not list foreign addresses or phone numbers, because we do not have them."),
 ("Can your engineers sign off or stamp drawings in our country?",
  "No. No BIMRACE engineer holds professional licensure or registration in any of the markets "
  "described on this site. All engineering we produce is delivered under your licensed engineer, "
  "consultant or practitioner of record, who reviews it and takes professional responsibility."),
 ("Which markets do you actually work with?",
  "The markets described on these pages are where our standards familiarity and working overlap "
  "make a remote appointment workable. We are not claiming project history in each one — this site "
  "publishes no project history until a client releases it."),
 ("How do you handle a large time difference?",
  "With a scheduled daily handover and a written progress, blocker and decision note, rather than "
  "an expectation of live availability. For the US and Canada the practical benefit is overnight "
  "progression; for the UK, Europe, the Gulf and Australia there is real same-day overlap."),
 ("What happens to our model data?",
  "It stays inside the environment agreed in the appointment, under an NDA signed before anything "
  "is shared. Where a client requires work to be done inside their own environment and systems, "
  "that is the normal team-extension arrangement."),
], title="International delivery — the questions that decide it",
   lede="Starting with the two that a location page should never make you go looking for.")}
{related_block("Where this connects", [
  ("engineering.html", "Engineering services",
   "The five capability groups, and every deliverable in them."),
  ("industries.html", "Industries",
   "Where coordination difficulty sits across eight building types."),
  ("technology.html", "Standards and QA",
   "ISO 19650 information management and the checks applied before issue."),
  ("about.html", "About BIMRACE",
   "Who this is, where it is, and what it does not claim to be."),
])}
"""
    faqs_for_ld = [
        ("Do you have offices outside India?",
         "No. BIMRACE is an India-based practice and every market page on this site says so "
         "explicitly. We do not list foreign addresses or phone numbers, because we do not have "
         "them."),
        ("Can your engineers sign off or stamp drawings in our country?",
         "No. No BIMRACE engineer holds professional licensure or registration in any of the "
         "markets described on this site. All engineering we produce is delivered under your "
         "licensed engineer, consultant or practitioner of record."),
    ]
    ld = (breadcrumb_ld([("Home", ""), ("Locations", "locations.html")]) + faq_ld(faqs_for_ld))
    page("locations",
         "International MEP &amp; BIM Delivery | BIMRACE",
         "MEP engineering and BIM delivered remotely to the USA, UK, UAE, Saudi Arabia, Australia, "
         "Canada and Europe — with the licensure boundary stated on every market page.",
         body, "locations.html", extra=ld,
         cta_block=cta_band(
             "Tell us where the project is and what stage it is at.",
             "You will get a technical response from an engineer, including an honest read on "
             "whether our remote model suits your project's approval route — and where it does "
             "not.",
             secondary=("engineering.html", "See what is delivered")))


REDIRECT_PAGES = [
    ("capabilities", "engineering.html", "Capabilities"),
]


def redirect_page(slug, target, label):
    """A static-host-safe redirect. Also emit 301s in netlify.toml for hosts
    that read it; Amplify needs an equivalent rule set in its console."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{label} has moved | BIMRACE</title>
<meta name="description" content="This page has moved. {label} is now published at
/{target} as part of the BIMRACE platform restructure.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{SITE}/{target}">
<meta http-equiv="refresh" content="0; url=/{target}">
<meta name="theme-color" content="{THEME}">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<main id="main" class="nf">
  <div class="shell">
    <p class="nf__code">MOVED — 301</p>
    <h1>{label} is now Engineering.</h1>
    <p>This page has moved as part of the platform restructure.
    <a href="/{target}" style="color:var(--sig)">Continue to {target}</a>.</p>
  </div>
</main>
</body>
</html>
"""
# No inline <script> redirect: the Content-Security-Policy this site ships with
# sets script-src 'self', which would block it silently. The meta refresh above
# does the work, the real 301 is in netlify.toml and amplify-redirects.json, and
# the visible link is the fallback if both are somehow missing.
    (OUT / f"{slug}.html").write_text(html, encoding="utf-8")


# ============================================================================
#  BUILD
# ============================================================================
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()

DESC_HOME = ("BIMRACE provides MEP engineering design, BIM modelling, Revit coordination and "
             "engineering documentation for architects, contractors, developers and engineering "
             "teams worldwide.")

ORG_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "Organization",
    "name": "BIMRACE", "legalName": ENTITY, "url": SITE + "/",
    "logo": SITE + "/logo.svg", "image": SITE + "/og-image.png",
    "email": EMAIL, "telephone": "+91-75079-58364",
    "description": DESC_HOME,
    "slogan": "MEP engineering and BIM, delivered as one.",
    "address": {"@type": "PostalAddress", "addressCountry": "IN"},
    "founder": {"@type": "Person", "name": "Somnath Baste", "jobTitle": "Founder"},
    "knowsAbout": [
        "MEP Engineering", "HVAC Design", "Electrical Design",
        "Plumbing and Public Health Design", "Fire Protection Design",
        "Building Information Modelling", "Revit MEP", "BIM Coordination",
        "Clash Detection", "BIM Modelling and Documentation", "ISO 19650",
        "Model Quality Assurance", "BIM Automation", "Revit Automation",
    ],
    "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "email": EMAIL,
                      "telephone": "+91-75079-58364", "availableLanguage": ["en"]}]
}, indent=2) + '</script>\n'

SERVICE_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "ItemList",
    "name": "BIMRACE service categories",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "item": {"@type": "Service", "name": n, "description": d,
                  "provider": {"@type": "Organization", "name": "BIMRACE"},
                  "url": f"{SITE}/{u}"}}
        for i, (n, d, u) in enumerate([
            ("MEP Engineering",
             "Mechanical, electrical, public health and fire protection engineering modelled as "
             "connected systems.", "engineering.html#mep"),
            ("BIM Modelling and Documentation",
             "Discipline models authored to an agreed level of information need, with model-derived "
             "drawings and schedules.", "engineering.html#modelling"),
            ("BIM Coordination",
             "Federated models, clash detection, clearance and access checking, with decisions "
             "tracked to closure.", "engineering.html#coordination"),
            ("Design and Engineering Automation",
             "Parametric and scripted automation of model production, checking, documentation and "
             "quantity extraction.", "engineering.html#automation"),
            ("Construction Support",
             "Shop and fabrication drawings, builders work, as-built models and quantity take-off.",
             "engineering.html#construction"),
        ])]
}, indent=2) + '</script>\n'

FAQ_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Is the BIMRACE AI platform available to buy?",
         "acceptedAnswer": {"@type": "Answer", "text":
          "No. The intelligence layer is internal software in development, used on our own delivery. "
          "It is not a released product and is not offered for licence. Capabilities on the website "
          "are labelled live, in development or roadmap."}},
        {"@type": "Question", "name": "Does BIMRACE automation change models without review?",
         "acceptedAnswer": {"@type": "Answer", "text":
          "No. Automated routines read models, apply engineering rules and draft output. They do not "
          "write to a live model, close an issue, change a status code or issue a deliverable. A "
          "named engineer accepts, amends or rejects every output."}},
        {"@type": "Question", "name": "Is BIMRACE certified to ISO 19650?",
         "acceptedAnswer": {"@type": "Answer", "text":
          "No. BIMRACE structures delivery to align with ISO 19650 principles on every appointment. "
          "That is a statement of working method, not third-party certification."}},
        {"@type": "Question", "name": "Does BIMRACE deliver digital twins?",
         "acceptedAnswer": {"@type": "Answer", "text":
          "Not yet. A digital twin requires a BIM model, asset data, live data, engineering rules and "
          "analytics. BIMRACE delivers the first two today and structures models so a twin remains "
          "possible later. Live data and analytics are roadmap, not built."}},
    ]
}, indent=2) + '</script>\n'

page("index",
     "MEP Engineering &amp; BIM Services for Building Projects | BIMRACE",
     DESC_HOME,
     HOME, "index.html", extra=ORG_LD + SERVICE_LD + FAQ_LD)

page("platform",
     "Intelligence Stack | BIM, AI &amp; Automation | BIMRACE",
     "The five-layer BIMRACE intelligence stack — BIM data, engineering rules, AI analysis, "
     "automation and output — with every component honestly labelled.",
     PLATFORM, "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html"), ("Capability status", "platform.html")]))

page("intelligence",
     "BIM Intelligence | The Model as a Database | BIMRACE",
     "How BIM becomes a queryable engineering data layer: what a model holds, and the "
     "information-first authoring discipline that makes it usable.",
     INTELLIGENCE, "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html"),
                          ("BIM Intelligence", "intelligence.html")]))

page("automation",
     "AI &amp; Engineering Automation for BIM | BIMRACE",
     "AI-assisted engineering workflows, automated BIM QA, clash intelligence and quantity "
     "extraction — with an engineering approval step at the end of every one.",
     AUTOMATION, "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html"),
                          ("AI and Automation", "automation.html")]))

page("digital-twin",
     "Digital Twin | What a Twin Actually Requires | BIMRACE",
     "A digital twin needs a model, asset data, live data, engineering rules and analytics. "
     "BIMRACE delivers two of the five today, and publishes which two.",
     DIGITAL_TWIN, "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html"),
                          ("Digital Twin", "digital-twin.html")]))

# The hubs link down to every child page. Without this block the new cluster
# pages are reachable only from the footer, which is how orphan pages happen.
SERVICE_HUB = f"""
<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Service pages</p>
      <h2 class="sec-title">Each capability in detail</h2>
      <p class="sec-lede">Deliverables, sequence, required inputs, where automation applies and what
      the appointment does not include — set out per service rather than summarised.</p>
    </header>
    <div class="hub">
{chr(10).join(f'''      <a class="hub__i" href="services/{s['slug']}.html">
        <span class="hub__t">{s['nav']}</span>
        <span class="hub__d">{strip_tags(s['lede'])}</span>
        <span class="hub__m">{strip_tags(s['eyebrow'])}</span>
      </a>''' for s in SERVICE_PAGES)}
    </div>
  </div>
</section>"""

INDUSTRY_HUB = f"""
<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Sector pages</p>
      <h2 class="sec-title">Each sector in detail</h2>
      <p class="sec-lede">What drives coordination difficulty, which discipline dominates, what the
      model has to be able to answer, and where automation earns its place — per building type.</p>
    </header>
    <div class="hub">
{chr(10).join(f'''      <a class="hub__i" href="industries/{i['slug']}.html">
        <span class="hub__t">{i['nav']}</span>
        <span class="hub__d">{strip_tags(i['lede'])}</span>
        <span class="hub__m">{strip_tags(i['meta'][0][0])}: {strip_tags(i['meta'][0][1])}</span>
      </a>''' for i in INDUSTRY_PAGES)}
    </div>
  </div>
</section>"""

LOCATION_STRIP = f"""
<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">International delivery</p>
      <h2 class="sec-title">Where these services are delivered</h2>
      <p class="sec-lede">BIMRACE is an India-based practice working remotely. Every market page
      states the standards basis, the working overlap and — first — that we hold no local office and
      no local licensure there.</p>
    </header>
    <div class="hub hub--tight">
{chr(10).join(f'''      <a class="hub__i" href="locations/{l['slug']}.html">
        <span class="hub__t">{l['nav']}</span>
        <span class="hub__m">{strip_tags(l['meta'][2][0])}: {strip_tags(l['meta'][2][1])}</span>
      </a>''' for l in LOCATION_PAGES)}
    </div>
  </div>
</section>"""

page("engineering",
     "MEP Engineering &amp; BIM Delivery Services | BIMRACE",
     "MEP engineering, BIM modelling, coordination, design automation and construction support "
     "— defined by deliverable, with capability status against every line.",
     ENGINEERING + SERVICE_HUB + LOCATION_STRIP, "engineering.html",
     extra=breadcrumb_ld([("Home", ""), ("Services", "engineering.html")]) + SERVICE_LD)

page("industries",
     "Industries | MEP &amp; BIM by Sector | BIMRACE",
     "Where coordination difficulty actually sits by sector: commercial, residential, "
     "healthcare, data centres, industrial, hospitality, education and retail.",
     INDUSTRIES + INDUSTRY_HUB, "industries.html",
     extra=breadcrumb_ld([("Home", ""), ("Industries", "industries.html")]))

for _s in SERVICE_PAGES:
    service_page(_s)
for _i in INDUSTRY_PAGES:
    industry_page(_i)
locations_hub()
for _l in LOCATION_PAGES:
    location_page(_l)

page("technology/mcp-for-revit",
     "MCP for Revit | Model Context Protocol | BIMRACE",
     "What the Model Context Protocol is, what a Revit MCP server would have to do, and why "
     "BIMRACE has not shipped one. Published as roadmap, not as a product.",
     _mcp.body(B, phero, faq_block, related_block, faq_ld),
     "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html"),
                          ("MCP for Revit", "technology/mcp-for-revit.html")])
           + faq_ld(_mcp.FAQS),
     cta_block=cta_band(
         "Evaluating AI for BIM? Ask for the working session, not the demo.",
         "We will show the extraction and checking work that is real today, describe honestly where "
         "the protocol layer would sit, and tell you which of the claims you have read elsewhere "
         "are further away than they are being presented as.",
         primary=("contact.html", "Discuss your project"),
         secondary=("automation.html", "See the automation workflows"),
         prefill="automation"))

page("projects",
     "Projects | Case Study Structure &amp; Rules | BIMRACE",
     "Case studies structured around the engineering problem. None are published yet — this "
     "page explains exactly why, and what every entry will contain when they are.",
     PROJECTS, "projects.html",
     extra=breadcrumb_ld([("Home", ""), ("Projects", "projects.html")]))

page("technology",
     "Standards &amp; QA | ISO 19650 Delivery | BIMRACE",
     "ISO 19650 information management, the artefacts that govern an appointment, and the six "
     "quality checks applied before anything is issued.",
     TECHNOLOGY, "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("BIM and Technology", "technology.html")]))

page("insights",
     "Insights on MEP Engineering &amp; BIM | BIMRACE",
     "Plain-english explainers on MEP coordination, BIM level of detail, model data quality and "
     "where AI genuinely helps on building projects.",
     INSIGHTS, "insights.html",
     extra=breadcrumb_ld([("Home", ""), ("Insights", "insights.html")])
           + faq_ld(INSIGHTS_FAQS))

page("about",
     "About | An Engineering Practice With Its Own Tools | BIMRACE",
     "BIMRACE is a focused MEP and BIM engineering practice building its own intelligence "
     "layer, and publishing the capability status of every claim on this site.",
     ABOUT, "about.html",
     extra=breadcrumb_ld([("Home", ""), ("About", "about.html")]))

page("contact",
     "Talk to Engineering | Project Enquiry | BIMRACE",
     "Send a scope, a drawing set or a workflow you want automated. You get a technical reply "
     "from an engineer — approach, disciplines and deliverables — within two working days.",
     CONTACT, "contact.html", cta=False,
     extra=breadcrumb_ld([("Home", ""), ("Contact", "contact.html")]))

page("thank-you", "Enquiry received | BIMRACE",
     "Your enquiry has reached BIMRACE. A technical response from an engineer follows within "
     "two working days, and urgent items can be raised by telephone.",
     THANKYOU, "contact.html", cta=False,
     extra='<meta name="robots" content="noindex, follow">\n')

page("404", "Page not found | BIMRACE",
     "The page you requested is not on this site. The current structure of the BIMRACE site is "
     "listed here, with a link to every main section.",
     NOTFOUND, "", cta=False,
     extra='<meta name="robots" content="noindex, follow">\n')

page("project-template", "Case study template | BIMRACE",
     "Internal template for BIMRACE case studies. Not a published page: it is marked noindex "
     "and excluded from the sitemap.",
     PROJECT_TEMPLATE, "projects.html", cta=False,
     extra='<meta name="robots" content="noindex, nofollow">\n')

page("privacy", "Privacy Policy | BIMRACE",
     "How BIMRACE handles personal data submitted through this website: what is collected, "
     "why, how long it is kept, and how to have it removed.",
     PRIVACY, "", cta=False)
page("terms", "Terms of Use | BIMRACE",
     "The terms on which the BIMRACE website is made available, including use of content, "
     "capability statements and the limitation of liability that applies.",
     TERMS, "", cta=False)
page("cookies", "Cookie Policy | BIMRACE",
     "What cookies and third-party requests the BIMRACE website makes, what is stored in your "
     "browser and why, and how to control or remove it.",
     COOKIES, "", cta=False)

for slug, target, label in REDIRECT_PAGES:
    redirect_page(slug, target, label)

# ------------------------------------------------------------- static files --
for f in ["style.css", "script.js", "lead-capture.js", "config.js", "logo.svg", "logo-mark.svg",
          "favicon.svg", "favicon.ico", "apple-touch-icon.png", "icon-192.png", "icon-512.png",
          "og-image.png"]:
    src = ROOT / f
    if src.exists():
        shutil.copy(src, OUT / f)

(OUT / "site.webmanifest").write_text(json.dumps({
    "name": "BIMRACE", "short_name": "BIMRACE",
    "description": "Engineering intelligence built around BIM",
    "start_url": "/", "display": "standalone",
    "background_color": "#FFFFFF", "theme_color": THEME,
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
              {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]
}, indent=2) + "\n", encoding="utf-8")

(OUT / "robots.txt").write_text(
    "# BIMRACE — https://bimrace.com\n"
    "# Everything public is crawlable. The two disallowed paths are a\n"
    "# post-submission page and an internal template; both also carry a\n"
    "# noindex tag, and neither is in the sitemap.\n\n"
    "User-agent: *\n"
    "Allow: /\n"
    "Disallow: /project-template.html\n"
    "Disallow: /thank-you.html\n"
    "Disallow: /_source/\n\n"
    "# Nothing blocks CSS, JS, SVG or images: blocking them breaks rendering\n"
    "# for the crawler and costs more than it protects.\n\n"
    f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

# ------------------------------------------------------------------ sitemap --
# Generated from REGISTRY, which every indexable page appends itself to at build
# time. A page therefore cannot be missing from the sitemap, and the sitemap
# cannot list a URL that was never built. Do not hand-maintain a list here again.
#
# No <priority> and no <changefreq>: Google ignores both, and a file full of
# values nobody reads is a file nobody keeps accurate. <lastmod> is the build
# date, which is honest for a generated static site — every page is rewritten on
# every build.
NOINDEX = {"thank-you.html", "404.html", "project-template.html",
           "capabilities.html"}
SITEMAP_URLS = [u for u in REGISTRY if u not in NOINDEX]
assert len(SITEMAP_URLS) == len(set(SITEMAP_URLS)), "duplicate URL in sitemap registry"
BUILD_DATE = datetime.date.today().isoformat()

(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n"
                f"    <lastmod>{BUILD_DATE}</lastmod>\n  </url>"
                for u in SITEMAP_URLS)
    + "\n</urlset>\n", encoding="utf-8")

# ------------------------------------------------------------ host config --
# Two hosts, two formats, one source of truth. amplify-redirects.json is emitted
# because Amplify reads neither netlify.toml nor _redirects: the 301s written for
# the platform restructure were live on Netlify and dead on Amplify, which is the
# host amplify.yml actually deploys from. Paste the JSON into
# Amplify > App settings > Rewrites and redirects.
REDIRECT_RULES = [
    ("/capabilities", "/engineering.html", 301),
    ("/capabilities.html", "/engineering.html", 301),
    # Directory-style requests for the cluster hubs, so a hand-typed or
    # mis-linked /services/ lands on the hub instead of a 404.
    ("/services", "/engineering.html", 301),
    ("/services/", "/engineering.html", 301),
    ("/industries/", "/industries.html", 301),
    ("/locations/", "/locations.html", 301),
    ("/technology/", "/technology.html", 301),
]

SECURITY_HEADERS = [
    ("X-Frame-Options", "SAMEORIGIN"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "geolocation=(), microphone=(), camera=(), payment=()"),
    ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
    # The enquiry form posts to Supabase and the fonts come from Google.
    # Everything else is same-origin, so the policy can be tight.
    # 'unsafe-inline' is required for style-src only because the generator emits
    # a number of inline style attributes; there is no inline <script> anywhere,
    # so script-src stays strict.
    ("Content-Security-Policy",
     "default-src 'self'; "
     "script-src 'self'; "
     "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
     "font-src 'self' https://fonts.gstatic.com; "
     # The founder photograph on the About page is served from Supabase
     # Storage. Self-hosting it would let this drop to 'self' data:, and the
     # cookie policy already says so.
     "img-src 'self' data: https://*.supabase.co; "
     "connect-src 'self' https://*.supabase.co; "
     "form-action 'self'; "
     "frame-ancestors 'self'; "
     "base-uri 'self'; "
     "object-src 'none'"),
]

_nl = "\n"
(OUT / "netlify.toml").write_text(
    "# Netlify configuration - static site, no build step required." + _nl
    + "# Generated by _source/build.py. Do not edit in place." + _nl + _nl
    + '[build]' + _nl + '  publish = "."' + _nl + _nl
    + "".join('[[redirects]]' + _nl + f'  from = "{f}"' + _nl + f'  to = "{t}"' + _nl
              + f'  status = {c}' + _nl + '  force = true' + _nl + _nl
              for f, t, c in REDIRECT_RULES)
    + '[[redirects]]' + _nl + '  from = "/_source/*"' + _nl
    + '  to = "/404.html"' + _nl + '  status = 404' + _nl + _nl
    + '[[headers]]' + _nl + '  for = "/*"' + _nl + '  [headers.values]' + _nl
    + "".join(f'    {k} = "{v}"' + _nl for k, v in SECURITY_HEADERS) + _nl
    + '[[headers]]' + _nl + '  for = "/*.css"' + _nl + '  [headers.values]' + _nl
    + '    Cache-Control = "public, max-age=31536000, immutable"' + _nl + _nl
    + '[[headers]]' + _nl + '  for = "/*.js"' + _nl + '  [headers.values]' + _nl
    + '    Cache-Control = "public, max-age=31536000, immutable"' + _nl + _nl
    + '[[headers]]' + _nl + '  for = "/*.html"' + _nl + '  [headers.values]' + _nl
    + '    Cache-Control = "public, max-age=0, must-revalidate"' + _nl + _nl
    + '[[headers]]' + _nl + '  for = "/sitemap.xml"' + _nl + '  [headers.values]' + _nl
    + '    Cache-Control = "public, max-age=3600"' + _nl,
    encoding="utf-8")

(OUT / "amplify-redirects.json").write_text(json.dumps(
    [{"source": f, "target": t, "status": str(c), "condition": None}
     for f, t, c in REDIRECT_RULES]
    + [{"source": "/<*>", "target": "/404.html", "status": "404", "condition": None}],
    indent=2) + _nl, encoding="utf-8")

# Amplify's custom-headers editor takes YAML, not JSON. Emitted by hand rather
# than with a yaml library so the generator keeps its no-dependencies rule.
# Every value is single-quoted because the CSP contains ':' and ',', which bare
# YAML scalars treat as structure.
HEADER_GROUPS = [
    ("**", SECURITY_HEADERS),
    ("**/*.css", [("Cache-Control", "public, max-age=31536000, immutable")]),
    ("**/*.js", [("Cache-Control", "public, max-age=31536000, immutable")]),
    ("**/*.html", [("Cache-Control", "public, max-age=0, must-revalidate")]),
]


def _yq(v):
    """Double-quoted YAML scalar. The CSP is full of 'self' and empty of double
    quotes, so double-quoting keeps it readable; single-quoting would double
    every quote in it and make the one value anyone needs to check unreadable."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


(OUT / "amplify-headers.yml").write_text(
    "# BIMRACE - AWS Amplify custom headers." + _nl
    + "# Generated by _source/build.py. Paste into:" + _nl
    + "#   Amplify console > App settings > Custom headers > Edit" + _nl
    + "# Amplify reads netlify.toml for nothing, so this has to be applied by hand." + _nl
    + "customHeaders:" + _nl
    + "".join(
        f"  - pattern: {_yq(pat)}" + _nl
        + "    headers:" + _nl
        + "".join(f"      - key: {_yq(k)}" + _nl + f"        value: {_yq(v)}" + _nl
                  for k, v in hdrs)
        for pat, hdrs in HEADER_GROUPS),
    encoding="utf-8")

# --install copies the build over the deployed folder in one step, so site/
# can never drift from this generator again.
if "--install" in sys.argv:
    site = ROOT.parent / "site"
    keep = {"config.js"}                       # runtime config is environment-specific
    built = set()
    for f in OUT.rglob("*"):
        if f.is_dir():
            continue
        rel = f.relative_to(OUT)
        built.add(rel.as_posix())
        if rel.as_posix() in keep and (site / rel).exists():
            continue
        (site / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, site / rel)
    # A page removed from the generator must disappear from the deployed folder,
    # or it stays live, stays indexed and contradicts the sitemap.
    for stale in site.rglob("*.html"):
        if stale.relative_to(site).as_posix() not in built:
            stale.unlink()
    for d in sorted((p for p in site.rglob("*") if p.is_dir()),
                    key=lambda p: len(p.parts), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    print("installed ->", site)

print(f"built {len(list(OUT.rglob('*.html')))} pages "
      f"({len(SITEMAP_URLS)} indexable) ->", OUT)
