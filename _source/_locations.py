"""
BIMRACE — international market page content.

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    BIMRACE is an India-based engineering studio delivering remotely.
    It has no office, no registered entity and no professional licensure
    in any of the markets below. Every page in this file says so, in the
    page body, above the fold-adjacent content — not in a footnote.

    A location page that implies local presence is a lie that is cheap to
    tell and expensive to be caught in, and it is the single most common
    form of dishonesty in this sector's international SEO. These pages
    exist because the regulatory context, the standards basis and the
    collaboration model genuinely differ by market, which is real
    information a buyer needs. They do not exist to rank for a city name.

    Standards and authority references below are general industry context,
    not legal advice and not a claim of accreditation.
"""

# slug, nav, h1, title, desc, eyebrow, lede, meta, cc (ISO country code for the form)
# intro      — [(heading, paragraph)]
# standards  — [(name, note)] the codes and standards basis engineering here is written to
# overlap    — working-hours statement, specific and checkable
# model      — [(name, detail)] how the collaboration actually runs
# honest     — [str] the licensure and presence boundary. Mandatory, never empty.
# typical    — [(name, detail)] the engagements that actually come from this market
# sectors    — industry slugs
# services   — service slugs
# faqs

LOCATIONS = [

{
 "slug": "usa",
 "nav": "United States",
 "cc": "US",
 "h1": "MEP engineering and BIM services for projects in the United States",
 "title": "MEP Engineering &amp; BIM Services for the USA | BIMRACE",
 "desc": "MEP engineering and BIM for US projects on ASHRAE, ICC and NFPA basis in imperial "
         "units, delivered remotely under your engineer of record.",
 "eyebrow": "United States",
 "lede": "Remote MEP engineering support and BIM production for US project teams, working to "
         "ASHRAE, ICC and NFPA basis in imperial units — under your engineer of record, never "
         "around them.",
 "meta": [("Model", "Remote delivery from India"), ("Units", "Imperial"),
          ("Basis", "ASHRAE · ICC · NFPA"), ("Licensure", "Yours, not ours")],
 "intro": [
   ("What US teams actually outsource, and why it goes wrong",
    "The work that comes to an offshore team from a US practice is rarely the design decision. It "
    "is the production: modelling to an established design, coordination cycles, documentation, "
    "shop drawing support and quantity extraction. That work fails offshore for one of two "
    "reasons — the team does not understand the code basis well enough to spot when the design "
    "they are modelling is wrong, or the model comes back in a state the US practice cannot "
    "maintain. We address the first with engineers rather than modellers, and the second by "
    "working inside your templates and standards and handing back documentation for anything we "
    "build."),
   ("Imperial is not a units setting",
    "Duct sizing conventions, pipe schedules, wire gauge, nominal dimensions and the rounding "
    "habits that make a drawing readable to a US installer are practice, not arithmetic. A model "
    "converted from metric at the end reads as foreign to the people who have to build from it. "
    "We author in imperial from the template onward on US appointments."),
 ],
 "standards": [
   ("ASHRAE", "Standard 90.1 for energy, 62.1 for ventilation, and the ASHRAE Handbook basis for "
    "load and system design."),
   ("ICC model codes", "IMC, IPC and IFC as adopted and amended by the state or jurisdiction — "
    "adoption varies, and which amendment applies is a project fact we ask for rather than assume."),
   ("NFPA", "NFPA 13 for sprinkler design basis and NFPA 70 (NEC) for electrical, as adopted "
    "locally."),
   ("BIMForum LOD", "Level of Development as the level-of-information-need vocabulary most US "
    "projects use. We agree it element by element rather than as a blanket project number."),
   ("COBie", "Where a federal, institutional or owner requirement calls for structured handover "
    "data, populated during authoring rather than assembled afterwards."),
 ],
 "overlap": "India is UTC+5:30. For US East Coast teams that is a working overlap of roughly two to "
            "three hours at the start of your day, and for West Coast teams a shorter one. The "
            "practical value is not the overlap — it is that work issued at your close of business "
            "is progressed overnight and is waiting when you open. We schedule a fixed daily "
            "handover rather than expecting ad-hoc availability, because an overlap nobody has "
            "agreed a time for is not an overlap.",
 "model": [
   ("Design support under your EOR", "We produce engineering design and BIM deliverables; your "
    "licensed engineer of record reviews, seals and submits. This is the only arrangement we offer "
    "in the US, and it is stated on every proposal."),
   ("Team extension", "Modelling and engineering capacity inside your environment, your templates "
    "and your BEP, for a defined period."),
   ("Package delivery", "A defined scope with a fixed deliverable list and schedule — a discipline "
    "model, a coordination package, a drawing set."),
   ("Overnight production cycle", "A fixed daily handover at your close of business, with a written "
    "note of what progressed, what is blocked and what needs a decision."),
 ],
 "honest": [
   "BIMRACE has no office, no registered entity and no employees in the United States.",
   "No BIMRACE engineer holds a Professional Engineer licence in any US state. We do not seal "
   "drawings, and we do not make submissions to any Authority Having Jurisdiction.",
   "All engineering we produce for US projects is design support delivered under a licensed "
   "engineer of record who reviews it and takes professional responsibility for it.",
   "We have no US certifications, accreditations or partnerships, and claim none.",
 ],
 "typical": [
   ("MEP production support for design firms", "Modelling, coordination and documentation to your "
    "design, at the LOD and schedule your project requires."),
   ("Contractor coordination support", "Federated coordination, clash and clearance rule sets and "
    "builders work extraction for the installing party."),
   ("Shop and spool drawing production", "Fabrication-level output derived from the coordinated "
    "model, for mechanical and fire protection subcontractors."),
   ("Automation for US practices", "A QA rule set, a quantity routine or a documentation pipeline "
    "built for your standards and handed over documented."),
 ],
 "sectors": ["commercial", "healthcare", "data-centres", "industrial"],
 "services": ["mep-engineering-services", "bim-coordination-clash-detection",
              "construction-support-bim", "bim-automation-services"],
 "faqs": [
   ("Can BIMRACE stamp drawings for a US project?",
    "No. No BIMRACE engineer holds a PE licence in any US state. We produce engineering design and "
    "BIM deliverables as design support, and your licensed engineer of record reviews, seals and "
    "submits. Any offshore provider telling you otherwise is describing something that is not "
    "legal in any US jurisdiction."),
   ("Do you have a US office?",
    "No. BIMRACE is an India-based practice delivering remotely. We do not list a US address, a US "
    "phone number or a US entity, because we do not have one."),
   ("How do you handle the time difference?",
    "With a fixed daily handover rather than an expectation of overlap. Work issued at your close "
    "of business is progressed overnight, with a written note of progress, blockers and decisions "
    "needed waiting when you open. Live calls are scheduled in the morning-Eastern window."),
   ("Do you work in imperial units?",
    "Yes, from the template onward on US appointments — including the sizing conventions, nominal "
    "dimensions and rounding practice that make a drawing readable to a US installer. Converting "
    "at the end produces a model that reads as foreign to the people building from it."),
   ("Which code basis do you design to?",
    "The one adopted in the project's jurisdiction, which we ask for rather than assume. ICC model "
    "code adoption and amendment varies by state and municipality, and designing to the wrong "
    "amendment is a real failure mode rather than a theoretical one."),
 ],
},

{
 "slug": "uk",
 "nav": "United Kingdom",
 "cc": "GB",
 "h1": "MEP engineering and BIM services for projects in the United Kingdom",
 "title": "MEP Engineering &amp; BIM Services for the UK | BIMRACE",
 "desc": "MEP engineering and BIM for UK projects on CIBSE and Building Regulations basis, with "
         "ISO 19650 information management and RIBA stage alignment.",
 "eyebrow": "United Kingdom",
 "lede": "The market where the information management standard we already work to is the national "
         "expectation rather than an aspiration — which makes the collaboration model unusually "
         "straightforward.",
 "meta": [("Model", "Remote delivery from India"), ("Units", "Metric"),
          ("Basis", "CIBSE · Building Regs · BS EN"), ("Information", "ISO 19650")],
 "intro": [
   ("ISO 19650 is the reason UK work fits this practice well",
    "We structure delivery to ISO 19650 principles on every appointment regardless of whether a "
    "client mandates it — naming, status codes, federation strategy, level of information need and "
    "the information container discipline. In most markets that is a differentiator we have to "
    "explain. In the UK it is the baseline the client already expects, which removes most of the "
    "friction from an offshore appointment: the deliverable structure, the status codes and the "
    "CDE workflow are the same vocabulary on both sides."),
   ("RIBA stages make scope arguments avoidable",
    "A UK appointment usually names the stage, and the stage carries an understood level of "
    "information need. That is a considerably better starting point than a blanket LOD number, and "
    "it is why UK scoping conversations are shorter. We still agree level of information need "
    "element by element, because a stage is a useful shorthand rather than a specification."),
 ],
 "standards": [
   ("CIBSE", "Guides A, B and the design guidance basis for building services design in the UK."),
   ("Building Regulations", "Approved Documents including Part L, Part F and Part B as the "
    "compliance basis, with the devolved equivalents in Scotland and Northern Ireland where they "
    "apply."),
   ("BS and BS EN standards", "Including BS 9999 and BS EN 12845 for fire, BS 7671 for electrical "
    "installations, and BS EN 806 and BS EN 12056 for water and drainage."),
   ("ISO 19650", "Information management across the delivery phase — naming, status codes, the "
    "CDE workflow and level of information need. We align to it as standard practice and are not "
    "certified to it."),
   ("BSRIA and NBS", "BG 6 design framework vocabulary and NBS specification interfaces where a "
    "project uses them."),
 ],
 "overlap": "India is UTC+5:30, which gives roughly four to five hours of genuine overlap with a UK "
            "working day — your morning is our afternoon. In practice that is enough for same-day "
            "resolution of most queries and for a live coordination call without either side "
            "working unsociable hours, which is why UK appointments run more smoothly than any "
            "other market we work in.",
 "model": [
   ("Package delivery", "Defined stage deliverables with a fixed list and programme, priced "
    "against the deliverable rather than against hours."),
   ("Team extension", "Capacity inside your environment, your templates and your BEP, working to "
    "your CDE and status codes."),
   ("Coordination appointment", "Federation, clash and clearance resolution across contributing "
    "disciplines, with the issue history as a deliverable."),
   ("Automation engagement", "A QA rule set or documentation pipeline built for your standards and "
    "handed over documented."),
 ],
 "honest": [
   "BIMRACE has no office, no registered entity and no employees in the United Kingdom.",
   "No BIMRACE engineer holds UK chartered status (CEng, or CIBSE or IMechE membership at that "
   "grade). We do not act as the responsible designer for Building Regulations compliance.",
   "We are not certified to ISO 19650. We structure delivery to align with its principles, which "
   "is a statement of working method and not third-party certification.",
   "We do not undertake duties under CDM 2015. Designer duties sit with your appointed designer.",
 ],
 "typical": [
   ("Stage 3 and 4 MEP production", "Modelling, coordination and documentation to the stage's "
    "level of information need, inside your BEP."),
   ("Coordination and clash resolution", "Federated coordination with the issue history and the "
    "re-test evidence as deliverables."),
   ("ISO 19650 delivery support", "Naming, status, federation and information container discipline "
    "for practices setting up or tightening their information management."),
   ("Automation for UK practices", "Automated QA against your project rule set, quantity routines "
    "and documentation pipelines."),
 ],
 "sectors": ["healthcare", "education", "residential", "commercial"],
 "services": ["mep-engineering-services", "bim-coordination-clash-detection",
              "bim-modelling-documentation", "bim-automation-services"],
 "faqs": [
   ("Are you certified to ISO 19650?",
    "No. We structure delivery to align with ISO 19650 principles on every appointment, which is a "
    "working method rather than a certification. If a project requires a certified provider, we are "
    "not one and will say so at enquiry stage."),
   ("Can a BIMRACE engineer act as the responsible designer?",
    "No. No BIMRACE engineer holds UK chartered status and we do not take designer duties under "
    "CDM 2015. We deliver engineering design and BIM output under your appointed designer."),
   ("How much working overlap is there with a UK day?",
    "Roughly four to five hours — your morning is our afternoon. It is enough for same-day query "
    "resolution and live coordination calls without either side working unsociable hours."),
   ("Can you work inside our CDE and to our status codes?",
    "Yes, and it is the normal case. Working to your information container naming and status codes "
    "is what makes the deliverables usable on receipt rather than requiring a translation step."),
   ("Do you work to CIBSE or ASHRAE basis?",
    "Whichever the project names. UK appointments normally run on CIBSE and Building Regulations "
    "basis, and we author in metric to UK conventions."),
 ],
},

{
 "slug": "uae",
 "nav": "United Arab Emirates",
 "cc": "AE",
 "h1": "MEP engineering and BIM services for projects in the UAE",
 "title": "MEP &amp; BIM Services for the UAE | BIMRACE",
 "desc": "MEP engineering and BIM for UAE projects on ASHRAE and NFPA basis, delivered remotely "
         "behind your licensed local consultant of record.",
 "eyebrow": "United Arab Emirates",
 "lede": "Near-complete working-hour overlap, a shared ASHRAE and NFPA design basis, and an "
         "authority submission process that a remote team supports but never fronts.",
 "meta": [("Model", "Remote delivery from India"), ("Overlap", "Near-complete"),
          ("Basis", "ASHRAE · NFPA · local authority"),
          ("Submissions", "Your licensed local consultant")],
 "intro": [
   ("Authority requirements, not the design basis, are what differ",
    "The engineering basis on most UAE projects is familiar — ASHRAE for mechanical, NFPA for fire, "
    "IEC-derived practice for electrical. What differs, and what an offshore team has to respect, "
    "is that approval runs through specific authorities with their own submission formats, review "
    "cycles and licensed-consultant requirements. A remote team can produce every drawing and "
    "model in that process. It cannot be the submitting party, and a provider that implies "
    "otherwise is describing something that does not exist."),
   ("Cooling load is the whole engineering argument",
    "Design conditions in the Gulf make cooling the dominant load by a wide margin, and they make "
    "plant size, riser allocation and the depth of the mechanical zone the decisions the rest of "
    "the building is arranged around. Getting the load basis and the plant selection right is worth "
    "more than every downstream efficiency, and it is where the engineering attention on a UAE "
    "project belongs."),
 ],
 "standards": [
   ("ASHRAE", "Load calculation, ventilation and energy basis, applied against Gulf design "
    "conditions."),
   ("NFPA", "Fire protection design basis, alongside the local civil defence requirements that "
    "govern approval."),
   ("Local authority requirements", "Dubai Municipality, DEWA and Dubai Civil Defence in Dubai; "
    "Abu Dhabi's municipal and distribution authority requirements in Abu Dhabi; free-zone "
    "authorities where applicable. Which applies is a project fact we ask for rather than assume."),
   ("Green building regulation", "Al Sa'fat in Dubai and Estidama Pearl in Abu Dhabi where a "
    "project is subject to them."),
   ("ISO 19650", "Information management structure, increasingly specified on larger UAE "
    "appointments and applied by us as standard practice regardless."),
 ],
 "overlap": "India is UTC+5:30 and the UAE is UTC+4 — a difference of ninety minutes. In practice "
            "the working day is shared almost completely. Live coordination, same-day turnaround "
            "and joining a client's internal meetings are all straightforward, which makes the UAE "
            "the market where remote delivery feels least remote.",
 "model": [
   ("Production support to a licensed local consultant", "We produce engineering and BIM "
    "deliverables; the licensed consultant of record reviews and submits. This is the standard "
    "arrangement and the only one we offer."),
   ("Contractor BIM delivery", "Coordination, shop drawings and builders work for the installing "
    "contractor, which is a large share of UAE BIM scope."),
   ("Team extension", "Capacity inside your environment and standards for a defined period."),
   ("Automation engagement", "QA rule sets, quantity routines and documentation pipelines built "
    "for your standards."),
 ],
 "honest": [
   "BIMRACE has no office, no trade licence and no registered entity in the United Arab Emirates.",
   "We are not a licensed engineering consultancy in any UAE emirate and cannot be the consultant "
   "of record.",
   "We do not make submissions to Dubai Municipality, DEWA, Dubai Civil Defence, Abu Dhabi "
   "authorities or any free-zone authority. Submissions are made by your licensed local consultant.",
   "We hold no UAE accreditations, approvals or authority registrations, and claim none.",
 ],
 "typical": [
   ("Contractor coordination and shop drawings", "Federated coordination, clash and clearance "
    "resolution, and fabrication-level output for the installing contractor."),
   ("Consultant production support", "Modelling, documentation and coordination behind a licensed "
    "local consultant's appointment."),
   ("BIM delivery for large mixed-use", "High-volume documentation and coordination across "
    "residential, retail and hospitality components."),
   ("Automation for UAE delivery teams", "Rule-based QA and documentation routines for teams "
    "running high-volume production."),
 ],
 "sectors": ["hospitality", "commercial", "residential", "retail"],
 "services": ["mep-engineering-services", "hvac-bim-services",
              "construction-support-bim", "bim-coordination-clash-detection"],
 "faqs": [
   ("Can BIMRACE submit drawings to Dubai Municipality or Civil Defence?",
    "No. Submissions are made by a licensed local consultant. BIMRACE has no UAE trade licence and "
    "is not a licensed engineering consultancy in any emirate. We produce the engineering and BIM "
    "deliverables that go into that submission."),
   ("Do you have a Dubai office?",
    "No. BIMRACE is an India-based practice delivering remotely. We do not list a UAE address or "
    "phone number because we do not have one."),
   ("How well does the time difference work?",
    "It barely registers — ninety minutes. Live coordination calls, same-day turnaround and joining "
    "your internal meetings are all normal, which is not true of every market we work in."),
   ("Do you work for contractors as well as consultants?",
    "Yes, and in the UAE contractor-side BIM is a large share of the market. Coordination, shop "
    "drawings and builders work for the installing contractor is a common appointment."),
   ("Which authority requirements do you work to?",
    "Whichever applies to the project, which we ask for at enquiry stage rather than assume — "
    "requirements differ between emirates and between free zones, and designing to the wrong set is "
    "a real failure mode."),
 ],
},

{
 "slug": "saudi-arabia",
 "nav": "Saudi Arabia",
 "cc": "SA",
 "h1": "MEP engineering and BIM services for projects in Saudi Arabia",
 "title": "MEP &amp; BIM Services for Saudi Arabia | BIMRACE",
 "desc": "MEP engineering and BIM for Saudi projects on Saudi Building Code basis, delivered "
         "remotely behind your registered local engineering office.",
 "eyebrow": "Saudi Arabia",
 "lede": "A market defined by programme volume, where the constraint on an offshore team is rarely "
         "capability and almost always whether production throughput and information discipline "
         "can hold at scale.",
 "meta": [("Model", "Remote delivery from India"), ("Overlap", "Substantial"),
          ("Basis", "Saudi Building Code"), ("Submissions", "Your registered local office")],
 "intro": [
   ("Volume is the engineering condition",
    "The scale and pace of current Saudi delivery means the recurring failure on large appointments "
    "is not a design error but an information one: models issued at inconsistent status, "
    "typologies that drifted between packages, quantities that cannot be reconciled, and a "
    "coordination process that stopped scaling around the third package. Those are exactly the "
    "failures that rule-based checking and model-derived documentation are for, and the argument "
    "for them is stronger here than in any market with normal programme pressure."),
   ("Saudi Building Code is its own basis, not a rebadged international one",
    "The SBC draws on international model codes but is a distinct set of requirements with its own "
    "structure and its own amendments. Treating it as ASHRAE or IBC with a different cover is a "
    "way of being wrong in specific and expensive places. We work to the SBC parts the project "
    "names and ask which edition and amendment applies rather than assuming."),
 ],
 "standards": [
   ("Saudi Building Code (SBC)", "Including the mechanical, plumbing, electrical, fire and energy "
    "conservation parts as adopted for the project. Edition and amendment are a project fact we "
    "ask for."),
   ("Saudi Civil Defence requirements", "Fire protection approval basis alongside the code."),
   ("ASHRAE and NFPA", "Where referenced by the SBC or specified by the project as the underlying "
    "design basis."),
   ("SASO", "Product and equipment conformity requirements where they bear on specification and "
    "scheduling."),
   ("ISO 19650", "Information management structure, increasingly specified on giga-project "
    "programmes and applied by us as standard practice regardless."),
 ],
 "overlap": "India is UTC+5:30 and Saudi Arabia is UTC+3 — a difference of two and a half hours, "
            "so most of the working day is shared. Note that the Saudi working week runs Sunday to "
            "Thursday against our Monday to Friday; we cover the Sunday and adjust the Friday by "
            "arrangement rather than pretending the calendars align.",
 "model": [
   ("Production support to a registered local office", "We produce engineering and BIM "
    "deliverables; the locally registered engineering office of record reviews and submits."),
   ("Programme-scale package delivery", "High-volume modelling, coordination and documentation "
    "across multiple packages with consistent standards enforced by rule set rather than by "
    "supervision."),
   ("Contractor BIM delivery", "Coordination, shop drawings and builders work for the installing "
    "contractor."),
   ("Automation engagement", "The strongest case in any of our markets — rule-based QA and "
    "documentation pipelines are what make consistency survive programme scale."),
 ],
 "honest": [
   "BIMRACE has no office, no commercial registration and no employees in Saudi Arabia.",
   "BIMRACE is not registered with the Saudi Council of Engineers and is not a licensed local "
   "engineering office. We cannot be the engineering office of record.",
   "We do not make submissions to Saudi Civil Defence, municipal authorities or any project "
   "authority. Submissions are made by your registered local office.",
   "We hold no Saudi accreditations, prequalifications or authority registrations, and claim none. "
   "We have no giga-project appointments to point to, and this page does not imply any.",
 ],
 "typical": [
   ("Multi-package production support", "Consistent modelling and documentation across packages, "
    "with conformance enforced by rule set."),
   ("Coordination at programme scale", "Federated coordination where the number of contributing "
    "models is the difficulty rather than their individual complexity."),
   ("Contractor shop drawing production", "Fabrication-level output derived from the coordinated "
    "model."),
   ("Standards and automation setup", "Templates, parameter schemas and checking routines for "
    "delivery teams whose process has stopped scaling."),
 ],
 "sectors": ["hospitality", "commercial", "residential", "industrial"],
 "services": ["mep-engineering-services", "bim-automation-services",
              "bim-coordination-clash-detection", "bim-modelling-documentation"],
 "faqs": [
   ("Can BIMRACE be the engineering office of record in Saudi Arabia?",
    "No. BIMRACE is not registered with the Saudi Council of Engineers and holds no commercial "
    "registration in the Kingdom. We deliver production and coordination support behind a locally "
    "registered engineering office that reviews and submits."),
   ("Do you have giga-project experience?",
    "This page makes no such claim. This site publishes no project history until a client releases "
    "it, and we would rather lose an enquiry than imply appointments we do not hold. What we can "
    "demonstrate at enquiry stage is the rule sets and the live QA output that address the "
    "failure modes programme-scale delivery actually has."),
   ("How do you handle the Sunday to Thursday working week?",
    "We cover Sunday as a working day and adjust Friday by arrangement. Saying the calendars align "
    "when they do not is how an offshore appointment loses two days a week that nobody budgeted "
    "for."),
   ("Do you work to Saudi Building Code?",
    "Yes, to the parts and the edition the project names — which we ask for rather than assume. The "
    "SBC draws on international model codes but is a distinct set of requirements, and treating it "
    "as a rebadged international code is a way of being wrong in specific places."),
 ],
},

{
 "slug": "australia",
 "nav": "Australia",
 "cc": "AU",
 "h1": "MEP engineering and BIM services for projects in Australia",
 "title": "MEP &amp; BIM Services for Australia | BIMRACE",
 "desc": "MEP engineering and BIM for Australian projects on NCC and AS/NZS basis, delivered "
         "remotely under your registered practitioner.",
 "eyebrow": "Australia",
 "lede": "A standards environment that is genuinely its own — AS/NZS rather than a variant of "
         "anyone else's — and a time difference that happens to give a real shared working "
         "afternoon.",
 "meta": [("Model", "Remote delivery from India"), ("Overlap", "Your afternoon"),
          ("Basis", "NCC · AS/NZS"), ("Certification", "Your registered practitioner")],
 "intro": [
   ("AS/NZS standards are not close enough to guess at",
    "AS/NZS 3000 is not BS 7671 and it is not the NEC. AS 3500 is not BS EN 12056. AS 2118 is not "
    "NFPA 13. An offshore team that treats Australian standards as a regional dialect of something "
    "it already knows will produce work that looks right and is wrong in the details that "
    "certification actually examines. We work to the AS/NZS standards the project names, and where "
    "we are not confident in a specific requirement we ask rather than interpolate."),
   ("NCC performance solutions change what the model has to evidence",
    "Where a project uses a performance solution rather than a deemed-to-satisfy pathway, the "
    "evidence requirement changes — what has to be demonstrated, and in what form. That affects "
    "what the model has to be able to answer, which is a level-of-information-need conversation "
    "that should happen at the start rather than at certification."),
 ],
 "standards": [
   ("National Construction Code (NCC)", "The compliance basis, including the deemed-to-satisfy and "
    "performance solution pathways and the state variations that apply."),
   ("AS/NZS 3000", "Wiring rules, as the electrical installation basis."),
   ("AS 3500", "Plumbing and drainage standards for water, sanitary and stormwater."),
   ("AS 1668 and AS 2118", "Mechanical ventilation and fire control, and automatic fire sprinkler "
    "systems respectively."),
   ("NATSPEC National BIM Guide", "Where a project specifies it as the BIM delivery framework, "
    "alongside ISO 19650 which we apply as standard practice."),
   ("NABERS and Green Star", "Where a project is subject to a rating requirement that bears on "
    "the services design and the data the model has to carry."),
 ],
 "overlap": "India is UTC+5:30; eastern Australia is UTC+10 or UTC+11 depending on daylight saving. "
            "That puts our morning against your afternoon — roughly four hours of genuine overlap "
            "with Sydney, Melbourne and Brisbane, and more with Perth. Unusually for a remote "
            "arrangement, the overlap falls in the part of your day when decisions actually get "
            "made rather than at the edges of it.",
 "model": [
   ("Design support under your certifier or registered practitioner", "We produce engineering and "
    "BIM deliverables; your registered practitioner certifies. Registration requirements vary by "
    "state and we work behind yours."),
   ("Team extension", "Capacity inside your environment, templates and BEP for a defined period."),
   ("Package delivery", "Defined scope with a fixed deliverable list and programme."),
   ("Automation engagement", "QA rule sets and documentation pipelines built for your standards "
    "and handed over documented."),
 ],
 "honest": [
   "BIMRACE has no office, no registered entity and no employees in Australia.",
   "No BIMRACE engineer holds Australian professional registration — not RPEQ in Queensland, nor "
   "registration under any other state or territory scheme. We do not certify and we do not act as "
   "the registered practitioner.",
   "We do not make submissions to any Australian certifier or authority.",
   "We hold no Australian accreditations or partnerships, and claim none.",
 ],
 "typical": [
   ("MEP production support for consultancies", "Modelling, coordination and documentation to your "
    "design, at the level of information need your stage requires."),
   ("Contractor coordination support", "Federated coordination and builders work extraction for "
    "the installing party."),
   ("NATSPEC-aligned BIM delivery", "Where a project specifies the National BIM Guide as its "
    "framework."),
   ("Automation for Australian practices", "Rule-based QA against your project standards, quantity "
    "routines and documentation pipelines."),
 ],
 "sectors": ["commercial", "education", "healthcare", "residential"],
 "services": ["mep-engineering-services", "bim-modelling-documentation",
              "bim-coordination-clash-detection", "bim-automation-services"],
 "faqs": [
   ("Can BIMRACE certify work for an Australian project?",
    "No. No BIMRACE engineer holds Australian professional registration under any state or "
    "territory scheme. We deliver engineering design and BIM output as support, and your registered "
    "practitioner certifies."),
   ("Do you know AS/NZS standards, or do you work to international ones?",
    "We work to the AS/NZS standards the project names. They are genuinely distinct from the UK "
    "and US equivalents, and treating them as a regional variant is the characteristic failure of "
    "offshore work on Australian projects. Where we are not confident on a specific requirement we "
    "ask rather than interpolate."),
   ("How much overlap is there with an Australian working day?",
    "Around four hours with the east coast and more with Perth, falling in your afternoon. It "
    "coincides with the part of the day when decisions get made, which is more useful than a "
    "longer overlap at the edges."),
   ("Can you work to the NATSPEC National BIM Guide?",
    "Yes, where a project specifies it. We apply ISO 19650 information management as standard "
    "practice in any case, and the two are compatible."),
 ],
},

{
 "slug": "canada",
 "nav": "Canada",
 "cc": "CA",
 "h1": "MEP engineering and BIM services for projects in Canada",
 "title": "MEP &amp; BIM Services for Canada | BIMRACE",
 "desc": "MEP engineering and BIM for Canadian projects on provincial code and CSA basis, "
         "delivered remotely under your P.Eng of record.",
 "eyebrow": "Canada",
 "lede": "A market where the code that applies is provincial rather than national, and where "
         "assuming otherwise is the fastest way for an offshore team to produce confidently wrong "
         "work.",
 "meta": [("Model", "Remote delivery from India"), ("Units", "Metric, with imperial practice"),
          ("Basis", "NBC · provincial codes · CSA"), ("Licensure", "Your P.Eng of record")],
 "intro": [
   ("The code is provincial, and the differences are real",
    "The National Building Code is a model code. What governs is the provincial adoption — the "
    "Ontario Building Code, the BC Building Code, the Code de construction du Québec and their "
    "counterparts — each with its own amendments and its own timing. A design produced to the "
    "national model code and assumed to satisfy a province is a design that will be corrected at "
    "review. We ask which provincial code and which edition applies at enquiry stage, and we ask "
    "it first."),
   ("Climate makes the mechanical basis unlike the rest of our markets",
    "Heating-dominated design, freeze protection, ventilation heat recovery as a practical "
    "necessity rather than an efficiency option, and building envelope interaction that matters "
    "more than it does in the Gulf or the southern US. These are not exotic requirements, but they "
    "are the opposite of the default assumptions an offshore team builds up working on "
    "cooling-dominated projects — which is precisely why they need stating."),
 ],
 "standards": [
   ("National Building Code of Canada", "The model code, as adopted and amended provincially. "
    "Which provincial code and edition applies is a project fact we ask for."),
   ("Provincial codes", "Ontario Building Code, BC Building Code, the Québec construction code and "
    "the other provincial adoptions, with their amendments."),
   ("CSA C22.1", "The Canadian Electrical Code as the electrical installation basis."),
   ("ASHRAE and NECB", "Energy and ventilation basis, including the National Energy Code for "
    "Buildings where adopted."),
   ("NFPA", "Fire protection design basis as referenced by the applicable code."),
 ],
 "overlap": "India is UTC+5:30. Against Eastern Time that is a short overlap at the start of your "
            "day and effectively none against Pacific Time. As in the US, the working arrangement "
            "is a fixed daily handover rather than an expectation of live availability: work issued "
            "at your close of business is progressed overnight with a written note of progress, "
            "blockers and decisions needed waiting when you open.",
 "model": [
   ("Design support under your P.Eng of record", "We produce engineering and BIM deliverables; "
    "your licensed professional engineer reviews, seals and submits. This is the only arrangement "
    "we offer in Canada."),
   ("Team extension", "Capacity inside your environment, templates and standards for a defined "
    "period."),
   ("Contractor coordination support", "Federated coordination, clash and clearance rule sets and "
    "builders work extraction."),
   ("Overnight production cycle", "Fixed daily handover with a written progress and blocker note."),
 ],
 "honest": [
   "BIMRACE has no office, no registered entity and no employees in Canada.",
   "No BIMRACE engineer is licensed as a Professional Engineer by any provincial or territorial "
   "association. We do not seal drawings and we do not make authority submissions.",
   "All engineering we produce for Canadian projects is design support delivered under a licensed "
   "P.Eng of record who reviews it and takes professional responsibility for it.",
   "We hold no Canadian accreditations or partnerships, and claim none.",
 ],
 "typical": [
   ("MEP production support for consulting engineers", "Modelling, coordination and documentation "
    "to your design, under your seal."),
   ("Contractor coordination and shop drawings", "Federated coordination and fabrication-level "
    "output for the installing party."),
   ("Automation for Canadian practices", "QA rule sets, quantity routines and documentation "
    "pipelines built for your standards."),
   ("Model remediation and standards setup", "Templates, parameter schemas and checking routines "
    "for practices moving to information-first delivery."),
 ],
 "sectors": ["healthcare", "education", "commercial", "residential"],
 "services": ["mep-engineering-services", "bim-coordination-clash-detection",
              "bim-modelling-documentation", "bim-automation-services"],
 "faqs": [
   ("Can BIMRACE seal drawings for a Canadian project?",
    "No. No BIMRACE engineer holds P.Eng licensure with any provincial or territorial association. "
    "We produce engineering design and BIM deliverables as support, and your licensed professional "
    "engineer reviews, seals and takes responsibility."),
   ("Which code do you design to?",
    "The provincial code the project is subject to, and its edition — which we ask for at enquiry "
    "stage. Designing to the national model code and assuming provincial acceptance is a real "
    "failure mode, not a theoretical one."),
   ("How do you handle the time difference?",
    "With a fixed daily handover rather than an expectation of overlap, particularly for Pacific "
    "Time. Work issued at your close of business is progressed overnight with a written note of "
    "what moved, what is blocked and what needs a decision."),
   ("Do you have experience with heating-dominated design?",
    "It is the opposite of the default assumption an offshore team accumulates on cooling-dominated "
    "work, which is why we state the design conditions and the basis explicitly on Canadian "
    "appointments rather than carrying habits across."),
 ],
},

{
 "slug": "europe",
 "nav": "Europe",
 "cc": "EU",
 "h1": "MEP engineering and BIM services for projects in Europe",
 "title": "MEP &amp; BIM Services for Europe | BIMRACE",
 "desc": "MEP engineering and BIM for European projects on EN standards and national annexes, "
         "with openBIM and IFC exchange configured from the start.",
 "eyebrow": "Europe",
 "lede": "A shared standards framework with national annexes that are not interchangeable, and the "
         "market where openBIM and IFC exchange discipline matters most in practice rather than in "
         "principle.",
 "meta": [("Model", "Remote delivery from India"), ("Overlap", "Your morning"),
          ("Basis", "EN standards · national annexes"), ("Exchange", "IFC · openBIM")],
 "intro": [
   ("The national annex is where the engineering actually lives",
    "EN standards give a common framework and the national annex gives the numbers. Two projects "
    "in two member states can cite the same standard and require materially different design "
    "values. An offshore team that works to the EN and ignores the annex will produce something "
    "defensible in a seminar and wrong on the project. We ask which national annex applies before "
    "anything is designed, and we treat the answer as a design input rather than a formality."),
   ("openBIM is a practical requirement here, not a philosophy",
    "European public procurement and a substantial part of the private market run on IFC exchange "
    "rather than on native-file handover, and the difference between an IFC that validates and an "
    "IFC that is technically valid but carries none of the required data is enormous. Export "
    "configuration, classification mapping and property set discipline are authoring decisions "
    "made at the start, not an export setting chosen at the end."),
 ],
 "standards": [
   ("EN standards and national annexes", "The common framework with the country-specific values "
    "that actually govern. Which annex applies is a project fact we ask for."),
   ("National standards", "DIN and VDI in Germany, NEN in the Netherlands, NF in France and their "
    "counterparts, where a project works to them alongside or instead of the EN."),
   ("EPBD-derived national energy requirements", "As transposed into national regulation, which "
    "varies considerably between member states."),
   ("ISO 19650", "Information management, widely specified across European public and private "
    "procurement. We apply it as standard practice and are not certified to it."),
   ("IFC and buildingSMART", "openBIM exchange with property sets and classification mapping "
    "configured during authoring rather than at export."),
 ],
 "overlap": "India is UTC+5:30 and continental Europe is UTC+1 or UTC+2 — a difference of three and "
            "a half to four and a half hours. Your morning is our afternoon, giving roughly four "
            "hours of genuine overlap, which is enough for same-day query resolution and live "
            "coordination without unsociable hours on either side.",
 "model": [
   ("Production support under your local engineer of record", "We produce engineering and BIM "
    "deliverables; your locally qualified engineer reviews and takes responsibility. Qualification "
    "and liability requirements vary by member state and we work behind yours."),
   ("openBIM delivery", "IFC-based exchange with property sets, classification and export "
    "configuration agreed at the start."),
   ("Team extension", "Capacity inside your environment, templates and standards."),
   ("Automation engagement", "QA rule sets, IFC validation routines and documentation pipelines."),
 ],
 "honest": [
   "BIMRACE has no office, no registered entity and no employees in any European country.",
   "No BIMRACE engineer holds professional qualification or registration in any EU or EEA member "
   "state. We do not act as the responsible engineer and we do not make authority submissions.",
   "We are not certified to ISO 19650. We align to its principles as a working method.",
   "We hold no European accreditations or partnerships, and claim none.",
   "This page covers Europe as a delivery region. It does not imply capability in every national "
   "regulatory system — we work to the national annex and the national standards the project "
   "names, and will decline where we are not confident of the basis.",
 ],
 "typical": [
   ("openBIM production and IFC delivery", "Authoring configured for IFC exchange with the "
    "property sets and classification the project requires."),
   ("MEP production support", "Modelling, coordination and documentation behind a locally "
    "qualified engineer."),
   ("Coordination appointments", "Federated coordination with the issue history and re-test "
    "evidence as deliverables."),
   ("IFC validation and data automation", "Routines that test an IFC for the data it is supposed "
    "to carry, not just for whether it opens."),
 ],
 "sectors": ["commercial", "healthcare", "residential", "industrial"],
 "services": ["mep-engineering-services", "bim-modelling-documentation",
              "bim-coordination-clash-detection", "bim-automation-services"],
 "faqs": [
   ("Do you work to EN standards or to national standards?",
    "To the national annex and the national standards the project names. An EN cited without its "
    "national annex does not determine the design values, and working to the framework while "
    "ignoring the annex is the characteristic way offshore work goes wrong on European projects."),
   ("Can you deliver in IFC rather than native files?",
    "Yes, and configured properly — property sets, classification mapping and export settings "
    "agreed during setup rather than chosen at export. An IFC that opens but carries none of the "
    "required data passes a file check and fails the actual requirement."),
   ("Which countries do you cover?",
    "We work with European project teams remotely and to the standards basis the project names. We "
    "do not claim capability in every national regulatory system, and where we are not confident "
    "of the basis we will decline rather than interpolate."),
   ("Are you registered or qualified in any EU member state?",
    "No. No BIMRACE engineer holds professional qualification or registration in any EU or EEA "
    "member state. We deliver under your locally qualified engineer, who takes responsibility."),
 ],
},
]

LOCATION_BY_SLUG = {l["slug"]: l for l in LOCATIONS}
