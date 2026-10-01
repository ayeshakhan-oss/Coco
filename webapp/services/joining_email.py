"""The joining email: locked wording, Design 3 layout, PDF attachments.

SOURCE OF TRUTH FOR THE WORDING:
.claude/skills/07_contract-drafting/joining-emails.md — five locked
situations, given verbatim by Ayesha. Three more (Part-Time, Addendum,
Internal team-move) have no template yet and are REFUSED rather than invented.

SOURCE OF TRUTH FOR THE LAYOUT: CLAUDE.md Rule 15. `templates/
niete_joining_design3.html` and `templates/permanent_joining_design3.html`.
Design is not content: the layout is fixed and the wording comes from the
skill file.

🔴 THE PACKAGE RULE OVERRIDES EVERYTHING. A volunteer Fellow receives the NDA
   and NOTHING else. Sending an unpaid person an employment contract creates
   an obligation nobody agreed to, and it is a hard error, not a preference.

🔴 ATTACHMENTS ARE PDF, NEVER .docx (joining-emails rule 10, harness-blocked).
   `attachments_ok` refuses a Word attachment outright.

🔴 THE PILOT IS BYTE-IDENTICAL TO THE LIVE EMAIL (rule 5). No banner, no "this
   has not gone to anyone" note, no open questions inside the body. Those
   belong in chat. A pilot that differs from the live send proves nothing
   about the live send.

🔴 NEVER NAME THE WEEKDAY IN A DATE (rule 3, Ayesha 2026-08-13). "1st of
   August 2026", never "Saturday, 1st of August 2026".

🔴 BOLD WHAT THE CANDIDATE ACTS ON (rule 4): the joining date, the
   compensation figure, the duration.
"""

from __future__ import annotations

import html as _html
import os
import re
from typing import Optional

from . import contracts as spec

TEMPLATE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "templates")
)

# --------------------------------------------------------------------------
# The five locked situations
# --------------------------------------------------------------------------

#: engagement -> how the joining email is written for it. `template` is the
#: Design 3 file; `subject` and the prose come from joining-emails.md.
SITUATIONS: dict[str, dict] = {
    spec.PAID_FELLOW: {
        "label": "Paid Fellowship",
        "template": "niete_joining_design3.html",
        "subject": "Welcome to Taleemabad - {role} Fellow",
        "attachments": "Contract and Non-Disclosure Agreement (NDA)",
        "project": "Fellowship",
    },
    spec.VOLUNTEER_FELLOW: {
        "label": "Volunteer Fellowship",
        "template": "niete_joining_design3.html",
        "subject": "Welcome to Taleemabad - {role} Fellow",
        "attachments": "Non-Disclosure Agreement (NDA)",
        "project": "Fellowship",
        # No compensation line at all for an unpaid fellowship.
        "no_compensation": True,
    },
    spec.FELLOW_TO_PAID: {
        "label": "Unpaid to Paid Transition",
        "template": "niete_joining_design3.html",
        # Rule: this is a REPLY in the existing thread, so it carries no new
        # subject of its own.
        "subject": None,
        "in_thread": True,
        "attachments": "Contract",
        "project": "Fellowship",
    },
    spec.PROJECT_HIRE: {
        "label": "NIETE Coach",
        "template": "niete_joining_design3.html",
        "subject": "Congratulations {first_name} on Your Selection as a Coach for the NIETE Project!",
        "attachments": "Contract and Non-Disclosure Agreement (NDA)",
        "project": "NIETE",
    },
    spec.PERMANENT_HIRE: {
        "label": "Permanent Full-Time",
        "template": "permanent_joining_design3.html",
        "subject": "Welcome to Taleemabad, {first_name}!",
        "attachments": "Contract and Non-Disclosure Agreement (NDA)",
        "project": None,
    },
}

#: Engagements with no approved wording. Refused, never improvised.
NO_TEMPLATE = {
    spec.PROMOTION_SAME_TEAM: "Addendum / promotion",
    spec.TEAM_MOVE: "Internal team move",
}

#: 🔒 Ayesha 2026-10-01: EVERY joining email carries two links, the form for
#:    submitting the signed documents and the all-employee WhatsApp group.
#:    The form is chosen by ENTITY, not by programme: NIETE and NIETE
#:    fellowships get the NIETE form; OPL, OWT and OPL/OWT fellowships get the
#:    other one. Inc. has no form yet and is refused rather than guessed.
OPL_OWT_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf70SM4jlx4muDMLlN1ZMqHqVEQjJQgCBga-oRM-M1OZXCePw/viewform?usp=sharing&ouid=108638480093303713396&urp=gmail_link"
NIETE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdVAYfCZZhusF_tNLn7mxzoK5BFXDa7xfj2FZifRlva-YDBHQ/viewform"
FORM_URLS = {
    spec.NIETE: NIETE_FORM_URL,
    spec.OPL: OPL_OWT_FORM_URL,
    spec.OWT: OPL_OWT_FORM_URL,
}
WHATSAPP_URL = "https://chat.whatsapp.com/HglkfuENmLqEbaq8N5jSVq"


def links_for(entity: str) -> dict:
    """The two links every joining email carries, as Design 3 variables."""
    if entity not in FORM_URLS:
        raise JoiningEmailError(
            f"There is no submission form for {entity!r} yet. Ayesha has given "
            "the NIETE form and the OPL/OWT form only, and sending someone to "
            "another entity's form is worse than asking."
        )
    return {"ONBOARDING_FORM_URL": FORM_URLS[entity], "WHATSAPP_GROUP_URL": WHATSAPP_URL}

PILOT_RECIPIENT = "ayesha.khan@taleemabad.com"


class JoiningEmailError(ValueError):
    """The joining email cannot be produced or sent as asked."""


def situation_for(engagement: str) -> dict:
    if engagement in NO_TEMPLATE:
        raise JoiningEmailError(
            f"There is no approved joining email for a {NO_TEMPLATE[engagement]} "
            "yet. Ayesha has not given the wording, and inventing it is not an "
            "option: the templates are locked and only names, dates, duration "
            "and amount change."
        )
    if engagement not in SITUATIONS:
        raise JoiningEmailError(f"unknown engagement {engagement!r}")
    return SITUATIONS[engagement]


# --------------------------------------------------------------------------
# The rules that are checked, not remembered
# --------------------------------------------------------------------------

#: A weekday named anywhere in a date. Rule 3.
_WEEKDAY = re.compile(
    r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", re.I)

#: Meta-commentary that must never appear inside the body. Rule 5: the pilot
#: is byte-identical to the live email, so anything addressed to Ayesha about
#: the send belongs in chat.
_META = (
    "pilot", "nothing has gone", "has not been sent", "for your review",
    "draft for approval", "please confirm before", "open question",
    "[review]", "note to ayesha",
)


def check_body(html: str, *, compensation: Optional[str],
               start_date: Optional[str], entity: Optional[str] = None) -> list[str]:
    """Every reason this email must not be sent. Empty means it may."""
    problems: list[str] = []

    # Both links, and the RIGHT form for the entity (Ayesha 2026-10-01).
    if entity is not None:
        right = links_for(entity)["ONBOARDING_FORM_URL"]
        wrong = {u for u in FORM_URLS.values() if u != right}
        if _html.escape(right) not in (html or "") and right not in (html or ""):
            problems.append(
                f"The {entity} submission form link is missing. Every joining "
                "email carries the form for the signed documents."
            )
        if any(u in (html or "") or _html.escape(u) in (html or "") for u in wrong):
            problems.append(
                f"Another entity's submission form is linked. {entity} hires use "
                "their own entity's form."
            )
        if WHATSAPP_URL not in (html or ""):
            problems.append(
                "The WhatsApp group link is missing. Every joining email carries it."
            )
    text = re.sub(r"<[^>]+>", " ", html or "")

    if _WEEKDAY.search(text):
        problems.append(
            "A weekday is named in a date. Ayesha's rule is \"1st of August "
            "2026\", never \"Saturday, 1st of August 2026\"."
        )
    lowered = text.lower()
    for phrase in _META:
        if phrase in lowered:
            problems.append(
                f"The body contains {phrase!r}. The pilot has to be identical "
                "to what the candidate receives, so notes about the send go in "
                "chat, never inside the email."
            )
            break

    # Rule 4: the things the candidate acts on are bold.
    if compensation and compensation not in _bolded(html):
        problems.append(
            f"The compensation figure ({compensation}) is not bold. Ayesha's "
            "rule is that anything the candidate scans for is bold."
        )
    if start_date and start_date not in _bolded(html):
        problems.append(f"The joining date ({start_date}) is not bold.")

    if "http" in text and "Click here" not in html and "Click Here" not in html:
        problems.append(
            "A raw URL appears in the body. Links are always hyperlinked on "
            "the words \"Click here\"."
        )
    if re.search(r"\{\{[A-Z_]+\}\}", html or ""):
        left = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", html)))
        problems.append(f"The template did not fill in: {', '.join(left)}.")
    return problems


def _bolded(html: str) -> str:
    """Everything that actually renders bold, concatenated.

    🔴 BOTH WAYS OF BEING BOLD COUNT. Design 3 bolds the detail rows with
    `font-weight:bold` in the cell style, not with a <b> tag, so a check that
    only looked for tags reported the compensation figure and the joining date
    as unbolded on an email where both are plainly bold. A rule enforced by a
    check that misreads the layout gets switched off.
    """
    source = html or ""
    blocks = re.findall(r"<b[ >].*?</b>|<strong[ >].*?</strong>", source, re.S | re.I)
    # The backreference is BUILT, not written literally: a heredoc eats a
    # backslash-one into a control character and every check then reports
    # clean (CLAUDE.md Rule 31, hit three times in this session).
    styled = ("<(" + chr(92) + "w+)[^>]*font-weight:" + chr(92) + "s*bold"
              "[^>]*>(.*?)</" + chr(92) + "1>")
    blocks += [m.group(2) for m in re.finditer(styled, source, re.S | re.I)]
    return " ".join(re.sub(r"<[^>]+>", "", block) for block in blocks)


def attachments_ok(filenames: list[str], engagement: str) -> list[str]:
    """The package rule and the PDF rule, both as refusals."""
    problems: list[str] = []
    names = [n.lower() for n in filenames]

    for n in names:
        if n.endswith(".docx") or n.endswith(".doc"):
            problems.append(
                f"{n} is a Word file. Candidates receive PDF, never Word."
            )
    if not names:
        problems.append("There are no attachments.")

    # 🔴 The one that would do real harm.
    if engagement == spec.VOLUNTEER_FELLOW:
        if any("contract" in n for n in names):
            problems.append(
                "This is a VOLUNTEER fellowship and a contract is attached. An "
                "unpaid person receives the NDA and nothing else: a contract "
                "creates an obligation nobody agreed to."
            )
        if not any("nda" in n for n in names):
            problems.append("A volunteer fellowship must have the NDA attached.")
    elif engagement == spec.FELLOW_TO_PAID:
        if any("nda" in n for n in names):
            problems.append(
                "This is an unpaid-to-paid transition, so the contract goes "
                "alone. The NDA was signed at the unpaid stage and sending a "
                "second one implies the first did not count."
            )
    else:
        expected = situation_for(engagement)["attachments"]
        if "NDA" in expected and not any("nda" in n for n in names):
            problems.append(f"{expected} was promised but no NDA is attached.")
        if "Contract" in expected and not any("contract" in n for n in names):
            problems.append(f"{expected} was promised but no contract is attached.")
    return problems


def recipients_for(*, live: bool, candidate_email: Optional[str],
                   cc: Optional[list[str]] = None) -> dict:
    """A pilot goes to Ayesha and nobody else, with no CC (Rule 4 of CLAUDE.md).

    Built from nothing for a pilot rather than filtered from the live list, so
    a CC cannot survive by being forgotten.
    """
    if not live:
        return {"to": [PILOT_RECIPIENT], "cc": []}
    if not (candidate_email or "").strip():
        raise JoiningEmailError("a live joining email needs the candidate's address")
    return {"to": [candidate_email.strip()], "cc": list(cc or [])}


def subject_for(engagement: str, *, first_name: str, role: str) -> Optional[str]:
    """None for the transition email, which replies inside an existing thread."""
    situation = situation_for(engagement)
    if not situation["subject"]:
        return None
    return situation["subject"].format(
        first_name=_html.escape(first_name or "", quote=False),
        role=_html.escape(role or "", quote=False),
    )
