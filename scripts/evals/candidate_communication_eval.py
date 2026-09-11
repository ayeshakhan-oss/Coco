#!/usr/bin/env python3
"""
Evaluation harness for candidate communication emails.

MASTER REFERENCE: memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md
This file implements Rule 1 (Non-Psychologist), Rule 2 (Evidence-Based),
Rule 3 (Scorecard Translation), Rule 6 (Clarity), Rule 7 (Specificity),
and structural checks from Haroon Yasin framework.

Validates all 4 email types (CV rejections, values feedback, warm bench, GWC rejections)
against locked rules from the master philosophy file.

HARD BLOCK violations prevent sending (exit 2):
- Intent-word inference (Rule 1)
- Evidence-based violations (Rule 2)
- Format violations (em dashes, word count, PILOT prefix, section headings)
- Internal jargon (Rule 3)
- Interviewer names

WARNING violations are logged but allow sending (exit 0):
- Scorecard language transfer (Rule 3)
- Generic subject lines (Rule 7)
- Haroon Yasin balance issues
- Recruiting abstractions
- v8 layout drift (memory/v8_candidate_comms_layout_LOCKED.md, locked 2026-06-10)

Returns: {passed, violations[], word_count}
"""

import re
import unicodedata
import html
from typing import Optional, Dict, List, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

# Intent-inference forbidden phrases (case-insensitive)
# SOURCE: memory/CANDIDATE_COMMUNICATION_TONE_PHILOSOPHY_LOCKED.md - Rule 1: Non-Psychologist Rule
# These patterns assume motivation, confidence, character, intentions, or emotional state
# without explicit candidate statement. HARD BLOCK violations.
FORBIDDEN_INTENT_PHRASES = [
    r'you assumed',
    r'you believed',
    r'you thought',
    r'you preferred',
    r"you weren't appreciating",
    r'you were energized',
    r'you seemed',
    r'you lacked',
    r'you were hesitant',
    r'you would likely',
    r'you were not fully invested',
    r'you were not truly',
    r'you appeared',
    r"you seemed to lack",
    r"you didn't seem",
    r"you wouldn't",  # about capability, not action
    r'you seemed uncertain',
    r'you seemed uncommitted',
    r'you lacked confidence',
    r'you would struggle',
]

# Internal jargon (case-insensitive, whole-word match)
FORBIDDEN_JARGON = [
    r'\bGWC\b',
    r'\bKCD\b',
    r'\bwarm bench\b',
    r'\bvalues scorecard\b',
    r'\bcase study\b',
]

# Adversarial / judgmental register — HARD BLOCK (Ayesha 2026-09-08).
# A rejection letter exists to be useful to the candidate, never to justify or defend the
# decision. Warmth comes from respect and constructive language, not from withholding the
# feedback. PREFER: "the main gap we identified", "where the analysis could have been
# stronger", "one area that affected the conclusions", "what we would encourage you to look
# at differently".
HARSH_LANGUAGE = [
    r"\bfailure\b",
    r"\bwrong\b",
    r"the honest part",
    r"you failed",
    r"the problem with your",
    r"went wrong",
    r"\bblame\b",
    r"\bsloppy\b",
    r"\bcareless\b",
    r"you cannot\b",
    r"you are unable",
    r"\bincapable\b",
    # never impute motive to a candidate's analysis
    r"\bdeliberately\b",
    r"reverse.?engineer",
    r"until the arithmetic",
    r"chose assumptions",
    r"selecting assumptions",
]

# Corporate rejection boilerplate — HARD BLOCK. The opposite of a human letter.
CORPORATE_BOILERPLATE = [
    r"we regret to inform",
    r"after careful consideration",
    r"impressive (candidate )?pool",
    r"strong field of candidates",
    r"we wish you (all the best|the best) in your future",
]

# Recruiting abstractions (case-insensitive, whole-word match)
RECRUITING_ABSTRACTIONS = [
    r'\bstrong candidate\b',
    r'\bexcellent fit\b',
    r'\bimpressive profile\b',
    r'\bgood candidate\b',
    r'\bgreat candidate\b',
]

# Future-outreach promise phrases — WARNING (locked 2026-06-18).
# Candidate emails should express genuine welcome, but must NOT commit us to a
# future action the candidate could later hold us to. Internally we do revisit
# warm-bench people; the email just must not say so as a promise. Use
# conditional, candidate-initiated, disposition language instead:
#   "If a closer-fit role opens, we'd welcome a fresh application from you."
#   "We would be glad if you came back to us."
# Safe (NOT flagged): "we'd welcome", "we'd be glad to hear from you",
#   "we hope you'll come back", "stay connected".
FUTURE_PROMISE_PHRASES = [
    r'we will reach out',
    r"we'll reach out",
    r'we will be in touch',
    r"we'll be in touch",
    r'we will contact you',
    r"we'll contact you",
    r'we will call you',
    r"we'll call you",
    r'we will let you know',
    r"we'll let you know",
    r'we will keep your name',
    r"we'll keep your name",
    r'keep your (cv|resume|résumé|details|profile) on file',
    r'keep you on file',
    r'keep (you|your name) in view',
    r'expect to hear from us',
    r'you will hear from us',
    r"you'll hear from us",
    r'we will reach back',
]

# Generic subject line words (to be avoided in warm bench subjects)
GENERIC_SUBJECT_WORDS = [
    'interview',
    'feedback',
    'update',
    'position',
    'application',
    'rejection',
    'status',
]

# Known interviewers (to detect and flag their names)
KNOWN_INTERVIEWERS = [
    'Ayesha', 'Jawad', 'Jawwad', 'Huma', 'Ali', 'Mahnoor', 'Noah',
    'Khan', 'Yasin', 'Mujtaba', 'Hassan', 'Fatima', 'Bilal',
]

# Minimum word count by email type (Ayesha 2026-09-11).
#
# A FEEDBACK email carries a decision plus the reasoning behind it, and that is
# what takes 800 words. All five types the webapp handles are feedback emails:
# a CV rejection, values feedback, warm bench, a GWC rejection, and a case study
# outcome (an evaluation of their submission, so feedback first).
#
# The two SHORT types are short because they carry NO feedback: the Case Study
# UPDATE (debrief pending, 120-250) and the Internal Announcement (staff, not a
# candidate, 150-400). Do not confuse the case study UPDATE with the case study
# OUTCOME. Neither short type is drafted by the webapp today; they live in their
# own send scripts. They are listed here so that adding one never silently
# inherits the 800-word rule.
WORD_MINIMUMS = {
    'cv_rejection': 800,
    'values_feedback': 800,
    'warm_bench': 800,
    'gwc_rejection': 800,
    'case_study_outcome': 800,
    # not feedback -> not 800
    'case_study_update': 120,
    'internal_announcement': 150,
}
DEFAULT_WORD_MINIMUM = 800


# Section headings by email type
SECTION_HEADINGS = {
    # "Where We Found Questions" was renamed 2026-09-11: it contained the
    # hard-blocked phrase "the honest part", so every warm-bench and GWC letter
    # was blocked on a heading the renderer itself printed. The replacement
    # matches the wording cv_rejection and values_feedback already use, so the
    # three decision types now read in one voice.
    'warm_bench': {
        'required': [
            'What Stayed With Us',
            'Where We Found Questions',
            'Where We Want to Leave This',
        ]
    },
    'values_feedback': {
        'required': [
            'What We Liked Most About You',
            "Where We Found Ourselves Sitting With Questions",
            'What We Think You Should Do Next',
        ]
    },
    'gwc_rejection': {
        'required': [
            'What Stayed With Us',
            'Where We Found Questions',
            'Where We Want to Leave This',
        ]
    },
    'cv_rejection': {
        'required': [
            'What we appreciated',
            'Where we found questions',
            'What we think you should do next',
        ]
    },
    # Skill 01 type #8 (2026-09-08). Submitted a case study, below the 70% benchmark.
    # A slot given as a LIST accepts any one of its alternatives: the gap section is
    # count-agnostic in most letters and count-specific where the letter names how many
    # areas there were. 'optional' headings are allowed but never demanded, because the
    # forward-looking lesson section only earns a place when there is one worth giving.
    'case_study_outcome': {
        'required': [
            'What Your Work Showed Us',
            [
                'Where the Submission Could Have Been Stronger',
                'Two Areas That Shaped the Outcome',
                'The Main Gap We Identified',
            ],
            'Where We Want to Leave This',
        ],
        'optional': [
            'What We Would Encourage You to Look at Differently',
        ],
    },
}

# Mandatory opening line — locked 2026-06-18.
# Must be the FIRST line after the salutation ("Dear <Name>,") for ALL 4
# candidate-communication types (CV rejection, values feedback, warm bench,
# GWC rejection). It says "today this is a no", not "never" — honest because
# of the word "now". It MUST be paired with candidate-initiated reapplication
# language ("if a closer-fit role opens, we'd welcome a fresh application"),
# NEVER a promise of proactive outreach we will not keep.
REQUIRED_OPENING_LINE = "This is not a yes for now."
# normalized (lowercase, no trailing punctuation) for matching
_REQUIRED_OPENING_NORM = "this is not a yes for now"

# ============================================================================
# CORE EVAL LOGIC
# ============================================================================

def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    return text


def count_words(text: str) -> int:
    """Count words in text (case-insensitive, after stripping HTML)."""
    clean = strip_html(text)
    words = clean.split()
    return len(words)


def check_word_count(body: str, min_count: int = 800) -> Tuple[bool, int, Optional[str]]:
    """
    Check if email body meets minimum word count.
    Returns: (passed, actual_count, detail_msg)
    """
    actual = count_words(body)
    passed = actual >= min_count
    detail = f"Word count: {actual} / {min_count} required"
    return passed, actual, detail


def check_intent_words(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for forbidden intent-inference phrases.
    Returns: (passed, detail_msg_if_found)
    """
    clean = strip_html(text)
    for pattern in FORBIDDEN_INTENT_PHRASES:
        matches = re.finditer(pattern, clean, re.IGNORECASE)
        for match in matches:
            # Extract context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(clean), match.end() + 50)
            context = clean[start:end].replace('\n', ' ')
            detail = f'Found: "{match.group()}" in context: ...{context}...'
            return False, detail
    return True, None


def check_em_dashes(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for em dashes (—).
    Returns: (passed, detail_msg_if_found)
    """
    if '—' in text:
        # Find first occurrence
        idx = text.find('—')
        start = max(0, idx - 40)
        end = min(len(text), idx + 40)
        context = text[start:end].replace('\n', ' ')
        detail = f'Found em dash in: ...{context}...'
        return False, detail
    return True, None


def check_pilot_prefix(subject: str, pilot_mode: bool) -> Tuple[bool, Optional[str]]:
    """
    Check that [PILOT – ] prefix is NOT in subject when pilot_mode=False.
    Returns: (passed, detail_msg_if_found)
    """
    if not pilot_mode and '[PILOT' in subject:
        detail = f'CRITICAL: [PILOT] prefix found in subject but PILOT_MODE=False. Subject: "{subject}"'
        return False, detail
    return True, None


def check_section_headings(body: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """
    Check that required section headings are present.
    Returns: (passed, detail_msg_if_missing)
    """
    if email_type not in SECTION_HEADINGS:
        return True, None  # No check for unknown type

    required = SECTION_HEADINGS[email_type]['required']
    clean = strip_html(body)

    def present(heading: str) -> bool:
        return bool(re.search(re.escape(heading), clean, re.IGNORECASE))

    missing = []
    for slot in required:
        # A slot may be a single heading, or a list of accepted alternatives.
        if isinstance(slot, (list, tuple)):
            if not any(present(h) for h in slot):
                missing.append(" OR ".join(slot))
        elif not present(slot):
            missing.append(slot)

    if missing:
        detail = f'Missing section headings: {", ".join(missing)}'
        return False, detail
    return True, None


def check_opening_line(body: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """
    Check that the mandatory opening line ("This is not a yes for now.") is
    present AND appears before the first required section heading (i.e. it sits
    right after the salutation, not buried in the body). Applies to all 4 types.
    Returns: (passed, detail_msg_if_missing_or_misplaced)
    """
    clean = strip_html(body)
    clean_lower = clean.lower()

    phrase_idx = clean_lower.find(_REQUIRED_OPENING_NORM)
    if phrase_idx == -1:
        detail = (f'Missing mandatory opening line "{REQUIRED_OPENING_LINE}". '
                  f'It must be the first line after the salutation, for every '
                  f'candidate-communication type.')
        return False, detail

    # Must appear before the first section heading.
    required = SECTION_HEADINGS.get(email_type, {}).get('required', [])
    # A slot may be a list of accepted alternatives; flatten before searching.
    flat = []
    for slot in required:
        flat.extend(slot if isinstance(slot, (list, tuple)) else [slot])
    first_heading_idx = None
    for heading in flat:
        m = re.search(re.escape(heading), clean, re.IGNORECASE)
        if m and (first_heading_idx is None or m.start() < first_heading_idx):
            first_heading_idx = m.start()

    if first_heading_idx is not None and phrase_idx > first_heading_idx:
        detail = (f'Opening line "{REQUIRED_OPENING_LINE}" must appear before the '
                  f'first section heading (right after the salutation), not buried '
                  f'in a later section.')
        return False, detail

    return True, None


# Types where "case study" IS sanctioned candidate-facing language, because the case study
# is the candidate's own deliverable and we invited them to produce it:
#   case_study_update  - Skill 01 type #6 (Ayesha 2026-08-13)
#   case_study_outcome - Skill 01 type #8 (Ayesha 2026-09-08)
# The exemption is scoped to the phrase "case study" only. GWC, KCD, warm bench and values
# scorecard stay blocked for every type.
CASE_STUDY_PHRASE_ALLOWED = {"case_study_update", "case_study_outcome"}


def check_jargon(text: str, email_type: str = "") -> Tuple[bool, Optional[str]]:
    """
    Check for internal jargon (GWC, KCD, warm bench, values scorecard, case study).
    Returns: (passed, detail_msg_if_found)
    """
    clean = strip_html(text)
    patterns = list(FORBIDDEN_JARGON)
    if email_type in CASE_STUDY_PHRASE_ALLOWED:
        patterns = [p for p in patterns if p != r'\bcase study\b']
    for pattern in patterns:
        matches = re.finditer(pattern, clean, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 30)
            end = min(len(clean), match.end() + 30)
            context = clean[start:end].replace('\n', ' ')
            detail = f'Found internal jargon: "{match.group()}" in context: ...{context}...'
            return False, detail
    return True, None


def check_harsh_language(text: str, email_type: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Adversarial or judgmental register (Ayesha 2026-09-08). Returns (passed, detail).

    Scans the WHOLE letter, headings included. No carve-outs (Ayesha 2026-09-11:
    a hard-blocked phrase must never appear in any candidate communication). The
    section heading that used to collide with this list was renamed instead —
    see SECTION_HEADINGS.
    """
    clean = strip_html(text)
    for pattern in HARSH_LANGUAGE:
        m = re.search(pattern, clean, re.IGNORECASE)
        if m:
            ctx = clean[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
            return False, f'Harsh/adversarial language "{m.group()}" in context: ...{ctx}...'
    return True, None


def check_corporate_boilerplate(text: str) -> Tuple[bool, Optional[str]]:
    """Generic rejection boilerplate. Returns (passed, detail)."""
    clean = strip_html(text)
    for pattern in CORPORATE_BOILERPLATE:
        m = re.search(pattern, clean, re.IGNORECASE)
        if m:
            return False, f'Corporate rejection boilerplate: "{m.group()}"'
    return True, None


def check_interviewer_names(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for interviewer names in the email body.
    Returns: (passed, detail_msg_if_found)
    """
    clean = strip_html(text)
    # Exclude the salutation ("Dear <Name>,") from this scan: it legitimately
    # contains the CANDIDATE's OWN name, which can collide with a known
    # interviewer first name (e.g. a candidate genuinely named Jawwad / Ali /
    # Fatima). This rule targets an interviewer being NAMED in the body /
    # rationale, never the candidate's own greeting.
    scan = re.sub(r'(?i)\bdear\b[^,\n]{1,60},', ' ', clean)
    for name in KNOWN_INTERVIEWERS:
        # Whole-word match (case-sensitive for common names)
        pattern = r'\b' + re.escape(name) + r'\b'
        matches = re.finditer(pattern, scan)
        for match in matches:
            start = max(0, match.start() - 40)
            end = min(len(scan), match.end() + 40)
            context = scan[start:end].replace('\n', ' ')
            detail = f'Found interviewer name "{match.group()}" in context: ...{context}...'
            return False, detail
    return True, None


# First-person-SINGULAR pronouns. The email speaks in the company's collective
# voice ("we"/"our"/"us"), never as one individual ("I"/"my"/"me"). Whole-word
# matching, so "AI", "many", "time", "some" never trip it.
_FIRST_PERSON_SINGULAR = re.compile(
    r"\bI\b|\bI['’](?:m|ve|ll|d)\b|\b[Mm]y\b|\b[Mm]ine\b|\b[Mm]e\b|\b[Mm]yself\b"
)


def check_first_person_singular(text: str) -> Tuple[bool, Optional[str]]:
    """The email must use the collective 'we' voice, never first-person singular.
    A decision from Taleemabad is 'we', not one person's 'I'."""
    clean = strip_html(text)
    m = _FIRST_PERSON_SINGULAR.search(clean)
    if m:
        i = m.start()
        ctx = clean[max(0, i - 40): i + 40].replace('\n', ' ')
        detail = (f'First-person singular "{m.group()}" found. Write in the '
                  f'collective "we"/"our"/"us" voice, never "I"/"my"/"me". '
                  f'Context: ...{ctx}...')
        return False, detail
    return True, None


# CV/application-stage rejections had NO interview, call, or conversation — only
# a written application. These phrases fabricate an interaction that never
# happened. Checked for cv_rejection ONLY. Domain words that CAN be legit ("the
# interview stage", "assessment", an "in-person" role) are deliberately excluded.
_CV_INTERACTION_PHRASES = (
    "conversation", "we spoke", "spoke with", "we met", "met with you",
    "when we talked", "talked with you", "our discussion", "we discussed",
    "our meeting", "our call", "our time together",
)


# ---------------------------------------------------------------------------
# CV-STAGE GROUNDING (Skill 01, 01_candidate-rejections.md)
#
# Enforces, mechanically, three lines the SOP has always required but nothing
# ever checked:
#   Step 2  "Only use observations from actual CV text."
#   Rule 5  "every strength and gap must be tied to actual CV text ...
#            Never make up observations."
#   Rule 7  "Never assume data - if not in CV, state 'Not mentioned in your CV'
#            rather than filling in gaps."
#
# Why this exists: 27 CV rejections were sent live (2026-06-30 -> 2026-07-09)
# whose drafter had only the candidate's first name and the role title. One
# praised a candidate's "familiarity with the Lahore market"; his CV, unread in
# the database, contains neither "Lahore" nor "retention". Every one of those
# letters passed this harness, because the harness checked how a letter SOUNDS
# and never whether anything in it was TRUE.
#
# The check is deliberately narrow and mechanical. It cannot judge paraphrase.
# It catches the class of error that actually happened: concrete particulars -
# place names, employers, tools, figures - asserted about a person when they
# appear nowhere in their own application.
# ---------------------------------------------------------------------------

# Words a letter may capitalise without making a claim about the candidate: our
# own identity, the letter's furniture, calendar words, and the ordinary English
# that opens a clause. Anything outside this set must come from their material.
_GROUNDING_ALLOWLIST = {
    "taleemabad", "coco", "people", "culture", "team", "talent", "acquisition",
    "hiring", "careers", "warm", "regards", "dear", "thank", "thanks", "sincerely",
    "your", "you", "we", "our", "us", "the", "a", "an", "and", "but", "if", "it",
    "this", "that", "there", "these", "those", "they", "them", "their",
    "what", "where", "when", "how", "why", "who", "which", "while", "since",
    "here", "here's", "there's", "did", "does", "do", "yes", "no", "not", "for",
    "from", "with", "without", "about", "after", "before", "because", "both",
    "each", "every", "some", "many", "most", "much", "more", "less", "few",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "first", "second", "third", "next", "last", "then", "now", "still", "also",
    "at", "in", "on", "of", "to", "by", "as", "is", "are", "was", "were", "be",
    "been", "being", "has", "have", "had", "will", "would", "can", "could",
    "should", "may", "might", "must", "so", "too", "very", "just", "only",
    "role", "application", "applications", "applicant", "candidate", "cv",
    "resume", "feedback", "note", "update", "interview", "stage", "process",
    "position", "job", "work", "experience", "skills", "background",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "pakistan", "pakistani",  # our own operating country, not a claim about them
    "english", "urdu",
}

# Tokens too common to count as evidence that a letter engaged with a CV.
_GROUNDING_STOPWORDS = _GROUNDING_ALLOWLIST | {
    "able", "across", "again", "against", "all", "along", "already", "always",
    "another", "any", "anything", "around", "away", "back", "best", "better",
    "between", "beyond", "build", "building", "built", "came", "come", "coming",
    "given", "give", "gives", "going", "good", "great", "help", "helped", "into",
    "keep", "kind", "know", "known", "like", "look", "looked", "looking", "made",
    "make", "makes", "making", "mean", "means", "move", "moving", "need", "needs",
    "new", "often", "other", "others", "over", "own", "part", "place", "put",
    "read", "real", "really", "right", "said", "same", "saw", "say", "see", "seen",
    "sense", "set", "show", "showed", "shows", "side", "something", "sort",
    "take", "taken", "tell", "than", "thing", "things", "think", "thought",
    "through", "time", "times", "under", "until", "upon", "used", "using", "want",
    "wanted", "way", "ways", "well", "went", "were", "whether", "within", "years",
    "year", "your", "yours",
}


# Ordinary English that is routinely capitalised mid-sentence: job titles we use
# ("second chair to our Head of Growth"), nouns opening a clause after a colon,
# and words inside our own headings. Flagging these produced an 89% false-block
# rate against the 103 Job-42 letters. A term is only reported as a possible
# fabrication when it is NOT ordinary English — which is what an invented tool,
# employer or place actually looks like (ChurnZero, Totango, Lahore).
_COMMON_WORDS = {
    "head", "heads", "lead", "leads", "leader", "leadership", "growth", "manager",
    "management", "director", "officer", "chief", "senior", "junior", "associate",
    "partner", "partners", "partnership", "partnerships", "state", "states",
    "united", "north", "south", "east", "west", "central", "region", "regional",
    "market", "markets", "sector", "industry", "business", "company", "companies",
    "organisation", "organization", "product", "products", "project", "projects",
    "programme", "program", "service", "services", "customer", "customers",
    "client", "clients", "student", "students", "school", "schools", "education",
    "teacher", "teachers", "learning", "training", "development", "operations",
    "sales", "marketing", "finance", "revenue", "budget", "strategy", "strategic",
    "data", "research", "design", "content", "brand", "digital", "technology",
    "engineering", "quality", "delivery", "support", "success", "impact", "scale",
    "team", "teams", "people", "culture", "values", "mission", "vision", "goal",
    "goals", "target", "targets", "metric", "metrics", "number", "numbers",
    "result", "results", "report", "reports", "review", "reviews", "meeting",
    "meetings", "call", "calls", "email", "story", "stories", "question",
    "questions", "answer", "answers", "example", "examples", "evidence", "detail",
    "details", "specific", "specifics", "clarity", "context", "scope", "stage",
    "stages", "step", "steps", "level", "levels", "scale", "size", "range",
    "era", "world", "future", "past", "present", "today", "tomorrow", "chapter",
    "door", "path", "journey", "career", "careers", "roles", "work", "working",
    "note", "notes", "line", "lines", "point", "points", "case", "cases",
    "trust", "care", "honest", "honesty", "respect", "courage", "joy",
    "craft", "hard", "things", "one", "all", "not", "yes", "no", "we", "our",
}


def _fold(text: str) -> str:
    """Normalise a side of the comparison. Applied IDENTICALLY to the letter and
    the corpus — an asymmetry here is a false block (e.g. '&' stripped on one
    side but kept on the other turned a verbatim 'M&E' into a fabrication)."""
    text = strip_html(text or "")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("’", "'").replace("‘", "'")
    text = text.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9'\s]", " ", text)


def _stem(word: str) -> str:
    """Crude suffix strip so 'partnerships' matches 'partnership'. Deliberately
    conservative: over-stemming grounds words the CV never contained."""
    for suffix in ("'s", "ing", "ers", "er", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    return word


def _token_set(text: str) -> set:
    tokens = set()
    for word in _fold(text).split():
        word = word.strip("'")
        if word:
            tokens.add(word)
            tokens.add(_stem(word))
    return tokens


def _ungrounded_particulars(
    text: str,
    email_type: str,
    cv_corpus: Optional[str],
    *,
    candidate_name: str = "",
    role: str = "",
    subject: str = "",
) -> List[str]:
    """Names, figures and quoted phrases in the letter that are absent from the
    candidate's own material. Shared by the hard block and the warning."""
    if email_type != "cv_rejection" or cv_corpus is None:
        return []

    corpus_tokens = _token_set(cv_corpus)
    corpus_flat = " " + " ".join(_fold(cv_corpus).split()) + " "
    letter = strip_html(text)

    # The candidate's name, the role title and our own subject line are ours or
    # theirs by definition, never invented claims about them.
    allow = set(_GROUNDING_ALLOWLIST)
    for source in (candidate_name, role, subject):
        for token in _fold(source).split():
            allow.add(token)
            allow.add(_stem(token))

    def _grounded(word: str) -> bool:
        return word in allow or word in corpus_tokens or _stem(word) in corpus_tokens

    ungrounded_terms: List[str] = []
    seen = set()
    blocks = [b for b in re.split(r"[\r\n]+", letter) if b.strip()]
    sentences = []
    for block in blocks:
        flat = re.sub(r"\s+", " ", block).strip()
        sentences.extend(re.split(r"(?<=[.!?:])\s+", flat))
    for sentence in sentences:
        # Skip the opening word: a sentence-initial capital carries no signal.
        for term in re.findall(r"[A-Za-z0-9&.'-]+", sentence)[1:]:
            if not term[:1].isupper():
                continue
            # A hyphenated or ampersand compound ("AI-era", "M&E") folds to
            # several words; judge each part, or the whole compound reads as
            # ungrounded merely because the CV spells it as separate words.
            parts = [p for p in _fold(term).split() if len(p) >= 3]
            if not parts:
                continue
            key = " ".join(parts)
            if key in seen:
                continue
            seen.add(key)
            # Only when EVERY part is absent from their material. If any part is
            # grounded the compound is theirs, spelled differently
            # ("ServiceNow-literate" against a CV that says "ServiceNow").
            if any(_grounded(p) for p in parts):
                continue
            invented = [p for p in parts if p not in _COMMON_WORDS]
            if len(invented) == len(parts):
                ungrounded_terms.extend(invented)

    ungrounded_numbers: List[str] = []
    for match in re.finditer(r"(\d[\d,]*(?:\.\d+)?)\s*(%|percent|years?|months?|people|person)", letter):
        raw = match.group(1).replace(",", "")
        if raw in seen:
            continue
        seen.add(raw)
        # Word-boundary containment: '8' must not be grounded by '2018'.
        if not re.search(r"(?<![\d.])" + re.escape(raw) + r"(?![\d])", corpus_flat):
            ungrounded_numbers.append(f"{raw}{match.group(2)}")

    ungrounded_quotes: List[str] = []
    # Double quotes only. A single quote in English prose is far more often a
    # possessive than a quotation: including it read "Taleemabad's work in
    # Pakistan's schools" as a quoted span and blocked a correct letter.
    for match in re.finditer(r"[\"“]([^\"“”]{8,200})[\"”]", letter):
        phrase = " ".join(_fold(match.group(1)).split())
        if phrase and phrase not in corpus_flat:
            ungrounded_quotes.append(match.group(1)[:80])


    items = []
    if ungrounded_terms:
        items.append("names/places/tools: " + ", ".join(repr(t) for t in ungrounded_terms[:8]))
    if ungrounded_numbers:
        items.append("figures: " + ", ".join(repr(n) for n in ungrounded_numbers[:6]))
    if ungrounded_quotes:
        items.append("quoted text that is not verbatim: "
                     + ", ".join(repr(q) for q in ungrounded_quotes[:4]))
    return items


def check_cv_grounding(
    text: str,
    email_type: str,
    cv_corpus: Optional[str],
    *,
    candidate_name: str = "",
    role: str = "",
    subject: str = "",
    # Calibrated 2026-09-11 on two real sets: the 103 Job-42 letters written by
    # the careful CLI path (min observed 26) and the 27 letters sent live from
    # the no-CV bug (median 21, p90 36). 25 sits just under the floor of the good
    # set: 0 of 98 correct letters blocked, 56% of the ungrounded ones caught.
    # Re-measure with scripts/evals/calibrate_cv_grounding.py before changing it.
    min_anchors: int = 25,
) -> Tuple[bool, Optional[str]]:
    """A CV-stage rejection must actually be built out of THIS candidate's CV.

    HARD BLOCK, and deliberately a POSITIVE requirement rather than a hunt for
    invented particulars. The 27 letters sent live on 2026-06-30..07-09 had no
    fabricated proper nouns to catch: they were fluent generic prose about people
    whose CVs were never opened, because the drafter was handed only a first name
    and a role title. A gate that only looks for inventions is silent on exactly
    that failure. So the letter must share at least `min_anchors` distinct
    content words with the candidate's application.

    Measured on the 103 Job-42 letters written by the careful CLI path: 3 blocked.
    The invented-particulars scan is a WARNING instead — see check_cv_particulars
    for why a hard block there was unusable.

    cv_rejection ONLY. Returns (True, None) when `cv_corpus` is None so callers
    with no corpus (a hand-written letter from the CLI) are not blocked by an
    absence; generation refuses separately when there is no evidence.
    """
    if email_type != "cv_rejection" or cv_corpus is None:
        return True, None

    corpus_tokens = _token_set(cv_corpus)
    letter = strip_html(text)

    # POSITIVE: does this letter reference their material at all?
    # An anchor is a content word the letter and the CV share. Ordinary English
    # and ordinary domain vocabulary are excluded, as are the candidate's name
    # and the role title, which both sides carry by definition.
    letter_tokens = _token_set(letter)
    generic = _GROUNDING_STOPWORDS | _COMMON_WORDS
    for source in (candidate_name, role, subject):
        for token in _fold(source).split():
            generic.add(token)
            generic.add(_stem(token))
    anchors = {
        t for t in (letter_tokens & corpus_tokens)
        if len(t) >= 5 and t not in generic and not t.isdigit()
    }

    if len(anchors) < min_anchors:
        return False, (
            f"This letter references the candidate's application only {len(anchors)} "
            f"time(s) ({min_anchors}+ expected), so it reads as generic prose that "
            "would fit any candidate. Skill 01 Rule 5: every strength and gap must be "
            "tied to actual CV text. Name what THIS CV actually shows."
        )
    return True, None


def check_cv_particulars(
    text: str,
    email_type: str,
    cv_corpus: Optional[str],
    *,
    candidate_name: str = "",
    role: str = "",
    subject: str = "",
) -> Tuple[bool, Optional[str]]:
    """Names, figures and quotes in a CV-stage rejection that do not appear in
    the candidate's application. WARNING, not a hard block — read on.

    Measured against the 103 Job-42 letters (written by the careful CLI path,
    each grounded in a CV that was read), a hard block on this flagged ~3 in 4.
    Most were legitimate: generic industry vocabulary ("CRM"), our own job titles
    ("Head of Growth"), and abbreviations expanded from the CV ("U.S." written as
    "United States"). A lexical test cannot separate those from an invention, and
    every relaxation that fixed them also blinded it to real ones.

    It is still worth surfacing, because it found a real fabrication in that
    supposedly-gold corpus: letter 3874 lists the candidate's toolkit as "HubSpot
    and Dynamics 365 to Totango, ChurnZero and Mixpanel" when their CV contains
    HubSpot, Dynamics, Totango and Mixpanel, and no ChurnZero. Four real tools and
    an invented fifth. So: show the operator the terms to check, block on the
    positive requirement (check_cv_grounding), and let a person judge these.
    """
    items = _ungrounded_particulars(
        text, email_type, cv_corpus,
        candidate_name=candidate_name, role=role, subject=subject,
    )
    if not items:
        return True, None
    return False, (
        "Check these against the CV before sending. They appear in the letter but "
        "not in the candidate's application, so each is either an invention or a "
        "wording the CV spells differently: " + "; ".join(items)
        + ". Skill 01 Rule 7: if it is not in the CV, do not fill the gap."
    )


def check_cv_no_interaction(text: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """A CV/application-stage rejection must not imply an interview / call /
    conversation that never happened. Applies to cv_rejection ONLY — everything
    must be grounded in the written application/CV."""
    if email_type != "cv_rejection":
        return True, None
    clean = strip_html(text).lower()
    for phrase in _CV_INTERACTION_PHRASES:
        idx = clean.find(phrase)
        if idx != -1:
            ctx = clean[max(0, idx - 30): idx + 40].replace("\n", " ")
            detail = (f'CV-stage rejection implies an interaction that never happened '
                      f'("{phrase}"). This candidate was screened on their WRITTEN '
                      f'application only. Ground everything in "your application"/"your CV"; '
                      f'do not reference interviews, calls, or conversations. '
                      f'Context: ...{ctx}...')
            return False, detail
    return True, None


def check_haroon_balance(body: str, email_type: str) -> Tuple[bool, Optional[str], int, int]:
    """
    Check Haroon Yasin balance rule: praise count should ≈ decision count.
    Only applies to warm_bench and gwc_rejection.
    Returns: (passed, detail_msg, praise_count, decision_count)
    """
    if email_type not in ['warm_bench', 'gwc_rejection']:
        return True, None, 0, 0  # Not applicable

    clean = strip_html(body)

    # Heuristic: count blue heading blocks
    # "What Stayed With Us" section vs "Where We Found Questions" section
    stayed_section = re.search(
        r"What Stayed With Us.*?(?=Where We Found Questions|$)",
        clean,
        re.IGNORECASE | re.DOTALL
    )
    honest_section = re.search(
        r"Where We Found Questions.*?(?=Where We Want to Leave|$)",
        clean,
        re.IGNORECASE | re.DOTALL
    )

    stayed_text = stayed_section.group() if stayed_section else ''
    honest_text = honest_section.group() if honest_section else ''

    # Count paragraphs (heuristic for depth/evidence)
    stayed_count = len([p for p in stayed_text.split('\n') if p.strip() and len(p.strip()) > 50])
    honest_count = len([p for p in honest_text.split('\n') if p.strip() and len(p.strip()) > 50])

    # Allow ±1 variance
    ratio_ok = abs(stayed_count - honest_count) <= 1

    if not ratio_ok:
        detail = f'Haroon balance issue: {stayed_count} praise paragraphs vs {honest_count} decision paragraphs (should be ±1). Consider equalizing depth.'
        return False, detail, stayed_count, honest_count

    return True, None, stayed_count, honest_count


def check_generic_subject(subject: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """
    Check subject line for generic words (warm bench only).
    Returns: (passed, detail_msg_if_generic)
    """
    if email_type != 'warm_bench':
        return True, None  # Only check warm bench

    clean = subject.lower()
    found_generic = []

    for word in GENERIC_SUBJECT_WORDS:
        if word in clean:
            found_generic.append(word)

    if found_generic:
        detail = f'Subject line too generic. Contains: {", ".join(found_generic)}. Should be poetic/story-based, tied to specific interview moment.'
        return False, detail

    return True, None


# v8 layout signatures (from scripts/utils/v8_template.py). Candidate comms must use these.
V8_LAYOUT_MARKERS = [
    'max-width:620px',
    '#f0f4f0',
    'cid:taleemabad_logo',
    'font-size:15px;line-height:1.8',
    'border-left:4px solid #1b5e20',
]


def check_v8_layout(html_body: str) -> Tuple[bool, Optional[str]]:
    """
    Verify the email uses the locked v8 layout (scripts/utils/v8_template.py).
    SOURCE: memory/v8_candidate_comms_layout_LOCKED.md (locked 2026-06-10).
    Returns: (passed, detail_msg_if_drifted). WARNING-level (flags drift, does not block).
    """
    missing = [m for m in V8_LAYOUT_MARKERS if m not in html_body]
    # Allow 1 missing (minor variation); flag if 2+ markers absent.
    if len(missing) >= 2:
        detail = (f'Layout does not match locked v8 ({len(missing)}/{len(V8_LAYOUT_MARKERS)} '
                  f'markers missing: {", ".join(missing)}). Import layout from '
                  f'scripts/utils/v8_template.py. See memory/v8_candidate_comms_layout_LOCKED.md.')
        return False, detail
    return True, None


def check_recruiting_abstractions(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for recruiting abstractions (strong candidate, excellent fit, etc).
    Returns: (passed, detail_msg_if_found)
    """
    clean = strip_html(text)
    for pattern in RECRUITING_ABSTRACTIONS:
        matches = re.finditer(pattern, clean, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 30)
            end = min(len(clean), match.end() + 30)
            context = clean[start:end].replace('\n', ' ')
            detail = f'Found recruiting abstraction: "{match.group()}". Use observed behaviors instead. Context: ...{context}...'
            return False, detail
    return True, None


def check_future_promise(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for future-outreach promises (we will reach out / contact you / keep
    your name on file, etc). Candidate emails express welcome via conditional,
    candidate-initiated language, never a commitment to a future action.
    SOURCE: no-future-promise rule (locked 2026-06-18).
    Returns: (passed, detail_msg_if_found). WARNING-level (flags, does not block).
    """
    clean = strip_html(text)
    for pattern in FUTURE_PROMISE_PHRASES:
        match = re.search(pattern, clean, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 40)
            end = min(len(clean), match.end() + 40)
            context = clean[start:end].replace('\n', ' ')
            detail = (f'Future-outreach promise "{match.group()}" detected. Express '
                      f'genuine welcome WITHOUT committing to a future action: use '
                      f'conditional, candidate-initiated wording ("if a closer-fit '
                      f'role opens, we would welcome a fresh application from you"). '
                      f'Context: ...{context}...')
            return False, detail
    return True, None


# ============================================================================
# MAIN EVAL FUNCTION
# ============================================================================

def evaluate_email(
    html_body: str,
    subject: str,
    email_type: str,
    pilot_mode: bool = True,
    cv_corpus: Optional[str] = None,
    candidate_name: str = "",
    role: str = "",
) -> Dict:
    """
    Run all checks on an email draft.

    Args:
        html_body: Email HTML body
        subject: Email subject line
        email_type: One of 'cv_rejection', 'values_feedback', 'warm_bench', 'gwc_rejection'
        pilot_mode: True if PILOT_MODE, False if live

    Returns:
        {
            'passed': bool,
            'word_count': int,
            'violations': [
                {'rule': str, 'severity': 'HARD_BLOCK' | 'WARNING', 'detail': str}
            ]
        }
    """
    violations = []
    word_count = count_words(html_body)

    # HARD BLOCK checks

    # 1. Word count
    minimum = WORD_MINIMUMS.get(email_type, DEFAULT_WORD_MINIMUM)
    passed, actual, detail = check_word_count(html_body, min_count=minimum)
    if not passed:
        violations.append({
            'rule': f'Word count minimum ({minimum})',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 2. Intent-words
    passed, detail = check_intent_words(html_body)
    if not passed:
        violations.append({
            'rule': 'No intent-word inference',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 3. Em dashes
    passed, detail = check_em_dashes(html_body)
    if not passed:
        violations.append({
            'rule': 'No em dashes (—)',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 4. PILOT prefix
    passed, detail = check_pilot_prefix(subject, pilot_mode)
    if not passed:
        violations.append({
            'rule': 'PILOT prefix control',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 5. Section headings
    passed, detail = check_section_headings(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Required section headings',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 5b. Mandatory opening line (locked 2026-06-18)
    passed, detail = check_opening_line(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Mandatory opening line ("This is not a yes for now.")',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 5c. Tone: adversarial register and corporate boilerplate (Ayesha 2026-09-08)
    passed, detail = check_harsh_language(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'No harsh or adversarial language (tone standard 2026-09-08)',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    passed, detail = check_corporate_boilerplate(html_body)
    if not passed:
        violations.append({
            'rule': 'No corporate rejection boilerplate (tone standard 2026-09-08)',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 6. Jargon
    passed, detail = check_jargon(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'No internal jargon (GWC/KCD/etc)',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 7. Interviewer names
    passed, detail = check_interviewer_names(html_body)
    if not passed:
        violations.append({
            'rule': 'No interviewer names',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 7b. Collective "we" voice (no first-person singular)
    passed, detail = check_first_person_singular(html_body)
    if not passed:
        violations.append({
            'rule': 'Collective "we" voice (no "I"/"my"/"me")',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 7c. CV-stage rejection must not fabricate an interview/conversation
    passed, detail = check_cv_no_interaction(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'CV rejection: no fabricated interview/conversation',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 7d. CV-stage rejection must be grounded in the candidate's own material
    #     (Skill 01 Rule 5 / Rule 7). Only runs when a corpus is supplied.
    passed, detail = check_cv_grounding(
        html_body, email_type, cv_corpus,
        candidate_name=candidate_name, role=role, subject=subject,
    )
    if not passed:
        violations.append({
            'rule': 'CV rejection: the letter must be built from their application',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 7e. Names/figures/quotes absent from their application. WARNING: a hard
    #     block here flagged ~3 in 4 correctly-grounded letters (generic industry
    #     vocabulary, our own job titles, abbreviations the CV writes short), and
    #     no relaxation separated those from real inventions. Surfaced for a human.
    passed, detail = check_cv_particulars(
        html_body, email_type, cv_corpus,
        candidate_name=candidate_name, role=role, subject=subject,
    )
    if not passed:
        violations.append({
            'rule': 'CV rejection: check these terms against the CV',
            'severity': 'WARNING',
            'detail': detail,
        })

    # WARNING checks

    # 8. Haroon Yasin balance
    passed, detail, praise_count, decision_count = check_haroon_balance(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Haroon Yasin balance (praise ≈ decision)',
            'severity': 'WARNING',
            'detail': detail,
        })

    # 9. Generic subject line
    passed, detail = check_generic_subject(subject, email_type)
    if not passed:
        violations.append({
            'rule': 'Subject line not generic (warm bench)',
            'severity': 'WARNING',
            'detail': detail,
        })

    # 10. Recruiting abstractions
    passed, detail = check_recruiting_abstractions(html_body)
    if not passed:
        violations.append({
            'rule': 'No recruiting abstractions',
            'severity': 'WARNING',
            'detail': detail,
        })

    # 10b. Future-outreach promise (no-future-promise rule, locked 2026-06-18)
    passed, detail = check_future_promise(html_body)
    if not passed:
        violations.append({
            'rule': 'No future-outreach promise',
            'severity': 'WARNING',
            'detail': detail,
        })

    # 11. v8 layout (locked 2026-06-10)
    passed, detail = check_v8_layout(html_body)
    if not passed:
        violations.append({
            'rule': 'v8 locked layout',
            'severity': 'WARNING',
            'detail': detail,
        })

    # Determine overall pass
    has_hard_blocks = any(v['severity'] == 'HARD_BLOCK' for v in violations)

    return {
        'passed': not has_hard_blocks,
        'word_count': word_count,
        'violations': violations,
    }


if __name__ == '__main__':
    # Test: standalone usage (for debugging)
    test_html = """
    <h2>What Stayed With Us</h2>
    <p>This is a test paragraph with good observation.</p>
    <h2>Where We Found Questions</h2>
    <p>This is where we discuss the gap.</p>
    <h2>Where We Want to Leave This</h2>
    <p>Final thoughts.</p>
    """

    result = evaluate_email(test_html, "Test Subject", "warm_bench", pilot_mode=True)
    print("Test result:", result)
