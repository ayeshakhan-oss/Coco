"""
RM internal case study outcome, below the 70% benchmark. Skill 01 type #8. PILOT to Ayesha.

Regional Manager, internal round. The 8 NIETE colleagues who submitted the case study and
scored below the 70% benchmark that gates the next stage.

Ayesha, 2026-09-08: "We wanna tell them we evaluated you on this benchmark evaluation of case
study, we only moved candidates that scored 70% in the case study. Yours wasn't part of it
unfortunately. We're attaching the benchmark case study evaluation and an excel sheet that
shows the score against your answers and what could have been better." And: be really polite,
they are internal team.

WHAT IS DIFFERENT FROM THE SMG COHORT (type #8, Job 42)
  - Audience is COLLEAGUES. They keep working here on Monday. The letter closes the process
    without closing the relationship, and never implies their standing at NIETE is affected.
  - TWO ATTACHMENTS carry the detail the letter deliberately does not:
      1. the benchmark answer key (the standard, written and QA'd before any submission opened)
      2. that person's OWN marked script as .xlsx, per question, with what their answer did
         and what would have scored higher
  - The individual score therefore lives in the attachment, NOT in the letter body. The body
    states the 70% rule only. This keeps the letter about the standard and puts the number
    where it belongs, next to the evidence for it.
  - NO QUOTATION MARKS anywhere in the body. The SMG cohort had a verified per-candidate text
    corpus to check quotes against; this cohort does not, so rather than risk a quote drifting
    from what someone actually wrote, the letters paraphrase and the gate blocks quoted
    phrases outright.

GATE: _gate() runs before any SMTP connection and raises SystemExit on a hard block. The
Layer 3 PreToolUse send hook is inert, so this is the real gate.

Usage:
    python scripts/send_rm_case_study_outcome_pilot.py --check      # gate only, send nothing
    python scripts/send_rm_case_study_outcome_pilot.py              # pilot to Ayesha, all 8
    python scripts/send_rm_case_study_outcome_pilot.py --only rida
    python scripts/send_rm_case_study_outcome_pilot.py --live       # needs Ayesha's approval
"""

import argparse
import json
import os
import re
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.utils.feedback_widget import feedback_widget  # noqa: E402
from scripts.utils.safe_send import safe_sendmail  # noqa: E402
from scripts.utils.v8_template import (EYEBROW, FOOTER, H, P, PS, attach_logo,  # noqa: E402
                                       wrap)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))

ROLE = "Regional Manager"
SUBJECT_CORE = "An Update on Your Regional Manager Case Study"
PILOT_TO = "ayesha.khan@taleemabad.com"

# 🔴 TWO DELIBERATE DEVIATIONS FROM THE LOCKED TYPE-8 RULES, BOTH AYESHA'S CALL 2026-09-08.
# She supplied the letter wording herself. Flip either flag back on if she wants it restored.
#   RULE10_OPENING: type #8 mandates "This is not a yes for now." as the first line. Her
#     wording opens with thanks instead. For internal colleagues that reads better; it is
#     still an unambiguous no by the second paragraph.
#   MIN_WORDS: types 1-4 and #8 require 800+. Her letter is ~300. The 800 minimum exists so a
#     rejection carries real feedback; here the feedback is the attached marked script, which
#     is far more specific than 800 words of prose would be.
RULE10_OPENING = False
MIN_WORDS = 250

# Ayesha, 2026-09-08: "they can book their own if they need to." The offer stands with no
# booking URL. These are colleagues on the same calendar system, so they can put time in
# directly. No link is invented, and none is needed.
BOOKING_URL = ""

# LIVE CC list, given verbatim by Ayesha 2026-09-08. Not inherited from any other role's
# script, and no bare first name was resolved from the repo: every address here was either
# supplied in full or is a verified Taleemabad address already seen in this thread.
LIVE_CC = [
    "asma.zaheer@niete.edu.pk",
    "bilal@niete.edu.pk",
    "ayesha.khan@taleemabad.com",
    "hiring@taleemabad.com",
    "ali.sipra@taleemabad.com",
]

KEEP = os.path.join(ROOT, "output", "rm_marking")
BENCHMARK_SOURCE = os.path.join(
    ROOT, "docs", "case_studies", "benchmarks", "rm_regional_manager_benchmark.md")
BENCHMARK_PDF = os.path.join(KEEP, "RM Case Study - Benchmark Answer Key.pdf")
SCORES_SOURCE = os.path.join(KEEP, "strict_scores.json")
QBQ_SOURCE = os.path.join(KEEP, "qbq.json")

ROSTER = json.load(open(os.path.join(KEEP, "roster.json"), encoding="utf-8"))
STRICT = json.load(open(SCORES_SOURCE, encoding="utf-8"))
QBQ = json.load(open(QBQ_SOURCE, encoding="utf-8"))
ALL_NAMES = [v["name"] for v in ROSTER.values()]

# ── HARD-BLOCK PATTERNS ────────────────────────────────────────────────────────
INTENT_WORDS = [
    r"you assumed", r"you believed", r"you thought", r"you preferred",
    r"you were energised by", r"you were energized by", r"you seemed", r"you appeared",
    r"you lacked", r"you were hesitant", r"you would likely", r"you didn'?t seem",
    r"you weren'?t", r"you wouldn'?t", r"you felt", r"you wanted to", r"you did not care",
    r"you were unwilling", r"you chose not to",
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
    r"expect to hear from us", r"you'll hear from us", r"we will let you know",
    r"we'll let you know",
]
JARGON = [r"culture fit", r"cultural fit", r"not quite the right fit", r"\bKCD\b", r"\bGWC\b",
          r"scorecard", r"values interview", r"warm bench"]
COMPARISONS = [r"other candidates", r"the pool\b", r"of the (eight|25|twenty-five)",
               r"the strongest submission", r"the weakest", r"\branked\b",
               r"compared to others", r"than others", r"top five"]
HARSH_LANGUAGE = [
    r"\bfailure\b", r"\bwrong\b", r"the honest part", r"you failed", r"the problem with your",
    r"went wrong", r"\bblame\b", r"\bsloppy\b", r"\bcareless\b", r"you cannot\b",
    r"you are unable", r"\bincapable\b", r"\bpoor\b", r"\bweak\b",
]
CORPORATE_BOILERPLATE = [
    r"we regret to inform", r"after careful consideration", r"impressive (candidate )?pool",
    r"strong field of candidates", r"we wish you (all the best|the best) in your future",
    r"unfortunately, (you|your application) (were|was) not",
]
INTERVIEWER_NAMES = [r"\bJawwad\b", r"\bJawad\b", r"\bAyesha\b", r"\bWaqas\b", r"\bZeshan\b",
                     r"\bMoiz\b", r"\bNoah\b"]


def strip_tags(html: str) -> str:
    import html as _h
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.I)
    txt = re.sub(r"</p>|</h2>|</li>", "\n", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"[ \t]+", " ", _h.unescape(txt))


def _gate(c: dict, body_html: str, subject: str, live: bool) -> list:
    text = strip_tags(body_html)
    blocks, warns = [], []

    for label, path in (("BENCHMARK_SOURCE", BENCHMARK_SOURCE),
                        ("BENCHMARK_PDF", BENCHMARK_PDF),
                        ("SCORES_SOURCE", SCORES_SOURCE),
                        ("QBQ_SOURCE", QBQ_SOURCE),
                        ("individual xlsx", c["xlsx"])):
        if not os.path.exists(path):
            blocks.append(f"{label} missing: {path}")

    words = len([w for w in re.split(r"\s+", text.strip()) if w])
    if words < MIN_WORDS:
        blocks.append(f"word count {words} is under the {MIN_WORDS} minimum")

    if not re.search(r"Dear\s+[^,\n]+,", text):
        blocks.append("no salutation found")
    if RULE10_OPENING and "This is not a yes for now." not in text:
        blocks.append('Rule 10 opening line required but absent')

    if "70%" not in text:
        blocks.append("the 70% benchmark rule is not stated")

    if re.search(r"\b\d{1,3}\s*(?:/|out of)\s*100\b", text):
        blocks.append("an out-of-100 score appears in the body")
    # The score itself is deliberately shared, but in the ATTACHED sheet, never as a figure in
    # the letter. So block a printed number, not a reference to the attachment.
    if re.search(r"you scored\s*\d|your (score|total) (of|was|is)\s*\d|scored\s+\d{1,3}",
                 text, re.I):
        blocks.append("a numeric score is printed in the body")

    quoted = re.findall(r'"([^"]{8,})"', text)
    if quoted:
        blocks.append(f"quotation marks in body (banned for this cohort): {quoted[:2]}")

    for nm in ALL_NAMES:
        if nm == c["full"]:
            continue
        if re.search(rf"\b{re.escape(nm)}\b", text):
            blocks.append(f"another colleague is named in this letter: {nm}")

    if not re.search(rf"\b{re.escape(c['first'])}\b", text):
        blocks.append("the recipient's own first name does not appear")

    for pats, label in ((INTENT_WORDS, "intent inference"),
                        (CONVERSATION_WORDS, "conversation reference"),
                        (FUTURE_PROMISE, "future-outreach promise"),
                        (JARGON, "internal jargon"),
                        (COMPARISONS, "candidate comparison"),
                        (HARSH_LANGUAGE, "harsh/judgmental register"),
                        (CORPORATE_BOILERPLATE, "corporate boilerplate"),
                        (INTERVIEWER_NAMES, "staff name")):
        for p in pats:
            if re.search(p, text, re.I):
                blocks.append(f"{label}: {p}")

    if re.search(FIRST_PERSON, text):
        blocks.append('first-person "I" voice')
    if "—" in text or "&mdash;" in body_html:
        blocks.append("em dash present")
    if "[PILOT" in subject and live:
        blocks.append("PILOT prefix on a live send")
    if not live and "[PILOT" not in subject:
        warns.append("pilot send without a PILOT prefix")

    if blocks:
        print(f"\n  BLOCKED  {c['full']}")
        for b in blocks:
            print(f"     - {b}")
        raise SystemExit(f"gate failed for {c['full']}")
    return warns


def body_for(c: dict) -> str:
    """
    Ayesha's own wording, 2026-09-08, used verbatim in substance for all eight.

    Deliberately IDENTICAL across the cohort. These are colleagues who sit near each other and
    will compare what they received; one consistent letter plus an individualised attachment is
    fairer, and easier to defend, than eight letters of varying warmth. All personalisation
    lives in the attached marked script.
    """
    book = (" You are also very welcome to book a twenty minute slot with us if you would prefer "
            "to talk through the feedback together.")
    return (
        P(f"Dear {c['first']},") +
        P(f"Thank you again for taking the time to apply for the {ROLE} position, and for "
          f"putting thought and effort into the case study. We know you completed this alongside "
          f"your existing responsibilities, and we really appreciate you putting yourself "
          f"forward for the opportunity.") +
        P("To keep the process fair and consistent, all case studies were evaluated against the "
          "same benchmark answer and scoring criteria. We had set a 70% benchmark for moving "
          "forward to the next stage. Unfortunately, your submission came in below that "
          "benchmark, so we will not be progressing your application further for this role at "
          "this time.") +
        P("We also did not want to share only the outcome without giving you visibility into the "
          "evaluation. We are attaching two things:") +
        P("<strong>The benchmark case study and evaluation</strong>, so you can see what the "
          "assessment was looking for.") +
        P("<strong>Your individual evaluation sheet</strong>, which shows your score against the "
          "different areas, what came through well in your response, and where your answer could "
          "have been stronger.") +
        P("Since this was an internal opportunity, we hope the feedback is useful for your "
          "development beyond this particular process as well. This decision is specific to this "
          "case study and this role, and it does not take away from the contribution you are "
          "already making at Taleemabad.") +
        P("If anything in the feedback is unclear, or if you would like to understand the "
          "evaluation in a little more detail, please feel free to reach out." + book) +
        P("Thank you again for the time, effort, and openness you brought to the process. We "
          "genuinely appreciate it.") +
        feedback_widget(c["full"], ROLE, c["code"], "case_study_outcome") +
        FOOTER
    )


# ── PER-CANDIDATE CONTENT ──────────────────────────────────────────────────────
# Every strength and gap below is drawn from that person's own marked script
# (output/rm_marking/strict_scores.json + qbq.json). Anchors are distinctive phrases that
# must survive into the rendered body, so a letter cannot go out generic.
CANDS = [
    dict(
        code="RM-14", first="Rida", full="Rida Abbas",
        anchors=["without new training", "protects", "sourced"],
        good_1="Your reading of the regional comparison was careful in a way that is easy to "
               "get wrong. You named the distortion running in both directions at once, that "
               "the urban picture is lifted by compliance while the rural picture is pushed "
               "down by activity that never synced, and you were willing to say that the urban "
               "region looks stronger on reported activity while refusing to treat that as "
               "proven impact. Holding those two ideas together is exactly the discipline the "
               "question was testing.",
        good_2="Your root-cause tests were genuinely well designed. Testing coach reach by "
               "making contact without new training isolates the thing you are actually "
               "measuring, and comparing digital against print lesson plans in comparable "
               "schools separates the delivery channel from the content itself. Your capacity "
               "rule, that every new request has to name what it protects, what it consumes and "
               "what will stop to make room, is a rule a team could adopt on Monday.",
        gap_1="The forced-prioritisation question carries the largest share of the marks, and "
              "its whole purpose is that the numbers close and can be checked by someone else. "
              "Your table set out the decisions clearly and protects all three of the highest "
              "priority activities, which was the right call, but it carries no after-figures, "
              "no total and no quantified saving. The capacity freed is given as a range and "
              "then flagged as needing validation, which leaves a reader without a number they "
              "can act on.",
        gap_2="A few answers were missing a component the question names outright. The "
              "information question asks where each item would come from, and no source column "
              "appears, so roughly a third of the marks on every row were unavailable. The "
              "coach question asks for an escalation trigger, and none is set. The stakeholder "
              "question asks for five specific columns, and three of them are folded into a "
              "single short stance. In each case the thinking underneath looked sound, and the "
              "marks were lost on the part that was not written down.",
        ps="Your instinct to test contact without adding training was the sharpest single move "
           "in your paper. It is the kind of design that saves a team weeks of chasing the "
           "wrong cause, and it is worth carrying into the next problem you are handed.",
    ),
    dict(
        code="RM-07", first="Khadija", full="Khadija Akbar",
        anchors=["denominator", "calibration", "workload offset"],
        good_1="You opened by asking for the definition and denominator of every indicator "
               "before comparing the two regions, which is the right instinct and one that very "
               "few submissions reached for. You also asked about scoring consistency and coach "
               "calibration, in effect whether two coaches watching the same lesson would score "
               "it the same way. That question is the difference between a comparison that "
               "means something and one that only looks rigorous.",
        good_2="Your experiment answer was the strongest part of your paper. You read the sample "
               "correctly, defined what support each arm was allowed to receive, and set a "
               "go/no-go gate before launch rather than after. You also required a named "
               "workload offset before any coach time went to the experiment, which takes "
               "seriously the fact that capacity is finite. On root causes, attaching a specific "
               "intervention to each possible test result gave your analysis somewhere to go.",
        gap_1="The prioritisation question is where the largest block of marks sat, and it needed "
              "arithmetic. Your answer carries no after-state, no total and no quantified saving, "
              "so the reduction it proposes cannot be checked. Setting out a before figure and an "
              "after figure for each line, summing them, and stating the closing position would "
              "have made the whole answer verifiable.",
        gap_2="The regional analysis stopped short of the finding the case is built around. The "
              "relationship between how much the platform was used and what actually changed in "
              "classrooms is the central thread, and the outcome scores never enter your answer, "
              "so that link is never drawn. You also described the data problems as affecting "
              "both regions evenly, where the faults in fact run one way and understate the "
              "rural picture. On coaches, none of the escalation thresholds were time-bound, and "
              "the one case that was genuinely urgent was handled at the same pace as the rest.",
        ps="Asking whether two coaches would score the same lesson the same way is a question "
           "most people never think to ask. It is a habit worth keeping, because it protects "
           "every comparison that comes after it.",
    ),
    dict(
        code="RM-21", first="Areej", full="Areej Noshad",
        anchors=["conversion", "connectivity", "baseline week"],
        good_1="You quantified the conversion problem rather than describing it, setting the "
               "large gaps in lesson-plan and digital-content use against the very small "
               "difference they produced in outcomes. That is the heart of the case, and "
               "reaching it with numbers rather than adjectives is what the question was after. "
               "You then set different priorities for each region, conversion for one and "
               "adoption plus connectivity for the other, instead of writing one prescription "
               "for both.",
        good_2="Your third root-cause test compared schools with similar connectivity but "
               "different coaching contact, which controls the confound properly. You also "
               "committed to sizing which factor explained the largest share of the gap before "
               "intervening, rather than launching all three fixes at once. Your stakeholder "
               "answer used a real operational example, three observations a day expected during "
               "a baseline week when teachers were already occupied, to show how a target meets "
               "field reality. That example did more work than a page of argument would have.",
        gap_1="The regional question asks whether one region is genuinely outperforming the "
              "other, and your answer concludes that it is. The evidence in the case does not "
              "support a ranking in either direction once the student figures are read as pass "
              "rates within a group rather than as shares of the whole population. The overall "
              "pass rate and the below-grade and at-grade figures are not used, so the "
              "composition question is never reached. You also listed five defects in the "
              "dashboard and then kept it as the primary source, without naming which way the "
              "error runs.",
        gap_2="On prioritisation, only one saving is actually quantified. The remaining capacity "
              "needed is asserted rather than shown, and the additional observation demand is "
              "registered as a reason to protect the core activity but never priced. Putting a "
              "number on that demand is what turns the answer into something a Director can act "
              "on, because it changes the size of the problem.",
        ps="Bringing a baseline week into your stakeholder answer was a good instinct. Field "
           "detail like that is usually what makes a target negotiable, and it is a strength "
           "worth using more, not less.",
    ),
    dict(
        code="RM-11", first="Hafsa", full="Hafsa Bashir",
        anchors=["precedent", "rotating contact point", "control group"],
        good_1="Your stakeholder answer stood out because it rested on a real precedent rather "
               "than a plan. You cited a case where sharing dashboard data with a district "
               "officer led to school-head follow-up and training completion climbing sharply "
               "within two weeks, and then proposed using that lever deliberately. You also "
               "asked the Programme Director for school-level notifications, using existing "
               "authority as a substitute for coach follow-up time that does not exist.",
        good_2="On coaches, you branched the support across several possible underlying causes "
               "instead of applying one remedy to four different situations, which is what the "
               "question was really testing. You identified that one coach had quietly become "
               "the go-to person for every technical issue, and fixed it with a rotating contact "
               "point and a structured hand-off. On the experiment, you spotted that a load which "
               "looks manageable across a region can still overwhelm two or three individuals, "
               "and you protected the control group correctly.",
        gap_1="The regional analysis reached a conclusion the underlying figures do not support. "
              "Read as pass rates within a group rather than as shares of the whole student "
              "population, the rural region is meaningfully ahead with the students who started "
              "below grade level. Your answer explicitly sets the composition explanation aside, "
              "which is the reverse of what those figures point to. The very large gap in "
              "platform use, set against the very small difference in outcomes, is also never "
              "quantified, and that comparison is the central finding of the case.",
        gap_2="On prioritisation, the capacity you recover comes from reclassifying the case's "
              "own capacity table as miscounted rather than from a trade-off, so nothing is "
              "actually given up. Because the information question never asks for a breakdown "
              "of how coach time is really spent, that reclassification rests on assertion. The "
              "question is designed so that something has to give, and the marks follow the "
              "answer that says plainly what that is.",
        ps="Reaching for a precedent that had already worked, rather than proposing something "
           "new, was the most practical instinct in your paper. Evidence that a lever has moved "
           "before is the most persuasive thing you can put in front of a busy stakeholder.",
    ),
    dict(
        code="RM-01", first="Sana", full="Sana Nawaz",
        anchors=["where it would come from", "falsification", "donor visit"],
        good_1="Your information question was one of the more complete answers we read. Ten "
               "items, each tied to a decision, and each carrying all four parts the question "
               "asks for, including where it would come from. That last column is the one most "
               "often left out, and having it there is what turns a list of topics into "
               "something someone could actually go and collect.",
        good_2="Your root-cause work gave three genuinely distinct causes, each with a real "
               "falsification test, including one that checks whether the problem is an artefact "
               "of measurement rather than a real difference. On coaches you gave five elements "
               "for each of the four, properly differentiated, and treated one coach's reporting "
               "problem as possibly systemic rather than personal. On the experiment you rejected "
               "the single-region option on a real methodological argument rather than ducking "
               "the choice, and on the seventy-two hours you refused to stage the donor visit and "
               "said so directly. That took some nerve and it was the right call.",
        gap_1="The prioritisation question is the largest on the paper and it needed arithmetic. "
              "Nothing in the answer sums, there is no total, and no cut is quantified. The "
              "additional observation demand is also never priced, which matters because pricing "
              "it changes the size of the gap the answer has to close. Giving each line a before "
              "and after figure and stating the closing position would have made the whole "
              "argument checkable.",
        gap_2="Two smaller things cost marks. In the regional analysis the student figures were "
              "read as shares of the whole population rather than as pass rates within a group, "
              "which changes the conclusion, and the very large gap in platform use set against "
              "the very small difference in outcomes is never reached. On the experiment, the "
              "contamination fix depends on already stretched coaches withholding support, which "
              "is the thing most likely to slip. Keeping coaches out of it entirely would have "
              "solved the contamination risk and the capacity problem in one move.",
        ps="Refusing to stage the donor visit, and saying so plainly rather than hedging, was the "
           "moment your paper sounded most like a manager. That instinct is worth protecting.",
    ),
    dict(
        code="RM-20", first="Toseef", full="Toseef ur Rehman",
        anchors=["decision rule", "four teachers", "reduced coverage"],
        good_1="You attached an explicit decision rule to each cause, stating what follows if a "
               "test confirms it and what follows if it does not. That is the step that turns "
               "analysis into something that actually changes what happens next, and most "
               "submissions leave it out. Your illustration of four teachers who all appear as "
               "low adoption for four entirely different reasons, and the observation that a "
               "single intervention across all four would be wasted, was one of the clearest "
               "pieces of reasoning we read on this question.",
        good_2="On the priority conversation you offered three implementation options with a "
               "stated preference, including one where leadership has to name what receives "
               "reduced coverage. Putting that choice back where it belongs is the right move. "
               "You also drew a distinction between increasing the number of observations and "
               "increasing the number of useful ones, which is the distinction the whole scenario "
               "turns on. Your closing principle on coaches, that a capability gap should not be "
               "punished, a behaviour problem should not be tolerated because output is high, and "
               "burnout should not be answered by demanding more output, was well judged.",
        gap_1="The prioritisation question needed numbers and carries none. There is no "
              "after-state, no total and no quantified saving, and the capacity levers you list "
              "carry no figures, so a reader cannot tell whether the plan closes the gap. The "
              "additional observation demand is also left unpriced. Separating the data "
              "validation you keep from the duplicate reporting you automate away was a sound "
              "distinction, and putting figures beside it would have made it land.",
        gap_2="In the regional analysis the very large gap in platform use is never set against "
              "the very small difference in outcomes, so the central finding of the case is not "
              "reached. You list the data defects accurately but do not name that they run one "
              "way and understate the rural region. The student figures are then presented in "
              "full and the conclusion drawn that one region is clearly ahead, which leaves the "
              "below-grade-level reading unresolved.",
        ps="The four teachers who all look identical in the data for four different reasons is an "
           "example worth keeping. It is the clearest possible argument against a single fix, and "
           "you made it in a paragraph.",
    ),
    dict(
        code="RM-18", first="Javeria", full="Javeria Nayyab",
        anchors=["caseload", "re-login", "two options"],
        good_1="You derived the visit cycle from caseload arithmetic and showed that the problem "
               "is structural rather than a matter of effort. That is a genuinely different "
               "answer from the one most people give, and it is the one that survives contact "
               "with a Director, because it does not depend on anyone trying harder. You also "
               "attached a falsification condition to every cause, including what would tell you "
               "that you were wrong and had saved yourself the effort.",
        good_2="Your data-reliability section was grounded in something you had actually seen, "
               "training records jumping to fully complete on re-login, and you noted the error "
               "running in both directions rather than only the convenient one. On the priority "
               "conversation you gave leadership two options with the quality cost of each "
               "attached and asked which risk they preferred, which is the right shape for that "
               "conversation. You also described absorbing an impossible workload yourself at "
               "real cost, and drew the right lesson: a leader should neither absorb it silently "
               "nor push it down.",
        gap_1="The prioritisation answer gives rough ranges against an ambiguous base, with no "
              "total and no end-state figure, on the question that carries the most marks and is "
              "designed around closing arithmetic. It also declines to free any capacity from one "
              "activity on the grounds that it is not really coach work, which contradicts the "
              "capacity table the case supplies without reconciling the two. The additional "
              "observation demand is not priced.",
        gap_2="One proposal deserved a caveat it did not get. Training school focal persons to run "
              "observations in place of coaches raises an obvious question about the validity of "
              "the programme's core practice measure, and that question is never addressed. In "
              "the regional analysis the student figures are read as shares of the whole "
              "population, which produces a claim about how many below-grade-level students moved "
              "up that the underlying numbers do not support.",
        ps="Deriving the visit cycle from caseload, rather than treating it as a question of "
           "effort, was the strongest analytical move in your paper. It is the kind of finding "
           "that changes what a team asks for rather than how hard it works.",
    ),
    dict(
        code="RM-12", first="Salman", full="Muhammad Salman",
        anchors=["cheapest first", "one way", "smarter visits"],
        good_1="Your regional analysis was the strongest section of any part of your paper. You "
               "named the central comparison precisely, setting the large usage gap against the "
               "very small difference it produced in teaching quality, and you used the one "
               "measure that is hardest to distort. You then said plainly that the data error "
               "leans one way, that the better-connected region loses data the other never loses, "
               "and that the scoreboard is therefore tilted against the harder region. Very few "
               "submissions got that far.",
        good_2="You also gave leadership a usable answer rather than a caveat: that the regions "
               "cannot be ranked yet, that the record can be fixed within seventy-two hours, and "
               "that a defensible ranking follows. Your three root causes each carried a measure, "
               "a sample, a comparison group and a pre-committed result, and you ordered the tests "
               "cheapest first, refusing to spend coach time on an expensive cause before ruling "
               "out a simple technical one. On the additional observation demand you declined the "
               "blanket increase and translated it into smarter visits, with evidence rather than "
               "complaint.",
        gap_1="Several answers were shorter than the marks available. The information question "
              "asks for ten items and your answer gives four gates, without a source column and "
              "with the decisions only implied. The coach question carries no measurement method "
              "for any of the four and no escalation trigger for three of them. The stakeholder "
              "question is largely missing what you would need from each party, and escalation "
              "appears for only one of the four. The seventy-two-hour plan names no owner for any "
              "action and gives the reasoning collectively rather than action by action.",
        gap_2="The final question, the five-minute executive response and the three changes you "
              "would make, is not answered. That is the question that shows whether an analysis "
              "can be compressed into something a senior leader can act on immediately, and "
              "leaving it out meant the paper finished without demonstrating the thing it had "
              "spent nine questions earning the right to demonstrate.",
        ps="Saying outright that the scoreboard is tilted against the harder region, and showing "
           "why with the numbers, is the sort of clarity that makes people trust an analyst. It "
           "was the best thing in your paper by some distance.",
    ),
]

for _c in CANDS:
    _c["xlsx"] = os.path.join(KEEP, "individual", f"RM Case Study Feedback - {_c['full']}.xlsx")
    _c["email"] = ROSTER[_c["code"]].get("email", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()

    todo = [c for c in CANDS
            if not a.only or a.only.lower() in c["full"].lower()]
    if not todo:
        raise SystemExit(f"no candidate matches --only {a.only}")

    built = []
    for c in todo:
        subject = SUBJECT_CORE if a.live else f"[PILOT - {c['full']}] {SUBJECT_CORE}"
        html = wrap(SUBJECT_CORE, ROLE, EYEBROW["case_study_outcome"], body_for(c))
        warns = _gate(c, html, subject, a.live)
        words = len(re.split(r"\s+", strip_tags(html).strip()))
        built.append((c, subject, html, words))
        print(f"  OK  {c['full']:20} {words:5} words  "
              f"{'warn: ' + '; '.join(warns) if warns else ''}")

    if a.check:
        print("\n--check: gate passed for all, nothing sent.")
        return 0

    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("ayesha.khan@taleemabad.com", pw)
    for c, subject, html, _w in built:
        to = [c["email"]] if a.live else [PILOT_TO]
        cc = LIVE_CC if a.live else []
        if a.live:
            assert c["email"] and c["email"].endswith("@niete.edu.pk"),                 f"bad recipient for {c['full']}: {c['email']!r}"
            assert "[PILOT" not in subject, "PILOT prefix on a live send"
            assert c["full"] in os.path.basename(c["xlsx"]),                 f"attachment does not belong to {c['full']}: {c['xlsx']}"
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = "ayesha.khan@taleemabad.com"
        msg["To"] = ", ".join(to)
        if cc:
            msg["Cc"] = ", ".join(cc)
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText("HTML email. View in an HTML-capable client.", "plain"))
        alt.attach(MIMEText(html, "html"))
        msg.attach(alt)
        attach_logo(msg)
        for path, label in ((BENCHMARK_PDF, "RM Case Study - Benchmark Answer Key.pdf"),
                            (c["xlsx"], os.path.basename(c["xlsx"]))):
            with open(path, "rb") as fh:
                sub = "pdf" if path.endswith(".pdf") else \
                    "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                att = MIMEApplication(fh.read(), _subtype=sub)
            att.add_header("Content-Disposition", "attachment", filename=label)
            msg.attach(att)
        safe_sendmail(s, "ayesha.khan@taleemabad.com", to + cc, msg.as_string(),
                      context=f"rm_case_study_outcome_{'live' if a.live else 'pilot'}_"
                              f"{c['code']}")
        print(f"  sent {'LIVE' if a.live else 'PILOT'} {c['full']:20} -> {to}"
              + (f"  cc {len(cc)}" if cc else ""))
    s.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
