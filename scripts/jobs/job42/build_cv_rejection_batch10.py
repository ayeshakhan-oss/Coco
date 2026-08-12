# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 10 (apps 3998-4007).
Locked-template mechanics identical to batch09. Six org-side paragraphs baked in."""
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
 "app_id": 3998, "first": "Zulfiqar", "name": "Syed Zulfiqar Hameed",
 "subject": "Thirty-four years of service, answered with respect",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A record spanning three and a half decades of public and institutional service deserves a respectful, direct explanation, and that is what this letter is.", WHY),
 "s1": paras(
   "The breadth of institutional service in your record is remarkable by any standard: a decade as the longest-serving General Manager of the Associated Press of Pakistan; service as Liaison Officer and Secretary to the Honorable Chief Justice of Pakistan; a communications and records chapter with the USAID mission for Afghanistan and Pakistan; contract management for Meinhardt on EMAAR-DHA work; and roots going back to the Deputy Commissioner's office in Rawalpindi and the Municipality of Taxila. Few careers touch that many of the state's institutions.",
   "The learning trail never stopped either: from a Punjab University masters through certificates in information systems, project preparation, negotiation and fire safety, to a four-year homeopathy diploma pursued, in your own words, to serve ailing humanity. The Quaid-e-Azam Scout decoration of 1977 and two Best Public Relations Man awards speak to a lifetime of showing up for institutions and people alike.",
   "We read the warmth in your letter as well as the record, and both are acknowledged here."),
 "s2": paras(
   "Here is where the decision came from, stated plainly and with respect. This seat is a field-intensive commercial role: it carries a sales pipeline into provincial education departments and development-sector organizations, requires forty to sixty percent domestic travel with district-level groundwork, and is scoped for a professional roughly four to six years into a business development career.",
   "The written application documents administration, communications, protocol and contract management, and we could not find commercial deal origination in it; the seat's shape and its demands simply belong to a different lane than the one your long record was built in. That is a statement about fit, not about worth."),
 "s3": paras(
   "Our suggestion, offered sincerely: your record's natural continuation is advisory and part-time institutional work, board secretarial roles, protocol and liaison advisory, contracts review, bilingual drafting, where organizations pay for exactly the judgment and correspondence craft a career like yours accumulates, without the field grind this seat demands. The freelance bilingual communication practice you already run is the right instinct; formalizing it toward institutional clients would suit the record well.",
   *ORG,
   "Our openings live at taleemabad.com; if a role matched to advisory and administrative depth opens, we would welcome a fresh application from you."),
 "ps": "A career that has served a Chief Justice, a national news agency and a scout's oath with equal seriousness needs no addition from us. Thank you, genuinely, for offering it to an education company; the respect is returned in full."
},
{
 "app_id": 3999, "first": "Sobia", "name": "Sobia Bilal Ali",
 "subject": "From ORIC to NASTP, the ecosystem builder's path",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your record runs closer to institutional terrain than most of this pool, so the explanation below is exact about what stood out and what decided it.", WHY),
 "s1": paras(
   "The institutional-ecosystem thread across your record is genuine and sustained. At NASTP you have worked business development inside an aerospace technology park under Air Headquarters, liaising with industry, assessing project proposals through market analysis, and connecting private-sector collaborations to the right divisions. Before that, the ORIC chapter at NUMS put you at the university-industry interface for nearly four years: assessing the commercial and patent merit of research, linking inventors to investors, and coordinating international MoU visits to China and Malaysia alongside the Vice Chancellor.",
   "The accelerator chapter at TiE Islamabad adds startup-ecosystem management, mentors, investors, training calendars, donor-facing documentation, and the PMP certification with an MBA in finance gives the coordination record formal spine. Founding a consulting practice serving startups, SMEs and universities is a natural continuation of all of it.",
   "Nine years of standing between institutions and commerce, and being trusted by both sides, is a real credential."),
 "s2": paras(
   "Here is where the decision came from. This seat is a deal-carrying role scoped for roughly four to six years of commercial depth: it originates education-sector agreements with provincial departments and development organizations and closes them personally, at forty to sixty percent field travel, reporting into our Head of Growth as their second.",
   "Two facts decided it. First, motion: across the record the work is facilitation, assessment and program management, enabling other parties' agreements, and we could not find commercial cycles owned to signature with revenue accountability. Second, calibration: nine-plus years and an expectation of PKR 600,000 sit well above what this seat is scoped and graded for. Both concern the fit between one seat and one record, nothing broader."),
 "s3": paras(
   "Our suggestion is to aim at the seats the record actually argues for: partnerships and commercialization leadership at technology parks, incubators, ORICs and public-private platforms, where facilitation at institutional scale is the job itself. The consulting practice you have launched is well positioned for exactly that market, and formalizing two or three anchor retainers would convert the network into a durable business.",
   *ORG,
   "Our openings live at taleemabad.com, and senior partnership roles do open as the organization grows; if a seat matched to ecosystem leadership opens, we would welcome a fresh application from you."),
 "ps": "University research that found investors, startups that found mentors, and an aerospace park that found industry partners all have one coordinator in common in this record. Ecosystems need exactly that person; price the role accordingly."
},
{
 "app_id": 4000, "first": "Aimal", "name": "Aimal Khan",
 "subject": "Spirometry in Loralai, policy briefs in Islamabad",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because the mismatch here is structural, between a research career and a commercial seat, we want to explain it plainly and usefully.", WHY),
 "s1": paras(
   "The research record is careful and field-hardened. Your MPhil work on marble-dust exposure in Loralai, systematic field surveys, clinical spirometry, dose-response analysis in SPSS, ending in concrete recommendations on protective equipment and ventilation, is applied environmental health done where it is hardest to do. The groundwater assessment mapping contamination hotspots for municipal authorities shows the same pattern: rigorous collection, honest analysis, actionable output.",
   "The current chapter at the Pakistan China Economic and Cultural Council widens the lens: policy briefs on bilateral trade and investment corridors, analysis for senior advisors, and facilitation of business-to-business and government-to-government platforms. Add the operations chapter supervising a hundred-plus-employee office, and the record shows someone who can both think and run things.",
   "An M.Phil from Quaid-i-Azam University with EPA and meteorological internships underneath is a solid scientific foundation."),
 "s2": paras(
   "Here is the structural fact. This seat is a commercial growth role: originating partnerships with provincial education departments and development-sector organizations, carrying a sales pipeline personally, and traveling forty to sixty percent of the time toward signed agreements, against a bar of four to six years of business development depth.",
   "The written application documents research, policy analysis and office operations, and we could not find commercial work in it: no sales, no partnership cycles, no revenue ownership. The record belongs to the research and policy profession, and we would rather say that cleanly than imply a near miss."),
 "s3": paras(
   "Our suggestion is to compound the lane you are in: environmental and public-health research, monitoring and evaluation, and policy analysis roles at development organizations, where your field-survey discipline and SPSS depth are direct qualifications, and where the PCECC policy-writing chapter reads as senior evidence. Climate and health programs in Pakistan are funded and growing; your record sits squarely in their hiring profile.",
   *ORG,
   "Our openings live at taleemabad.com, and research and M&E roles do open as our work grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "Most policy briefs are written far from the dust they describe. Yours are written by someone who carried the spirometer to Loralai personally, and that difference shows in the work."
},
{
 "app_id": 4001, "first": "Mohsin", "name": "Mohsin Adeel",
 "subject": "Forty-five people on the floor, and the years still counting",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are early in your arc, this letter is exact about the variable that decided it.", WHY),
 "s1": paras(
   "The record shows early responsibility handled without drama: supervising a floor of forty to forty five employees at Hayzel Technology with a reported twenty five percent productivity lift; holding fifty-plus client accounts remotely for Kite Telco with retention improved by fifteen percent; onboarding a hundred-plus experts in the current networking role; and a real-estate marketing chapter running research, content and digital campaigns.",
   "The Public Accounts Committee internship stands out as an unusual early credential: reviewing government financial reports and audit findings, preparing briefing notes for committee members, and documenting proceedings inside the National Assembly. Exposure to how public accountability actually works is rare at any career stage.",
   "Three years in, the record already spans operations, accounts and stakeholder coordination, which suggests an operator still choosing his lane, from a position of competence rather than confusion."),
 "s2": paras(
   "Here is the variable. This seat requires roughly four to six years of business development depth with owned institutional deal cycles, government and development-sector counterparties, and a personally-carried pipeline through heavy field travel.",
   "The written application documents roughly three years across operations supervision, account handling and marketing support, and we could not find commercial origination or institutional cycles in it. The gap is stage and lane, both of which are still fully in your control."),
 "s3": paras(
   "Our suggestion is to pick the commercial lane now if it calls to you: business development executive and key-account roles at technology and services companies would convert your account-handling base into origination reps, and the parliamentary exposure gives you unusual comfort with formal institutions that most early-career salespeople lack. Three focused years there changes what every future application can claim.",
   *ORG,
   "Our openings live at taleemabad.com, and early-career roles open from time to time; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "Not many twenty-somethings have summarized audit findings for the Public Accounts Committee and then run a forty-person floor. The ingredients are unusual; the recipe is yours to choose."
},
{
 "app_id": 4002, "first": "Ali", "name": "Ali Khalid",
 "subject": "Nine markets, one seat, and an honest arithmetic",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Function-wise, yours is among the strongest commercial records in this entire pool, so the explanation below is precise about the arithmetic that decided it.", WHY),
 "s1": paras(
   "The partnerships record is elite by this market's standards. Regional merchant acquisition across nine MENA markets at talabat, with teams managed and a new vertical launched in Iraq; the HomeChefs vertical scaled nationally at foodpanda with partnerships spanning Nestle, Shan Foods, Jazz, Bank Alfalah and USAID; a national Innovation Sales function established at Bank Alfalah covering the full lifecycle from acquisition through API integration to revenue; and most recently the commercial launch of an integrated family entertainment destination at House of Habib, delivered at one hundred sixty percent of revenue targets.",
   "The foundations are equally serious: Pakistan's first quick-commerce operating model designed inside Carrefour, digital-banking and Easypaisa chapters carrying enterprise payment solutions, a Manchester economics degree and an executive MBA from the Lahore School of Economics.",
   "Ten years of building commercial functions from zero, across two regions, with named partners and delivered numbers: the craft is not in question anywhere in this letter."),
 "s2": paras(
   "Here is the arithmetic, honestly. This seat is a second-in-command execution role scoped for roughly four to six years of depth, reporting into our Head of Growth, with a compensation band that your stated expectation of PKR 770,000 exceeds by nearly double. Ten-plus years and function-head seats at House of Habib and Bank Alfalah sit well above its calibration, and the record's terrain, marketplaces, fintech and consumer platforms, does not include the provincial-government education cycles this seat runs on, though the USAID partnership thread comes closest.",
   "Seniority, band and terrain each narrowed the case; together they closed it. None of the three says anything against the record itself."),
 "s3": paras(
   "Our suggestion is to hold your level and price: commercial director and country-lead seats at platforms, fintechs and diversified groups are where this record belongs, and the House of Habib launch numbers give it a current, verifiable headline. If the impact sector genuinely interests you at some point, a senior seat with an education or development platform would inherit everything this record proves, at a calibration that respects it.",
   *ORG,
   "Our openings live at taleemabad.com, and senior commercial roles do open as the organization grows; if a seat matched to your scale opens, we would welcome a fresh application from you."),
 "ps": "Most careers get one zero-to-one story; this record contains at least four, on two continents. Whoever hires you next is buying that pattern, and it is worth exactly what you ask for it."
},
{
 "app_id": 4003, "first": "Ali", "name": "Ali Imtisal Naqi",
 "subject": "Seven market launches and the machinery behind them",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The operations record is deep and consistently quantified. Six years inside the Delivery Hero system, from scaling fifty-plus Pandamarts and delivering a three hundred fifty percent order increase in the twin cities, to managing global logistics across five APAC markets with a fifteen percent service-level uplift and seven market launches inside twelve months. Rider retention held at ninety five percent, order completion at ninety eight and a half, shrinkage below five percent: the numbers are named and unusually complete.",
   "The current LAAM chapter shows the same machinery applied to a marketplace: a partner ecosystem built from the ground up to a ninety six percent NPS, AI-enabled automation replacing manual workflows entirely, nine million rupees of quarterly GMV erosion prevented through governance frameworks, and pricing models that supported a tenfold GMV expansion into new categories.",
   "Eight years of building the systems that let platforms grow is a genuine and scarce record."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial origination role: partnerships with provincial education departments and development-sector organizations, pursued in person across districts at forty to sixty percent travel, closed as the accountable deal-carrier, against a four to six year calibration and a band your stated expectation of PKR 800,000 exceeds by roughly double.",
   "The written application documents platform operations, logistics strategy and vendor-ecosystem management, with the NGO rider-acquisition alliances at foodpanda as the nearest partnership thread, and we could not find owned institutional deal cycles or government counterparties in it. Terrain, calibration and band each pointed the same way."),
 "s3": paras(
   "Our suggestion is to aim at the seats this record commands: marketplace operations leadership, head-of-logistics and platform-strategy roles at e-commerce and quick-commerce companies across Pakistan and the Gulf, where the seven-launch APAC chapter and the LAAM automation work are direct qualification at senior level. The AI-automation thread is your differentiator; few operations leaders in this market can claim it with delivered systems.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Seven markets launched in a year means seven times someone trusted you with a blank map. Records like that do not wait long between chapters."
},
{
 "app_id": 4004, "first": "Sana", "name": "Sana Sherazi",
 "subject": "Fourteen years where mothers and newborns needed systems",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A fourteen-year development record deserves an exact explanation, so here is what we appreciated and precisely where the decision came from.", WHY),
 "s1": paras(
   "The maternal and child health record is substantial and current: leading the IPSAR project across Balochistan health facilities for Afghan refugees and host communities at Indus Hospital, building capacity in Kangaroo Mother Care and newborn care for lady health workers, and managing procurement, budgets and donor reporting under UNHCR and IRC coordination, all rolled out within a three-month inception window.",
   "The Pak Aid chapter adds the resource-mobilization thread this sector runs on: donor mapping, expressions of interest that secured grants from EHSAS UK and RDMC, and a monitoring and evaluation department established from scratch with SOPs and dashboards. The consultancy chapter on micronutrients and maternal outcomes shows the technical depth is real, not just managerial.",
   "Gender-transformative framing, MNCH specialization and hands-on budget discipline in one record is exactly what health programming needs more of."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial education-sector role: originating partnerships with provincial education departments and development organizations, carrying a pipeline personally through forty to sixty percent field travel, closing agreements with revenue accountability, scoped at four to six years of business development depth.",
   "The written application documents health-program implementation and grant acquisition, delivery-side craft, and we could not find commercial deal cycles, education-sector counterparties or sales accountability in it. Fourteen years also sit above the seat's calibration. The record argues, strongly, for a different seat than this one."),
 "s3": paras(
   "Our suggestion is to stay in the health-development lane where your record compounds: program management and business-development roles at health-focused organizations, where the grant wins at Pak Aid and the Balochistan delivery record are direct qualifications, and where MNCH specialization commands seniority. If proposal-writing energizes you, formalizing the resource-mobilization thread into a dedicated BD role at an INGO would use both halves of the record at once.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Somewhere in Balochistan there are health workers who hold newborns differently because of trainings you organized. Careers are measured in many currencies; that one holds its value."
},
{
 "app_id": 4005, "first": "Aman", "name": "Muhammad Aman Khan",
 "subject": "Eight countries of partnerships, built from Mardan",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours has genuine commercial threads running through it, so the explanation below is precise about what stood out and what decided it.", WHY),
 "s1": paras(
   "The Dunya Consultants chapter documents real commercial building: partnerships and representation agreements secured with universities and recruitment partners across eight countries, a counselling and sales team grown from two to twelve, a seventy percent enrolment-pipeline lift through structured outreach, branch profit-and-loss ownership, and twenty education seminars and expos delivered across the region. Building that from Mardan, outside the big-city ecosystems, deserves specific credit.",
   "The operations chapters before it, real estate administration at BRIQS and J7, office leadership at SoftoSol, show the record's administrative floor: documentation, MIS reporting and stakeholder coordination handled dependably across sectors.",
   "Willingness to relocate and travel nationwide, stated plainly in the application, was noted and appreciated."),
 "s2": paras(
   "Here is where the decision came from. This seat's cycles run at provincial-government scale: agreements with education departments and development-sector organizations, negotiated over months, at a Senior Manager calibration of four to six years of institutional deal depth.",
   "Your commercial record's motion is student-recruitment consultancy, university representation agreements and B2C enrolment pipelines, real commercial craft, but at a different counterparty scale and on the private side of education. The written application could not show government cycles or development-sector agreements, and the deep commercial chapter is one role, roughly two and a half years against a longer administrative arc. Terrain and depth together decided it."),
 "s3": paras(
   "Our suggestion is to keep converting education-sector access into bigger counterparties: institutional-sales roles at edtech companies, school-network expansion roles, or partnerships seats at education service providers would move you from recruiting students toward signing institutions, which is the exact bridge between your record and seats like this one. The eight-country partnership file is your proof of origination; aim it at organizational buyers next.",
   *ORG,
   "Our openings live at taleemabad.com, and education-facing roles at several levels open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "A team grown from two to twelve, and a pipeline grown seventy percent, in a market most companies ignore: you have already proven you can build where it is hard. Scale of counterparty is the only variable left."
},
{
 "app_id": 4006, "first": "Saad", "name": "Saad Salman Khan",
 "subject": "Dashboards three companies ran on",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The analytics record is corporate-grade and verifiable: real-time inventory and revenue tracking with automated ETL built at LG Electronics Toronto, lifting operational efficiency twenty percent and cutting repair turnaround from six days to three; an automated reporting framework covering seventy five client reports at Reformulary Group with financial models that armed the sales team's value cases; and twenty-plus SQL-backed Tableau dashboards across HR, finance and operations at Ericsson Montreal, alongside a company-wide server migration.",
   "The credential set matches: a Carleton MBA in finance on top of a computer science degree, with Tableau, Power BI, SQL and Python applied in production rather than listed. Three multinational employers across five years is a record that survived scrutiny repeatedly.",
   "The return to Pakistan brings a toolkit this market genuinely lacks at depth."),
 "s2": paras(
   "Here is where the decision came from. This seat is a field-origination role: partnerships with provincial education departments and development-sector organizations, built in person across districts at forty to sixty percent travel and carried to signature, against a bar of four to six years of deal-side depth.",
   "The written application documents business intelligence and strategy analytics in support of other teams' commercial motion, and we could not find owned deal cycles, institutional counterparties or field acquisition in it. The craft is the instrument panel; this seat is the driver's seat, and they are hired separately."),
 "s3": paras(
   "Our suggestion is to price the toolkit where it is scarcest: analytics and strategy leadership at Pakistani banks, telecoms and platforms, where five years of Canadian enterprise BI is a differentiated record, or revenue-operations roles where analysts sit closest to commercial teams. If deal-side work attracts you, RevOps is the proven bridge from your lane to quota-carrying seats.",
   *ORG,
   "Our openings live at taleemabad.com, and data roles do open as our work grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "Repair times halved, reports automated, migrations survived: your record's pattern is making other people's work measurable. Organizations eventually notice who built the instruments; make sure your CV says it first."
},
{
 "app_id": 4007, "first": "Dua", "name": "Syeda Dua Zehra Zaidi",
 "subject": "The early chapters, read carefully",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are at the start of your professional arc, this letter is honest about the gap and specific about what closes it.", WHY),
 "s1": paras(
   "What the written application shows: business development exposure with market and competitor research supporting strategic decisions, client pipelines built and managed on CRM systems, communication material developed for technology consulting services, and contribution to institutional campaigns including Pinktober with content strategy and student engagement threads.",
   "Those are the right first chapters for a commercial career: research discipline, pipeline hygiene and audience-facing communication, each of which compounds. The application also reached us from Karachi for an Islamabad-based national role, which we read as ambition rather than oversight.",
   "We want to be straightforward that the application's brevity limited what we could weigh; what was present, we weighed fully."),
 "s2": paras(
   "Here is where the decision came from. This seat requires roughly four to six years of documented business development depth, with institutional deal cycles owned personally at government scale and forty to sixty percent domestic field travel.",
   "The written application documents early-stage experience measured in months rather than years, and at this seat's calibration that gap cannot be reasoned past; it can only be closed by time and documented reps."),
 "s3": paras(
   "Our practical suggestions: first, take business development executive or associate roles where pipeline work is daily and measurable, and record every number you move. Second, build the document as you go, dates, employers, outcomes with figures, because at early stages the CV's completeness is itself evidence of professional discipline. Third, if education or impact work calls to you, coordinator roles at education companies and nonprofits are real doorways, and your student-engagement thread is relevant evidence for them.",
   *ORG,
   "Our openings live at taleemabad.com, including early-career roles from time to time; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "Every commercial career in this country started with someone building their first pipeline in a CRM nobody thanked them for maintaining. Yours has started; keep the receipts."
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
