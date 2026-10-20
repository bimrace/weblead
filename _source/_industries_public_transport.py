"""
BIMRACE — public & government and transportation sector pages.

Kept in their own module because these two sectors carry more than the
original eight: building types, typical deliverables, an engagement process,
an explicit scope boundary and an on-page enquiry form (see the optional
blocks in build.py). Scope follows the service catalogue's Building Types
sheet:

    Public/Government  — All core MEP disciplines                    (Phase 1)
    Transportation     — Building-services scope, subject to
                         specialist requirements                      (Conditional)

As with every sector page, nothing here claims completed projects, public-
sector contracts, security clearances or sector accreditations. The pages
describe capability and workflow fit, and say so.
"""

# Shared engagement process: the same five steps the catalogue describes for
# every appointment, worded for a client who may not use BIM terminology.
PROCESS = [
    ("01", "Enquiry and inputs",
     "You send the scope, stage and the drawings or models you have. We confirm what is usable, "
     "what is missing and which services the project actually needs."),
    ("02", "Scope and proposal",
     "We agree the deliverables, the level of model detail (LOD/LOI — how much geometry and data "
     "each element carries), file formats, programme and what is excluded."),
    ("03", "Modelling and coordination",
     "Revit models are built from your design information and checked against architecture, "
     "structure and each other. AI-assisted checking groups the issues; engineers resolve them."),
    ("04", "QA/QC and issue",
     "Every issue passes model QA/QC before it leaves us. Drawings, schedules, quantities and clash "
     "reports are issued under revision control."),
    ("05", "Handover",
     "Native models, drawings, registers and a handover note listing files, assumptions and "
     "anything left open — so the building owner can actually use what they receive."),
]

PUBLIC_FIGURE = (
    '''<svg viewBox="0 0 520 300" role="img" aria-labelledby="pg-fig-t">
          <title id="pg-fig-t">Illustrative section through a public administrative building showing a roof plant room, a central service riser, ceiling-zone ductwork, water and drainage pipework, cable containment and fire protection mains on each floor</title>
          <rect class="sf-slab" x="30" y="268" width="460" height="10"/>
          <rect class="sf-slab" x="50" y="196" width="420" height="8"/>
          <rect class="sf-slab" x="50" y="128" width="420" height="8"/>
          <rect class="sf-slab" x="50" y="60" width="420" height="8"/>
          <path class="sf-st" d="M50 268V60M470 268V60M150 268V60M370 268V60"/>
          <path class="sf-st" d="M70 268v-40M90 268v-40M110 268v-40M410 268v-40M430 268v-40M450 268v-40"/>
          <rect class="sf-mech" x="300" y="22" width="120" height="38"/>
          <text class="sf-lbl" x="308" y="16">ROOF PLANT ROOM</text>
          <rect class="sf-zone" x="236" y="60" width="44" height="208"/>
          <text class="sf-lbl" x="232" y="290">SERVICE RISER</text>
          <path class="sf-mech" d="M244 68v200h10V68z"/>
          <path class="sf-plumb" d="M262 68v200M268 68v200"/>
          <path class="sf-elec" d="M275 68v200"/>
          <rect class="sf-mech" x="60" y="140" width="170" height="12"/>
          <rect class="sf-mech" x="286" y="140" width="170" height="12"/>
          <rect class="sf-mech" x="60" y="208" width="170" height="12"/>
          <rect class="sf-mech" x="286" y="208" width="170" height="12"/>
          <rect class="sf-mech" x="60" y="72" width="170" height="12"/>
          <rect class="sf-mech" x="286" y="72" width="170" height="12"/>
          <path class="sf-plumb" d="M60 158h170M286 158h170M60 226h170M286 226h170M60 90h170M286 90h170"/>
          <path class="sf-elec" d="M60 164h170M286 164h170M60 232h170M286 232h170M60 96h170M286 96h170"/>
          <path class="sf-fire" d="M60 170h170M286 170h170M60 238h170M286 238h170M60 102h170M286 102h170"/>
          <path class="sf-fire" d="M80 170v5M120 170v5M160 170v5M200 170v5M300 170v5M340 170v5M380 170v5M420 170v5"/>
          <text class="sf-lbl" x="292" y="190">CEILING ZONE</text>
          <text class="sf-lbl" x="292" y="258">PUBLIC HALL</text>
        </svg>''',
    "Illustrative section — not a BIMRACE project",
)

TRANSPORT_FIGURE = (
    '''<svg viewBox="0 0 520 306" role="img" aria-labelledby="tr-fig-t">
          <title id="tr-fig-t">Illustrative section through a passenger terminal building showing a long-span roof with smoke extract ductwork, a concourse level with services in the ceiling zone, a plant room, and a platform level below where only building services are in scope</title>
          <path class="sf-st" d="M30 120Q260 20 490 120"/>
          <path class="sf-st" d="M30 120v150M490 120v150"/>
          <path class="sf-st" d="M110 86v184M200 62v208M320 62v208M410 86v184"/>
          <rect class="sf-slab" x="30" y="180" width="460" height="10"/>
          <rect class="sf-slab" x="20" y="270" width="480" height="10"/>
          <path class="sf-mech" d="M70 112Q260 34 450 112l0 10Q260 46 70 122z"/>
          <text class="sf-lbl" x="216" y="110">SMOKE EXTRACT</text>
          <rect class="sf-mech" x="40" y="194" width="440" height="11"/>
          <path class="sf-plumb" d="M40 211h440"/>
          <path class="sf-elec" d="M40 217h440"/>
          <path class="sf-fire" d="M40 223h440"/>
          <path class="sf-fire" d="M80 223v5M150 223v5M220 223v5M290 223v5M360 223v5M430 223v5"/>
          <text class="sf-lbl" x="38" y="170">CONCOURSE</text>
          <rect class="sf-mech" x="330" y="140" width="72" height="40"/>
          <text class="sf-lbl" x="334" y="134">PLANT ROOM</text>
          <path class="sf-plumb" d="M60 180v-56M66 180v-56"/>
          <text class="sf-lbl" x="214" y="258">PLATFORM LEVEL</text>
          <path class="sf-zone" d="M20 288h480"/>
          <text class="sf-lbl" x="140" y="302">TRACK · ROADS · AIRSIDE SYSTEMS EXCLUDED</text>
        </svg>''',
    "Illustrative section — not a BIMRACE project",
)


PUBLIC_GOVERNMENT = {
 "slug": "public-government",
 "nav": "Public &amp; government",
 "h1": "MEP BIM services for public and government buildings",
 "title": "Government Building MEP BIM Services | BIMRACE",
 "desc": "MEP BIM modelling, coordination and clash detection for public and government "
         "buildings: civic offices, courts, libraries and public service centres.",
 "eyebrow": "Public &amp; government buildings",
 "lede": "Public buildings are owned and run for decades, documented for audit and handed between "
         "many teams. The model has to be coordinated, traceable and usable long after the "
         "project team has gone.",
 "meta": [("Sector scope", "All core MEP disciplines"), ("Priority", "Traceable revisions"),
          ("Handover", "Maintainable asset information"),
          ("Disciplines", "Plumbing · HVAC · FP · Electrical")],
 "form": True,
 "figure": PUBLIC_FIGURE,
 "types_title": "The public and civic buildings we support",
 "types_lede": "Building-services modelling and coordination for public-sector and institutional "
               "buildings, subject to the agreed scope and the project's own requirements.",
 "types": [
   ("Government and administrative offices", "Ministries, departmental and municipal offices — "
    "large open floors, meeting suites and secure areas served from shared risers."),
   ("Municipal and civic buildings", "Town halls, civic centres and council chambers, often with "
    "public halls and assembly spaces needing their own ventilation strategy."),
   ("Public service centres", "Citizen service centres, registries and public counters with high "
    "occupancy and long operating hours."),
   ("Courts and judicial buildings", "Courtrooms, custody and secure circulation where services "
    "routes must respect separated zones and access control."),
   ("Libraries and cultural facilities", "Libraries, archives, museums and galleries with "
    "environmental control and protected collections."),
   ("Public healthcare and education buildings", "Public clinics, schools and training centres. "
    "Specialist healthcare requirements need defined project criteria."),
   ("Community and institutional facilities", "Community halls, sports and welfare buildings "
    "serving the public."),
 ],
 "profile_title": "What public-sector projects need from the model",
 "profile": [
   ("Many hands, one record",
    "A public building passes through a client body, design consultants, contractors, auditors and "
    "a facilities team. Each needs to understand what was decided and why. That only works when the "
    "coordinated model, the drawings and the revision register agree with each other — so we keep "
    "them as one source rather than three parallel documents."),
   ("Every change has to be traceable",
    "Public projects are reviewed, re-scoped and audited. A clash that moved a duct, a design change "
    "that moved a riser, a quantity that changed between revisions — each needs a record of what "
    "changed, when and on whose instruction. Revision control and change reports are part of the "
    "deliverable, not an afterthought."),
   ("Handover outlives the project",
    "The organisation that runs the building is usually not the one that built it. Asset registers, "
    "equipment schedules and a clear handover note are what let a facilities team find and maintain "
    "plant years later."),
 ],
 "drivers_eyebrow": "Coordination and documentation priorities",
 "drivers_title": "What we prioritise on public and government buildings",
 "drivers_lede": "These are the practical priorities that make a public-sector BIM deliverable "
                 "useful to the client body, the contractor and the people who maintain the building.",
 "drivers_kicker": "Priority",
 "drivers": [
   ("Coordinated documentation", "Plans, sections, risers and schedules derived from one coordinated "
    "model, so drawings and model never disagree."),
   ("Traceable revisions", "Drawing and model revision registers, clash issue logs and quantity "
    "change reports that show what changed, when and why."),
   ("Multidisciplinary collaboration", "Architectural, structural and MEP models federated on shared "
    "coordinates, with clash reports the whole team can act on."),
   ("Maintainable asset information", "Equipment and asset registers, and COBie-style data where the "
    "client specifies it, prepared for the facilities team."),
   ("Clearly defined deliverables", "LOD/LOI, formats, exclusions and handover contents agreed in "
    "the proposal — the deliverable list is a document, not an assumption."),
 ],
 "lead_disc": "HVAC and electrical usually dominate ceiling and riser space in large public floors, "
              "but the deciding factor is often documentation discipline across many stakeholders.",
 "info_req": [
   "Equipment and asset data on model elements, ready for the client's asset register",
   "Revision history for models and drawings, kept with the deliverables",
   "Room and space data aligned with the architectural model for maintenance planning",
   "Exchange files (IFC, NWC/NWD) where the client's systems or reviewers require them",
 ],
 "autos": [
   ("AI-assisted document review", "live", "Tender drawings and specifications read to list systems, "
    "gaps and conflicts before modelling starts."),
   ("AI-drafted revision and change reports", "live", "What changed between issues, drafted from model "
    "data and checked by an engineer before it is issued."),
   ("Asset register extraction", "live", "Equipment and asset data extracted from the model into a "
    "structured register for handover."),
 ],
 "delivers": [
   ("Native Revit MEP models", "Plumbing, HVAC, fire protection and electrical models in editable "
    ".RVT, developed from the supplied drawings and design information."),
   ("Federated model and clash reports", "Coordinated architectural, structural and MEP models with "
    "clash matrices, issue lists, screenshots and viewpoints."),
   ("Plant room, riser and shaft coordination", "Coordinated layouts and sections for plant rooms, "
    "risers, shafts and other service spaces."),
   ("Shop drawings and construction documentation", "Plans, sections, risers, details and builders' "
    "work drawings, issued as PDF and agreed DWG."),
   ("Schedules, quantities and BOQ support", "Equipment schedules, model-based quantity takeoffs and "
    "BOQ support from approved design information."),
   ("QA/QC, revision register and handover", "Model QA/QC report, revision register, exchange files "
    "and a handover note. As-built models from verified site information, when commissioned."),
 ],
 "process": PROCESS,
 "excludes_title": "What a public-sector appointment does not include",
 "excludes": [
   "Statutory approvals, authority submissions and professional sign-off remain with the project's "
   "appointed designers and licensed professionals.",
   "Engineering design and calculations are provided only when included in the agreed scope and "
   "supported by appropriately qualified personnel.",
   "We do not claim public-sector framework appointments, security clearances or government "
   "accreditations. Where a project requires them, tell us at enquiry stage.",
   "As-built accuracy depends on verified site information and a defined verification "
   "responsibility.",
 ],
 "faqs": [
   ("Do you work on government and public-sector buildings?",
    "Yes — public and government buildings are a core sector in our service catalogue, across all "
    "four MEP disciplines. This page describes the scope and workflow; it does not claim specific "
    "public-sector contracts, because we publish no project history until a client releases it."),
   ("Can you work to our public-sector BIM standards and templates?",
    "Yes. We work to the client's BIM execution plan, templates, naming and exchange requirements "
    "where they exist, and agree them at the start where they do not."),
   ("What does 'traceable revisions' mean in practice?",
    "Every issue of the model and drawings is logged in a revision register, clash issues are "
    "tracked to closure, and quantity changes between revisions are reported. Anyone reviewing the "
    "project later can see what changed and when."),
   ("Do you hold security clearances?",
    "Not that we publish here. If a project requires cleared personnel or specific data-handling "
    "arrangements, say so in your enquiry and we will confirm what is possible before we commit."),
   ("What will the facilities team receive at handover?",
    "Native models, drawings, equipment and asset registers, and a handover note listing files, "
    "assumptions and open items. The exact contents are agreed in the proposal."),
 ],
 "services": ["bim-coordination-clash-detection", "hvac-bim-services", "bim-modelling-documentation",
              "electrical-bim-services", "plumbing-public-health-bim", "fire-protection-bim-services",
              "quantity-takeoff-boq", "revit-services", "as-built-bim-services"],
}


TRANSPORTATION = {
 "slug": "transportation",
 "nav": "Transportation buildings",
 "h1": "MEP BIM for transportation buildings and facilities",
 "title": "Transportation Building MEP BIM Services | BIMRACE",
 "desc": "MEP BIM modelling and coordination for transportation buildings: airport terminals, "
         "railway and metro stations, bus terminals, depots and parking buildings.",
 "eyebrow": "Transportation buildings &amp; facilities",
 "lede": "Terminals and stations are buildings first: long spans, large volumes, high occupancy and "
         "long operating hours. We model and coordinate their building services — not the track, "
         "roads or airside systems around them.",
 "meta": [("Sector scope", "Building services only"), ("Availability", "Conditional"),
          ("Priority", "Large-volume ventilation"),
          ("Disciplines", "Plumbing · HVAC · FP · Electrical")],
 "form": True,
 "figure": TRANSPORT_FIGURE,
 "types_title": "The transportation buildings we support",
 "types_lede": "The building and facility components of transportation projects. Taken on where "
               "the project's specialist requirements and inputs are confirmed.",
 "types": [
   ("Airport terminals and passenger buildings", "Concourses, check-in halls, gate lounges and "
    "landside passenger buildings — building services only."),
   ("Railway and metro stations", "Station buildings, concourses and ticket halls, with the "
    "building-services interfaces to platform areas."),
   ("Bus terminals and interchanges", "Passenger interchange buildings, waiting halls and "
    "operational offices."),
   ("Transport administration buildings", "Control, administration and office buildings serving "
    "transport operators."),
   ("Depots and maintenance buildings", "Depot and workshop buildings, where the scope is building "
    "services rather than process or rolling-stock systems."),
   ("Parking structures and associated buildings", "Multi-storey car parks with ventilation, "
    "drainage, lighting and fire protection."),
   ("Passenger amenities and support buildings", "Retail, toilet blocks, staff facilities and "
    "operational support buildings."),
 ],
 "profile_title": "What makes transportation buildings different",
 "profile": [
   ("Large volumes change the ventilation problem",
    "A concourse or terminal hall is a single tall space, not a stack of floors. Ventilation, smoke "
    "extraction and comfort cooling have to work across long spans, and the ductwork that does it "
    "often runs at high level along the roof structure. Coordinating that against long-span steel "
    "and roof drainage is where the effort concentrates."),
   ("Buildings that never close",
    "Stations and terminals operate for most of the day, every day. Maintenance has to happen "
    "around passengers, so access to plant, valves and dampers is a design requirement. We test "
    "access and maintenance clearances as part of coordination, not only hard clashes."),
   ("A clear line between building and infrastructure",
    "Transportation projects combine buildings with specialist infrastructure. Our scope is the "
    "building services inside and serving the building. Track, signalling, roads, bridges, tunnels "
    "and airside systems need their own specialists, and we say so at the start."),
 ],
 "drivers_eyebrow": "Coordination and documentation priorities",
 "drivers_title": "What we prioritise on transportation buildings",
 "drivers_lede": "The building-services issues that drive coordination effort in terminals, stations "
                 "and their support buildings.",
 "drivers_kicker": "Priority",
 "drivers": [
   ("Long-span and high-level services", "Ductwork, drainage and containment routed along roof "
    "structure and at height, coordinated with long-span steel."),
   ("Ventilation and smoke extraction modelling", "Large-volume ventilation and smoke extract "
    "ductwork modelled and coordinated to the design supplied."),
   ("Access and maintenance clearance", "Clearances for plant, valves and dampers tested as rules, "
    "because maintenance happens while the building is in use."),
   ("Plant-room and equipment-space coordination", "Plant rooms, risers and equipment spaces laid "
    "out with replacement routes and access."),
   ("Construction-stage updates", "Model updates during construction and as-built handover, if "
    "included in scope."),
 ],
 "lead_disc": "HVAC and fire protection usually lead in large passenger volumes, with drainage "
              "and electrical containment following the long-span structure.",
 "info_req": [
   "Clear scope boundary between building services and infrastructure systems",
   "Access and maintenance zones modelled, not assumed",
   "Equipment data for operator asset registers",
   "Exchange formats agreed with the wider project team, often IFC and NWC/NWD",
 ],
 "autos": [
   ("AI clash grouping and prioritisation", "live", "Clashes on large federated models grouped by "
    "cause and responsible discipline, so coordination meetings resolve rather than discover."),
   ("Clearance rule sets", "live", "Access and maintenance clearances tested across the whole "
    "model, not sampled by eye."),
   ("Quantity extraction and revision comparison", "live", "Duct, pipe and containment quantities "
    "measured from the model and compared between revisions."),
 ],
 "delivers": [
   ("Native Revit MEP models", "HVAC, ventilation, plumbing, drainage, fire protection and "
    "electrical distribution and lighting models in editable .RVT."),
   ("Federated model and clash reports", "Federated models with clash and access/maintenance "
    "clearance reviews, issue logs and viewpoints."),
   ("Plant-room and equipment-space coordination", "Coordinated plant rooms, risers and equipment "
    "spaces with sections."),
   ("Shop drawings and schedules", "Installation drawings, builders' work drawings and equipment "
    "schedules derived from the coordinated model."),
   ("Quantity takeoffs", "Model-based quantities and BOQ support with stated measurement rules."),
   ("Construction updates and as-built handover", "Construction-stage model updates and as-built "
    "handover from verified site information, if included in scope."),
 ],
 "process": PROCESS,
 "excludes_title": "What is excluded on transportation projects",
 "excludes": [
   "Rail alignments, track systems, roads, bridges, tunnels and other civil infrastructure are "
   "excluded unless separately agreed and supported by the appropriate specialists.",
   "Signalling, communications, traction power and airside/aviation systems are specialist "
   "engineering scopes and are excluded unless separately agreed.",
   "Specialist smoke-control analysis, tunnel ventilation and fire engineering require agreed design "
   "responsibility and qualified specialists.",
   "We do not claim specialist airport, railway or metro credentials. Statutory and operator "
   "approvals remain with the appointed designers.",
 ],
 "faqs": [
   ("Do you work on airport terminals and railway stations?",
    "On their building services — HVAC, ventilation, plumbing, drainage, fire protection and "
    "electrical — yes, where the project's specialist requirements are confirmed. We do not work on "
    "track, signalling, roads, tunnels or airside systems."),
   ("What is the difference between a transportation building and transportation infrastructure?",
    "The building is the terminal, station, depot or car park and the services inside it. The "
    "infrastructure is the track, roads, bridges, tunnels and systems such as signalling. Our scope "
    "is the building services; infrastructure needs its own specialists."),
   ("Can you coordinate our MEP models with the wider project's infrastructure models?",
    "We can federate building-services models with the models the wider team supplies and report "
    "clashes at the interfaces. Resolving infrastructure design remains with its designers."),
   ("Do you model smoke extraction systems?",
    "We model and coordinate smoke extract ductwork and equipment to the design supplied. Smoke "
    "control analysis and tunnel ventilation design are specialist scopes we do not provide unless "
    "separately agreed with qualified specialists."),
   ("Do you have airport or railway project credentials?",
    "We do not publish project history until a client releases it, and we do not claim sector "
    "credentials we have not verified. Ask at enquiry stage and we will show our workflow and QA "
    "output under NDA."),
 ],
 "services": ["hvac-bim-services", "fire-protection-bim-services", "bim-coordination-clash-detection",
              "plumbing-public-health-bim", "electrical-bim-services", "bim-modelling-documentation",
              "quantity-takeoff-boq", "revit-services", "as-built-bim-services"],
}

PAGES = [PUBLIC_GOVERNMENT, TRANSPORTATION]
