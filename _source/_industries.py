"""
BIMRACE — sector landing page content.

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    A sector page that is the previous sector page with the building type
    renamed is a doorway page. Each entry below has to answer one question
    that is only true of that sector: what specifically makes coordination
    hard here, which discipline dominates, what the information requirement
    looks like, and where automation earns its place.

    None of these pages claims completed projects in the sector. The site
    publishes no client work until a client releases it, and that rule
    applies here too — these pages describe capability and workflow fit,
    and say so explicitly.
"""

# slug, nav, h1, title, desc, eyebrow, lede, meta
# profile   — [(heading, paragraph)] the sector argument, 2-3 blocks
# drivers   — [(name, detail)] what actually drives coordination difficulty
# lead_disc — the discipline that dominates, and why (one sentence)
# info_req  — [str] information requirements characteristic of the sector
# autos     — [(name, status, text)]
# faqs, related, services

INDUSTRIES = [

{
 "slug": "commercial",
 "nav": "Commercial &amp; offices",
 "h1": "MEP engineering and BIM for commercial and office projects",
 "title": "Commercial &amp; Office MEP and BIM | BIMRACE",
 "desc": "MEP engineering and BIM for commercial and office buildings: core and shell, fit-out, "
         "ceiling void congestion and repeated tenant coordination cycles.",
 "eyebrow": "Commercial &amp; offices",
 "lede": "The sector where the same ceiling void is coordinated four times, for four different "
         "tenants, against a core-and-shell design that was fixed before any of them existed.",
 "meta": [("Dominant constraint", "Ceiling void depth"), ("Cycles", "Repeated per tenant"),
          ("Where automation pays", "Re-checking after change"),
          ("Disciplines", "M · E · P · FP")],
 "profile": [
   ("The cost is in the re-coordination, not the coordination",
    "A core-and-shell design is coordinated once. Then every fit-out re-coordinates the same void "
    "against a new ceiling layout, new small power, new terminal positions and a new tenant "
    "specification — against a shell that cannot move. The first coordination is a project. The "
    "fourth is the same project again with a different architect, and it is where the margin goes. "
    "Rule-based checking changes the economics of that fourth pass specifically, because the rule "
    "set was already written and the eleventh run costs what the first one did."),
   ("Landlord and tenant interfaces are an information problem",
    "The recurring failure is not geometric, it is about who owns what. A terminal unit the "
    "landlord installed and the tenant modified, a riser capacity allocated but not recorded, a "
    "board with spare ways that three fit-outs have each assumed were theirs. These are answerable "
    "from a model that carries system and ownership data on the elements, and unanswerable from "
    "one that does not."),
 ],
 "drivers": [
   ("Ceiling void depth", "Usually fixed by the shell before the fit-out brief exists, and the "
    "single constraint every subsequent coordination cycle works inside."),
   ("Element count", "High, repetitive and heavily scheduled — which is the condition under which "
    "manual checking degrades fastest and rule-based checking performs best."),
   ("Tenant variation", "Each fit-out is a new coordination against an unchanged shell, so the "
    "marginal cost of re-checking dominates the total."),
   ("Riser and capacity allocation", "Shared vertical capacity allocated across tenants, where the "
    "record of what has been committed is more valuable than the geometry."),
 ],
 "lead_disc": "Mechanical usually sets the void, and electrical absorbs the consequences — but the "
              "coordination effort concentrates in the interface between landlord and tenant scope.",
 "info_req": [
   "System and ownership data on every element, so landlord and tenant scope is queryable",
   "Riser capacity allocation recorded against the model rather than in a spreadsheet",
   "Ceiling zone allocation agreed and modelled as a constraint, not as an intention",
   "Fit-out models federated against the retained shell model on every cycle",
 ],
 "autos": [
   ("Re-checking after change", "live", "The rule set that was written for the shell coordination "
    "re-runs against each fit-out at a fraction of the original cost. This is the clearest "
    "commercial case for rule-based checking anywhere in the sector list."),
   ("Ceiling zone compliance", "live", "Every element tested against its allocated zone, so zone "
    "encroachment is a finding rather than a discovery."),
   ("Schedule and quantity extraction", "live", "High element counts with heavy scheduling is "
    "exactly the condition automated extraction is for."),
 ],
 "faqs": [
   ("Do you work on fit-out as well as core and shell?",
    "Yes, and the fit-out case is usually the stronger one for our approach, because the rule set "
    "written during shell coordination is reusable on every subsequent tenant at very little "
    "marginal cost."),
   ("Can you coordinate a fit-out against a landlord model we did not author?",
    "Yes. We check the incoming model's health on receipt and will report where it is not in a "
    "state that can be coordinated, which is information worth having early even when it is "
    "unwelcome."),
   ("Have you delivered commercial projects?",
    "This page describes the discipline mix and workflow fit for the sector. This site publishes "
    "no project history until a client releases it, and that rule applies here. If you want "
    "evidence rather than a description, ask at enquiry stage and we will screen-share live "
    "workflows and QA output under NDA."),
 ],
 "services": ["mep-engineering-services", "bim-coordination-clash-detection",
              "bim-automation-services", "electrical-bim-services"],
},

{
 "slug": "residential",
 "nav": "Residential &amp; mixed use",
 "h1": "MEP engineering and BIM for residential and mixed-use projects",
 "title": "Residential &amp; Mixed-Use MEP and BIM | BIMRACE",
 "desc": "MEP and BIM for residential and mixed use: repeatable unit typologies, riser "
         "coordination and documentation volume at scale.",
 "eyebrow": "Residential &amp; mixed use",
 "lede": "Repetition is usually described as the easy part of residential. It is actually the part "
         "that decides whether the project is efficient or expensively wrong two hundred times.",
 "meta": [("Dominant constraint", "Riser coordination"), ("Character", "High repetition"),
          ("Where automation pays", "Typology validation"),
          ("Volume", "Documentation-heavy")],
 "profile": [
   ("An error in a typology is an error in every instance of it",
    "This is the defining property of residential work and it cuts both ways. Get the unit typology "
    "right and the rest of the building is a placement exercise. Get a clearance wrong in the "
    "bathroom pod and it is wrong in four hundred apartments, discovered on site, in all of them. "
    "The engineering effort therefore belongs almost entirely at typology stage, and the checking "
    "effort belongs in proving that every instance actually matches the typology it claims to be — "
    "which is a comparison across hundreds of near-identical assemblies and precisely the kind of "
    "work people do badly and rule sets do well."),
   ("Risers are where mixed use actually gets difficult",
    "Residential above retail or amenity means vertical services passing through a transfer level "
    "into a completely different structural and spatial logic. Riser position is effectively "
    "immovable once the cores are set, the drainage cannot deviate, and the transfer level is "
    "where every discipline's constraint arrives at once. It is worth more engineering attention "
    "than the four hundred repeated floors above it."),
 ],
 "drivers": [
   ("Typology repetition", "The dominant characteristic. Effort concentrates at typology design; "
    "risk concentrates in instance-to-typology drift."),
   ("Riser and transfer coordination", "The one genuinely hard spatial problem, usually at the "
    "podium-to-tower transfer level."),
   ("Documentation volume", "Very high sheet counts with low variation — the ideal case for "
    "model-derived documentation."),
   ("Gravity drainage", "Stack positions fix the architectural cores and cannot be traded away "
    "later."),
 ],
 "lead_disc": "Public health dominates the immovable decisions; documentation volume dominates the "
              "production cost.",
 "info_req": [
   "Typology defined as an assembly with its data schema, not as a drawing",
   "Every instance traceable to its typology so drift is detectable",
   "Riser allocation fixed and modelled before the cores are frozen",
   "Sheet and view standards that support very high documentation volume without hand-assembly",
 ],
 "autos": [
   ("Typology conformance checking", "live", "Every instance tested against its declared typology, "
    "so one apartment that was locally modified in month four is a finding rather than a site "
    "discovery."),
   ("Documentation generation", "live", "High sheet counts with low variation is the strongest "
    "case on any project type for deriving sheets and schedules from model state."),
   ("Quantity extraction", "live", "Repetition makes model-measured quantities both reliable and "
    "valuable, with each line traceable."),
   ("Generated content from typology rules", "dev", "Producing repeated assemblies from engineering "
    "intent and rules. In development and used on our own delivery, not offered as a product."),
 ],
 "faqs": [
   ("Is repetition an advantage or a risk?",
    "Both, and which one you get depends entirely on whether instance-to-typology conformance is "
    "actually checked. Unchecked, repetition multiplies a single error. Checked as a rule set, it "
    "is the cheapest engineering condition there is."),
   ("Can you handle very high drawing volumes?",
    "Yes, and it is the wrong question to ask a provider. The right question is whether the "
    "drawings are derived from model state or drafted alongside it, because only the first scales "
    "without proportionally more people and proportionally more drift."),
   ("Do you work on the podium and transfer levels as well as the tower?",
    "Yes, and we would argue the transfer level deserves a disproportionate share of the "
    "engineering attention on a mixed-use project — it is where every discipline's hardest "
    "constraint arrives simultaneously."),
 ],
 "services": ["plumbing-public-health-bim", "bim-modelling-documentation",
              "bim-automation-services", "mep-engineering-services"],
},

{
 "slug": "healthcare",
 "nav": "Healthcare",
 "h1": "MEP engineering and BIM for healthcare projects",
 "title": "Healthcare MEP &amp; BIM Services | BIMRACE",
 "desc": "MEP and BIM for healthcare: dense services, strict clearance and maintenance access, "
         "and validation that makes evidence part of the deliverable.",
 "eyebrow": "Healthcare",
 "lede": "The sector where clearance and maintenance access matter more than hard clashes, and "
         "where the evidence that a check was performed is part of what is being bought.",
 "meta": [("Dominant constraint", "Clearance &amp; access"), ("Character", "Services-dense"),
          ("Where automation pays", "Evidenced checking"),
          ("Disciplines", "M · E · P · FP · specialist")],
 "profile": [
   ("Access failures outnumber collisions, and cost more",
    "In a healthcare ceiling void the services do not usually collide — they are drawn by "
    "competent people and the hard clashes get resolved. What fails is access: a damper above a "
    "sealed clean-room ceiling, an isolating valve behind a permanent bulkhead, a filter that "
    "cannot be changed without taking a department out of service. None of these appear in a clash "
    "report, all of them are geometric, and all of them are testable as explicit clearance rules. "
    "This is the sector where the difference between clash detection and coordination is most "
    "expensive to get wrong."),
   ("Validation makes the evidence a deliverable",
    "Healthcare projects are routinely asked to demonstrate that a check was carried out, not just "
    "to assert that it was. A manual check by a competent engineer produces a resolved model and "
    "very little evidence. A rule set produces a resolved model, a written threshold, an element "
    "ID against every finding and a re-test that proves closure. The second is worth more in this "
    "sector than the difference in effort between them."),
 ],
 "drivers": [
   ("Maintenance and replacement access", "Access to dampers, valves, filters and plant while the "
    "department remains operational — the dominant constraint."),
   ("Services density", "Medical gases, specialist ventilation and high electrical resilience on "
    "top of a normal MEP load."),
   ("Clearance tolerance", "Tighter than commercial work, and frequently specified rather than "
    "inferred."),
   ("Validation expectation", "Evidence of checking, not assertion of checking."),
   ("Compartmentation", "Extensive, with every crossing service needing a sealed, accessible "
    "penetration."),
 ],
 "lead_disc": "Mechanical and specialist ventilation dominate the spatial problem; the coordination "
              "effort concentrates in access rather than in collision.",
 "info_req": [
   "Clearance and access requirements stated as dimensioned zones, not as specification prose",
   "Compartment lines in the federated model as geometry",
   "Room data sheets with the engineering criteria attached to the model rooms",
   "Asset and maintenance attributes populated during authoring for handover",
 ],
 "autos": [
   ("Clearance and access rule sets", "live", "Damper, valve, filter and plant access tested "
    "geometrically across the whole federated model — the check a clash engine structurally cannot "
    "perform."),
   ("Evidenced QA reporting", "live", "An element ID against every finding and a re-test against "
    "every closure, which is the form validation actually asks for."),
   ("Compartment penetration detection", "live", "Every service crossing a compartment boundary "
    "identified and scheduled across all disciplines."),
   ("Parameter completeness for handover", "live", "Asset attributes tested for completeness "
    "before issue rather than assembled afterwards."),
 ],
 "faqs": [
   ("Why do you emphasise access over clash detection in healthcare?",
    "Because in a services-dense ceiling void the hard clashes get found and fixed, and the access "
    "failures do not — they are invisible to a clash engine and only surface once the ceiling is "
    "closed and a filter needs changing. They are entirely testable as clearance rules, which is "
    "why we write those rules down and run them."),
   ("Can you support a validation or verification requirement?",
    "We can produce the evidence: written thresholds, an element ID against every finding, and a "
    "re-test against every closure. We are not a validation authority and do not certify — the "
    "responsible party does that, and our output is what they need in order to."),
   ("Do you have healthcare project experience?",
    "This page describes discipline fit and workflow, not project history. This site publishes no "
    "project history until a client releases it. If you need evidence of capability at enquiry "
    "stage, ask for a working session — we will show the rule sets and live QA output under NDA."),
   ("Do you work on medical gas systems?",
    "We can model and coordinate medical gas distribution as part of an MEP appointment. Specialist "
    "medical gas design, certification and commissioning sit with an appropriately accredited "
    "specialist, and we would say so rather than absorb that scope."),
 ],
 "services": ["mep-engineering-services", "bim-coordination-clash-detection",
              "fire-protection-bim-services", "plumbing-public-health-bim"],
},

{
 "slug": "data-centres",
 "nav": "Data centres",
 "h1": "MEP engineering and BIM for data centre projects",
 "title": "Data Centre MEP &amp; BIM Services | BIMRACE",
 "desc": "MEP and BIM for data centres: high-density mechanical and electrical distribution, "
         "where parameter and sizing consistency is the dominant risk.",
 "eyebrow": "Data centres",
 "lede": "The highest services density we work at, where the dominant risk is not spatial conflict "
         "but sizing and parameter inconsistency across a large repeated electrical and mechanical "
         "topology.",
 "meta": [("Dominant constraint", "Tolerance &amp; consistency"),
          ("Character", "High-density M&amp;E"),
          ("Where automation pays", "Parameter &amp; sizing consistency"),
          ("Disciplines", "M · E dominant")],
 "profile": [
   ("Consistency is the risk, not collision",
    "A data hall is a repeated topology: the same containment arrangement, the same cooling "
    "approach, the same distribution pattern, many times over. Spatial conflict in that topology "
    "gets resolved early because it is obvious. What does not get caught is the eleventh row where "
    "a busbar rating, a cable size or a CRAC duty was carried over from a revision that changed — "
    "consistent-looking, wrong, and invisible to a geometric test. The dominant delivery risk in "
    "this sector is parameter consistency across instances, and it is a data problem with a data "
    "solution."),
   ("Resilience topology has to be readable from the model",
    "N+1, 2N and the distinction between A and B paths are properties of how systems are assigned, "
    "not of how the geometry looks. A model in which the A and B electrical paths cannot be "
    "separated by query is a model that cannot be used to check the resilience claim — and the "
    "resilience claim is essentially the product being sold. System assignment discipline is worth "
    "more here than anywhere else we work."),
 ],
 "drivers": [
   ("Repeated topology", "High instance counts of near-identical arrangements — consistency, not "
    "geometry, is the risk."),
   ("Resilience paths", "A and B separation has to be queryable, not just drawn."),
   ("Containment density", "Very high, with strict separation and fill requirements."),
   ("Cooling distribution", "Tight tolerance against containment and structure, at density."),
   ("Change control", "Late equipment selection changes propagate through the whole topology."),
 ],
 "lead_disc": "Electrical and mechanical are co-dominant, and the coordination effort concentrates "
              "in parameter and sizing consistency rather than in spatial resolution.",
 "info_req": [
   "System assignment that separates resilience paths as a queryable property",
   "Sizing and rating parameters populated on every element, not held in a parallel schedule",
   "Instance-to-template traceability across repeated arrangements",
   "A change process that re-runs the consistency checks rather than sampling them",
 ],
 "autos": [
   ("Parameter consistency across instances", "live", "Every instance of a repeated arrangement "
    "compared against its template, so the one row that carries a superseded rating is a finding."),
   ("Sizing reconciliation", "live", "Calculated against as-modelled, element by element, across "
    "the whole topology."),
   ("Separation and fill rule sets", "live", "Containment separation, segregation class and fill "
    "tested geometrically at density."),
   ("Resilience path querying", "dev", "Reading system assignment to test A and B path separation "
    "as a property of the model. In development on our own delivery."),
 ],
 "faqs": [
   ("What is the biggest BIM risk on a data centre project?",
    "Not clashes. It is parameter and sizing inconsistency across repeated arrangements — a rating, "
    "a size or a duty carried over from a superseded revision into one instance out of forty. It "
    "looks correct, passes every geometric test, and is found at commissioning. It is caught "
    "cheaply by comparing instances against the template as a rule."),
   ("Can you check resilience path separation?",
    "Only if the model was authored with system assignment that makes A and B distinguishable. "
    "Where it was, testing the separation is straightforward. Where it was not, the honest answer "
    "is that the model cannot answer the question and we will say so rather than produce a check "
    "that means nothing."),
   ("Do you have data centre project experience?",
    "This page describes discipline fit and the workflow we would apply. This site publishes no "
    "project history until a client releases it. For evidence at enquiry stage, ask for a working "
    "session under NDA."),
 ],
 "services": ["electrical-bim-services", "hvac-bim-services",
              "bim-automation-services", "bim-coordination-clash-detection"],
},

{
 "slug": "industrial",
 "nav": "Industrial &amp; warehousing",
 "h1": "MEP engineering and BIM for industrial and warehouse projects",
 "title": "Industrial &amp; Warehouse MEP and BIM | BIMRACE",
 "desc": "MEP and BIM for industrial and warehousing — long-span structures, process services and "
         "the recurring conflict between fire protection routing and structural bracing.",
 "eyebrow": "Industrial &amp; warehousing",
 "lede": "Long spans, few ceilings, and one conflict that recurs so predictably it should be "
         "designed for at zoning stage rather than resolved forty times at coordination stage.",
 "meta": [("Dominant constraint", "Structure vs fire protection"),
          ("Character", "Long-span, repetitive bay"),
          ("Where automation pays", "Bay-level repetition"),
          ("Disciplines", "FP · M · E · process")],
 "profile": [
   ("The structure–sprinkler conflict is predictable, so design for it",
    "In a long-span portal or truss structure, the sprinkler main and the structural bracing want "
    "the same envelope, bay after bay after bay. Because the structural bay is repeated, the "
    "conflict is repeated, and because it is repeated it is not really forty coordination problems "
    "— it is one zoning decision made once and applied everywhere. Projects that treat it as forty "
    "problems spend forty times as long on it and get a different answer in some of the bays."),
   ("Process services are an interface problem, not a services problem",
    "Where a building serves a process, the boundary between building services and process services "
    "is where information goes missing: connection points, loads, tolerances and responsibility. "
    "The coordination difficulty is rarely geometric. It is that two parties hold different "
    "versions of the interface and neither has it in the model."),
 ],
 "drivers": [
   ("Long-span structural bracing", "The recurring conflict with fire protection distribution."),
   ("Bay repetition", "The same coordination condition many times — solve once, apply everywhere."),
   ("Process interfaces", "Connection points, loads and responsibility boundaries."),
   ("Fire protection scale", "Large coverage areas with high-hazard classifications and "
    "correspondingly large distribution."),
   ("Few ceilings", "Services are visible and their arrangement is part of the finished condition."),
 ],
 "lead_disc": "Fire protection routing against structure is the dominant coordination problem, with "
              "process interfaces the dominant information problem.",
 "info_req": [
   "Structural bay geometry available early enough to zone against",
   "Hazard classification fixed before sprinkler distribution is routed",
   "Process interface points modelled and owned, with responsibility stated",
   "Support and bracket requirements treated as a deliverable, since services are exposed",
 ],
 "autos": [
   ("Bay-level conformance", "live", "One bay coordinated properly, then every other bay tested "
    "against it as a rule — which is the whole economic argument in this sector."),
   ("Clearance against structure", "live", "Distribution against bracing and truss members tested "
    "geometrically across every bay."),
   ("Penetration extraction", "live", "Services crossing structural elements identified and "
    "scheduled automatically."),
   ("Support layout routines", "dev", "Bracket and support positions generated from routing and "
    "rules for engineering review. In development on our own delivery."),
 ],
 "faqs": [
   ("Why does fire protection dominate industrial coordination?",
    "Because the distribution is large, the coverage areas are large, the hazard classification is "
    "often high, and the structure it has to pass through is a repeated bracing pattern that leaves "
    "very little envelope. It is the conflict that recurs, and recurrence is what makes it worth "
    "solving as a zoning rule rather than forty times by hand."),
   ("Can you coordinate process services?",
    "We coordinate the building services and the interface to the process — connection points, "
    "loads, spatial allocation and responsibility. The process design itself belongs to the process "
    "engineer, and we would not absorb that scope."),
   ("Is BIM worth it on a warehouse?",
    "Sometimes not, and we will say so. On a simple shed with light services the honest answer can "
    "be that the modelling effort exceeds the coordination benefit. Where there is high-hazard fire "
    "protection, process services or significant prefabrication, the answer changes completely."),
 ],
 "services": ["fire-protection-bim-services", "construction-support-bim",
              "bim-coordination-clash-detection", "mep-engineering-services"],
},

{
 "slug": "hospitality",
 "nav": "Hospitality",
 "h1": "MEP engineering and BIM for hospitality projects",
 "title": "Hotel &amp; Hospitality MEP and BIM | BIMRACE",
 "desc": "MEP and BIM for hotels: guest room typology repetition, back-of-house density and "
         "finish-critical ceiling coordination.",
 "eyebrow": "Hospitality",
 "lede": "Two buildings in one: a repeated guest-room typology where the engineering is decided "
         "once, and a back-of-house where the services density rivals healthcare.",
 "meta": [("Dominant constraint", "Finish-critical ceilings"),
          ("Character", "Typology + dense BOH"),
          ("Where automation pays", "Typology conformance"),
          ("Disciplines", "M · P · FP · E")],
 "profile": [
   ("Front of house is a coordination problem with an architectural veto",
    "In guest areas, every visible element — sprinkler head, diffuser, detector, downlight — is an "
    "architectural decision as much as an engineering one, and the setting-out is negotiated "
    "against a reflected ceiling plan that the operator's brand standard constrains. The usual "
    "failure is that the engineering layout satisfies the code and the ceiling layout satisfies the "
    "brand, and the two were never reconciled in the same model. Coverage and spacing then become "
    "the casualty of a late compromise."),
   ("Back of house is where the services actually are",
    "Kitchens, laundry, plant and service corridors carry a density comparable to healthcare, in a "
    "fraction of the floor area, with extract, grease duct, gas and drainage all competing for the "
    "same routes and all subject to access and cleaning requirements. Projects that spend their "
    "coordination effort proportionally to floor area get this backwards."),
 ],
 "drivers": [
   ("Brand standard ceilings", "Visible element setting-out is negotiated, not free."),
   ("Guest room typology", "High repetition; effort concentrates at typology stage."),
   ("Back-of-house density", "Kitchen and laundry extract, grease duct routing and access."),
   ("Acoustic separation", "Services crossing between guest rooms and plant, with real "
    "consequences."),
   ("Operational access", "Maintenance without taking guest floors out of service."),
 ],
 "lead_disc": "Mechanical extract and fire protection dominate back of house; the front-of-house "
              "problem is a reconciliation problem between engineering layout and ceiling design.",
 "info_req": [
   "Reflected ceiling plans federated with the services model, not reviewed as separate drawings",
   "Guest room typology defined as an assembly with its data schema",
   "Grease duct and kitchen extract routes with access and cleaning clearance modelled",
   "Acoustic requirements expressed as constraints against the model, not only in a specification",
 ],
 "autos": [
   ("Typology conformance", "live", "Every guest room instance tested against its declared "
    "typology, so a local modification does not silently become four hundred."),
   ("Coverage and spacing checking", "live", "Sprinkler and detector coverage tested against the "
    "actual ceiling layout, which is where the engineering-versus-brand compromise shows up."),
   ("Access clearance in back of house", "live", "Cleaning and maintenance access to extract and "
    "grease duct tested as rules at the density where it matters."),
   ("Documentation generation", "live", "High repetition with high sheet counts — the standard case "
    "for model-derived documentation."),
 ],
 "faqs": [
   ("How do you handle the conflict between brand standard ceilings and sprinkler coverage?",
    "By testing coverage against the actual reflected ceiling plan inside the federated model, "
    "early and repeatedly, so the conflict is a finding at the point it can still be negotiated "
    "rather than a compliance problem after the ceiling is signed off."),
   ("Is back of house a separate appointment?",
    "It does not need to be, but it should be scoped deliberately. The services density in back of "
    "house per square metre is far higher than front of house, and pricing coordination by floor "
    "area rather than by density is how hospitality appointments end up underquoted."),
   ("Do you model kitchen and laundry extract?",
    "Yes, including grease duct routing with cleaning access as a modelled clearance requirement. "
    "The access requirement is the part most often omitted and the part that causes the "
    "operational problem."),
 ],
 "services": ["hvac-bim-services", "fire-protection-bim-services",
              "bim-modelling-documentation", "mep-engineering-services"],
},

{
 "slug": "education",
 "nav": "Education",
 "h1": "MEP engineering and BIM for education projects",
 "title": "Education MEP &amp; BIM Services | BIMRACE",
 "desc": "MEP and BIM for schools, colleges and universities: phased delivery on live campuses, "
         "standard room types and ventilation-led services.",
 "eyebrow": "Education",
 "lede": "Phased delivery on a site that cannot close makes model status and revision discipline "
         "more important than coordination complexity — which is an information management problem, "
         "not an engineering one.",
 "meta": [("Dominant constraint", "Phasing &amp; status"),
          ("Character", "Standard room types"),
          ("Where automation pays", "Status &amp; revision control"),
          ("Disciplines", "M dominant · E · P · FP")],
 "profile": [
   ("Phasing turns information management into the primary risk",
    "A campus that stays operational through construction means the model represents several "
    "different states of the building at once: what exists, what is being built this summer, what "
    "is demolished next year, and what the end state looks like. The engineering is rarely the hard "
    "part. The hard part is that a contractor working from a drawing at the wrong status, for the "
    "wrong phase, will build something correct for a different year. Phase and status have to be "
    "properties of elements in the model, and they have to be checked, because they are not "
    "visually obvious."),
   ("Ventilation leads, and it leads the architecture",
    "Education services are ventilation-dominated, and in naturally or mixed-mode ventilated "
    "buildings the strategy is an architectural decision with engineering consequences — facade "
    "openings, cross-ventilation paths, acoustic attenuation, and where that fails, the fallback "
    "mechanical provision. Standardised room types make the analysis tractable, and repeated room "
    "types make the checking cheap."),
 ],
 "drivers": [
   ("Phased delivery", "Multiple building states in one model; status and phase discipline is the "
    "dominant risk."),
   ("Room type standardisation", "Classroom, lab and hall typologies repeat and can be validated "
    "as a set."),
   ("Ventilation strategy", "Natural, mixed-mode or mechanical, with acoustic and facade "
    "consequences."),
   ("Live site constraints", "Works within an operating campus, with access and isolation "
    "requirements."),
   ("Specialist rooms", "Science labs, workshops and kitchens carry services out of proportion to "
    "their area."),
 ],
 "lead_disc": "Mechanical ventilation leads the engineering; information management leads the risk.",
 "info_req": [
   "Phase and status as element properties, tested rather than assumed",
   "Room type definitions carrying their engineering criteria",
   "Existing conditions captured to a stated accuracy, with what is unverified marked as such",
   "A drawing register that makes the phase and status of every issued sheet unambiguous",
 ],
 "autos": [
   ("Status and phase checking", "live", "Every element tested for correct phase and status "
    "assignment before issue — the check that prevents building next year's scheme this summer."),
   ("Room type conformance", "live", "Each room instance validated against its declared type and "
    "engineering criteria."),
   ("Naming and revision compliance", "live", "Views, sheets and issued documents tested against "
    "the project convention automatically."),
   ("Model health across phases", "live", "Reporting that distinguishes existing, demolished and "
    "proposed rather than reporting on the file as a whole."),
 ],
 "faqs": [
   ("Why do you treat phasing as the main risk in education?",
    "Because the engineering in most education buildings is well understood, and the expensive "
    "failures come from information rather than design — a sheet issued at the wrong status, an "
    "element assigned to the wrong phase, a contractor building the correct detail for a different "
    "year. Those are checkable as rules, and rarely checked."),
   ("Can you work on live campus projects with summer works windows?",
    "Yes. The deliverable discipline that matters is status and phase control, and that is "
    "something we test rather than rely on people remembering under programme pressure."),
   ("Do you assess natural ventilation strategies?",
    "We support the strategy with engineering input and model it, including the mechanical fallback "
    "provision. Detailed dynamic thermal or CFD analysis sits with a specialist and we would say so "
    "rather than absorb the scope."),
 ],
 "services": ["hvac-bim-services", "bim-modelling-documentation",
              "mep-engineering-services", "bim-automation-services"],
},

{
 "slug": "retail",
 "nav": "Retail",
 "h1": "MEP engineering and BIM for retail projects",
 "title": "Retail Fit-Out MEP &amp; BIM Services | BIMRACE",
 "desc": "MEP and BIM for retail fit-out: landlord and tenant interfaces, compressed programmes "
         "and model-derived documentation that keeps pace.",
 "eyebrow": "Retail",
 "lede": "Programmes measured in weeks against a landlord shell that cannot change — which makes "
         "documentation speed, not coordination depth, the thing that decides whether the "
         "appointment works.",
 "meta": [("Dominant constraint", "Programme"), ("Character", "Repeat fit-out cycles"),
          ("Where automation pays", "Documentation speed"),
          ("Disciplines", "M · E · FP")],
 "profile": [
   ("A short programme changes which capability matters",
    "On a retail fit-out there is often less to coordinate than on any other project type and far "
    "less time to do it in. The provider who wins is not the one with the deepest coordination "
    "capability — it is the one who can turn a landlord shell, a tenant layout and a brand standard "
    "into a coordinated model and a complete drawing set inside the programme. That is a "
    "documentation production problem, and documentation production is the thing most easily and "
    "most completely automated."),
   ("The landlord interface is the recurring source of surprise",
    "Capped-off services that are not where the demise drawing says, a board with fewer spare ways "
    "than allocated, a condensate route that three previous tenants each assumed was available. "
    "The engineering response is unremarkable; the value is in establishing the actual interface "
    "condition fast and recording it against the model so the next fit-out inherits the truth "
    "rather than the demise drawing."),
 ],
 "drivers": [
   ("Programme compression", "Weeks, not months. Documentation throughput decides the outcome."),
   ("Landlord interface accuracy", "The demise condition is frequently not what the drawing says."),
   ("Brand standards", "Fixed ceiling and lighting arrangements that engineering has to fit "
    "around."),
   ("Shopfront coordination", "Facade, signage, entrance conditioning and fire protection at one "
    "interface."),
   ("Repeat roll-out", "The same brand, many units — repetition across sites rather than within "
    "one."),
 ],
 "lead_disc": "Mechanical and electrical carry most of the work, but the constraint is programme "
              "rather than discipline.",
 "info_req": [
   "The actual demise condition captured and recorded against the model, not assumed from the "
   "demise drawing",
   "Brand standard ceiling and lighting arrangement as geometry",
   "A template and content set that makes a new unit a placement exercise, not a new project",
   "Sheet standards that let a complete drawing set be produced from model state in days",
 ],
 "autos": [
   ("Documentation generation", "live", "The highest-value automation in this sector by a wide "
    "margin — a complete set derived from model state rather than drafted under programme "
    "pressure."),
   ("Roll-out template conformance", "live", "For repeat brands, each new unit validated against "
    "the standard arrangement so deviation is deliberate rather than accidental."),
   ("Quantity extraction", "live", "Fast, model-measured quantities for pricing inside a "
    "compressed programme."),
   ("Model QA before issue", "live", "The standards pass run as a rule set, which is the only "
    "version of QA that survives a three-week programme."),
 ],
 "faqs": [
   ("Can you deliver inside a three or four week fit-out programme?",
    "That depends almost entirely on whether a template and content set already exists for the "
    "brand. With one, a new unit is a placement and documentation exercise and the programme is "
    "achievable. Without one, the first unit builds the kit and the second onwards is fast. We "
    "would rather set that expectation at enquiry stage than miss a date."),
   ("Do you work for retail roll-out programmes across multiple sites?",
    "Yes, and it is the strongest case in this sector for the template-and-conformance approach — "
    "the engineering is decided once and every subsequent unit is validated against it."),
   ("What if the landlord's information is wrong?",
    "It frequently is. We capture the actual condition, record it against the model and report the "
    "difference. That record is worth more to the next fit-out than the demise drawing was."),
 ],
 "services": ["bim-modelling-documentation", "bim-automation-services",
              "mep-engineering-services", "electrical-bim-services"],
},
]

INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}
