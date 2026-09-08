"""
Case Study Outcome, Below the Benchmark. Skill 01 type #8. PILOT to Ayesha.

Job 42, Senior Manager Growth. The five candidates who submitted the Execution Sprint case
study and scored below the 70% benchmark that gates final interviews.

Evidence for every claim comes from exactly two places, per the type doc:
  1. the candidate's own submission, quoted through the evaluation record that read it
  2. docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md, written and QA'd
     BEFORE any submission was opened

The 70% rule is stated. No individual score, band or ranking appears in any letter.
No letter references a conversation: all five had a Zero In Call booked, but a booking is
not a held interview, and these letters do not need one.

GATE: _gate() runs before any SMTP connection and raises SystemExit on a hard block. This is
deliberate. The Layer 3 PreToolUse send hook is inert (it matches tool_name against "send"
but is registered on the "Bash" matcher, so it never fires). Do not rely on it.

Usage:
    python scripts/send_case_study_outcome_pilot.py            # pilot to Ayesha, all five
    python scripts/send_case_study_outcome_pilot.py --only kanooz
    python scripts/send_case_study_outcome_pilot.py --check    # gate only, send nothing
    python scripts/send_case_study_outcome_pilot.py --live     # requires Ayesha's approval
"""

import argparse
import os
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils.feedback_widget import feedback_widget  # noqa: E402
from scripts.utils.safe_send import (allow_candidate_addresses,  # noqa: E402
                                     safe_sendmail)
from scripts.utils.v8_template import (EYEBROW, FOOTER, H, P, PS, attach_logo,  # noqa: E402
                                       wrap)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))

ROLE = "Senior Manager Growth"
SUBJECT_CORE = "An Update on Your Case Study for Senior Manager Growth"
PILOT_TO = "ayesha.khan@taleemabad.com"

# LIVE CC, given by Ayesha 2026-09-08. Same list as the Case Study Update type (#6).
LIVE_CC = [
    "waqas.tanveer@taleemabad.com",
    "ali.sipra@taleemabad.com",
    "hiring@taleemabad.com",
    "ayesha.khan@taleemabad.com",
]

BENCHMARK_SOURCE = os.path.join(
    ROOT, "docs", "case_studies", "benchmarks", "smg_execution_sprint_benchmark.md")

# Text extracted from each candidate's ACTUAL submitted files, pulled from their Drive
# folder by scripts/evals/fetch_submission_corpora.py. The gate checks every quoted phrase
# in a letter against this, so a quote cannot drift from what the candidate actually wrote.
CORPUS_DIR = os.path.join(ROOT, "output", "smg_submission_corpora")

# Full Job 42 case-study roster, both batches. Used to block cross-contamination: no
# candidate's letter may name any other candidate. Ambiguous name parts ("Ali", "Khan",
# "Siddiqui") are deliberately excluded from the scan to avoid false positives.
ROSTER_NAMES = [
    "Shahmir", "Arshan", "Yusra", "Umar Zahid", "Junaid", "Arooj", "Khushal", "Furqan",
    "Hania", "Vaneeza", "Shafaq", "Lamis", "Kanooz", "Rimsha", "Basit", "Irfan", "Wajdan",
    "Ahmad Taj",
]

# ── HARD-BLOCK PATTERNS ────────────────────────────────────────────────────────
INTENT_WORDS = [
    r"you assumed", r"you believed", r"you thought", r"you preferred",
    r"you were energized by", r"you were energised by", r"you seemed", r"you appeared",
    r"you lacked", r"you were hesitant", r"you would likely", r"you were not fully invested",
    r"you didn'?t seem", r"you weren'?t", r"you wouldn'?t", r"you felt", r"you wanted to",
    r"you did not care", r"you were unwilling",
]
FIRST_PERSON = r"\b(I|I'm|I've|I'll|I'd|my|me|mine|myself)\b"
CONVERSATION_WORDS = [
    r"\bwe spoke\b", r"\bwe met\b", r"our conversation", r"our discussion", r"our call\b",
    r"our meeting", r"our time together", r"when we talked", r"\byour interview\b",
    r"in the interview", r"during the call",
]
FUTURE_PROMISE = [
    r"we will reach out", r"we'll reach out", r"we will be in touch", r"we'll be in touch",
    r"we will contact you", r"we'll contact you", r"keep your name on file",
    r"keep your name with us", r"expect to hear from us", r"you'll hear from us",
    r"we will let you know", r"we'll let you know",
]
JARGON = [r"culture fit", r"cultural fit", r"not quite the right fit", r"growth opportunity",
          r"\bKCD\b", r"\bGWC\b", r"scorecard", r"values interview"]
COMPARISONS = [r"other candidates", r"the pool\b", r"of the fifteen", r"the strongest submission",
               r"the weakest", r"ranked", r"compared to others", r"than others"]
# Adversarial, judgmental or corporate register. Ayesha 2026-09-08: the letter must read as
# feedback offered to be useful, never as us arguing our case against the candidate. Warmth
# comes from respect and constructive language, not from withholding the actual feedback.
HARSH_LANGUAGE = [
    r"\bfailure\b", r"\bwrong\b", r"the honest part", r"you failed", r"you did wrong",
    r"the problem with your", r"went wrong", r"\bblame\b", r"\bsloppy\b", r"\bcareless\b",
    r"you cannot\b", r"you are unable", r"\bincapable\b", r"\bdeliberately\b",
    r"reverse.?engineer", r"until the arithmetic", r"chose assumptions", r"selecting assumptions",
]
# Corporate rejection boilerplate. Banned outright: it is the opposite of a human letter.
CORPORATE_BOILERPLATE = [
    r"we regret to inform", r"after careful consideration", r"impressive (candidate )?pool",
    r"strong field of candidates", r"we wish you (all the best|the best) in your future",
    r"unfortunately, (you|your application) (were|was) not",
]
INTERVIEWER_NAMES = [r"\bJawwad\b", r"\bJawad\b", r"\bAyesha\b", r"\bWaqas\b", r"\bAli Sipra\b",
                     r"\bZeshan\b", r"\bNoah\b"]


def strip_tags(html: str) -> str:
    """Rendered text, entities resolved, for the gate's pattern scans."""
    import html as _h
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.I)
    txt = re.sub(r"</p>|</h2>|</li>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = _h.unescape(txt)
    return re.sub(r"[ \t]+", " ", txt)


def _quotes_are_verbatim(c: dict, text: str) -> list:
    """
    Every phrase in quotation marks must appear verbatim in that candidate's own submission.

    Added 2026-09-08. An audit of the letters against the real submitted files found four
    quotes that had drifted: a silently corrected typo, an em dash normalised to a comma, our
    own gloss sitting inside quotation marks, and a reordered sentence. Nothing was fabricated,
    but nothing inside quotation marks may be approximate either.
    """
    path = os.path.join(CORPUS_DIR, "CORPUS_%s.txt" % c["corpus"])
    if not os.path.exists(path):
        return ["submission corpus missing, cannot verify quotes: %s" % path]

    def norm(x):
        for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'),
                     ("\u2013", "-"), ("\u2014", "-"), ("\xa0", " ")):
            x = x.replace(a, b)
        return re.sub(r"\s+", " ", x).lower()

    corpus = norm(open(path, encoding="utf-8", errors="replace").read())
    bad = []
    for q in re.findall(r'"([^"]{8,400})"', text):
        if norm(q).strip(" .,;:") not in corpus:
            bad.append('quoted phrase is not verbatim in their submission: "%s"' % q[:90])
    return bad


def _gate(c: dict, body_html: str, subject: str, live: bool) -> list:
    """Hard blocks. Returns warnings; raises SystemExit on any block."""
    text = strip_tags(body_html)
    blocks, warns = [], []

    # 1. sources must exist on disk
    if not os.path.exists(BENCHMARK_SOURCE):
        blocks.append(f"BENCHMARK_SOURCE missing: {BENCHMARK_SOURCE}")
    if not os.path.exists(c["submission_source"]):
        blocks.append(f"SUBMISSION_SOURCE missing: {c['submission_source']}")

    # 2. word count
    words = len([w for w in re.split(r"\s+", text.strip()) if w])
    if words < 800:
        blocks.append(f"word count {words} is under the 800 minimum")

    # 3. Rule 10 opening line, first line after the salutation
    m = re.search(r"Dear\s+[^,\n]+,\s*(.*)", text)
    if not m:
        blocks.append("no salutation found")
    elif not m.group(1).lstrip().startswith("This is not a yes for now."):
        blocks.append('"This is not a yes for now." is not the first line after the salutation')

    # 4. the 70% rule must be stated
    if "70%" not in text:
        blocks.append("the 70% benchmark rule is not stated")

    # 5. no individual score, band or ranking
    if re.search(r"\b\d{1,3}\s*(?:/|out of)\s*100\b", text):
        blocks.append("an out-of-100 score appears in the body")
    if re.search(r"you scored|your score|your total", text, re.I):
        blocks.append("the candidate's own score is referenced")
    for pat in (r"\bstrong yes\b", r"\bborderline\b", r"\bno hire\b"):
        if re.search(pat, text, re.I):
            blocks.append(f"internal band label in body: {pat}")

    # 5b. every quoted phrase must be verbatim in the candidate's own submission
    blocks.extend(_quotes_are_verbatim(c, text))

    # 6. at least three verbatim anchors from this candidate's own submission
    missing = [a for a in c["anchors"] if a not in text]
    if len(c["anchors"]) < 3:
        blocks.append(f"only {len(c['anchors'])} anchors declared, 3 required")
    if missing:
        blocks.append(f"anchors declared but absent from body: {missing}")

    # 7. no other candidate named
    for nm in ROSTER_NAMES:
        if nm.lower() in c["full"].lower() or nm.lower() in c["first"].lower():
            continue
        if re.search(rf"\b{re.escape(nm)}\b", text):
            blocks.append(f"another candidate is named in this letter: {nm}")

    # 8. em dashes
    if "—" in text or "&mdash;" in body_html:
        blocks.append("em dash present")

    # 9. collective voice
    fp = re.findall(FIRST_PERSON, text)
    if fp:
        blocks.append(f"first-person singular: {sorted(set(fp))}")

    # 10. no intent inference
    for pat in INTENT_WORDS:
        if re.search(pat, text, re.I):
            blocks.append(f"intent-word: {pat}")

    # 11. no fabricated interaction
    if not c.get("interview_reference_allowed", False):
        for pat in CONVERSATION_WORDS:
            if re.search(pat, text, re.I):
                blocks.append(f"conversation reference with no verified interview: {pat}")

    # 12. no interviewer names, no jargon, no pool comparisons
    for pat in INTERVIEWER_NAMES:
        if re.search(pat, text):
            blocks.append(f"interviewer or staff name: {pat}")
    for pat in JARGON:
        if re.search(pat, text, re.I):
            blocks.append(f"internal jargon: {pat}")
    for pat in COMPARISONS:
        if re.search(pat, text, re.I):
            blocks.append(f"candidate comparison: {pat}")

    # 12b. tone: adversarial/judgmental register and corporate boilerplate (Ayesha 2026-09-08)
    for pat in HARSH_LANGUAGE:
        if re.search(pat, text, re.I):
            blocks.append(f"harsh or adversarial language: {pat}")
    for pat in CORPORATE_BOILERPLATE:
        if re.search(pat, text, re.I):
            blocks.append(f"corporate rejection boilerplate: {pat}")

    # 13. pilot prefix discipline
    if live and "[PILOT" in subject:
        blocks.append("live send carries a [PILOT] subject prefix")
    if not live and "[PILOT" not in subject:
        blocks.append("pilot send is missing its [PILOT] subject prefix")

    # warnings
    for pat in FUTURE_PROMISE:
        if re.search(pat, text, re.I):
            warns.append(f"future-outreach promise: {pat}")
    if re.search(r"you failed|you were missing|you did not have", text, re.I):
        warns.append("personal-shortcoming framing, prefer role-fit")

    print(f"  gate: {words} words, {len(c['anchors'])} anchors verified")
    if warns:
        for w in warns:
            print(f"  WARNING  {w}")
    if blocks:
        print(f"\n  HARD BLOCK, {c['full']}:")
        for b in blocks:
            print(f"    - {b}")
        raise SystemExit(f"BLOCKED: {c['full']} ({len(blocks)} violations)")
    return warns


# ══════════════════════════════════════════════════════════════════════════════
# THE FIVE LETTERS
# ══════════════════════════════════════════════════════════════════════════════

OPENING = (
    "Thank you for the work you put into the Execution Sprint case study for {role}. "
    "Every deliverable you submitted was read in full and scored against a benchmark answer "
    "that was written and reviewed before any submission was opened, so that everyone was "
    "measured against the same standard rather than against each other. Candidates who "
    "meet the bar move to the final interviews. Your submission did not meet the 70% "
    "benchmark on this occasion, and so we won&#39;t be moving forward with your "
    "application for this role. You gave this real hours, so the least we owe you is the "
    "specifics rather than a form letter."
)

CLOSE_COMMON = (
    "We are not going to dress this up as an encouragement to try again somewhere in the "
    "abstract. What we can tell you honestly is that this decision is about one submission "
    "measured against one standard, on one week, for one role. It is not a verdict on how "
    "far you can go in growth work. If a role opens here where {closing_fit}, we would be "
    "glad to hear from you."
)


def letter_irfan():
    return (
        P("Dear Irfan,") +
        P("<strong>This is not a yes for now.</strong>") +
        P(OPENING.format(role=ROLE)) +

        H("What Your Work Showed Us") +
        P("One piece of your Assignment 1 was genuinely original. You broke the Pakistan "
          "registration funnel down by state and surfaced <strong>23 users whose WhatsApp "
          "template never delivered</strong> and <strong>52 who opened the registration flow "
          "and then abandoned it</strong>. That is seventy five addressable people sitting "
          "inside a dataset that most readings treat as one undifferentiated pool. When both "
          "figures were recomputed from the raw 546 rows, they were exact. Nothing in the "
          "brief asked for that cut. You went and found it, and it is the kind of question "
          "that separates someone who reads a dashboard from someone who interrogates one.") +
        P("Your kill criteria were the second thing worth saying out loud. Most plans state a "
          "threshold and leave it sitting in the document as decoration. Yours were written "
          "as compound falsifiable conditions, which means they could actually fire and stop "
          "work. The benchmark specifically looks for that discipline, because a growth plan "
          "with no way to be disproved is a wish list. You wrote yours so they could be "
          "disproved, "
          "and that is not a small thing to get right under time pressure.") +

        H("Where the Submission Could Have Been Stronger") +
        P("The main gap we identified sits in the email to the district education officer. "
          "It presents figures drawn from the platform wide dataset as results from "
          "the forty school pilot. The 275 lesson plans, 105 presentations and 88 coaching "
          "sessions are totals from a different scenario. The line that carried the most "
          "weight for us was <strong>\"Of the students formally assessed, 59% are now "
          "reading at or above grade level\"</strong>. In the data, 59% is the reading "
          "assessment completion rate, 51 of 87 attempts. It is not a measure of how many children can read.") +
        P("You did label these as placeholder assumptions, and we want to be fair about that: "
          "under our rubric this is not fabricated data, and we did not treat it as such. But "
          "the same figures reappear without that label in the internal update, and this role "
          "would put you in front of government counterparts on our behalf. A number that "
          "cannot be traced back to its source does not cost us a meeting when it is caught. "
          "It costs us the relationship when it is not. That is why this weighed heavily "
          "instead of being noted and set aside.") +
        P("The second gap is the choice at the centre of Assignment 1. The submission selects "
          "lesson plans and presentation generation as the leverage areas, on the evidence "
          "that they carry the most users. The benchmark treats exactly that reasoning as the "
          "case's central trap. Those two features are convenience utilities: 275 and 105 "
          "sessions is real volume, and nothing in the data links either to a return visit. "
          "The feature actually holding the platform's retention is coaching, with 35 "
          "adopters and a 75% completion rate. Your own slide 1 says the focus should be "
          "coaching and reading. Slide 3 then selects lesson plans instead. Reading the "
          "submission as a whole, we could not tell which of the two positions you were "
          "putting forward, and on a document whose job is to point a team at one thing, that "
          "ambiguity mattered.") +
        P("Two smaller things, worth knowing because they are cheap to fix. Slides 4 and 5 "
          "were headings with nothing underneath them. The experiments did exist in your "
          "workbook, so the thinking was there, but the deck a reader opens first did not "
          "carry it. And Assignment 3 carried no probability on the deal at all, which was "
          "one of the few numbers the brief asked for directly.") +

        H("Where We Want to Leave This") +
        P("The instinct that produced the state level funnel breakdown is the hardest part of "
          "this work to teach. Most people can be taught to build a plan. Far fewer will "
          "voluntarily go and disaggregate a funnel until it gives up seventy five specific "
          "people nobody knew were stuck. If there is one thing to carry forward from this, "
          "it is to point that same suspicion at your own conclusions: the numbers you send "
          "outward deserve the interrogation you gave the ones you pulled inward.") +
        P(CLOSE_COMMON.format(
            closing_fit="that kind of digging is the centre of the job rather than a part of it")) +

        PS("<strong>P.S.</strong> The 23 undelivered templates and the 52 abandoned flows were "
           "nobody's assignment. You found them because you went looking. Keep doing that.")
    )


def letter_basit():
    return (
        P("Dear Basit,") +
        P("<strong>This is not a yes for now.</strong>") +
        P(OPENING.format(role=ROLE)) +

        H("What Your Work Showed Us") +
        P("Your arithmetic was clean and correctly sourced throughout, which is less common "
          "than it should be on an exercise like this. The user counts, the "
          "<strong>43.8% against 45.6%</strong> registration comparison between the two "
          "markets, and the <strong>34 coaching users in Pakistan against zero in Sri "
          "Lanka</strong> all reconciled against the raw data when we checked them. Nothing "
          "was inflated and nothing was quietly rounded in a helpful direction.") +
        P("You also got the central read right. You identified that coaching and reading users "
          "are four to five times more engaged than everyone else on every retention measure "
          "available, and your executive recommendation followed from it: deepen engagement "
          "with the users who already reached the core product rather than spend to acquire "
          "more reach. That is the correct high level call on this dataset, and a good number "
          "of ways of reading these numbers lead somewhere worse. Your headline judgment was "
          "sound.") +

        H("Where the Submission Could Have Been Stronger") +
        P("The gap is between that judgment and a plan someone could execute on Monday. "
          "Assignment 2 restates the strategy rather than operationalising it. "
          "<strong>\"Conduct teacher orientation sessions\"</strong>, "
          "<strong>\"send automated reminders\"</strong> and "
          "<strong>\"present coaching outcomes\"</strong> would sit comfortably in a plan for "
          "any company selling anything to anyone. The owners are department names rather "
          "than a person doing a named thing on a named day, and no phase carries an exit "
          "criterion, so nothing in the document says when a phase is finished or when it has "
          "failed. The tracker that was meant to carry the operating detail is two example "
          "rows and a dropdown list.") +
        P("We want to be direct about why this specific dimension counted for so much. The "
          "role description leads with hands on execution and forty to sixty percent travel, "
          "because this is a job that lives in the field rather than in the plan. Execution "
          "carries the heaviest weight in our scoring for that reason. On the dimension that "
          "matters most for this particular seat, the submission was at its thinnest.") +
        P("The commercial judgment in Assignment 3 is the other place the submission struggled. "
          "You put <strong>65%</strong> on closing the district deal. The scenario in front of "
          "you had six weeks of silence from the sponsor, nothing in writing, no verified "
          "procurement stage, five weeks left to the budget close and an active competitor. "
          "There is a defensible case for a low number with named events that would move it in "
          "either direction. What is hard to defend is a number above even odds attached to no "
          "gating events at all, because a forecast that cannot move is not a forecast. The "
          "benchmark answer sits at 35% with the events named on both sides.") +
        P("One last item, raised plainly because it is the sort of thing that matters more later "
          "than it does now. Your second deck was described in your own submission note as made "
          "through NotebookLM, and it arrived as eight slides of images with no extractable "
          "text, alongside no disclosure of what was AI assisted and what was yours. We have no "
          "issue with using these tools. We ask candidates to say where they were used, per "
          "deliverable, and that disclosure was missing.") +

        H("Where We Want to Leave This") +
        P("The distance you have to travel here is a shorter one than it might feel reading the "
          "above. You already reason correctly about what the data means, which is the part "
          "that is the harder half to get right. What was missing is the translation layer: a "
          "named "
          "person, a specific action, a date, and a number that says stop. If you sit down with "
          "your own Assignment 2 and rewrite one phase of it so that a growth associate could "
          "be handed it on a Monday morning and know exactly what to do by Wednesday, you will "
          "have closed most of the gap this exercise found.") +
        P(CLOSE_COMMON.format(
            closing_fit="the weight sits on analysis and recommendation rather than on running "
                        "the plan yourself")) +

        PS("<strong>P.S.</strong> Deepen engagement rather than expand reach was the right call "
           "on this data, and you reached it from your own numbers. That judgment is worth "
           "keeping hold of.")
    )


def letter_kanooz():
    return (
        P("Dear Kanooz,") +
        P("<strong>This is not a yes for now.</strong>") +
        P(OPENING.format(role=ROLE)) +

        H("What Your Work Showed Us") +
        P("Your submission contained the clearest statement of the Sri Lanka problem we read. "
          "Your deck puts it flatly, recording <strong>\"nearly identical sign-up and "
          "registration-completion rates\"</strong> and then that <strong>\"Sri Lanka has "
          "never converted a single registrant into a coaching or reading user\"</strong>. "
          "Pakistan coaching completion "
          "at <strong>75.65%</strong> against Sri Lanka at <strong>0.00%</strong>, both exact. "
          "That is the single most important fact in the dataset, and stating it that plainly "
          "is harder than it looks, because every top of funnel metric available invites the "
          "opposite conclusion.") +
        P("Your original contribution was grade breadth, and it is a genuine one. Instead of "
          "asking which grade a teacher teaches, you asked how many. Pakistani registered "
          "teachers who select multiple grades adopt coaching at <strong>44.2%</strong> "
          "against <strong>19.2%</strong> for single grade teachers, and inside the single "
          "grade group the spread runs from Secondary at 50% down to Early Years at zero. You "
          "also noticed that reading skews the opposite way from coaching, toward the younger "
          "grades. That is an actionable targeting rule, and it is not in our benchmark answer. "
          "You found something the standard itself did not have.") +
        P("Two more things. Your kill criteria were anchored to measured baselines rather than "
          "to round numbers, so a threshold that effectively says no better than doing "
          "nothing is doing real work. And in Assignment 2, at the moment the administrator notices a "
          "win, your instruction to the growth team was <strong>\"do not approach the "
          "administrator first\"</strong>. The brief asked candidates to run the loop as "
          "designed rather than quietly replace it with direct selling. That line is the "
          "sound of someone actually doing so.") +

        H("Where the Submission Could Have Been Stronger") +
        P("The email to the district education officer is the deliverable that decided this, "
          "and the reason is a single omission. It is warm, it is courteous, it is correctly "
          "short, and attaching a pilot results report so the officer has something to "
          "circulate internally is a good move. <strong>But it never mentions the budget "
          "deadline.</strong> The entire scenario turns on five weeks to a cycle close, after "
          "which the expansion waits a year. The ask reads "
          "<strong>\"We would welcome the opportunity to meet with you at a time convenient "
          "for you\"</strong>: undated, open ended, and requesting a meeting rather than a "
          "named person or a specific next action. Nothing in it gives a busy official who has "
          "already let six weeks pass a reason to reply this week rather than next month. In a "
          "role where a large part of the job is moving government counterparts inside their "
          "own calendars, that omission is close to the centre of the work.") +
        P("The second gap is a mismatch between what Assignment 1 asked and what it received. "
          "You proposed three experiments and all three are well built. But all three are "
          "targeting and messaging tests, and the assignment asked about product to channel "
          "and channel to model fit. The distinction matters because the dataset carries no "
          "channel attribution at all, and noticing that the question is currently "
          "unanswerable is part of what the exercise was testing.") +
        P("Assignment 2 thins out after its strong opening. There is no tracker file, no "
          "numeric exit criterion for any phase, and the weekly metrics are a list of field "
          "names rather than an operating cadence. Your definition of the loop coefficient is "
          "careful, including the clause that only teacher sharing and referral acquisitions "
          "count, which is the clause most submissions leave out. What is missing is any "
          "working of the number, any decomposition into the drivers underneath it, and any "
          "instrument that would collect it. Assignment 3 has the same shape: the five week "
          "ordering is right and running procurement in parallel rather than afterwards is "
          "correct, but nothing in it states what result would make you stop, downgrade or "
          "change route.") +

        H("Where We Want to Leave This") +
        P("This was a close decision and it would be dishonest to imply otherwise. The "
          "analytical work is strong, the grade breadth finding is yours, and the discipline in "
          "your kill criteria is real. What separated this submission from the ones that "
          "cleared the bar was not insight. It was the last mile: turning a correct read into a "
          "dated, gated, named plan, and into an email that makes a specific person do a "
          "specific thing by a specific day.") +
        P(CLOSE_COMMON.format(
            closing_fit="the analytical half of this work is the larger half")) +

        PS("<strong>P.S.</strong> Asking how many grades a teacher spans, rather than which "
           "one, is a question our own answer key did not think to ask. That instinct is the "
           "most valuable thing in your submission.")
    )


def letter_wajdan():
    return (
        P("Dear Ali,") +
        P("<strong>This is not a yes for now.</strong>") +
        P(OPENING.format(role=ROLE)) +

        H("What Your Work Showed Us") +
        P("Your arithmetic was exact to the row. The feature table reconciles precisely against "
          "the raw data: lesson plans at <strong>170 users and 275 uses</strong>, presentations "
          "at 91 and 105, general chat at 433 and 949. So does the registration state table, "
          "with <strong>flow_sent at 180</strong> and template_send_failed at 26. You then "
          "sized the stuck onboarding pool correctly at <strong>206</strong> and called it a "
          "low hanging fruit that should be addressed at priority, which is right, and which is "
          "a lever a real team could pull next week.") +
        P("You also identified coaching as the retention engine, and the instinct underneath "
          "that pick was a good one: that coaching creates a feedback loop which improves "
          "teaching over time, so teachers keep coming back. One of your product ideas, letting "
          "a raw voice note over twenty seconds route straight into coaching without multi step "
          "commands, is the kind of friction removal that comes from actually picturing a "
          "teacher holding a phone at the end of a school day.") +
        P("Your reflective response was the strongest thing you submitted. The account of "
          "pushing lines per bill through cash incentives, then discovering on a market visit "
          "that reps were adding <strong>matches and sachets</strong> to hit the target and "
          "unlock the bonus, is a precise diagnosis of a gamed metric. What made it good was "
          "the fix: capping credit for low value items and clubbing both metrics so the "
          "incentive only unlocks on both. That is a structural answer where most people reach "
          "for a motivational one.") +

        H("Where the Submission Could Have Been Stronger") +
        P("The submission reads coaching two different ways and never reconciles them. Your "
          "feature table measures it through the audio coaching field, which sums to one across "
          "all 546 users, and your conclusion follows from that table: "
          "<strong>\"the features with the strongest engagement appear to be General Chat &amp; "
          "Lesson Plans\"</strong>. Two paragraphs later, coaching is your top priority, on "
          "completely different figures of roughly 75% completion and 57% repeat usage, both of "
          "which are correct and both of which come from a different pair of fields. Each half "
          "is defensible on its own. Together they mean the noise section contradicts the "
          "priority section, and a reader cannot tell which one you are asking them to act on.") +
        P("Sri Lanka is never examined. It appears in your submission among the countries with "
          "the strongest sign up completion, which is true and is a positive framing, and "
          "nowhere does the submission record that its 261 users have produced zero coaching "
          "adopters and zero reading adopters. That is the largest single fact in the data and "
          "the one the case is built around.") +
        P("Assignment 2 is four prose steps with no dates, no phasing, no owners and no exit "
          "metrics, and the tracker the brief asked for was not submitted, along with any "
          "supporting workbook. The content inside those steps is not unreasonable, and "
          "targeting administrators at schools with multiple active teachers is a sensible "
          "rule. But there is nothing here that could be handed to a growth associate. For a "
          "role that leads with hands on execution, that is the dimension we weight most "
          "heavily. Relatedly, most of your kill criteria have no number in them: "
          "<strong>\"Registration rate falls below the existing threshold\"</strong> cannot "
          "fire, because no threshold is stated.") +
        P("Two things in Assignment 3 need saying plainly. The email to the district officer "
          "contains an unfilled placeholder, <strong>\"over xxx lesson planning and coaching "
          "sessions\"</strong>, and a claim of visible improvements in student literacy metrics "
          "that the supplied data does not support: there are reading assessments in it, but no "
          "measured improvement. Neither should reach a government counterpart. The rest of "
          "that email is well judged, and had those two lines been handled differently it would "
          "have been solid. Separately, your week three heading reads "
          "<strong>\"External Multi-Stakeholder Pressure\"</strong> and weeks four and five "
          "propose daily on ground presence at the district and procurement offices. Against a "
          "sponsor who has already gone quiet for six weeks, daily physical presence is at "
          "least as likely to harden the silence as to break it.") +

        H("Where We Want to Leave This") +
        P("The most useful thing we can tell you is that your reflection was better than your "
          "analysis, and that is unusual and worth thinking about. The market visit story shows "
          "someone who checks a number against the reality it claims to describe. That is "
          "exactly the habit the coaching contradiction and the unfilled placeholder needed. "
          "The instinct is clearly there. This submission did not turn it on itself.") +
        P(CLOSE_COMMON.format(
            closing_fit="product and onboarding judgment carries more of the weight than the "
                        "field plan does")) +

        PS("<strong>P.S.</strong> Capping the credit and clubbing the two metrics together was "
           "the right answer to a gamed incentive, and you got there from a market visit rather "
           "than a spreadsheet. That is a good way to work.")
    )


def letter_rimsha():
    """Tone revised per Ayesha 2026-09-08: developmental, not corrective. Substance unchanged."""
    return (
        P("Dear Rimsha,") +
        P("<strong>This is not a yes for now.</strong>") +
        P("Before anything else, thank you. The Execution Sprint case study is a substantial "
          "piece of work, and you gave it real hours across a written submission and a workbook "
          "with live formulas sitting behind it. That effort was seen. Your submission was read "
          "in full, every deliverable, rather than skimmed for a verdict.") +
        P("It seems fairest to be transparent about how the assessment worked. Every submission "
          "was scored against a benchmark answer that was written and reviewed before any "
          "candidate&#39;s work was opened, so submissions were measured against that fixed "
          "standard and never against each other. Candidates who meet the bar move to the "
          "final interviews. Your submission did not meet the 70% benchmark on this occasion, "
          "and so we won&#39;t be moving forward with your application for this role. We "
          "would rather say that plainly than leave you reading between lines.") +
        H("What Your Work Showed Us") +
        P("Your Assignment 2 was the strongest part of the submission, and it was genuinely "
          "detailed. The phased table carrying Description, Responsible, Action, Channel, "
          "Frequency and Targeted Result columns pushed you to be specific in a way that plans "
          "at this stage often are not, and the responsibility split was named at the level it "
          "actually needs to be, with <strong>scoping by the Senior Manager Growth, "
          "endorsement by the Growth Lead and execution by Growth Associates</strong>. Your "
          "daily tracker ran "
          "to twenty nine columns, covering the chain from coaching status through report "
          "generation and admin sharing to school conversion, with live formulas behind it "
          "rather than headings over empty cells. That is real operational thinking, and "
          "building an instrument that would actually collect what the plan claims to measure "
          "is a step many plans skip entirely.") +
        P("Your country level arithmetic was exact. Pakistan at <strong>3.16 sessions and 2.26 "
          "active days</strong> against Sri Lanka&#39;s 1.71 and 1.36 all reconcile against the "
          "raw data. So does your school affiliation cut, and that one is more than exact, it is "
          "sound: teachers with a school affiliation genuinely are the better segment on this "
          "data, at 3.04 sessions and 2.20 active days against 2.00 and 1.52, and you found that "
          "yourself. Your three experiments each carry a hypothesis, a first week action, a "
          "numeric success metric and a numeric kill criterion, which is structurally complete "
          "and is a discipline the benchmark specifically looks for. You also flagged your own "
          "weakest assumption in writing, noting that the <strong>calculations assume that there "
          "is no drop out</strong>. Marking the limits of your own numbers, unprompted, is a "
          "habit good analysts have, and it counted in your favour.") +

        H("Two Areas That Shaped the Outcome") +
        P("There were two areas in the analysis that ultimately affected the overall score, and "
          "we want to walk you through them, because we think the context will be more useful "
          "than simply sharing the result.") +
        P("<strong>The first is which coaching field the analysis was built on.</strong> The "
          "dataset carries two, and they describe very different things. One, "
          "<strong>audio_coaching_sessions</strong>, sums to <strong>1</strong> across all 546 "
          "users. The other, coaching_started, sums to 118 across 35 adopters with 88 "
          "completions. The analysis appears to have been built using the first field. Read on "
          "its own, that field leads "
          "exactly where your submission goes, and the arithmetic on top of it is careful and "
          "internally consistent throughout. The effect, though, is that the feature the case "
          "positions as its core value proposition, and the one carrying nearly all of the "
          "platform&#39;s repeat usage, comes out recommended for deprioritisation. Because that "
          "reading sat at the top of the analysis, the priorities underneath it pointed away "
          "from where the retention actually was. With two nearly identically named columns "
          "sitting in the same file, this is an understandable thing to get caught by. It is "
          "worth separating that from the quality of the reasoning built on top of it, which "
          "held together.") +
        P("<strong>The second is how two of the headline figures were derived.</strong> Both "
          "priorities rest on the finding that <strong>presentation users average 11.1 active "
          "days</strong> against 4.47 for lesson plan users. Tracing that number back through "
          "the workbook, it divides the total active days of every Pakistani user by the count "
          "of presentation sessions, so the numerator and the denominator are describing "
          "different populations. On the same data, the comparable figures come out at 3.02 and "
          "2.58. The effect here is subtle and worth understanding: presentations are the least "
          "used feature on the platform, so the smallest denominator produces the largest "
          "result, and the measure ends up ordering the features in reverse of how much they "
          "are actually used. The registration and week one comparison has a similar shape, "
          "where the field reads true for 541 of 546 users and therefore cannot separate the two "
          "markets.") +
        P("The loop coefficient belongs in the same area. The chain runs 200 teachers, 70% "
          "activating, 50% referring, two links each, 40% clicking and 50% converting, arriving "
          "at 0.2. Each of those rates is a reasonable sounding planning assumption. What is "
          "missing is a link back to the dataset: none of them is derived from it, and the base "
          "the platform actually has is 35 adopters rather than 200 teachers. The consequence is "
          "that the 0.2 could not be validated against anything in the data, so it is difficult "
          "to plan against or to defend in a review, however sensible each individual step "
          "looks. The eight weekly cohorts of twenty five teachers in Assignment 2 sit in the "
          "same position. Anchoring the first number in a chain like that to the base that "
          "exists, and then showing the arithmetic forward from it, would have made both "
          "considerably stronger.") +

        H("What We Would Encourage You to Look at Differently") +
        P("If there is one thread running through both areas, it is the short step between "
          "having a figure and building on it. Everything around that step is already in place "
          "in your work. You compute carefully, you show your working, you keep your formulas "
          "live so a reader can trace them, and you write down your own assumptions without "
          "being asked to. What we would add is a pause before a number becomes a foundation, "
          "and three questions to fill it: which population sits on each side of this ratio, can "
          "this field discriminate at all, and where does this rate come from. They take seconds "
          "to ask, and they would have caught both of the areas above, because the structure "
          "they need was already there in what you built.") +

        H("Where We Want to Leave This") +
        P("We want to be careful about what this decision does and does not mean. It is one case "
          "study, assessed against one benchmark answer, for one role, in one week. It is not a "
          "read on what you are capable of, and it is not a statement about your analytical "
          "ability. Your arithmetic was checkable, your segment finding was sound, and the parts of "
          "the analysis built on solid ground held up.") +
        P("What your submission demonstrated clearly is real strength in operational planning "
          "and process design. Phasing work properly. Naming who is accountable at each step "
          "rather than leaving it to a department. Building the instrument that would collect "
          "the evidence. Thinking in structures rather than in intentions. Being open about the "
          "limits of your own numbers. Those are genuine capabilities, they are harder to teach "
          "than people assume, and they travel well. If a role opens here where that kind of "
          "planning and process work matters, we would be glad to hear from you.") +

        PS("<strong>P.S.</strong> Calling out that your calculations assumed no drop out was a "
           "particularly strong part of the submission. Being transparent about the limitations "
           "of your own analysis is a habit worth keeping.")
    )


CANDIDATES = [
    dict(
        key="kanooz", corpus="Kanooz", first="Kanooz", full="Kanooz Siddiqui",
        markaz_name="Kanooz Ahmed Siddiqui",
        email="kanoozay@gmail.com", app=4111, cand=3083,
        drive="https://drive.google.com/drive/folders/1AQy-QpAQDnkXuu7nPlGlcvY2BHNmSAaL",
        submission_source=os.path.join(
            ROOT, "scripts", "reports", "send_smg_case_study_evaluation_round2_pilot.py"),
        anchors=["75.65%", "44.2%", "do not approach the administrator first",
                 "We would welcome the opportunity to meet with you at a time convenient for you"],
        body=letter_kanooz,
    ),
    dict(
        key="irfan", corpus="Irfan", first="Irfan", full="Irfan Siddiqui",
        markaz_name="Irfan Siddiqui",
        email="irfanmsiddiqui@outlook.com", app=4144, cand=659,
        drive="https://drive.google.com/drive/folders/10CM1Mvz7YgO8hS0dOOU4sx0LWhr69Y4B",
        submission_source=os.path.join(
            ROOT, "scripts", "reports", "send_smg_case_study_evaluation_pilot.py"),
        anchors=["23 users whose WhatsApp template never delivered",
                 "52 who opened the registration flow", "51 of 87", "275 lesson plans"],
        body=letter_irfan,
    ),
    dict(
        key="wajdan", corpus="Wajdan", first="Ali", full="Ali Wajdan Khan",
        markaz_name="Ali Wajdan Khan",
        email="malikaliwajdan@gmail.com", app=3977, cand=3219,
        drive="https://drive.google.com/drive/folders/1fKGJ3LtOXPy5N4EVXShdnDbdiQp3LyBA",
        submission_source=os.path.join(ROOT, "scripts", "reports", "smg_round4_candidates.py"),
        anchors=["170 users and 275 uses", "flow_sent at 180", "206",
                 "matches and sachets"],
        body=letter_wajdan,
    ),
    dict(
        key="basit", corpus="Basit", first="Basit", full="Syed Basit Hussain",
        markaz_name="Syed Basit Hussain",
        email="syed.basit89@gmail.com", app=4142, cand=3350,
        drive="https://drive.google.com/drive/folders/1ENRRftnC4SLDykVG3nSeE2pacNUGEQMi",
        submission_source=os.path.join(
            ROOT, "scripts", "reports", "send_smg_case_study_evaluation_pilot.py"),
        anchors=["43.8% against 45.6%", "34 coaching users in Pakistan against zero in Sri Lanka",
                 "Conduct teacher orientation sessions", "65%"],
        body=letter_basit,
    ),
    dict(
        key="rimsha", corpus="Rimsha", first="Rimsha", full="Rimsha Taj",
        markaz_name="Rimsha Taj",
        email="rimsha-taj@live.com", app=3956, cand=3201,
        drive="https://drive.google.com/drive/folders/1cplnC8M84DO9Zia11tum6gdT3KXBje57",
        submission_source=os.path.join(
            ROOT, "scripts", "reports", "send_smg_case_study_evaluation_round2_pilot.py"),
        anchors=["audio_coaching_sessions", "presentation users average 11.1 active days",
                 "3.16 sessions and 2.26 active days",
                 "calculations assume that there is no drop out"],
        body=letter_rimsha,
    ),
]


def build(c: dict) -> str:
    body = c["body"]() + feedback_widget(
        c["full"], ROLE, c["app"], "Case Study Feedback") + FOOTER
    return wrap(subject_line=SUBJECT_CORE, role=f"{ROLE} &nbsp;&middot;&nbsp; Job 42",
                eyebrow=EYEBROW["case_study_outcome"], body_html=body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="send to candidates, needs approval")
    ap.add_argument("--check", action="store_true", help="run the gate only, send nothing")
    ap.add_argument("--only", help="one candidate key")
    ap.add_argument("--cc", default=",".join(LIVE_CC),
                    help="comma-separated CC list, LIVE only")
    args = ap.parse_args()

    cands = [c for c in CANDIDATES if not args.only or c["key"] == args.only]
    if not cands:
        raise SystemExit(f"no candidate matching --only {args.only}")

    built = []
    for c in cands:
        subject = (SUBJECT_CORE if args.live
                   else f"[PILOT - {c['full']}] {SUBJECT_CORE}")
        html = build(c)
        print(f"\n{c['full']} (app {c['app']})")
        _gate(c, html, subject, args.live)
        built.append((c, subject, html))

    print(f"\n{'='*70}\nGATE PASSED for all {len(built)} letters")
    if args.check:
        print("--check: nothing sent")
        return

    sender = os.environ.get("EMAIL_USER", "ayesha.khan@taleemabad.com")
    password = os.environ["EMAIL_PASSWORD"]
    cc = [a.strip() for a in args.cc.split(",") if a.strip()] if args.live else []

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(sender, password)
        for c, subject, html in built:
            to = c["email"] if args.live else PILOT_TO
            if args.live:
                # the bouncer blocks external domains unless explicitly allowed;
                # allow exactly this candidate, nobody else.
                allow_candidate_addresses([to])
            msg = MIMEMultipart("related")
            msg["Subject"] = subject
            msg["From"] = f"Taleemabad People and Culture <{sender}>"
            msg["To"] = to
            if cc:
                msg["Cc"] = ", ".join(cc)
            alt = MIMEMultipart("alternative")
            alt.attach(MIMEText(html, "html"))
            msg.attach(alt)
            attach_logo(msg)
            safe_sendmail(s, sender, [to] + cc, msg.as_string(),
                          context=f"case_study_outcome_{'live' if args.live else 'pilot'}_"
                                  f"{c['key']}_app{c['app']}")
            print(f"  sent: {c['full']} -> {to}{' cc ' + ','.join(cc) if cc else ''}")

    print(f"\n{'LIVE' if args.live else 'PILOT'} send complete: {len(built)} emails")


if __name__ == "__main__":
    main()
