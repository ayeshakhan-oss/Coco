# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 06 (apps 3945-3955).
Locked-template mechanics identical to batch05. Org-side paragraphs baked in."""
import os, re

TEMPLATE = open(r"c:\Agent Coco\templates\cv_rejection_template_locked.html", encoding="utf-8").read()
OUT = r"c:\Agent Coco\output\job42\rejection_emails"
os.makedirs(OUT, exist_ok=True)

P = ('<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;'
     'font-size:15px;line-height:1.8;">{}</p>')

def paras(*texts):
    return "".join(P.format(t) for t in texts)

WHY = ("We write to every applicant this way for a simple reason: a decision that affects someone's "
       "next months should come with its reasoning attached. What follows is specific to you and to "
       "what you actually submitted, and we hope it is useful well beyond this one process.")

ORG = [
 "A note on how we work with applications at this stage: every submission to this role was read in full by a person, not filtered by software, and the decision recorded here was made on the written record alone. That is also why this letter cites your own material rather than a score or a template phrase.",
 "For context on the bar we applied: Taleemabad's growth work runs through government and institutional partnership cycles that take months of groundwork, district visits and patient follow-through before anything is signed, and the person in this seat carries that cycle personally from first meeting to closure. When we weigh written applications, documented evidence of having carried a comparable cycle end to end is the heaviest single factor in the decision.",
 "We also want to acknowledge the effort an application takes. Preparing a CV, answering the questions, and waiting through a process costs real time, and it is not lost on us that most organizations answer that effort with silence. We would rather answer it with specifics, as we have tried to do above.",
]

EMAILS = [
{
 "app_id": 3945, "first": "Ulfat", "name": "Ulfat Mahmood Khan",
 "subject": "Two thousand three hundred schools, and one narrowly shaped seat",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A twenty-one year record of education and development leadership deserves an exact explanation, so here is what we appreciated and precisely where the decision came from.", WHY),
 "s1": paras(
   "Few applications in any cycle document system-scale education delivery the way yours does. Leading the implementation of over 2,300 BRAC schools across Sindh, Punjab, KPK and Balochistan; the 1,400-school Sindh portfolio funded through the Education Fund for Sindh and the Sindh Education Foundation; the 700-school initiative in Rahim Yar district of southern Punjab with Adam Smith International and the Punjab Education Foundation; 255 pre-primary schools in KPK with 401 government teachers trained under UK Aid. These are exactly the ecosystems our own work lives in.",
   "The donor and partnership range is equally substantial: UNICEF, FCDO, USAID, UNDP, GIZ, Oxfam and provincial education foundations, with concept notes, proposals, budgets and business development plans authored across two decades, and two stints as Acting Country Representative holding donor relations and country strategy together.",
   "And the record keeps compounding: CEO of Hamza Development Foundation, Regional Director for Asia and Africa at MMTI, now Director of Project Development and Alliances at Pak Aid, alongside third-party validation and consulting engagements for the World Bank and FCDO through PricewaterhouseCoopers. The evaluation and research layer, baselines across 500-school portfolios, gives the delivery record an evidence discipline many senior careers never build."),
 "s2": paras(
   "Here is where the decision came from, and it is about the seat, not the stature of the record. This role is a hands-on growth-execution second-in-command: it reports into our Head of Growth, is scoped for someone roughly four to six years into their career, personally carries a partnership pipeline toward signed agreements, and spends forty to sixty percent of its time in domestic field travel doing origination work.",
   "Your last decade has been spent at CEO, Regional Director and Country Programme Manager altitude, directing organizations and portfolios rather than carrying a single pipeline. Asking a two-decade programme leader to operate as a second chair, several levels below the scope already held, would serve neither you nor the seat, and the delivery-leadership shape of the record, brilliant at running funded programmes, is a different craft from originating and closing the commercial agreements this role exists to produce. That distinction, narrow but real, decided it."),
 "s3": paras(
   "Our suggestion is to keep aiming exactly where your record commands: country-level programme leadership, business development directorships at development organizations, and senior advisory work of the kind the World Bank and FCDO engagements already document. Organizations negotiating education portfolios at provincial scale need precisely the donor fluency and delivery credibility your application shows.",
   *ORG,
   "Our openings live at taleemabad.com, and senior roles do open as the organization grows; if a seat matched to programme leadership scale opens, we would welcome a fresh application from you."),
 "ps": "Somewhere across four provinces there are thousands of classrooms that exist because portfolios you led got built. Few careers in this country can point to a footprint like that, and no single hiring decision touches it."
},
{
 "app_id": 3947, "first": "Uzam", "name": "Uzam Zafar",
 "subject": "A silver medal in Berlin and a control tower in Karachi",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The operations record is disciplined and measured. At The Road Ways you ran end-to-end freight operations exceeding five hundred thousand dollars a month, coordinated fifty vendors as a control-tower operator, and managed a million-dollar monthly fleet portfolio for clients including Unilever and Nestle. At inDrive you supervised a team of ten and lifted productivity twenty percent in a quarter. At Hutchison Ports you completed an intensive eighteen-month vessel-planning certification and held stock reconciliation at full accuracy.",
   "The Berlin chapter shows the same standards travel well: EU-wide invoicing at Sungrow with ninety eight percent on-time accuracy, vendor processing across SAP and Dynamics 365 improved by thirty percent, and an MBA at Hochschule Steinbeis finished as a silver medalist while working. Numbers, systems and follow-through, consistently.",
   "What the record tells us about you as a professional: you take unglamorous operational complexity, freight, ports, invoicing, and impose order on it. That is a durable, portable craft."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial growth role: partnerships with provincial education departments and development-sector organizations, a personally-carried deal pipeline, and forty to sixty percent domestic field travel toward signed agreements. Its evidence bar is owned commercial cycles, prospecting through negotiation to closure.",
   "The written application documents supply-chain and operations excellence, and we could not find in it commercial origination work: no partnership building, no sales pipeline ownership, no government or education-sector engagement. The record is strong; it simply argues for a different seat than this one. With one role to fill, we went with applications carrying evidence on the seat's exact motion."),
 "s3": paras(
   "Our suggestion is to compound where the record already leads: supply-chain, logistics and operations-excellence roles in Pakistan or the German market you are now qualified in, where the Sungrow ERP work and the freshly-minted MBA make a coherent, competitive story. If commercial work genuinely attracts you, the bridge in your record is vendor negotiation, the freight-bidding tools and cost negotiations you built are commercial acts, and roles in procurement or commercial operations would let you cross while keeping your operational depth.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "A silver medal earned in a second language, in a foreign system, while processing invoices to pay for the privilege: that line says more about your ceiling than any job title on the page."
},
{
 "app_id": 3948, "first": "Tariq", "name": "Mohammad Tariq",
 "subject": "Thirty years of ledgers that balance",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A working record reaching back three decades deserves a straightforward explanation, so here is what we noted and where the decision came from.", WHY),
 "s1": paras(
   "The record documents a steady, self-built ascent through one of Pakistan's largest retail organizations: from warehouse and procurement in-charge at Utility Stores Corporation's regional offices, through senior auditor and audit team lead at head office, to Regional Accounts Officer for Rawalpindi and Islamabad, and since 2021 Regional Head of Corporate Reporting at the head office of an organization with twelve thousand employees, four thousand stores and a turnover above one hundred twenty five billion rupees.",
   "The craft underneath is thorough: internal audits of entire regions, reconciliations, inventory valuation, sales-tax preparation, and the discipline of writing audit reports that competent authorities act on. The systems trail shows continuous adaptation, from GBMS through Microsoft Dynamics and Oracle e-Business training to the organization-wide ODOO ERP transition of 2022, where you work across six modules.",
   "And the education kept pace with the career rather than preceding it: an MPhil in Management Sciences, a Master of Economics, an MBA and a postgraduate diploma, layered on while working. That is persistence most careers do not contain."),
 "s2": paras(
   "Here is where the decision came from, stated plainly. This seat is a commercial growth role: its work is originating partnerships with provincial education departments and development-sector organizations, carrying a sales pipeline personally, and spending forty to sixty percent of the time in domestic field travel toward signed agreements.",
   "The written application documents an accounting, audit and corporate-reporting career, and we could not find commercial origination work in it: no partnership building, no sales ownership, no education-sector engagement. That is not a shortfall in the record; it is evidence the record belongs to a different profession than this seat, and we would rather say so plainly than leave ambiguity."),
 "s3": paras(
   "Our suggestion is to aim your applications where three decades of your evidence is the qualification itself: senior accounts, audit and corporate-reporting roles in retail networks, distribution companies and public-sector organizations, where the USC scale, the ERP transition experience and the audit authorship are exactly what hiring teams need documented. The ODOO modules line deserves a prominent place; ERP-transition veterans are scarcer than the certificates suggest.",
   *ORG,
   "Our openings live at taleemabad.com, and finance and operations roles do open as the organization grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "From a hospital dispensary in 1992 to corporate reporting for a hundred-billion-rupee network, with the ledgers balancing at every step in between: that is a career built on reliability, and reliability never goes out of demand."
},
{
 "app_id": 3949, "first": "Sana", "name": "Sana Pervaiz Malik",
 "subject": "Case formulations, group therapy, and a seat in a different field",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because your record sits mostly in another profession, we want to be clear about what we saw and why the decision was structural.", WHY),
 "s1": paras(
   "The clinical training arc is serious and current: an MS in Clinical Psychology at Bahria University underway on top of a BS in Psychology, with supervised placements at the Punjab Institute of Mental Health, Fountain House and the Step Ahead Autism Center, spanning assessments, case formulation, group and family therapy, and applied behavior analysis with children. Institutions of that standing do not hand placements to passengers.",
   "What caught our attention for a commercial application specifically: alongside the clinical track you have carried a business development role at Hajar Travels, analyzed market trends and negotiated partnerships there, recruited technical candidates using LinkedIn Sales Navigator and HubSpot at Mavericks United, and assisted teaching and research at Bahria. The capacity to run parallel professional tracks while completing a clinical degree is a real signal of organization and drive.",
   "The breadth of the internship trail, from Punjab Police community engagement to psychological evaluation work, shows someone who accumulates applied experience deliberately rather than waiting for it."),
 "s2": paras(
   "Here is where the decision came from. This seat is a full-time commercial growth role in the education sector: partnerships with provincial education departments and development-sector organizations, a personally-carried pipeline toward signed agreements, forty to sixty percent domestic field travel, and a bar of roughly four to six years of documented commercial experience.",
   "The written application documents a clinical career in progress with commercial work as a side current: the Hajar Travels role is recent and part-time alongside the MS, and we could not find owned commercial cycles, institutional partnerships or education-sector business work of the depth this seat requires. The record points, credibly and clearly, toward clinical psychology; this seat points elsewhere, and we do not think it would honor the training you are most invested in."),
 "s3": paras(
   "Our suggestion is to protect the main track: complete the MS, and if the intersection of psychology and organizations attracts you, roles in school mental-health programs, child-development organizations and education nonprofits would use both halves of your record at once, the clinical craft and the stakeholder skills. Organizations in our sector do hire for exactly that intersection, and your placements at autism and rehabilitation centers are direct qualifications for it.",
   *ORG,
   "Our openings live at taleemabad.com; if a role closer to psychology and child development opens, we would welcome a fresh application from you."),
 "ps": "A trainee who spends mornings in psychiatric wards and evenings negotiating travel partnerships is not confused about direction; she is building range early. When the two tracks eventually meet, that range will be the advantage."
},
{
 "app_id": 3950, "first": "Faheem", "name": "Muhammad Faheem",
 "subject": "Clean tracking, lean budgets, and a different center of gravity",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The application shows an unusually complete paid-acquisition toolkit for its stage. End-to-end ownership of lead-generation funnels across Meta, Google and TikTok; conversion tracking done properly, Meta Pixel, Tag Manager, GA4 and the Conversion API named as implemented systems rather than keywords; CRM lead flow through HubSpot, GoHighLevel and Zapier; and nurture sequencing behind the click, which most media buyers never touch.",
   "The client record has real range: ten UK-based small businesses managed simultaneously at One Key Solutions across restaurants, beauty and wholesale, each with its own targeting, tone and weekly reporting; e-commerce accounts where you rebuilt attribution to survive browser restrictions; and a current in-house seat at Mobisyntex owning pipeline reporting from ad platform to CRM.",
   "The discipline reads clearly: weekly KPI dashboards, budget reallocation by performance, A/B tested landing pages. For turning lean budgets into measured pipeline, the craft is genuine."),
 "s2": paras(
   "Here is where the decision came from. This seat's center of gravity is institutional: partnerships with provincial education departments, government and development-sector organizations, built through forty to sixty percent domestic field travel and a personally-carried deal pipeline, at a bar of roughly four to six years of commercial experience with owned institutional cycles.",
   "The written application documents channel-level acquisition craft for small and mid-sized commercial clients, and we could not find in it institutional partnership work, government-facing engagement, education-sector clients or field-based acquisition. The seat would spend a minority of its time anywhere near an ad manager, and with one role to fill we went with evidence proven on its actual terrain."),
 "s3": paras(
   "Our suggestion is to keep compounding the measurable: your strongest differentiator is tracking integrity, and in-house growth-marketing roles at product companies, where you own one funnel deeply rather than ten shallowly, will convert that into the revenue-ownership evidence that unlocks senior seats. Publishing your CPL and ROAS outcomes as concrete before-and-after figures in the CV will let careful readers see the depth in seconds.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Most people in paid media learn the ad platforms and skip the plumbing. You built the plumbing first, and that choice is why your numbers can be trusted; it will pay compounding returns for the rest of your career."
},
{
 "app_id": 3951, "first": "Moiz", "name": "Moiz Uddin Khan",
 "subject": "A hundred and ten partnerships, and a seat several sizes smaller",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A twenty-year executive record deserves an exact explanation, so here is what we appreciated and precisely where the decision came from.", WHY),
 "s1": paras(
   "The alliance-building record is the standout: more than one hundred ten strategic partnerships built at ARY Digital Network across banking, airlines, retail, hospitality and telecom, assembled into one of the UAE's largest lifestyle loyalty ecosystems, with Dubai Tourism and DTCM among the counterparties. That is partnership craft executed at ecosystem scale.",
   "The record around it is broad and senior: the First Gulf Bank PAYIT payment-ecosystem integration and bank-agnostic interoperability work at WOW Electronic Transportation under RTA compliance; a two billion rupee investment proposal structured at IMARAT Group; current international expansion leadership at Aamerah Holding in Doha; and a banking foundation running from ABN AMRO through Barclays, ADIB and Al Hilal, including the launch of the UAE's first Islamic credit card and over eight hundred eighty commercial due-diligence visits.",
   "Two decades across GCC markets, with named institutional references at chairman and banking-executive level, is an executive file, and we read it as one."),
 "s2": paras(
   "Here is where the decision came from, stated without decoration. This seat is a hands-on execution role scoped for someone roughly four to six years into their career: it reports into our Head of Growth as their second, carries its own pipeline into provincial education departments and development-sector organizations, and runs on forty to sixty percent domestic Pakistan field travel.",
   "Three structural facts made the decision. The altitude gap: a Chief Growth Officer operating as a second chair would be a misuse of both. The terrain gap: the record's institutional world is GCC banking, media and government services, and we could not find Pakistan education-sector or development-sector cycles in it. And the practical gap: a Doha base against a Pakistan field seat, with an expectation of PKR 800,000 that sits far above what this role carries. Each alone would narrow the case; together they closed it."),
 "s3": paras(
   "Our suggestion is to aim at the seats your file already argues for: chief commercial and growth-executive roles at GCC and Pakistani groups expanding across markets, where the loyalty-ecosystem build and the payment-interoperability work are the qualification. For Pakistan specifically, advisory and non-executive positions with fintech and consumer groups would monetize the network without asking the executive record to shrink into an execution seat.",
   *ORG,
   "Our openings live at taleemabad.com, and senior roles do open as the organization grows; if a seat matched to executive scale opens, we would welcome a fresh application from you."),
 "ps": "A hundred and ten partnerships is not a number, it is a habit of turning acquaintance into architecture. Habits like that outlast every market cycle they are built in."
},
{
 "app_id": 3952, "first": "Zaeem", "name": "Muhammad Zaeem Akmal",
 "subject": "Dashboards for a hundred thousand learners",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The analytics record is genuinely strong, and parts of it touch our world directly. As DAP Administrator for the State Bank's National Financial Literacy Program at MCB you manage learning data for more than one hundred thousand participants across 1,395 branches, with nationwide dashboards, sixty percent faster reporting turnaround and one hundred percent on-time regulatory cycles. Education-program analytics at national scale is not a common line on a CV.",
   "The trail before it is consistent: LMS and CRM analytics for seven thousand users at Askari Bank; real-time assessment dashboards on a UNICEF education project at Teletaleem, integrating hardware clickers with Moodle; and five years of freelance BI delivery. Power BI, SQL, AWS and embedded analytics, applied rather than listed.",
   "The engineering base underneath, a computer engineering degree and full-stack capability, explains why your dashboards ship as products rather than reports."),
 "s2": paras(
   "Here is where the decision came from. This seat is not an analytics seat: it is a commercial growth role whose daily work is originating partnerships with provincial education departments and development-sector organizations, carrying a pipeline personally through forty to sixty percent domestic field travel, and closing agreements. Data supports that motion; the motion itself is relational and commercial.",
   "The written application documents measurement and platform craft of a high order, and we could not find in it commercial origination: no partnership cycles owned, no sales or revenue responsibility, no field acquisition. The education-adjacent chapters, SBP literacy analytics and the UNICEF project, sit on the reporting side of those programs rather than the deal side. With one seat to fill, we went with records proven on the deal side."),
 "s3": paras(
   "Our suggestion is to lean into the rare intersection you already occupy: education-program analytics. EdTech companies, development organizations and program funders all need people who can make learning data legible at national scale, and your SBP-program chapter is direct evidence. Analytics leadership or data-product roles in that lane would use everything the application shows, and the embedded-analytics work positions you for product seats most analysts cannot reach.",
   *ORG,
   "Our openings live at taleemabad.com, and data and technology roles do open as our work grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "A hundred thousand learners across 1,395 branches, rendered legible on one screen: that is quiet, national-scale infrastructure work, and the people it serves will mostly never know your name. The ones who read CVs carefully will."
},
{
 "app_id": 3953, "first": "Ibrahim", "name": "Ibrahim Shah",
 "subject": "An honest reply to your application",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. We reply to every applicant with honesty rather than a form letter, and we want to do the same for you, including being honest about what your application did and did not give us to work with.", WHY),
 "s1": paras(
   "What the written application shows: schooling at Punjab Cadet High School, a basic computer course certification, and your base in Taunsa Sharif. It also shows something the document itself cannot say: the willingness to put your name forward for a demanding role at a national organization, which takes a measure of ambition that deserves a real answer instead of silence.",
   "We want to be careful not to invent praise the document does not support, because that would be a disrespect dressed as kindness. What we can say truthfully is that applying is a start every career requires, and that the honest gap here is documentation, not necessarily ability: a CV of a few lines gives a reader nothing to weigh, whatever the person behind it can actually do."),
 "s2": paras(
   "Here is where the decision came from, plainly. This seat is a senior commercial role: it requires roughly four to six years of documented business development or partnerships experience, involves working with provincial education departments and development-sector organizations, and carries heavy travel and a personally-managed deal pipeline.",
   "The written application does not document work experience of any kind, and at this seat's level that gap cannot be reasoned past. We would rather tell you that directly, together with what could change it, than leave you guessing."),
 "s3": paras(
   "If you want a path toward roles like this one, it builds in steps, and each step is achievable from where you are. First, any commercial experience is better than none: shop work, distribution, sales for a local business, mobile-load or agri-trading work all count if you record what you did and what changed because of you. Second, write it down: a one-page CV that lists an employer, dates, duties and one number you improved is worth more than any format or design. Third, add a skill with a certificate behind it, the computer course you completed shows you already know how to do this, and free courses in digital marketing or sales exist in Urdu. Entry-level roles, apprenticeships and sales trainee positions are the honest doorway, and people walk through it every year.",
   *ORG,
   "Our openings live at taleemabad.com, including junior roles from time to time; if a role matched to the experience you build opens, we would welcome a fresh application from you."),
 "ps": "You sent an application from Taunsa Sharif to an organization you had no connection to, on the strength of intention alone. Keep that boldness, add documentation to it, and it will start opening doors."
},
{
 "app_id": 3954, "first": "Ibrahim", "name": "Muhammad Ibrahim Janjua",
 "subject": "Four hundred sixty seven percent, and the years still arriving",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours is one of the applications where the reason is narrow and worth stating precisely, so here it is in full.", WHY),
 "s1": paras(
   "The growth record is real and unusually international for its stage. At Fleek, a Y Combinator W22 marketplace, you own new business across US, UK and EU markets: full-cycle identification, outreach, onboarding and nurturing of retail and reseller buyers, with an ICP rebuild that scaled the qualified prospect pool by four hundred sixty seven percent and lifted client acquisition by two hundred twenty five percent. Those are origination numbers, on cross-border terrain, with the mechanism named.",
   "The founder thread runs deep: a tourism and photography company started at sixteen and run for four years through a pandemic with zero outside capital, fifty-plus custom tours delivered to clients from seventeen nationalities; a current digital-transformation agency co-founded from zero; and a growth consultancy where you built a paid programme embedding early operators into live sales and ops functions. LUMS economics and political science sits underneath it.",
   "The pattern across all of it is the same: given nothing, you build a pipeline. That instinct is the scarcest raw material in commercial work."),
 "s2": paras(
   "Here is the narrow center of the decision. This seat carries a Senior Manager title against roughly four to six years of post-degree depth and, specifically, owned institutional deal cycles with government and development-sector counterparties in Pakistan, closed personally, at the scale of provincial education departments. Much of your record runs concurrently and internationally, which makes the effective depth roughly two to three years, and the expectation of PKR 600,000 you shared sits far above what this role carries.",
   "What we could not find in the written application was Pakistani institutional terrain: government-facing cycles, education-sector partnerships, or the district-level field motion this seat runs on daily. The marketplace craft is proven; the seat's specific arena is not yet, and at this title we could not bridge that on potential alone. This is a calibration decision, not a ceiling judgment, and we want that distinction to be unmissable."),
 "s3": paras(
   "Our suggestion is to keep taking seats that hand you closing reps, and if impact-sector work genuinely attracts you, take one deliberate engagement with a development organization or edtech, even a short consulting cycle, because it would connect origination craft we can already verify to the terrain sector hiring teams weigh heaviest. Keep the four sixty seven and two twenty five figures at the top of the CV with their mechanisms attached; they are the lines a careful reader remembers.",
   *ORG,
   "Our openings live at taleemabad.com, and roles at several levels open as we grow; if a role matched to your current stage opens, we would welcome a fresh application from you, and we mean that concretely."),
 "ps": "A sixteen-year-old who builds a company, keeps it alive through a pandemic, and then rebuilds prospect pools for a Y Combinator marketplace is running on something that cannot be taught. The years will catch up to the record; they usually do."
},
{
 "app_id": 3955, "first": "Abdullah", "name": "Abdullah Usama",
 "subject": "A decade of service levels held above ninety percent",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The operations record is long and quantified. A decade at Zong running a forty-agent customer-care team to a ninety five percent service-quality rating, holding a twenty-four-hour helpline above ninety percent service levels, and pre-launching the PAYMAX mobile-wallet helpline from pilot through five thousand-plus customers supported, with onboarding time cut by a quarter. At Zameen you were the liaison between a three-hundred-member sales force and its support teams, and the reporting cadence you built claimed a twenty five percent lift in decision-making efficiency.",
   "The current chapter shows upward trajectory: Manager Sales Planning and Performance at Mumtaz Group, working with executive leadership on strategy, redesigning SOPs and SLAs, and cutting turnaround time by thirty percent. The certification trail is being built deliberately alongside it, Lean Six Sigma Black Belt, PMP training, business analysis and Agile foundations, which signals someone converting operational experience into formal method.",
   "Across thirteen years the consistent skill is the same: taking a service operation, instrumenting it, and holding it to a number. That is a real and durable craft."),
 "s2": paras(
   "Here is where the decision came from. This seat's motion is commercial origination: building partnerships with provincial education departments and development-sector organizations, carrying a deal pipeline personally, and spending forty to sixty percent of time in domestic field travel toward signed agreements.",
   "The written application documents service operations, planning and process excellence, and we could not find in it owned commercial cycles: no partnership origination, no deal closure, no government or education-sector engagement on the buying side. The Mumtaz role plans and measures sales rather than making them, and that distinction, between the engine room and the hunt, is precisely the line this seat sits on the other side of."),
 "s3": paras(
   "Our suggestion is to aim where the record compounds: sales-operations, revenue-operations and service-excellence leadership in telecom, marketplaces and retail groups, where the Zong decade and the Six Sigma toolkit are direct qualifications. Revenue operations in particular is a growing discipline in Pakistani companies, and your combination of CS leadership, reporting infrastructure and process redesign is its exact profile.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Ten years of keeping a twenty-four-hour helpline above ninety percent is a promise kept roughly three and a half thousand nights in a row. People who keep promises at that frequency are rarer than any certification implies."
},
]

built = []
for e in EMAILS:
    html = TEMPLATE
    html = html.split("<!DOCTYPE")[1]
    html = "<!DOCTYPE" + html
    html = html.split("<!--\nCV REJECTION RULES")[0]
    html = html.replace("[SUBJECT_LINE]", e["subject"])
    html = html.replace("[ROLE]", e["role"])
    html = html.replace("[CANDIDATE_FIRST_NAME]", e["first"])
    html = re.sub(r'<p style="margin:0 0 18px 0;[^"]*">\[OPENING_PARAGRAPH:[^\]]*\]</p>', e["opening"], html)
    html = re.sub(r'<p style="margin:0 0 18px 0;[^"]*">\[SECTION_1_CONTENT:[^\]]*\]</p>', e["s1"], html)
    html = re.sub(r'<p style="margin:0 0 18px 0;[^"]*">\[SECTION_2_CONTENT:[^\]]*\]</p>', e["s2"], html)
    html = re.sub(r'<p style="margin:0 0 18px 0;[^"]*">\[SECTION_3_CONTENT:[^\]]*\]</p>', e["s3"], html)
    html = html.replace("[PS_CONTENT: one memorable, character-affirming line tied to a specific moment.]", e["ps"])
    html = re.sub(r'<!-- \[FEEDBACK_WIDGET\][^>]*-->', '<!-- FEEDBACK_WIDGET_HERE -->', html)
    assert "[" not in re.sub(r'<!--.*?-->', '', html, flags=re.S), f"unfilled placeholder in {e['name']}"
    path = os.path.join(OUT, f"{e['app_id']}_{re.sub(r'[^a-zA-Z0-9]', '_', e['name'])}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    words = len(re.sub(r'<[^>]+>', ' ', html).split())
    built.append((e["app_id"], e["name"], words))
    print(f"built {e['app_id']} {e['name']}: ~{words} words")
