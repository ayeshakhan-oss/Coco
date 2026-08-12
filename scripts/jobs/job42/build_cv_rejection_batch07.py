# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 07 (apps 3957-3968).
Locked-template mechanics identical to batch05/06. All five org-side paragraphs baked in."""
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
 "One last note on process: this decision closes your application for this specific opening only. Our roles are posted publicly as they open, each is read with the same care that produced this letter, and a future application from you starts from a clean page, weighed on the evidence it carries at that time rather than on this outcome.",
]

EMAILS = [
{
 "app_id": 3957, "first": "Mujtaba", "name": "Mujtaba Shuja",
 "subject": "A return on ad spend taken from three to ten",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours was among the more closely weighed applications in this pool, so the explanation below is precise about both what stood out and what decided it.", WHY),
 "s1": paras(
   "The digital growth record is deep and consistently quantified across a decade. At Bilbayt you took return on ad spend from three to ten on a two hundred ten dollar average order value while lifting acquisition three to five percent monthly; at the Imarat, Graana and Agency21 portfolio you ran roughly thirty million rupees of annual media toward a reported fifty-times return on high-ticket property; and at Connect Station and Telenor you ran acquisition for a long roster of consumer digital products, Tamasha, StarzPlay and the Telenor self-care app among them, with cost-per-acquisition held to single-digit rupees on some lines.",
   "The current Fiz chapter shows the full modern stack: lifecycle tooling evaluations across MoEngage and Braze, attribution infrastructure on Adjust, retention journeys built from drop-off analysis, and dashboards owning acquisition and lifecycle end to end. Add the product-management thread at Postingly, roadmaps, hypothesis testing, requirements, and the profile reads as a complete consumer-growth operator, not a channel specialist.",
   "The craft certifications, Google belts, platform credentials, marketing-automation depth across CleverTap and OneSignal, confirm what the outcomes already imply."),
 "s2": paras(
   "Here is where the decision came from. This seat's growth engine is institutional rather than digital: partnerships with provincial education departments, government officials and development-sector organizations, originated and closed personally, through forty to sixty percent domestic field travel and a pipeline discipline that lives in district offices more than dashboards.",
   "Across ten documented years we could not find in the written application a government-facing cycle, an education-sector engagement, or a field-based acquisition motion; the record's terrain is consumer apps and property portfolios, run brilliantly from behind the funnel. With one seat to fill on this specific ground, we went with evidence proven there, and we want to be clear the decision reflects terrain, not capability."),
 "s3": paras(
   "Our suggestion is to keep operating where your record is already elite: consumer growth leadership at apps, marketplaces and digital-product companies in Pakistan and the Gulf, where the Bilbayt and Fiz chapters are direct qualification. If the impact sector interests you, one engagement running digital growth for an edtech or development organization would add the terrain layer this application could not show.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Three-to-ten on return on ad spend is not luck twice over; it is a system. Operators who build systems find that their results follow them across any product they touch."
},
{
 "app_id": 3959, "first": "Sania", "name": "Sania Sardar",
 "subject": "Five years of coverage that never dropped",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The workload documented in your application is remarkable in a way that deserves naming. For extended stretches you held an onsite team-management role at Jacked Nutrition, a second concurrent onsite role at Jacked Fitness Arena, and separate night-shift remote engagements at Commerce Cave and Enove Automation, training teams, resolving escalations and coordinating with marketing and logistics across all of them at once. Very few professionals can document sustained parallel service operations like that.",
   "The craft itself is real: five-plus years leading customer support and online sales operations, building training programs that upskilled team members, monitoring live channels daily, and coordinating schedules so coverage never lapsed. Escalation handling and workflow coordination across e-commerce operations is unglamorous work that businesses quietly depend on.",
   "And the trajectory is upward: from operations assistant at a transport company to running multiple support teams, built step by step alongside completing a B.Com."),
 "s2": paras(
   "Here is where the decision came from. This seat is a senior commercial role: it requires roughly four to six years of business development or partnerships experience, carries a personally-owned deal pipeline into provincial education departments and development-sector organizations, and runs on forty to sixty percent domestic field travel toward signed agreements.",
   "The written application documents service-operations leadership, and we could not find in it commercial origination: no partnership building, no sales-cycle ownership, no institutional or education-sector engagement. The record is genuine; it argues for a different seat than this one."),
 "s3": paras(
   "Our suggestion is to aim where five years of your evidence counts fully: customer-experience leadership, support-operations management and e-commerce operations roles, where team training, escalation systems and multi-channel coverage are the job itself. Given the concurrent-roles history, one practical note: consolidating the story into outcomes per employer, response times improved, retention numbers, team sizes, will make the CV read as strongly as the work behind it.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Working days onsite and nights remote, for years, while finishing a degree, is endurance most CVs never have to prove. Whatever role you take next inherits that engine."
},
{
 "app_id": 3960, "first": "Mirha", "name": "Mirha Khan",
 "subject": "Fourteen thousand QAR in two months, three years out of university",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are early in a promising arc, we want this letter to be precise about the one variable that decided it.", WHY),
 "s1": paras(
   "For a 2023 graduate, the record moves quickly. At 365 Adventures you already hold a Products Manager seat: leading online travel agency strategy across Viator and GetYourGuide, onboarding directly with account managers, running the Meta ads account end to end across three destinations, and generating over fourteen thousand QAR in sales across March and April. Owning both the channel relationships and the paid engine at once is more surface area than most early-career marketers ever touch.",
   "The chapters before it compound: influencer campaigns, SEO-optimized content through SurferSEO, partnership building in the marketing-and-communications seat, and platform-specific strategies with KPIs attached as an intern. The economics degree underneath finished at 3.89, and the B2B partnerships exposure alongside B2C campaigns shows range.",
   "The pattern is a professional who gets handed more responsibility every few months and keeps absorbing it."),
 "s2": paras(
   "Here is the one variable, honestly stated. This seat carries a Senior Manager title scoped for roughly four to six years of commercial depth, and specifically for owned institutional deal cycles, government and development-sector counterparties, district-level field motion, agreements signed personally. Your record is approximately two years old and lives in consumer travel and digital channels; the written application could not yet show institutional cycles because the career has not yet had time to contain them.",
   "That is a timing gap, not a talent verdict, and we would rather name it exactly than dress it in vaguer language."),
 "s3": paras(
   "Our suggestion: keep taking seats where ownership arrives early, and if partnership work attracts you, tilt toward the B2B side of your current role, the OTA onboarding and partnership threads are already the right muscle. In two to three years, a record that adds owned commercial agreements to the current pace will read very differently against senior seats, including ours.",
   *ORG,
   "Our openings live at taleemabad.com, and roles at several levels open as we grow; if a role matched to your current stage opens, we would welcome a fresh application from you."),
 "ps": "A Products Manager seat within eighteen months of graduation, in a foreign market, with revenue attached: the trajectory is the credential. Protect it by choosing roles for what they let you own."
},
{
 "app_id": 3961, "first": "Fahim", "name": "Fahim Shaukat",
 "subject": "Ten years of showing up for the sale",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows a decade of steady commercial work across genuinely different selling environments: paint distribution at Berger, showroom and solutions sales at Cretesol, corporate furniture sales at Interwood with architect relationships built deliberately, and now managing the KRLF Cash and Carry store, where you hold inventory, budget, vendor purchasing and a team, and report a five percent sales lift from merchandising changes you implemented.",
   "Two threads stand out. First, relationship durability: the Interwood chapter describes maintaining client relationships through support and guidance rather than transaction-chasing, and building an architect network is patient, referral-grade work. Second, completeness: the current role makes you a full commercial operator, buying, stocking, pricing, selling and training, which is a wider span than most sales careers ever cover.",
   "The MBA completed mid-career, alongside the technical certification trail, shows the same steady accumulation."),
 "s2": paras(
   "Here is where the decision came from. This seat is a senior institutional-growth role: partnerships with provincial education departments and development-sector organizations, a personally-carried pipeline toward signed agreements at that scale, forty to sixty percent domestic field travel, and an evidence bar of owned institutional cycles.",
   "The written application documents retail, showroom and store commercial work with individual and corporate customers, and we could not find in it institutional or government-facing cycles, education-sector engagement, or deal work at the contract scale this seat operates on. The record is honest, consistent commercial craft; the seat simply sits on different terrain."),
 "s3": paras(
   "Our suggestion is to aim where the full-operator profile pays: branch, territory and retail-operations management roles at distribution companies and retail networks, where owning inventory, vendors and a sales team at once is the qualification. Quantifying the KRLF chapter further, basket sizes, recovery, stock-turn improvements, will strengthen every future application.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "From paint counters to corporate showrooms to running a store outright, the record reads like someone who never waited to be told the next thing to learn. That habit is the career."
},
{
 "app_id": 3962, "first": "Zeeshan", "name": "Muhammad Zeeshan",
 "subject": "A decade of interfaces, and a seat about agreements",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because the mismatch here is structural rather than a matter of quality, we want to explain it plainly.", WHY),
 "s1": paras(
   "The design record is long and increasingly senior: from freelance interface work on Fiverr and Upwork in 2015, through agency and product seats, to Senior Product Designer roles at Duseca and Wasila Tech in Dubai, and now Lead UI and UX Designer at Vizz Web Solutions, owning design strategy for web platforms, SaaS products and mobile applications, building scalable design systems and mentoring juniors.",
   "The portfolio breadth is real: call-center tooling like Onboardiq and Vox Insight with analytics and CRM integration thought through, a women's health tracker, a news product, an eye-testing application. Designers who work across domains that varied develop judgment that single-product designers do not.",
   "And the discipline shows in the process language: research, information architecture, usability testing, design systems, handoff. A computer science degree from FAST underneath gives the craft an engineering floor."),
 "s2": paras(
   "Here is the structural fact. This seat is a commercial growth role: its work is originating partnerships with provincial education departments and development-sector organizations, carrying a sales pipeline personally, and spending forty to sixty percent of time in domestic field travel toward signed agreements. It is staffed from records in business development, partnerships or sales.",
   "The written application documents a design career, and we could not find commercial work in it: no sales, no partnerships, no revenue ownership. That is not a gap in your record; it is evidence the record belongs to a different profession than this seat, and we would rather say so directly."),
 "s3": paras(
   "Our suggestion is to aim at the seats a decade of your evidence commands: lead and principal product-design roles, design-system ownership at SaaS companies, and design-management tracks, where the Vizz and Duseca chapters are direct qualification. If our sector appeals to you specifically, edtech products need exactly the research-driven, accessibility-conscious design your portfolio shows, and design roles do open in organizations like ours.",
   *ORG,
   "Our openings live at taleemabad.com, and design and product roles do open as our work grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "Ten years ago the record starts with freelance gigs; today it reads design systems, mentorship and strategy. That climb was self-built, client by client, and it shows in the work."
},
{
 "app_id": 3964, "first": "Ahmed", "name": "Ahmed Ali Jumani",
 "subject": "Nine years of quota, from Blue Area to Dubai",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours was weighed carefully, because the commercial record is real, so the explanation below is precise about what decided it.", WHY),
 "s1": paras(
   "The deal-carrying evidence across nine years is concrete. At Stonefly you held monthly sales targets of one hundred thousand dollars in cloud and IT solutions while leading a team of twelve past their numbers by thirty percent; at Zones IT you grew a managed account base by forty five percent; at the Etisalat SME channel in Dubai you built partnerships with twelve vendors and lifted business volume forty percent while running a cluster team against KPI targets. Acquisition, upselling, onboarding and retention all appear as owned work, not adjacency.",
   "The foundation is solid too: a Cardiff Business School MBA, an early banking chapter at NIB with one hundred fifty million rupees in current-account deposits raised, and CRM fluency across Zoho, HubSpot and Dynamics. The record describes a complete B2B commercial operator who has closed in two markets.",
   "We also noted the seniority arc: from relationship manager to territory ownership with full accountability for team results."),
 "s2": paras(
   "Here is where the decision came from. This seat's counterparties are provincial education departments, government officials and development-sector organizations; its motion is district-level field origination across Pakistan at forty to sixty percent travel; and its cycles are institutional agreements rather than corporate procurement.",
   "The written application documents corporate and SME technology sales, telecom channel work and banking, in Islamabad and Dubai, and we could not find in it a government-facing cycle, an education-sector engagement, or Pakistan field-acquisition work of the kind this seat runs on daily. The commercial muscle is proven; the specific terrain is not, and with one seat to fill we went with records proven on that exact ground."),
 "s3": paras(
   "Our suggestion is to aim the nine years where they compound immediately: enterprise and SME sales leadership at technology, telecom and cloud companies in Pakistan or the Gulf, where the Stonefly and Etisalat chapters are direct qualification. If institutional terrain attracts you, public-sector account roles at IT companies serving government would build the missing layer while using everything you have.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "A hundred thousand dollars a month in quota, met consistently, is a habit of finishing. Terrain can be learned; that habit usually cannot, and you already have it."
},
{
 "app_id": 3965, "first": "Imran", "name": "Imran Ullah",
 "subject": "Three roles in ten months, and the depth still to come",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are at the start of your professional arc, we want this letter to be exact about the gap, since it is one that time will close.", WHY),
 "s1": paras(
   "What the application shows is early momentum handled seriously. Within roughly ten months you have moved through operations at HBL Microfinance, client relations at Airblue, and into a Business Monitoring Officer seat at Zameen, tracking regional performance metrics, preparing management dashboards and flagging process deviations. Alongside it you have begun an MS in Project Management at SZABIST and stacked foundational certifications from Google and PMI.",
   "The instinct to document is visible everywhere in the CV: structured records, daily reports, tracked cases, process-bottleneck proposals. People who treat coordination as a craft rather than a chore tend to compound quickly, and the toolkit list, from advanced Excel through Trello, Asana and CRM systems, shows deliberate assembly.",
   "The move from a political science degree in Gilgit-Baltistan to operational seats in Islamabad, under your own steam, is its own evidence of initiative."),
 "s2": paras(
   "Here is where the decision came from, plainly. This seat requires roughly four to six years of documented business development or partnerships experience, with owned institutional deal cycles at the scale of provincial education departments, and it carries heavy field travel and a personally-managed pipeline.",
   "The written application documents under a year of professional experience, in monitoring and coordination rather than commercial origination. At this seat's level that gap cannot be reasoned past; it can only be closed by years, and yours have simply not arrived yet."),
 "s3": paras(
   "Our suggestion is to stay on exactly this trajectory but choose seats that add commercial exposure: business development coordinator, partnerships associate or project roles with revenue adjacency, where the reporting discipline you already have becomes the backbone of pipeline management. The MS in Project Management will pair well with commercial work; the combination of both is scarcer than either alone.",
   *ORG,
   "Our openings live at taleemabad.com, including early-career roles from time to time; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "From Karakoram International University to running dashboards at one of Pakistan's largest property platforms in under a year: the distance already covered says more than the CV's length does."
},
{
 "app_id": 3966, "first": "Yamna", "name": "Yamna Sarwar",
 "subject": "Three years of learning gap, closed in eighteen months",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. We want to be careful with this one, because the mission alignment in your record is real and the reason for the decision is narrow.", WHY),
 "s1": paras(
   "The Teach For Pakistan fellowship chapter is the heart of the application, and it is substantial. Selected at a four percent acceptance rate, you taught English to two hundred twenty girls in grades six and seven at a government school in Korangi and closed a three-year learning gap within eighteen months through deliberate lesson planning and remediation. You then became a recruitment assessor for the fellowship itself and built Ta'awun, a community partnership project connecting parents, students and teachers through structured engagement. That is education-sector work at the ground truth level, exactly where our own products live.",
   "The surrounding record shows range: a NUST civil engineering degree with a published thesis on digital twins for structural health monitoring, an AKU internship restructuring an academic catalogue, and a year of marketing work at Sparkleo lifting social outreach by sixty percent using outbound tools.",
   "Engineering rigor, classroom credibility and communication craft is an unusual and valuable combination."),
 "s2": paras(
   "Here is the narrow reason. This seat is a senior commercial role: roughly four to six years of business development depth, owned institutional deal cycles with government and development-sector counterparties, and a personally-carried pipeline through heavy field travel. Your professional record is approximately two years old, and its education chapter is teaching and community mobilization rather than commercial partnership work; the written application could not show deal cycles because the career stage has not yet contained them.",
   "That is a calibration decision about one seat, not a judgment of direction, and given where you have chosen to spend your first working years, we hope the direction continues."),
 "s3": paras(
   "Our suggestion is specific: your fellowship record is a strong doorway into education-sector roles at program associate and coordinator level, in edtech, education nonprofits and development programs, and the classroom credibility you carry is something most commercial education professionals never acquire. Roles that add partnership and stakeholder work on top of it would move you toward seats like this one quickly.",
   *ORG,
   "Our openings live at taleemabad.com, and education-facing roles at several levels open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you, and on this record we would read it with particular interest."),
 "ps": "Two hundred and twenty girls in Korangi read better because you spent eighteen months refusing to accept a three-year gap. Whatever the title on your next CV, that line already outranks most of what we read."
},
{
 "app_id": 3967, "first": "Maria", "name": "Maria Qazi",
 "subject": "Eighty percent audience growth on a national stage",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The storytelling record has genuine public-sector weight. At the Prime Minister's Youth Programme you built content strategy across five platforms toward roughly eighty percent audience growth, ran editorial calendars balancing policy priorities with audience interest, wrote and edited for the official youth magazine, and produced and hosted more than twenty podcasts and digital features. Translating technical government material into stories young audiences actually engage with is a craft our own communications work depends on.",
   "The range beyond it is real: leading a twenty-person team at Motive and building training for over three hundred employees, community building at Daftarkhwan inside the startup ecosystem, engagement work at SadaPay and DARVIS, and international representation at a youth advocacy conference in Japan as a panel speaker on global health.",
   "The through-line is audience insight: every chapter shows someone studying what people respond to and adjusting deliberately."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial growth role in which storytelling is an instrument rather than the job: its core motion is originating partnerships with provincial education departments and development-sector organizations and carrying deals personally to signature, through forty to sixty percent domestic field travel, at a bar of roughly four to six years of commercial depth.",
   "The written application documents communications, content and community craft, with the PMYP chapter adjacent to government but on the storytelling side of it, and we could not find owned commercial cycles, partnership origination or deal closure in the record. With one seat to fill, we went with evidence on the deal side of that line."),
 "s3": paras(
   "Our suggestion is to aim at the seats your record already argues for: communications and content-strategy leadership at development organizations, government programs and mission-driven companies, where the PMYP portfolio is direct qualification. If commercial work attracts you, partnership-marketing roles, where content craft meets sponsorship and alliance building, are the natural bridge from your record to deal-carrying seats.",
   *ORG,
   "Our openings live at taleemabad.com, and communications roles do open as our work grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "Twenty podcasts, a national magazine, five platforms and a stage in Japan, all before most careers find their voice: yours is already found. The only question left is which rooms you point it at."
},
{
 "app_id": 3968, "first": "Shafi", "name": "Muhammad Shafi",
 "subject": "Five thousand riders, and the ground you covered",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and because your record contains something this pool mostly lacked, we want to name it honestly alongside the decision.", WHY),
 "s1": paras(
   "What the record documents is real field-operations craft. At foodpanda you helped manage supply operations for the twin cities across a fleet of roughly five thousand riders, cut weekly offboarding from fifty two riders to fourteen through better training and process fixes, reduced no-shows from eight percent to five, and handled document verification and KYC compliance with sensitive data. Those are named, checkable operational outcomes.",
   "The inDrive chapters add the rarest thing in this pool: genuine ground game. Field surveys mapping travel demand across universities, terminals and markets; competitor studies across ride-hailing, vans and taxis; and recruiting drivers to the platform face to face, which is persuasion work done in the open air rather than over email. Most applications we read never leave the office; yours mostly lives outside it.",
   "The pattern across both companies is dependable execution where the operation actually happens."),
 "s2": paras(
   "Here is where the decision came from. This seat is a senior commercial role: roughly four to six years of business development depth, partnerships with provincial education departments and development-sector organizations, and institutional agreements carried personally from first meeting to signature.",
   "The written application documents field operations and individual-level recruitment, rider by rider, and we could not find in it institutional cycles, organizational partnerships or contract-scale commercial work. The field instinct is there; the counterparty scale this seat requires is not yet in the record."),
 "s3": paras(
   "Our suggestion is to convert the ground game into commercial rungs: field sales and territory officer roles at distribution companies, telecom franchises or fintech agent networks, where recruiting and managing partners, shopkeepers and agents rather than individual riders builds exactly the institutional muscle senior seats require. Your foodpanda metrics belong at the top of the CV; numbers that specific are rare at this level and readers notice them.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Reducing rider no-shows in a gig fleet is one of the hardest behavior problems in operations, and you moved it three points. Whoever hires you next should ask you exactly how; the answer is worth more than most certificates."
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
