"""
BIMRACE — service landing page content.

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    The service list follows the BIMRACE Building Sector Service
    Catalogue (the Excel workbook) and nothing else: nine service lines,
    in the catalogue's order. Each page's "Catalogue scope" table is
    generated from _catalogue.py, so a page cannot list a capability the
    catalogue does not carry.

    Nine pages, nine different arguments. A service page that is the
    previous service page with the discipline noun swapped is a doorway
    page. Each entry states an engineering position that is only true of
    that service: what goes wrong in it, what is delivered, what we need
    to start, where automation does and does not help, and what we will
    not do.

    The catalogue's scope boundary applies to every page: BIM modelling
    and coordination do not, by themselves, include engineering design,
    calculations, statutory compliance or professional approval. Those
    are provided only when included in the agreed scope and supported by
    appropriately qualified personnel.
"""
from _catalogue import CATALOGUE

# Each service:
#   slug, nav, h1, title (SEO), desc (meta), eyebrow, lede
#   codes     — catalogue code prefixes ("PL-") or exact codes ("ADD-03")
#   meta      — the phero definition list, 3-4 pairs
#   position  — [(heading, paragraph), ...] the argument, 2-3 blocks
#   delivers  — [(name, detail), ...] deliverables, the commercial core
#   inputs    — [str, ...] what we need from the client to start
#   process   — [(step_no, name, text), ...]
#   autos     — [(name, status, text), ...] where automation applies
#   nots      — [str, ...] scope boundary
#   faqs      — [(q, a), ...]
#   related   — [(href, title, blurb), ...]
#   prefill   — the contact form's lead_type value

DESIGN_SCOPE = ("Only where design responsibility is explicitly agreed and supported by "
                "qualified engineers.")

SERVICES = [

# ---------------------------------------------------------------------------
{
 "slug": "plumbing-public-health-bim",
 "nav": "Plumbing BIM",
 "h1": "Plumbing and drainage BIM services",
 "title": "Plumbing BIM Services | Water &amp; Drainage Models | BIMRACE",
 "desc": "Plumbing BIM modelling in Revit: cold and hot water, soil, waste and vent, stormwater, "
         "pump rooms, risers, shop drawings and plumbing quantities.",
 "eyebrow": "Plumbing BIM &amp; engineering",
 "lede": "The only discipline on the project that cannot be rerouted around a problem, because "
         "gravity is not negotiable — which makes it the one that should be routed first and "
         "almost never is.",
 "codes": ["PL-"],
 "meta": [("Discipline", "Plumbing"), ("Status", "Live"),
          ("Systems", "Water supply · Drainage · Stormwater · Pump rooms"),
          ("Output", "Revit model · Risers · Schedules · Shop drawings")],
 "position": [
   ("Gravity sets the sequence, so gravity should set the routing order",
    "A soil stack has one place it can be. A drainage run has a required fall, a maximum length "
    "before an access point, and a fixed invert at the connection. None of those are negotiable in "
    "the way a cable tray route is. On projects where drainage is routed after mechanical and "
    "electrical, the resolution is almost always a pumped solution nobody budgeted for, or a "
    "dropped ceiling nobody wanted. We route the gravity systems first."),
   ("Falls have to be modelled, not annotated",
    "A drainage run drawn flat with a note saying \"1:80 fall\" cannot be coordinated. It does not "
    "clash where it will actually be, and it does not tell you that the invert at the far end is "
    "below the slab. Modelling the fall is more work at authoring and very much less work at "
    "coordination, which is the same trade the rest of this practice is built on."),
   ("Connectivity is what makes the model checkable",
    "Plumbing is where broken connectivity hides most easily: a run that looks continuous in a 3D "
    "view but is three disconnected segments to the software. Authoring with connectivity intact "
    "is what lets a routine follow a run from fixture to connection and tell you it does not "
    "actually get there."),
 ],
 "delivers": [
   ("Water supply models", "Domestic cold water, hot water and circulation, and water "
    "distribution piping modelled in Revit with system assignment, risers and schedules."),
   ("Drainage models", "Soil, waste and vent, sanitary drainage, sewage and wastewater piping "
    "modelled with true falls, access points and connectivity intact."),
   ("Stormwater and water reuse", "Stormwater and rainwater drainage, rainwater harvesting, "
    "greywater and recycled-water distribution."),
   ("Pump rooms, tanks and basement drainage", "Plumbing pump-room and equipment-room models, "
    "tanks, pumps and valves, and basement drainage with sump-pump piping."),
   ("Risers, fixtures and schedules", "Riser diagrams and schematics, fixture and equipment "
    "layouts, and equipment schedules with connection details."),
   ("Shop drawings and quantities", "Plumbing shop drawings and installation layouts, with pipe "
    "quantities, material takeoffs and BOQ support."),
   ("Pipe sizing and hydraulic calculations", "Water demand, drainage flow and pipe sizing "
    "calculations. " + DESIGN_SCOPE),
 ],
 "inputs": [
   "Design drawings or consultant layouts — PDF, DWG or RVT",
   "Architectural model with sanitary layouts and room data",
   "Structural model with slab levels, foundations and shafts",
   "Connection points, invert levels and the water supply arrangement",
   "The plumbing standard, LOD/LOI and BIM requirements the project runs to",
 ],
 "process": [
   ("01", "Connection constraints", "Fix inverts, connection points and the levels the whole system "
    "has to work back from. Everything else is downstream of this."),
   ("02", "Stack and riser positions", "Agreed with the architect early, because they are the "
    "hardest thing on the project to move."),
   ("03", "Gravity routing", "Drainage modelled with true falls and access points at the required "
    "intervals."),
   ("04", "Pressurised systems", "Domestic water, boosting and hot water return, routed against "
    "the gravity systems already fixed."),
   ("05", "Coordination", "Federated testing against structure and the other services, with "
    "shaft and service-zone coordination."),
   ("06", "Documentation", "Plans, risers, schedules and shop drawings, issued with the QA rule "
    "set run."),
 ],
 "autos": [
   ("Connectivity and continuity checking", "live", "Every run traced from fixture to connection "
    "as a graph, so a visually continuous but disconnected system is caught at authoring rather "
    "than at coordination."),
   ("Fall and gradient validation", "live", "Modelled gradient tested against the required fall "
    "for the pipe size, run by run, with failures listed by element."),
   ("Access point spacing rules", "live", "Rodding and access point intervals tested as a rule "
    "along each run."),
   ("Quantity extraction", "live", "Pipe, fitting and fixture quantities measured from the model "
    "for takeoffs and BOQ support."),
 ],
 "nots": [
   "Pipe sizing and hydraulic calculations are not included unless explicitly scoped and supported "
   "by project inputs and qualified engineers.",
   "We do not carry out drainage adoption applications or negotiate with the adopting authority.",
   "We do not certify compliance with a jurisdiction's plumbing code; we model to the design and "
   "standard you name and your engineer of record certifies.",
 ],
 "faqs": [
   ("Can you model plumbing from PDF or CAD drawings?",
    "Yes. We develop native Revit plumbing models from PDF, DWG or consultant-issued drawings. "
    "Model accuracy depends on the completeness of the source information, which we review before "
    "modelling starts."),
   ("Do you model drainage with real falls?",
    "Yes, as a matter of course. A flat run with a fall annotation cannot be coordinated and will "
    "produce a coordination report that is wrong in the one discipline where being wrong is most "
    "expensive to fix."),
   ("Do you carry out pipe sizing and hydraulic calculations?",
    "Only where they are explicitly part of the agreed scope and supported by appropriate inputs "
    "and qualified engineers. By default we model the design information you provide."),
   ("What if the drainage connection level is not yet known?",
    "We model to a stated assumed invert and flag it as an assumption on the issue. What we will "
    "not do is pick a level quietly, because every run in the building is dimensioned back from it."),
 ],
 "related": [
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Gravity systems tested against structure and everything else."),
   ("services/quantity-takeoff-boq.html", "Quantity takeoff &amp; BOQ",
    "Pipe and fixture quantities measured from the model."),
   ("industries/healthcare.html", "Healthcare",
    "Where drainage, clearance and validation requirements are at their strictest."),
   ("industries/residential.html", "Residential and mixed use",
    "Repeated riser typologies — the ideal condition for rule-based checking."),
 ],
 "prefill": "plumbing_bim",
},

# ---------------------------------------------------------------------------
{
 "slug": "hvac-bim-services",
 "nav": "HVAC BIM",
 "h1": "HVAC BIM modelling services",
 "title": "HVAC BIM Services | Ductwork &amp; Plant Rooms | BIMRACE",
 "desc": "HVAC BIM modelling in Revit: ductwork, chilled and condenser water, VRF, ventilation, "
         "car-park and smoke extraction, plant rooms, shop drawings and HVAC takeoffs.",
 "eyebrow": "HVAC BIM &amp; engineering",
 "lede": "The discipline that usually decides how deep the ceiling void has to be — and therefore "
         "the one whose routing decisions everything else inherits.",
 "codes": ["HVAC-"],
 "meta": [("Discipline", "HVAC"), ("Status", "Live"),
          ("Systems", "Air · Chilled water · VRF · Ventilation"),
          ("Output", "Revit model · Plant rooms · Schedules · Shop drawings")],
 "position": [
   ("Duct depth is the constraint the rest of the project pays for",
    "Rectangular ductwork is the largest single object in most ceiling voids, it cannot be "
    "rerouted as cheaply as cable tray, and it is usually drawn last. The result is a familiar "
    "sequence: the void is set architecturally, the mechanical route does not fit, and the "
    "resolution is either a bulkhead nobody wanted or an aspect-ratio change nobody checked the "
    "consequence of. We resolve the primary mechanical route first, and treat every subsequent "
    "change to it as an engineering change rather than a drafting one."),
   ("Aspect ratio is an engineering decision, not a coordination workaround",
    "Flattening a duct to clear a beam changes its hydraulic diameter, its pressure drop and its "
    "fan duty. Done once it is invisible; done eleven times along a run it is a plant selection "
    "problem discovered at commissioning. We report those changes to the responsible engineer as "
    "they are made, which is the only point at which they are cheap to argue about."),
   ("Plant access is designed, not left over",
    "Coil pull space, filter access, damper access and tube pull are dimensioned requirements. They "
    "are also the requirements most often satisfied by whatever space happens to remain. We model "
    "them as clearance zones and test them as rules, so an access failure is a finding rather than "
    "an argument on site."),
 ],
 "delivers": [
   ("HVAC Revit models", "Supply, return, exhaust and fresh-air systems, toilet and kitchen "
    "exhaust, basement and car-park ventilation, modelled with system assignment and insulation."),
   ("Water-side and refrigerant piping", "Chilled-water, condenser-water and VRF/VRV refrigerant "
    "piping, with split, multi-split and ducted AC systems."),
   ("Plant rooms and equipment", "Chiller plant and mechanical plant-room models, cooling tower and "
    "pump-room coordination, AHU, FCU and FAHU equipment."),
   ("Smoke extraction modelling", "Mechanical smoke-control ductwork modelled and coordinated to "
    "the design supplied."),
   ("Risers, schematics and schedules", "HVAC riser diagrams, system schematics, equipment and "
    "technical schedules from Revit."),
   ("Shop drawings and quantities", "HVAC shop drawings and installation layouts, with duct, pipe "
    "and insulation takeoffs and BOQ support."),
   ("Loads, sizing and airflow calculations", "Heating and cooling loads, duct and pipe sizing, "
    "airflow and air-distribution schedules. " + DESIGN_SCOPE),
 ],
 "inputs": [
   "HVAC design drawings, schematics and equipment selections",
   "Architectural model or plans with ceiling heights and compartment lines",
   "Structural model or beam layouts — the depth constraint comes from here",
   "Selected plant data, if already procured",
   "The project BIM requirements, LOD/LOI and templates",
 ],
 "process": [
   ("01", "Design basis", "Confirm the HVAC design, equipment selections and criteria — supplied "
    "by your engineer, or calculated by us where that is explicitly in scope."),
   ("02", "Zoning", "Allocate the mechanical zone in the ceiling void and the riser allocation, "
    "and agree it with the other disciplines in writing."),
   ("03", "Primary distribution", "Route the largest ducts and mains first, against structure. "
    "Everything that follows is fitted to this, not the other way round."),
   ("04", "Terminals and equipment", "Place terminals, equipment and accessories, with tags and "
    "schedules populated from the model."),
   ("05", "Access and clearance", "Test coil pull, filter access, damper access and valve access "
    "as clearance rules across the whole model."),
   ("06", "Documentation", "Drawings, schedules and shop drawings issued with the QA rule set run."),
 ],
 "autos": [
   ("Duct and pipe parameter validation", "live", "Every run tested for size, system assignment, "
    "insulation and connectivity completeness before issue."),
   ("Clearance rule sets for plant access", "live", "Coil pull, filter and damper access tested as "
    "geometric rules across the federated model, not sampled by eye."),
   ("Quantity extraction", "live", "Duct, pipe and insulation quantities measured from the model "
    "for takeoffs and BOQ support."),
   ("Fan duty drift detection", "dev", "Accumulated pressure consequence of geometry changes along "
    "a run, reported as the change is made. In development on our own delivery."),
 ],
 "nots": [
   "Load calculations, duct and pipe sizing and specialist smoke-control analysis are not included "
   "unless design responsibility, inputs and qualified engineering resources are agreed.",
   "We do not perform CFD analysis, on-site commissioning or balancing.",
   "We do not certify compliance with a jurisdiction's mechanical code; your engineer of record "
   "certifies.",
 ],
 "faqs": [
   ("Which HVAC systems do you model?",
    "Ducted air systems, ventilation and exhaust, car-park ventilation, smoke-extract ductwork, "
    "chilled and condenser water piping, VRF/VRV refrigerant piping, split and ducted units, and "
    "mechanical plant rooms."),
   ("Do you calculate loads, or only model what we give you?",
    "By default we model to the HVAC design your engineer supplies, and we will tell you if the "
    "modelled network disagrees with it. Load calculations and sizing are offered only where they "
    "are explicitly in scope and supported by qualified engineers."),
   ("Can you produce HVAC shop drawings?",
    "Yes — installation layouts and shop drawings derived from the coordinated model. State the "
    "level of detail at enquiry stage, because it changes how the model is authored."),
   ("How do you handle a ceiling void that is too shallow?",
    "We report it as a finding with the options and their consequences — aspect ratio change, a "
    "bulkhead, a re-zoning, or a raised slab-to-slab. What we will not do is quietly flatten the "
    "duct until it fits."),
 ],
 "related": [
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where the mechanical route meets everyone else's."),
   ("services/bim-modelling-documentation.html", "MEP shop drawings",
    "Installation drawings derived from the coordinated model."),
   ("services/quantity-takeoff-boq.html", "Quantity takeoff &amp; BOQ",
    "Duct, pipe and insulation quantities from the model."),
   ("industries/data-centres.html", "Data centre MEP",
    "Where mechanical density and tolerance are at their most demanding."),
 ],
 "prefill": "hvac_bim",
},

# ---------------------------------------------------------------------------
{
 "slug": "fire-protection-bim-services",
 "nav": "Fire protection BIM",
 "h1": "Fire protection and sprinkler BIM services",
 "title": "Fire Protection BIM | Sprinkler &amp; Hydrant Models | BIMRACE",
 "desc": "Fire protection BIM in Revit: sprinkler, hydrant, wet riser, hose reel and fire pump-room "
         "models, ceiling-zone coordination, risers, shop drawings and fire protection BOQs.",
 "eyebrow": "Fire protection BIM &amp; engineering",
 "lede": "The discipline whose coordination failures are the most consequential and the most "
         "geometric — coverage is a spatial test, and a spatial test is something a rule set can "
         "actually run.",
 "codes": ["FP-"],
 "meta": [("Discipline", "Fire protection"), ("Status", "Live"),
          ("Systems", "Sprinkler · Hydrant · Wet riser · Hose reel · Suppression"),
          ("Output", "Revit model · Layouts · Schedules · Shop drawings")],
 "position": [
   ("Obstruction, not collision, is the failure mode",
    "A sprinkler head that does not clash with anything can still be useless. Coverage depends on "
    "distance to obstruction, deflector position relative to the ceiling and the obstruction rules "
    "for the hazard class — none of which a standard clash test looks at. Fire protection is the "
    "clearest example on any project of why clash detection and coordination are different "
    "activities."),
   ("Compartmentation is a model-wide constraint",
    "Every service that crosses a compartment line creates a penetration that needs a seal, a "
    "damper or both, and needs access to it. That only becomes visible when the compartment lines "
    "are in the federated model as geometry rather than in a fire strategy PDF."),
   ("Routing against structure is the recurring conflict",
    "In long-span structures the sprinkler main and the structural bracing want the same place, "
    "repeatedly and predictably. Because it is predictable, it is worth designing for at zoning "
    "stage rather than resolving eleven times at coordination stage."),
 ],
 "delivers": [
   ("Sprinkler system models", "Automatic, wet-pipe, dry-pipe and pre-action sprinkler systems "
    "modelled in Revit, with sprinkler head and equipment layouts."),
   ("Hydrant, riser and hose reel systems", "Fire hydrant piping networks, wet risers and "
    "standpipes, hose reels and fire department / breeching inlet arrangements."),
   ("Fire pump rooms and fire-water tanks", "Plant-room models and sections, with fire-water "
    "supply and distribution piping."),
   ("Special suppression layouts", "Clean-agent, kitchen hood, deluge and water-spray system "
    "layouts where applicable."),
   ("Risers, schedules and coordination", "Fire protection riser diagrams, valve, accessory and "
    "equipment schedules, and ceiling-zone coordination layouts."),
   ("Shop drawings and quantities", "Fire protection shop drawings with quantities and BOQ "
    "support."),
   ("Fire pipe sizing and hydraulic calculations", "Calculation reports. " + DESIGN_SCOPE),
 ],
 "inputs": [
   "Fire protection design drawings and system schematics",
   "Fire strategy, or the hazard classification and code named by the client",
   "Architectural reflected ceiling plans and compartment lines",
   "Structural model — bracing and long-span members drive the recurring conflict",
   "Equipment data for pumps, valves and suppression systems",
 ],
 "process": [
   ("01", "Hazard and standard", "Fix the classification and the standard the client names. Head "
    "spacing and obstruction rules follow from it and nothing can start without it."),
   ("02", "Compartmentation in the model", "Compartment lines brought into the federated model as "
    "geometry so penetrations become visible as findings rather than as a later discovery."),
   ("03", "Main routing", "Sprinkler mains and hydrant networks routed against structure at the "
    "same stage as the mechanical primary, not after it."),
   ("04", "Head layout", "Placed against the ceiling plan and tested for spacing and obstruction "
    "as a rule set."),
   ("05", "Coordination", "Federated testing, with obstruction and access treated as first-class "
    "findings alongside hard clashes."),
   ("06", "Documentation", "Layouts, risers, schedules and shop drawings issued with the QA rule "
    "set run."),
 ],
 "autos": [
   ("Coverage and spacing rule sets", "live", "Head spacing, wall distance and area per head tested "
    "geometrically against the stated hazard class across the whole model."),
   ("Obstruction checking", "live", "Distance to obstruction and deflector position tested as "
    "rules — the check a clash report structurally cannot perform."),
   ("Compartment penetration detection", "live", "Every service crossing a compartment boundary "
    "identified automatically and scheduled, across all disciplines."),
   ("Quantity extraction", "live", "Pipe, fitting, head and valve quantities measured from the "
    "model for BOQ support."),
 ],
 "nots": [
   "Fire alarm, detection and voice evacuation are electrical/ELV scopes, not part of fire "
   "suppression modelling, unless expressly included.",
   "Hydraulic calculations are provided only when explicitly scoped and supported by qualified "
   "engineers.",
   "We do not author the fire strategy, issue system certificates or obtain authority approval; "
   "those remain with the appointed fire engineer and licensed professionals.",
 ],
 "faqs": [
   ("Does fire protection BIM include fire alarm systems?",
    "No. Fire alarm and detection are treated as electrical/ELV scope. They can be added as a "
    "separate, explicitly defined scope item on the electrical side."),
   ("Do you design the sprinkler system or model someone else's design?",
    "We model to the design, hazard class and standard supplied. Hydraulic calculations are "
    "available only where explicitly agreed with qualified engineers; the fire engineer remains "
    "responsible for the strategy and certification."),
   ("Will the model be approved by the fire authority?",
    "We do not provide statutory approval. Submissions and approvals remain with the project's "
    "appointed designers and licensed professionals; our models and drawings support that process."),
   ("Is this useful before the ceiling design is fixed?",
    "The main routing is. Head layout is not, because it is entirely determined by the reflected "
    "ceiling plan and will be redone. We would rather sequence it correctly than bill for work "
    "that gets thrown away."),
 ],
 "related": [
   ("services/electrical-bim-services.html", "Electrical BIM",
    "Where fire alarm and detection layouts sit, as a separate scope."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where obstruction and access are separated from hard clashes."),
   ("industries/industrial.html", "Industrial and warehousing",
    "Long-span structures where fire protection against structure is the recurring conflict."),
   ("industries/hospitality.html", "Hospitality",
    "Finish-critical ceilings where head position is an architectural negotiation."),
 ],
 "prefill": "fire_protection_bim",
},

# ---------------------------------------------------------------------------
{
 "slug": "electrical-bim-services",
 "nav": "Electrical BIM",
 "h1": "Electrical BIM modelling services",
 "title": "Electrical BIM Services | Lighting &amp; Power | BIMRACE",
 "desc": "Electrical BIM in Revit: lighting and power layouts, cable tray and containment, panel "
         "and switchgear rooms, risers, single-line diagrams, panel schedules and electrical BOQs.",
 "eyebrow": "Electrical BIM &amp; engineering",
 "lede": "The discipline with the most flexible routes and the least respected space allocation — "
         "which is exactly why its coordination failures surface last and cost most.",
 "codes": ["EL-"],
 "meta": [("Discipline", "Electrical"), ("Status", "Live"),
          ("Systems", "Lighting · Power · Containment · Panel rooms · ELV"),
          ("Output", "Revit model · Schedules · Diagrams · Shop drawings")],
 "position": [
   ("Containment is treated as infinitely flexible until it is not",
    "Cable tray can go almost anywhere, so on most projects it goes wherever is left. That works "
    "until the cumulative result is a tray route with eleven changes of level, no maintained "
    "separation from the chilled water above it, and no clear access for cable pulling. We "
    "allocate the containment zone at the same time as the mechanical zone, and test the "
    "separation requirement as a rule rather than as an instruction in a specification."),
   ("Circuit data belongs on the element",
    "A cable tray drawn as a generic object is a rectangle. A cable tray carrying its circuits and "
    "its segregation class is a thing the model can be asked about — including whether the route "
    "it was given still satisfies the segregation requirement after three rounds of coordination "
    "moved it. The difference is entirely in how it was authored."),
   ("Distribution boards are a spatial commitment",
    "A board schedule that fits on a page can still fail when the board, its working space and the "
    "containment arriving at it are put in a riser cupboard dimensioned from an earlier revision. "
    "We model the working space as a clearance zone, because that is the only form in which a "
    "checking routine can test it."),
 ],
 "delivers": [
   ("Electrical Revit models", "Lighting fixture layouts, general and emergency lighting, and small "
    "power and socket layouts modelled in Revit."),
   ("Conduit, cable tray and containment", "Conduit, cable tray, trunking and ladder layouts, with "
    "cable routing and containment coordinated against other services."),
   ("Panels, switch rooms and equipment rooms", "Distribution board and panel placement, "
    "switchgear, panel-room, transformer and electrical equipment-room models."),
   ("Risers, single-line diagrams and schedules", "Electrical riser diagrams, single-line and "
    "schematic documentation, circuiting and panel schedules."),
   ("Earthing and lightning protection", "Earthing and bonding layouts and lightning protection "
    "system modelling."),
   ("ELV, fire alarm, data and security", "ELV containment, fire alarm and detection layouts, and "
    "data, telecom and security device layouts — each as a separately defined scope."),
   ("Shop drawings and quantities", "Electrical shop drawings and installation layouts, with "
    "quantities and BOQs. Load schedules and calculations: " + DESIGN_SCOPE.lower()),
 ],
 "inputs": [
   "Electrical design drawings, schematics and single-line diagrams",
   "Architectural model with ceiling plans and riser locations",
   "Structural model — penetrations and beam depths govern tray routes",
   "Lighting and equipment data where available",
   "Segregation and containment standards the project runs to",
 ],
 "process": [
   ("01", "Design basis", "Confirm the distribution strategy, single-line diagram and load "
    "schedule supplied by the electrical engineer."),
   ("02", "Zoning", "Containment zone in the void and riser allocation, agreed alongside "
    "mechanical rather than after it."),
   ("03", "Primary containment", "Main tray and busbar routes set against structure and "
    "mechanical, with separation designed in."),
   ("04", "Final circuits and outlets", "Lighting, small power and specialist systems placed "
    "against the architectural layouts."),
   ("05", "Working space and access", "Board clearance and pulling access tested as clearance "
    "rules."),
   ("06", "Schedules and issue", "Panel schedules, risers and shop drawings derived from model "
    "state, with the QA rule set run."),
 ],
 "autos": [
   ("Segregation and separation checking", "live", "Minimum separation between containment classes "
    "and between electrical and wet services tested geometrically across the federated model."),
   ("Circuit and parameter completeness", "live", "Every element tested for rating, circuit "
    "reference and classification before issue."),
   ("Board working space rules", "live", "Clearance in front of and around distribution equipment "
    "tested as a rule, including where an architectural change has since encroached on it."),
   ("Schedule reconciliation", "live", "Panel schedule against modelled circuits, so the two "
    "cannot silently disagree."),
 ],
 "nots": [
   "Specialist calculations — cable sizing, fault level, protection coordination, short circuit and "
   "arc flash — require explicit scope and suitably qualified engineering resources.",
   "Fire alarm, data, telecom and security are separate scope items, included only when defined.",
   "We do not issue electrical certificates, perform site testing or sign off compliance with a "
   "national wiring regulation.",
 ],
 "faqs": [
   ("Do you produce panel schedules from the model?",
    "Yes. Deriving them from model state rather than maintaining a parallel spreadsheet removes the "
    "most common source of drift between the electrical drawings and the electrical schedule."),
   ("Do you model ELV and fire alarm systems?",
    "Yes, as separately defined scope items: ELV containment, fire alarm and detection layouts, and "
    "data, telecom and security device and containment layouts."),
   ("Can you produce single-line diagrams?",
    "We prepare single-line and schematic documentation from the engineer's design. Electrical "
    "calculations and protection studies are provided only where explicitly scoped."),
   ("Can you route containment if the mechanical model is not finished?",
    "We can start, but the sequence matters. Containment routed before the primary mechanical "
    "distribution is fixed will be re-routed, because ductwork has far less freedom."),
 ],
 "related": [
   ("services/hvac-bim-services.html", "HVAC BIM",
    "The discipline that sets the zone containment has to work around."),
   ("services/fire-protection-bim-services.html", "Fire protection BIM",
    "Suppression systems, kept separate from fire alarm scope."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Separation and access tested as rules, not read off sections."),
   ("industries/commercial.html", "Commercial and offices",
    "Tenant variation and repeated coordination cycles."),
 ],
 "prefill": "electrical_bim",
},

# ---------------------------------------------------------------------------
{
 "slug": "bim-coordination-clash-detection",
 "nav": "BIM coordination &amp; clash detection",
 "h1": "BIM coordination and clash detection services",
 "title": "BIM Coordination &amp; Clash Detection Services | BIMRACE",
 "desc": "Federated architectural, structural and MEP models, hard and soft clash detection, "
         "clash reports with viewpoints, issue tracking and coordinated MEP model revisions.",
 "eyebrow": "BIM coordination",
 "lede": "Clash detection produces a number. Coordination produces a decision — what actually "
         "conflicts, why, whose model has to move, and evidence that it did.",
 "codes": ["BIM-"],
 "meta": [("Status", "Live"), ("Input", "Architectural, structural and MEP models"),
          ("Output", "Clash reports · Issue log · Coordinated model"),
          ("Formats", "RVT · NWC/NWD · BCF · PDF/XLSX")],
 "position": [
   ("A clash count is not a coordination report",
    "Eleven thousand clashes is not information. Most of it is insulation touching insulation, the "
    "same duct counted against forty hangers, and two disciplines that were never going to "
    "conflict in reality. A report nobody can act on is worse than no report, because it consumes "
    "the time that should have gone into the two hundred findings that matter. We group, "
    "prioritise and classify before anything is issued."),
   ("Most coordination failures are not collisions",
    "The parts do not touch; they just cannot be installed in that order, or maintained afterwards, "
    "or reached at all. Soft clashes — clearance, access and maintainability — do not appear in a "
    "hard clash test, and on a services-dense project they outnumber true clashes. We test them as "
    "explicit rule sets that a client can review and disagree with."),
   ("The issue history is a deliverable",
    "Why a duct moved in March is usually in someone's inbox. The next stage inherits the geometry "
    "without the reasoning and re-litigates it. Our coordination appointments produce an auditable "
    "record — finding, cause, decision, who accepted it, and the re-test that proved it closed."),
 ],
 "delivers": [
   ("Federated models", "Architectural, structural and MEP models federated on shared coordinates, "
    "with Navisworks NWC/NWD coordination models prepared as agreed."),
   ("Hard and soft clash detection", "Hard clash, clearance, access and maintainability reviews, "
    "including MEP-versus-structure and MEP-versus-architecture analysis."),
   ("Clash reports and matrix", "Clashes grouped, prioritised and classified in a clash matrix, "
    "reported with screenshots and viewpoints as PDF or Excel."),
   ("Issue tracking", "Clash issue logs and status reporting, with BCF exchange where the project "
    "platform supports it, and coordination meeting action logs."),
   ("Clash resolution and model revision", "Duct, pipe, cable tray and ceiling coordination, with "
    "updated models and a closure report where resolution is in our scope."),
   ("Model QA/QC and audits", "Model QA/QC, standards checks, audit reports, worksharing and "
    "linked-model support, and BEP/standards implementation."),
 ],
 "inputs": [
   "Discipline models (RVT/IFC) or drawings to be modelled",
   "Shared coordinates and model origin",
   "Clash rules, tolerances and priorities — or ours, if none are stated",
   "The BEP or coordination procedure the project runs to, if any",
   "The issue tracking environment the project uses, if one is mandated",
 ],
 "process": [
   ("01", "Federation strategy", "Agree what is federated, how often, on what coordinates, and who "
    "is responsible for each model. Most coordination problems are actually federation problems."),
   ("02", "Rule set definition", "Write the clash, clearance and access rules down and have the "
    "project agree them before the first run."),
   ("03", "Model health check", "Every received model checked for coordinates, units, naming and "
    "parameter completeness before it enters the federation."),
   ("04", "Test and classify", "Run the rule sets, then group, prioritise and classify by cause "
    "and responsible discipline rather than presenting a raw count."),
   ("05", "Resolve and record", "Route findings, track decisions, record who accepted what."),
   ("06", "Re-test and evidence", "Close nothing without a re-test that proves it."),
 ],
 "autos": [
   ("Rule-based clash and clearance testing", "live", "Hard clash, clearance and access run as "
    "defined rule sets across the federated model on every cycle."),
   ("Classification by cause", "live", "Findings clustered so that one template error producing "
    "two hundred findings is reported as one cause, not two hundred tickets."),
   ("Model health checking on receipt", "live", "Coordinates, units, naming, classification and "
    "parameter completeness tested on every incoming model."),
   ("Prioritisation and routing", "dev", "Severity and responsible-discipline assignment proposed "
    "automatically for review. In development, used on our own delivery."),
 ],
 "nots": [
   "Clash detection identifies coordination issues; it does not automatically authorise design "
   "changes or certify that a model is construction-compliant.",
   "We do not accept responsibility for another party's design decisions; the originating designer "
   "resolves.",
   "We do not close an issue without a re-test.",
 ],
 "faqs": [
   ("What is the difference between clash detection and BIM coordination?",
    "Clash detection is a geometric test that produces findings. Coordination is the process of "
    "deciding what those findings mean, who resolves them, and evidencing that they closed."),
   ("What is the difference between a hard and a soft clash?",
    "A hard clash is a physical intersection between elements. A soft clash is a breach of a "
    "required clearance — access, insulation or maintenance space — even where elements do not "
    "touch."),
   ("Which clash workflow and tools do you use?",
    "Revit models coordinated through Navisworks NWC/NWD files, with BCF issue exchange where the "
    "project platform supports it. Where a project mandates a different environment we work in it."),
   ("Can you coordinate models authored by other consultants?",
    "Yes — that is the normal case. We check each model's health on receipt and will report where "
    "an incoming model is not in a state that can be coordinated."),
 ],
 "related": [
   ("services/bim-modelling-documentation.html", "MEP shop drawings",
    "Drawings derived from the coordinated model."),
   ("services/fire-protection-bim-services.html", "Fire protection BIM",
    "The clearest case for separating obstruction from collision."),
   ("services/revit-services.html", "Revit modelling",
    "Clean, correctly located models — the precondition for coordination."),
   ("industries/data-centres.html", "Data centres",
    "Tolerance coordination at the highest services density."),
 ],
 "prefill": "bim_coordination",
},

# ---------------------------------------------------------------------------
{
 "slug": "bim-modelling-documentation",
 "nav": "MEP shop drawings &amp; documentation",
 "h1": "MEP shop drawings and BIM documentation services",
 "title": "MEP Shop Drawings &amp; BIM Documentation Services | BIMRACE",
 "desc": "MEP shop drawings and construction documentation from coordinated BIM: floor plans, "
         "installation layouts, sections, risers, builders' work and opening drawings, registers.",
 "eyebrow": "BIM documentation &amp; drawings",
 "lede": "Drawings are a view of the coordinated model, not a parallel deliverable — which is the "
         "only way a change stays one event instead of two.",
 "codes": ["DOC-"],
 "meta": [("Status", "Live"), ("Disciplines", "Plumbing · HVAC · FP · Electrical"),
          ("Output", "Shop drawings · Sections · Risers · Registers"),
          ("Formats", "PDF · DWG · RVT sheets · IFC")],
 "position": [
   ("Drawings are a view of the model, not a parallel deliverable",
    "Where drawings are drafted alongside the model, a change is two events and they eventually "
    "disagree. Where drawings are derived from model state, a change is one event. Getting to the "
    "second condition requires template, view and sheet discipline set up before authoring starts, "
    "which is why we do that first and will not skip it to save a week."),
   ("Builders' work has to be agreed before the slab is poured",
    "Penetrations, openings and cast-in items are the deliverable with the hardest deadline on the "
    "project and the one most often produced last. We take the coordinated model, extract every "
    "penetration, and issue it as a drawing and a schedule the structural engineer can review — "
    "before the pour, not as an RFI afterwards."),
   ("Level of detail is a scope decision",
    "Installation drawings need real fittings, real support positions and real clearances. A "
    "design-stage model does not hold those by default, so the level of development for shop "
    "drawings is agreed explicitly — it is the largest single driver of drawing cost."),
 ],
 "delivers": [
   ("General arrangements and MEP floor plans", "GA drawings and MEP floor plans issued as PDF "
    "and DWG sheets."),
   ("Installation layouts and details", "Detailed installation layouts, installation drawings, "
    "equipment installation and connection details."),
   ("Sections, risers and plant rooms", "Sections and sectional elevations, riser diagrams, and "
    "enlarged plant and equipment-room drawings."),
   ("Builders' work and openings", "Builders' work drawings, opening and penetration layouts and "
    "schedules."),
   ("Ceiling, shaft and service-zone coordination", "Reflected ceiling coordination plans, shaft "
    "and service-zone layouts."),
   ("Shop drawing packages and registers", "Issue-ready construction/shop drawing sets, drawing "
    "registers and revision schedules, with DWG and IFC exports where contracted."),
   ("As-built and record documentation", "As-built drawings from verified site information, and "
    "record-model and handover documentation support."),
 ],
 "inputs": [
   "Coordinated model, or design drawings to be modelled first",
   "Title block, sheet standards and naming conventions",
   "Equipment submittals and approved product data",
   "Issue status and approval workflow",
   "The structural engineer's review requirements for builders' work",
 ],
 "process": [
   ("01", "Sheet standards", "Title blocks, view templates, naming and the drawing register set up "
    "before any sheet is produced."),
   ("02", "Level of development", "Agree what has to be modelled to installation standard and what "
    "does not — the scope conversation, made explicit."),
   ("03", "Coordinated basis", "Drawings produced only from the coordinated model, so they reflect "
    "the resolved position of services."),
   ("04", "Builders' work", "Penetrations and openings extracted, dimensioned and scheduled for "
    "structural review."),
   ("05", "Production", "Plans, sections, risers, details and shop drawing sheets derived from "
    "model state."),
   ("06", "Issue", "Issued under revision control with the drawing register updated."),
 ],
 "autos": [
   ("Penetration extraction", "live", "Every service crossing a structural element identified and "
    "scheduled automatically across the federated model."),
   ("Drawing and schedule generation", "live", "Views, sheets and schedules derived from model "
    "state as a routine rather than drafted."),
   ("Naming and register checking", "live", "Sheets and views tested against the project naming "
    "convention, and the register reconciled against issued sheets."),
   ("Support layout routines", "dev", "Generating bracket and support positions from routing and "
    "rules, for review. In development on our own delivery."),
 ],
 "nots": [
   "Shop drawing review and approval follow the project's contract and client process.",
   "Typical mounting and support details are prepared subject to the project's design "
   "responsibility.",
   "As-built accuracy depends on verified site information; we state the verification status "
   "rather than certify what we have not received.",
 ],
 "faqs": [
   ("Are shop drawings produced from the model or drafted separately?",
    "From the model. Plans, sections and details are generated from the coordinated Revit model so "
    "drawings reflect the coordinated position of services."),
   ("Can you work to our title block and drawing standards?",
    "Yes. We set up sheets, view templates and naming to your standards or the project's BIM "
    "requirements."),
   ("Do you produce builders' work drawings?",
    "Yes. Penetration extraction from the coordinated model is automated, and the output is a "
    "dimensioned drawing plus a schedule the structural engineer can review."),
   ("Can you deliver DWG and IFC as well as PDF?",
    "Yes, where contracted. The export settings and layer or IFC mapping are agreed at the start."),
 ],
 "related": [
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "The coordinated model every drawing is derived from."),
   ("services/revit-services.html", "Revit modelling",
    "Templates, view setup and sheet standards."),
   ("services/as-built-bim-services.html", "As-built &amp; existing-building BIM",
    "Record models and handover after construction."),
   ("industries/commercial.html", "Commercial and offices",
    "Repeated coordination and documentation cycles."),
 ],
 "prefill": "bim_documentation",
},

# ---------------------------------------------------------------------------
{
 "slug": "quantity-takeoff-boq",
 "nav": "Quantity takeoff &amp; BOQ",
 "h1": "MEP quantity takeoff and BOQ services",
 "title": "MEP Quantity Takeoff &amp; BOQ Services | BIMRACE",
 "desc": "Model-based MEP quantity takeoffs, Revit material schedules, Excel takeoffs and BOQ "
         "preparation from approved design information, with revision comparison reports.",
 "eyebrow": "Quantity takeoff, schedules &amp; BOQ",
 "lede": "A quantity is only as good as the rule that measured it. Ours state the rule, the source "
         "model and its version on every line.",
 "codes": ["QTO-"],
 "meta": [("Status", "Live"), ("Disciplines", "Plumbing · HVAC · FP · Electrical"),
          ("Output", "Takeoffs · Schedules · BOQ · Change reports"),
          ("Formats", "XLSX · PDF · Revit schedules")],
 "position": [
   ("A takeoff is not a BOQ, and a BOQ is not a price",
    "Measured quantities from a model answer \"how much is drawn\". A bill of quantities answers "
    "\"how much is to be built, under which measurement rules, with which allowances\". Pricing is "
    "a third question again. We keep the three separate on paper, because blurring them is how a "
    "takeoff ends up treated as a commitment it never was."),
   ("The measurement rule has to travel with the number",
    "Is that pipe length measured centre-line through fittings or net between them? Are hangers "
    "counted, or allowed for? A quantity without its rule cannot be checked, compared or defended. "
    "Every takeoff we issue states the measurement rules, the exclusions, the allowances and the "
    "source model version."),
   ("Revisions are where quantities earn their keep",
    "The first takeoff is useful. The comparison between revision C and revision D is what a "
    "commercial team actually needs — what moved, by how much, and where. Model-based quantities "
    "make that comparison a routine rather than a re-measure."),
 ],
 "delivers": [
   ("Plumbing and fire protection takeoffs", "Pipe quantity takeoffs, fixtures, sprinkler heads, "
    "valves and equipment schedules."),
   ("HVAC takeoffs", "Duct, pipe and insulation quantities and HVAC equipment schedules."),
   ("Electrical takeoffs", "Cable tray and conduit quantities, lighting fixture and electrical "
    "equipment schedules."),
   ("Consolidated MEP workbook", "Revit material takeoff schedules and consolidated, Excel-based "
    "quantity schedules and model-based material lists."),
   ("BOQ preparation", "BOQ from approved design information, structured to your item "
    "descriptions, with procurement quantity support."),
   ("Revision comparison and change reports", "Quantity comparison between model revisions, "
    "variation and change reports."),
   ("Validation and registers", "Quantity validation, model completeness checks, drawing/model "
    "reconciliation, and equipment and asset registers."),
 ],
 "inputs": [
   "Revit model, or drawings to be modelled first",
   "The measurement standard or method to follow",
   "BOQ structure, item descriptions and exclusions",
   "Design revision and issue status of the source information",
   "Whether rates and pricing are in or out of scope",
 ],
 "process": [
   ("01", "Measurement basis", "Agree measurement rules, allowances, exclusions and the BOQ "
    "structure before anything is counted."),
   ("02", "Model completeness check", "Test that the elements to be measured exist, are classified "
    "and carry the parameters the takeoff depends on."),
   ("03", "Extraction", "Quantities extracted from the model by discipline, classified to the "
    "agreed structure."),
   ("04", "Reconciliation", "Model quantities reconciled against drawings, with discrepancies "
    "listed rather than absorbed."),
   ("05", "BOQ and workbook", "Consolidated workbook and BOQ issued with the measurement notes."),
   ("06", "Revision comparison", "Each new revision compared with the last and the changes "
    "reported."),
 ],
 "autos": [
   ("Quantity extraction", "live", "Measured from geometry and parameters, classified, with the "
    "measurement rule visible per line and traceable back to elements."),
   ("Completeness checking", "live", "Unclassified, unmeasurable or parameter-incomplete elements "
    "listed before the takeoff is issued."),
   ("Revision comparison", "live", "Quantities compared between model revisions and the "
    "differences reported by item."),
   ("Rate application", "road", "Applying a client rate library to measured quantities. Not "
    "offered today; pricing is excluded unless stated."),
 ],
 "nots": [
   "A model-based quantity takeoff is not automatically a priced BOQ; rates, wastage, labour and "
   "accessories are included only when agreed.",
   "Every takeoff states its measurement rules, exclusions, source model and version, and "
   "allowances — quantities issued without them are not issued.",
   "We do not certify quantities for contractual valuation.",
 ],
 "faqs": [
   ("Do your BOQs include rates and pricing?",
    "Not by default. We prepare quantities and BOQ structures; rates and pricing are included only "
    "when explicitly agreed."),
   ("Can you take off quantities without a Revit model?",
    "We can first model the systems from your drawings and then extract quantities, which also "
    "gives you a reusable model for later revisions."),
   ("Which measurement standard do you follow?",
    "The one the project names. We state it, with the allowances and exclusions, on every issue."),
   ("Can you compare quantities between design revisions?",
    "Yes — revision comparison and change reports are a standard deliverable, and usually the most "
    "useful one to a commercial team."),
 ],
 "related": [
   ("services/revit-services.html", "Revit modelling",
    "Parameters and families set up so quantities can be extracted."),
   ("services/plumbing-public-health-bim.html", "Plumbing BIM",
    "Pipe and fixture models behind the plumbing takeoff."),
   ("services/electrical-bim-services.html", "Electrical BIM",
    "Containment and equipment models behind the electrical takeoff."),
   ("industries/retail.html", "Retail",
    "Short programmes where fast, reliable quantities matter."),
 ],
 "prefill": "quantity_takeoff",
},

# ---------------------------------------------------------------------------
{
 "slug": "revit-services",
 "nav": "Revit modelling &amp; model management",
 "h1": "Revit modelling and model management services",
 "title": "Revit MEP Modelling &amp; Model Management | BIMRACE",
 "desc": "Revit MEP modelling and model management: CAD and PDF to Revit conversion, families, "
         "parameters, templates, worksharing, model audits and IFC exchange.",
 "eyebrow": "Revit modelling &amp; model management",
 "lede": "Most of what goes wrong in a Revit project was decided in the first week, in the "
         "template and the parameter schema, by someone who was told to start modelling.",
 "codes": ["REV-"],
 "meta": [("Status", "Live"), ("Scope", "Conversion · Content · Setup · Management"),
          ("Exchange", "IFC · Navisworks · Schedules"),
          ("Formats", "RVT · RFA · RTE · IFC")],
 "position": [
   ("The template is the cheapest lever on the whole project",
    "View templates, browser organisation, naming, shared parameters, worksets and the project "
    "parameter schema take days at the start and decide months of behaviour afterwards. Projects "
    "that skip them do not save the days — they spend them repeatedly, in smaller pieces, for the "
    "rest of the job, and end up with a model nothing can be extracted from."),
   ("Downloaded families are the most common cause of unqueryable data",
    "Manufacturer content is built to sell a product, not to satisfy your data schema. Dropped "
    "into a project and patched, it produces elements that look correct and schedule wrongly. We "
    "build parametric content against the project schema, which is more work once and less work "
    "permanently."),
   ("Conversion quality is decided by the source",
    "A Revit model converted from clean DWG layouts and one converted from a scanned PDF are "
    "different jobs at different prices. We review the source before quoting and say plainly what "
    "accuracy it can support."),
 ],
 "delivers": [
   ("CAD, PDF and drawing to Revit conversion", "2D drawings, PDF and DWG converted to native Revit "
    "models, including MEP models from consultant-issued design documents."),
   ("Families and content libraries", "Revit family creation and modification, MEP equipment and "
    "fixture families, and template and content library development."),
   ("Parameters, schedules and tags", "Shared-parameter setup, parameter mapping, schedules and "
    "tag configuration."),
   ("Templates, views and sheets", "View templates, sheet setup, and model browser and view "
    "organisation."),
   ("Model management", "Linked-model management and coordinates setup, model splitting and "
    "worksharing setup, revision and change incorporation."),
   ("Model audit and cleanup", "Model auditing and warnings review, cleanup and optimisation, and "
    "detailing to the agreed LOD/LOI."),
   ("Exchange and handover", "IFC export and model exchange preparation, and model handover "
    "packaging."),
 ],
 "inputs": [
   "Source drawings (DWG, PDF) or existing models",
   "Revit version and project template, if any",
   "LOD/LOI, naming and coordinate requirements",
   "The data you need to get out of the model at the end — this drives the schema",
   "Exchange and handover requirements",
 ],
 "process": [
   ("01", "Requirements first", "Agree LOD/LOI, coordinate system, naming, software version and "
    "exchange requirements, and design the parameter schema from what has to come out at handover."),
   ("02", "Source review", "Check the quality of the drawings or models being converted and state "
    "the accuracy they can support."),
   ("03", "Template and content", "Views, sheets, browser organisation, parameters and families "
    "built and tested before authoring."),
   ("04", "Authoring", "Modelling with the schema populated as elements are placed."),
   ("05", "Audit", "Warnings reviewed, model cleaned and checked against the agreed standard."),
   ("06", "Handover", "Model, content library and documentation packaged so your team can "
    "maintain it."),
 ],
 "autos": [
   ("Parameter update and management routines", "live", "Bulk parameter population and correction "
    "run as documented routines rather than by hand."),
   ("Naming and view organisation", "live", "Views, sheets and families named and organised against "
    "the project convention automatically."),
   ("Model checking routines", "live", "The project rule set run inside the authoring environment "
    "during production, not only before issue."),
   ("AI-assisted model interrogation", "dev", "Asking structured questions of model data — element "
    "counts by system, parameter completeness, where a family is used. In development; see the MCP "
    "for Revit page for what this would and would not involve."),
 ],
 "nots": [
   "LOD/LOI, coordinate systems, naming, software versions and exchange requirements are agreed per "
   "project; we do not promise a universal LOD.",
   "Model accuracy from PDF conversion depends on source quality, which we state before starting.",
   "We do not sell or resell Revit licences, and we are not an Autodesk partner.",
 ],
 "faqs": [
   ("Can you convert our CAD or PDF drawings to Revit?",
    "Yes. We review the source first and tell you what accuracy it supports — clean DWG converts "
    "very differently from scanned PDF."),
   ("Can you create custom MEP families?",
    "Yes. We create and modify equipment, fixture and accessory families with the parameters needed "
    "for scheduling and quantities."),
   ("Which Revit versions do you work in?",
    "Whichever the project mandates. Version has real consequences for exchange and handover, so we "
    "agree it at the start."),
   ("Can you set up a Revit project standard from scratch?",
    "Yes. Templates, shared parameters, naming, browser organisation, view templates, sheet "
    "standards and a starter content library, documented so your team can maintain it."),
 ],
 "related": [
   ("services/bim-modelling-documentation.html", "MEP shop drawings &amp; documentation",
    "The sheets the template exists to produce."),
   ("services/quantity-takeoff-boq.html", "Quantity takeoff &amp; BOQ",
    "What becomes possible once parameters are populated."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Linked models on correct coordinates, ready to federate."),
   ("technology/mcp-for-revit.html", "MCP for Revit",
    "What connecting an AI assistant to model data would actually require."),
 ],
 "prefill": "revit_modelling",
},

# ---------------------------------------------------------------------------
{
 "slug": "as-built-bim-services",
 "nav": "As-built &amp; existing-building BIM",
 "h1": "As-built, existing-building and handover BIM services",
 "title": "As-Built &amp; Existing Building BIM | BIMRACE",
 "desc": "As-built and existing-building MEP BIM models from verified site information, existing "
         "services documentation, asset registers, handover packages and specialist BIM support.",
 "eyebrow": "Additional building BIM services",
 "lede": "As-built means what was installed, not what was designed — and a record model is only "
         "as trustworthy as the verification behind it.",
 "codes": ["ADD-"],
 "meta": [("Status", "Live"), ("For", "Owners · Contractors · Facility teams"),
          ("Output", "Record model · Asset register · Handover package"),
          ("Basis", "Verified site information")],
 "position": [
   ("As-built means what was installed, not what was designed",
    "A record model that is the design model with a new title block is a liability dressed as a "
    "handover deliverable. We update against verified site information and state clearly what has "
    "been verified and what has not, because an operator who trusts an unverified record model will "
    "find out the hard way."),
   ("Existing buildings start with what can actually be verified",
    "Refurbishment and fit-out projects inherit services nobody has drawn accurately for years. "
    "Modelling them from old drawings without checking produces a confident model of the wrong "
    "building. We agree the verification responsibility first — survey, scan or marked-up site "
    "information — and model to it."),
   ("Handover is information, not a folder of files",
    "An owner needs to find the equipment, know what it is and know what was left open. Asset "
    "registers, a file index and a handover note listing assumptions and limitations are what make "
    "a model usable after the project team has gone."),
 ],
 "delivers": [
   ("As-built BIM models", "Record models developed from verified site information and marked-up "
    "as-installed drawings."),
   ("Existing-building models", "Existing-condition Revit models and existing MEP services "
    "documentation for refurbishment and fit-out."),
   ("Asset registers and handover", "Model-based handover and asset registers, with COBie/asset "
    "information preparation where the project requires it."),
   ("Space and equipment validation", "Model-based space and equipment validation reports."),
   ("Change impact and value engineering", "Design revision impact and quantity comparison, and "
    "MEP value-engineering coordination support."),
   ("BIM standards and workflow support", "BEP, templates and standards implementation support."),
   ("Specialist support", "Point-cloud / laser-scan-to-BIM, 4D construction sequencing and "
    "model-based progress visualisation, subject to specialist inputs and tools."),
 ],
 "inputs": [
   "Marked-up as-installed drawings and the coordinated design model",
   "Verified site information, survey or scan data",
   "Asset data requirements (e.g. COBie), if any",
   "Handover, file-naming and exchange requirements",
   "Who holds verification responsibility on site",
 ],
 "process": [
   ("01", "Verification responsibility", "Agree who verifies what on site, and in what form the "
    "information reaches us."),
   ("02", "Source assembly", "Collect the design model, mark-ups, survey or scan data and site "
    "records."),
   ("03", "Model update", "Update or build the model against verified information only."),
   ("04", "Status marking", "Record verification status element by element."),
   ("05", "Asset data", "Populate equipment and asset registers to the agreed schema."),
   ("06", "Handover", "Model, drawings, registers and a handover note with assumptions and "
    "limitations."),
 ],
 "autos": [
   ("Asset register extraction", "live", "Equipment and asset data extracted from the model into a "
    "structured register."),
   ("Model audit before handover", "live", "Warnings, naming and parameter completeness checked "
    "before the record model is issued."),
   ("Revision quantity comparison", "live", "Quantities compared between design and as-built "
    "revisions."),
   ("Scan-to-BIM and 4D workflows", "road", "Specialist workflows offered only after tools, inputs "
    "and requirements are confirmed for the project."),
 ],
 "nots": [
   "As-built accuracy depends on verified site information, survey or scan inputs and a defined "
   "verification responsibility.",
   "Point-cloud modelling, 4D sequencing and COBie data are specialist, project-specific scopes "
   "confirmed before we commit.",
   "We do not supervise or inspect installation on site.",
 ],
 "faqs": [
   ("Do you carry out site surveys?",
    "Site verification responsibility is defined per project. We model from the verified "
    "information supplied, and scan-based modelling is available as a specialist scope."),
   ("What makes an as-built model trustworthy?",
    "Stated verification status, element by element. A record model that does not distinguish "
    "between what was verified on site and what was carried over from design invites trust it has "
    "not earned."),
   ("Can you model an existing building's MEP services?",
    "Yes — existing-condition models and services documentation, from the drawings and site "
    "information available, with the accuracy each source supports stated."),
 ],
 "related": [
   ("services/bim-modelling-documentation.html", "MEP shop drawings &amp; documentation",
    "As-built drawings and record documentation."),
   ("services/revit-services.html", "Revit modelling",
    "Conversion and model management behind existing-building models."),
   ("services/quantity-takeoff-boq.html", "Quantity takeoff &amp; BOQ",
    "Asset registers and revision comparison."),
   ("industries/healthcare.html", "Healthcare",
    "Where verified handover information matters most to operators."),
 ],
 "prefill": "additional_bim",
},
]

# Where AI is used on each service. Prepended to the page's automation list so
# AI and automation are shown together, each line with its real status.
AI_USE = {
    "plumbing-public-health-bim": [
        ("AI-assisted drawing review", "live", "Plumbing drawings and schedules read to list fixtures, "
         "risers, falls and missing invert or connection data before modelling starts."),
        ("AI-assisted QA", "live", "Connectivity, slope and parameter findings grouped by cause and "
         "drafted for the modeller to fix, then re-checked."),
    ],
    "hvac-bim-services": [
        ("AI-assisted drawing review", "live", "HVAC layouts and equipment schedules read to extract "
         "systems, equipment and gaps before modelling."),
        ("AI-assisted clearance triage", "live", "Duct and plant clearance findings ranked by impact so "
         "the primary route is resolved first."),
    ],
    "fire-protection-bim-services": [
        ("AI-assisted drawing review", "live", "Fire protection schematics read to list systems, "
         "risers, valves and missing hazard or standard information."),
        ("AI-assisted coverage triage", "live", "Spacing and obstruction findings grouped by ceiling "
         "zone for the modeller and the fire engineer to review."),
    ],
    "electrical-bim-services": [
        ("AI-assisted drawing review", "live", "Electrical layouts, SLDs and panel schedules read to "
         "extract circuits, equipment and missing data."),
        ("AI-assisted schedule checking", "live", "Panel and equipment schedules compared against "
         "the model, with mismatches drafted as findings."),
    ],
    "bim-coordination-clash-detection": [
        ("AI clash grouping and prioritisation", "live", "Clashes clustered by cause and responsible "
         "discipline, ranked by impact, with issue descriptions drafted for the coordinator."),
        ("AI-drafted coordination reports", "live", "Clash reports and meeting action logs drafted "
         "from issue data and checked before issue."),
    ],
    "bim-modelling-documentation": [
        ("AI-assisted sheet checking", "live", "Sheets, tags, title blocks and registers checked "
         "against the drawing standard before issue."),
        ("AI-drafted registers and notes", "live", "Drawing registers, revision schedules and issue "
         "notes drafted from model data for review."),
    ],
    "quantity-takeoff-boq": [
        ("AI quantity reconciliation", "live", "Quantities reconciled between model and drawings, and "
         "between revisions, with anomalies flagged."),
        ("AI-assisted BOQ mapping", "live", "Measured items mapped to your BOQ descriptions for a "
         "quantity surveyor to confirm."),
    ],
    "revit-services": [
        ("AI-assisted CAD/PDF conversion", "live", "Source drawings read to identify systems, sizes and "
         "annotations before conversion, so the model starts from a checked list."),
        ("AI-assisted model audit", "live", "Warnings, naming and parameter gaps grouped by root cause "
         "so a template fix replaces hundreds of element fixes."),
    ],
    "as-built-bim-services": [
        ("AI-assisted mark-up reading", "live", "Marked-up as-installed drawings read to list the "
         "changes to apply to the record model."),
        ("AI-drafted asset registers", "live", "Equipment and asset registers drafted from model data "
         "and checked before handover."),
    ],
}
for _s in SERVICES:
    _s["autos"] = AI_USE[_s["slug"]] + _s["autos"]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


def catalogue_items(service):
    """The catalogue rows a service page lists, in catalogue order."""
    return [i for i in CATALOGUE
            if any(i["code"].startswith(c) if c.endswith("-") else i["code"] == c
                   for c in service["codes"])]


# Service pages that existed before the catalogue realignment. Each maps to the
# page that now carries its content, and build.py emits a 301 for it.
RETIRED = {
    "mep-engineering-services": "engineering.html",
    "bim-automation-services": "engineering.html",
    "construction-support-bim": "services/bim-modelling-documentation.html",
}
