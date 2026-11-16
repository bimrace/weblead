"""Founding Business Associates invitation page content."""
from urllib.parse import quote


EMAIL = "bimraceglobal@gmail.com"
SUBJECT = "Application – Founding Business Associate – BIM RACE"
MESSAGE = """Dear BIM RACE Team,

I am interested in becoming a Founding Business Associate of BIM RACE Private Limited.

My details are as follows:

Full Name:
Current Profession:
Area of Expertise:
Years of Experience:
Business/Technical Contribution:
Proposed Role:
Willingness to Contribute Towards Organizational Expenses:
Brief Introduction:

I would like to understand the proposed business associate arrangement, financial contribution structure, project participation and future opportunities.

Regards,
[Your Name]"""
MAILTO = (
    f"mailto:{EMAIL}?subject={quote(SUBJECT, safe='')}"
    f"&body={quote(MESSAGE, safe='')}"
).replace("&", "&amp;")


BODY = f"""
<section class="fba-hero">
  <div class="shell fba-hero__in">
    <div class="fba-hero__copy">
      <nav class="crumb fba-crumb" aria-label="Breadcrumb">
        <a href="index.html">Home</a><span aria-hidden="true">/</span>
        <a href="about.html">About</a><span aria-hidden="true">/</span>
        <span aria-current="page">Founding Business Associates</span>
      </nav>
      <p class="fba-kicker"><span aria-hidden="true"></span> BIM RACE PRIVATE LIMITED · INVITATION TO APPLY</p>
      <h1>BUILD TOGETHER.<br>GROW TOGETHER.<br><span>SHARE OPPORTUNITIES.</span></h1>
      <h2>Become a Founding Business Associate at BIM RACE Private Limited.</h2>
      <p class="fba-hero__lede">We are inviting committed professionals, technical experts and
      business-minded individuals to participate in establishing and growing a professional MEP
      Engineering and BIM Consulting organization.</p>
      <p class="fba-issuer">An invitation from <strong>Somnath Baste</strong>, Director, BIM RACE Private Limited · Pune</p>
      <div class="fba-actions">
        <a class="fba-btn fba-btn--light" href="{MAILTO}">Apply to become an associate
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M8 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>
        </a>
        <a class="fba-btn fba-btn--outline" href="#opportunity">Explore opportunity</a>
      </div>
    </div>
    <aside class="fba-hero__aside" aria-label="Opportunity overview">
      <p class="fba-aside__label">THE OPPORTUNITY</p>
      <h2>Build the foundations for enduring work.</h2>
      <p>Contribute professional expertise and shared, documented investment toward an emerging engineering practice.</p>
      <div class="fba-aside__stats">
        <div><span>Initial estimate</span><strong>₹35,000</strong></div>
        <div><span>Ways to contribute</span><strong>Professional + financial</strong></div>
      </div>
      <a href="#investment" class="fba-aside__link">View initial requirements <span aria-hidden="true">↓</span></a>
    </aside>
  </div>
  <div class="fba-hero__rule" aria-hidden="true"><span>ENGINEERING</span><i></i><span>PARTNERSHIP</span><i></i><span>GROWTH</span></div>
</section>

<section class="section section--flush" id="opportunity">
  <div class="shell fba-intro">
    <div>
      <p class="eyebrow">01 / About the opportunity</p>
      <h2 class="sec-title">A business-building opportunity, not a Director appointment.</h2>
    </div>
    <div class="fba-intro__body">
      <p class="sec-lede">BIM RACE is seeking founding business associates—not additional Directors.
      Associates contribute financially and professionally to the organization's establishment,
      operations, business development and project delivery.</p>
      <p class="fba-copy">The aim is to build a professionally managed organization with a strong
      technical team, reliable business operations, domestic and international project opportunities,
      and a sustainable business model. Contributions are discussed and documented before any
      commitment is made.</p>
      <div class="fba-contrib">
        <span>01</span><p>Company establishment and statutory compliance</p>
        <span>02</span><p>Business development and client opportunities</p>
        <span>03</span><p>Technical project execution and operational development</p>
        <span>04</span><p>Long-term organizational growth and reinvestment</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--raise" id="investment">
  <div class="shell">
    <header class="sec-head sec-head--wide fba-head">
      <p class="eyebrow">02 / Initial financial requirements</p>
      <h2 class="sec-title">Establish the essentials, in considered phases.</h2>
      <p class="sec-lede">These are current estimates for essential company infrastructure and
      compliance. Any expenditure and the contribution arrangement will be agreed and documented
      before funds are committed.</p>
    </header>
    <div class="fba-investments">
      <article class="fba-investment">
        <div class="fba-investment__top"><span class="fba-step">PHASE 01</span><span class="fba-mark" aria-hidden="true">01</span></div>
        <p class="fba-investment__eyebrow">CA &amp; company compliance</p>
        <p class="fba-price">₹20,000 <span>/ year</span></p>
        <p class="fba-investment__intro">Foundational accounting, filings and statutory coordination.</p>
        <ul>
          <li>CA appointment and coordination</li>
          <li>Annual company filings</li>
          <li>Accounting and documentation</li>
          <li>Mandatory statutory compliance</li>
        </ul>
      </article>
      <article class="fba-investment fba-investment--phase-two">
        <div class="fba-investment__top"><span class="fba-step">PHASE 02</span><span class="fba-mark" aria-hidden="true">02</span></div>
        <p class="fba-investment__eyebrow">Professional website development</p>
        <p class="fba-price">₹15,000 <span>one-time</span></p>
        <p class="fba-investment__intro">A professional digital presence to support the company's work.</p>
        <ul>
          <li>Corporate website</li>
          <li>Company profile</li>
          <li>Professional portfolio</li>
          <li>Digital corporate presence</li>
        </ul>
      </article>
    </div>
    <div class="fba-total">
      <div><span>ESTIMATED INITIAL REQUIREMENT</span><p>Annual compliance + one-time website development</p></div>
      <strong>₹35,000</strong>
    </div>
    <p class="fba-disclaimer"><strong>Contribution arrangement:</strong> Actual contributions will be
    divided equally among participating associates according to the mutually agreed arrangement.
    All contributions and expenditures will be documented transparently.</p>
  </div>
</section>

<section class="section" id="benefits">
  <div class="shell">
    <header class="sec-head sec-head--wide fba-head">
      <p class="eyebrow">03 / What associates receive</p>
      <h2 class="sec-title">Meaningful participation, with terms agreed in writing.</h2>
      <p class="sec-lede">The opportunity is to contribute to real work and organizational growth.
      Participation, responsibilities and commercial terms are defined clearly—not assumed.</p>
    </header>
    <div class="fba-benefits">
      <article class="fba-card"><span>01</span><h3>Project participation</h3><p>Contribute to suitable domestic and international MEP/BIM projects, based on expertise, project needs and availability.</p></article>
      <article class="fba-card"><span>02</span><h3>Project revenue and profit sharing</h3><p>Project-specific profit-sharing percentages are mutually agreed and documented before execution.</p></article>
      <article class="fba-card"><span>03</span><h3>Business development incentives</h3><p>Discussed incentives may apply when an associate independently brings a client or project.</p></article>
      <article class="fba-card"><span>04</span><h3>Founding Business Associate recognition</h3><p>Recognition of your contribution to the early establishment and growth of BIM RACE.</p></article>
      <article class="fba-card"><span>05</span><h3>Strategic business participation</h3><p>Opportunity to contribute to business development and planning within agreed responsibilities.</p></article>
      <article class="fba-card"><span>06</span><h3>Financial transparency</h3><p>Shared expenses, project calculations and agreed distributions are documented and reviewable.</p></article>
      <article class="fba-card"><span>07</span><h3>Professional networking</h3><p>Build professional relationships through technical collaboration and approved business activities.</p></article>
      <article class="fba-card"><span>08</span><h3>Long-term growth opportunities</h3><p>Contribute to a sustainable engineering organization and the opportunities it develops over time.</p></article>
    </div>
    <p class="fba-note"><strong>Project profit-sharing is not automatic.</strong> The percentage and
    distribution formula will be mutually agreed for each project, considering scope, expenses,
    client acquisition, delivery responsibilities and company retention.</p>
  </div>
</section>

<section class="section section--raise" id="roles">
  <div class="shell">
    <header class="sec-head sec-head--wide fba-head">
      <p class="eyebrow">04 / Associate roles</p>
      <h2 class="sec-title">Bring the expertise the organization needs.</h2>
      <p class="sec-lede">Roles are business responsibilities agreed between participants. They do
      not automatically confer statutory Directorship.</p>
    </header>
    <div class="fba-roles">
      <article><span>01</span><h3>Business Development Associate</h3><p>Develop client relationships, identify opportunities and support proposals and business growth.</p></article>
      <article><span>02</span><h3>MEP Engineering Associate</h3><p>Contribute mechanical, electrical or plumbing engineering knowledge to project delivery.</p></article>
      <article><span>03</span><h3>BIM Associate</h3><p>Support Revit modelling, BIM coordination, documentation and model quality.</p></article>
      <article><span>04</span><h3>Project Management Associate</h3><p>Coordinate project planning, communication, delivery schedules and execution.</p></article>
      <article><span>05</span><h3>Operations Associate</h3><p>Help develop the organizational processes and day-to-day operations of the practice.</p></article>
      <article><span>06</span><h3>Finance &amp; Compliance Associate</h3><p>Support CA coordination, financial administration and organized documentation.</p></article>
    </div>
    <a class="fba-text-link" href="/services/mep-design-services.html">Explore BIM RACE MEP engineering services <span aria-hidden="true">→</span></a>
  </div>
</section>

<section class="section" id="project-arrangements">
  <div class="shell fba-arrangement">
    <div>
      <p class="eyebrow">05 / Project revenue distribution</p>
      <h2 class="sec-title">Agree the commercial arrangement before work begins.</h2>
      <p class="sec-lede">Every project has its own documented arrangement. The distribution
      formula is agreed mutually before execution so that work, acquisition and reinvestment are
      accounted for.</p>
      <a class="fba-text-link" href="/services/bim-coordination-clash-detection.html">See BIM coordination capabilities <span aria-hidden="true">→</span></a>
    </div>
    <ol class="fba-factors">
      <li><span>01</span>Total project revenue received</li>
      <li><span>02</span>Project execution and operational expenses</li>
      <li><span>03</span>Client acquisition contribution</li>
      <li><span>04</span>Technical and managerial responsibilities</li>
      <li><span>05</span>Company retention and reinvestment</li>
      <li><span>06</span>Agreed project profit-sharing percentage</li>
    </ol>
  </div>
</section>

<section class="section section--raise" id="transparency">
  <div class="shell">
    <header class="sec-head sec-head--wide fba-head">
      <p class="eyebrow">06 / Financial transparency &amp; ownership</p>
      <h2 class="sec-title">Clarity protects every participant.</h2>
      <p class="sec-lede">The business associate relationship is based on agreed contributions,
      defined project participation and written commercial terms.</p>
    </header>
    <div class="fba-governance">
      <div class="fba-governance__items">
        <article><span>01</span><div><h3>Documented organizational expenses</h3><p>Shared organizational expenses will be mutually approved and documented.</p></div></article>
        <article><span>02</span><div><h3>Recorded contributions</h3><p>All financial contributions will be recorded with appropriate financial documentation.</p></div></article>
        <article><span>03</span><div><h3>Transparent project accounts</h3><p>Project revenues and expenses will be transparent according to the agreed arrangements.</p></div></article>
        <article><span>04</span><div><h3>Written project agreements</h3><p>Project participation and profit-sharing will be governed by written agreements.</p></div></article>
      </div>
      <aside class="fba-governance__boundary">
        <p class="fba-boundary__label">IMPORTANT DISTINCTIONS</p>
        <p>Business Associate status does <strong>not</strong> automatically provide company
        shareholding or Directorship.</p>
        <p>Any future equity participation, if considered, requires separate legal documentation
        and applicable corporate approvals.</p>
        <p>Company intellectual property, assets and client relationships remain protected; no
        ownership is automatically transferred to an associate.</p>
      </aside>
    </div>
    <div class="fba-expectations">
      <p class="eyebrow eyebrow--plain">What we value</p>
      <p>Professional ethics · Financial discipline · Equal responsibility for agreed expenses ·
      Long-term business development · Teamwork and mutual respect</p>
    </div>
  </div>
</section>

<section class="section" id="vision">
  <div class="shell fba-vision">
    <div class="fba-vision__stamp" aria-hidden="true"><span>BR</span><i></i><span>MEP · BIM</span></div>
    <div>
      <p class="eyebrow">07 / Our vision</p>
      <h2 class="sec-title">Building a professional engineering organization.</h2>
      <p class="sec-lede">Our vision is to establish BIM RACE as a recognized MEP Engineering and BIM
      Consulting organization serving domestic and international clients.</p>
      <p class="fba-copy">We aim to create a strong technical team, build sustainable business
      operations and develop long-term opportunities for everyone contributing to the organization.</p>
      <a class="fba-text-link" href="/about.html">Learn more about BIM RACE <span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<section class="fba-apply" id="application">
  <div class="shell fba-apply__in">
    <div>
      <p class="fba-kicker"><span aria-hidden="true"></span> 08 / EXPRESSION OF INTEREST</p>
      <h2>Interested in building something together?</h2>
      <p>If you believe in teamwork, professional responsibility, financial transparency and
      long-term business growth, we invite you to express your interest in becoming a Founding
      Business Associate.</p>
      <p class="fba-apply__fine">We will discuss individual responsibilities, financial contributions,
      project participation, revenue-sharing arrangements and future opportunities before
      formalizing any association.</p>
    </div>
    <div class="fba-apply__contact">
      <a class="fba-btn fba-btn--light fba-btn--apply" href="{MAILTO}">Apply via email
        <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4.5h12v8H2zM2.5 5l5.5 4 5.5-4" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
      </a>
      <a class="fba-email" href="mailto:{EMAIL}">{EMAIL}</a>
      <button class="fba-btn fba-btn--copy" type="button" data-copy-email="{EMAIL}" aria-describedby="copy-status">Copy email address</button>
      <p class="fba-copy-status" id="copy-status" role="status" aria-live="polite"></p>
      <p class="fba-apply__signoff">Let's establish something valuable together.<br><strong>Somnath Baste</strong> · Director, BIM RACE Private Limited · Pune</p>
    </div>
  </div>
</section>
"""
