"""
BIMRACE — legal page content (privacy, terms, cookies).

Split out of build.py during the Engineering Intelligence rebuild so the legal
text stays byte-identical while the marketing pages are rewritten. Exports
PRIVACY, TERMS and COOKIES.
"""

SITE   = "https://bimrace.com"
EMAIL  = "info@bimrace.com"
PHONE  = "+91 75079 58364"
TEL    = "+917507958364"
ENTITY = "BIMRACE PVT LTD"

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

