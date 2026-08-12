# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — BATCH 08 (apps 3969-3982).
Locked-template mechanics identical to batch07. All five org-side paragraphs baked in."""
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
 "app_id": 3969, "first": "Sameen", "name": "Sameen Amjad",
 "subject": "Five hundred enterprises onboarded, and a seat scoped smaller",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours was among the closest applications in this pool on terrain, so the explanation below is precise about what stood out and exactly what decided it.", WHY),
 "s1": paras(
   "The institutional reach in your record is real and rare. At the Special Technology Zones Authority you led the end-to-end facilitation of zone developers and enterprises, onboarding more than five hundred enterprises through structured outreach and regulatory facilitation, building a network of over a hundred zone developers and institutional partners, facilitating MoUs and LoIs, and serving as focal person for the Gilgit Baltistan technology zones initiative. That is government-adjacent ecosystem work at national scale, on exactly the public-private terrain our own growth function lives on.",
   "The record around it is wide: transaction-advisory stakeholder engagement on P3A-funded feasibility studies for the COMSATS IT Park; STZA licensing processes managed end to end for Heavy Industries Taxila; a head-of-marketing chapter at Rapidev spanning rebranding and international events from GITEX to ITCN Asia; and a speaking footprint across NASTP, NIC and university platforms that shows genuine ecosystem standing.",
   "A decade of moving between the Chairman's office, regulators, investors and media without dropping threads is a coordination craft few applications document."),
 "s2": paras(
   "Here is where the decision came from. This seat is a hands-on deal-execution role scoped for roughly four to six years of commercial depth: it personally carries a pipeline of education-sector agreements with provincial departments and development organizations, from district-level groundwork to signature, at forty to sixty percent field travel, reporting into our Head of Growth as their second.",
   "Two facts decided it. First, motion: across the record, the institutional work is facilitation, communication and coordination, enabling agreements around you, and we could not find commercial cycles owned to signature as the accountable deal-carrier. Second, calibration: ten-plus years and an expectation of PKR 650,000 sit far above what this seat is scoped and graded for. Both are statements about fit between one seat and one record, not about the standing of the record itself."),
 "s3": paras(
   "Our suggestion is to aim at the seats your file actually argues for: partnerships and ecosystem-development leadership at technology authorities, development programs, investment-promotion bodies and public-private platforms, where convening, facilitation and government relations are the job itself rather than the support function. The STZA and P3A chapters are direct qualification for that lane at director level.",
   *ORG,
   "Our openings live at taleemabad.com, and senior roles do open as the organization grows; if a seat matched to ecosystem and partnerships leadership opens, we would welcome a fresh application from you."),
 "ps": "Five hundred enterprises brought into a new regulatory framework, one briefing and one roundtable at a time, is nation-building paperwork most people never see. It is seen here."
},
{
 "app_id": 3970, "first": "Zeerak", "name": "Zeerak Bhatti",
 "subject": "From LUMS to the planning desk, quickly",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are early in a well-built arc, this letter is precise about the single variable that decided it.", WHY),
 "s1": paras(
   "The record is young but unusually disciplined. A LUMS masters in supply chain and retail management on top of a COMSATS accounting and finance degree; a material-planning chapter at Fauji Fresh n Freeze running MRP on SAP and Oracle against stock-outs and excess inventory; and a current specialist seat at Systems Limited working the BAT account, where you manage new-product-introduction tracking, packaging artwork compliance and PO/GRN cycles reported at zero non-compliance.",
   "The LAAM chapter adds commercial hygiene: ledgers kept to IFRS standards, reporting templates that lifted efficiency seventeen percent, and variance reports feeding cost optimization of twelve percent. Internships at PTCL and PIA round out an early record that already touches planning, finance and execution.",
   "What the document says about you: process seriousness arrived before seniority did, which is the right order."),
 "s2": paras(
   "Here is the single variable. This seat requires roughly four to six years of commercial depth with owned institutional deal cycles, government and development-sector counterparties, district field motion, agreements signed personally. Your professional record is roughly two years old and sits in planning, procurement and reporting rather than commercial origination; the written application could not show deal cycles because the career stage has not yet contained them.",
   "That is a timing decision about one seat, and nothing more."),
 "s3": paras(
   "Our suggestion is to keep compounding inside the supply-chain lane where your credentials now stack cleanly, or, if commercial work calls, move toward demand-side roles, key account and trade marketing seats in FMCG, where planners who understand the numbers behind the shelf routinely become the strongest commercial operators. The BAT-account exposure is a door into exactly that path.",
   *ORG,
   "Our openings live at taleemabad.com, and roles at several levels open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "Zero non-compliance on procurement cycles in your first year on a global account is the kind of line that reads quiet and means a lot. Standards set early tend to stay."
},
{
 "app_id": 3972, "first": "Osama", "name": "Osama Ali",
 "subject": "Seven roles, honest reasons, and one missing thread",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, including the notes you added about your transitions, and here is an honest account of what we saw and where the decision came from.", WHY),
 "s1": paras(
   "First, something uncommon that deserves credit: your application explains its own job changes, company closures, a dissolved startup, timezone constraints, plainly and without varnish. That candor is rare in a hiring pile and it reads well.",
   "The record itself shows adaptability across genuinely different work: a current account-management seat at Zones IT Solutions handling B2B hardware, software and services portfolios with vendor partners like Cisco and Lenovo; top-seller stretches in US real-estate appointment setting; merchandising on Magento with Jira and ClickUp discipline; and two entrepreneurial chapters running flour-mill trading operations, buying wheat, managing the mill team, selling the product. Very different rooms, and you functioned in all of them.",
   "The BBA in marketing underneath, completed while working, fits the same pattern of persistence."),
 "s2": paras(
   "Here is where the decision came from. This seat is a senior commercial role: roughly four to six years of continuous business development depth, owned institutional cycles with government and development-sector counterparties, and a personally-carried pipeline through heavy field travel.",
   "The written application documents short chapters across sales support, virtual assistance, trading and account management, with the current B2B seat only months old, and we could not find sustained institutional cycles or education-sector work in it. The breadth is real; the seat needs depth on one specific terrain, and the record has not yet had the chance to build it in one place."),
 "s3": paras(
   "Our suggestion is consolidation: the Zones seat is the strongest platform in your record, and two to three unbroken years there, with named revenue outcomes and account growth you can claim, would convert a scattered-looking history into a coherent B2B story. Where the past chapters ended for external reasons, the current one is yours to compound; guard it.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "A person who can set appointments for Texas realtors by night and run a flour mill by day does not lack range or work ethic. What the next years should buy you is the one thing missing: an unbroken run."
},
{
 "app_id": 3974, "first": "Imran", "name": "Imran Sheikh",
 "subject": "An honest reply to your application",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. We reply to every applicant honestly rather than with a form letter, and in your case that includes being honest about what your application materials allowed us to evaluate.", WHY),
 "s1": paras(
   "What reached us legibly from your CV: a Bachelor of Commerce from Karachi University, links to a self-publishing presence on Amazon, a YouTube channel on Pakistani online business, an AI-focused podcast, and a Behance portfolio. The document itself is built as a visual piece, and much of its content did not survive conversion into readable text on our side.",
   "We want to be straight about the consequence: a hiring decision at this level rests on verifiable written evidence, employers, dates, responsibilities, outcomes, and the application as received did not carry that layer. Whatever the full story of your work is, the document did not get to tell it, and we will not guess at what we could not read.",
   "What we can acknowledge genuinely is the builder instinct the links imply: publishing, broadcasting and portfolio work under your own name takes initiative that many conventional CVs never show."),
 "s2": paras(
   "Here is where the decision came from. This seat requires roughly four to six years of documented business development or partnerships experience with institutional counterparties, and it is filled on written evidence of that record.",
   "The application as submitted did not document professional experience in an assessable form, and at this seat's level that gap cannot be reasoned past. We would rather tell you that plainly, along with exactly what would change it, than send a vague regret."),
 "s3": paras(
   "Two practical suggestions. First, pair the creative CV with a plain-text version: one page, employers, dates, three outcome lines per role with numbers attached, because most systems and many readers will only ever see what survives as text. Second, your self-built channels are assets if they are framed as evidence, subscriber counts, revenue, growth rates, rather than as links a reader must go explore. Make the document carry the proof.",
   *ORG,
   "Our openings live at taleemabad.com; if a role matched to your documented experience opens, we would welcome a fresh application from you."),
 "ps": "A person running a podcast, a channel and a publishing catalogue under his own name clearly knows how to start things. Put the same authorship into the document that represents you; it is the one channel a hiring team is guaranteed to watch."
},
{
 "app_id": 3975, "first": "Huboor", "name": "Huboor Sohail",
 "subject": "Four product lines, three continents, one remote desk",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows a digital marketer who wins international remote work repeatedly, which is its own market verdict. Managing four product lines simultaneously at Absoluit across the US, UK, UAE, EU and Norway; three years running B2B and B2C lead generation for a Canadian immigration firm across six-plus emerging markets; contract chapters in Saudi Arabia and Toronto health-tech; and a current growth-manager engagement at Stixor spanning CRM architecture, automation workflows and a website revamp.",
   "The craft trail is consistent: SEO audits that moved rankings within sixty days, weekly analytics reporting that redirected budgets, A/B tested funnels, and campaign lifecycles owned end to end. The MPhil in Economics from FJWU underneath gives the analytical habit a foundation.",
   "Holding distributed clients across five time zones for five years requires a self-management discipline most office careers never test."),
 "s2": paras(
   "Here is where the decision came from. This seat is field-first and institutional: partnerships with provincial education departments and development-sector organizations, originated in person across districts at forty to sixty percent travel, carried to signed agreements. Digital demand generation supports that engine; it is not the engine.",
   "The written application documents channel and CRM craft for commercial clients abroad, and we could not find in it institutional cycles, government-facing work, education-sector engagement, or on-ground acquisition in Pakistan. With one seat to fill, we went with evidence proven on that specific terrain."),
 "s3": paras(
   "Our suggestion is to formalize what you already are: a remote growth operator for international SMBs. In-house senior digital roles at product companies, or a productized consultancy with named retainers, would convert the scattered contracts into compounding equity. If the impact sector appeals, development organizations increasingly hire remote digital-demand specialists, and your multi-market record is direct qualification for those seats.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "An economist by training who became the person four foreign companies trusted with their pipelines: that trust was earned one report at a time, and it travels with you."
},
{
 "app_id": 3976, "first": "Jamil", "name": "Jamil Haider",
 "subject": "Six MOUs, ten hand pumps, and the scale still ahead",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Yours sits closer to our terrain than most of this pool, so we owe you a particularly exact account of what decided it.", WHY),
 "s1": paras(
   "The current chapter is genuinely on our map. As Strategic Partnerships and Philanthropy Coordinator at Shifa Foundation you have developed six MOUs with corporates, NGOs and educational institutions, authored proposals, concept notes and donor reports, run MEAL functions across live programs, and coordinated three multi-sectoral campaigns spanning healthcare, WASH and food security. The earlier Shifa Foundation USA chapter adds international donor engagement with a twenty percent lift in donor engagement and grant proposals that secured real funding for flood-affected communities.",
   "The range before it matters too: a business-development chapter at a software house running staffing pipelines for the Canadian market, a real-estate sales run with roughly twenty percent revenue growth, and a civil engineering degree at 3.72 that explains the structured, SOP-building instinct visible across every role.",
   "Partnerships work, donor fluency and delivery discipline in one early-career record is exactly the combination this sector needs more of."),
 "s2": paras(
   "Here is the honest center of the decision, and it is about scale and tenure rather than direction. This seat carries a Senior Manager title against roughly four to six years of commercial depth, and its cycles run at provincial-government scale: agreements with education departments and development organizations negotiated over months and signed personally. Your partnership record is real but young, roughly four years across mixed functions, with cycles at the MOU-and-campaign scale of a coordinator seat, and the written application could not yet show government counterparties or agreements at the magnitude this role carries daily.",
   "In a different cycle this profile is a development-sector growth career in the making; in this one, against this title, the depth gap decided it."),
 "s3": paras(
   "Our suggestion is to stay exactly on this road and let the cycles grow: partnerships officer and manager seats at larger development organizations and education programs will hand you government counterparties and bigger agreements, and each closed cycle compounds. Keep the six MOUs, the donor-engagement percentages and the volunteer-scale numbers at the top of the CV; they are already the right kind of evidence, they just need larger successors.",
   *ORG,
   "Our openings live at taleemabad.com, and partnerships roles at several levels open as we grow; if a role matched to your current stage opens, we would welcome a fresh application from you, and on this record we would read it with genuine interest."),
 "ps": "Ten community hand pumps exist because paperwork you wrote persuaded someone to fund them. That is the entire craft of this profession in miniature; the only variable left is scale."
},
{
 "app_id": 3978, "first": "Awais", "name": "Awais Tahir",
 "subject": "From the gym floor to corporate closings in five years",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The trajectory documented is steady and self-made: from customer service at a communications firm, through retention work at Vostro World Gym and a sales team lead seat at KK Marketing, into the corporate-sales track at Hanif Rajput x Vinci, where you were converted from management trainee to Assistant Corporate Sales Manager within six months and now run end-to-end B2B cycles, lead generation, proposals, quotations, tender and RFQ preparation, negotiation and closure, with corporate and institutional clients.",
   "The toolkit is being assembled deliberately: CRM pipeline discipline, proposal writing, a masters in supply chain management added alongside the work, and an eye on AI productivity tools. Promotion inside six months at a demanding catering-and-events business is a concrete performance signal.",
   "The record reads like someone learning the full commercial cycle on purpose, stage by stage."),
 "s2": paras(
   "Here is where the decision came from. This seat requires roughly four to six years of business development depth with owned institutional cycles at government scale, education departments, development-sector organizations, agreements built across districts over months, and it carries a Senior Manager title calibrated to that evidence.",
   "The written application documents around five years of commercial work whose institutional chapter, the current corporate-sales seat, is about eighteen months old and operates at the catering-contract scale rather than the provincial-agreement scale. We could not find government or education-sector cycles in the record, and the seat's bar on that specific terrain could not be bridged on trajectory alone."),
 "s3": paras(
   "Our suggestion is to keep exactly this slope but choose rooms with bigger contracts: institutional and government-facing sales roles at facilities, services and FMCG companies that bid formally, where your tender and RFQ experience becomes the core skill rather than a side one. Two or three closed institutional cycles from now, applications like this one will read very differently.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Trainee to Assistant Manager in six months is a sentence any reader understands instantly. Keep collecting sentences like it."
},
{
 "app_id": 3979, "first": "Hasaan", "name": "Hasaan Mehmood",
 "subject": "A decade of exports, read against a domestic field seat",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from. We also note you applied twice; both applications were read and this letter answers them together.", WHY),
 "s1": paras(
   "The export-marketing record is solid and institutional in its own right: a decade across Pakistan's textile majors, Kohinoor, Faisal Fabrics, and currently Nishat Mills' bath division, developing business with international buyers in the USA and Australia, carrying accounts from query and product development through pilot production to on-time shipment. Holding client relationships across time zones and seasons in home textiles is patient, detail-heavy commercial work.",
   "The strategic-costing thread stands out: implementing costing initiatives to protect retention and profitability is commercial judgment, not just merchandising. And the early ChenOne branch-manager chapter shows retail floor leadership before the export career began.",
   "MBA in marketing from International Islamic University underneath, and a record of promotion at each employer: the professional arc is coherent and earned."),
 "s2": paras(
   "Here is where the decision came from. This seat's terrain is domestic and institutional: provincial education departments, government officials and development-sector organizations, engaged in person across Pakistani districts at forty to sixty percent travel, with agreements carried to signature personally.",
   "The written application documents export-account management with international commercial buyers, run from the mill side, and we could not find domestic institutional cycles, government-facing work or education-sector engagement in it. The record is a different, genuine commercial craft on a different map, and with one seat to fill we went with evidence on this seat's map."),
 "s3": paras(
   "Our suggestion is to aim where ten years of your evidence counts at full weight: senior export-marketing and key-account leadership in textiles and home goods, or country-level buying-house roles representing international retailers, where your mill-to-shipment fluency is the entry requirement. Quantifying the account portfolios and retention record in the CV will sharpen an already credible story.",
   *ORG,
   "Our openings live at taleemabad.com; if a closer-fit role opens, we would welcome a fresh application from you."),
 "ps": "Careers that survive a decade in Pakistani textile exports have been stress-tested by cotton prices, freight crises and buyer seasons alike. That durability is the credential under all the others."
},
{
 "app_id": 3981, "first": "Mobeen", "name": "Mobeen Jamshed Khattak",
 "subject": "A gold medal, five publications, and a commercial seat",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read in full, and here is an honest, specific account of what we appreciated and where the decision came from.", WHY),
 "s1": paras(
   "The record shows a genuine analyst-administrator hybrid built inside higher education. At Air University you have risen from operations management to Assistant Director Placement, running job placements and internships, industrial linkages, alumni portal management, employment data and ranking analytics, alongside a five-year operations chapter handling budgets, procurement and HEC reporting. Career fairs, development weeks and SDG-focused events sit on top as delivered projects.",
   "The analytical layer is unusually deep for an administrative track: an MPhil in management sciences finished with a gold medal, five published research papers, a Google Data Analytics certification, and applied projects spanning Power BI, R and Python, including GIS election mapping for observation missions. A certified impact rater credential and an Asian Productivity Organization project in the Philippines round it out.",
   "Someone who runs the placements office and publishes peer-reviewed consumer research is carrying two careers competently at once."),
 "s2": paras(
   "Here is where the decision came from. This seat is a commercial growth role: partnerships with provincial education departments and development-sector organizations originated and closed personally, forty to sixty percent field travel, and a bar of four to six years of business development depth.",
   "The written application documents university operations, placement coordination and analytics, and while industrial linkages brush against partnership work, we could not find commercial cycles, revenue or agreement ownership, or deal-carrying evidence in the record. The craft documented is institutional administration and analysis, and this seat's craft is institutional selling; they are neighbors, but they are not the same street."),
 "s3": paras(
   "Our suggestion is to choose deliberately between your two strong lanes. If analytics is the future, the publication record plus the toolkit points at research and BI roles in education bodies and development programs. If partnerships attract you, university-industry liaison and corporate-relations leadership at larger institutions would convert the placement network you already run into formal partnership craft. Either lane rewards the record; splitting between them is the only real risk.",
   *ORG,
   "Our openings live at taleemabad.com, and education-facing analytical roles do open as we grow; if a matched role opens, we would welcome a fresh application from you."),
 "ps": "A gold medal, a Philippines productivity project and the annual career fair, all run by the same person, describes a rare kind of institutional glue. Whichever lane you choose, choose it on purpose; you have earned the choice."
},
{
 "app_id": 3982, "first": "Noor", "name": "Noor Fatima",
 "subject": "Three years of content, and the craft showing early",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Because you are early in your professional arc, this letter is exact about the variable that decided it, since it is one that time closes.", WHY),
 "s1": paras(
   "The record shows a working content professional, not an aspiring one. At Dragon Boat you have led promotional content production, run paid campaigns across Meta, Google and marketplace channels, managed listings on Daraz and MiliMart, and worked website usability alongside it. The parallel social-media management track since 2022 spans platform strategy, community engagement and a practical fluency in rental and marketplace advertising formats most marketers never touch.",
   "The tooling is current: AI-assisted production across image, video and copy workflows, Adobe and Canva craft, and platform-specific content instincts across five networks. A masters in media studies at SZABIST is underway on top of the broadcasting degree, and the thesis-adjacent coursework in AI-driven content matches where the industry is actually going.",
   "Three documented years of shipping content daily, while studying, is a real foundation."),
 "s2": paras(
   "Here is the variable. This seat is a senior commercial role: roughly four to six years of business development depth, institutional partnership cycles with government and development-sector counterparties, heavy field travel, and a personally-carried pipeline. Your record is three years old and lives in content and digital channels; the written application could not show commercial cycles because the career has not yet contained them.",
   "That is a timing and lane decision about one seat, not a verdict on the work."),
 "s3": paras(
   "Our suggestion is to finish the masters and then choose the lane on purpose: content and social leadership at brands, or the strategist track at agencies, where your AI-forward production skills are ahead of the market's average. If the education and impact sector appeals to you, organizations like ours hire content creators who can explain complex programs simply, and that is precisely the skill your record documents.",
   *ORG,
   "Our openings live at taleemabad.com, and content and communications roles do open as we grow; if a role matched to your stage opens, we would welcome a fresh application from you."),
 "ps": "You have spent three years learning to hold an audience's attention honestly, which is harder than most commercial skills. Wherever you point that next, it compounds."
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
