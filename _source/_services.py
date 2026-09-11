"""
BIMRACE — service landing page content.

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    Ten pages, ten different arguments. A service page that is the
    previous service page with the discipline noun swapped is a doorway
    page, and Google is better at spotting those than we are at writing
    them. Each entry below states an engineering position that is only
    true of that service: what actually goes wrong in it, what is
    delivered, what we need to start, where automation does and does not
    help, and what we will not do.

    Nothing here may claim a capability the main site does not already
    carry a live badge for. The badge vocabulary is the same one in
    build.py: live / dev / road / demo.
"""

# Each service:
#   slug, nav_title, h1, title (SEO), desc (meta), eyebrow, lede
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
#   group     — which CAPS anchor on engineering.html this belongs to

SERVICES = [

# ---------------------------------------------------------------------------
{
 "slug": "mep-engineering-services",
 "nav": "MEP engineering",
 "h1": "MEP engineering design and BIM services",
 "title": "MEP Engineering &amp; BIM Services | BIMRACE",
 "desc": "MEP engineering design support and BIM delivery across mechanical, electrical, public "
         "health and fire protection, modelled as connected systems.",
 "eyebrow": "MEP engineering",
 "lede": "Mechanical, electrical, public health and fire protection engineered as one interacting "
         "set of systems rather than four models that happen to share a coordinate origin.",
 "meta": [("Disciplines", "M · E · P · FP"), ("Status", "Live"),
          ("Output", "Models · Drawings · Schedules · Calculations"),
          ("Standard", "ISO 19650 aligned")],
 "position": [
   ("MEP is a spatial problem before it is a calculation problem",
    "Sizing a duct is the part of MEP engineering that a competent graduate can do. Getting that "
    "duct through a structural zone, past a cable tray, above a ceiling that has already been set "
    "by the architect, with enough clearance left for someone to reach the fire damper in ten "
    "years' time, is the part that consumes the programme. We treat the two as one activity, "
    "because a size decided without the route is a size that will change."),
   ("Systems, not layers",
    "A model in which chilled water pipework is a collection of cylinders is not an engineering "
    "model. It is a drawing that happens to be three-dimensional. Ours are authored with system "
    "assignment, connectivity and design parameters populated during authoring, so that "
    "\"check the chilled water system\" is an instruction a machine can resolve rather than an "
    "instruction to open a view and look."),
   ("Where our accountability starts and stops",
    "BIMRACE provides engineering design and BIM delivery. Statutory approvals, authority "
    "submissions and the professional stamp belong to the licensed engineer of record on the "
    "project — your practice, or the local consultant you appoint. We are explicit about this "
    "because the alternative is a delivery model that quietly leaves a liability gap."),
 ],
 "delivers": [
   ("Discipline models", "Mechanical, electrical, public health and fire protection models "
    "authored to an agreed level of information need, with system assignment and design "
    "parameters carried on the elements."),
   ("Plant room and riser layouts", "Plant arrangement with maintenance and replacement access "
    "resolved, riser allocations by discipline, and builders work implications identified early "
    "rather than discovered on site."),
   ("Sizing and load calculations", "Heating and cooling loads, duct and pipe sizing, electrical "
    "load schedules and distribution calculations — reconciled against the as-modelled network so "
    "the calculation and the model cannot silently diverge."),
   ("Equipment schedules", "Plant, terminals and devices scheduled from the model with performance "
    "data attached, so a schedule change and a model change are the same event."),
   ("General arrangement drawings", "Plans, sections and details derived from the model, at the "
    "status codes the appointment requires."),
   ("Services zoning strategy", "Allocated horizontal and vertical zones per discipline, agreed "
    "before routing starts, which is what prevents coordination becoming a negotiation later."),
 ],
 "inputs": [
   "Architectural and structural models or drawings, at whatever stage they exist",
   "Design criteria, or the standard you want applied where criteria are not yet fixed",
   "Room data sheets or a schedule of accommodation, if available",
   "The EIR, BEP or BIM standard the project runs to — or ours, if there is none",
   "Ceiling and clearance constraints, and who owns them",
   "Programme, stage gates and the issue dates you are working to",
 ],
 "process": [
   ("01", "Scope and criteria", "We agree disciplines, level of information need, deliverable list "
    "and the design criteria before any authoring starts. Ambiguity at this point is the single "
    "most expensive thing on an MEP appointment."),
   ("02", "Model setup", "Templates, shared coordinates, naming, classification and the project "
    "parameter schema are established first. This is the unglamorous work that decides whether "
    "anything can be checked automatically later."),
   ("03", "Zoning and routing", "Spatial allocation per discipline, then primary distribution. "
    "Routes are tested against clearance and access rules as they are drawn, not after."),
   ("04", "Sizing and systems", "Calculations driven from the modelled network, with results "
    "written back to the elements so the model carries the engineering, not just the geometry."),
   ("05", "Coordination", "Federation with the other disciplines, clash and clearance testing, "
    "resolution tracked to closure with the decision recorded."),
   ("06", "Documentation and issue", "Drawings and schedules derived from model state, QA rule set "
    "run before issue, and a named engineer signs."),
 ],
 "autos": [
   ("Parameter completeness checking", "live", "Every element tested against the project parameter "
    "schema before issue, with failures clustered by cause so you fix a family or a template "
    "rather than 241 elements one at a time."),
   ("Clearance and access rule sets", "live", "Maintenance access, valve access and damper access "
    "tested as rules rather than checked by eye. Most MEP coordination failures are access "
    "failures, and access failures do not appear in a clash report."),
   ("Calculation reconciliation", "live", "Sizing output compared against the as-modelled network "
    "so a duct that was resized in a spreadsheet and never changed in the model is caught before "
    "issue rather than on site."),
   ("Model interrogation and anomaly detection", "dev", "Reading elements, parameters, systems and "
    "relationships as structured data and detecting what does not fit the pattern. In development, "
    "used on our own delivery, not a released product."),
 ],
 "nots": [
   "We do not issue statutory or authority submissions, and we do not stamp drawings.",
   "We do not hold professional engineering licensure in the territories listed under Locations. "
   "Where a stamp is required, it comes from your engineer of record.",
   "We do not take on MEP design where no architectural or structural basis exists at all — "
   "there is nothing to coordinate against, and the work would be rewritten.",
   "We do not offer the AI intelligence layer as a licensable product. It is internal software.",
 ],
 "faqs": [
   ("Do you provide MEP design, or only MEP modelling?",
    "Both, and the distinction matters commercially. Modelling means authoring to a design someone "
    "else has fixed. Design support means we make the sizing, routing and system decisions against "
    "stated criteria and you review them. Say which you want at enquiry stage and the proposal "
    "will price the correct one."),
   ("Can you work to our templates and BIM execution plan?",
    "Yes, and we prefer it. Working inside your standards means the model returns to you in a state "
    "your team can maintain. Where there is no standard, we apply ours and hand over the "
    "documentation for it."),
   ("Who signs off the engineering?",
    "The engineer of record on the project. BIMRACE produces engineering design and BIM "
    "deliverables and a named BIMRACE engineer is accountable for the quality of what we issue, "
    "but statutory sign-off sits with the licensed professional appointed for that jurisdiction."),
   ("How do you handle a change to the architectural model mid-stage?",
    "Re-federate, re-run the clearance and clash rule sets, and report what the change broke as a "
    "prioritised list grouped by discipline. Because the checking is rule-based rather than manual, "
    "the cost of re-checking after a change is a fraction of the cost of checking the first time — "
    "which is the practical argument for automating it."),
   ("What software do you work in?",
    "Revit for authoring, Navisworks for federation and clash workflows, Dynamo and in-house "
    "routines for automation, IFC for exchange. Where a project mandates a different toolchain we "
    "work in it. Software names are listed to describe practice; no partnership is implied."),
 ],
 "related": [
   ("services/hvac-bim-services.html", "HVAC and ductwork",
    "Load, sizing, distribution and plant — the discipline that usually sets the ceiling void."),
   ("services/electrical-bim-services.html", "Electrical distribution",
    "Containment, distribution and the coordination conflicts containment causes."),
   ("services/plumbing-public-health-bim.html", "Public health and drainage",
    "Gravity systems, the one discipline that cannot be rerouted around a problem."),
   ("services/fire-protection-bim-services.html", "Fire protection",
    "Sprinkler coverage against structure, ceilings and every other service."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Federation, clash and clearance testing, issues tracked to closure."),
   ("industries/healthcare.html", "Healthcare MEP",
    "The sector where clearance and validation dominate the coordination effort."),
 ],
 "prefill": "mep_bim",
 "group": "mep",
},

# ---------------------------------------------------------------------------
{
 "slug": "hvac-bim-services",
 "nav": "HVAC design &amp; BIM",
 "h1": "HVAC design and ductwork BIM services",
 "title": "HVAC Design &amp; Ductwork BIM Services | BIMRACE",
 "desc": "HVAC design support and ductwork BIM: heating and cooling loads, duct and pipe sizing, "
         "plant room layouts and distribution modelled with performance data on the elements.",
 "eyebrow": "HVAC",
 "lede": "The discipline that usually decides how deep the ceiling void has to be — and therefore "
         "the one whose routing decisions everything else inherits.",
 "meta": [("Discipline", "Mechanical"), ("Status", "Live"),
          ("Systems", "Air · Chilled water · Heating · Ventilation"),
          ("Output", "Models · Loads · Sizing · Schedules")],
 "position": [
   ("Duct depth is the constraint the rest of the project pays for",
    "Rectangular ductwork is the largest single object in most ceiling voids, it cannot be "
    "rerouted as cheaply as cable tray, and it is usually drawn last. The result is a familiar "
    "sequence: the void is set architecturally, the mechanical route does not fit, and the "
    "resolution is either a bulkhead nobody wanted or an aspect-ratio change nobody calculated the "
    "pressure consequence of. We resolve the primary mechanical route first, and treat every "
    "subsequent change to it as an engineering change rather than a drafting one."),
   ("Aspect ratio is an engineering decision, not a coordination workaround",
    "Flattening a duct to clear a beam changes its hydraulic diameter, its pressure drop and its "
    "fan duty. Done once it is invisible; done eleven times along a run it is a plant selection "
    "problem discovered at commissioning. Where our model carries the sizing parameters, that "
    "accumulation is measurable while the change is being made, which is the only point at which "
    "it is cheap to argue about."),
   ("Plant access is designed, not left over",
    "Coil pull space, filter access, damper access and tube pull for a shell-and-tube heat "
    "exchanger are dimensioned requirements. They are also the requirements most often satisfied "
    "by whatever space happens to remain. We model them as clearance zones and test them as rules, "
    "so an access failure is a finding rather than an argument on site."),
 ],
 "delivers": [
   ("Heating and cooling load calculations", "Room-by-room or zone loads against stated internal "
    "and external design conditions, with the assumptions listed rather than buried."),
   ("Duct and pipe sizing", "Sized against the modelled network with velocity and pressure "
    "criteria stated, and the sizing parameters written onto the elements."),
   ("Ductwork and pipework models", "Supply, extract, fresh air, chilled water, heating and "
    "condensate modelled with system assignment, insulation and connectivity intact."),
   ("Plant room layouts", "Arrangement with access, replacement routes and plinth and drainage "
    "requirements resolved, coordinated against structure and electrical."),
   ("Equipment schedules", "AHUs, FCUs, chillers, pumps, terminals and dampers scheduled from the "
    "model with duties attached."),
   ("Ventilation and fire damper strategy", "Damper locations against compartment lines, with "
    "access provision modelled rather than assumed."),
 ],
 "inputs": [
   "Architectural model or plans with ceiling heights and compartment lines",
   "Structural model or beam layouts — the depth constraint comes from here",
   "Design conditions, occupancy and internal gains, or the standard to apply",
   "Selected plant, if already procured; otherwise we schedule to duty",
   "Acoustic and pressure criteria where they govern",
 ],
 "process": [
   ("01", "Loads and criteria", "Establish design conditions and calculate loads before any "
    "geometry exists, because the plant size decides the plant room and the plant room decides the "
    "architecture."),
   ("02", "Zoning", "Allocate the mechanical zone in the ceiling void and the riser allocation, "
    "and agree it with the other disciplines in writing."),
   ("03", "Primary distribution", "Route the largest ducts and mains first, against structure. "
    "Everything that follows is fitted to this, not the other way round."),
   ("04", "Sizing and terminals", "Size the network, place terminals, and write the sizing "
    "parameters back onto the elements."),
   ("05", "Access and clearance", "Test coil pull, filter access, damper access and valve access "
    "as clearance rules across the whole model."),
   ("06", "Documentation", "Drawings, schedules and the duty data, issued with the QA rule set "
    "run and a named engineer's signature."),
 ],
 "autos": [
   ("Duct and pipe parameter validation", "live", "Every run tested for size, system assignment, "
    "insulation and connectivity completeness before issue."),
   ("Clearance rule sets for plant access", "live", "Coil pull, filter and damper access tested as "
    "geometric rules across the federated model, not sampled by eye."),
   ("Sizing reconciliation", "live", "Calculated size against modelled size, element by element, "
    "so a spreadsheet change that never reached the model is caught."),
   ("Fan duty drift detection", "dev", "Accumulated pressure consequence of geometry changes along "
    "a run, reported as the change is made. In development on our own delivery."),
 ],
 "nots": [
   "We do not perform detailed CFD analysis.",
   "We do not carry out on-site commissioning or balancing.",
   "We do not certify compliance with a jurisdiction's mechanical code; we design to the criteria "
   "you state or the standard you name, and your engineer of record certifies.",
 ],
 "faqs": [
   ("Do you calculate loads, or only model what we give you?",
    "Either. Load calculation is a live capability and can be appointed on its own. If you already "
    "hold the loads, we size and model against them and will tell you if the modelled network "
    "disagrees with the sizing basis you supplied."),
   ("Which sizing method do you use?",
    "Equal friction or static regain for air, with velocity and pressure criteria agreed at the "
    "start and stated on the output. The method is a project decision and we will recommend one, "
    "but we will not apply one silently."),
   ("Can you model to fabrication level of detail?",
    "Yes — spool and fabrication drawings are a construction support deliverable. Say so at "
    "enquiry stage, because the authoring approach and the level of information need are different "
    "from a design model and cannot be retro-fitted cheaply."),
   ("How do you handle a ceiling void that is too shallow?",
    "We report it as an engineering finding with the options and their consequences — aspect ratio "
    "change and its pressure cost, a bulkhead, a re-zoning, or a raised slab-to-slab. What we will "
    "not do is quietly flatten the duct until it fits and let the fan duty absorb it."),
 ],
 "related": [
   ("services/mep-engineering-services.html", "Full MEP engineering",
    "All four disciplines coordinated as one set of interacting systems."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where the mechanical route meets everyone else's."),
   ("services/bim-automation-services.html", "BIM automation",
    "The QA and quantity routines that make re-checking after a change affordable."),
   ("industries/data-centres.html", "Data centre MEP",
    "Where mechanical density and tolerance are at their most demanding."),
 ],
 "prefill": "mep_bim",
 "group": "mep",
},

# ---------------------------------------------------------------------------
{
 "slug": "electrical-bim-services",
 "nav": "Electrical design &amp; BIM",
 "h1": "Electrical design and containment BIM services",
 "title": "Electrical Design &amp; Containment BIM | BIMRACE",
 "desc": "Electrical BIM and design support: LV distribution, containment routing, lighting, "
         "small power and model-derived load and panel schedules.",
 "eyebrow": "Electrical",
 "lede": "The discipline with the most flexible routes and the least respected space allocation — "
         "which is exactly why its coordination failures surface last and cost most.",
 "meta": [("Discipline", "Electrical"), ("Status", "Live"),
          ("Systems", "LV distribution · Containment · Lighting · Small power"),
          ("Output", "Models · Load schedules · Panel schedules · Drawings")],
 "position": [
   ("Containment is treated as infinitely flexible until it is not",
    "Cable tray can go almost anywhere, so on most projects it goes wherever is left. That works "
    "until the cumulative result is a tray route with eleven changes of level, no maintained "
    "separation from the chilled water above it, and no clear access for cable pulling. "
    "Flexibility is a property of the early design and a liability in the late one. We allocate "
    "the containment zone at the same time as the mechanical zone, and test the separation "
    "requirement as a rule rather than as an instruction in a specification."),
   ("Circuit data belongs on the element",
    "A cable tray drawn as a generic object is a rectangle. A cable tray carrying its fill "
    "percentage, its circuits and its segregation class is a thing the model can be asked about — "
    "including whether the route it was given still satisfies the segregation requirement after "
    "three rounds of coordination moved it. The difference is entirely in how it was authored."),
   ("Distribution boards are a spatial commitment",
    "A board schedule that fits on a page can still fail when the board, its working space, its "
    "escape route clearance and the containment arriving at it are put in a riser cupboard "
    "dimensioned from an earlier revision. We model the working space as a clearance zone, because "
    "that is the only form in which a checking routine can test it."),
 ],
 "delivers": [
   ("LV distribution models", "Boards, submains, busbar and final circuits modelled with circuit "
    "and rating data carried on the elements."),
   ("Containment routing", "Tray, ladder, basket, trunking and conduit routed against structure "
    "and other services, with segregation and fill accounted for."),
   ("Lighting and small power layouts", "Luminaire and outlet layouts against the reflected "
    "ceiling plan, with switching and emergency provision."),
   ("Load and panel schedules", "Derived from the model, so a circuit added in the model appears "
    "in the schedule rather than in a separate spreadsheet that drifts."),
   ("Earthing and bonding layouts", "Where in scope, modelled and scheduled against the "
    "distribution design."),
   ("Riser and cupboard coordination", "Board working space, containment entry and access "
    "clearance resolved as modelled zones."),
 ],
 "inputs": [
   "Architectural model with ceiling plans and riser locations",
   "Structural model — penetrations and beam depths govern tray routes",
   "Incoming supply arrangement and load schedule, or the basis to calculate one",
   "Lighting design criteria, or the lux levels and standard to apply",
   "Segregation and containment standards the project runs to",
]
 ,
 "process": [
   ("01", "Load basis", "Establish connected and maximum demand, diversity and the distribution "
    "strategy before routing."),
   ("02", "Zoning", "Containment zone in the void and riser allocation, agreed alongside "
    "mechanical rather than after it."),
   ("03", "Primary containment", "Main tray and busbar routes set against structure and "
    "mechanical, with separation designed in."),
   ("04", "Final circuits and outlets", "Lighting, small power and specialist systems placed "
    "against the architectural layouts."),
   ("05", "Working space and access", "Board clearance, escape route and pulling access tested as "
    "clearance rules."),
   ("06", "Schedules and issue", "Panel and load schedules derived from model state, QA rule set "
    "run, engineer signs."),
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
   "We do not carry out protective device discrimination or arc flash studies.",
   "We do not issue electrical certificates or perform site testing and inspection.",
   "We do not sign off compliance with a national wiring regulation; we design to the standard you "
   "name and your engineer of record certifies.",
 ],
 "faqs": [
   ("Do you produce panel schedules from the model?",
    "Yes. Deriving them from model state rather than maintaining a parallel spreadsheet is the "
    "point — it removes the most common source of drift between the electrical drawings and the "
    "electrical schedule."),
   ("Can you route containment if the mechanical model is not finished?",
    "We can start, but the sequence matters. Containment routed before the primary mechanical "
    "distribution is fixed will be re-routed, because ductwork has far less freedom. We will say "
    "so rather than produce work that has to be redone."),
   ("How is segregation between services checked?",
    "As a geometric rule across the federated model, at the separation distance the project "
    "standard requires, rather than by visual inspection of sections. It re-runs on every "
    "federation, which is what makes it useful after a change rather than only at first issue."),
   ("Do you model to containment fabrication detail?",
    "Bracket and support layouts and builders work drawings are construction support deliverables "
    "and can be appointed. State the level of information need at enquiry stage."),
 ],
 "related": [
   ("services/mep-engineering-services.html", "Full MEP engineering",
    "All four disciplines coordinated together."),
   ("services/hvac-bim-services.html", "HVAC and ductwork",
    "The discipline that sets the zone containment has to work around."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Separation and access tested as rules, not read off sections."),
   ("industries/commercial.html", "Commercial and offices",
    "Tenant variation and repeated coordination cycles."),
 ],
 "prefill": "mep_bim",
 "group": "mep",
},

# ---------------------------------------------------------------------------
{
 "slug": "plumbing-public-health-bim",
 "nav": "Public health &amp; drainage",
 "h1": "Plumbing, public health and drainage BIM services",
 "title": "Public Health, Plumbing &amp; Drainage BIM | BIMRACE",
 "desc": "Public health and plumbing BIM: above and below ground drainage, domestic water and "
         "rainwater, modelled with true falls and connectivity intact.",
 "eyebrow": "Public health",
 "lede": "The only discipline on the project that cannot be rerouted around a problem, because "
         "gravity is not negotiable — which makes it the one that should be routed first and "
         "almost never is.",
 "meta": [("Discipline", "Public health"), ("Status", "Live"),
          ("Systems", "Soil · Waste · Rainwater · Domestic water"),
          ("Output", "Models · Falls · Sizing · Schedules")],
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
    "Public health is where broken connectivity hides most easily: a run that looks continuous in "
    "a 3D view but is three disconnected segments to the software. Authoring with connectivity "
    "intact is what lets a routine follow a run from appliance to connection and tell you it does "
    "not actually get there."),
 ],
 "delivers": [
   ("Above-ground drainage", "Soil, waste and vent modelled with falls, access points and "
    "connectivity intact."),
   ("Below-ground drainage", "Runs, inverts, chambers and connections coordinated against "
    "foundations and other buried services."),
   ("Domestic cold and hot water", "Distribution, boosting, storage and return, sized and modelled "
    "with system assignment."),
   ("Rainwater and syphonic systems", "Roof drainage and downpipe routing coordinated with "
    "structure and facade."),
   ("Sanitaryware and appliance schedules", "Scheduled from the model against the architectural "
    "room data."),
   ("Pipe sizing and discharge calculations", "Sized against the modelled network with the "
    "loading units and method stated."),
 ],
 "inputs": [
   "Architectural model with sanitary layouts and room data",
   "Structural model with slab levels, foundations and any existing below-ground constraints",
   "Connection points, invert levels and the adopted sewer arrangement",
   "Water supply pressure and any storage or boosting requirement",
   "The drainage standard the project runs to",
 ],
 "process": [
   ("01", "Connection constraints", "Fix inverts, connection points and the levels the whole system "
    "has to work back from. Everything else is downstream of this."),
   ("02", "Stack and riser positions", "Agreed with the architect early, because they are the "
    "hardest thing on the project to move."),
   ("03", "Gravity routing", "Above and below ground, modelled with true falls and access points "
    "at the required intervals."),
   ("04", "Pressurised systems", "Domestic water, boosting and hot water return, routed and sized "
    "against the gravity systems already fixed."),
   ("05", "Coordination", "Federated testing against structure and the other services, with "
    "access chamber and rodding access clearance included."),
   ("06", "Documentation", "Drawings, schedules and calculations, QA rule set run, engineer signs."),
 ],
 "autos": [
   ("Connectivity and continuity checking", "live", "Every run traced from appliance to connection "
    "as a graph, so a visually continuous but disconnected system is caught at authoring rather "
    "than at coordination."),
   ("Fall and gradient validation", "live", "Modelled gradient tested against the required fall "
    "for the pipe size, run by run, with failures listed by element."),
   ("Access point spacing rules", "live", "Rodding and access point intervals tested as a rule "
    "along each run."),
   ("Invert clash against structure", "live", "Below-ground runs tested against foundations and "
    "slab levels as part of the federated rule set."),
 ],
 "nots": [
   "We do not carry out drainage adoption applications or negotiate with the adopting authority.",
   "We do not perform CCTV survey or condition assessment of existing drainage.",
   "We do not certify compliance with a jurisdiction's plumbing code; we design to the standard "
   "you name and your engineer of record certifies.",
 ],
 "faqs": [
   ("Do you model drainage with real falls?",
    "Yes, as a matter of course. A flat run with a fall annotation cannot be coordinated and will "
    "produce a coordination report that is wrong in the one discipline where being wrong is most "
    "expensive to fix."),
   ("Can you coordinate below-ground drainage against foundations?",
    "Yes. It is part of the federated rule set rather than a separate exercise, and invert-against-"
    "foundation is one of the checks that most often finds something."),
   ("Which sizing method do you use?",
    "Discharge unit or loading unit methods to the standard the project names, with the method and "
    "the assumed simultaneity stated on the output rather than implied."),
   ("What if the drainage connection level is not yet known?",
    "We model to a stated assumed invert and flag it as an assumption on the issue. What we will "
    "not do is pick a level quietly, because every run in the building is dimensioned back from it."),
 ],
 "related": [
   ("services/mep-engineering-services.html", "Full MEP engineering",
    "All four disciplines coordinated together."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Gravity systems tested against structure and everything else."),
   ("industries/healthcare.html", "Healthcare",
    "Where drainage, clearance and validation requirements are at their strictest."),
   ("industries/residential.html", "Residential and mixed use",
    "Repeated riser typologies — the ideal condition for rule-based checking."),
 ],
 "prefill": "mep_bim",
 "group": "mep",
},

# ---------------------------------------------------------------------------
{
 "slug": "fire-protection-bim-services",
 "nav": "Fire protection BIM",
 "h1": "Fire protection and sprinkler BIM services",
 "title": "Fire Protection &amp; Sprinkler BIM Services | BIMRACE",
 "desc": "Fire protection BIM: sprinkler layouts, coverage and obstruction checking, riser "
         "routing and compartment penetration coordination.",
 "eyebrow": "Fire protection",
 "lede": "The discipline whose coordination failures are the most consequential and the most "
         "geometric — coverage is a spatial test, and a spatial test is something a rule set can "
         "actually run.",
 "meta": [("Discipline", "Fire protection"), ("Status", "Live"),
          ("Systems", "Sprinkler · Wet &amp; dry riser · Detection containment"),
          ("Output", "Models · Layouts · Coverage checks · Drawings")],
 "position": [
   ("Obstruction, not collision, is the failure mode",
    "A sprinkler head that does not clash with anything can still be useless. Coverage depends on "
    "distance to obstruction, deflector position relative to the ceiling and the obstruction rules "
    "for the hazard class — none of which a standard clash test looks at. Fire protection is the "
    "clearest example on any project of why clash detection and coordination are different "
    "activities, and it is the discipline where treating them as the same thing is least "
    "forgivable."),
   ("Compartmentation is a model-wide constraint",
    "Every service that crosses a compartment line creates a penetration that needs a seal, a "
    "damper or both, and needs access to it. That is not a fire protection deliverable in "
    "isolation — it is a constraint on all four disciplines that only becomes visible when the "
    "compartment lines are in the federated model as geometry rather than in a fire strategy PDF."),
   ("Routing against structure is the recurring conflict",
    "In long-span industrial and warehouse structures the sprinkler main and the structural "
    "bracing want the same place, repeatedly and predictably. Because it is predictable, it is "
    "worth designing for at zoning stage rather than resolving eleven times at coordination stage."),
 ],
 "delivers": [
   ("Sprinkler layouts", "Head placement against the reflected ceiling plan and hazard class, with "
    "spacing and obstruction rules applied."),
   ("Pipework distribution models", "Mains, ranges and drops modelled with system assignment and "
    "sizing data."),
   ("Wet and dry riser routing", "Riser positions, landing valve locations and access coordinated "
    "with the architectural cores."),
   ("Compartment penetration schedules", "Every service crossing a compartment line identified, "
    "scheduled and coordinated for damper or seal access."),
   ("Coverage and obstruction reports", "Coverage tested as a geometric rule and reported by "
    "element, not certified by eye."),
   ("Coordination drawings", "Derived from the model at the status the appointment requires."),
 ],
 "inputs": [
   "Fire strategy, or the hazard classification to apply",
   "Architectural model with reflected ceiling plans and compartment lines",
   "Structural model — bracing and long-span members drive the recurring conflict",
   "Water supply arrangement, pressure and any tank or pump requirement",
   "The sprinkler standard the project runs to",
 ],
 "process": [
   ("01", "Hazard and standard", "Fix the classification and the standard. Head spacing, "
    "obstruction rules and density all follow from it and nothing can start without it."),
   ("02", "Compartmentation in the model", "Compartment lines brought into the federated model as "
    "geometry so penetrations become visible as findings rather than as a later discovery."),
   ("03", "Main routing", "Sprinkler mains routed against structure at the same stage as the "
    "mechanical primary, not after it."),
   ("04", "Head layout", "Placed against the ceiling plan and tested for spacing and obstruction "
    "as a rule set."),
   ("05", "Coordination", "Federated testing, with obstruction and access treated as first-class "
    "findings alongside hard clashes."),
   ("06", "Documentation", "Layouts, schedules and reports issued with the QA rule set run."),
 ],
 "autos": [
   ("Coverage and spacing rule sets", "live", "Head spacing, wall distance and area per head tested "
    "geometrically against the hazard class across the whole model."),
   ("Obstruction checking", "live", "Distance to obstruction and deflector position tested as "
    "rules — the check a clash report structurally cannot perform."),
   ("Compartment penetration detection", "live", "Every service crossing a compartment boundary "
    "identified automatically and scheduled, across all disciplines."),
   ("Damper access clearance", "live", "Access to fire and smoke dampers tested as a clearance "
    "zone, because a damper nobody can reach fails at the first inspection."),
 ],
 "nots": [
   "We do not act as the fire engineer and we do not author the fire strategy.",
   "We do not carry out hydraulic certification or issue sprinkler system certificates.",
   "We do not perform fire modelling, evacuation modelling or smoke control analysis.",
   "Our coverage and obstruction checking supports the responsible fire protection engineer; it "
   "does not replace their approval.",
 ],
 "faqs": [
   ("Do you design the sprinkler system or model someone else's design?",
    "We provide layout and coordination support and model to the hazard class and standard stated "
    "in the fire strategy. The fire engineer remains responsible for the strategy and for "
    "certification. Where you need a full hydraulically certified design, that is a different "
    "appointment and we will say so."),
   ("What does obstruction checking actually test?",
    "Distance from each head to obstructions in its coverage area and deflector position relative "
    "to the ceiling, against the rules for the stated hazard class. It runs as a geometric rule "
    "over the federated model and reports by head, with an element ID against every finding."),
   ("Can you identify compartment penetrations across all disciplines?",
    "Yes, provided the compartment lines are in the federated model as geometry. That is usually "
    "the missing input rather than a technical limitation, and it is the first thing we ask for."),
   ("Is this useful before the ceiling design is fixed?",
    "The main routing is. Head layout is not, because it is entirely determined by the reflected "
    "ceiling plan and will be redone. We would rather sequence it correctly than bill for work "
    "that gets thrown away."),
 ],
 "related": [
   ("services/mep-engineering-services.html", "Full MEP engineering",
    "All four disciplines coordinated together."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where obstruction and access are separated from hard clashes."),
   ("industries/industrial.html", "Industrial and warehousing",
    "Long-span structures where fire protection against structure is the recurring conflict."),
   ("industries/hospitality.html", "Hospitality",
    "Finish-critical ceilings where head position is an architectural negotiation."),
 ],
 "prefill": "mep_bim",
 "group": "mep",
},

# ---------------------------------------------------------------------------
{
 "slug": "bim-coordination-clash-detection",
 "nav": "BIM coordination &amp; clash detection",
 "h1": "BIM coordination and clash detection services",
 "title": "BIM Coordination &amp; Clash Detection | BIMRACE",
 "desc": "Federated model assembly, clash and clearance rule sets, findings classified by cause "
         "and responsible discipline, and tracked to evidenced closure.",
 "eyebrow": "Coordination",
 "lede": "Clash detection produces a number. Coordination produces a decision — what actually "
         "conflicts, why, whose model has to move, and evidence that it did.",
 "meta": [("Status", "Live"), ("Input", "Federated discipline models"),
          ("Output", "Resolved model · Issue history"),
          ("Tested", "Clash · Clearance · Access · Zoning")],
 "position": [
   ("A clash count is not a coordination report",
    "Eleven thousand clashes is not information. Most of it is insulation touching insulation, the "
    "same duct counted against forty hangers, and two disciplines that were never going to "
    "conflict in reality. A report nobody can act on is worse than no report, because it consumes "
    "the time that should have gone into the two hundred findings that matter. We classify by "
    "cause and by who has to move before anything is issued."),
   ("Most coordination failures are not collisions",
    "The parts do not touch; they just cannot be installed in that order, or maintained afterwards, "
    "or reached at all. Clearance, access and installation sequence failures do not appear in a "
    "hard clash test, and on a services-dense project they outnumber true clashes. We test them as "
    "explicit rule sets, which means we have to write the rules down — and a written rule set is "
    "something a client can review and disagree with, which is the point."),
   ("The issue history is a deliverable",
    "Why a duct moved in March is usually in someone's inbox. The next stage inherits the geometry "
    "without the reasoning and re-litigates it. Our coordination appointments produce an auditable "
    "record — finding, cause, decision, who accepted it, and the re-test that proved it closed."),
 ],
 "delivers": [
   ("Federated model assembly", "All contributing disciplines assembled on shared coordinates, at "
    "an agreed federation frequency, with model health checked on receipt."),
   ("Clash and clearance rule sets", "Written rule sets covering hard clash, clearance, "
    "maintenance access and zoning compliance — reviewable before they are run."),
   ("Classified issue lists", "Findings grouped by cause and by responsible discipline, with an "
    "element ID against each, and true clashes separated from access and clearance failures."),
   ("Resolution tracking", "Issues tracked to closure with the decision and the accepting party "
    "recorded, and a re-test that evidences the close."),
   ("Coordination reports", "Per-cycle reporting on what was found, what closed, what is open and "
    "where the same cause keeps recurring."),
   ("Coordination workshop support", "Preparation, viewpoints and the evidence pack for the "
    "meeting, so the meeting resolves rather than discovers."),
 ],
 "inputs": [
   "Discipline models from every contributing party, on agreed shared coordinates",
   "The BEP, or the federation and naming convention the project runs to",
   "Clearance, access and zoning requirements — or ours, if none are stated",
   "Compartment lines and ceiling zones as geometry, not as a PDF",
   "The issue tracking environment the project uses, if one is mandated",
 ],
 "process": [
   ("01", "Federation strategy", "Agree what is federated, how often, on what coordinates, and who "
    "is responsible for each model. Most coordination problems are actually federation problems."),
   ("02", "Rule set definition", "Write the clash, clearance, access and zoning rules down and "
    "have the project agree them before the first run."),
   ("03", "Model health check", "Every received model checked for coordinates, units, naming and "
    "parameter completeness before it enters the federation. A bad model in produces noise out."),
   ("04", "Test and classify", "Run the rule sets, then classify by cause and responsible "
    "discipline rather than presenting a raw count."),
   ("05", "Resolve and record", "Route findings, track decisions, record who accepted what."),
   ("06", "Re-test and evidence", "Close nothing without a re-test that proves it. The re-test is "
    "the deliverable, not the assertion."),
 ],
 "autos": [
   ("Rule-based clash and clearance testing", "live", "Hard clash, clearance, access and zoning "
    "run as defined rule sets across the federated model on every cycle."),
   ("Classification by cause", "live", "Findings clustered so that one template error producing "
    "two hundred findings is reported as one cause, not two hundred tickets."),
   ("Model health checking on receipt", "live", "Coordinates, units, naming, classification and "
    "parameter completeness tested on every incoming model."),
   ("Prioritisation and routing", "dev", "Severity and responsible-discipline assignment proposed "
    "automatically for engineering review. In development, used on our own delivery."),
 ],
 "nots": [
   "We do not accept responsibility for another party's design decisions; we identify, classify and "
   "track, and the originating designer resolves.",
   "We do not close an issue without a re-test.",
   "We do not report a clash count as a performance metric, and we will push back if asked to.",
 ],
 "faqs": [
   ("What is the difference between clash detection and BIM coordination?",
    "Clash detection is a geometric test that produces findings. Coordination is the process of "
    "deciding what those findings mean, who resolves them, and evidencing that they closed. A "
    "provider selling clash detection is selling you a file. A coordination appointment is "
    "accountable for the resolved model and the issue history."),
   ("How do you avoid a report with eleven thousand meaningless clashes?",
    "By writing the rule sets before running them, filtering by tolerance and element class, and "
    "clustering findings by cause. A recurring cause — a family with wrong insulation, a template "
    "error, a coordinate offset — is reported once with its element list, not once per element."),
   ("Do you test maintenance access as well as clashes?",
    "Yes, as a separate rule set with its own findings, because access failures and hard clashes "
    "have different causes, different owners and different costs. On services-dense projects the "
    "access findings are usually the more valuable half."),
   ("Can you coordinate models authored by other consultants?",
    "Yes — that is the normal case. We check each model's health on receipt and will report where "
    "an incoming model is not in a state that can be coordinated, which is information the project "
    "needs whether or not it is welcome."),
   ("Which clash workflow and tools do you use?",
    "Navisworks for federation and clash workflows, with in-house routines for the clearance, "
    "access and zoning rule sets that a standard clash engine does not express. Where a project "
    "mandates a different environment we work in it."),
 ],
 "related": [
   ("services/mep-engineering-services.html", "MEP engineering",
    "The discipline depth that makes a clearance rule set defensible."),
   ("services/fire-protection-bim-services.html", "Fire protection",
    "The clearest case for separating obstruction from collision."),
   ("services/bim-automation-services.html", "BIM automation",
    "Why re-checking after a change costs a fraction of the first check."),
   ("automation.html", "AI and automation",
    "Clash intelligence, and where the engineer signs."),
   ("industries/data-centres.html", "Data centres",
    "Tolerance coordination at the highest services density we work at."),
 ],
 "prefill": "bim_coordination",
 "group": "coordination",
},

# ---------------------------------------------------------------------------
{
 "slug": "bim-modelling-documentation",
 "nav": "BIM modelling &amp; documentation",
 "h1": "BIM modelling and documentation services",
 "title": "BIM Modelling &amp; Documentation Services | BIMRACE",
 "desc": "Discipline BIM models authored to an agreed level of information need, with drawings and "
         "schedules derived from model state rather than drafted separately.",
 "eyebrow": "Modelling",
 "lede": "A model authored to look right and a model authored to be read are visually identical "
         "and completely different assets. We produce the second kind.",
 "meta": [("Status", "Live"), ("Disciplines", "A · S · M · E · P · FP"),
          ("Basis", "Level of information need"),
          ("Output", "Models · Drawings · Schedules")],
 "position": [
   ("Information-first authoring is the whole argument",
    "Parameters populated during authoring cost a little at the time. Parameters retro-fitted "
    "before handover cost a great deal, are usually incomplete, and produce a model that cannot be "
    "checked automatically — which means every downstream promise about automation, quantities and "
    "asset data quietly fails. This is unglamorous and it is the precondition for everything else "
    "on this site."),
   ("Drawings are a view of the model, not a parallel deliverable",
    "Where drawings are drafted alongside the model, a change is two events and they eventually "
    "disagree. Where drawings are derived from model state, a change is one event. Getting to the "
    "second condition requires template, view and sheet discipline set up before authoring starts, "
    "which is why we do that first and will not skip it to save a week."),
   ("Level of information need is a commercial instrument",
    "\"LOD 400\" as a blanket statement across a project is a way of not deciding. The useful "
    "version is element-by-element: what has to be accurate, what has to carry data, and what is "
    "placeholder geometry. We agree it explicitly, because it is the single largest driver of "
    "authoring cost and the thing most often left vague until it is expensive."),
 ],
 "delivers": [
   ("Discipline models", "Architectural, structural and MEP models authored to the agreed level of "
    "information need with classification and parameters populated during authoring."),
   ("Model setup and templates", "Project templates, shared coordinates, browser organisation, "
    "view templates, naming and the project parameter schema."),
   ("General arrangement drawings", "Plans, sections, elevations and details derived from model "
    "state, at the required status codes."),
   ("Schedules", "Door, room, equipment and component schedules generated from the model."),
   ("Family and content creation", "Parametric content built to the project's data schema rather "
    "than downloaded and patched."),
   ("Model audit and health reporting", "Regular reporting on file health, warnings, naming "
    "compliance and parameter completeness."),
 ],
 "inputs": [
   "Existing drawings, models or survey data in whatever state they exist",
   "The EIR, BEP or modelling standard the project runs to",
   "Level of information need per element, or a session to agree one",
   "Sheet standard, title block and drawing register",
   "Classification system, if one is mandated",
 ],
 "process": [
   ("01", "Standards and schema", "Templates, naming, classification and the project parameter "
    "schema established before a single element is placed."),
   ("02", "Level of information need", "Agreed element by element and written down, because it is "
    "the cost driver and the source of most scope disputes."),
   ("03", "Authoring", "Modelled with parameters populated as elements are placed, not afterwards."),
   ("04", "Continuous QA", "The project rule set runs during authoring rather than only before "
    "issue, so failures are corrected while the context is still fresh."),
   ("05", "Documentation", "Views, sheets and schedules derived from model state."),
   ("06", "Issue", "Through the CDE at the correct status code, under a named engineer."),
 ],
 "autos": [
   ("Parameter completeness rule sets", "live", "Every element tested against the project schema, "
    "with failures clustered by family or template so the fix is one change rather than hundreds."),
   ("Naming and classification checking", "live", "Views, sheets, families and elements tested "
    "against the project convention automatically."),
   ("Model health auditing", "live", "Warnings, file size, purgeable content, unplaced elements and "
    "view organisation reported on a schedule."),
   ("Documentation generation", "live", "Views and schedules derived from model state as a routine "
    "rather than assembled by hand."),
 ],
 "nots": [
   "We do not retro-fit parameters into a model that was authored without them and call the result "
   "queryable — we will quote the remediation honestly or advise against it.",
   "We do not produce a model at a level of information need that was never agreed and then invoice "
   "for the difference.",
   "We do not deliver drawings drafted separately from the model.",
 ],
 "faqs": [
   ("What does 'information-first modelling' mean in practice?",
    "That the project parameter schema exists before authoring starts and parameters are populated "
    "as elements are placed. The visible model looks the same either way. The difference appears "
    "the first time anyone tries to check, schedule or extract anything from it."),
   ("Can you work inside our Revit template and standards?",
    "Yes, and it is usually the better option — the model comes back in a state your team can "
    "maintain. Where there is no standard we apply ours and hand over the documentation."),
   ("Can you remediate an existing model that was not authored this way?",
    "Sometimes, and we will tell you honestly which case you are in. Some models can be brought up "
    "to a queryable standard economically. Others cost more to remediate than to re-author, and we "
    "would rather say that at enquiry stage than discover it at forty per cent."),
   ("Do you create Revit families?",
    "Yes — built parametrically to the project's data schema. Content downloaded from a "
    "manufacturer site and patched is the most common single cause of parameter completeness "
    "failure later."),
   ("How is level of information need agreed?",
    "Element by element, in writing, before authoring. A blanket LOD number across a whole project "
    "is a way of postponing the decision until it is expensive."),
 ],
 "related": [
   ("services/revit-services.html", "Revit services",
    "Templates, families, parameter schemas and MEP authoring."),
   ("services/bim-automation-services.html", "BIM automation",
    "What becomes possible once the model was authored to be read."),
   ("intelligence.html", "BIM Intelligence",
    "The full argument for treating the model as an engineering database."),
   ("technology.html", "Standards and QA",
    "ISO 19650 information management and the six checks before issue."),
 ],
 "prefill": "bim_modelling",
 "group": "modelling",
},

# ---------------------------------------------------------------------------
{
 "slug": "revit-services",
 "nav": "Revit services",
 "h1": "Revit services: templates, families, MEP authoring and parameter schemas",
 "title": "Revit Services | Templates, Families, MEP | BIMRACE",
 "desc": "Revit project setup, template and family creation, MEP authoring, parameter schema "
         "design and Dynamo automation, handed over documented.",
 "eyebrow": "Revit",
 "lede": "Most of what goes wrong in a Revit project was decided in the first week, in the "
         "template and the parameter schema, by someone who was told to start modelling.",
 "meta": [("Status", "Live"), ("Scope", "Setup · Content · Authoring · Automation"),
          ("Exchange", "IFC · Navisworks · Schedules"),
          ("Automation", "Dynamo · in-house routines")],
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
   ("Automation in Revit is ordinary engineering practice, not a novelty",
    "Dynamo graphs and scripted routines have been how competent teams handle parameter updates, "
    "naming, sheet creation and data extraction for years. We treat them as delivery tooling with "
    "the same review expectations as anything else we issue — and we hand them over, documented, "
    "rather than keeping them as leverage."),
 ],
 "delivers": [
   ("Project setup", "Templates, shared coordinates, worksets, browser organisation, view templates "
    "and sheet standards."),
   ("Parameter schema design", "Shared parameter files and the project parameter schema, designed "
    "against what actually has to be extracted later."),
   ("Family and content creation", "Parametric families built to the project schema, with the "
    "connectors, types and data a scheduling and checking routine needs."),
   ("MEP authoring", "Mechanical, electrical, public health and fire protection modelled with "
    "system assignment and connectivity intact."),
   ("Dynamo and scripted routines", "Automation for parameter management, naming, sheet and view "
    "creation, data extraction and checking — handed over with documentation."),
   ("Interoperability and exchange", "IFC export configuration, Navisworks preparation and "
    "structured data exports."),
 ],
 "inputs": [
   "Existing template and content library, if there is one",
   "The data you need to get out of the model at the end — this drives the schema",
   "Classification and naming conventions the project mandates",
   "Sheet standard and title block",
   "Revit version and worksharing arrangement",
 ],
 "process": [
   ("01", "Extraction requirements first", "Start from what has to come out of the model at "
    "handover and design the parameter schema backwards from it. Schemas designed forwards from "
    "authoring convenience never satisfy the handover."),
   ("02", "Template build", "Views, sheets, browser organisation, naming, worksets and schedules."),
   ("03", "Content", "Families built parametrically against the schema, tested in a schedule "
    "before they are released into the project."),
   ("04", "Authoring", "Modelling with the schema populated as elements are placed."),
   ("05", "Routine development", "Dynamo graphs and scripts for the repetitive work, reviewed like "
    "any other deliverable."),
   ("06", "Handover", "Template, content library, routines and documentation, so your team can "
    "maintain it without us."),
 ],
 "autos": [
   ("Parameter update and management routines", "live", "Bulk parameter population and correction "
    "run as documented routines rather than by hand."),
   ("Naming and view organisation", "live", "Views, sheets and families named and organised against "
    "the project convention automatically."),
   ("Sheet and view generation", "live", "Sheets, views and schedules created from model state as "
    "a routine."),
   ("Model checking routines", "live", "The project rule set run inside the authoring environment "
    "during production, not only before issue."),
   ("AI-assisted model interrogation", "dev", "Asking structured questions of model data — element "
    "counts by system, parameter completeness, where a family is used. In development and used on "
    "our own delivery; see the MCP for Revit page for what this would and would not involve."),
 ],
 "nots": [
   "We do not sell or resell Revit licences, and we are not an Autodesk partner.",
   "We do not run automation that writes to a live model without a named engineer accepting the "
   "change first.",
   "We do not keep delivery routines proprietary as a lock-in mechanism — what we build for your "
   "project is handed over with documentation.",
 ],
 "faqs": [
   ("Can you set up a Revit project standard from scratch?",
    "Yes. Templates, shared parameters, naming, browser organisation, view templates, sheet "
    "standards and a starter content library, documented so your team can maintain it."),
   ("Why not use manufacturer families?",
    "Because they are built to describe a product, not to satisfy your data schema. They usually "
    "schedule incorrectly, carry the wrong parameter names, and are the most common single cause of "
    "parameter completeness failures at QA. Where a specific product must be represented, we "
    "rebuild it against the schema."),
   ("Do you hand over the Dynamo graphs you build?",
    "Yes, documented. Routines built for your project on your appointment are yours. The internal "
    "intelligence tooling is a separate thing and is not licensable — the site is explicit about "
    "that distinction."),
   ("Which Revit versions do you work in?",
    "Whichever the project mandates. Version is a project decision with real consequences for "
    "exchange and for upgrade timing, so we work to yours rather than imposing ours."),
   ("Can you do Revit work as an extension of our team?",
    "Yes — team extension inside your environment and your standards for a defined period is one "
    "of the four appointment models on the engineering page."),
 ],
 "related": [
   ("services/bim-modelling-documentation.html", "BIM modelling and documentation",
    "The authoring discipline the template exists to enforce."),
   ("services/bim-automation-services.html", "BIM automation",
    "Where routines stop being convenience and become a service category."),
   ("technology/mcp-for-revit.html", "MCP for Revit",
    "What connecting an AI assistant to model data would actually require."),
   ("services/mep-engineering-services.html", "MEP engineering",
    "The discipline depth behind the authoring."),
 ],
 "prefill": "bim_modelling",
 "group": "modelling",
},

# ---------------------------------------------------------------------------
{
 "slug": "bim-automation-services",
 "nav": "BIM automation",
 "h1": "BIM and design automation services",
 "title": "BIM Automation Services | Automated QA &amp; QTO | BIMRACE",
 "desc": "Automated BIM QA rule sets, quantity extraction and documentation routines, delivered "
         "as tooling plus the engineering behind it.",
 "eyebrow": "Automation",
 "lede": "Automation is scoped, priced and delivered here as a service category in its own right — "
         "not as a paragraph at the end of a modelling proposal.",
 "meta": [("Status", "Live"), ("Delivered as", "Tooling + engineering"),
          ("Review", "Engineer signs every output"),
          ("Handover", "Documented, yours to keep")],
 "position": [
   ("Checking should not scale with headcount",
    "Doubling the model doubles the checking. The conventional lever is more people, and more "
    "people checking by hand produces less consistency rather than more — every reviewer has a "
    "slightly different threshold and none of them write it down. A rule set has exactly one "
    "threshold, it is written down, and the eleventh run costs the same as the first. That is the "
    "entire economic argument, and it only works if the model was authored to be read."),
   ("The value is in the rules, not the script",
    "Anyone can write a Dynamo graph. The difficult part is knowing what a competent engineer "
    "actually checks and at what threshold — which requires people who have sized the systems the "
    "rules govern. An automation practice without discipline depth produces confident nonsense at "
    "scale, and there is a great deal of it in this sector right now."),
   ("Automation drafts; engineers decide",
    "No routine we deliver writes to a live model, closes an issue, changes a status code or "
    "issues a deliverable. It reads, tests and drafts, and a named engineer accepts, amends or "
    "rejects. This is a design constraint we do not intend to remove, because engineering "
    "liability does not automate."),
 ],
 "delivers": [
   ("Automated QA rule sets", "The project standards pass — parameter validation, naming, family "
    "audit, system integrity — run as a rule set with an element ID against every finding."),
   ("Quantity extraction routines", "Quantities measured from geometry and parameters, classified, "
    "with the measurement rule visible per line and traceable back to elements."),
   ("Documentation pipelines", "Sheets, views and schedules derived from model state, so a model "
    "change and a drawing change are one event."),
   ("Parameter and data management", "Bulk population, correction and migration of model data, run "
    "as documented routines."),
   ("Model health and audit reporting", "Scheduled reporting on warnings, naming compliance, "
    "parameter completeness and file health."),
   ("Data export and integration", "Structured exports to the formats your downstream systems "
    "actually consume."),
 ],
 "inputs": [
   "A model, or a representative sample of the models the routine has to run against",
   "The check you currently perform by hand, described as you currently describe it",
   "The threshold or standard the check applies — or a session to write it down",
   "The format the output has to arrive in",
   "Who reviews the output, so the handover point is designed rather than assumed",
 ],
 "process": [
   ("01", "Find the real cost", "Identify which manual step actually consumes the time. It is "
    "frequently not the one the team nominates."),
   ("02", "Write the rule down", "Turn the check into an explicit, reviewable threshold. This step "
    "produces most of the value even before anything is automated."),
   ("03", "Build and calibrate", "Develop the routine and run it against known-good and known-bad "
    "models to establish its false-positive rate."),
   ("04", "State the false-positive rate", "A checker with an unstated false-positive rate cannot "
    "be evaluated. We measure it and publish it to you."),
   ("05", "Design the review point", "Decide explicitly where the engineer reviews and what they "
    "are reviewing. Automation without a designed handover point is just faster error production."),
   ("06", "Handover", "Routine, documentation and the rule set, so your team can run and amend it."),
 ],
 "autos": [
   ("Model QA", "live", "The standards pass before every issue, run as a rule set instead of a "
    "person opening views one at a time, with failures clustered by cause."),
   ("Clash intelligence", "live", "Findings classified by cause and responsible discipline rather "
    "than counted."),
   ("Engineering calculations from model data", "live", "Sizing and load calculation driven from "
    "model parameters and reconciled against the as-modelled network."),
   ("Documentation", "live", "Draft sheets and schedules derived from model state for engineering "
    "review."),
   ("Quantity intelligence", "live", "Measured from geometry, classified, every line traceable."),
   ("Design automation", "dev", "Generating model content from engineering intent and rules — "
    "routing, supports, penetrations, repeated typologies. In development and used on our own "
    "delivery; not offered as a product."),
 ],
 "nots": [
   "We do not deliver a routine without stating its false-positive rate.",
   "We do not build automation that commits changes to a live model unattended.",
   "We do not automate a workflow where the honest answer is that it is not worth automating — we "
   "will say so, and that has cost us work.",
   "We do not licence the internal intelligence layer. Routines built on your appointment are "
   "yours; the platform is not a product.",
 ],
 "faqs": [
   ("What can realistically be automated on a BIM project today?",
    "Model QA, clash classification, quantity extraction, documentation generation, parameter "
    "management and calculation reconciliation are live and running on client appointments now. "
    "Generative design content is in development and used internally. Anything further is roadmap "
    "and labelled as such on this site."),
   ("How do you price an automation engagement?",
    "Against the defined workflow and its deliverable — the rule set, the routine, the "
    "documentation and the engineering behind it. Not as a licence, because there is no product to "
    "licence."),
   ("What is a false-positive rate and why do you publish it?",
    "It is the proportion of findings a checking routine raises that turn out on review to be "
    "wrong. Every rule set has one. A provider who does not state theirs is asking you to trust a "
    "checker you cannot evaluate, and we think that is the wrong way round."),
   ("Does automation replace engineers?",
    "It replaces the part of an engineer's day spent doing something a rule could do more "
    "consistently. The engineering judgement about what to check, at what threshold, and what a "
    "finding means is the part that is not automatable — and it is also the part that carries the "
    "liability."),
   ("Will you tell us if a workflow is not worth automating?",
    "Yes, and we do. A routine that takes four weeks to build and saves two hours a month is a bad "
    "trade, and saying so is cheaper for both parties than discovering it afterwards."),
 ],
 "related": [
   ("automation.html", "AI and automation",
    "The agents, the workflows and where the engineer signs."),
   ("technology/mcp-for-revit.html", "MCP for Revit",
    "What connecting an AI assistant to a model would require, and what it would not do."),
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "Where clash intelligence is applied on live appointments."),
   ("platform.html#status", "Capability status",
    "The four-state legend behind every badge on this page."),
 ],
 "prefill": "automation",
 "group": "automation",
},

# ---------------------------------------------------------------------------
{
 "slug": "construction-support-bim",
 "nav": "Construction support",
 "h1": "Construction support: shop drawings, builders work and as-built models",
 "title": "Shop Drawings, BWIC &amp; As-Built BIM | BIMRACE",
 "desc": "Model-derived construction support: shop and spool drawings, builders work and "
         "penetration drawings, bracket layouts and as-built models.",
 "eyebrow": "Construction support",
 "lede": "Output produced for the people installing the work, at the detail and tolerance "
         "installation actually requires — not at the level a design model happens to hold.",
 "meta": [("Status", "Live"), ("For", "Contractors · Subcontractors · Fabricators"),
          ("Output", "Shop &amp; spool drawings · BWIC · As-built"),
          ("Basis", "Model-derived")],
 "position": [
   ("A design model is not a fabrication model, and pretending otherwise is expensive",
    "The level of information need for installation is different in kind, not just in degree: real "
    "fittings rather than generic ones, real connection detail, real support positions, and "
    "tolerances that reflect what can actually be manufactured and carried through a door. "
    "Uprating a design model to fabrication is a scoped piece of work. It is not a setting."),
   ("Builders work has to be agreed before the slab is poured",
    "Penetrations, cast-in items and structural openings are the deliverable with the hardest "
    "deadline on the project and the one most often produced last. We take the coordinated model, "
    "extract every penetration, and issue it as a drawing and a schedule that the structural "
    "engineer can actually review — before the pour, not as an RFI afterwards."),
   ("As-built means what was installed, not what was designed",
    "A record model that is the design model with a new title block is a liability dressed as a "
    "handover deliverable. We update against site information and state clearly what has been "
    "verified and what has not, because an operator who trusts an unverified record model will "
    "find out the hard way."),
 ],
 "delivers": [
   ("Shop and fabrication drawings", "Discipline shop drawings at installation level of detail, "
    "derived from the coordinated model."),
   ("Spool and prefabrication drawings", "Assemblies broken down for offsite manufacture with "
    "piece marks and connection detail."),
   ("Builders work and penetration drawings", "Every penetration extracted from the coordinated "
    "model, dimensioned, scheduled and issued for structural review."),
   ("Bracket and support layouts", "Support positions and types set out against structure and the "
    "installed services."),
   ("As-built and record models", "Updated against site information with the verification status "
    "stated element by element."),
   ("Quantity take-off", "Measured from the model, classified, with each line traceable to the "
    "elements behind it."),
 ],
 "inputs": [
   "The coordinated design model, and who owns it",
   "Selected products and manufacturers — fabrication detail depends entirely on real products",
   "Installation tolerances and any offsite manufacture constraints",
   "The structural engineer's review requirements for builders work",
   "Site survey or verification data for as-built work",
 ],
 "process": [
   ("01", "Level of information need uplift", "Agree what has to be modelled to installation "
    "standard and what does not. This is the scope conversation and it has to be explicit."),
   ("02", "Product substitution", "Generic content replaced with the selected products, because "
    "fabrication detail is a property of the actual item."),
   ("03", "Re-coordination", "Re-run the clash and clearance rule sets against the uprated model. "
    "Real fittings clash where generic ones did not."),
   ("04", "Supports and penetrations", "Bracket layouts and penetration extraction, scheduled and "
    "issued for review."),
   ("05", "Production", "Shop, spool and BWIC drawings derived from model state."),
   ("06", "Record", "As-built updated against verified site information with status stated."),
 ],
 "autos": [
   ("Penetration extraction", "live", "Every service crossing a structural element identified and "
    "scheduled automatically across the federated model."),
   ("Quantity take-off", "live", "Measured from geometry and parameters, classified, with the "
    "measurement rule visible for each line."),
   ("Drawing and schedule generation", "live", "Shop drawing sheets and schedules derived from "
    "model state rather than drafted."),
   ("Support layout routines", "dev", "Generating bracket and support positions from routing and "
    "rules, for engineering review. In development on our own delivery."),
 ],
 "nots": [
   "We do not supervise or inspect installation on site.",
   "We do not certify as-built accuracy for elements we have not received verification data for — "
   "we state the verification status instead.",
   "We do not produce fabrication drawings against generic content; real products have to be "
   "selected first, and we will wait rather than guess.",
 ],
 "faqs": [
   ("Can you uprate our design model to fabrication level?",
    "Usually yes, and the honest answer depends on how the design model was authored. A model with "
    "a clean parameter schema and correct system assignment uprates economically. One without "
    "often costs more to uprate than to re-author, and we will tell you which case you are in "
    "before you commit."),
   ("Do you produce builders work drawings?",
    "Yes. Penetration extraction from the coordinated model is automated, and the output is a "
    "dimensioned drawing plus a schedule the structural engineer can review — issued before the "
    "pour rather than raised as an RFI after it."),
   ("Do you work directly for contractors and subcontractors?",
    "Yes. Construction support is most often appointed by the installing party rather than the "
    "design team, and the deliverable list above reflects that."),
   ("What makes an as-built model trustworthy?",
    "Stated verification status, element by element. A record model that does not distinguish "
    "between what was verified on site and what was carried over from design is worse than no "
    "record model, because it invites trust it has not earned."),
 ],
 "related": [
   ("services/bim-coordination-clash-detection.html", "BIM coordination",
    "The coordinated model construction support is derived from."),
   ("services/bim-modelling-documentation.html", "BIM modelling",
    "Why the authoring standard decides whether an uplift is economic."),
   ("services/bim-automation-services.html", "BIM automation",
    "Penetration extraction and quantity take-off as routines."),
   ("industries/industrial.html", "Industrial and warehousing",
    "Where prefabrication and offsite manufacture pay back hardest."),
 ],
 "prefill": "bim_consulting",
 "group": "construction",
},
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}
