"""
BIMRACE — MEP engineering design service pages.

Catalogue basis: Service Packages sheet, PKG-05 "MEP Engineering Design" —
"System layouts, sizing, calculations and engineering documentation for
explicitly contracted disciplines", offered "only with qualified resources and
explicit design responsibility". BIMRACE confirmed it holds those resources, so
these pages offer design as a service in its own right.

Every page states the same responsibility boundary: the design is prepared by
BIMRACE's qualified engineers within the design responsibility written into
the appointment; where a jurisdiction requires a locally licensed engineer to
sign, stamp or submit, that engineer of record does so and we support them.
No page claims licences, stamps or authority approvals.
"""

RESPONSIBILITY = (
    "Design is carried out by BIMRACE's qualified engineers within the design responsibility "
    "written into the appointment. Where a jurisdiction requires a locally licensed engineer to "
    "sign, stamp or submit drawings and calculations, that engineer of record does so; we prepare "
    "and support the submission. Authority approvals are obtained by the appointed professionals.")

DESIGN_PROCESS = [
    ("01", "Brief and design basis", "Building use, occupancy, design conditions, the codes the "
     "project must meet and the responsibility split — agreed and written down before any "
     "calculation is run."),
    ("02", "Concept and system selection", "System options compared for space, energy, capital "
     "and maintenance cost, with plant and riser space reserved early so the architecture can "
     "accommodate them."),
    ("03", "Calculations and sizing", "Loads, flows and sizes calculated to the stated method, "
     "with assumptions listed on the calculation rather than buried in it."),
    ("04", "Layouts in the model", "The design is drawn directly in Revit, so sizes, routes and "
     "equipment data live on the elements and coordination starts from the design, not after it."),
    ("05", "Coordination and review", "Federated clash and clearance checks against architecture, "
     "structure and the other services; an independent engineering review before issue."),
    ("06", "Issue and support", "Design drawings, calculations, schematics and schedules issued "
     "under revision control, with support through tender, approvals and construction queries."),
]

DESIGN_SERVICES = [

# ---------------------------------------------------------------------------
{
 "slug": "mep-design-services",
 "nav": "MEP engineering design",
 "h1": "MEP engineering design services",
 "title": "MEP Design Services | HVAC, Plumbing, Electrical &amp; Fire | BIMRACE",
 "desc": "MEP engineering design for buildings: HVAC, plumbing, electrical and fire protection "
         "design with calculations, schematics and coordinated Revit drawings, worldwide.",
 "eyebrow": "MEP engineering design",
 "lede": "Mechanical, electrical, plumbing and fire protection designed together, calculated by "
         "engineers and drawn straight into a coordinated model — so the design that is approved "
         "is the design that fits.",
 "codes": ["PL-16", "PL-17", "HVAC-17", "HVAC-18", "HVAC-19", "FP-16", "EL-12", "EL-14"],
 "meta": [("Disciplines", "HVAC · Plumbing · Electrical · Fire"), ("Status", "Live"),
          ("Output", "Calculations · Schematics · Design drawings"),
          ("Basis", "Codes named by the project")],
 "position": [
   ("Design and coordination are one activity",
    "A duct sized without its route is a size that will change. We size and route together, in "
    "the model, so the design that leaves us has already been tested against the ceiling void, "
    "the structure and the other services. That removes the most expensive cycle in building "
    "services: the design that is correct on paper and impossible on site."),
   ("Calculations you can check",
    "Every calculation states its method, inputs, design conditions and assumptions. A reviewer "
    "at the client, the contractor or the authority can follow it without asking us what we "
    "meant — which is what lets a design move through approval without avoidable comments."),
   ("A clear line of design responsibility", RESPONSIBILITY),
 ],
 "delivers": [
   ("Design basis report", "Design conditions, occupancy, codes and standards, system strategy and "
    "the assumptions everything else depends on."),
   ("Engineering calculations", "Heating and cooling loads, airflow, duct and pipe sizing, water "
    "demand and drainage flows, hydraulic calculations and electrical load schedules."),
   ("System schematics", "HVAC, plumbing, fire protection and electrical schematics and single-line "
    "diagrams."),
   ("Coordinated design drawings", "Layouts, risers, plant rooms and sections drawn in Revit and "
    "coordinated with architecture and structure."),
   ("Equipment schedules and specification input", "Plant and equipment schedules with duties, "
    "and technical input for the project specification."),
   ("Tender and construction support", "Responses to tender queries, review of contractor "
    "submittals and shop drawings, and design clarifications during construction."),
 ],
 "inputs": [
   "Architectural drawings or model, and the structural grid",
   "Building use, occupancy and operating hours",
   "The codes and standards the project must comply with, and the jurisdiction",
   "Client or tenant requirements, and any energy or sustainability targets",
   "The design responsibility split and who is engineer of record",
 ],
 "process": DESIGN_PROCESS,
 "autos": [
   ("Calculation-to-model reconciliation", "live", "Calculated sizes compared with modelled sizes, "
    "element by element, so the drawing and the calculation cannot silently disagree."),
   ("Design rule checking", "live", "Velocity, pressure, clearance and spacing rules tested across "
    "the whole model before issue."),
 ],
 "nots": [
   "We do not stamp drawings or act as engineer of record where a local licence is required; the "
   "appointed local engineer does, with our support.",
   "We do not obtain authority approvals on the client's behalf; we prepare and support submissions.",
   "We do not provide commissioning, site testing or certification.",
 ],
 "faqs": [
   ("Do you provide MEP design or only BIM modelling?",
    "Both. We provide MEP engineering design — calculations, system design, schematics and design "
    "drawings — and BIM modelling, coordination and documentation. Design is delivered within the "
    "design responsibility agreed in the appointment."),
   ("Which codes and standards do you design to?",
    "The ones the project names. Typical examples are ASHRAE and CIBSE guidance for HVAC, NFPA and "
    "BS EN for fire protection, IPC/UPC or BS EN for plumbing, and IEC, BS 7671 or the NEC for "
    "electrical, alongside India's National Building Code where it applies."),
   ("Can you design for projects outside India?",
    "Yes. We design remotely for international projects to the client's codes. Where the "
    "jurisdiction requires a locally licensed engineer to sign, that engineer of record reviews and "
    "stamps, and we support the submission."),
   ("Do you deliver the design as a Revit model?",
    "Yes. The design is drawn in Revit from the start, so the model, drawings, schedules and "
    "quantities all come from the same coordinated source."),
 ],
 "related": [
   ("services/hvac-design-services.html", "HVAC design", "Loads, ventilation, ductwork and plant."),
   ("services/plumbing-design-services.html", "Plumbing design", "Water supply and drainage design."),
   ("services/electrical-design-services.html", "Electrical design", "Power, lighting and distribution."),
   ("services/fire-protection-design-services.html", "Fire protection design",
    "Sprinkler, hydrant and suppression design."),
 ],
 "prefill": "mep_design",
},

# ---------------------------------------------------------------------------
{
 "slug": "hvac-design-services",
 "nav": "HVAC design",
 "h1": "HVAC design services",
 "title": "HVAC Design Services | Load Calculations &amp; Ductwork | BIMRACE",
 "desc": "HVAC design for buildings: heating and cooling load calculations, ventilation, ductwork "
         "and pipe sizing, plant selection, schematics and coordinated HVAC drawings.",
 "eyebrow": "HVAC design",
 "lede": "Cooling, heating and ventilation designed from the loads up — and drawn into the model "
         "at the same time, so the ductwork that is calculated is ductwork that fits.",
 "codes": ["HVAC-07", "HVAC-16", "HVAC-17", "HVAC-18", "HVAC-19", "HVAC-21"],
 "meta": [("Discipline", "HVAC"), ("Status", "Live"),
          ("Systems", "Chilled water · VRF · Ventilation · Smoke"),
          ("Output", "Load calcs · Sizing · Schematics · Drawings")],
 "position": [
   ("Loads decide the plant, the plant decides the plant room",
    "Cooling and heating loads set equipment sizes, which set plant-room area, riser size and roof "
    "space. Getting the loads right early is what stops the architecture being redrawn around an "
    "oversized chiller later."),
   ("System choice is a whole-life decision",
    "Chilled water, VRF, packaged or split systems differ in capital cost, energy use, space and "
    "maintenance. We compare the realistic options for the building and its operator, not the "
    "one we always use."),
   ("Design responsibility", RESPONSIBILITY),
 ],
 "delivers": [
   ("Heating and cooling load calculations", "Zone-by-zone loads against stated design conditions, "
    "occupancy and internal gains."),
   ("Ventilation and fresh air design", "Fresh air, exhaust, toilet and kitchen extract and "
    "car-park ventilation to the applicable code."),
   ("Duct and pipe sizing", "Ductwork, chilled water and refrigerant pipe sizing with velocity and "
    "pressure criteria stated."),
   ("Plant and equipment selection", "AHU, FCU, chiller, VRF and pump duties, with equipment "
    "schedules."),
   ("HVAC schematics and drawings", "System schematics, plant-room layouts and coordinated ductwork "
    "and pipework drawings in Revit."),
   ("Smoke control design input", "Smoke extraction ductwork and equipment design to the fire "
    "strategy; specialist smoke analysis where separately scoped."),
 ],
 "inputs": [
   "Architectural model or plans with ceiling heights and room uses",
   "Design conditions, occupancy and operating hours — or the standard to apply",
   "Fire strategy for smoke control and damper requirements",
   "Energy or sustainability targets, if any",
   "Preferred system types or client standards",
 ],
 "process": DESIGN_PROCESS,
 "autos": [
   ("Load-to-model reconciliation", "live", "Modelled terminal airflows compared with calculated "
    "loads, zone by zone."),
   ("Velocity and pressure checks", "live", "Duct and pipe runs tested against the stated design "
    "criteria before issue."),
 ],
 "nots": [
   "CFD and dynamic thermal simulation are separate specialist scopes.",
   "We do not commission, test or balance systems on site.",
   "Local stamping and authority approval stay with the engineer of record where required.",
 ],
 "faqs": [
   ("Do you carry out heating and cooling load calculations?",
    "Yes. Zone-by-zone loads to ASHRAE, CIBSE or the method the project names, with design "
    "conditions and assumptions stated on the output."),
   ("Can you design VRF and chilled water systems?",
    "Yes — chilled water, VRF/VRV, packaged and split systems, with a comparison of the realistic "
    "options for your building."),
   ("Do you design car-park and smoke extract ventilation?",
    "We design car-park ventilation and smoke extract ductwork to the fire strategy. Specialist "
    "smoke modelling is a separate scope we arrange where needed."),
 ],
 "related": [
   ("services/mep-design-services.html", "MEP engineering design", "All four disciplines together."),
   ("services/hvac-bim-services.html", "HVAC BIM", "Modelling an HVAC design you already have."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where the HVAC design meets everything else."),
 ],
 "prefill": "hvac_design",
},

# ---------------------------------------------------------------------------
{
 "slug": "plumbing-design-services",
 "nav": "Plumbing design",
 "h1": "Plumbing and drainage design services",
 "title": "Plumbing Design Services | Water Supply &amp; Drainage | BIMRACE",
 "desc": "Plumbing design for buildings: water demand and pipe sizing, hot water, drainage and "
         "stormwater design, pump and tank sizing, risers and coordinated plumbing drawings.",
 "eyebrow": "Plumbing design",
 "lede": "Water supply and drainage designed from fixture units and falls — the discipline that "
         "cannot be rerouted around a problem, designed first so it never has to be.",
 "codes": ["PL-11", "PL-13", "PL-16", "PL-17", "PL-18"],
 "meta": [("Discipline", "Plumbing"), ("Status", "Live"),
          ("Systems", "Water supply · Hot water · Drainage · Stormwater"),
          ("Output", "Sizing calcs · Risers · Schedules · Drawings")],
 "position": [
   ("Gravity is not negotiable",
    "Drainage needs fall, access and fixed connection levels. Designing it first — and reserving "
    "stack and riser positions with the architect — is what avoids pumped drainage and dropped "
    "ceilings later."),
   ("Sized to the method, not to habit",
    "Water demand and drainage flows are calculated with the loading-unit or fixture-unit method "
    "the project's code requires, and the method is stated on every calculation."),
   ("Design responsibility", RESPONSIBILITY),
 ],
 "delivers": [
   ("Water demand and pipe sizing", "Cold and hot water demand, pipe sizing, pressure and "
    "boosting requirements."),
   ("Drainage design", "Soil, waste and vent, sanitary drainage and stormwater design with falls "
    "and access points."),
   ("Tanks, pumps and hot water", "Storage tank, pump and hot-water plant sizing and schedules."),
   ("Water reuse", "Rainwater harvesting, greywater and recycled-water system design where "
    "required."),
   ("Plumbing schematics and risers", "Riser diagrams and schematics for every system."),
   ("Coordinated plumbing drawings", "Layouts, plant rooms and sections drawn in Revit."),
 ],
 "inputs": [
   "Architectural model with sanitary layouts and room data",
   "Occupancy and fixture schedule, or the basis to derive one",
   "Connection points, invert levels and mains water pressure",
   "The plumbing code the project must comply with",
   "Water reuse or sustainability targets, if any",
 ],
 "process": DESIGN_PROCESS,
 "autos": [
   ("Fall and gradient validation", "live", "Modelled drainage gradients tested against the "
    "design falls."),
   ("Sizing reconciliation", "live", "Calculated pipe sizes compared with the model."),
 ],
 "nots": [
   "Drainage adoption applications and utility negotiations stay with the client's appointed party.",
   "CCTV survey of existing drainage is not included.",
   "Local stamping and authority approval stay with the engineer of record where required.",
 ],
 "faqs": [
   ("Which method do you use for plumbing sizing?",
    "The loading-unit or fixture-unit method required by the project's code — for example BS EN "
    "806/12056, IPC/UPC or India's National Building Code — stated on the calculation."),
   ("Do you design rainwater harvesting and greywater systems?",
    "Yes, including storage, treatment space allowance, pumps and distribution, where the project "
    "requires them."),
   ("Can you size water tanks and booster pumps?",
    "Yes. Storage, booster and transfer pump duties are calculated and scheduled."),
 ],
 "related": [
   ("services/mep-design-services.html", "MEP engineering design", "All four disciplines together."),
   ("services/plumbing-public-health-bim.html", "Plumbing BIM", "Modelling an existing plumbing design."),
   ("services/fire-protection-design-services.html", "Fire protection design",
    "Shared water storage and pump rooms."),
 ],
 "prefill": "plumbing_design",
},

# ---------------------------------------------------------------------------
{
 "slug": "electrical-design-services",
 "nav": "Electrical design",
 "h1": "Electrical design services",
 "title": "Electrical Design Services | Power, Lighting &amp; SLD | BIMRACE",
 "desc": "Electrical design for buildings: load assessment, power distribution, single-line "
         "diagrams, lighting design, containment and coordinated electrical drawings.",
 "eyebrow": "Electrical design",
 "lede": "Power and lighting designed from the load assessment up, with distribution, containment "
         "and switch rooms sized before they are squeezed into the space that is left.",
 "codes": ["EL-02", "EL-03", "EL-04", "EL-12", "EL-13", "EL-14"],
 "meta": [("Discipline", "Electrical"), ("Status", "Live"),
          ("Systems", "Power · Lighting · Distribution · ELV containment"),
          ("Output", "Load schedules · SLD · Layouts · Drawings")],
 "position": [
   ("The load assessment sets everything downstream",
    "Connected and maximum demand decide the incoming supply, transformer and switchgear, and "
    "therefore the size of the electrical rooms. We establish it first and keep it current as the "
    "other disciplines' equipment changes."),
   ("Switch rooms are a spatial commitment",
    "Boards, their working space and the containment arriving at them need dimensioned rooms and "
    "risers. Designing those in the model avoids the late discovery that the room no longer fits."),
   ("Design responsibility", RESPONSIBILITY),
 ],
 "delivers": [
   ("Electrical load assessment", "Connected and maximum demand, diversity and supply "
    "requirements."),
   ("Single-line diagrams and distribution design", "Distribution strategy, single-line "
    "diagrams, board and panel schedules."),
   ("Lighting design", "General and emergency lighting layouts to the required illuminance."),
   ("Small power and containment", "Power layouts, cable tray and containment routes."),
   ("Earthing and lightning protection", "Earthing, bonding and lightning protection layouts."),
   ("Coordinated electrical drawings", "Layouts, risers and switch rooms drawn in Revit."),
 ],
 "inputs": [
   "Architectural model with room uses and ceiling plans",
   "Mechanical and plumbing equipment loads, or the basis to estimate them",
   "Incoming supply arrangement and utility requirements",
   "Lighting criteria, or the standard to apply",
   "The wiring regulations the project must comply with",
 ],
 "process": DESIGN_PROCESS,
 "autos": [
   ("Schedule reconciliation", "live", "Panel schedules compared with modelled circuits."),
   ("Working space rules", "live", "Clearance around switchgear and boards tested as a rule."),
 ],
 "nots": [
   "Protection coordination, short-circuit and arc-flash studies are specialist scopes agreed "
   "separately.",
   "We do not test, inspect or certify installations on site.",
   "Local stamping and authority approval stay with the engineer of record where required.",
 ],
 "faqs": [
   ("Do you prepare single-line diagrams and load schedules?",
    "Yes — the load assessment, distribution strategy, single-line diagrams and panel schedules "
    "are core electrical design deliverables."),
   ("Do you do lighting design?",
    "Yes, general and emergency lighting layouts to the illuminance and standard the project "
    "requires."),
   ("Which wiring regulations do you design to?",
    "The project's — for example IEC 60364, BS 7671, the NEC or India's IS 732 and National "
    "Building Code."),
 ],
 "related": [
   ("services/mep-design-services.html", "MEP engineering design", "All four disciplines together."),
   ("services/electrical-bim-services.html", "Electrical BIM", "Modelling an electrical design you have."),
   ("services/hvac-design-services.html", "HVAC design", "The largest electrical loads in most buildings."),
 ],
 "prefill": "electrical_design",
},

# ---------------------------------------------------------------------------
{
 "slug": "fire-protection-design-services",
 "nav": "Fire protection design",
 "h1": "Fire protection and sprinkler design services",
 "title": "Fire Protection &amp; Sprinkler Design Services | BIMRACE",
 "desc": "Fire protection design for buildings: sprinkler, hydrant, wet riser and hose reel "
         "design, hydraulic calculations, fire pump and tank sizing and coordinated drawings.",
 "eyebrow": "Fire protection design",
 "lede": "Sprinkler and hydrant systems designed to the hazard class and code, hydraulically "
         "calculated, and laid out in the model against the real ceiling.",
 "codes": ["FP-01", "FP-04", "FP-05", "FP-08", "FP-13", "FP-16"],
 "meta": [("Discipline", "Fire protection"), ("Status", "Live"),
          ("Systems", "Sprinkler · Hydrant · Wet riser · Pumps"),
          ("Output", "Hydraulic calcs · Layouts · Schedules · Drawings")],
 "position": [
   ("Hazard class first",
    "Head spacing, design density and water supply all follow from the hazard classification and "
    "the code the project names. Nothing is laid out until those are fixed."),
   ("Hydraulics decide the pump room",
    "Hydraulic calculations set pump duties and tank volumes, which set the size of the fire pump "
    "room. Calculating early keeps that room from being an afterthought."),
   ("Design responsibility", RESPONSIBILITY + " Fire alarm and detection are electrical/ELV "
    "scope unless included."),
 ],
 "delivers": [
   ("Sprinkler system design", "Wet, dry and pre-action sprinkler design to the hazard class."),
   ("Hydrant, wet riser and hose reel design", "Hydrant networks, risers, landing valves and hose "
    "reels."),
   ("Hydraulic calculations", "Pipe sizing and hydraulic calculations for the most demanding area."),
   ("Fire pumps and water storage", "Pump duties, tank volumes and fire pump-room layout."),
   ("Fire protection schematics", "Riser diagrams and system schematics."),
   ("Coordinated fire protection drawings", "Layouts and sections drawn in Revit against the "
    "reflected ceiling plan."),
 ],
 "inputs": [
   "Fire strategy or the hazard classification to apply",
   "Architectural model with reflected ceiling plans and compartment lines",
   "Water supply arrangement and available pressure",
   "The fire protection code the project must comply with",
   "Insurer requirements, if any",
 ],
 "process": DESIGN_PROCESS,
 "autos": [
   ("Coverage and spacing rules", "live", "Head spacing and coverage tested against the hazard "
    "class across the model."),
   ("Obstruction checking", "live", "Distance to obstruction tested as a rule, not by eye."),
 ],
 "nots": [
   "We do not author the fire strategy; the fire engineer does.",
   "Fire alarm, detection and voice evacuation are separate electrical/ELV scopes.",
   "Local stamping, authority approval and system certification stay with the appointed "
   "professionals.",
 ],
 "faqs": [
   ("Do you carry out sprinkler hydraulic calculations?",
    "Yes — pipe sizing and hydraulic calculations to the code the project names, such as NFPA 13, "
    "BS EN 12845 or India's NBC Part 4."),
   ("Do you design fire pump rooms?",
    "Yes, including pump duties, tank volumes, the pump-room layout and its coordination."),
   ("Does fire protection design include fire alarms?",
    "No. Fire alarm and detection are electrical/ELV scope and can be added as a separate item."),
 ],
 "related": [
   ("services/mep-design-services.html", "MEP engineering design", "All four disciplines together."),
   ("services/fire-protection-bim-services.html", "Fire protection BIM",
    "Modelling a fire protection design you have."),
   ("services/plumbing-design-services.html", "Plumbing design", "Shared tanks and pump rooms."),
 ],
 "prefill": "fire_design",
},
]
