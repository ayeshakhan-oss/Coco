# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 05 (apps 3931-3942).
Same locked-template mechanics as build_cv_rejection_wave1.py. Drafted in main line
(agents unavailable). Every claim grounded in output/job42/cv_texts_all/<app>_*.txt."""
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

EMAILS = [
{
 "app_id": 3931, "first": "Aurangzaib", "name": "Aurangzaib Qureshi",
 "subject": "From a three hundred million portfolio to six billion, read closely",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A record spanning two decades of financial leadership deserves a precise explanation rather than a template, so here is an honest account of what we appreciated and exactly where the decision came from.", WHY),
 "s1": paras(
   "The banking arc is substantial by any measure. At Askari Bank you worked a credit portfolio from three hundred million rupees to six billion; at MCB you headed the credit hub for all of Balochistan with a portfolio above seven billion; and across twelve years at BankIslami you rose from Relationship Manager to Hub Manager responsible for the performance and expansion of seven branches, having mobilized an Islamic assets portfolio of a billion rupees along the way. Those are numbers earned in one of the most compliance-heavy industries there is.",
   "The learning appetite alongside the career is its own signal: an MBA at 3.78, a BBA at 3.96 with three scholarships, then an LLB and an LLM in corporate and commercial law completed mid-career, plus certified trainer credentials that made you the Islamic-banking resource person for an entire region. Professionals who keep formally studying two decades into their career are rare.",
   "And the recent chapters show range: Director of Business Development at Hybrid Solutions across commodities and currencies, Head of Business Development and Operations at FinTech Investments, and now Chief Operating Officer at North Cape Markets, analyzing economic and regulatory trends and advising clients on investments. You have operated at the top of small organizations and inside the machinery of large ones."),
 "s2": paras(
   "Here is where the decision came from, stated plainly. This seat is a hands-on growth-execution role in Pakistan's education ecosystem: its counterparties are provincial education departments, government officials and development-sector organizations, its rhythm is forty to sixty percent domestic field travel, and it is scoped for someone roughly four to six years into their career, carrying a pipeline personally and reporting into our Head of Growth as their second.",
   "The written application gave us two structural mismatches we could not reason past. First, terrain: twenty years of the record sit inside banking, capital markets and investment services, and we could not find an engagement with education, government-as-client, or the development sector. Second, altitude: a career that has reached Chief Operating Officer and Director level would be asked to operate several levels below its established scope, and the expectation of PKR 450,000 you shared sits well above what this role carries. With one seat to fill, we made the narrow choice to go with records proven on the seat's exact terrain and scale."),
 "s3": paras(
   "Our honest suggestion is to aim where your stack of credentials compounds rather than resets: senior commercial, credit or operations leadership in financial institutions, Islamic-finance ventures, or fintech firms building toward regulated markets, where the LLM in corporate law, the SBP training footprint and the branch-network expansion record are entry requirements rather than context that needs explaining. That is the arena in which two decades of your evidence speaks fluently and at full volume.",
   "Our openings live at taleemabad.com, and the organization does grow; if a role matched to financial leadership scope opens, we would welcome a fresh application from you."),
 "ps": "A credit portfolio grown twentyfold, then a law degree pursued in the middle of a full banking career. The pattern in your record is a person who refuses to stop building capacity, and that pattern will outlast any single process."
},
{
 "app_id": 3932, "first": "Tanzeela", "name": "Tanzeela Shahzadi",
 "subject": "A 3.7 while building three projects at once",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are early in your career, we want to be especially careful that this letter reads as what it is: a fit decision about one specific seat, with honest notes you can actually use.", WHY),
 "s1": paras(
   "What we noticed first is the breadth you have built while still completing your BBA in IT in Business at International Islamic University Islamabad, and holding a 3.7 while doing it. The application shows business analytics work turning customer and sales data into Excel dashboards, a responsive web project built in HTML and CSS with Python automation behind it, and a digital marketing engagement running since 2026 where you manage Facebook pages, Messenger and Instagram content for multiple clients.",
   "That last one matters more than it may feel from the inside: handling live community channels for real pages, while studying full time, is genuine working experience in audience behavior, content cadence and client accountability. Many graduates finish their degree without ever having owned a channel that real people respond to.",
   "The certification trail, digital marketing and web development completed in mid 2025, alongside SEO, reporting and Python foundations, shows someone deliberately assembling a modern commercial toolkit rather than waiting for a syllabus to provide one. That instinct is the raw material careers are made from."),
 "s2": paras(
   "Here is the honest center of the decision. This particular seat is scoped for someone roughly four to six years into their career: it reports to our Head of Growth as their second, carries responsibility for partnerships with provincial education departments and development-sector organizations, and runs on forty to sixty percent domestic field travel with a personally-owned pipeline and CRM discipline underneath it.",
   "The written application documents a professional story that is one to two years old and still running alongside a degree. That is not a shortfall against your stage; it is simply a different stage than this seat is built for, and placing someone at the start of their arc into a role calibrated for the middle of one serves neither the person nor the work. The gap here is time and reps, nothing else, and time and reps are exactly the things that accumulate on their own if you keep doing what the application already shows you doing."),
 "s3": paras(
   "Practical suggestions, offered directly. Target coordinator, executive and associate roles in marketing, growth or community work, where the interval between what you do and what you learn is shortest, and treat your current multi-page management work as a portfolio: screenshots, growth numbers, before-and-after engagement figures. Concrete artifacts separate early-career applications from the pile. When your BBA completes in 2026, two years of documented channel ownership plus the degree will read very differently than either alone.",
   "Our openings live at taleemabad.com, including early-career roles as the organization grows; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "Holding a 3.7, running client pages, and shipping a working website in the same stretch of life is a workload most people only manage once someone is paying them properly to do it. You are doing it on your own initiative, and that is the part that does not need a certificate."
},
{
 "app_id": 3933, "first": "Taqi", "name": "Muhammad Taqi Chattha",
 "subject": "Eight years of funnels, from zero to eight paying clients",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read closely and in full, and because it documents real craft, we want to give you an honest account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The performance-marketing record is concrete where many applications are vague. At USE Group you generated over a thousand qualified leads and five thousand app downloads while cutting Facebook cost-per-click by twenty eight percent; at Expedey you lifted qualified inbound enquiries by sixty percent and grew organic traffic forty five percent in six months; at Krank you built a full-funnel LinkedIn strategy with native lead-gen forms and improved click-through by more than twenty percent. Numbers, channels and mechanisms, all named.",
   "The achievement we kept returning to is scaling a startup agency from zero to eight paying clients in under three months, building the go-to-market strategy, the lead-generation engine and the positioning from scratch, profitable in its first quarter. Whatever else a hiring team debates, building a client base from nothing is not teachable from a course.",
   "And the adaptation instinct is current: AI-assisted content workflows cutting production time by thirty five to forty percent, an organic-first strategy that reached page one for a platform-restricted brand using only SEO, Quora and Reddit, and a deliberate move to formalize the craft with a digital media marketing degree in progress. The toolkit is being resharpened continuously."),
 "s2": paras(
   "Here is where the decision came from. This seat is the execution engine of a growth function whose counterparties are provincial education departments, government officials and development-sector organizations; whose rhythm is forty to sixty percent domestic field travel ending in district offices and classrooms; and whose core motions are institutional partnership building and deal closure, with digital channels in a supporting role rather than the lead one.",
   "The craft in your application is digital-first and campaign-shaped: paid media, SEO, conversion optimization, executed for SaaS, agency and e-commerce clients. Across eight years we could not find in the written application a government or public-sector engagement, an education-sector client, or a field-based acquisition motion, and the expectation of PKR 450,000 you shared sits well above what this role carries. The seat is also Islamabad-based with national travel, against a Karachi-anchored record. With one seat to fill, we went with evidence proven on that specific terrain."),
 "s3": paras(
   "A direct suggestion: your strongest documented pattern is building demand engines from nothing, so aim at roles where that is the whole job, growth or performance-marketing leadership in SaaS, e-commerce or agency settings, and lead every application with the zero-to-eight-clients story and the USE Group numbers, because they are verifiable and rare. If the impact sector attracts you, one deliberate digital-growth project for an education or development organization would connect craft we can already verify to terrain hiring teams in this sector need proven.",
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Page-one rankings for a brand that could not run a single paid ad, earned through SEO, Quora and Reddit alone, is the kind of constraint-driven creativity that no budget can buy. That resourcefulness travels everywhere."
},
{
 "app_id": 3934, "first": "Anwer", "name": "Anwer Hasan",
 "subject": "Ten years of analytics, from Herbion's 213 percent to a 30 million raise",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read closely and in full, and it deserves a specific accounting of what stood out and exactly where the decision came from.", WHY),
 "s1": paras(
   "The measurement discipline in your record is the deepest we have read in this cycle. A decade across FMCG, HR tech, telecommunications, healthcare, SaaS and logistics, with GA4, Tag Manager, Amplitude, Looker, Tableau and Mixpanel not listed as keywords but attached to actual systems you built: measurement frameworks at Bayt, subscription analytics at Zension, executive reporting for a UK client portfolio at Wicked Digital.",
   "The outcomes are named and unusual. Two hundred thirteen percent e-commerce growth in twelve months for Herbion's North American market; a thirty percent month-on-month sales lift at greenO with a top-performer recognition to show for it; a role in the go-to-market of Zaam, the GCC's first tech-subscription model, and in the partnership enablement between Zension and Virgin Mobile; and a contribution, through three consecutive years of exceeded benchmarks, to a thirty million dollar investment round. Analytics that ends in raised capital is analytics taken seriously.",
   "We also noted the early chapter that overlaps our world in spirit: being part of the core team that launched Pakistan's first nationwide same-day delivery service at TCS, a genuinely operational, on-the-ground undertaking."),
 "s2": paras(
   "Here is where the decision came from. This seat is not primarily an analysis seat: it is a hands-on partnerships-and-deal-closure role whose counterparties are provincial education departments, government officials and development-sector organizations, with forty to sixty percent domestic field travel and a personally-carried pipeline. Measurement supports the motion; the motion itself is relational and institutional.",
   "The written application documents ten years of digital strategy and analytics for consumer and corporate brands, largely in remote or regional-hub settings, and we could not find in it a government or education-sector engagement, an institutional deal cycle owned end to end, or a field-based acquisition rhythm. Your expectation of PKR 400,000 sits at the very top of what this seat carries, which narrows the case further when the terrain evidence is missing. With one seat to fill, we made the narrow choice to go with records proven on that exact ground. The relocation intent to Islamabad noted in your application was read and appreciated; the decision did not turn on it."),
 "s3": paras(
   "Our suggestion is to aim at the seats your record already argues for: senior digital analytics, growth strategy or marketing-science roles in subscription, e-commerce and platform businesses, in Pakistan or the Gulf market you have already worked, where the Zension and Bayt chapters read as direct qualification. If the impact sector calls to you specifically, analytics leadership inside a development organization or edtech would let the measurement depth transfer while the institutional terrain gets built.",
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Three consecutive years of exceeded benchmarks feeding into a thirty million dollar raise is the quiet kind of achievement that rarely fits on one CV line, and yours documents it. Numbers people trust get built into companies' futures; that is what happened there."
},
{
 "app_id": 3935, "first": "Waleed", "name": "Waleed Bin Malik",
 "subject": "Six years of paid media across three markets",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "Six years of hands-on paid-media execution across UK, US and MENA markets is a real foundation. The record shows end-to-end Google Ads management for a London executive-car service with conversion-attribution work aimed squarely at cost per lead; Meta and Google campaigns holding a steady B2B pipeline for agency clients at Good Omens; multi-channel accounts across Meta and TikTok driving direct sales at Marktonix; and e-commerce operations on Amazon, eBay and Shopify at AWM.",
   "Two things distinguish the application beyond the platforms. First, the collaboration line: refining lead-qualification criteria with sales teams to improve conversion is exactly the unglamorous interface work where paid media either compounds or leaks. Second, the certification discipline, Meta, Google Ads and Google Analytics all current, on top of an electrical engineering degree from GIKI, which explains the comfort with attribution models and tracking mechanics that many media buyers avoid.",
   "The trajectory from e-commerce operations to running client accounts to a remote UK marketing-manager seat inside six years shows steady, earned expansion of responsibility."),
 "s2": paras(
   "Here is where the decision came from. This seat is a growth-execution role whose center of gravity is institutional: partnerships with provincial education departments, government and development-sector organizations, pursued through forty to sixty percent domestic field travel and a personally-carried deal pipeline. Digital acquisition is one instrument in that motion, not the motion itself.",
   "The written application documents deep instrument-level craft in paid channels, and we could not find in it an institutional partnership, a government-facing engagement, an education-sector client, or field-based acquisition work. The seat would ask for a majority of time spent in rooms and districts rather than ad managers, and nothing in the record lets us verify that motion. With one seat to fill, we went with applications carrying evidence on that specific terrain."),
 "s3": paras(
   "Our suggestion is to keep compounding where the record is already strong and add the layer that multiplies it: performance-marketing roles in product companies rather than agencies, where you own a funnel end to end and the revenue number that follows it. The UK and MENA client work positions you well for remote-first growth teams, and one in-house chapter with a documented revenue outcome would move your applications into a different tier. Publishing your CPL and ROAS outcomes as concrete figures, the way your attribution work deserves, will help careful readers see the depth quickly.",
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "An electrical engineer from GIKI who chose marketing and then made the tracking layer a strength rather than an afterthought: that combination of rigor and channel craft is scarcer than either alone."
},
{
 "app_id": 3936, "first": "Muneeb", "name": "Muhammad Muneeb",
 "subject": "AI agents, RAG pipelines and an aircraft license",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and because the mismatch here is structural rather than a matter of quality, we want to explain it honestly.", WHY),
 "s1": paras(
   "The technical range in the application is genuine. Six years spanning AI automation, database administration, quality assurance and IT support, with current work that is squarely on the frontier: building AI agents on OpenAI and custom large language models, constructing retrieval-augmented generation pipelines, automating business processes and CRM workflows through APIs, and integrating those systems with databases and third-party services.",
   "The foundation underneath is unusually solid for someone doing frontier work: SQL Server administration with query tuning, stored procedures and security; disciplined manual and API testing with documented cases in Jira; and years of enterprise IT support. People who can both build the automation and administer the database it runs on are rare, and the certification trail, from AI agent development through Azure DevOps, shows the stack being maintained deliberately.",
   "And the origin story is memorable: an EASA Part-66 aircraft maintenance engineering license before the move into software. Aviation maintenance is a discipline of checklists, accountability and zero-tolerance quality, and that heritage is visible in how the QA chapters of your record are written."),
 "s2": paras(
   "Here is the structural fact, stated without decoration. This seat is a commercial growth role: its work is building partnerships with provincial education departments, government and development-sector organizations, carrying a sales pipeline personally, and spending forty to sixty percent of the time in domestic field travel. It is staffed from records in business development, partnerships, sales or growth marketing.",
   "The written application documents an engineering and operations career, and we could not find in it commercial work of any kind: no sales, no partnerships, no marketing, no revenue ownership. That is not a gap in the record; it is evidence the record belongs to a different profession than the seat. We would rather say that plainly than leave the impression something was almost there."),
 "s3": paras(
   "Two suggestions, offered in good faith. First, aim your applications at the seats your record argues for: AI automation engineering, workflow-automation consulting, QA leadership or database administration, where six years of hands-on evidence puts you in the strongest tier of applicants rather than outside the profile. Second, if commercial roles genuinely interest you, the bridge that exists in your record is the CRM workflow and automation work: solution-engineering and technical pre-sales roles at software companies value exactly that combination and would let you cross over without discarding the stack.",
   "Our openings live at taleemabad.com, and technology roles do open as the organization grows; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "From certifying aircraft to building AI agents is a career built twice from scratch. Whatever room you work in next, that capacity for reinvention is the most durable qualification in the file."
},
{
 "app_id": 3937, "first": "Taha", "name": "Muhammad Taha Arif",
 "subject": "The Exam Prep vertical you built, and what the years still owe you",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. We want to be precise about why, because yours was among the closest applications in this pool and the reason is narrower than you might guess.", WHY),
 "s1": paras(
   "The Dot and Line chapter is the most role-relevant thing we read in your application. Launching and scaling an Exam Prep vertical inside an edtech company, managing a cross-functional team of twelve, overseeing more than a hundred tutors, building an organic acquisition strategy that reached a fifty one percent conversion rate, developing B2B outreach frameworks for schools with pricing and curriculum mapping, and drafting a phased expansion roadmap across fourteen countries: that is growth work, in education, with the commercial and operational threads held together.",
   "The surrounding record reinforces it. At Egan-Jones you run marketing operations for more than eighty seven international conferences and negotiated commercial contracts above fifty thousand dollars; at Patients' Aid Foundation you built relationships with medical schools and managed donor engagement and fund reconciliation; at Calibre Institute you helped scale to three locations while revenue grew from eighty thousand to two hundred sixty eight thousand dollars; and at Wolfster you took a product from business model to two thousand units in twenty retail locations across four cities.",
   "The automation layer caught our attention too: workflows built on Make.com, the Claude API, Airtable and GitHub Actions to shorten turnaround times. That is a current, compounding skill most applicants at any level have not touched."),
 "s2": paras(
   "Here is the narrow, honest center of the decision. This seat carries a Senior Manager title for a reason: it is scoped for someone roughly four to six years past their degree who has carried institutional deal cycles end to end, alone, at government scale. Your bachelor's degree completed in 2024, and much of the record runs concurrently rather than sequentially, which makes the effective depth roughly two years. The expectation of PKR 420,000 you shared also sits above what the role carries.",
   "What we could not resolve from the written application was evidence of owned, closed institutional deals with public-sector counterparties, the specific motion this seat runs on daily. The B2B school frameworks at Dot and Line are the right direction; a completed arc of them, negotiated and signed by you, is what the seat's level demands. This is a timing decision about seat calibration, not a judgment about trajectory, and we want that distinction to be unmissable."),
 "s3": paras(
   "Our suggestion is specific: stay exactly on this path, but take the seats that let you close. Growth or partnerships roles at edtech and education companies scoped at the associate-to-manager level will hand you the deal cycles this application could not yet show, and given the pace your record documents, the gap between your years and this seat's window will close quickly. Keep the fifty one percent conversion figure, the fourteen-country roadmap and the contract negotiations at the top of your CV; they are the lines a careful reader remembers.",
   "Our openings live at taleemabad.com, and roles at several levels open as we grow; if a role matched to your current stage opens, we would welcome a fresh application from you, and we mean that concretely rather than politely."),
 "ps": "Most people describe verticals they worked in. Your application describes one you launched, staffed, priced and mapped across fourteen countries before your degree was two years old. The years will catch up to the record; they usually do."
},
{
 "app_id": 3938, "first": "Asad", "name": "Asad Bashir",
 "subject": "Sixty campuses, fourteen cities, and a seat shaped differently",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. An education-sector record of thirteen years deserves an exact explanation, so here is what we appreciated and precisely where the decision came from.", WHY),
 "s1": paras(
   "You have spent your career inside the world we work in. Ten years at The Millennium Education building and running a national career-guidance framework across sixty campuses in fourteen cities, conducting capacity-building visits across the network, organizing international university fairs with USEFP and the British Council, and negotiating MOUs with domestic and international universities: that is institutional education work at genuine national scale.",
   "The recognition trail supports the record: Outstanding Performance awards four consecutive years, the only staff member in the division to receive them consecutively, and the authorship of the High Achiever Book, a flagship publication adopted across all sixty campuses. Building a resource that an entire network standardizes on is a form of institutional influence most careers never produce.",
   "The current chapter adds commercial discipline: as Regional Manager at AHZ you direct multi-branch operations with a thirty percent expansion plan, structured KPI systems down to daily counsellor touchpoints, compliance oversight, and MOU development with international universities across eight countries. The management operating system described there, briefings, file-review standards, seventy-two-hour processing disciplines, is concrete and credible."),
 "s2": paras(
   "Here is where the decision came from. This seat is a hands-on growth-execution role scoped for someone roughly four to six years into their career: it reports into our Head of Growth as their second, personally carries a partnership pipeline with provincial education departments and development-sector organizations, and runs on forty to sixty percent domestic field travel. It is a deal-origination seat, not a network-administration one.",
   "Two structural facts made the decision. First, altitude: thirteen years of the record sit at senior manager and regional manager level, directing teams and multi-branch systems; this seat would ask you to operate well below that scope, carrying the pipeline yourself. Second, motion: the record's institutional relationships are admissions and counselling partnerships, universities receiving students, rather than government bodies buying or adopting programs, and the expectation of PKR 550,000 you shared sits far above what this role carries. Both facts are about the seat's shape, not about the professional described in the application."),
 "s3": paras(
   "Our suggestion is to aim at the level and motion your record has already earned: national or regional commercial leadership in education consultancies, school networks and edtech companies, where MOU portfolios, multi-branch expansion planning and counselling-network capacity building are the job itself. The AHZ expansion plan and the Millennium network footprint, stated with their numbers, make that case on their own.",
   "Our openings live at taleemabad.com, and senior roles do open as the organization grows; if a seat matched to leadership scale opens, we would welcome a fresh application from you."),
 "ps": "Four consecutive years of a recognition nobody else in the division earned even twice, inside a sixty-campus system, is consistency at a scale that cannot be faked. That record will speak for itself wherever it is read."
},
{
 "app_id": 3939, "first": "Moiz", "name": "Moiz Ahmed",
 "subject": "From ebook funnels to a fifteen-person growth unit",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest account of what we noted and where the decision came from.", WHY),
 "s1": paras(
   "The application documents a rapid climb through Karachi's digital-services industry: from lead and region-manager roles beginning in 2017, through Business Unit Manager at Protech and a unit-head seat at Enermation, to Vice President and Business Unit Head at 9to5 Digital Solutions, and now Head of Growth at Creatics since the start of 2025. Titles arrived early and kept arriving, which itself says something about delivery under pressure.",
   "The operating range described is wide: standing up a growth unit for the US market and building a team of fifteen, owning operations end to end from investor relations to brand activation and quality assurance, and reporting a two hundred eighty five percent return on investment alongside significant reductions in customer acquisition cost. The current work adds a product dimension, developing a self-service book-publishing application backed by AI insights.",
   "The self-investment is visible too: certifications in advanced analytics, search ads, content marketing and sales management, all completed within a single year, and a continuing project-management credential. The toolkit has been maintained alongside the climb."),
 "s2": paras(
   "Here is where the decision came from. This seat operates in a different arena than the one your record documents: its counterparties are provincial education departments, government officials and development-sector organizations; its motion is institutional partnership building and deal closure conducted through forty to sixty percent domestic field travel; and its evidence bar is owned public-sector or education-sector deal cycles.",
   "Across the written application, the growth craft described is digital-services and conversion-rate work, ebook funnels, web-design brands, PPC and inbound models, for private commercial clients. We could not find an education-sector engagement, a government-facing deal, or a field-based acquisition motion, and the expectation of PKR 550,000 you shared sits far above what this role carries. The seat is also Islamabad-based with heavy national travel against a Karachi-anchored record. With one seat to fill, we made the narrow choice to go with evidence proven on the seat's exact terrain."),
 "s3": paras(
   "Our suggestion is to consolidate where the record is already strong: growth and commercial leadership in digital products, SaaS and agency businesses, where unit economics, funnel discipline and team building are the whole job. One practical note on the document itself: the application's outcome claims, the return-on-investment figure and acquisition-cost reductions in particular, will land harder with careful readers when each is anchored to a named period, baseline and measurement source, because claims that specific invite verification, and verification is what converts a reader.",
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "A team of fifteen built from a standing start for a market eight time zones away is an act of organization as much as growth. That muscle, once built, transfers to any industry that will hand you a blank page."
},
{
 "app_id": 3942, "first": "Batul", "name": "Batul Jafri",
 "subject": "The trainer who trains the master trainers",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. A twenty-five year record in education deserves a precise explanation, so here is an honest account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "Your record sits at a rare junction of Pakistan's public and private education systems. As Evaluator and Trainer of Master Trainers at QAED you helped select the master trainers for Punjab and KPK; as a British Council training consultant on Project PEELI you have worked the public-sector teacher-development pipeline since 2016; and you reviewed academic materials against the Single National Curriculum 2020 and NCP 2022 for early childhood and primary. Very few professionals have credibility in both the provincial training machinery and elite private networks at the same time.",
   "The private-sector arc is equally substantial: Head of Early Years at The Educators' head office, Phase Leader at The City School's northern regional office, coordination and leadership roles across two decades at Beaconhouse and LGS, and authorship of textbooks used by a private school chain. Author, evaluator, trainer and system leader is a combination that compounds.",
   "The professional-development trail may be the most disciplined we have read this cycle: CELTA, ICELT from Cambridge, an AKU-IED certificate in educational leadership completed in 2024, Cambridge digital-technologies programme leadership, and a dozen more, sustained across every phase of a long career. The craft has never been allowed to sit still."),
 "s2": paras(
   "Here is where the decision came from, and it is entirely about the seat's shape. This role is a commercial growth-execution seat: it carries a partnership pipeline with provincial education departments and development-sector organizations toward signed agreements, reports into our Head of Growth as their second, is scoped for someone roughly four to six years into a commercial career, runs on forty to sixty percent domestic field travel, and is Islamabad-based against your Lahore anchor.",
   "The written application documents pedagogical, curricular and training leadership of a high order, and those are different crafts from deal origination and closure. We could not find in the application commercial pipeline work, revenue or agreement ownership, and the expectation of PKR 400,000 you shared sits at the top of what the seat carries, for a role that would use little of what makes your record exceptional. Placing a curriculum authority into a sales seat would waste the authority and serve neither side."),
 "s3": paras(
   "Our suggestion is to aim at the seats your record uniquely commands: academic leadership, teacher-development direction, curriculum advisory and ECE policy work with school networks, development programs and education companies, where the QAED and PEELI chapters are the qualification itself. Organizations building early-years products and programs, ourselves included, depend on precisely the expertise your application documents; the fit question here was about this one commercial seat, not about your relevance to education organizations.",
   "Our openings live at taleemabad.com, and education-craft roles do open as our work grows; if a role matched to academic and training leadership opens, we would welcome a fresh application from you."),
 "ps": "Somewhere in Punjab and KPK there are master trainers, selected partly by your judgment, now training teachers who teach children by the thousands. Few careers can trace their fingerprints that far downstream."
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
