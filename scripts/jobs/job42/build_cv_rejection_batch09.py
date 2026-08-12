# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 09 (apps 3984-3997).
Locked-template mechanics identical to prior batches. Six org-side paragraphs baked in."""
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
 "If you choose to apply again, whether with us or elsewhere, the same principle will serve you: lead the document with the numbers and outcomes only you can claim, because they are what a careful reader remembers after the file is closed.",
 "We are conscious, too, of what it means to receive a letter like this one. A no with reasons attached is still a no, and no paragraph of appreciation changes that on the day it arrives. We simply believe an applicant is owed the reasons, stated as carefully as we could manage them, and we hope their usefulness to you outlasts the disappointment.",
 "One last note on process: this decision closes your application for this specific opening only. Our roles are posted publicly as they open, each is read with the same care that produced this letter, and a future application from you starts from a clean page, weighed on the evidence it carries at that time rather than on this outcome.",
]

EMAILS = [
{
 "app_id": 3984, "first": "Sundas", "name": "Ummutullah Sundas Khan",
 "subject": "Fifty Shopify stores and the systems behind them",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record documents a genuine builder of commercial infrastructure. At Digital Blocs you have supervised the development of roughly fifty Shopify stores and a hundred WordPress sites, architected integration pipelines connecting storefronts to ERP and CRM systems, and assembled marketing data pipelines that pull Meta, Google and email data into unified dashboards. That is the plumbing on which other people's growth runs, built rather than merely operated.",
   "The earlier chapters compound it: a five-hundred-account portfolio held at ninety five percent retention at ANZ Inc, project leadership across UK and EMEA acquisition platforms at Calworth Glenford, marketing automation at LangSpire, and a data-science chapter modernizing hospital management systems. Three degrees, an MBA from Istanbul, a project-management masters and an MIS-focused BBA, plus a data-science bootcamp, show the toolkit being renewed deliberately.",
   "A decade of turning messy business requirements into working systems is a durable, verifiable craft."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial origination role: its work is building partnerships with provincial education departments and development-sector organizations in person, carrying a pipeline through forty to sixty percent domestic field travel, and closing institutional agreements.",
   "The written application documents technical program delivery and platform operations for commercial clients, and we could not find in it owned deal cycles, government or education-sector counterparties, or field acquisition work. The record argues for a different seat than this one, and with one role to fill we went with evidence on its exact motion."),
 "s3": paras(
   "Our suggestion is to lean into the rare intersection you hold: operators who understand both commerce and code are scarce, and e-commerce program leadership, digital-transformation consulting and technical product-operations roles would use the whole record at once. Naming revenue outcomes of the stores and pipelines you built, not just their count, will lift every future application.",
   *ORG,
   "Our openings live at taleemabad.com, and technology-facing roles do open as we grow; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "A hundred and fifty storefronts and sites exist because you built or supervised them. Builders with that count behind them rarely stay unclaimed for long."
},
{
 "app_id": 3987, "first": "Urooj", "name": "Syeda Urouj Abdulkhaliq",
 "subject": "Fifteen years of keeping the customer from leaving",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows steady, multi-department operational leadership. At Changan Auto Capital you lead CRM, after-sales, HR and parts simultaneously, manage internal and external audits under quality risk management protocols, run weekly KPI meetings, and carry customer-satisfaction improvement as a named accountability. Holding four departments at once in an automotive dealership environment is coordination work of real weight.",
   "The arc before it has range: administrative and HR support at Kashmir Education Foundation with compliance documentation, and a vice-principal chapter at a school leading academic and administrative staff. Education administration, NGO operations and automotive retail are three different disciplines, and the record shows competence in each.",
   "Fifteen years of showing up for operational detail, audits, filing systems, inventory, KPI cadences, is the kind of reliability organizations discover they cannot function without."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial growth role: originating partnerships with provincial education departments and development-sector organizations, carrying a deal pipeline personally, and traveling forty to sixty percent of the time toward signed agreements, with a bar of four to six years of business development depth.",
   "The written application documents operations, CRM administration and after-sales leadership, and we could not find in it commercial origination: no partnership building, no sales-cycle ownership, no institutional deal work. The record is genuine; its craft is retention and compliance rather than acquisition, and this seat lives on the acquisition side."),
 "s3": paras(
   "Our suggestion is to aim where the record compounds: after-sales and CRM operations leadership in automotive networks and service businesses, where QRM certification, audit readiness and CSI improvement are the exact profile. The education-administration chapter also keeps a door open to school-operations management, a field that rewards precisely your combination of academic and administrative oversight.",
   *ORG,
   "Our openings live at taleemabad.com, and operations roles do open as we grow; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "CRM, after-sales, HR and parts, audited and running, under one person: that sentence describes an operations professional at full stretch, and it is your current job description."
},
{
 "app_id": 3988, "first": "Nabila", "name": "Nabila Khan",
 "subject": "A hundred demonstrations in the country's teaching hospitals",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your record touches our terrain more than most in this pool, so we owe you an exact account of what decided it.", WHY),
 "s1": paras(
   "The institutional-education thread in your record is real. At IHI-Kupgrade you have delivered more than a hundred demonstrations and training sessions on clinical resources across top medical institutions nationwide, run monthly CME webinars with renowned hospitals and universities, coordinated faculty engagements and academic workshops, and led onboarding for new associates. Working senior faculty, clinicians and students toward adoption of a digital resource is institutional persuasion work, done inside exactly the kind of academic environments our own team walks into.",
   "The recognition trail is genuine: consecutive scholarships from the University of Karachi Alumni Association, a certified-trainer credential, and facilitation of a 3D anatomy virtual-reality setup at a medical college. The MS in Project Management just completed at Bahria adds formal structure to four years of applied coordination.",
   "Adoption-building, training delivery and stakeholder engagement at national scale, four years in, is a strong early record."),
 "s2": paras(
   "Here is where the decision came from. This seat carries a Senior Manager title against roughly four to six years of commercial depth, and specifically against owned deal cycles: agreements with provincial education departments and development organizations negotiated to signature, with revenue or contract accountability attached.",
   "Your record's institutional work is adoption and training on the delivery side of an existing product relationship, and the written application could not show commercial cycles, negotiation-to-signature ownership, or government counterparties. The distance between your record and this seat is one specific muscle, deal ownership, and it is a muscle your current terrain could let you build quickly."),
 "s3": paras(
   "Our suggestion is precise: you are closer to this work than most rejected applicants, and the shortest path across is a business development or institutional partnerships seat at a medical education, edtech or publishing company, where your demonstrated access to academic institutions becomes the pipeline and you take on the closing. Two years of owned agreements added to this record would make an application like this one read very differently.",
   *ORG,
   "Our openings live at taleemabad.com, and education-facing roles at several levels open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "A hundred rooms of clinicians and students, won over one demonstration at a time, is evidence of something no certificate shows: people let you teach them. That is the raw material of every partnership career."
},
{
 "app_id": 3990, "first": "Usman", "name": "Usman Bhatti",
 "subject": "The ninety million rupee pilot, a decade on",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours contains the single most on-terrain deal in this entire pool, so the explanation below is careful about what stood out and what decided it.", WHY),
 "s1": paras(
   "The Promethean chapter is the literal shape of this seat's work: launching digital interactive learning in Pakistan alongside the Sindh Ministry of Education, engaging UNDP and USAID stakeholders toward policy adoption, presenting the business case to a Federal Minister, and securing approval for a ninety million rupee pilot to digitize a hundred public schools, with Microsoft and Intel partner programs and a British High Commissioner launch built around it. Client acquisition across AKUH, Beaconhouse, KGS and Pakistan Army rounds out an education-B2G chapter very few careers in this country contain.",
   "The record around it shows executive range: a digital-transformation chapter at Sanofi building the multi-channel marketing framework with regional reporting into Turkey and Paris, and most recently co-founding, scaling and exiting A-LIST, a wellness business built from a twenty five million rupee project cost to six and a half million in monthly sales, twenty five percent annual growth and a successful acquisition, with DHA, CBC and KE liaison handled personally.",
   "Founder, corporate transformation lead and edtech pioneer in one record is genuine breadth."),
 "s2": paras(
   "Here is where the decision came from, honestly. The education-B2G evidence, commanding as it is, sits a decade back: the Promethean chapter closed in 2015, and the years since run through pharmaceutical digital strategy and consumer wellness entrepreneurship. This seat is a hands-on execution role scoped for roughly four to six years of current commercial depth, reporting into our Head of Growth as their second, at forty to sixty percent field travel.",
   "Eighteen years and a CEO exit sit well above the seat's calibration, the current-decade record sits off its terrain, and the expectation of PKR 400,000 lands at the very top of what it carries. Each fact narrowed the case; together they decided it. None of them diminish what the record contains."),
 "s3": paras(
   "Our suggestion is to aim at seats where the whole arc counts: commercial director and country-lead roles at edtech and education-services companies, where the ministry-facing pilot, the corporate transformation chapter and the founder exit read as a complete qualification rather than a mixed one. The education-B2G market has grown enormously since your Promethean years; senior seats in it would welcome that history back.",
   *ORG,
   "Our openings live at taleemabad.com, and senior roles do open as the organization grows; if a seat matched to that scale opens, we would welcome a fresh application from you."),
 "ps": "Somewhere in Sindh there are classrooms that went digital because you walked a business case up to a Federal Minister and came back with ninety million rupees. That sentence belongs at the top of every version of your CV."
},
{
 "app_id": 3991, "first": "Abdul", "name": "Abdul Jabbar",
 "subject": "Eighty percent lifts, measured and repeatable",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows a digital strategist whose claims come with percentages and mechanisms attached: an eighty percent performance improvement through a content audit and accessibility overhaul at Middlesex University, a sixty percent lead-generation increase from SEO-driven product content at Dynamics Solution and Technology, a newsletter converting at forty percent, and a ground-up WordPress and technical-SEO build for a UK green-energy brand, complete with AI-assisted tools you prototyped yourself.",
   "The credentials underneath are earned recently and deliberately: an MSc in Digital Marketing from Middlesex with a leadership award, an MPhil in cultural studies on merit scholarship, GDPR and AI-governance certifications, and working fluency across the modern technical-SEO stack including answer-engine and generative-engine optimization, which most practitioners have not yet touched.",
   "Higher education, green energy and B2B tech across Pakistan, the UAE and the UK is a genuinely portable record."),
 "s2": paras(
   "Here is where the decision came from. This seat is field-first and institutional: partnerships with provincial education departments and development-sector organizations in Pakistan, originated in person across districts at forty to sixty percent travel and carried to signed agreements. Digital visibility supports that engine; it is not the engine.",
   "The written application documents channel strategy, content governance and platform builds for institutional clients abroad, with a current UK base, and we could not find in it commercial deal cycles, Pakistani institutional counterparties or field acquisition work. With one seat to fill, we went with evidence proven on that terrain."),
 "s3": paras(
   "Our suggestion is to compound where the record already leads: senior organic-growth and digital-strategy roles at UK institutions and agencies, where the Middlesex and green-energy chapters are direct qualification and your AEO and GEO fluency is ahead of the market. If Pakistan's impact sector attracts you, remote digital-strategy engagements with development organizations would connect the craft to the terrain without requiring relocation.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "From a cultural-studies MPhil in Lahore to prototyping AI tools for an English energy firm: the record documents a person who refuses to let his lane be assigned. That has clearly served you, and it will keep doing so."
},
{
 "app_id": 3993, "first": "Usama", "name": "Usama Gilani",
 "subject": "Four promotions in two years, and the lane question",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record documents eight years of brand and growth marketing with real outcomes attached: a thirty percent brand-awareness lift and a first LinkedIn B2B campaign capturing two hundred qualified leads at Al Jamal Group; a co-marketing partnership expanding market reach by a quarter; a thirty percent lead and sales increase for a US client at Hanzo; and four promotions in two years at Nayatel, which is the kind of internal verdict no reference letter can fake.",
   "The chapter we weighed most carefully was Al Ghafoor Hospital, because building a patient-referral network with local hospitals and clinics is genuine institutional partnership work: identifying counterparties, structuring cooperation, and turning relationships into measurable volume. Alongside it you cut a marketing budget by ten percent through renegotiated vendor contracts, which is commercial discipline, not just creativity.",
   "A NUST MBA underneath and a stated fluency in AI-powered workflows keep the record current."),
 "s2": paras(
   "Here is where the decision came from. This seat's core is institutional deal origination at government scale: provincial education departments and development-sector organizations, engaged across districts at forty to sixty percent travel, with agreements carried personally to signature.",
   "The written application is anchored in brand strategy and integrated marketing, with the referral-network chapter as its one true partnerships thread, and we could not find government counterparties, education-sector cycles or field acquisition at the seat's scale. One documented institutional motion against a bar that demands years of them was the honest gap."),
 "s3": paras(
   "Our suggestion is to make the hospital chapter the seed of the next one: partnership-marketing and alliances roles at healthcare, services and consumer companies would let you convert brand craft into deal craft deliberately. Two or three owned partnership cycles from now, the record supports seats like this one, and the marketing depth will then be an advantage most pure salespeople lack.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Four promotions in two years happened because the people watching you daily kept deciding you deserved more. Carry that fact into every negotiation of your career."
},
{
 "app_id": 3994, "first": "Jonathan", "name": "Jonathan Shahid",
 "subject": "Nine years on the phones, honestly counted",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record documents nearly a decade of survival and progression in one of the hardest commercial environments there is: outbound and inbound sales floors. From customer sales associate chapters at Emmzee, Micronox and Touchstone, through a closer's seat at Momento verifying and closing medical-equipment sales, to a sales-manager chapter at Standard Telemarketing and a current revenue-consultant role at Next Order running HubSpot pipelines, lead qualification, demos and closings.",
   "Two things stand out. First, range of product: solar solutions, medical equipment, financial services and now software, each requiring a new pitch learned from scratch. Second, the climb itself: floor associate to team coach to manager to consultant is a progression earned call by call, and the current role's vocabulary, funnel optimization, pipeline management, data-driven decisions, shows the craft has modernized with the market.",
   "Phone sales careers that last nine years are rarer than they look; most people leave inside two."),
 "s2": paras(
   "Here is where the decision came from. This seat is an institutional field role: partnerships with provincial education departments and development-sector organizations, built face to face across districts at forty to sixty percent travel, with agreements negotiated over months and signed personally.",
   "The written application documents remote, individual-consumer sales cycles measured in calls and days, and we could not find institutional counterparties, contract-scale negotiation or field-based work in it. The selling instinct is proven; the counterparty scale and motion this seat requires are not yet in the record."),
 "s3": paras(
   "Our suggestion is to convert the closing skill into bigger rooms deliberately: B2B inside-sales and account-executive roles at software and services companies, where your HubSpot fluency and demo experience transfer directly and deal sizes grow with tenure. Each step up in contract size is a step toward institutional seats, and your record shows you climb.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Nine years of dial tones and objections would have filtered out most people by year two. Whatever room you sell in next, you have already passed the endurance test that matters."
},
{
 "app_id": 3995, "first": "Raza", "name": "Raza Qazi",
 "subject": "The operating system you built, and the seat that sells",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record documents a systems architect in the organizational sense: at Health and Group you designed a complete stage-based operating framework from narrative through sourcing, training, placement and post-placement; built a four-layer talent screening system; negotiated enterprise software procurement at discounts worth forty six thousand dollars annually; and designed the customer acquisition model, pricing logic and unit economics for the whole venture.",
   "The Edge Technologies chapters underneath are equally structural: a company-wide knowledge headquarters that became the source of truth, business-continuity protocols, HR policy authorship, a hundred fifty SCORM courses serving eight thousand learners, and an LMS ecosystem built and deployed globally. An MS in Public Health in progress and an IELTS 8.0 sit alongside.",
   "Very few six-year records contain this much institutional machinery designed from zero."),
 "s2": paras(
   "Here is where the decision came from. This seat is not a design seat: it is a deal-carrying one. Its work is originating partnerships with provincial education departments and development-sector organizations in person, across districts, at forty to sixty percent travel, and closing agreements as the accountable owner.",
   "The written application documents strategy, systems and commercial modeling built around other people's selling, and we could not find owned deal cycles, government counterparties or field acquisition in it. The expectation of PKR 500,000 also sits well above what this role carries. The record is impressive; it is simply the blueprint side of growth, and this seat is the signature side."),
 "s3": paras(
   "Our suggestion is to name your lane and charge for it: revenue-operations leadership, growth-infrastructure consulting and chief-of-staff roles at scaling companies are precisely what six years of your evidence argues for, and they pay for the systems mind rather than asking it to carry a bag. If you want the deal side, take one quota-carrying chapter deliberately; the combination of both would be rare and valuable.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Most operators run machines someone else designed. You keep designing the machine itself, four times now by our count. Organizations pay well for that once it has a name; make them use yours."
},
{
 "app_id": 3996, "first": "Alina", "name": "Alina Moin",
 "subject": "Forecasts three markets trust",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows a commercial analyst trusted with real markets: at Systems Limited on the BAT account you forecast Modern Oral volume sales for the Japan end market, own monthly industry-volume and share reporting for local and global consumption, and consolidate the cycle plan feeding demand-review and S&OP meetings. Forecasting a category for one of the world's most scrutinized FMCG portfolios is analytical work with money on it.",
   "The chapters before it deepen the same craft: revenue-growth-management solutions for BAT Romania that reduced missed revenue opportunities, route-to-market models built for Reynolds American across Tennessee using footfall and socio-economic segmentation, and two years running dynamic price segmentation and competitor NPI analysis for the Australian market. A GIKI electronics engineering degree explains the comfort with structured data underneath.",
   "Three continents of commercial analytics inside five years is a record that compounds."),
 "s2": paras(
   "Here is where the decision came from. This seat is a field-origination role: partnerships with provincial education departments and development-sector organizations, built in person across Pakistani districts at forty to sixty percent travel, carried to signed agreements, with a bar of four to six years of deal-side depth.",
   "The written application documents pricing, forecasting and market analytics performed for commercial teams, and we could not find owned deal cycles, institutional counterparties or field work in it. The craft is the intelligence behind commercial motion rather than the motion itself, and this seat is staffed from the motion side."),
 "s3": paras(
   "Our suggestion is to keep compounding the RGM lane, it is among the best-paid analytical specialties in FMCG, or, if the deal side calls, move to key-account roles where your pricing fluency becomes a negotiation weapon most salespeople never carry. Either path is well served by the record; the seat you applied for simply belongs to a third one.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "An engineer from GIKI whose forecasts steer decisions in Tokyo, Bucharest and Tennessee: quiet influence, three markets wide, five years in. That is not a small record; it is an early one."
},
{
 "app_id": 3997, "first": "Meriam", "name": "Meriam Hafeez Khan",
 "subject": "Fifty-seven thousand retailers on the other end of the line",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The Telenor chapter shows institutional coordination at genuine scale: leading the rollout of a nationwide HSE policy framework across more than four hundred franchise locations, holding franchise compliance above ninety percent month on month, and managing engagement with the Sacha Yar community of fifty seven thousand retailers through live streams and digital channels. Policy design, rollout discipline and mass-stakeholder communication in one role is a strong foundation.",
   "The surrounding record adds texture: a top-three quality ranking and a thirty percent customer-satisfaction lift at SadaPay, where you also built an internal audit system on Notion that raised that team's efficiency by half; an SEO chapter with thirty first-page rankings per client; and a co-founded social venture that worked toward a school for differently-abled young adults and financial-empowerment campaigns for the transgender community in Islamabad. A NUST MBA and a Dean's honor list underneath.",
   "The social-venture thread, brief as it was, tells us the mission instinct is real rather than rhetorical."),
 "s2": paras(
   "Here is where the decision came from. This seat carries a Senior Manager title against roughly four to six years of commercial depth, specifically owned institutional deal cycles: agreements with education departments and development organizations negotiated personally to signature.",
   "Your record spans roughly four years across coordination, compliance, customer experience and digital work, in chapters of one year or less, and the written application could not show commercial origination or deal ownership in any of them. The breadth is real and the trajectory is upward; the specific muscle this seat is built around has not yet had a chapter of its own."),
 "s3": paras(
   "Our suggestion is to choose the partnerships lane deliberately and stay in it: franchise-development, trade-partnerships or institutional-engagement roles at telecom, fintech and distribution companies would convert your compliance-rollout and retailer-engagement experience into owned commercial cycles. One sustained two-year chapter with agreements signed under your name changes everything about how this record reads.",
   *ORG,
   "Our openings live at taleemabad.com, and roles at several levels open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "A person who can hold four hundred franchises to a safety standard and still co-found a school project for differently-abled young adults is carrying both discipline and conviction. Careers built on that pairing tend to find their room."
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
