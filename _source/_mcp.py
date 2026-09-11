"""
BIMRACE — MCP for Revit.

    THE RULE THAT GOVERNS THIS FILE
    ------------------------------------------------------------------
    BIMRACE has not built and does not operate a Model Context Protocol
    server for Revit. This page says that in the first section, in the
    hero metadata, and again in the FAQ. Every capability statement on it
    carries a badge, and the MCP layer itself carries `road`.

    The page exists because the question "what would it actually take to
    connect an AI assistant to a Revit model, and what should it never be
    allowed to do" is a real engineering question that this sector is
    currently answering badly and loudly. Answering it properly is worth
    more than claiming an integration we do not have.

    Anything in this file that describes BIMRACE capability must be
    traceable to a badge that already exists elsewhere on the site:
      - model data extraction and reasoning ....... dev
      - automation and checking routines ......... live
      - MCP server for Revit ..................... road
"""

FAQS = [
 ("Does BIMRACE have a working MCP server for Revit?",
  "No. This is marked roadmap on this page and in the platform navigation, and nothing on this "
  "page should be read as a released integration. What exists today is model data extraction and "
  "reasoning, which is in development and used on our own delivery, and the automation and "
  "checking routines that have been live on client appointments for years. The protocol layer "
  "between them and an AI assistant is not built."),
 ("What is the Model Context Protocol?",
  "An open protocol for connecting AI assistants to external tools and data. A server exposes a "
  "set of typed tools and resources; a client — an AI assistant — discovers them and calls them. "
  "The value is that the interface is declared and enumerable rather than improvised, which means "
  "the set of things an assistant is able to do against a system is a finite list somebody wrote "
  "down and can review."),
 ("Why is Revit a difficult target for this?",
  "Because the Revit API is not a service. Calls have to run on Revit's main thread inside a valid "
  "API context, model changes require transactions, and Revit is not designed to run headless for "
  "interactive documents. An MCP server cannot simply call the API from a request handler — it has "
  "to marshal every call into Revit's execution context and hand the result back. That is an "
  "engineering problem with known solutions, but it is the reason a Revit MCP integration is more "
  "than a wrapper."),
 ("Would it be able to change our models?",
  "Not in anything we would build. The read boundary is the design: query, extract, report and "
  "draft. Write operations against a live model would remain behind the same constraint as every "
  "other automation on this site — a named engineer accepts, amends or rejects, and nothing "
  "commits without that. This is not a technical limitation we expect to remove later. It is the "
  "thing that makes an engineering deliverable worth anything."),
 ("Does model data leave our environment?",
  "That is the question to ask any vendor proposing this, and the answer determines whether it is "
  "adoptable at all. A model contains commercially sensitive design information and frequently sits "
  "under an NDA that predates anyone's AI strategy. Any architecture we would propose has to be "
  "explicit about what leaves the machine, what is retained, and by whom — before it is "
  "interesting rather than after."),
 ("Can we talk to you about this anyway?",
  "Yes, and it is a more useful conversation than a demonstration would be. We can show the "
  "extraction and checking work that is real today, describe honestly where the protocol layer "
  "would sit, and tell you which parts of what you have read elsewhere are further away than they "
  "are being presented as."),
]


def body(B, phero, faq_block, related_block, faq_ld):
    return f"""
{phero([("Home", "index.html"), ("Platform", "platform.html"), ("MCP for Revit", None)],
       "MCP for Revit: connecting AI assistants to model data",
       "What the Model Context Protocol is, what a Revit MCP server would actually have to do, "
       "which workflows it would be useful for, and what it must never be allowed to do. BIMRACE "
       "has not built one — this page explains the architecture rather than selling it.",
       [("BIMRACE status", "Roadmap — not built"), ("What is live", "Automation routines"),
        ("What is in development", "Model data extraction"),
        ("Write access", "Not proposed")])}

<section class="section section--flush">
  <div class="shell">
    <div class="note note--sig" style="max-width:none">
      <p><strong>Read this first.</strong> BIMRACE does not have a working Model Context Protocol
      server for Revit. We have not shipped one, we do not operate one, and nothing on this page is
      a product you can buy or licence. {B('road')} is the honest badge for the protocol layer and
      it is the badge it carries in our navigation.</p>
      <p>What is real today is underneath it: automation and checking routines that have been
      {B('live')} on client appointments for years, and model data extraction and reasoning that is
      {B('dev')} and used on our own delivery. This page describes how those would connect to an AI
      assistant through MCP, because it is a question worth answering properly in a market that is
      currently answering it loudly and badly.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell split split--mid">
    <div>
      <p class="eyebrow">What it is</p>
      <h2 class="sec-title">A declared interface, not a smarter chatbot</h2>
      <p class="sec-lede">The Model Context Protocol is an open standard for connecting AI
      assistants to external tools and data. A server exposes a set of typed tools and resources; a
      client discovers what is available and calls it. The protocol itself is unremarkable — which
      is the point.</p>
      <p class="lede" style="margin-top:22px">What matters for engineering is the consequence of
      that structure: the complete set of things an assistant can do against your model is a finite,
      enumerable list that somebody wrote and somebody else can review. Compare that with the
      alternative currently being sold, which is an assistant with unspecified access and a
      reassuring paragraph about safety.</p>
      <p class="lede" style="margin-top:16px">An engineering practice should be able to read the
      tool list, disagree with an entry, and have it removed. That is a governable interface. An
      integration you cannot enumerate is not.</p>
    </div>
    <div>
      <div class="panel">
        <div class="panel__bar">
          <span><b>ARCHITECTURE</b> / WHERE MCP WOULD SIT</span>
          <span>{B('road')}</span>
        </div>
        <div class="panel__body">
          <ol class="steps">
            <li class="is-human"><span class="steps__k">Engineer</span><h3>Asks a question</h3>
              <p>In their own words, about a model they are accountable for.</p></li>
            <li class="is-ai"><span class="steps__k">Assistant</span><h3>Selects a declared tool</h3>
              <p>From an enumerable list, not from unspecified access.</p></li>
            <li class="is-ai"><span class="steps__k">MCP layer</span><h3>Marshals the call</h3>
              <p>Into Revit's API context, inside a read-only boundary.</p></li>
            <li class="is-ai"><span class="steps__k">Model</span><h3>Returns structured data</h3>
              <p>Elements, parameters, systems, relationships — with element IDs.</p></li>
            <li class="is-human"><span class="steps__k">Engineer</span><h3>Reviews and decides</h3>
              <p>Nothing is committed to the model by anything above this line.</p></li>
          </ol>
        </div>
        <div class="panel__foot">
          <span>READ BOUNDARY — NO WRITE PATH PROPOSED</span>
          <span>ARCHITECTURE DESCRIPTION, NOT A RELEASED PRODUCT</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">The hard part</p>
      <h2 class="sec-title">Why a Revit MCP server is not a wrapper around the API</h2>
      <p class="sec-lede">Most published enthusiasm about AI and Revit skips this section. It is
      the section that determines whether any of it works on a real project.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Constraint 01<b>The API is not a service</b></div>
        <div class="spec__v">Revit API calls must execute on Revit's main thread inside a valid API
        context. A server receiving a request cannot simply call the API from its request handler;
        every call has to be marshalled into Revit's execution context and the result handed back.
        This is solvable with external events and an idling handler, and it is why a Revit MCP
        server is an application hosted inside Revit rather than a process beside it.</div></div>
      <div class="spec__row"><div class="spec__k">Constraint 02<b>Transactions and document state</b></div>
        <div class="spec__v">Any model modification requires a transaction, and a transaction opened
        by a background process against a document a person is actively editing is a way to lose
        someone's afternoon. Read operations have their own version of this problem: a query
        answered against a document mid-edit may not describe anything that will exist a minute
        later.</div></div>
      <div class="spec__row"><div class="spec__k">Constraint 03<b>No headless interactive mode</b></div>
        <div class="spec__v">Revit is not designed to run headless against interactive documents.
        That constrains the deployment shape considerably: the server lives where Revit lives, on a
        workstation or a controlled session, not as a scalable cloud service answering questions
        about a model that is not open.</div></div>
      <div class="spec__row"><div class="spec__k">Constraint 04<b>Model size versus context</b></div>
        <div class="spec__v">A federated MEP model contains far more data than can be handed to a
        language model. Any useful implementation is therefore mostly a query and summarisation
        problem — resolving a question to a narrow, structured extract — and only incidentally an AI
        problem. Tools that return whole model dumps are demonstrations, not workflows.</div></div>
      <div class="spec__row"><div class="spec__k">Constraint 05<b>Non-determinism against engineering</b></div>
        <div class="spec__v">A language model will occasionally return a confident answer that is
        wrong. In a conversational product that is an annoyance. Against a model that a duct size
        will be taken from, it is a defect with a professional liability attached, and it is the
        reason the read boundary and the engineer review step are architectural rather than
        optional.</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Use cases</p>
      <h2 class="sec-title">What it would genuinely be useful for</h2>
      <p class="sec-lede">Ordered by how close each one is to being real. The badge on each is the
      status of the underlying capability at BIMRACE, not of the MCP layer — that remains
      {B('road')} throughout.</p>
    </header>
    <div class="g3">
      <article class="card"><p class="card__k">01</p><h3>Model interrogation {B('dev')}</h3>
        <p>Element counts by system, parameter completeness by family, where a given type is used,
        which elements are missing a required value. Today this is a script somebody has to write
        for each question. The value of a declared tool interface is that the question no longer
        needs a script.</p></article>
      <article class="card"><p class="card__k">02</p><h3>QA interrogation {B('live')}</h3>
        <p>Asking why a QA run produced a finding, which rule fired, and what else shares the same
        root cause. The rule sets and the findings are live today; what is missing is the
        conversational route into them.</p></article>
      <article class="card"><p class="card__k">03</p><h3>Coordination questions {B('live')}</h3>
        <p>Which findings belong to which discipline, what changed since the last federation, which
        issues recurred. The coordination data exists; querying it in plain language does
        not.</p></article>
      <article class="card"><p class="card__k">04</p><h3>Quantity queries {B('live')}</h3>
        <p>Quantities by system, by level, by classification, with the measurement rule and the
        element list behind each line. Automated extraction is live; asking for a cut of it is
        not.</p></article>
      <article class="card"><p class="card__k">05</p><h3>Documentation drafting {B('dev')}</h3>
        <p>Drafting the repetitive parts of a report, a schedule note or an issue description from
        model state, for an engineer to correct rather than to write from nothing.</p></article>
      <article class="card"><p class="card__k">06</p><h3>Onboarding a model {B('road')}</h3>
        <p>Answering "how is this model organised" for someone who has just inherited it — worksets,
        naming, parameter schema, system structure, where the conventions have been broken. Not
        built, and arguably the most valuable of the six.</p></article>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell split split--mid split--rev">
    <div>
      <div class="note note--sig" style="max-width:none">
        <p><strong>The read boundary is the design.</strong> Every use case above is a read. That is
        not a phase-one limitation with write access scheduled for phase two — it is the boundary we
        would build to and stay behind.</p>
        <p>A routine that silently edits a live model removes the one thing that makes an
        engineering deliverable worth anything: a person who is answerable for it. Automation here
        drafts, proposes and reports. It does not commit.</p>
      </div>
      <div class="note" style="margin-top:18px;max-width:none">
        <p><strong>Where an engineer signs.</strong> The review step is not a checkbox at the end. It
        is the point at which a named person takes responsibility for an output, and it is why the
        architecture keeps every AI-produced artefact in a reviewable state rather than in the
        model.</p>
      </div>
    </div>
    <div>
      <p class="eyebrow">What it must never do</p>
      <h2 class="sec-title">The list is short, and none of it is negotiable</h2>
      <ul class="spec__list" style="margin-top:22px">
        <li>Write to a live model without a named engineer accepting the change first.</li>
        <li>Close a coordination issue, change a status code or issue a deliverable.</li>
        <li>Produce an engineering value — a size, a load, a rating — presented as authoritative
        rather than as a draft for checking.</li>
        <li>Send model data outside the environment the client agreed to, or retain it afterwards.</li>
        <li>Operate against a document somebody else is actively editing, without their knowledge.</li>
        <li>Present a probabilistic answer with the confidence of a deterministic one.</li>
      </ul>
      <p class="lede" style="margin-top:22px">Every item on that list is currently being done
      somewhere in this sector, usually in a demonstration video, usually with the reviewing
      engineer edited out.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Security</p>
      <h2 class="sec-title">The questions to ask any vendor proposing this, including us</h2>
      <p class="sec-lede">These are not rhetorical. They are the questions that decide whether an
      AI integration is adoptable by a practice with NDAs and professional indemnity, and most
      current offerings answer them badly or not at all.</p>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Question 01<b>What leaves the machine?</b></div>
        <div class="spec__v">Which model data is transmitted, to which service, in which
        jurisdiction. "It is secure" is not an answer to this question; an architecture diagram
        is.</div></div>
      <div class="spec__row"><div class="spec__k">Question 02<b>What is retained, and by whom?</b></div>
        <div class="spec__v">Whether prompts, extracts or model data are stored, for how long, and
        whether they are used for training. A client NDA that predates the AI strategy does not stop
        applying because the tool is new.</div></div>
      <div class="spec__row"><div class="spec__k">Question 03<b>Can the tool list be enumerated and restricted?</b></div>
        <div class="spec__v">If the set of operations an assistant can perform cannot be listed and
        reduced, the integration cannot be governed, whatever the marketing says.</div></div>
      <div class="spec__row"><div class="spec__k">Question 04<b>Is there an audit trail?</b></div>
        <div class="spec__v">Which tool was called, against which document, by whom, and what it
        returned. Without this, an incident cannot be investigated and a finding cannot be
        defended.</div></div>
      <div class="spec__row"><div class="spec__k">Question 05<b>What happens when it is wrong?</b></div>
        <div class="spec__v">Not whether it can be wrong — it can. Whether the workflow has a review
        point designed into it that catches a wrong answer before it reaches a deliverable, and who
        is named at that point.</div></div>
      <div class="spec__row"><div class="spec__k">Question 06<b>Does it degrade safely?</b></div>
        <div class="spec__v">If the service is unavailable or the answer is refused, does the
        engineer's workflow continue, or has a dependency been introduced into the critical path of
        issuing a deliverable.</div></div>
    </div>
  </div>
</section>

<section class="section section--raise">
  <div class="shell">
    <header class="sec-head sec-head--wide">
      <p class="eyebrow">Where we actually are</p>
      <h2 class="sec-title">The honest position, stated as three lines</h2>
    </header>
    <div class="spec">
      <div class="spec__row"><div class="spec__k">Layer<b>Automation and checking routines</b>{B('live')}</div>
        <div class="spec__v">Running on client appointments now — model QA rule sets, clash
        classification, quantity extraction, documentation generation, parameter management. This
        predates the platform framing; it is how the work already gets done.</div></div>
      <div class="spec__row"><div class="spec__k">Layer<b>Model data extraction and reasoning</b>{B('dev')}</div>
        <div class="spec__v">Elements, parameters, systems and relationships read as structured
        data, with pattern and anomaly detection over it. In development, used internally on our own
        delivery, not released and not licensable.</div></div>
      <div class="spec__row"><div class="spec__k">Layer<b>MCP server for Revit</b>{B('road')}</div>
        <div class="spec__v">Not built. Published here because the architecture is coherent and the
        constraints are worth writing down, not because it exists. No date is committed, and if that
        changes this page changes with it.</div></div>
    </div>
    <p class="tiny" style="margin-top:26px">If you find a claim on this page that we cannot support
    at enquiry stage, that is a defect and we want to hear about it. The four-state legend behind
    every badge is published at <a href="platform.html#status" style="color:var(--sig)">capability
    status</a>.</p>
  </div>
</section>
{faq_block(FAQS, title="MCP and Revit — the questions worth asking",
           lede="Including the one about whether this is real, which is answered first.")}
{related_block("Where this connects to work that already exists", [
  ("services/bim-automation-services.html", "BIM automation services",
   "The live routines the protocol layer would sit above."),
  ("services/revit-services.html", "Revit services",
   "Templates, families and the parameter schema that make a model answerable at all."),
  ("automation.html", "AI and automation",
   "The eight agent workflows, their status, and where the engineer signs."),
  ("intelligence.html", "BIM Intelligence",
   "Why a model has to be authored to be read before any of this is possible."),
  ("platform.html#status", "Capability status",
   "The four-state legend this page is badged against."),
  ("digital-twin.html", "Digital Twin",
   "The other page on this site whose honest answer is mostly 'not yet'."),
])}
"""
