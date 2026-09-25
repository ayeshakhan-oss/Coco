"""Passive candidate sourcing: the pool, the outreach state, and the Markaz gate.

SOURCE OF TRUTH: .claude/skills/05_talent-sourcing/SKILL.md and
memory/talent_sourcing_workflow_locked_2026_06_04.md.

WHAT THIS DOES AND DOES NOT DO. The skill's 3-layer web search stays in Claude
Code: it drives a LOCAL headless Chrome against a public SearXNG instance that
answers an anti-bot proof-of-work, and the built-in web search is effectively
blind to Pakistani LinkedIn
(memory/sourcing_fundraising_partnerships_2026_09_08.md). Running that from a
datacenter IP would be both fragile and rude. Everything downstream of the
search -- the pool, who has been contacted, who replied, and who may be put
into Markaz -- is where the daily work actually is, and that is what lives
here.

🔴 THE CORE RULE, NOW MECHANICAL: Markaz is touched ONLY after confirmed
   interest, never speculatively. It has always been discipline; `may_push_to_markaz`
   makes it a condition the API enforces.

🔴 AN UNVERIFIED PROFILE MUST NEVER LOOK VERIFIED. On 2026-09-08 a subagent
   invented twelve people with plausible `pk.linkedin.com/in/...` slugs, and
   then falsely retracted six real ones. Verification state is therefore a
   first-class column with four values, not a boolean, and:

     * NOT_FOUND IS NOT "FAKE". The verifier produces false negatives -- Savera
       Bokhari came back NOT_FOUND while sitting verbatim in the raw captures.
       Nothing here may delete or hide a row on that basis.
     * Neither an agent's claim NOR its confession is evidence. Both get
       machine-checked, and the state recorded here is the machine's.
"""

from __future__ import annotations

import re
from typing import Iterable, Optional

# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------

#: The claimed profile was independently confirmed.
CONFIRMED = "confirmed"
#: Checked, and the claim did not come back. NOT evidence that the person is
#: invented -- the verifier has known false negatives.
NOT_FOUND = "not_found"
#: Has a URL, not yet checked.
UNCONFIRMED = "unconfirmed"
#: No profile URL at all to check.
NO_URL = "no_url"

VERIFICATION_STATES = (CONFIRMED, UNCONFIRMED, NOT_FOUND, NO_URL)

#: Only a confirmed profile may be described as verified anywhere a person
#: reads. Everything else is shown as what it is.
def is_verified(state: Optional[str]) -> bool:
    return state == CONFIRMED


# --------------------------------------------------------------------------
# Outreach
# --------------------------------------------------------------------------

NOT_CONTACTED = "not_contacted"
CONTACTED = "contacted"
REPLIED_INTERESTED = "replied_interested"
REPLIED_NOT_INTERESTED = "replied_not_interested"
NO_REPLY = "no_reply"

OUTREACH_STATES = (
    NOT_CONTACTED, CONTACTED, REPLIED_INTERESTED, REPLIED_NOT_INTERESTED, NO_REPLY,
)

#: The only state that opens the Markaz gate.
INTERESTED = REPLIED_INTERESTED


class SourcingError(ValueError):
    """The sourcing record does not make sense."""


def validate_states(verification: str, outreach: str) -> None:
    if verification not in VERIFICATION_STATES:
        raise SourcingError(
            f"unknown verification state {verification!r}; must be one of "
            f"{VERIFICATION_STATES}"
        )
    if outreach not in OUTREACH_STATES:
        raise SourcingError(
            f"unknown outreach state {outreach!r}; must be one of {OUTREACH_STATES}"
        )


# --------------------------------------------------------------------------
# The Markaz gate
# --------------------------------------------------------------------------


def may_push_to_markaz(row: dict) -> Optional[str]:
    """Why this person may NOT go into Markaz yet, or None if they may.

    The skill's core rule, made mechanical: "Markaz is ONLY touched after
    confirmed interest. Never speculatively." A sourced person who has not said
    yes is not an applicant, and putting them in the pipeline makes them look
    like one to every report that counts applications.
    """
    if row.get("markaz_application_id"):
        return "already in Markaz"
    if row.get("outreach_state") != INTERESTED:
        return (
            "they have not confirmed interest. Sourcing only enters Markaz after "
            "somebody says yes, never speculatively."
        )
    if not (row.get("name") or "").strip():
        return "no name on record"
    return None


# --------------------------------------------------------------------------
# Tenure: a column that admits it does not know
# --------------------------------------------------------------------------

#: 🔴 NEVER regex the first integer out of a free-text tenure note. The first
#: Band classifier did, and read calendar years as tenure ("8+" because a post
#: was dated 2023) and CONNECTION COUNTS as tenure (Sadaf Gul, "8+" from "26
#: connections"), wrongly promoting two people to Tier 1. Match only on the
#: WORD year or yr, check the hedges FIRST, and default to unknown.
_OVER_CAP = re.compile(r"\b(may exceed|exceeds|above|over)\b.*\bcap\b", re.I)
_HEDGE = re.compile(r"\b(likely|probably|approx|around|maybe|unclear|unverified|\?)", re.I)
_YEARS = re.compile(r"\b(\d{1,2})\s*\+?\s*(?:years?|yrs?|yr)\b", re.I)


def years_from_note(note: Optional[str]) -> Optional[int]:
    """Years of experience, or None when the note does not actually say.

    A column that admits it does not know beats one that quietly invents a
    number.
    """
    text = (note or "").strip()
    if not text:
        return None
    if _OVER_CAP.search(text) or _HEDGE.search(text):
        return None
    match = _YEARS.search(text)
    if not match:
        return None
    value = int(match.group(1))
    # 40 years of experience in a sourcing note is a parse error, not a career.
    return value if 0 < value <= 40 else None


# --------------------------------------------------------------------------
# Identity and duplicates
# --------------------------------------------------------------------------

_SLUG = re.compile(r"linkedin\.com/in/([^/?#\s]+)", re.I)


def linkedin_slug(url: Optional[str]) -> Optional[str]:
    """The identifying part of a LinkedIn URL, lowercased.

    Country subdomains vary for the same person (`pk.linkedin.com`,
    `www.linkedin.com`), so the slug is what identifies them, never the whole
    URL.
    """
    match = _SLUG.search(url or "")
    if not match:
        return None
    return match.group(1).strip().lower().rstrip("/")


def identity_key(row: dict) -> str:
    """What makes two rows the same person.

    The slug when there is one, otherwise name plus organisation. Two people
    with the same name at different organisations are different people, and
    collapsing them loses one.
    """
    slug = linkedin_slug(row.get("linkedin_url"))
    if slug:
        return f"slug:{slug}"
    name = " ".join((row.get("name") or "").split()).lower()
    org = " ".join((row.get("organization") or "").split()).lower()
    return f"name:{name}|{org}"


def find_duplicates(rows: Iterable[dict]) -> dict[str, list]:
    """Identity keys that appear more than once, with the rows that share them."""
    seen: dict[str, list] = {}
    for row in rows:
        seen.setdefault(identity_key(row), []).append(row)
    return {k: v for k, v in seen.items() if len(v) > 1}


# --------------------------------------------------------------------------
# Pool summary
# --------------------------------------------------------------------------


def summarise(rows: Iterable[dict]) -> dict:
    """Counts a reader can act on, with the unverified never folded into the
    verified."""
    rows = list(rows)
    by_verification = {s: 0 for s in VERIFICATION_STATES}
    by_outreach = {s: 0 for s in OUTREACH_STATES}
    for r in rows:
        by_verification[r.get("verification_state", UNCONFIRMED)] = (
            by_verification.get(r.get("verification_state", UNCONFIRMED), 0) + 1
        )
        by_outreach[r.get("outreach_state", NOT_CONTACTED)] = (
            by_outreach.get(r.get("outreach_state", NOT_CONTACTED), 0) + 1
        )
    ready = [r for r in rows if may_push_to_markaz(r) is None]
    return {
        "total": len(rows),
        "verification": by_verification,
        "outreach": by_outreach,
        "in_markaz": sum(1 for r in rows if r.get("markaz_application_id")),
        "ready_for_markaz": len(ready),
        "caveat": (
            f"{by_verification[NOT_FOUND]} profiles came back NOT FOUND. That is "
            "not evidence they are invented: the verifier has known false "
            "negatives, and a real person has been marked not-found before."
        ),
    }
