# -*- coding: utf-8 -*-
"""Job 42 CV-rejection feedback emails — WAVE 1 (3 archetype pilots).
Layout: templates/cv_rejection_template_locked.html (v8, LOCKED — placeholders only).
Rules: 800+ words, CV-only evidence (no fabricated interaction), no em dashes, we-voice,
role-fit framing, no intent inference, candidate-initiated reapplication, no abstractions.
Outputs: output/job42/rejection_emails/<app_id>_<name>.html
"""
import io, os, re

TEMPLATE = open(r"c:\Agent Coco\templates\cv_rejection_template_locked.html", encoding="utf-8").read()
OUT = r"c:\Agent Coco\output\job42\rejection_emails"
os.makedirs(OUT, exist_ok=True)

P = ('<p style="margin:0 0 18px 0;text-align:justify;font-family:Georgia,serif;'
     'font-size:15px;line-height:1.8;">{}</p>')

def paras(*texts):
    return "".join(P.format(t) for t in texts)

EMAILS = [
{
 "app_id": 3986, "first": "Adnan", "name": "Adnan Riaz", "email": "adnanriaz999@gmail.com",
 "subject": "What 300 negotiations told us about your craft",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. Your application was read closely and in full, and because the work you described deserves more than a form letter, we want to give you an honest account of what we appreciated and where the decision came from.",
   "We write to every applicant this way for a simple reason: a decision that affects someone's next months should come with its reasoning attached. What follows is specific to you and to what you actually submitted, and we hope it is useful well beyond this one process."),
 "s1": paras(
   "The first thing that stood out was the sheer negotiating mileage in your record. Three hundred plus roaming and wholesale agreements across one hundred and forty five territories, closed against usage forecasts and volume-tiered proposals rather than charm, with an average twelve percent IOT reduction and 2.1 million dollars in annual savings to show for it. That is deal discipline built the hard way, one counterparty at a time, and it does not happen by accident.",
   "Second, the ownership arc at Jazz reads like real product stewardship, not caretaking. A 1.6 billion rupee ARR portfolio held end to end, from retail and wholesale propositions through pricing frameworks to partner expansion, delivering twenty four percent year-on-year growth over twenty three months. The 99.2 percent launch success rate across four hundred plus operators, with zero SLA breaches, tells us you finish what you open.",
   "Third, the systems instinct. Cutting a sixteen-week launch cycle to four by bringing Agile cadence into a cross-functional machine of technical, finance, commercial, legal and billing teams; building a KPI framework that reduced reliance on external clearing houses and saved forty five thousand dollars a year; forecasting traffic and revenue to eighty five percent accuracy with models built from historical settlement data. You do not just run pipelines, you re-engineer the plumbing they run through.",
   "Even the earlier IBM chapter carries the same signature: one hundred and fifty omnichannel customer journeys designed and deployed for Fortune 500 telecommunications clients, campaign delivery cut from eight days to two through reusable templates and SQL-driven segmentation, twenty plus client workshops run to a 4.7 out of 5 satisfaction score. Wherever the CV is opened, the same professional appears: structured, measured, and accountable to numbers he publishes."),
 "s2": paras(
   "Here is where the decision came from, and we want to be as concrete about this as we were about the strengths. This seat is the execution engine of our growth function inside Pakistan's education ecosystem. Its counterparties are provincial education departments, government officials, development-sector and donor organizations, and school systems; its rhythm involves forty to sixty percent domestic travel to partner sites and field visits that end in classrooms, not clearing houses.",
   "The partnership craft in your application, and it is real craft, was built in a different arena: operator-to-operator wholesale, international counterparties, largely remote or headquarters-based commercial motions. Across six years we could not find in the written application an engagement with a Pakistani government or public-sector institution, a development-sector partner, or a field-based acquisition motion. What left us uncertain was not whether you can negotiate, the record settles that, but whether this specific seat, with its ground game and its government-facing texture, is the arena where your particular machinery has been proven. With one seat to fill, we made the narrow call to go with evidence we could see on that exact terrain."),
 "s3": paras(
   "Two things, offered carefully. First, if the impact sector genuinely pulls you, your wholesale negotiation depth, settlement rigor and forecasting accuracy transfer more directly to institutional and B2G partnership work than most commercial skill sets do; the missing layer is demonstrated time with public-sector counterparties. Even one deliberate engagement in that world, a government digitization project, a donor-funded connectivity program, a telecom-for-education initiative of the kind several operators already run, would change how an application like yours reads to a hiring team in our sector, because it would connect craft we can already verify to terrain we need it proven on.",
   "Second, one small practical note offered in good faith: the expected-salary field in your application form reached us as a figure we could not interpret, so wherever you apply next and forms are read closely, it is worth a re-check before submitting. Our openings live at taleemabad.com; if a role closer to your proven arena opens, we would welcome a fresh application from you."),
 "ps": "The detail we kept returning to was the 99.2 percent launch success rate across four hundred operators. Most careers never produce a numerator that clean at that denominator. Whatever arena you choose next, that finishing instinct will travel with you."
},
{
 "app_id": 4023, "first": "Naeem", "name": "Muhammad Naeem Ayubi", "email": "mrmna4@outlook.com",
 "subject": "Twenty-eight years of institutional selling, read closely",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. An application carrying twenty eight years of work deserves a precise explanation rather than a template, so here is an honest account of what we appreciated and exactly where the decision came from.",
   "We want to say at the outset that nothing in this letter is a verdict on the career it describes. The decision below is about the fit between one specific seat and one specific record, and we have tried to make that distinction visible in every paragraph that follows, because it is the distinction that matters."),
 "s1": paras(
   "You have spent the last eight years doing, at Oxford University Press, something remarkably close to the heart of our work: driving institutional adoption of educational material through schools, colleges and educators, sustained by relationships with academic decision-makers rather than one-off transactions. The OxfordAQA launch from that platform, and the consistent revenue growth held alongside credit control and timely collections, describe a professional who builds education-sector demand patiently and keeps the commercial hygiene intact while doing it.",
   "The Sanofi arc before that speaks for itself: nineteen years, entered as a medical representative and finished directing nationwide sales operations, promoted step by step on performance rather than tenure. Careers with that gradient are built on thousands of unglamorous field days, and we read it that way.",
   "And the training record, from LUMS business-performance workshops to train-the-trainer certification, shows someone who kept sharpening the saw across three decades. The habit of building and retaining teams through coaching, delegation and counselling appears in every chapter of the CV, which tells us it is conviction, not resume language.",
   "We also noted the range: pharmaceutical selling into clinicians and institutions, FMCG national trade at Qarshi with distributor networks and trade promotions, then education publishing into academic decision-makers. Moving a commercial craft across three industries with that little friction is its own credential, and the CRM-driven forecasting discipline named in the OUP chapter shows the toolkit kept pace with the market rather than staying frozen in an earlier era."),
 "s2": paras(
   "Here is the honest center of the decision, and it has nothing to do with the quality of the record. This particular seat is a hands-on execution role. It reports into our Head of Growth as their second, it is scoped for someone roughly four to six years into their career, and its daily reality is carrying a pipeline personally: writing the follow-ups, sitting in the district office waiting room, running the CRM discipline with their own hands rather than reviewing it in a Monday meeting.",
   "Your last fifteen years have been spent directing regional and national salesforces, building multi-tiered teams of sales managers and area managers, and operating at a leadership altitude this seat simply does not offer. The role would use a fraction of the scope you have carried, and what left us uncertain, reading the written application alone, was how a seat deliberately scoped this early in a career arc could be a fair exchange for what you bring. We concluded that placing a national-scale sales leader into a second-chair execution role would serve neither you nor the person this seat is designed to grow. That is a statement about the shape of the seat, not about you."),
 "s3": paras(
   "Our suggestion is direct: aim at the altitude you have earned. Education publishing and the wider edtech sector in Pakistan have commercial leadership seats, regional and national in scope, where an OUP institutional-adoption record combined with pharmaceutical-grade salesforce discipline is a rare and legible asset. An application aimed there does not need to explain itself the way one aimed at a mid-level seat does.",
   "A smaller, practical note on the CV itself: the OUP chapter currently lists responsibilities more than results. The revenue growth is mentioned, but a hiring team reading quickly will want the numbers you certainly have, adoption counts, territory growth percentages, the scale of the OxfordAQA launch, stated as plainly as the Sanofi promotions are. Your record earns those numbers; let the document show them. Our own openings live at taleemabad.com, and roles of different scope do open as we grow; if a seat matched to leadership scale opens, we would welcome a fresh application from you."),
 "ps": "Two details stayed with us: a career that begins with a 1990 degree and still shows a training certificate dated 2017, and a promotion ladder climbed one rung at a time for nineteen years at one company. That is what showing up for three decades actually looks like on paper."
},
{
 "app_id": 4053, "first": "Wasib", "name": "Wasib Javed", "email": "wasibjaved@gmail.com",
 "subject": "Fifty-seven percent of a region's revenue, and an honest constraint",
 "role": "Senior Manager Growth · Taleemabad",
 "opening": paras(
   "We have completed our evaluation of your application for the Senior Manager Growth role, and we will not be moving you forward at this time. We want to be unusually direct with you about why, because in your case the decision has little to do with capability and a great deal to do with two structural facts about this seat, and you deserve to hear both plainly.",
   "We write detailed letters like this to every applicant because we believe a decision should carry its reasoning with it. In your case especially, a one-line regret would have been a disservice to a record that took sixteen years to build, so please read what follows as it is intended: as a straight answer, given with respect."),
 "s1": paras(
   "The record is not in question, so let us name what we saw. Sixteen years at Oxford University Press, rising to Senior Manager and head of department, contributing fifty seven percent of regional revenue while holding twelve percent annual growth, is institutional selling at a scale and consistency few people in this market can document. The portfolio of government, semi-government and private institutional contracts, won through solution demos, proposals and bid coordination, sits squarely in the world we work in.",
   "The award cadence is its own kind of evidence: Employee of the Year twice, Team Lead of the Year, High Achiever in 2016-17 and again in 2023-24. Sustaining recognition across a fifteen-year span at one employer, through changing markets and changing management, is rarer than winning it once.",
   "And the early chapters matter too: managing sales across four hundred and fifty plus private schools in Northern Pakistan, running book fairs and anti-piracy operations, then enterprise relationships at Citibank with accounts like Mobilink, Telenor and Serena. The arc from field-level school selling to department leadership is complete and self-made.",
   "One more thing the CV documents that deserves naming: durability of standards. Weekly reviews and course corrections held for years, collections and dispute resolution kept clean alongside the revenue numbers, compliance treated as part of the job rather than an obstacle to it. Growth figures are common in applications; growth figures sitting next to sixteen years of clean commercial hygiene at one institution are not."),
 "s2": paras(
   "Here are the two facts, stated without decoration. First, compensation: you shared an expectation of one million rupees monthly, and this role carries a band that sits far below that figure. This is not a gap that negotiation closes at the margins; it is structural to how the seat is graded, and we would rather tell you that cleanly than draw you into a process that ends at an offer you could not reasonably accept.",
   "Second, the shape of the seat itself. This is a hands-on second-in-command execution role reporting into our Head of Growth, scoped for someone four to six years into their career who carries their own pipeline daily. You have led a team of thirteen and run a regional P&L as head of department. The seat would ask you to operate well below the scope you have held for years, and nothing in a record like yours suggests that would remain satisfying past the first quarter. Both constraints are about the seat we happen to have open right now, not about the professional described in the application, and we would not want a process to obscure that distinction for you."),
 "s3": paras(
   "Hold your expectation; the record supports it. The seats that fit what you documented are senior institutional-sales and commercial leadership roles, in education publishing, edtech, and enterprise sales into government, where a department-head scope and a bid-coordination track record are the entry requirements rather than an overshoot. We would also say: keep the awards and the fifty seven percent figure at the top of the CV, because they compress sixteen years into two lines that any hiring team can verify and none can ignore.",
   "And because sixteen years at one institution can read two ways, let the CV preempt the question: a line or two on what changed under your leadership, the systems you introduced, the accounts that exist because of you, turns tenure from a duration into a body of work. The evidence is clearly there; the document just needs to argue it. Our openings live at taleemabad.com; roles of larger scope do open as the organization grows, and if a seat matched to your level opens, we would welcome a fresh application from you."),
 "ps": "High Achiever in 2016-17 and again in 2023-24, seven years apart at the same institution. Consistency over that distance is the hardest thing to fake in a career, and yours is documented."
},
]

built = []
for e in EMAILS:
    html = TEMPLATE
    html = html.split("<!DOCTYPE")[1]
    html = "<!DOCTYPE" + html  # drop the top comment block
    html = html.split("<!--\nCV REJECTION RULES")[0]  # drop trailing rules comment
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
    built.append((e["app_id"], e["name"], path, words))
    print(f"built {e['app_id']} {e['name']}: ~{words} words -> {path}")
