"""Filling a contract from what we already know, and saying where each bit came from.

Ayesha's ask: name the person and the job, and have the contract drafted,
rather than retyping a CNIC and a salary that already exist somewhere.

WHERE EACH THING COMES FROM, and none of it is guessed:

  Markaz, `applications.contract_drafting_*`, written by the onboarding form
  the candidate fills in themselves:
    - the FULL LEGAL NAME they typed
    - their CNIC
  Markaz, `jobs`:
    - the position
  Today:
    - the current date on the contract
  The offer letter thread in the mailbox (`offer_evidence`):
    - the compensation, the start date and the end date

🔴 THE LEGAL NAME BEATS THE MARKAZ NAME, ALWAYS. On the 17 people who have
   submitted the form, EIGHT typed a legal name different from the one stored
   against their application: Marzia Hasnain is Marzia Hasnain Khandwala,
   Raheela is Bibi Raheela, Muzzamil Patel is Muhammad Muzzammil Patel. A
   contract carries the legal name. This is CLAUDE.md Rule 22 with a second
   source that is better than both the display name and the CV filename,
   because the person typed it themselves for this exact purpose.

🔴 A PROPOSAL IS NOT A DECISION. Every value carries `source`, and anything
   read out of an email carries the message it came from. The salary in
   particular is a proposal: Mariam and Hafiza both countered and the agreed
   figure was not the one in the first offer letter.

🔴 NOTHING IS INVENTED. A field with no source is left empty with `source`
   set to null, so the page shows a blank box rather than a plausible value
   nobody can trace.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Optional

from . import contracts as spec

# --------------------------------------------------------------------------
# Matching a discovered field to something we know
# --------------------------------------------------------------------------

#: What a placeholder means, recognised from its own text. The masters label
#: most of their fields ("EMPLOYEE'S CNIC", "CURRENT DATE"), so this reads the
#: document rather than assuming a fixed order.
_MEANING = (
    ("cnic", re.compile(r"\bcnic\b|\bnic\b|identity\s*(card|no)", re.I)),
    # 🔴 EMPLOYER BEFORE EMPLOYEE, AND THE ORDER IS THE WHOLE POINT. The NIETE
    #    master has a field literally called "EMPLOYER NAME DESIGNATION", which
    #    a plain `\bname\b` rule matched as the employee's name and filled with
    #    the CANDIDATE's name, into the signature block where the signing
    #    officer belongs. Caught on the real master, not in theory.
    ("employer", re.compile(r"\bemployer\b", re.I)),
    ("legal_name", re.compile(
        r"employee.?s?\s*name|fellow\s*name|\bname\b", re.I)),
    ("current_date", re.compile(r"current\s*date|^date$", re.I)),
    ("start_date", re.compile(
        r"joining|effective\s*date|commenc|start", re.I)),
    ("employer", re.compile(r"employer\s*name|designation.*employer", re.I)),
    ("direct_report", re.compile(r"direct\s*report|reports?\s*to|line\s*manager", re.I)),
    ("position", re.compile(r"\bposition\b|\bdesignation\b(?!.*employer)|\brole\b", re.I)),
)


#: Checked against the TAIL of the words before a field, because the word that
#: says what a date is sits immediately in front of it. The NIETE term reads
#: "for the duration of this Contract i.e., from <A> to <B>": both fields are
#: written "DATE, MONTH, YEAR", and only "from" and "to" tell them apart.
#: Matching anywhere in the preceding text would find "from" in both.
_TAIL_MEANING = (
    # 🔴 THE MONEY LINES FIRST, and they fill the NUMBER only. The master
    #    already prints "PKR" before the field, so writing "PKR 108,000" into
    #    it produces "Total Earnings PKR PKR 108,000" on a real contract.
    ("total_pay", re.compile(
        r"total\s+earnings?\s*:?\s*(pkr|rs\.?)?\s*$", re.I)),
    ("base_pay", re.compile(
        r"\b(base|basic)\s+salary\s*:?\s*(pkr|rs\.?)?\s*$", re.I)),
    ("medical_pay", re.compile(r"\bmedical\s*:?\s*(pkr|rs\.?)?\s*$", re.I)),
    ("other_pay", re.compile(r"\bothers?\s*:?\s*(pkr|rs\.?)?\s*$", re.I)),
    ("end_date", re.compile(r"\b(to|until|till|through|ending)\s*[:,]?\s*$", re.I)),
    ("duration", re.compile(r"\bduration\s+of\s*$", re.I)),
    ("cnic", re.compile(r"\bcnic\s*(no\.?|#|number)?\s*[:.]?\s*$", re.I)),
    # "will join Orenda <date>" puts the employer between the verb and the
    # field, so the cue is not the last word. Named explicitly rather than
    # loosening the pattern, which would start matching ordinary nouns.
    ("start_date", re.compile(
        r"\b(from|join|joins|joining|commencing|commences|effective|"
        r"starting|on|join\s+orenda)\s*[:,]?\s*$", re.I)),
)


def meaning_from_context(before: str) -> Optional[str]:
    """What the words running up to a field say it is.

    The tail is checked first and on its own: it carries the preposition, and
    a match anywhere in the wider text picks the wrong one.
    """
    text = (before or "").strip()
    if not text:
        return None
    tail = text[-28:]
    for name, pattern in _TAIL_MEANING:
        if pattern.search(tail):
            return name
    return meaning_of(text)


def meaning_of(placeholder: str) -> Optional[str]:
    """What a field is for, or None when the placeholder does not say.

    A bare "XYZ" returns None on purpose. In the NIETE contract the same XYZ
    is a duration in one sentence and a CNIC in another, so guessing puts a
    national ID number where a contract term belongs.
    """
    text = (placeholder or "").strip()
    if spec.is_opaque(text):
        return None
    for name, pattern in _MEANING:
        if pattern.search(text):
            return name
    return None


def _pretty_date(value) -> str:
    """"1st October 2026". Never names the weekday (joining-emails rule 3)."""
    if isinstance(value, str):
        try:
            value = dt.date.fromisoformat(value)
        except ValueError:
            return value
    suffix = (
        "th" if 11 <= value.day <= 13
        else {1: "st", 2: "nd", 3: "rd"}.get(value.day % 10, "th")
    )
    return f"{value.day}{suffix} {value:%B} {value.year}"


def build_prefill(
    *,
    groups: list[dict],
    markaz: dict,
    offer: Optional[dict] = None,
    today: Optional[dt.date] = None,
) -> dict:
    """{field key: {value, source}} for the fields we can actually fill.

    `markaz` is the application row; `offer` is `offer_evidence.read_thread`.
    """
    today = today or dt.date.today()
    known: dict[str, dict] = {}

    legal = (markaz.get("legal_name") or "").strip()
    stored = (markaz.get("markaz_name") or "").strip()
    if legal:
        known["legal_name"] = {
            "value": legal,
            "source": (
                "the onboarding form they filled in themselves"
                + (f", which differs from the name stored in Markaz ({stored})"
                   if stored and stored.lower() != legal.lower() else "")
            ),
        }
    elif stored:
        known["legal_name"] = {
            "value": stored,
            "source": "Markaz. They have NOT submitted the onboarding form, so "
                      "this is the stored name, not a legal name they confirmed.",
        }

    if markaz.get("cnic"):
        known["cnic"] = {
            "value": markaz["cnic"],
            "source": "the onboarding form they filled in themselves",
        }
    if markaz.get("position"):
        known["position"] = {"value": markaz["position"], "source": "the job in Markaz"}
    if markaz.get("hiring_manager"):
        known["direct_report"] = {
            "value": markaz["hiring_manager"],
            "source": "the hiring manager on the job in Markaz. Check it is who "
                      "they actually report to.",
        }
    known["current_date"] = {"value": _pretty_date(today), "source": "today"}

    if offer:
        proposed = offer.get("proposed") or {}
        for key, field in (("start_date", "start_date"), ("end_date", "end_date")):
            item = proposed.get(key)
            if item:
                known[field] = {
                    "value": _pretty_date(item["date"]),
                    "source": f"the offer email of {item['source']['date'][:10]}",
                }
        # The duration is derived from the term, never read as its own figure:
        # a contract whose duration disagrees with its own dates is worse than
        # one with the duration left blank.
        start, end = proposed.get("start_date"), proposed.get("end_date")
        if start and end:
            known["duration"] = {
                "value": f"{_pretty_date(start['date'])} to {_pretty_date(end['date'])}",
                "source": "worked out from the start and end dates, so it cannot "
                          "disagree with them",
            }
        total = proposed.get("total") or proposed.get("stipend")
        if total:
            known["compensation"] = {
                "value": total["text"],
                "source": f"the offer email of {total['source']['date'][:10]}",
            }
        # The bare number, for the fields that already print "PKR" in front.
        for meaning, key in (("total_pay", "total"), ("base_pay", "base"),
                             ("medical_pay", "medical"), ("other_pay", "other")):
            item = proposed.get(key) or (
                proposed.get("stipend") if key == "total" else None)
            if item:
                known[meaning] = {
                    "value": f"{item['amount']:,}",
                    "source": (
                        f"the offer email of {item['source']['date'][:10]}. A "
                        "salary is the field most worth checking: candidates "
                        "counter, and the first offer is not always what was "
                        "agreed."
                    ),
                }

    # Map what we know onto the actual fields this master asks for.
    values: dict[str, str] = {}
    sources: dict[str, str] = {}
    for group in groups:
        what = meaning_of(group["placeholder"])
        inferred = False
        if what is None:
            # 🔴 THE SENTENCE, NOT A GUESS. An opaque "X Y Z" says nothing, but
            #    the words running up to it often do: "bearing CNIC No: X Y Z"
            #    and "will join Orenda <date>". That is reading the document.
            #    The salary lines have nothing before them at all and stay
            #    blank, which is correct: a figure nobody stated is not ours
            #    to supply.
            what = meaning_from_context(group.get("before") or "")
            inferred = what is not None
        if what and what in known:
            values[group["key"]] = known[what]["value"]
            source = known[what]["source"]
            if inferred:
                source = (
                    f"{source}. This field is unlabelled in the master; it was "
                    f"matched from the words before it "
                    f"({group.get('before', '')[-40:].strip()!r})."
                )
            sources[group["key"]] = source

    filled = len(values)
    return {
        "values": values,
        "sources": sources,
        "filled": filled,
        "total_fields": len(groups),
        "still_needed": [g["key"] for g in groups if g["key"] not in values],
        "warnings": list((offer or {}).get("warnings") or []),
        # Said every time. The salary is the field most likely to be wrong and
        # the most expensive to get wrong.
        "caveat": (
            "Everything here is a proposal with a source, not a decision. Check "
            "the salary and the dates against what was actually agreed before "
            "building."
        ),
    }
