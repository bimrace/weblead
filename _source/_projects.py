"""
BIMRACE — published case studies.

HOW TO ADD A PROJECT
--------------------
1. Get the client's written permission to publish. Without it, do not add the
   entry (or keep "client_released": False, which the build refuses to publish).
2. Copy the EXAMPLE dict below into CASE_STUDIES and fill every field.
3. Optional image: put a JPG/PNG/WEBP in _source/projects/ and set "image" to
   its file name and "image_alt" to a description of what it shows.
4. cd _source && python build.py --install && python audit.py --strict
   The page appears at /projects/<slug>.html, on the Projects page, in the
   sitemap and with structured data. Then commit on a branch and open a PR.

RULES THE BUILD ENFORCES
------------------------
- "client_released" must be True.
- "outcome" is optional; if given it needs "outcome_basis" (how it was
  measured). No basis, no number.
- Every slug in "services" must be a real service page.
- "sector" must be a real sector page slug (industries/<sector>.html).
"""

EXAMPLE = {
    "slug": "riverside-hospital-mep-coordination",          # URL: /projects/<slug>.html
    "client_released": False,                               # must be True to publish
    "client": "Confidential healthcare developer",          # or the client's name, with permission
    "title": "Hospital MEP Coordination, 12 Floors | BIMRACE",    # <= 60 characters
    "desc": "MEP BIM coordination for a 12-floor hospital: federated models, 1,400 clashes "
            "resolved before construction drawings were issued.",  # 120-160 characters
    "h1": "Coordinating dense hospital services inside a fixed ceiling void",
    "sector": "healthcare",
    "location": "Pune, India",
    "scale": "38,000 m², 12 floors",
    "stage": "Construction documentation",
    "year": "2026",
    "services": ["bim-coordination-clash-detection", "hvac-bim-services"],
    "problem": "One paragraph, in the client's terms: what was slow, risky or unresolvable.",
    "scope": ["Disciplines modelled", "Coordination scope", "Level of information need",
              "What stayed with others"],
    "approach": ["How the model was structured", "Which checks were automated",
                 "Where engineers reviewed"],
    "deliverables": ["Coordinated Revit models", "Clash reports", "Shop drawings"],
    "outcome": "",                 # e.g. "1,400 clashes closed before IFC issue"
    "outcome_basis": "",           # e.g. "Navisworks clash log, rev C to rev F"
    "lessons": "What did not work, what was abandoned, what had to be rewritten.",
    "image": "",                   # file in _source/projects/, optional
    "image_alt": "",
}

# Published case studies, newest first. Empty until a client releases one.
CASE_STUDIES = []

REQUIRED = ["slug", "client_released", "client", "title", "desc", "h1", "sector", "location",
            "scale", "stage", "year", "services", "problem", "scope", "approach", "deliverables",
            "lessons"]


def validate(case, service_slugs, sector_slugs):
    """Raise on anything that would publish an unverifiable or broken page."""
    missing = [k for k in REQUIRED if k not in case or case[k] in ("", [], None)]
    if missing:
        raise ValueError(f"case study {case.get('slug')!r}: missing {missing}")
    if case["client_released"] is not True:
        raise ValueError(f"case study {case['slug']!r}: client_released is not True — not publishable")
    if case.get("outcome") and not case.get("outcome_basis"):
        raise ValueError(f"case study {case['slug']!r}: outcome given without outcome_basis")
    bad = [s for s in case["services"] if s not in service_slugs]
    if bad:
        raise ValueError(f"case study {case['slug']!r}: unknown services {bad}")
    if case["sector"] not in sector_slugs:
        raise ValueError(f"case study {case['slug']!r}: unknown sector {case['sector']!r}")
