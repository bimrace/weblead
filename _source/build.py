#!/usr/bin/env python3
"""
BIMRACE corporate website — static site generator.

One source of truth for the head, top bar, navigation, CTA band and footer, so
those blocks cannot drift between pages. Run `python3 build.py` after editing.
"""
import json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dist"

SITE   = "https://bimrace.com"
EMAIL  = "info@bimrace.com"
PHONE  = "+91 75079 58364"
TEL    = "+917507958364"
ENTITY = "BIMRACE PVT LTD"

WORD_D = re.search(r'<path d="(.*?)"', (ROOT / "logo.svg").read_text(), re.S).group(1)
WORD_TF = "scale(0.3333333) translate(0,306) scale(0.25,-0.25)"

# --------------------------------------------------------------- navigation --
CAPS = [
    ("bim-modelling",   "BIM Modelling &amp; Documentation", "Architectural, structural and MEP models with drawing production."),
    ("mep-engineering", "MEP Engineering",                   "Mechanical, electrical, plumbing and fire protection services."),
    ("coordination",    "BIM Coordination",                  "Federated models, clash resolution and coordination reporting."),
    ("digital",         "Digital Engineering",               "Automation, parametric workflows and model data management."),
    ("construction",    "Construction Support",              "Shop drawings, as-builts and quantity take-off."),
]

NAV = [
    ("capabilities.html", "Capabilities", CAPS),
    ("industries.html",   "Industries",   None),
    ("projects.html",     "Projects",     None),
    ("technology.html",   "Technology",   None),
    ("about.html",        "About",        None),
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
<meta name="theme-color" content="#FFFFFF">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">

<meta property="og:type" content="website">
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
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<svg class="svg-defs" aria-hidden="true" focusable="false"><defs>
  <g id="wm" fill="currentColor" transform="{WORD_TF}"><path d="{WORD_D}"/></g>
</defs></svg>
"""


def chrome(active):
    caret = '<svg viewBox="0 0 10 6" aria-hidden="true"><path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
    items = []
    for href, label, sub in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if sub:
            links = "\n".join(
                f'          <li><a href="capabilities.html#{a}"><span class="t">{t}</span>'
                f'<span class="d">{d}</span></a></li>' for a, t, d in sub)
            items.append(f"""      <li class="has-menu" data-open="false">
        <button type="button" aria-expanded="false" aria-controls="menu-cap">{label}{caret}</button>
        <ul class="submenu" id="menu-cap">
          <li><a href="{href}"{cur}><span class="t">All capabilities</span><span class="d">Full service architecture and scope.</span></a></li>
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
      <span class="brand__sub">Engineering</span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav__links" id="nav-links">
{nav_items}
        <li class="nav__cta"><a href="contact.html"{' aria-current="page"' if active=='contact.html' else ''}>Start an enquiry</a></li>
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
      <p class="eyebrow">Project enquiry</p>
      <h2>Send us the drawings. We will tell you what it takes.</h2>
      <p>Share a scope, a drawing set or an information requirement. You will get a
      considered response on approach, disciplines, deliverables and timeline — not a
      generic brochure.</p>
      <div class="cta__actions">
        <a class="btn btn--invert" href="contact.html">Start an enquiry</a>
        <a class="btn btn--invert-ghost" href="capabilities.html">Review capabilities</a>
      </div>
    </div>
    <dl class="cta__side">
      <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Telephone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
      <dt>Enquiry response</dt><dd style="font-family:var(--sans);font-size:14.5px">Within two working days</dd>
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
        <p class="foot__tagline">BIM, MEP and digital engineering delivery for complex building projects.</p>
        <p class="foot__entity">{ENTITY}</p>
        <p class="foot__contact">
          Somnath Baste, Founder<br>
          <a class="foot__link" href="tel:{TEL}">{PHONE}</a><br>
          <a class="foot__link" href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
      <div class="foot__cols">
        <nav class="foot__col" aria-labelledby="f-cap"><h2 id="f-cap">Capabilities</h2><ul>
          <li><a href="capabilities.html#bim-modelling">BIM Modelling</a></li>
          <li><a href="capabilities.html#mep-engineering">MEP Engineering</a></li>
          <li><a href="capabilities.html#coordination">BIM Coordination</a></li>
          <li><a href="capabilities.html#digital">Digital Engineering</a></li>
          <li><a href="capabilities.html#construction">Construction Support</a></li>
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-co"><h2 id="f-co">Company</h2><ul>
          <li><a href="about.html">About</a></li>
          <li><a href="industries.html">Industries</a></li>
          <li><a href="projects.html">Projects</a></li>
          <li><a href="technology.html">Technology</a></li>
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-del"><h2 id="f-del">Delivery</h2><ul>
          <li><a href="technology.html#standards">Standards</a></li>
          <li><a href="technology.html#methodology">Methodology</a></li>
          <li><a href="technology.html#quality">Quality assurance</a></li>
          <li><a href="about.html#global">Global delivery</a></li>
        </ul></nav>
        <nav class="foot__col" aria-labelledby="f-leg"><h2 id="f-leg">Legal</h2><ul>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="terms.html">Terms of Use</a></li>
          <li><a href="cookies.html">Cookie Policy</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul></nav>
      </div>
    </div>
    <div class="foot__rule" aria-hidden="true"></div>
    <div class="foot__bottom">
      <p>© 2026 {ENTITY.title().replace('Pvt Ltd','Pvt Ltd')}. All rights reserved.</p>
      <p class="foot__meta">Review · Automate · Coordinate · Engineer</p>
    </div>
  </div>
</footer>

<script src="config.js"></script>
<script src="script.js" defer></script>
<script src="lead-capture.js" defer></script>
</body>
</html>
"""


def page(slug, title, desc, body, active, cta=True, extra=""):
    html = head(title, desc, slug, extra) + chrome(active) + '\n<main id="main">\n' + body \
        + '\n</main>\n' + (CTA if cta else "") + footer()
    (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
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
             "item": f"{SITE}/{u}" if u else None}
            for i, (n, u) in enumerate(items)]
    }) + '</script>')


# ============================================================== page bodies ==

HOME = """
<section class="hero">
  <div class="hero__grid" aria-hidden="true"></div>
  <div class="shell hero__in">
    <div class="hero__copy">
      <p class="eyebrow">BIM · MEP · Digital Engineering</p>
      <h1 class="hero__title">Digital engineering for complex building projects.</h1>
      <p class="hero__lede">BIMRACE delivers BIM modelling, MEP engineering and multidisciplinary
      coordination for architects, engineers and contractors — structured around ISO 19650
      information management and delivered remotely to project teams anywhere.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="contact.html">Start an enquiry</a>
        <a class="btn btn--ghost" href="capabilities.html">View capabilities</a>
      </div>
      <dl class="hero__facts">
        <div><dt>Disciplines</dt><dd>Architectural · Structural · Mechanical · Electrical · Plumbing</dd></div>
        <div><dt>Information standard</dt><dd>Structured to ISO 19650 principles</dd></div>
        <div><dt>Delivery model</dt><dd>India-based studio, remote international delivery</dd></div>
      </dl>
    </div>

    <figure class="viz" id="hero-viz" style="margin:0">
      <div class="viz__frame">
        <div class="viz__head">
          <span>MODEL / BR-ISO-001</span>
          <span class="viz__live"><i></i>Illustrative preview</span>
        </div>
        <svg class="viz__svg" id="hero-svg" viewBox="0 0 620 560" role="img"
          aria-label="Isometric wireframe of a five-storey building model showing floor plates, columns and colour-coded mechanical, electrical and plumbing runs.">
        </svg>
        <div class="viz__hud">
          <div class="hud__cell"><span class="hud__k">Levels</span><span class="hud__v" data-count="5">0</span></div>
          <div class="hud__cell"><span class="hud__k">Disciplines</span><span class="hud__v" data-count="5">0</span></div>
          <div class="hud__cell"><span class="hud__k">Systems</span><span class="hud__v" data-count="18">0</span></div>
          <div class="hud__cell"><span class="hud__k">Runs</span><span class="hud__v" data-count="312">0</span></div>
        </div>
      </div>
      <figcaption class="viz__cap">Sample geometry shown for illustration. Not a client project model.</figcaption>
    </figure>
  </div>
</section>

<section class="section" id="capabilities">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Core expertise</p>
      <h2 class="sec-title">Five delivery capabilities — and the layer we are building on top</h2>
      <p class="sec-lede">The first five are services you can appoint today, defined by discipline
      and deliverable rather than by software. The sixth is an internal platform still in
      development, included here because it shapes how we model.</p>
    </header>
    <div class="pillars">
      <article class="pillar">
        <p class="pillar__n">01</p><h3>BIM Modelling &amp; Documentation</h3>
        <p>Discipline models built to an agreed level of information need, with the drawing and
        schedule output taken from the model rather than drawn separately.</p>
        <ul><li>Architectural, structural and MEP models</li><li>Drawing production and schedules</li>
        <li>Model setup, templates and naming</li><li>Family and content creation</li></ul>
        <a class="pillar__more" href="capabilities.html#bim-modelling">Scope detail</a>
      </article>
      <article class="pillar">
        <p class="pillar__n">02</p><h3>MEP Engineering</h3>
        <p>Building services modelled as connected systems — sized, routed and checked against
        the spatial and performance constraints they have to meet.</p>
        <ul><li>HVAC and ductwork</li><li>Electrical and containment</li>
        <li>Public health and plumbing</li><li>Fire protection</li></ul>
        <a class="pillar__more" href="capabilities.html#mep-engineering">Scope detail</a>
      </article>
      <article class="pillar">
        <p class="pillar__n">03</p><h3>BIM Coordination</h3>
        <p>Federated models, clash resolution tracked to closure, and coordination output an
        engineer can act on rather than a raw clash count.</p>
        <ul><li>Federated model assembly</li><li>Clash detection and resolution</li>
        <li>Coordination reports and trackers</li><li>Services zoning and clearances</li></ul>
        <a class="pillar__more" href="capabilities.html#coordination">Scope detail</a>
      </article>
      <article class="pillar">
        <p class="pillar__n">04</p><h3>Digital Engineering</h3>
        <p>Automation applied to the repetitive parts of model production, and model data
        managed as a deliverable in its own right.</p>
        <ul><li>Parametric and computational workflows</li><li>Model data and parameter management</li>
        <li>Automated checking routines</li><li>Digital delivery and CDE structure</li></ul>
        <a class="pillar__more" href="capabilities.html#digital">Scope detail</a>
      </article>
      <article class="pillar">
        <p class="pillar__n">05</p><h3>Construction Support</h3>
        <p>Model-derived output for the site team, produced to the tolerance and detail level
        that installation actually requires.</p>
        <ul><li>Shop and fabrication drawings</li><li>Builders work and penetrations</li>
        <li>As-built and record models</li><li>Quantity take-off</li></ul>
        <a class="pillar__more" href="capabilities.html#construction">Scope detail</a>
      </article>
      <article class="pillar">
        <p class="pillar__n">06</p><h3>Engineering Intelligence</h3>
        <p>An intelligence layer being developed in-house to read model information and support
        review, checking and reporting. In development — not a released product.</p>
        <ul><li>Model information extraction</li><li>Automated rule checking</li>
        <li>Engineering analytics</li><li>Natural-language model queries</li></ul>
        <a class="pillar__more" href="technology.html">How we are building it</a>
      </article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell split">
    <div>
      <p class="eyebrow">Engineering intelligence</p>
      <h2 class="sec-title">Information is not the same as intelligence</h2>
      <p class="sec-lede">A model already holds almost everything a project team needs to know.
      The difficulty is that it holds it passively — stored, opened and interpreted by hand.</p>
      <p class="lede" style="margin-top:22px">BIMRACE works information-first. Models are built
      so the data inside them can be queried, checked and reported on, not just looked at. The
      same discipline that makes a model useful to a coordinator is what makes it useful to an
      automated check later.</p>
      <p class="lede" style="margin-top:16px">We are developing that checking layer ourselves.
      It is described honestly on the technology page as work in progress, because it is.</p>
      <a class="btn btn--ghost" style="margin-top:32px" href="technology.html">Technology and standards</a>
    </div>
    <div>
      <svg class="dia" id="ai-svg" viewBox="0 0 900 620" role="img"
        aria-label="Network diagram: a central intelligence layer linked to the architectural model, structural model, mechanical, electrical, plumbing, equipment, spaces and systems."></svg>
    </div>
  </div>
</section>

<section class="section" id="methodology">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Delivery methodology</p>
      <h2 class="sec-title">A defined route from requirement to deliverable</h2>
      <p class="sec-lede">The sequence follows ISO 19650 information management: requirements
      are agreed before modelling starts, and every deliverable is checked against them before
      it is issued.</p>
    </header>
    <ol class="process" id="process">
      <li class="pstep"><p class="pstep__n">01</p><h3>Define</h3>
        <p>Confirm information requirements, scope, disciplines and level of information need.</p></li>
      <li class="pstep"><p class="pstep__n">02</p><h3>Plan</h3>
        <p>Execution plan, model structure, naming, shared coordinates and delivery programme.</p></li>
      <li class="pstep"><p class="pstep__n">03</p><h3>Model</h3>
        <p>Discipline authoring to the agreed standard, with data populated as the model is built.</p></li>
      <li class="pstep"><p class="pstep__n">04</p><h3>Coordinate</h3>
        <p>Federate, resolve clashes and record decisions against a tracked issue list.</p></li>
      <li class="pstep"><p class="pstep__n">05</p><h3>Validate</h3>
        <p>Model and data checks against the plan before anything is issued for use.</p></li>
      <li class="pstep"><p class="pstep__n">06</p><h3>Deliver</h3>
        <p>Issue through the common data environment with the agreed formats and status codes.</p></li>
    </ol>
  </div>
</section>

<section class="section section--tint" id="industries">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Sectors</p>
      <h2 class="sec-title">Building types we are equipped to model</h2>
      <p class="sec-lede">Services density, coordination difficulty and documentation depth vary
      considerably by sector. These are the building types our discipline mix suits.</p>
    </header>
    <div class="inds">
      <article class="ind"><p class="ind__n">01</p><h3>Commercial &amp; offices</h3><p>Fit-out and core-and-shell coordination, ceiling void congestion, tenant variation.</p></article>
      <article class="ind"><p class="ind__n">02</p><h3>Residential &amp; mixed use</h3><p>Repeatable unit typologies, riser coordination and high documentation volume.</p></article>
      <article class="ind"><p class="ind__n">03</p><h3>Healthcare</h3><p>Dense services, strict clearance and access requirements, demanding validation.</p></article>
      <article class="ind"><p class="ind__n">04</p><h3>Data centres</h3><p>High-density mechanical and electrical distribution with tight tolerance coordination.</p></article>
      <article class="ind"><p class="ind__n">05</p><h3>Industrial &amp; warehousing</h3><p>Long-span structures, process services and fire protection routing.</p></article>
      <article class="ind"><p class="ind__n">06</p><h3>Hospitality</h3><p>Back-of-house services, guest-room repetition and finish-critical coordination.</p></article>
      <article class="ind"><p class="ind__n">07</p><h3>Education</h3><p>Phased delivery, standardised room types and ventilation-led services.</p></article>
      <article class="ind"><p class="ind__n">08</p><h3>Retail</h3><p>Landlord and tenant interfaces, rapid fit-out programmes, shopfront coordination.</p></article>
    </div>
    <p class="tiny" style="margin-top:26px">Sector capability reflects the disciplines and
    workflows BIMRACE operates. Project references are being published as they are released
    for publication by clients.</p>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Why BIMRACE</p>
      <h2 class="sec-title">What actually differs</h2>
      <p class="sec-lede">Stated as things you can check rather than adjectives.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">01<b>Information-first modelling</b></div>
        <div class="spec__v">Models are structured so their data is queryable from the outset — parameters
        populated during authoring, not retro-fitted before handover. That is what makes automated
        checking and reliable schedules possible later.</div></div>
      <div class="spec__row"><div class="spec__k">02<b>MEP depth, not MEP as an add-on</b></div>
        <div class="spec__v">Building services are the centre of the practice rather than a discipline bolted
        onto architectural modelling. Mechanical, electrical, public health and fire protection are
        treated as connected systems with real spatial constraints.</div></div>
      <div class="spec__row"><div class="spec__k">03<b>Standards-aligned by default</b></div>
        <div class="spec__v">Naming, status codes, federation strategy and delivery are structured to
        ISO 19650 principles on every appointment, not only where a client mandates it.</div></div>
      <div class="spec__row"><div class="spec__k">04<b>Founder-led accountability</b></div>
        <div class="spec__v">BIMRACE is a focused practice. The person answering your technical questions
        is involved in the delivery, which shortens the distance between a query and a decision.</div></div>
      <div class="spec__row"><div class="spec__k">05<b>Automation applied where it pays</b></div>
        <div class="spec__v">Repetitive model production, checking and reporting are automated in-house.
        The benefit shows up as consistency and turnaround rather than as a marketing claim.</div></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell split">
    <div>
      <p class="eyebrow">Global delivery</p>
      <h2 class="sec-title">Built to work with international project teams</h2>
      <p class="sec-lede">BIMRACE operates from India and delivers remotely. Working practices are
      set up for distributed teams rather than adapted to them.</p>
    </div>
    <div>
      <div class="spec" style="border-top-color:var(--line)">
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Time zones<b style="font-size:15px">Overlap with EMEA and APAC working hours</b></div>
          <div class="spec__v small">IST sits within a workable overlap of European and Asia-Pacific hours,
          with an established handover window for North American teams.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Collaboration<b style="font-size:15px">Client CDE or ours</b></div>
          <div class="spec__v small">We work inside the appointing party's common data environment where one
          exists, and provide a structured environment where one does not.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr;border-bottom:0"><div class="spec__k">Language<b style="font-size:15px">English-language delivery</b></div>
          <div class="spec__v small">Documentation, model data and correspondence in English, to the
          conventions of the appointing party's region.</div></div>
      </div>
      <p class="tiny" style="margin-top:20px">BIMRACE operates as a single India-based studio.
      We do not claim overseas offices.</p>
    </div>
  </div>
</section>
"""

CAPABILITIES = """
<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Service architecture</p>
      <h2 class="sec-title">Scope defined by deliverable, not by software</h2>
      <p class="sec-lede">Each capability below lists what is actually produced and issued. Any
      of them can be appointed independently, or combined into one information delivery package
      under a single point of accountability.</p>
    </header>

    <div class="spec" id="bim-modelling">
      <div class="spec__row"><div class="spec__k">Capability 01<b>BIM Modelling &amp; Documentation</b></div>
        <div class="spec__v">Discipline models authored to an agreed level of information need, with
        drawings and schedules derived from the model rather than drafted separately. Model setup,
        templates, shared coordinates and naming conventions are established before authoring starts.
        <ul class="spec__list">
          <li>Architectural modelling</li><li>Structural modelling</li>
          <li>MEP modelling</li><li>General arrangement drawings</li>
          <li>Sections, elevations and details</li><li>Door, room and equipment schedules</li>
          <li>Family and content creation</li><li>Model templates and standards setup</li>
        </ul></div></div>

      <div class="spec__row" id="mep-engineering"><div class="spec__k">Capability 02<b>MEP Engineering</b></div>
        <div class="spec__v">Building services modelled as connected systems, routed against the spatial
        and access constraints they must satisfy. Sizing and performance data are held on the elements
        so the model can be interrogated rather than only viewed.
        <ul class="spec__list">
          <li>HVAC and ductwork distribution</li><li>Plant room layouts</li>
          <li>Electrical distribution and containment</li><li>Lighting and small power</li>
          <li>Public health and drainage</li><li>Domestic water services</li>
          <li>Fire protection and sprinklers</li><li>Equipment schedules and data</li>
        </ul></div></div>

      <div class="spec__row" id="coordination"><div class="spec__k">Capability 03<b>BIM Coordination</b></div>
        <div class="spec__v">Federated models assembled from all contributing disciplines, with clashes
        tracked to closure and each decision recorded. Output is a resolved model and an auditable
        issue history, not a raw clash count.
        <ul class="spec__list">
          <li>Federated model assembly</li><li>Clash detection and rule sets</li>
          <li>Clash resolution and re-testing</li><li>Coordination issue tracking</li>
          <li>Services zoning strategy</li><li>Clearance and maintenance access checks</li>
          <li>Coordination reports</li><li>Coordination workshop support</li>
        </ul></div></div>

      <div class="spec__row" id="digital"><div class="spec__k">Capability 04<b>Digital Engineering</b></div>
        <div class="spec__v">Automation applied to repetitive production and checking, and model data
        managed as a deliverable in its own right. Used where it measurably improves consistency or
        turnaround, not applied for its own sake.
        <ul class="spec__list">
          <li>Parametric and computational workflows</li><li>Automated model checking routines</li>
          <li>Parameter and data management</li><li>Model auditing and health checks</li>
          <li>Data export and reporting</li><li>Common data environment structure</li>
          <li>Naming and classification automation</li><li>Digital delivery packaging</li>
        </ul></div></div>

      <div class="spec__row" id="construction"><div class="spec__k">Capability 05<b>Construction Support</b></div>
        <div class="spec__v">Model-derived output produced for the people installing the work, at the
        detail and tolerance installation actually requires.
        <ul class="spec__list">
          <li>Shop and fabrication drawings</li><li>Spool and prefabrication drawings</li>
          <li>Builders work and penetration drawings</li><li>Bracket and support layouts</li>
          <li>As-built and record models</li><li>Quantity take-off and schedules</li>
          <li>Site query support</li><li>Handover information packaging</li>
        </ul></div></div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Appointment models</p>
      <h2 class="sec-title">How engagements are usually structured</h2>
    </header>
    <div class="g3">
      <article class="std"><p class="std__k">A</p><h3>Package delivery</h3>
        <p>A defined scope with fixed deliverables, a level of information need and an agreed issue
        programme. Suits discrete stages and clearly bounded packages.</p></article>
      <article class="std"><p class="std__k">B</p><h3>Team extension</h3>
        <p>Allocated resource working inside your standards, templates and CDE as an extension of your
        own team, reporting into your information manager.</p></article>
      <article class="std"><p class="std__k">C</p><h3>Coordination appointment</h3>
        <p>Federation, clash resolution and coordination reporting across models authored by others,
        with a tracked issue register and workshop support.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Software</p>
      <h2 class="sec-title">Tooling</h2>
      <p class="sec-lede">Deliverables are defined by the information required, not by a
      particular application. Where a project mandates a toolchain, we work in it.</p>
    </header>
    <div class="g4">
      <div><p class="eyebrow eyebrow--mute">Authoring</p><p class="small">Revit · AutoCAD · discipline-specific MEP authoring tools</p></div>
      <div><p class="eyebrow eyebrow--mute">Coordination</p><p class="small">Navisworks · federated model review and clash workflows</p></div>
      <div><p class="eyebrow eyebrow--mute">Automation</p><p class="small">Dynamo · scripted routines · custom checking tools</p></div>
      <div><p class="eyebrow eyebrow--mute">Exchange</p><p class="small">IFC · COBie-style data exports · common data environments</p></div>
    </div>
    <p class="tiny" style="margin-top:28px">Software names are the property of their respective
    owners and are listed to describe working practice. No partnership or certification is implied.</p>
  </div>
</section>
"""

INDUSTRIES = """
<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Sector capability</p>
      <h2 class="sec-title">Where coordination difficulty actually sits</h2>
      <p class="sec-lede">Sectors differ less in the software used than in services density,
      clearance tolerance, documentation volume and how much validation the client requires.
      These are the building types our discipline mix is set up for.</p>
    </header>
    <div class="g2">
      <article><h3 style="font-size:20px">Commercial &amp; offices</h3>
        <p class="small" style="margin-top:12px">Core-and-shell and fit-out coordination, with congested
        ceiling voids and tenant variation driving repeated re-coordination. Documentation volume is
        high and change is continuous, so model structure and naming discipline matter more than
        modelling speed.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> MEP modelling,
        federated coordination, builders work, shop drawings.</p></article>
      <article><h3 style="font-size:20px">Residential &amp; mixed use</h3>
        <p class="small" style="margin-top:12px">Repeatable unit typologies reward parametric and
        automated production, while riser coordination and vertical service continuity are where most
        issues concentrate. Schedule accuracy across many repeated rooms is the usual test.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> unit type modelling,
        riser coordination, quantity take-off, drawing production.</p></article>
      <article><h3 style="font-size:20px">Healthcare</h3>
        <p class="small" style="margin-top:12px">Among the most services-dense building types, with strict
        clearance, access and maintainability requirements. Validation expectations are correspondingly
        high, and coordination has to account for equipment that arrives late in the design.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> MEP modelling, clearance
        and access validation, coordination reporting, as-built models.</p></article>
      <article><h3 style="font-size:20px">Data centres</h3>
        <p class="small" style="margin-top:12px">Very high-density mechanical and electrical distribution
        with tight tolerances and heavy repetition. Containment routing, cable tray coordination and
        plant access dominate, and model data accuracy carries straight into procurement.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> electrical containment,
        mechanical distribution, clash resolution, take-off.</p></article>
      <article><h3 style="font-size:20px">Industrial &amp; warehousing</h3>
        <p class="small" style="margin-top:12px">Long-span structures with process services, high-level
        distribution and fire protection routing. Coordination is less congested than healthcare but
        spans large areas, so federation strategy and model performance matter.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> services routing, fire
        protection, structural coordination, penetration drawings.</p></article>
      <article><h3 style="font-size:20px">Hospitality</h3>
        <p class="small" style="margin-top:12px">Guest-room repetition alongside complex back-of-house
        services. Finishes are unforgiving, so services have to be coordinated to the ceiling and wall
        build-ups rather than to structure alone.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> room type modelling,
        back-of-house MEP, ceiling coordination, shop drawings.</p></article>
      <article><h3 style="font-size:20px">Education</h3>
        <p class="small" style="margin-top:12px">Standardised room types, phased delivery and
        ventilation-led services. Programmes are frequently constrained by occupation dates, which
        places weight on predictable issue schedules.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> MEP modelling, phased
        coordination, documentation, take-off.</p></article>
      <article><h3 style="font-size:20px">Retail</h3>
        <p class="small" style="margin-top:12px">Landlord and tenant interfaces with short fit-out
        programmes. The coordination question is usually about demarcation and capacity at the
        interface rather than about the tenant area itself.</p>
        <p class="small" style="margin-top:12px"><strong>Typical scope:</strong> fit-out MEP,
        interface coordination, as-built records.</p></article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell">
    <header class="sec-head"><p class="eyebrow">Note on sector claims</p>
      <h2 class="sec-title">What this page does and does not say</h2></header>
    <div class="g2">
      <p class="lede">The sectors above describe the building types BIMRACE's disciplines and
      workflows are equipped to serve, and the coordination characteristics each one presents.
      They are a statement of capability.</p>
      <p class="lede">They are not a claim of completed projects in every sector. Published
      project evidence is on the <a href="projects.html" style="color:var(--text);text-decoration:underline;text-underline-offset:3px">projects</a>
      page, and will grow as clients release work for publication.</p>
    </div>
  </div>
</section>
"""

PROJECTS = """
<section class="section section--flush">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Project evidence</p>
      <h2 class="sec-title">Published case studies</h2>
      <p class="sec-lede">Project work is published here once the client has released it. Rather
      than fill this page with stock imagery, the case study structure is set out below so you
      can see exactly what each published project will document.</p>
    </header>

    <div class="pcards">
      <article class="slot">
        <p class="slot__k">Slot 01 — awaiting release</p>
        <h3>Case study position one</h3>
        <p>Reserved for the first project released for publication. The template below shows the
        information each entry will carry.</p>
      </article>
      <article class="slot">
        <p class="slot__k">Slot 02 — awaiting release</p>
        <h3>Case study position two</h3>
        <p>Reserved. Client-identifying detail is only published with written permission; anonymised
        entries are used where a name cannot be released.</p>
      </article>
      <article class="slot">
        <p class="slot__k">Slot 03 — awaiting release</p>
        <h3>Case study position three</h3>
        <p>Reserved. Where a project cannot be published at all, its characteristics can still be
        discussed under NDA during an enquiry.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Case study template</p>
      <h2 class="sec-title">What every published project will document</h2>
      <p class="sec-lede">A fixed structure, so projects can be compared like for like rather than
      presented as a gallery.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Section 01<b>Project overview</b></div>
        <div class="spec__v">Client type, sector, location, project scale and stage at appointment.
        Named only where the client has agreed to be named.</div></div>
      <div class="spec__row"><div class="spec__k">Section 02<b>Scope and disciplines</b></div>
        <div class="spec__v">BIM scope, disciplines modelled, level of information need, and the
        specific deliverables issued.</div></div>
      <div class="spec__row"><div class="spec__k">Section 03<b>Challenge</b></div>
        <div class="spec__v">The engineering or information problem the appointment existed to solve,
        stated concretely rather than as a generic difficulty.</div></div>
      <div class="spec__row"><div class="spec__k">Section 04<b>Engineering approach</b></div>
        <div class="spec__v">Model structure, federation strategy, coordination method and any
        automation applied, with the reasoning behind each decision.</div></div>
      <div class="spec__row"><div class="spec__k">Section 05<b>Coordination record</b></div>
        <div class="spec__v">How clashes were tracked and closed, how decisions were recorded, and
        how the model was validated before issue.</div></div>
      <div class="spec__row"><div class="spec__k">Section 06<b>Deliverables issued</b></div>
        <div class="spec__v">The actual list of models, drawings, schedules and data issued, with
        formats and status codes.</div></div>
      <div class="spec__row"><div class="spec__k">Section 07<b>Outcome</b></div>
        <div class="spec__v">What changed as a result. Quantified only where the figure is measured
        and the client has agreed to its publication.</div></div>
      <div class="spec__row"><div class="spec__k">Section 08<b>Visual evidence</b></div>
        <div class="spec__v">Model views, coordination screenshots or drawing extracts, redacted where
        commercially necessary.</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split">
    <div>
      <p class="eyebrow">Why this page is honest</p>
      <h2 class="sec-title">No invented projects</h2>
      <p class="sec-lede">It is common for websites in this sector to show unattributed renders and
      implied project counts. We would rather show a rigorous template and fill it with real work.</p>
      <p class="lede" style="margin-top:20px">If you are evaluating BIMRACE for an appointment and
      need to assess capability now, ask. We can walk through modelling standards, coordination
      method and sample deliverables directly, under NDA where required.</p>
      <a class="btn btn--primary" style="margin-top:30px" href="contact.html">Request a capability walkthrough</a>
    </div>
    <div>
      <div class="std"><p class="std__k">For the site owner</p>
        <h3>Adding a case study</h3>
        <p>Copy <code>project-template.html</code>, complete the eight sections above, replace a slot
        card on this page with a <code>.pcard</code> linking to it, and add the URL to
        <code>sitemap.xml</code>. Full instructions are in <code>README.md</code>.</p></div>
    </div>
  </div>
</section>
"""

TECHNOLOGY = """
<section class="section section--flush" id="standards">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Information standards</p>
      <h2 class="sec-title">Structured to ISO 19650</h2>
      <p class="sec-lede">ISO 19650 is the international standard series for managing information
      using BIM across the life cycle of built assets. BIMRACE structures delivery around its
      principles by default.</p>
    </header>
    <div class="stds">
      <article class="std"><p class="std__k">Part 1</p><h3>Concepts and principles</h3>
        <p>Defines the core terms, roles and the information delivery cycle, including expectations
        for a common data environment, status codes and approval.</p></article>
      <article class="std"><p class="std__k">Part 2</p><h3>Delivery phase</h3>
        <p>The part most referenced in day-to-day practice. Covers information management during
        design and construction, and the artefacts that govern it.</p></article>
      <article class="std"><p class="std__k">Part 3</p><h3>Operational phase</h3>
        <p>Information management during operation and maintenance, and the transition from a project
        information model to an asset information model.</p></article>
      <article class="std"><p class="std__k">Part 4</p><h3>Information exchange</h3>
        <p>Process and decision criteria for individual information exchanges, including quality
        criteria for what is handed over.</p></article>
      <article class="std"><p class="std__k">Part 5</p><h3>Security-minded management</h3>
        <p>Applies where the sensitivity of the information requires protection — relevant to
        government, defence and critical infrastructure assets.</p></article>
      <article class="std"><p class="std__k">Part 6</p><h3>Health and safety information</h3>
        <p>The most recent addition to the series, covering the structuring of health and safety
        information.</p></article>
    </div>
    <div class="note" style="max-width:none">
      <p><strong>On certification.</strong> BIMRACE structures its delivery to align with ISO 19650
      principles. This is a statement of working method, not a claim of third-party certification
      to the standard. Where a project requires certified parties, we will say so at enquiry stage.</p>
    </div>
  </div>
</section>

<section class="section section--tint" id="methodology">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Working artefacts</p>
      <h2 class="sec-title">The documents that govern an appointment</h2>
      <p class="sec-lede">These are the instruments that make information delivery auditable. They
      are agreed before authoring begins.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">EIR<b>Exchange Information Requirements</b></div>
        <div class="spec__v">What the appointing party needs, when, in what format and to what level of
        information need. Everything downstream is measured against this.</div></div>
      <div class="spec__row"><div class="spec__k">BEP<b>BIM Execution Plan</b></div>
        <div class="spec__v">How the delivery team will meet those requirements — model structure,
        federation strategy, naming, coordinates, software and responsibilities.</div></div>
      <div class="spec__row"><div class="spec__k">MIDP / TIDP<b>Information delivery plans</b></div>
        <div class="spec__v">The master and task-level schedules that say who issues which container,
        at which milestone, in which state.</div></div>
      <div class="spec__row"><div class="spec__k">CDE<b>Common Data Environment</b></div>
        <div class="spec__v">The single source for project information, with status codes controlling
        whether a container is work in progress, shared, published or archived.</div></div>
      <div class="spec__row"><div class="spec__k">LOIN<b>Level of Information Need</b></div>
        <div class="spec__v">Defines what "complete" means for an object at a given milestone —
        geometry, alphanumeric data and documentation. It is the successor to inconsistent LOD usage
        and removes most of the ambiguity that caused.</div></div>
    </div>
  </div>
</section>

<section class="section" id="quality">
  <div class="shell">
    <header class="sec-head">
      <p class="eyebrow">Quality assurance</p>
      <h2 class="sec-title">What gets checked before anything is issued</h2>
    </header>
    <div class="g3">
      <article class="std"><p class="std__k">01</p><h3>Model health</h3>
        <p>File size and performance, warnings, unplaced and duplicated elements, worksets, links and
        shared coordinate integrity.</p></article>
      <article class="std"><p class="std__k">02</p><h3>Standards compliance</h3>
        <p>Naming, classification, view and sheet organisation, parameter completeness against the
        agreed level of information need.</p></article>
      <article class="std"><p class="std__k">03</p><h3>Geometric accuracy</h3>
        <p>Origin and orientation, level and grid alignment, discipline model alignment, tolerance
        against the coordination datum.</p></article>
      <article class="std"><p class="std__k">04</p><h3>Data completeness</h3>
        <p>Required parameters populated, schedules reconciling, exported data validating against the
        exchange requirement.</p></article>
      <article class="std"><p class="std__k">05</p><h3>Coordination status</h3>
        <p>Open clashes reviewed, resolutions re-tested, decisions recorded against a tracked issue
        list with an owner.</p></article>
      <article class="std"><p class="std__k">06</p><h3>Issue readiness</h3>
        <p>Correct status code and revision, correct formats, deliverable list reconciled against the
        delivery plan before upload.</p></article>
    </div>
  </div>
</section>

<section class="section section--tint" id="intelligence">
  <div class="shell split">
    <div>
      <p class="eyebrow">In development</p>
      <h2 class="sec-title">The intelligence layer we are building</h2>
      <p class="sec-lede">Alongside delivery work, BIMRACE is developing an internal platform that
      reads model information and assists with review, checking and reporting.</p>
      <p class="lede" style="margin-top:20px">It is described here as work in progress because that
      is what it is. It is not a released product, it is not available for licence, and nothing on
      this site should be read as a commitment to a feature or a date.</p>
      <p class="lede" style="margin-top:16px">The reason it exists is the same reason we model
      information-first: once a model's data is structured and reliable, a large share of routine
      checking stops needing a person to do it by hand.</p>
    </div>
    <div>
      <div class="spec" style="border-top-color:var(--line)">
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Being built to<b style="font-size:15px">Extract model information</b></div>
          <div class="spec__v small">Read elements, parameters, systems and relationships from the model as structured data.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Being built to<b style="font-size:15px">Run rule-based checks</b></div>
          <div class="spec__v small">Validate a model against project rules, standards and internal practice automatically.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Being built to<b style="font-size:15px">Report engineering analytics</b></div>
          <div class="spec__v small">Turn model data into quantities, distributions and system behaviour.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr;border-bottom:0"><div class="spec__k">Future capability<b style="font-size:15px">Natural-language model queries</b></div>
          <div class="spec__v small">Ask questions of BIM and engineering data in plain English.</div></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide" style="margin-bottom:32px">
      <p class="eyebrow">Platform architecture</p>
      <h2 class="sec-title">One intelligence layer over the delivery stack</h2>
    </header>
    <svg class="dia" id="platform-svg" viewBox="0 0 900 460" role="img"
      aria-label="Architecture diagram: an intelligence layer connected to BIM models, MEP systems, engineering data, an AI engine, automation, coordination and analytics."></svg>
  </div>
</section>
"""

ABOUT = """
<section class="section section--flush">
  <div class="shell split">
    <div>
      <p class="eyebrow">The practice</p>
      <h2 class="sec-title">A focused engineering practice, not a volume drafting shop</h2>
      <p class="sec-lede">BIMRACE was established to do one thing well: produce building information
      that is accurate enough to be relied on, and structured enough to be used by something other
      than a human reading a drawing.</p>
      <p class="lede" style="margin-top:20px">That focus shapes how the practice operates. Scope is
      agreed against an information requirement rather than a page count. Models are built so their
      data holds up under interrogation. Coordination output is a resolved model and a decision
      record, not a clash report thrown over a wall.</p>
      <p class="lede" style="margin-top:16px">It also shapes what we decline. Work that only wants
      geometry produced quickly, with no interest in the information inside it, is not what this
      practice is set up for.</p>
    </div>
    <div>
      <div class="spec" style="border-top-color:var(--line)">
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Legal entity<b style="font-size:15px">BIMRACE PVT LTD</b></div>
          <div class="spec__v small">Registered in India. Registered office and company identification
          number available on request and published here once confirmed.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Base<b style="font-size:15px">India</b></div>
          <div class="spec__v small">Single studio. We do not operate or claim overseas offices.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr"><div class="spec__k">Disciplines<b style="font-size:15px">Architectural · Structural · MEP</b></div>
          <div class="spec__v small">With building services as the centre of the practice.</div></div>
        <div class="spec__row" style="grid-template-columns:1fr;border-bottom:0"><div class="spec__k">Status<b style="font-size:15px">Actively taking appointments</b></div>
          <div class="spec__v small">Internal platform development runs alongside delivery work.</div></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint" id="founder">
  <div class="shell">
    <header class="sec-head"><p class="eyebrow">Leadership</p>
      <h2 class="sec-title">Founder</h2></header>
    <div class="split" style="align-items:center">
      <div>
        <h3 style="font-size:26px">Somnath Baste</h3>
        <p class="eyebrow" style="margin-top:8px;margin-bottom:0">Founder — BIMRACE</p>
        <p class="lede" style="margin-top:22px">“Building BIMRACE around a simple idea: engineering
        data should not only be stored in models — it should become intelligent, useful and
        actionable.”</p>
        <p class="small" style="margin-top:22px">Enquiries about scope, standards or delivery
        method reach the founder directly.</p>
        <p style="margin-top:20px;display:flex;flex-wrap:wrap;gap:14px 28px">
          <a class="foot__link" href="tel:+917507958364">+91 75079 58364</a>
          <a class="foot__link" href="mailto:info@bimrace.com">info@bimrace.com</a>
        </p>
      </div>
      <div>
        <figure style="margin:0;max-width:300px">
          <div class="founder__frame" style="position:relative;aspect-ratio:4/5;border:1px solid var(--line-strong);background:var(--surface-2);overflow:hidden">
            <span class="founder__fallback" aria-hidden="true"
              style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:34px;color:var(--text-mute)">SB</span>
            <img class="founder__photo"
              src="https://rhksfmwmqiwzwsiiuhng.supabase.co/storage/v1/object/public/somnathprofilepic/SAM.jpg"
              alt="Portrait of Somnath Baste, Founder of BIMRACE"
              width="800" height="1000" loading="lazy" decoding="async"
              style="position:relative;z-index:1;display:block;width:100%;height:100%;object-fit:cover;object-position:center 22%;filter:grayscale(1) contrast(1.04)">
          </div>
          <figcaption style="display:flex;justify-content:space-between;margin-top:10px;padding-top:9px;border-top:1px solid var(--line);font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--text-mute)">
            <span>Somnath Baste</span><span>Founder</span>
          </figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<section class="section" id="global">
  <div class="shell">
    <header class="sec-head"><p class="eyebrow">Global delivery</p>
      <h2 class="sec-title">How remote appointments actually run</h2></header>
    <div class="g3">
      <article class="std"><p class="std__k">01</p><h3>Inside your environment</h3>
        <p>We work in the appointing party's common data environment, templates and standards where
        they exist, and provide a structured environment where they do not.</p></article>
      <article class="std"><p class="std__k">02</p><h3>Defined issue rhythm</h3>
        <p>An agreed issue schedule with status codes, so progress is visible without status meetings
        being the only way to find out.</p></article>
      <article class="std"><p class="std__k">03</p><h3>Working-hours overlap</h3>
        <p>IST overlaps European and Asia-Pacific hours directly, with a handover window that suits
        North American teams.</p></article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="shell">
    <header class="sec-head"><p class="eyebrow">Positioning</p>
      <h2 class="sec-title">What we will not claim</h2>
      <p class="sec-lede">A short list, because in this sector the absence of these claims is
      itself informative.</p></header>
    <div class="g2">
      <div><p class="lede">This site publishes no client logos, no project counts, no headcount, no
      revenue figures, no awards and no testimonials — because none of those have been earned and
      verified yet. When they are, they will appear with attribution.</p></div>
      <div><p class="lede">Nor do we claim third-party certification to ISO 19650. We align our
      delivery to its principles, which is a different and checkable statement. If your procurement
      requires certified parties, we will tell you at enquiry stage rather than after appointment.</p></div>
    </div>
  </div>
</section>
"""

CONTACT = f"""
<section class="section section--flush">
  <div class="shell split">
    <div>
      <p class="eyebrow">Project enquiry</p>
      <h2 class="sec-title">Tell us about the project</h2>
      <p class="sec-lede">The more specific the scope, the more useful the response. If you have a
      drawing set, an information requirement or an execution plan, say so and we will ask for it.</p>

      <form class="form" id="enquiry-form" data-lead-form="project_enquiry" novalidate>
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
          <p class="err" data-for="f-email" role="alert"></p></div>

        <div class="field"><label for="f-phone">Telephone</label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel">
          <p class="err" data-for="f-phone" role="alert"></p></div>

        <div class="field"><label for="f-service">Service required</label>
          <select id="f-service" name="lead_type">
            <option value="">Select…</option>
            <option value="bim_modelling">BIM Modelling &amp; Documentation</option>
            <option value="mep_bim">MEP BIM / MEP Engineering</option>
            <option value="bim_coordination">BIM Coordination</option>
            <option value="bim_company_support">BIM Company Support (overflow / white-label)</option>
            <option value="bim_training">Training</option>
            <option value="bim_consulting">BIM Consulting / ISO 19650</option>
            <option value="resource_support">Staff / Resource Support</option>
            <option value="automation">Automation / Custom Workflows</option>
            <option value="general">Something else</option>
          </select></div>

        <div class="field"><label for="f-country">Country</label>
          <input id="f-country" name="country_code" type="text" maxlength="2"
                 placeholder="IN, GB, AE…" style="text-transform:uppercase"></div>

        <div class="field"><label for="f-stage">Project stage</label>
          <select id="f-stage" name="project_stage">
            <option value="">Select…</option>
            <option>Concept / feasibility</option><option>Developed design</option>
            <option>Technical design</option><option>Construction</option>
            <option>Handover / as-built</option>
          </select></div>

        <div class="field"><label for="f-sector">Sector</label>
          <input id="f-sector" name="industry" type="text" placeholder="e.g. healthcare, data centre"></div>

        <div class="field"><label for="f-location">Project location</label>
          <input id="f-location" name="project_location" type="text" placeholder="City, country"></div>

        <div class="field field--full"><label for="f-msg">Scope and requirements <span class="req" aria-hidden="true">*</span></label>
          <textarea id="f-msg" name="message" data-required data-minlen="20" required
            placeholder="Disciplines, deliverables, level of information need, programme, and anything already agreed in an EIR or BEP."></textarea>
          <p class="err" data-for="f-msg" role="alert"></p></div>

        <div class="form__foot">
          <p class="tiny" style="max-width:44ch">By sending this enquiry you agree to our
          <a href="privacy.html" style="color:var(--text)">Privacy Policy</a>. We use these details
          only to respond to your enquiry.</p>
          <button class="btn btn--primary btn--lg" type="submit">Send enquiry</button>
        </div>
        <p class="form-status" data-form-status hidden></p>
      </form>

      <div class="form-success" data-form-success hidden tabindex="-1">
        <p class="eyebrow">Enquiry received</p>
        <h3 style="font-size:22px">Thank you — we have your enquiry.</h3>
        <p class="lede" style="margin-top:12px">It has been logged and routed to the right person.
        We respond within two working days. If it is urgent, call
        <a href="tel:+917507958364" style="color:var(--text)">+91 75079 58364</a>.</p>
      </div>
    </div>

    <aside>
      <div class="std">
        <p class="std__k">Direct</p><h3>Speak to the founder</h3>
        <p>Technical questions about scope, standards or delivery method go straight to Somnath Baste.</p>
        <p style="margin-top:18px;display:flex;flex-direction:column;gap:10px">
          <a class="foot__link" href="mailto:{EMAIL}">{EMAIL}</a>
          <a class="foot__link" href="tel:{TEL}">{PHONE}</a>
        </p>
      </div>
      <div class="std" style="margin-top:24px">
        <p class="std__k">What happens next</p><h3>Response process</h3>
        <p><strong>1.</strong> We acknowledge within two working days.<br>
        <strong>2.</strong> If the scope is clear, you get an approach note covering disciplines,
        deliverables and indicative programme.<br>
        <strong>3.</strong> If it is not yet clear, we ask specific questions rather than send a
        generic proposal.</p>
      </div>
      <div class="std" style="margin-top:24px">
        <p class="std__k">Confidentiality</p><h3>NDAs</h3>
        <p>We sign non-disclosure agreements before receiving drawing sets or project information.
        Ask and we will return a signed copy of yours.</p>
      </div>
    </aside>
  </div>
</section>
"""

THANKYOU = """
<section class="nf">
  <div class="shell">
    <p class="nf__code">ENQUIRY RECEIVED</p>
    <h1>Thank you — your enquiry has been sent.</h1>
    <p>We acknowledge enquiries within two working days. If it is urgent, call
    <a href="tel:+917507958364" style="color:var(--text)">+91 75079 58364</a> directly.</p>
    <div class="nf__links">
      <a class="btn btn--primary" href="index.html">Back to home</a>
      <a class="btn btn--ghost" href="capabilities.html">Review capabilities</a>
    </div>
  </div>
</section>
"""

NOTFOUND = """
<section class="nf">
  <div class="shell">
    <p class="nf__code">ERROR 404</p>
    <h1>That page could not be found.</h1>
    <p>The address may be out of date, or the page may have moved. The main sections of the site
    are below.</p>
    <div class="nf__links">
      <a class="btn btn--primary" href="index.html">Home</a>
      <a class="btn btn--ghost" href="capabilities.html">Capabilities</a>
      <a class="btn btn--ghost" href="projects.html">Projects</a>
      <a class="btn btn--ghost" href="contact.html">Contact</a>
    </div>
  </div>
</section>
"""


# =========================================================== legal pages ====
LEGAL_UPDATED = "1 September 2026"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
CALL = f'<a href="tel:{TEL}">{PHONE}</a>'
P = lambda *t: "\n".join(f"          <p>{x}</p>" for x in t)
def UL(*i): return "          <ul>\n" + "\n".join(f"            <li>{x}</li>" for x in i) + "\n          </ul>"
def NOTE(*t): return '          <div class="note">\n' + "\n".join(f"            <p>{x}</p>" for x in t) + "\n          </div>"
FILL = lambda t: f'<span class="fill">[{t}]</span>'


def legal_body(title, sheet, intro, sections):
    toc = "\n".join(f'          <li><a href="#{i}">{h}</a></li>' for i, h, _ in sections)
    body = "\n\n".join(
        f'      <section id="{i}">\n        <h2>{h}</h2>\n{c}\n      </section>' for i, h, c in sections)
    return f"""<section class="legal">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow eyebrow--mute">{sheet}</p>
      <h1 class="sec-title">{title}</h1>
      {intro}
      <p class="legal__meta">Last updated: {LEGAL_UPDATED} · {ENTITY}</p>
    </header>
    <div class="legal__inner">
      <nav class="legal__toc" id="legal-toc" aria-label="On this page">
        <h2>On this page</h2>
        <ol>
{toc}
        </ol>
      </nav>
      <div class="prose">
{body}
      </div>
    </div>
  </div>
</section>"""


PRIVACY = legal_body("Privacy Policy", "Legal 01 — Privacy",
    P("This policy explains what happens to personal information when you visit the BIMRACE "
      "website or contact us about a project."),
    [
     ("who", "Who we are", P(
        f"BIMRACE is a BIM, MEP and digital engineering practice operated by <strong>{ENTITY}</strong>. "
        f"Our registered office is at {FILL('registered address')} and our company identification "
        f"number is {FILL('CIN')}.",
        f"For any question about this policy, email {MAIL} or call {CALL}.")),
     ("scope", "What this policy covers", P(
        "This policy covers this website and enquiries made through it. It does not cover project "
        "information handled under a separate appointment or non-disclosure agreement, which is "
        "governed by that agreement.",
        "It also does not cover third-party websites you reach from links on this site.")),
     ("collect", "Information we collect", P("We collect two kinds of information.") + "\n" + UL(
        "<strong>Information you give us.</strong> If you submit the enquiry form we receive your name, "
        "company, business email, and any telephone number, service, project stage, sector, location and "
        "message you choose to provide. If you email or call us we hold that correspondence.",
        "<strong>Technical information.</strong> Our hosting provider records standard server logs when a "
        "page is served: IP address, browser and device type, the page requested, and the date and time. "
        "This is ordinary web-server activity used for security and reliability.") + "\n" + P(
        "We do not run advertising trackers, we do not build visitor profiles, and we do not buy "
        "personal data from third parties.")),
     ("use", "How we use information", P("We use this information only to:") + "\n" + UL(
        "respond to and assess project enquiries;",
        "carry out an appointment where one follows;",
        "keep the website available, secure and working correctly;",
        "meet legal and record-keeping obligations that apply to us.") + "\n" + P(
        "We do not use your information for automated decision-making, and we do not sell it.")),
     ("cookies", "Cookies and analytics", P(
        "This site sets no cookies of its own and runs no analytics software. It makes third-party "
        "requests for typefaces, the founder photograph and enquiry form handling, all of which are "
        'set out in our <a href="cookies.html">Cookie Policy</a>.')),
     ("sharing", "Sharing your information", P("We share personal information only where necessary:") + "\n" + UL(
        "with our hosting and form-handling providers, who process data on our instructions;",
        "with professional advisers such as accountants or lawyers, where relevant;",
        "where required by law, regulation or a valid legal request.") + "\n" + P(
        "We do not sell, rent or trade personal information.")),
     ("retention", "How long we keep information", P(
        "Enquiry correspondence is kept for as long as the enquiry is live and for a reasonable period "
        "afterwards — normally no more than 24 months — unless it becomes part of a project record "
        "governed by an appointment. Server logs are kept for a short period set by our hosting provider.")),
     ("security", "Security", P(
        "We take reasonable technical and organisational measures to protect the information we hold, "
        "including restricting access to those who need it. No method of transmission or storage is "
        "completely secure, so we cannot guarantee absolute security. Project information received "
        "under a non-disclosure agreement is handled to the terms of that agreement.")),
     ("rights", "Your rights", P("Depending on where you live, you may have the right to:") + "\n" + UL(
        "ask what personal information we hold about you and get a copy of it;",
        "ask us to correct information that is wrong or incomplete;",
        "ask us to delete information we no longer have a reason to keep;",
        "object to or ask us to restrict certain uses of your information;",
        "withdraw consent where we relied on it, without affecting earlier processing;",
        "complain to your data protection authority.") + "\n" + P(
        f"To exercise any of these, email {MAIL}. We respond within the period required by applicable "
        "law. Visitors in India have rights under the Digital Personal Data Protection Act, 2023; "
        "visitors in the EEA and UK have rights under the GDPR.")),
     ("children", "Children's privacy", P(
        "This website is aimed at construction and engineering professionals. It is not directed at "
        "children and we do not knowingly collect information from them.")),
     ("intl", "International visitors", P(
        "We are based in India and our infrastructure providers may store data in other countries. "
        "Where information is transferred outside your country we take steps to ensure it remains "
        "protected to the standard required by applicable law.")),
     ("changes", "Changes to this policy", P(
        "We update this policy when the way we handle information changes. The date at the top of this "
        "page always shows the current version.")),
     ("contact", "Contact us", P(
        f"{ENTITY}<br>{FILL('registered address')}<br>Email: {MAIL}<br>Telephone: {CALL}") + "\n" + NOTE(
        "<strong>Before you publish:</strong> replace the highlighted placeholders with your registered "
        "company details and have this policy reviewed by a qualified adviser in your jurisdiction.")),
    ])

TERMS = legal_body("Terms of Use", "Legal 02 — Terms",
    P("These terms apply to your use of this website. They do not govern any appointment, which is "
      "covered by a separate written agreement."),
    [
     ("accept", "Acceptance of these terms", P(
        f"This website is operated by <strong>{ENTITY}</strong>. By using the site you accept these "
        "terms. If you do not accept them, please do not use the site.")),
     ("nature", "Nature of the information on this site", P(
        "This site describes services BIMRACE offers and working methods it applies. Capability "
        "descriptions are statements of what the practice is equipped to deliver.",
        "The internal platform described on the technology page is <strong>under development</strong>. "
        "Statements about it describe intent, not released functionality, and are not a commitment to "
        "deliver any feature or to any date.",
        "Nothing on this site is an offer capable of acceptance, a quotation, or a contractual "
        "commitment. Scope, price and programme are agreed in writing for each appointment.")),
     ("advice", "Not engineering advice", P(
        "Content on this site is general information about an engineering service. It is "
        "<strong>not</strong> engineering, design, structural, MEP, safety, regulatory, legal or "
        "financial advice, and must not be relied on as a substitute for the judgement of a qualified "
        "professional engaged on your project.",
        "Any engineering decision remains the responsibility of the competent professional making it. "
        "Models, drawings and system designs must be checked and approved by appropriately qualified "
        "people in accordance with applicable codes and standards.")),
     ("standards", "Statements about standards", P(
        "Where this site refers to ISO 19650, it describes alignment of working method with the "
        "principles of that standard series. It is not a claim of third-party certification, "
        "accreditation or conformity assessment by any body.")),
     ("use", "Permitted use", P("You may view, browse and share this site. You may not:") + "\n" + UL(
        "use the site in any unlawful way or for any unlawful purpose;",
        "attempt to gain unauthorised access to the site or any connected system;",
        "interfere with the site's operation, security or availability;",
        "scrape or systematically extract content by automated means without written permission;",
        f"misrepresent your affiliation with {ENTITY}.")),
     ("ip", "Intellectual property", P(
        "The BIMRACE name, the BIM RACE logo and wordmark, the site design, text, graphics, diagrams "
        f"and code are owned by {ENTITY} or used under licence, and are protected by intellectual "
        "property law. Third-party software names are the property of their respective owners.",
        "You may quote short extracts with clear attribution and a link back to this site. Any other "
        "reproduction, adaptation or commercial use requires our written permission.")),
     ("enquiries", "Enquiries and confidentiality", P(
        "Information you send through the enquiry form is received in confidence for the purpose of "
        "assessing the enquiry. Do not send commercially sensitive project information through the form "
        "before a non-disclosure agreement is in place — ask and we will put one in place first.")),
     ("links", "Third-party links", P(
        "The site may link to third-party websites. We do not control those sites and are not "
        "responsible for their content, accuracy, availability or privacy practices.")),
     ("avail", "Availability and changes", P(
        "We may change, suspend or withdraw any part of this site at any time without notice, including "
        "service descriptions. We may also update these terms; continuing to use the site after a change "
        "means you accept the updated terms.")),
     ("warranty", "Disclaimer of warranties", P(
        "This site is provided \u201cas is\u201d and \u201cas available\u201d. To the fullest extent "
        "permitted by law we exclude all warranties, conditions and representations, express or implied, "
        "including as to accuracy, completeness, fitness for a particular purpose and uninterrupted "
        "availability.")),
     ("liability", "Limitation of liability", P(
        f"To the fullest extent permitted by law, {ENTITY}, its directors, officers, employees and agents "
        "will not be liable for any indirect, incidental, special, consequential or punitive loss, or for "
        "any loss of profit, revenue, data, goodwill or business opportunity, arising out of or in "
        "connection with your use of this site.",
        "Nothing in these terms excludes or limits liability that cannot lawfully be excluded, including "
        "liability for death or personal injury caused by negligence, or for fraud.")),
     ("law", "Governing law", P(
        "These terms are governed by the laws of India. The courts at "
        f"{FILL('city of jurisdiction')} have exclusive jurisdiction over any dispute arising out of or "
        "in connection with them.")),
     ("contact", "Contact", P(
        f"{ENTITY}<br>{FILL('registered address')}<br>Email: {MAIL}<br>Telephone: {CALL}") + "\n" + NOTE(
        "<strong>Before you publish:</strong> replace the highlighted placeholders and have these terms "
        "reviewed by a qualified lawyer.")),
    ])

COOKIES = legal_body("Cookie Policy", "Legal 03 — Cookies",
    P("A short, accurate account of what this website stores on your device and what it requests "
      "from elsewhere."),
    [
     ("what", "What cookies are", P(
        "Cookies are small text files a website stores on your device, commonly used to keep you signed "
        "in, remember preferences or measure how a site is used. Similar technologies include local "
        "storage and tracking pixels.")),
     ("ours", "What this site stores", P(
        "<strong>This website sets no cookies of its own.</strong> It has no accounts and no advertising, "
        "so there is nothing for a cookie to do. It runs no analytics software, no advertising or social "
        "media pixels, and no session recording. Nothing is written to your browser's local storage.")),
     ("third", "Third-party requests", P(
        "The site makes the following requests to third parties. None sets a cookie for ordinary browsing, "
        "but as with any web request your IP address and browser details are visible to the server "
        "contacted, and that provider's terms apply.") + "\n" + UL(
        "<strong>Google Fonts</strong> (fonts.googleapis.com, fonts.gstatic.com) — serves the IBM Plex "
        "typefaces used across the site.",
        "<strong>Supabase Storage</strong> — hosts the founder photograph on the About page.",
        "<strong>Netlify</strong> — hosts the site and receives enquiry form submissions when you send "
        "the form. Netlify may set a cookie in connection with form spam prevention at the point of "
        "submission.") + "\n" + P(
        "The first two can be removed by self-hosting: download the IBM Plex families and reference them "
        "with a local <code>@font-face</code> declaration, and save the photograph alongside the site "
        "files. Neither change breaks anything — the site falls back to system typefaces and to the "
        "founder's initials respectively.")),
     ("manage", "Managing cookies", P(
        "Every major browser lets you view, block and delete cookies from its settings, usually under "
        "Privacy or Site Settings. Because this site sets none of its own, blocking them will not affect "
        "how it works.")),
     ("changes", "If this changes", P(
        "If we add analytics, embedded video, a chat widget or any other tool that uses cookies, we will "
        "update this page first and, where the law requires it, ask for your consent before those cookies "
        "are set.") + "\n" + NOTE(
        "<strong>Keep this page truthful.</strong> It is accurate for the site exactly as built. Adding "
        "any analytics or embed makes it inaccurate and will likely require a consent banner.")),
     ("contact", "Contact", P(
        f"Questions about this policy: {MAIL} or {CALL}.<br>See also our "
        '<a href="privacy.html">Privacy Policy</a> and <a href="terms.html">Terms of Use</a>.')),
    ])

PROJECT_TEMPLATE = """
<section class="section section--flush">
  <div class="shell">
    <div class="note" style="max-width:none;margin-bottom:48px">
      <p><strong>This is the case study template.</strong> Duplicate this file, rename it
      (for example <code>project-riverside-hospital.html</code>), replace every highlighted
      placeholder, update the title and meta description in the <code>&lt;head&gt;</code>, link it
      from <code>projects.html</code>, and add the URL to <code>sitemap.xml</code>. Delete this
      note before publishing.</p>
    </div>

    <div class="spec">
      <div class="spec__row"><div class="spec__k">Section 01<b>Project overview</b></div>
        <div class="spec__v">
          <ul class="spec__list">
            <li>Client type: <span class="fill">[client type]</span></li>
            <li>Sector: <span class="fill">[sector]</span></li>
            <li>Location: <span class="fill">[city, country]</span></li>
            <li>Scale: <span class="fill">[GIA / storeys / value band]</span></li>
            <li>Stage at appointment: <span class="fill">[stage]</span></li>
            <li>Appointment type: <span class="fill">[package / team extension]</span></li>
          </ul></div></div>
      <div class="spec__row"><div class="spec__k">Section 02<b>Scope and disciplines</b></div>
        <div class="spec__v"><span class="fill">[BIM scope, disciplines modelled, level of information
        need, specific deliverables issued]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 03<b>Challenge</b></div>
        <div class="spec__v"><span class="fill">[the engineering or information problem this appointment
        existed to solve — concrete, not generic]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 04<b>Engineering approach</b></div>
        <div class="spec__v"><span class="fill">[model structure, federation strategy, coordination
        method, automation applied, and the reasoning behind each]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 05<b>Coordination record</b></div>
        <div class="spec__v"><span class="fill">[how clashes were tracked and closed, how decisions were
        recorded, how the model was validated before issue]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 06<b>Deliverables issued</b></div>
        <div class="spec__v"><span class="fill">[models, drawings, schedules and data actually issued,
        with formats and status codes]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 07<b>Outcome</b></div>
        <div class="spec__v"><span class="fill">[what changed as a result — quantify only where the
        figure is measured and the client has approved publication]</span></div></div>
      <div class="spec__row"><div class="spec__k">Section 08<b>Visual evidence</b></div>
        <div class="spec__v"><span class="fill">[model views, coordination screenshots or drawing
        extracts, redacted where commercially necessary]</span></div></div>
    </div>
  </div>
</section>
"""

# ================================================================== build ====
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()

ORG_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "Organization",
    "name": "BIMRACE", "legalName": ENTITY, "url": SITE + "/",
    "logo": SITE + "/logo.svg", "image": SITE + "/og-image.png",
    "email": EMAIL, "telephone": "+91-75079-58364",
    "description": "BIMRACE delivers BIM modelling, MEP engineering and multidisciplinary "
                   "coordination for architects, engineers and contractors, structured around "
                   "ISO 19650 information management.",
    "address": {"@type": "PostalAddress", "addressCountry": "IN"},
    "founder": {"@type": "Person", "name": "Somnath Baste", "jobTitle": "Founder"},
    "knowsAbout": ["Building Information Modelling", "MEP Engineering", "BIM Coordination",
                   "ISO 19650", "Digital Engineering", "Clash Detection"],
    "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "email": EMAIL,
                      "telephone": "+91-75079-58364", "availableLanguage": ["en"]}]
}, indent=2) + '</script>\n'

SERVICE_LD = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "ItemList",
    "name": "BIMRACE capabilities",
    "itemListElement": [
        {"@type": "ListItem", "position": i + 1,
         "item": {"@type": "Service", "name": re.sub("&amp;", "&", t), "description": d,
                  "provider": {"@type": "Organization", "name": "BIMRACE"}}}
        for i, (a, t, d) in enumerate(CAPS)]
}, indent=2) + '</script>\n'

page("index", "BIMRACE | BIM, MEP &amp; Digital Engineering for Complex Projects",
     "BIMRACE delivers BIM modelling, MEP engineering and multidisciplinary coordination for "
     "architects, engineers and contractors, structured around ISO 19650 information management.",
     HOME, "index.html", extra=ORG_LD)

page("capabilities", "Capabilities | BIM Modelling, MEP Engineering &amp; Coordination | BIMRACE",
     "BIM modelling and documentation, MEP engineering, BIM coordination, digital engineering and "
     "construction support — scope defined by deliverable, not by software.",
     phero([("Home", "index.html"), ("Capabilities", None)],
           "Capabilities",
           "Five delivery capabilities covering model authoring, building services engineering, "
           "multidisciplinary coordination, automation and construction-stage output.",
           [("Disciplines", "Architectural · Structural · MEP"),
            ("Appointment", "Package, team extension or coordination"),
            ("Standard", "Structured to ISO 19650")]) + CAPABILITIES,
     "capabilities.html",
     extra=SERVICE_LD + breadcrumb_ld([("Home", ""), ("Capabilities", "capabilities.html")]) + "\n")

page("industries", "Industries | Sector Capability | BIMRACE",
     "Building types BIMRACE is equipped to model and coordinate: commercial, residential, "
     "healthcare, data centres, industrial, hospitality, education and retail.",
     phero([("Home", "index.html"), ("Industries", None)],
           "Industries",
           "Sectors differ in services density, clearance tolerance and validation expectation. "
           "These are the building types our discipline mix is set up for.",
           [("Sectors covered", "Eight building types"),
            ("Basis", "Capability, not project claims")]) + INDUSTRIES,
     "industries.html",
     extra=breadcrumb_ld([("Home", ""), ("Industries", "industries.html")]) + "\n")

page("projects", "Projects | Case Study Evidence | BIMRACE",
     "Published project evidence and the case study structure BIMRACE uses to document scope, "
     "approach, coordination record, deliverables and outcome.",
     phero([("Home", "index.html"), ("Projects", None)],
           "Projects",
           "Case studies are published as clients release them. The documentation structure "
           "every entry follows is set out in full below.",
           [("Published", "Awaiting client release"),
            ("Under NDA", "Capability walkthrough available")]) + PROJECTS,
     "projects.html",
     extra=breadcrumb_ld([("Home", ""), ("Projects", "projects.html")]) + "\n")

page("technology", "Technology &amp; Standards | ISO 19650 Delivery | BIMRACE",
     "How BIMRACE structures information delivery: ISO 19650 alignment, EIR, BEP, MIDP, CDE and "
     "level of information need, plus the quality checks applied before issue.",
     phero([("Home", "index.html"), ("Technology", None)],
           "Technology &amp; standards",
           "Information management structured to ISO 19650, the artefacts that govern an "
           "appointment, and the checks applied before anything is issued.",
           [("Framework", "ISO 19650 series"),
            ("Governing artefacts", "EIR · BEP · MIDP · CDE"),
            ("Platform", "In development")]) + TECHNOLOGY,
     "technology.html",
     extra=breadcrumb_ld([("Home", ""), ("Technology", "technology.html")]) + "\n")

page("about", "About | BIM &amp; MEP Engineering Practice | BIMRACE",
     "BIMRACE is an India-based BIM, MEP and digital engineering practice delivering remotely to "
     "international project teams. Founded by Somnath Baste.",
     phero([("Home", "index.html"), ("About", None)],
           "About BIMRACE",
           "A focused engineering practice built around one idea: information that is accurate "
           "enough to rely on and structured enough to be used automatically.",
           [("Entity", ENTITY), ("Base", "India · remote delivery"),
            ("Founder", "Somnath Baste")]) + ABOUT,
     "about.html",
     extra=breadcrumb_ld([("Home", ""), ("About", "about.html")]) + "\n")

page("contact", "Contact | Project Enquiry | BIMRACE",
     "Start a project enquiry with BIMRACE. Share scope, disciplines and deliverables and receive "
     "a considered response on approach and programme within two working days.",
     phero([("Home", "index.html"), ("Contact", None)],
           "Start an enquiry",
           "Tell us the scope and you will get a technical response, not a brochure.",
           [("Email", EMAIL), ("Telephone", PHONE),
            ("Response", "Within two working days")]) + CONTACT,
     "contact.html", cta=False,
     extra=breadcrumb_ld([("Home", ""), ("Contact", "contact.html")]) + "\n")

page("thank-you", "Enquiry received | BIMRACE",
     "Your enquiry has been received. BIMRACE responds to project enquiries within two working days.",
     THANKYOU, "", cta=False, extra='<meta name="robots" content="noindex, follow">\n')

page("404", "Page not found | BIMRACE",
     "The page you requested could not be found on the BIMRACE website.",
     NOTFOUND, "", cta=False, extra='<meta name="robots" content="noindex, follow">\n')

page("project-template", "Case study template | BIMRACE",
     "Internal case study template for publishing BIMRACE project evidence.",
     phero([("Home", "index.html"), ("Projects", "projects.html"), ("Case study template", None)],
           "Case study template",
           "Duplicate this page for each published project. Every section below must be completed "
           "or removed before publication.",
           [("Status", "Template — not published work")]) + PROJECT_TEMPLATE,
     "projects.html", extra='<meta name="robots" content="noindex, nofollow">\n')

page("privacy", "Privacy Policy | BIMRACE",
     "How BIMRACE Pvt Ltd handles personal information collected through the BIMRACE website and "
     "project enquiries.", PRIVACY, "", cta=False)
page("terms", "Terms of Use | BIMRACE",
     "The terms that apply to your use of the BIMRACE website, operated by BIMRACE Pvt Ltd.",
     TERMS, "", cta=False)
page("cookies", "Cookie Policy | BIMRACE",
     "What cookies and third-party requests the BIMRACE website uses, and how to control them.",
     COOKIES, "", cta=False)

# ------------------------------------------------------------- static files --
for f in ["style.css", "script.js", "lead-capture.js", "config.js", "logo.svg", "logo-mark.svg", "favicon.svg", "favicon.ico",
          "apple-touch-icon.png", "icon-192.png", "icon-512.png", "og-image.png"]:
    shutil.copy(ROOT / f, OUT / f)

(OUT / "site.webmanifest").write_text(json.dumps({
    "name": "BIMRACE", "short_name": "BIMRACE",
    "description": "BIM, MEP and digital engineering delivery",
    "start_url": "/", "display": "standalone",
    "background_color": "#ffffff", "theme_color": "#ffffff",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
              {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]
}, indent=2) + "\n")

(OUT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\nDisallow: /project-template.html\nDisallow: /thank-you.html\n\n"
    f"Sitemap: {SITE}/sitemap.xml\n")

PUBLIC = [("", "1.0", "monthly"), ("capabilities.html", "0.9", "monthly"),
          ("industries.html", "0.8", "monthly"), ("projects.html", "0.8", "weekly"),
          ("technology.html", "0.8", "monthly"), ("about.html", "0.7", "monthly"),
          ("contact.html", "0.9", "monthly"), ("privacy.html", "0.3", "yearly"),
          ("terms.html", "0.3", "yearly"), ("cookies.html", "0.3", "yearly")]
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(f"  <url>\n    <loc>{SITE}/{u}</loc>\n    <changefreq>{c}</changefreq>\n"
                f"    <priority>{p}</priority>\n  </url>" for u, p, c in PUBLIC)
    + "\n</urlset>\n")

(OUT / "netlify.toml").write_text("""# Netlify configuration — static site, no build step required.
# The deployable site sits at the ROOT of this folder. Drag this whole folder
# onto Netlify, or point a Git deploy at it with an empty build command.
[build]
  publish = "."

# Keep the generator source out of the public site.
[[redirects]]
  from = "/_source/*"
  to = "/404.html"
  status = 404

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=(), interest-cohort=()"

[[headers]]
  for = "/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.svg"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.png"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

# Pretty URLs: /capabilities -> /capabilities.html
[[redirects]]
  from = "/capabilities"
  to = "/capabilities.html"
  status = 200
[[redirects]]
  from = "/industries"
  to = "/industries.html"
  status = 200
[[redirects]]
  from = "/projects"
  to = "/projects.html"
  status = 200
[[redirects]]
  from = "/technology"
  to = "/technology.html"
  status = 200
[[redirects]]
  from = "/about"
  to = "/about.html"
  status = 200
[[redirects]]
  from = "/contact"
  to = "/contact.html"
  status = 200
[[redirects]]
  from = "/privacy"
  to = "/privacy.html"
  status = 200
[[redirects]]
  from = "/terms"
  to = "/terms.html"
  status = 200
[[redirects]]
  from = "/cookies"
  to = "/cookies.html"
  status = 200

[[redirects]]
  from = "/*"
  to = "/404.html"
  status = 404
""")

print(f"built {len(list(OUT.glob('*.html')))} pages ->", OUT)
