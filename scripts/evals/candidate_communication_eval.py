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

import os
import re
import unicodedata
import html
from functools import lru_cache
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
    # "case study" was REMOVED 2026-09-14 (Ayesha): it is not internal jargon.
    # The candidate wrote the case study, submitted it, and discussed it with us.
    # It is their own deliverable. A letter that cannot name it has to talk
    # around something they lived through, and it was blocking a warm-bench
    # letter for the phrase "in the case study conversation".
]

# Adversarial / judgmental register — HARD BLOCK (Ayesha 2026-09-08).
# A rejection letter exists to be useful to the candidate, never to justify or defend the
# decision. Warmth comes from respect and constructive language, not from withholding the
# feedback. PREFER: "the main gap we identified", "where the analysis could have been
# stronger", "one area that affected the conclusions", "what we would encourage you to look
# at differently".
HARSH_LANGUAGE = [
    # "failure" ONLY when it is aimed at the person or their work. A bare
    # \bfailure\b hard-blocked a warm-bench letter on "a total electricity
    # failure" - the candidate's OWN story about a power cut during a bake
    # sale, which is the kind of specific detail these letters are supposed
    # to carry. "their failure modes" is a technical term and is spared too.
    # 0/103 false positives on the sent corpus.
    r"\b(your|his|her|their) failure\b(?! modes?\b)",
    r"\bfailure to (demonstrate|show|deliver|meet|provide|answer|engage|address|complete)\b",
    r"\b(was|is|were|are|as) an? (complete |total |clear |real )?failure\b",
    r"\bwrong\b",
    # "the honest part" was REMOVED 2026-09-14 (Ayesha). It is the locked
    # warm-bench/GWC section heading ("Here's the Honest Part"), which
    # rendering.render_body prints itself, so every one of those letters was
    # hard-blocked on a heading no author chose. The phrase entered this list
    # from the case-study-outcome work, aimed at a letter that argued with the
    # candidate, not at our own heading. The rest of the list is untouched.
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

# Career-coaching register in a CV-stage rejection — WARNING (Ayesha 2026-09-14).
#
# A CV rejection reports what we could and could not see in the application. It
# is not a development plan, and it must not tell someone what to do with their
# career. Two failure modes, both from a real letter:
#   "here is what we would encourage you to develop and document"  -> a syllabus
#   "look for a Trainer or Coordinator role"  -> reads as "you are not senior enough"
# Say instead: "we could not clearly see X in the application; there may well be
# experience behind it that shows this more strongly."
#
# HARD BLOCK since 2026-09-14. It shipped as a WARNING and a live draft passed
# checks while telling a candidate we could not be confident in "your readiness"
# and pointing him toward "a role more closely aligned with your teaching and
# training expertise". Ayesha listed these phrasings as ones to AVOID, so
# "passes checks" has to mean the letter is sendable. Patterns are specific
# phrases, not judgement calls.
# Tone violations, grouped by the BEHAVIOUR they represent (Ayesha 2026-09-14).
#
# Previously all of these sat in one list reported under a single label,
# 'Report the evidence, do not coach their career'. That label covered five
# different behaviours at once, so a person reading the editor could not tell
# whether a letter was coaching, grading an answer, or judging the person, and
# could not tell whether a fix had worked. Each group is now reported by name.
COACHING_CATEGORIES = {
    # Coaching: telling them what to do or develop - advice about what the candidate should build, learn or do next
    'COACHING': [
        r'\byou could (work on|develop|build|focus|strengthen|improve)\b',
        r'\bwe (would )?(encourage|recommend|suggest|advise) (you|that you)\b',
        r'\bhere is what (you should|we would encourage|we would suggest)\b',
        r'\bwhat (you need|we would encourage you) to develop\b',
        r'\bspend (some )?time (writing|documenting|building|developing)\b',
        r'\bnext time,? (bring|share|try|make sure|focus|consider)\b',
        r'\bin (future|your next) (interviews?|applications?|conversations?)\b',
        r'\bif you apply again,? (make sure|try|bring|consider)\b',
        r'\bwhen you (apply|interview) again\b',
        r'\b(bring|share) (forward )?(more )?examples? of\b',
        r'\bwhat (you|we would) (should|want to) demonstrate\b',
        r'\breflect on your (career|experience|approach|journey)\b',
        r'\byour next step\b',
        r'\bbefore applying (for|to)\b',
        r'\bthat will make you (stronger|unstoppable|a better)\b',
        r'\blean into (that|this)\b',
        r'\bkeep building\b',
        r'\bdevelop (this|that) further\b',
        r'\bthe step forward for you\b',
        r'\bif you (were to|ever) (build|gain|acquire|develop|get)\b',
        r'\bwhether through (a|an) \w+',
        r'\bthat could change the picture\b',
        r'\bif you (decide|chose|choose) to spend time\b',
        r'\bwant to reconnect\b',
        r"\bthat.s your choice to make\b",
        r'\byou (should|need to|needs to|ought to|must|have to|will need to)\b',
        r"\byou'(ll|d) (need|want|have) to\b",
        r'\bwe would encourage you to\b',
    ],
    # Career direction: naming their lane - advice about which roles, functions or paths suit them
    'CAREER_DIRECTION': [
        r'\bbetter (suited|suit|fit) (to|for)\b',
        r'\byou (are|may be|might be|would be) (better )?suited\b',
        r'(role|position|opportunit\w+|path) (more )?(closely )?aligned with your \w+',
        r'\blook for a (next )?role (where|that)\b',
        r'\b(a|an) (trainer|coordinator|assistant|junior|entry.level) (role|position)\b',
        r'\b(seek|pursue|build) (out )?(a |more )?(leadership|senior|bigger|management) (role|experience|opportunit)',
        r'\bleadership philosophy\b',
    ],
    # Grading their answer - assessing the quality of an individual interview answer
    'GRADING': [
        r'\byour (answer|answers|response|responses|reasoning|thinking|explanation)\b',
        r'\b(stayed|remained|felt|was|were) (generic|surface|vague|thin|shallow)\b',
        r"\b(details?|answer|reasoning) (thinned|didn't deepen|did not deepen)\b",
        r'\bwhen we (pushed|probed|pressed) you\b',
        r'\byou misread\b',
        r"\byou (weren't|were not) able to (answer|explain|articulate)\b",
        r'\byou (could ?n.t|did ?n.t) (explain|articulate|answer)\b',
        r'\byour (reasoning|answer|response|thinking) (stayed|remained|was|felt) \w+',
        r'\bwe (expected|were expecting|were looking for) (you to|a)\b',
        r'\bbut we expected\b',
        r'\bat (a )?surface level\b',
        r'\blacked depth\b',
    ],
    # Person-level judgement - a claim about who they are, their motivation, readiness or future
    'PERSON_JUDGMENT': [
        r'\byour readiness\b',
        r'\breadiness for (this|the|a)\b',
        r'\bready for (this|the|a) (role|level|step|seniority|position)\b',
        r"\byou (aren't|are not|re not) ready\b",
        r'\bnot (quite )?there yet\b',
        r'\b(take|taking) the next step\b',
        r'\bgrow into\b',
        r'\b(professional|leadership) maturity\b',
        r'\byou need more experience\b',
        r"\byou (don't|do not) have\b",
        r'\byou should have\b',
        r"\byou (haven't|have not) (developed|led|owned|run|managed|built)\b",
        r'\byour motivation\b',
        r'\b(circumstantial|opportunistic) rather than\b',
        r'\brather than (mission|purpose).driven\b',
        r'\bthat.s (real|genuine|true) (maturity|humility|character|self.awareness)\b',
        r'\bmost people would\b',
        r'\byou lack\b',
        r'\bthe kind of (person|professional) you are\b',
        r"\bnot something you (can|could) (know|understand|learn)\b",
        r"\byou (can ?not|can't|could ?not|couldn't) (know|understand|see) (that|this)\b",
        r'\bwithout having been (inside|in|part of)\b',
        r'\bpulling (toward|towards|away)\b',
        r'\b(not )?away from something else\b',
        r'\brunning away from\b',
        r"\bthat.s rare\b",
        r'\bwill take you far\b',
        r'\bthe kind of (maturity|self.awareness|wisdom|humility) (that|you)\b',
        # Certifying the person through OUR OWN observation. The noun list
        # above is a spelling list, and a letter simply used a noun that was
        # not on it: "that's the kind of clarity about what actually matters
        # that we saw in you" (comm-b0e84207, Muneeb). Match the STRUCTURE.
        # Calibrated: fires on 0 of the 103 sent letters. "the kind of
        # grounding this role requires" stays clean - it describes the ROLE.
        r'\bthe kind of\b[^.]{0,80}\bwe saw in you\b',
        # Three more certifying shapes, all from ONE drafted letter
        # (comm-fce8f63f) in which the harness reported only "most people
        # would" and missed these. Calibrated: 0 hits on the 103 sent letters.
        # Widened from "...who" after a letter wrote "you're exactly the kind
        # of person WE WANT to build with". Chasing each instance is how this
        # list grew all night; match the construction. 0/103 false positives,
        # and the approved benchmark letter still passes.
        r'\bthe kind of (person|professional|leader|someone)\b',
        r'\btells us (that )?you (have|are|can|could|would|will)\b',
        r'\byou have (the |a |genuine |real )?(genuine |real )?capacity\b',
        r"\bthat.s someone who\b",
        r"\byou.?ve proven\b|\byou have proven\b",
        r'\bthe kind of\b[^.]{0,80}\bthat (will|would) (take|carry|serve) you\b',
        r'\bgo far in (your career|this field|life)\b',
        r"\byou.re going to do (great|well|big things)\b",
    ],
    # A conditional door - welcoming them back only once they have fixed the gap
    'CONDITIONAL_DOOR': [
        # Naming the functions a candidate belongs in, dressed as an open
        # door: "if an opportunity comes up ... whether that's growth,
        # strategy, or relationship building". Still career direction.
        r"\b(role|opportunity|position|opening)\b[^.]{0,80}\bwhether that.s\b",
        r'\b(welcome|glad to hear from|hear from) (you|your \w+) again,? (if|once|when|after) you\b',
        r'\bif you (take on|gain|build|get|develop|acquire)\b.{0,90}\b(experience|exposure|background|track record)\b',
        r'\b(once|after|when) you (have|had|gain|build|develop)\b.{0,40}\b(come back|apply again|reapply|reach out)\b',
        r'\b(come back|apply again|reapply) (once|after|when) you\b',
    ],
    # Replaying interview evidence - replaying a question or scenario and what was missing from the answer
    'REPORT_EVIDENCE': [
        r'\bwhen we (walked through|ran|posed|gave you) (a|the|that)\b',
        r'\bwe (asked|walked) you (to|through|about)\b',
        r'\bwhen we asked (you )?(about|how|why|what|for)\b',
        r'\bwe wanted you to (tell|show|walk|explain)\b',
        r'\bwhat we heard (was|back)\b',
        r'\bthe scenario we (gave|posed|walked)\b',
        r'\bin (that|the) (scenario|role.play|exercise)\b',
    ],
}

COACHING_CATEGORY_LABELS = {
    'COACHING': 'Coaching: telling them what to do or develop',
    'CAREER_DIRECTION': 'Career direction: naming their lane',
    'GRADING': 'Grading their answer',
    'PERSON_JUDGMENT': 'Person-level judgement',
    'CONDITIONAL_DOOR': 'A conditional door',
    'REPORT_EVIDENCE': 'Replaying interview evidence',
}

# Back-compat: some callers/tests import the flat list.
COACHING_REGISTER = [p for pats in COACHING_CATEGORIES.values() for p in pats]


# Corporate rejection boilerplate — HARD BLOCK. The opposite of a human letter.
CORPORATE_BOILERPLATE = [
    r"we regret to inform",
    r"after careful consideration",
    r"impressive (candidate )?pool",
    r"strong field of candidates",
    # Narrowed 2026-09-14: broadening this to a bare "well" blocked "We wish you
    # well in your career", which is warmth, not boilerplate. The cliche is the
    # future-endeavours form.
    r"we wish you (all the best|every success)\b",
    r"wish you (all the best|the best|well) (in|for) your (future|next|continued)\b",
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
    # An offered meeting is a promise we then have to keep. A letter said
    # "we'd be happy to have a conversation with you and our leadership".
    r"(we.d|we would|we.re|we are) (be )?(happy|glad|keen) to (have|set up|arrange|schedule) (a|another) (conversation|call|chat|discussion|meeting)",
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
WORD_MAXIMUMS = {
    # Ayesha 2026-09-15: "I think don't add more than 800 words." Selective, not
    # exhaustive. Reported as a WARNING, so a letter already approved at a higher
    # count is never stranded by the rule arriving after it.
    'cv_rejection': 800,
    'values_feedback': 800,
    'warm_bench': 800,
    'gwc_rejection': 800,
}

WORD_MINIMUMS = {
    # 800 for EVERY feedback letter, cv_rejection included (Ayesha 2026-09-14,
    # confirmed after briefly trialling 350-550). With career coaching and
    # application replay both hard-blocked, the length has to come from being
    # more specific about the candidate's OWN experience and about exactly what
    # this role needed. If a letter runs short, add evidence, never guidance.
    # 2026-09-15 (Ayesha): 800 became the CEILING, not the floor. Letters were
    # running 993-1144 words by listing everything in the scorecard, and
    # "personalization is selective, not exhaustive". The floor drops so a
    # disciplined 700-word letter is not forced to pad; the cap below is what
    # bites now.
    'cv_rejection': 650,
    'values_feedback': 650,
    'warm_bench': 650,
    'gwc_rejection': 650,
    # case_study_outcome keeps its own locked 800 (CLAUDE.md Rule 25).
    'case_study_outcome': 800,
    # not feedback -> not 800
    'case_study_update': 120,
    'internal_announcement': 150,
}
DEFAULT_WORD_MINIMUM = 800


# Section headings by email type
SECTION_HEADINGS = {
    # LOCKED (Ayesha 2026-09-14): "Here's the Honest Part" stays. I renamed it on
    # 2026-09-11 to resolve a collision with the HARSH_LANGUAGE list, which bans
    # "the honest part" - that was my call, not an instruction, and it is
    # reverted. The collision is REAL and unresolved: the renderer prints this
    # heading, so warm_bench and gwc_rejection letters hard-block on it. See
    # check_harsh_language.
    'warm_bench': {
        'required': [
            'What Stayed With Us',
            "Here's the Honest Part",
            'Where We Want to Leave This',
        ]
    },
    # Heading LOCKED. The section's CONTENT is retoned (no career prescriptions
    # - see COACHING_REGISTER and the shared feedback tone note), but the
    # heading wording is not mine to change.
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
            "Here's the Honest Part",
            'Where We Want to Leave This',
        ]
    },
    # Headings LOCKED. The CONTENT of these sections is retoned (Ayesha
    # 2026-09-14: report what we could and could not see, never coach the
    # career) - see the shared feedback tone note and COACHING_REGISTER. The
    # heading wording is not mine to change; the alternative wordings in her
    # brief were illustrating the tone, not instructing a rename.
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
# Kept for callers that still import it. "case study" is no longer forbidden
# for ANY type (2026-09-14), so this no longer gates anything.
CASE_STUDY_PHRASE_ALLOWED = {"case_study_update", "case_study_outcome"}


def check_jargon(text: str, email_type: str = "") -> Tuple[bool, Optional[str]]:
    """
    Check for internal jargon (GWC, KCD, warm bench, values scorecard). These are
    OUR labels for OUR process; the candidate never hears them. "case study" is
    NOT on the list: it is the candidate's own deliverable.
    Returns: (passed, detail_msg_if_found)
    """
    clean = strip_html(text)
    for pattern in FORBIDDEN_JARGON:
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


# EVERY template (Ayesha 2026-09-14: "ABOUT THE TONE FOR ALL TEMPLATE ... WE'RE
# NOT COACHING"). case_study_outcome is included now; it was exempt on my own
# reasoning that its guidance is about the submitted WORK, and that exemption was
# not asked for.
_COACHING_CHECKED_TYPES = ("cv_rejection", "values_feedback", "warm_bench",
                           "gwc_rejection", "case_study_outcome")


# Replaying the application back at the candidate — WARNING (Ayesha 2026-09-14).
#
# "Use the application internally as evidence to understand the candidate, but
# synthesize it into an overall hiring perspective." The letter must never walk
# through it question by question, quote answers back, or point out individual
# unanswered questions. A real example of what this prevents:
#   BAD:  "The application asked how you handled ambiguity and you responded
#          'NAAAAA'. That was an important signal."
#   GOOD: "We weren't able to get enough insight into how you've navigated
#          ambiguity, difficult trade-offs, and changing priorities."
# It is also a dignity rule: never reproduce a weak, incomplete or embarrassing
# response. Ask whether the candidate needs that detail to understand the
# decision; if not, leave it out.
APPLICATION_REPLAY = [
    # --- quoting or attributing an answer ---
    r'\byou (were asked|answered|responded|wrote|said|stated|put)\b',
    r'\byour (response|answer|reply) (was|to|read|said)\b',
    r'\bin (response|answer) to (that|this|the)\b',
    r'\bmarked as\b',
    r'\bsimply (put|wrote|said|answered)\b',
    # --- naming a question at all ---
    r'\b(the|that|this|a) (reflection|application|screening|written|core) question\b',
    r'\b(the|that|this) question (asking|about|on|regarding|that asked)\b',
    r'\bthe application (asked|invited|prompted|required)\b',
    r'\b(question|prompt) \d+\b',
    r'\bwhen asked (about|how|why|what|to)\b',
    r'\bwe asked you (to|about|how|why|what)\b',
    r'\basking you to (share|describe|explain|tell)\b',
    # --- flagging that something was not answered. The 2026-09-14 escape:
    #     "was left unanswered (marked as 'NAAAAA')" slipped past patterns that
    #     required "question was unanswered" adjacent. Match the CONCEPT.
    r'\bunanswered\b',
    r'\bleft\b[^.]{0,24}\b(blank|empty|incomplete|unfilled|unanswered)\b',
    r'\b(no|without a|missing|absent) (response|answer|reply)\b',
    r"\b(was|were|you) (not|n't) (answer|complet|fill|respond)\w*\b",
    r'\b(did ?n.t|didn.t|not) (answer|respond|complete|fill)\b',
    r'\bskipped (that|this|the) (question|section|prompt)\b',
    r'\bincomplete (submission|response|answer|application)\b',
    r'\btechnical error\b',
]


def check_application_replay(text: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """Question-by-question replay of the candidate's WRITTEN APPLICATION.

    cv_rejection ONLY. This rule came from the CV-rejection spec ("Do Not Repeat
    Application Answers"), where the evidence is a form someone filled in and
    quoting it back is an audit. I wrongly applied it to every type alongside the
    coaching rule, which Ayesha did scope to all templates.

    The interview-stage letters are the opposite case: warm bench, values
    feedback and GWC rejections are REQUIRED to quote the candidate's own
    interview moments ("quote their actual interview moments with specific
    timestamps" - warm_bench_final_locked_approach.md), and case_study_outcome
    must quote their submission verbatim. Blocking "you said" there blocked the
    core technique of the letter (application 3869, Muneeb).
    """
    if email_type != "cv_rejection":
        return True, None
    clean = strip_html(text)
    for pattern in APPLICATION_REPLAY:
        m = re.search(pattern, clean, re.IGNORECASE)
        if m:
            ctx = clean[max(0, m.start() - 45):m.end() + 45].replace("\n", " ")
            return False, (
                f'Replaying the application ("{m.group()}"). Use it internally as '
                f'evidence, then synthesise: "we were not able to get enough insight '
                f'into how you have navigated X". Never quote answers back, walk '
                f'through questions, or name an unanswered one. Context: ...{ctx}...'
            )
    return True, None


def _without_headings(clean: str, email_type: Optional[str]) -> str:
    """Drop the section headings the RENDERER prints, before a tone scan.

    Necessary for exactly one reason: the locked closing heading is "What we
    think you should do next", which contains "you should" - the single most
    important phrase in COACHING_REGISTER. Scanning the rendered letter flagged
    103/103 of the Job-42 letters and 98/100 webapp CV rejections on our own
    template furniture, which would have made the check useless.

    Only the exact canonical heading text is removed. The BODY is still scanned
    in full, so a paragraph saying "you should bring more examples" is caught.
    """
    if not email_type:
        return clean
    spec = SECTION_HEADINGS.get(email_type, {})
    headings = []
    for slot in list(spec.get("required", [])) + list(spec.get("optional", [])):
        headings.extend(slot if isinstance(slot, (list, tuple)) else [slot])
    for heading in headings:
        clean = re.sub(re.escape(heading), " ", clean, flags=re.IGNORECASE)
    return clean


# ---------------------------------------------------------------------------
# SCORECARD LEAKAGE (Ayesha 2026-09-14)
#
# Hiring managers write scorecards fast, for colleagues, in blunt internal
# shorthand. They are not writing to the candidate and do not expect the
# candidate to read their words. The letter IS candidate-facing and may be
# forwarded, screenshotted or posted publicly.
#
# So scorecard language must be TRANSLATED, never carried across. A real case:
# the scorecard said "Motivation reads circumstantial ... wants out of a remote
# night-shift job" and the draft told the candidate "Your motivation came
# through as circumstantial rather than mission-driven."
#
# This catches the mechanical form of the failure: a distinctive run of words
# lifted from the scorecard into the letter. It cannot catch a close paraphrase,
# which is what the prompt rules are for.
# ---------------------------------------------------------------------------
_LEAK_NGRAM = 4          # consecutive content words shared = lifted, not coincidence
_LEAK_STOP = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "that", "this", "it", "is", "was", "were", "be", "been", "as", "at", "by",
    "he", "she", "they", "his", "her", "their", "you", "your", "we", "our",
    "not", "no", "from", "had", "has", "have", "do", "did", "does", "so",
}


def _content_words(text: str) -> List[str]:
    return [w for w in re.findall(r"[a-z0-9']+", _fold(text)) if w not in _LEAK_STOP]


_BENCHMARK_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".claude", "skills", "01_candidate-communication",
    "00_BENCHMARK-approved-letter.md",
)
_BENCHMARK_NGRAM = 6


@lru_cache(maxsize=1)
def _benchmark_letter_words() -> Tuple[str, ...]:
    """Content words of the APPROVED letter's prose only.

    Only the section between the two markers: the surrounding commentary is
    rules language ("we needed", "could not establish") that letters are
    SUPPOSED to share, and scanning it would flag good writing.
    """
    try:
        with open(_BENCHMARK_PATH, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return ()
    if "## THE LETTER, AS SENT" not in text:
        return ()
    body = text.split("## THE LETTER, AS SENT", 1)[1].split("## HOW THIS LETTER", 1)[0]
    return tuple(_content_words(body))


def check_benchmark_echo(text: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """Passages this letter shares with the benchmark letter, which belongs to a
    DIFFERENT candidate.

    Two different failures, one measure:
      1. FABRICATION - another person's story reused as though it were theirs.
         The benchmark now ships inside the drafting prompt, so this is a real
         risk that did not exist before.
      2. FORMULA - the model's habitual sentences, identical across letters.
         Measured the day the benchmark was created: a freshly drafted letter
         shared 21 consecutive content words of opening with it, before the
         benchmark was in the prompt at all. Two candidates comparing letters
         would see the same paragraph, and our own feedback widget asks "Did it
         feel written for you specifically?".

    A WARNING, never a hard block: some shared phrasing is the house voice, and
    a human is better placed than an n-gram to tell reuse from resemblance.
    The mandatory opening line is exempt - it is required to be identical.
    """
    bw = _benchmark_letter_words()
    if not bw or email_type not in _COACHING_CHECKED_TYPES:
        return True, None

    prose = _letter_prose(text, email_type)
    # The opening line is mandated verbatim; it cannot be an echo.
    prose = re.sub(re.escape(REQUIRED_OPENING_LINE), " ", prose, flags=re.IGNORECASE)
    lw = _content_words(prose)
    n = _BENCHMARK_NGRAM
    if len(lw) < n:
        return True, None

    grams = {" ".join(bw[i:i + n]) for i in range(len(bw) - n + 1)}
    lifted = [False] * len(lw)
    for i in range(len(lw) - n + 1):
        if " ".join(lw[i:i + n]) in grams:
            for j in range(i, i + n):
                lifted[j] = True

    spans, i = [], 0
    while i < len(lw):
        if lifted[i]:
            j = i
            while j < len(lw) and lifted[j]:
                j += 1
            spans.append(" ".join(lw[i:j]))
            i = j
        else:
            i += 1
    if not spans:
        return True, None

    longest = max(len(s.split()) for s in spans)
    quoted = "; ".join(f'"{s}"' for s in spans[:4])
    return False, (
        f"{len(spans)} passage(s) shared with the benchmark letter, which was "
        f"written for a DIFFERENT candidate (longest run {longest} words): "
        f"{quoted}. Check each one: if it is that candidate's story or detail, "
        f"it is fabrication and must go. If it is our own habitual phrasing, "
        f"rewrite it so this letter reads as written for this person."
    )


def _proper_nouns(text: str) -> set:
    """Capitalised words that are NOT sentence-initial: names of projects,
    organisations, programmes, places, people.

    Used to spare a leaked span that is simply a NAME. A judgement can always be
    rewritten in our own words; a proper noun cannot, because it is what the
    thing is called. Sentence-initial words are excluded so "Motivation reads
    circumstantial" does not launder itself into a name.
    """
    out = set()
    for sentence in re.split(r"[.!?\n]+", text):
        tokens = re.findall(r"[A-Za-z][A-Za-z'\-]*", sentence)
        for idx, tok in enumerate(tokens):
            if idx == 0:
                continue  # sentence-initial capital carries no signal
            if tok[:1].isupper():
                out.add(_fold(tok).strip("'-"))
    return out


# Grief, illness, violence, family crisis. A candidate may tell us these things
# in an interview; that is not permission to retell them back. Ayesha
# 2026-09-15: "preserve the meaning without replaying unnecessary intimate
# details." A warm-bench letter had opened on a father's 25 days in ICU, the
# coma-scale readings, and the outcome named as "0" - and had put it in the
# SUBJECT LINE.
_SENSITIVE_TERMS = [
    r"\bI ?C ?U\b", r"\bintensive care\b", r"\bcoma\b", r"\bh(a)?emorrhage\b",
    r"\bbrain h(a)?emorrhage\b", r"\bterminal\b", r"\bcancer\b", r"\bchemo\w*",
    r"\bpassed away\b", r"\bdeath\b", r"\bdied\b", r"\bdying\b", r"\bfuneral\b",
    r"\bburial\b", r"\bwidow(er)?\b", r"\borphan\w*", r"\bshot and killed\b",
    r"\bmurder\w*", r"\bkilled\b", r"\bsuicide\b", r"\bmiscarriage\b",
    r"\bdivorce\b", r"\bbereave\w*", r"\bgrief\b", r"\bgrieving\b",
    r"\bhospitali[sz]ed\b", r"\blife support\b", r"\bdeathbed\b", r"\bbedside\b",
]


# A SECOND, HARDER LIST. Material that does not belong in a hiring letter AT
# ALL - not softened, not abstracted, ABSENT. A WARNING was not enough: a
# warm-bench draft was flagged for "an office boy at Jamshoro was killed ...
# the death benefit for his widow" and shipped it anyway, and closed its P.S.
# on the candidate having started THERAPY that year. A candidate discloses
# these things to build trust in an interview. Repeating them in a rejection,
# which may be forwarded or screenshotted, breaks that trust whatever the
# intent. Reference the BEHAVIOUR instead ("you fought your own organisation so
# a colleague's family got what they were owed") and leave the tragedy and the
# diagnosis out of it.

# Never, in any context: these name a specific death or its aftermath.
_NEVER_ANY = [
    r"\bshot (and|then) killed\b", r"\bmurder\w*", r"\bsuicide\b",
    r"\bfuneral\b", r"\bburial\b", r"\bdeathbed\b",
    r"\bwidow(er)?\b", r"\borphan\w*", r"\bdeath benefit\b",
    r"\bmiscarriage\b",
]

# Health and care. These are ALSO ordinary professional vocabulary - Taleemabad
# hires people who run counselling services and mental-health programmes - so a
# bare match is not enough. It counts only when the candidate is DISCLOSING
# their own care, not describing their work. Without this split the rule fired
# on 8 of the 103 sent letters, every one of them about somebody's profession.
_NEVER_PERSONAL_HEALTH = [
    r"\btherap(y|ist)\b", r"\bcounsell?ing\b", r"\bmental health\b",
    r"\bdepress(ion|ed)\b", r"\bpsychiatr\w*", r"\bdiagnos(is|ed)\b",
    r"\bmedication\b", r"\bchemo\w*", r"\bcancer\b",
    r"\bI ?C ?U\b", r"\bintensive care\b", r"\bcoma\b",
    r"\bh(a)?emorrhage\b", r"\blife support\b", r"\bterminal(ly)? ill\w*",
]

# The candidate telling us about their own care, rather than their work.
_DISCLOSURE_VERB = re.compile(
    r"\b(described|shared|told us|disclos\w*|opened|opening|started|starting|"
    r"began|beginning|sought|seeking|went to|going to|attending|undergoing|"
    r"receiving|your own|his own|her own)\b", re.IGNORECASE)

# A field of work, not a disclosure: "counselling notes", "mental health team".
_WORK_NOUN = re.compile(
    r"^\W{0,3}(notes|programme|program|service|services|sessions|practice|"
    r"department|team|experience|background|work|role|initiative|curriculum|"
    r"training|caseload|clients|support|chapter|sector)\b", re.IGNORECASE)

# A sector prefix: "education counselling", "career counselling".
_WORK_DOMAIN = re.compile(
    r"(education|career|school|academic|student|admissions|guidance|community)"
    r"\W{0,3}$", re.IGNORECASE)


def check_never_in_a_letter(text: str, subject: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """Material that must be ABSENT from a candidate letter, not merely softened."""
    if email_type not in _COACHING_CHECKED_TYPES:
        return True, None
    hay = (subject or "") + " " + _letter_prose(text, email_type)
    found: List[str] = []
    for pat in _NEVER_ANY:
        for m in re.finditer(pat, hay, re.IGNORECASE):
            if m.group(0).lower() not in found:
                found.append(m.group(0).lower())
    for pat in _NEVER_PERSONAL_HEALTH:
        for m in re.finditer(pat, hay, re.IGNORECASE):
            before = hay[max(0, m.start() - 70):m.start()]
            after = hay[m.end():m.end() + 30]
            if _WORK_NOUN.match(after) or _WORK_DOMAIN.search(before):
                continue  # their profession, not their private life
            if _DISCLOSURE_VERB.search(before) and m.group(0).lower() not in found:
                found.append(m.group(0).lower())
    if not found:
        return True, None
    return False, (
        "This letter repeats something the candidate disclosed in confidence: "
        + ", ".join(found[:8]) + ". A bereavement, a violent death, or a medical "
        "or mental-health disclosure has no place in a hiring decision letter, "
        "which may be forwarded or screenshotted. Do NOT soften it, REMOVE it. "
        "Say what they DID instead: \"you fought your own organisation so a "
        "colleague's family got what they were owed\". Never close a P.S. on it."
    )


def _sensitive_hits(text: str) -> List[str]:
    found = []
    for pat in _SENSITIVE_TERMS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            phrase = m.group(0).lower()
            if phrase not in found:
                found.append(phrase)
    return found


def check_sensitive_subject(subject: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """A bereavement, illness or act of violence must NEVER be the subject line.

    The subject is what shows in an inbox, on a phone lock screen, in a
    forwarded thread. "The 25 Days That Teach You What Matters" was drawn from
    a candidate's father dying in intensive care. Whatever the intent, it turns
    someone's grief into a headline about our hiring process.
    """
    if not subject or email_type not in _COACHING_CHECKED_TYPES:
        return True, None
    hits = _sensitive_hits(subject)
    if not hits:
        return True, None
    return False, (
        f'The subject line draws on something sensitive: {", ".join(hits)}. '
        f'A bereavement, illness, act of violence or family crisis must never be '
        f'the headline of a rejection email: it is what shows on a lock screen '
        f'and in a forwarded thread. Choose a subject from their WORK.'
    )


def check_sensitive_detail(text: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """Sensitive personal material in the body: keep the meaning, drop the detail.

    A WARNING, never a block. Sometimes the moment genuinely belongs in the
    letter, and only a human can judge whether it is being honoured or replayed.
    """
    if email_type not in _COACHING_CHECKED_TYPES:
        return True, None
    hits = _sensitive_hits(_letter_prose(text, email_type))
    if not hits:
        return True, None
    return False, (
        f'This letter retells something sensitive: {", ".join(hits[:8])}. Keep '
        f'what it MEANT (that they did not step away from something hard) and cut '
        f'the intimate particulars: clinical detail, sums of money, how someone '
        f'died. They told us in confidence in an interview; that is not permission '
        f'to narrate it back to them.'
    )


def check_scorecard_leakage(
    text: str, email_type: str, scorecard_text: Optional[str]
) -> Tuple[bool, Optional[str]]:
    """EVERY phrase lifted from the hiring manager's scorecard into the letter.

    Returns (True, None) when no scorecard text is supplied, so callers without
    one are never blocked by an absence.

    ALL matches, never the first. Reporting one leak at a time made the retry
    loop diverge instead of converge: the drafter was told about
    "one government adjacent example", rewrote that one sentence, and attempt 2
    came back leaking "remote night shift job" instead. Three attempts, three
    different phrases, three hard blocks in front of Ayesha. A letter drafted
    FROM the scorecard echoes it in several places at once, so the drafter and
    the review pass have to see the whole set or they play whack-a-mole. This is
    the same mistake check_tone_categories already fixed by listing every match.

    Overlapping n-grams are merged into the longest contiguous span, so the
    report reads as the phrase a human would recognise rather than as sliding
    four-word windows of the same sentence.
    """
    if not scorecard_text or email_type not in _COACHING_CHECKED_TYPES:
        return True, None

    proper = _proper_nouns(scorecard_text)
    letter_words = _content_words(_letter_prose(text, email_type))
    if len(letter_words) < _LEAK_NGRAM:
        return True, None

    sc_words = _content_words(scorecard_text)
    sc_grams = {
        " ".join(sc_words[i:i + _LEAK_NGRAM])
        for i in range(len(sc_words) - _LEAK_NGRAM + 1)
    }
    if not sc_grams:
        return True, None

    # Mark every letter position covered by a lifted n-gram, then read off the
    # maximal runs. Marking by POSITION (not by gram) is what merges the
    # overlaps: a seven-word lift marks one run of seven, not four separate hits.
    n = len(letter_words)
    lifted = [False] * n
    for i in range(n - _LEAK_NGRAM + 1):
        if " ".join(letter_words[i:i + _LEAK_NGRAM]) in sc_grams:
            for j in range(i, i + _LEAK_NGRAM):
                lifted[j] = True

    spans: List[str] = []
    i = 0
    while i < n:
        if lifted[i]:
            j = i
            while j < n and lifted[j]:
                j += 1
            span = letter_words[i:j]
            # A NAME is not the manager's private wording, it is a fact. "Punjab
            # Startup Portal feasibility" blocked a warm-bench letter for naming
            # the candidate's OWN project, which is exactly the specificity these
            # letters need. There is no warmer way to say a proper noun: you can
            # rewrite a judgement, you cannot rewrite what something is called.
            named = sum(1 for w in span if w in proper)
            if not (named >= 2 and named / len(span) >= 0.6):
                spans.append(" ".join(span))
            i = j
        else:
            i += 1

    if not spans:
        return True, None

    quoted = ", ".join(f'"{p}"' for p in spans)
    plural = "phrases" if len(spans) > 1 else "phrase"
    return False, (
        f'Scorecard wording carried into the letter ({len(spans)} {plural}): '
        f'{quoted}. The scorecard is internal shorthand written at speed for '
        f'colleagues; the letter is candidate-facing and may be forwarded or '
        f'posted. Rewrite EVERY one of these in your own warm words: say what '
        f'WE needed and could not establish, never the assessment itself.'
    )


def _letter_prose(text: str, email_type: Optional[str] = None) -> str:
    """The words a HUMAN WROTE. Strips our own furniture before any tone scan.

    Three pieces of every rendered email are template output, not authored prose:
      - the canonical section headings (rendering.render_body prints them),
      - the in-email feedback widget, whose button labels include the literal
        string "No, felt generic",
      - the signature/footer block.

    Scanning them produced phantom violations on EVERY webapp-rendered letter.
    The 103-letter corpus used to calibrate these rules carries no widget, so
    the false positive never showed up in measurement while real drafts kept
    failing on it (application 3869).
    """
    clean = strip_html(text)
    # Feedback widget: from its heading to the end of the useful-buttons row.
    clean = re.sub(r"Be honest\. We can take it\..*?(Not really|Was the feedback useful\?)",
                   " ", clean, flags=re.DOTALL | re.IGNORECASE)
    # Signature / footer.
    clean = re.sub(r"Warm regards,.*$", " ", clean, flags=re.DOTALL | re.IGNORECASE)
    return _without_headings(clean, email_type)


def check_tone_categories(text: str, email_type: str) -> List[Tuple[str, str, List[str]]]:
    """Every tone violation, grouped by the BEHAVIOUR it represents.

    Returns [(category, human label, [phrases]), ...]. Reporting one combined
    "coaching" verdict made it impossible to tell whether a letter was coaching,
    grading an answer, or judging the person, and impossible to tell whether a
    fix had landed. REPORT_EVIDENCE only applies to the interview-stage letters,
    where replaying a question is the risk; a cv_rejection has its own
    application-replay rule.
    """
    if email_type not in _COACHING_CHECKED_TYPES:
        return []
    clean = _letter_prose(text, email_type)
    out = []
    for category, patterns in COACHING_CATEGORIES.items():
        if category == "REPORT_EVIDENCE" and email_type == "cv_rejection":
            continue
        hits, seen = [], set()
        for pattern in patterns:
            for m in re.finditer(pattern, clean, re.IGNORECASE):
                phrase = m.group().strip()
                if phrase.lower() not in seen:
                    seen.add(phrase.lower())
                    hits.append(phrase)
        if hits:
            out.append((category, COACHING_CATEGORY_LABELS[category], hits))
    return out


def check_coaching_register(text: str, email_type: str) -> Tuple[bool, Optional[str]]:
    """Back-compat single verdict across every tone category."""
    found = check_tone_categories(text, email_type)
    if not found:
        return True, None
    parts = ["%s: %s" % (label, ", ".join('"%s"' % h for h in hits[:6]))
             for _, label, hits in found]
    return False, "; ".join(parts)


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


def _strip_quoted_spans(text: str) -> str:
    """Blank out anything inside quotation marks.

    The rule is that WE speak as "we", never as one person. It was never about
    the CANDIDATE's own words. A warm-bench letter quotes their interview
    verbatim, so their "I" and "my" are correct and must survive:
        You told us the truth: "It was a little difficult initially, since that
        was my child idea."
    Flagging that (application 3869, Muneeb) blocked a letter for quoting the
    person it was written to.

    Single quotes only count when they open after whitespace and close before
    punctuation or whitespace, so contractions like "didn't" are left alone.
    """
    text = re.sub(r'"[^"]{0,400}"', ' ', text)
    text = re.sub(r'[“][^”]{0,400}[”]', ' ', text)
    text = re.sub(r"(?<=\s)'[^']{0,400}'(?=[\s.,;:!?)]|$)", ' ', text)
    text = re.sub(r"(?<=\s)[‘][^’]{0,400}[’](?=[\s.,;:!?)]|$)", ' ', text)
    return text


def check_first_person_singular(text: str) -> Tuple[bool, Optional[str]]:
    """The email must use the collective 'we' voice, never first-person singular.
    A decision from Taleemabad is 'we', not one person's 'I'.

    Quoted spans are exempt: they are the candidate speaking, not us."""
    clean = _strip_quoted_spans(strip_html(text))
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
    # Generic professional vocabulary, measured as the dominant source of false
    # flags across the 98 Job-42 letters: "crm" alone accounted for 25. None of
    # these is a claim ABOUT a person; they are the words any hiring letter uses.
    "crm", "erp", "ats", "kpi", "kpis", "roi", "seo", "sem", "saas", "b2b", "b2c",
    "ngo", "ngos", "sql", "api", "apis", "hr", "it", "ui", "ux", "ai", "ml",
    "pkr", "usd", "gbp", "eur", "rs",
    "bachelor", "bachelors", "master", "masters", "mphil", "phd", "mba", "bsc",
    "msc", "ba", "bs", "ms", "diploma", "degree", "university", "college",
    "commission", "ministry", "federal", "provincial", "government", "public",
    "private", "sector", "cloud", "digital", "mobile", "web", "online",
    "higher", "lower", "senior", "junior", "mid", "entry", "cvs", "resume",
    "focused", "driven", "based", "led", "run", "max", "min",
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
    # "What Stayed With Us" section vs "Here's the Honest Part" section
    stayed_section = re.search(
        r"What Stayed With Us.*?(?=Here's the Honest Part|$)",
        clean,
        re.IGNORECASE | re.DOTALL
    )
    honest_section = re.search(
        r"Here's the Honest Part.*?(?=Where We Want to Leave|$)",
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

# ---------------------------------------------------------------------------
# ONE SOURCE OF TRUTH FOR WHAT BLOCKS A LETTER
#
# Ayesha 2026-09-15: "putting hard blocks is not the only solution, you need to
# FOLLOW those hard blocks." She is right, and the drift was structural: the
# harness knew 16 blocking rules while the drafting prompt carried a
# hand-written subset of them. A rule added here never reached the writer, so
# the writer kept breaking rules nobody had told it about.
#
# This list is injected verbatim into the writer and the reviewer, and
# test_hard_block_brief.py fails if a rule is added to the harness without a
# line here. Adding a block without telling the writer is now a test failure.
# ---------------------------------------------------------------------------
HARD_BLOCK_BRIEF = {
    "Mandatory opening line": 'Open with "This is not a yes for now." as the first line after the greeting.',
    "No em dashes": "Never use an em dash. Use a comma or a full stop.",
    "Collective": 'Speak as Taleemabad: "we", "our", "us". Never "I", "my" or "me" outside a quotation of the candidate.',
    "Required section headings": "Use the section headings exactly as given. Do not invent, rename or reorder them.",
    "No intent-word inference": 'Never say what they assumed, believed, thought, preferred, seemed or were energised by. Say what WE could not establish.',
    "No internal jargon": "Never use our internal vocabulary: GWC, KCD, warm bench, right seat, values scorecard.",
    "No interviewer names": "Never name the interviewer or panel member.",
    "No harsh or adversarial language": 'Never call their work a failure, say it went wrong, or argue with them.',
    "No corporate rejection boilerplate": 'Never "we regret to inform you" or "after careful consideration".',
    "Translate the scorecard": "Never reuse the hiring manager's wording. Say it in your own warm words.",
    "Never headline a bereavement or crisis": "The subject line comes from their WORK, never from a loss, illness or crisis.",
    "Never repeat a confidence": "Leave out another person's death, any medical or mental-health disclosure, and any family crisis told as a scene. Say what the candidate DID instead.",
    "Never replay the application back at them": "Never quote their application answers back or point out what they left unanswered.",
    "CV rejection: no fabricated interview": "A CV-stage letter had no conversation. Never imply one happened.",
    "CV rejection: the letter must be built from their application": "Every concrete detail must come from their own CV, cover letter or answers.",
    "PILOT prefix control": "Never write [PILOT] into the subject line yourself.",
    # The six tone behaviours. Keys match COACHING_CATEGORY_LABELS exactly;
    # test_hard_block_brief.py fails if they drift, and it caught three of these
    # on its first run.
    "Coaching": "Never say what to develop, learn, gain, document or demonstrate next time.",
    "Career direction": "Never name which roles, functions or sectors suit them.",
    "Grading their answer": "Never replay a question and assess the answer.",
    "Person-level judgement": "Never characterise the person. PRAISE COUNTS: not 'that's rare', not 'the kind of person', not 'you've proven you can'.",
    "A conditional door": "Never make a welcome back conditional on them fixing the gap. That is homework.",
    "Replaying interview evidence": "Never list what they failed to demonstrate. One sentence about what we could not establish, then stop.",
    "Private-note leakage": "Never let the hiring manager's private wording reach the candidate.",
}


def writer_hard_blocks(email_type: str) -> str:
    """The blocking rules, as the writer must be told them."""
    skip_cv = () if email_type == "cv_rejection" else ("CV rejection:",)
    lines = []
    for name, brief in HARD_BLOCK_BRIEF.items():
        if any(name.startswith(p) for p in skip_cv):
            continue
        lines.append(" - %s: %s" % (name, brief))
    return "\n".join(lines)


def evaluate_email(
    html_body: str,
    subject: str,
    email_type: str,
    pilot_mode: bool = True,
    cv_corpus: Optional[str] = None,
    candidate_name: str = "",
    role: str = "",
    scorecard_text: Optional[str] = None,
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

    # 1b. Word count CEILING (Ayesha 2026-09-15). A letter earns its length by
    # being specific about what mattered to the DECISION, not by retelling every
    # story in the scorecard. WARNING rather than HARD_BLOCK so an already
    # approved letter is never stranded; the drafting prompt targets 700-800.
    maximum = WORD_MAXIMUMS.get(email_type)
    if maximum and actual > maximum:
        violations.append({
            'rule': f'Over the {maximum}-word ceiling',
            'severity': 'WARNING',
            'detail': (
                f'{actual} words against a {maximum}-word ceiling. Personalisation '
                f'is selective, not exhaustive: keep the evidence that explains what '
                f'stayed with us or why the decision landed where it did, and cut '
                f'what is in the letter only because it came up in the interview. '
                f'If the decision turned on ONE role-fit gap, do not carry secondary '
                f'concerns alongside it.'
            ),
        })

    # 1c. Material that must be ABSENT, not softened (Ayesha 2026-09-15, second
    # pass). A WARNING was not enough: a draft was flagged for a colleague's
    # killing and shipped it anyway, and closed its P.S. on the candidate's
    # therapy. This one blocks.
    passed, detail = check_never_in_a_letter(html_body, subject, email_type)
    if not passed:
        violations.append({
            'rule': 'Never repeat a confidence: grief, violence, health',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # 1d. Sensitive personal material (Ayesha 2026-09-15).
    passed, detail = check_sensitive_subject(subject, email_type)
    if not passed:
        violations.append({
            'rule': 'Never headline a bereavement or crisis',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })
    passed, detail = check_sensitive_detail(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Sensitive story: keep the meaning, cut the detail',
            'severity': 'WARNING',
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

    # 7c2. Never replay the application back at the candidate. HARD BLOCK
    #      (Ayesha 2026-09-14). Shipped first as a WARNING, which let a live
    #      draft quote a candidate's answer of 'NAAAAA' back at them inside a
    #      rejection. "Passes checks" has to mean the letter is sendable.
    passed, detail = check_application_replay(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Never replay the application back at them',
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

    # Scorecard wording lifted into a candidate-facing letter (Ayesha 2026-09-14)
    passed, detail = check_scorecard_leakage(html_body, email_type, scorecard_text)
    if not passed:
        violations.append({
            'rule': 'Translate the scorecard, never repeat it',
            'severity': 'HARD_BLOCK',
            'detail': detail,
        })

    # Passages shared with the APPROVED benchmark letter, which belongs to a
    # different candidate. WARNING: a human tells reuse from resemblance.
    passed, detail = check_benchmark_echo(html_body, email_type)
    if not passed:
        violations.append({
            'rule': 'Shared wording with the benchmark letter',
            'severity': 'WARNING',
            'detail': detail,
        })

    # One HARD BLOCK per BEHAVIOUR, named, listing every phrase (2026-09-14).
    for _category, label, hits in check_tone_categories(html_body, email_type):
        listed = ", ".join('"%s"' % h for h in hits[:8])
        more = " (+%d more)" % (len(hits) - 8) if len(hits) > 8 else ""
        violations.append({
            'rule': label,
            'severity': 'HARD_BLOCK',
            'detail': (f'{len(hits)} phrase(s) to rewrite: {listed}{more}. Explain OUR '
                       f'decision and what we could not establish; do not tell the '
                       f'candidate what to do, judge who they are, or grade an answer.'),
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
        # The UI hardcoded "/ 800" and so showed "480 / 800" on a CV rejection
        # whose real floor is 350. Report the minimum that was actually applied.
        'word_minimum': minimum,
        'violations': violations,
    }


if __name__ == '__main__':
    # Test: standalone usage (for debugging)
    test_html = """
    <h2>What Stayed With Us</h2>
    <p>This is a test paragraph with good observation.</p>
    <h2>Here's the Honest Part</h2>
    <p>This is where we discuss the gap.</p>
    <h2>Where We Want to Leave This</h2>
    <p>Final thoughts.</p>
    """

    result = evaluate_email(test_html, "Test Subject", "warm_bench", pilot_mode=True)
    print("Test result:", result)
