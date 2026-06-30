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

# Section headings by email type
SECTION_HEADINGS = {
    'warm_bench': {
        'required': [
            'What Stayed With Us',
            "Here's the Honest Part",
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
            "Here's the Honest Part",
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

    missing = []
    for heading in required:
        # Case-insensitive search
        if not re.search(re.escape(heading), clean, re.IGNORECASE):
            missing.append(heading)

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
    first_heading_idx = None
    for heading in required:
        m = re.search(re.escape(heading), clean, re.IGNORECASE)
        if m and (first_heading_idx is None or m.start() < first_heading_idx):
            first_heading_idx = m.start()

    if first_heading_idx is not None and phrase_idx > first_heading_idx:
        detail = (f'Opening line "{REQUIRED_OPENING_LINE}" must appear before the '
                  f'first section heading (right after the salutation), not buried '
                  f'in a later section.')
        return False, detail

    return True, None


def check_jargon(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check for internal jargon (GWC, KCD, warm bench, values scorecard, case study).
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

def evaluate_email(
    html_body: str,
    subject: str,
    email_type: str,
    pilot_mode: bool = True,
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
    passed, actual, detail = check_word_count(html_body, min_count=800)
    if not passed:
        violations.append({
            'rule': 'Word count minimum (800)',
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

    # 6. Jargon
    passed, detail = check_jargon(html_body)
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
    <h2>Here's the Honest Part</h2>
    <p>This is where we discuss the gap.</p>
    <h2>Where We Want to Leave This</h2>
    <p>Final thoughts.</p>
    """

    result = evaluate_email(test_html, "Test Subject", "warm_bench", pilot_mode=True)
    print("Test result:", result)
