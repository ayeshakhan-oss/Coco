"""Track case-study submissions: who has sent one in, who has not, and what
the pool's submissions have in common that they should not.

SOURCE OF TRUTH: .claude/skills/02_candidate-evaluation/case-study-evaluation.md
(tracking, completeness and AI flags). SCORING is a different component --
`case_study_scoring.py` against a QA'd benchmark -- and nothing here scores.

🔴 THE DENOMINATOR IS NOT IN THE DATABASE. Measured 2026-09-22 across all 4,509
   applications: `case_study_status` is populated on 116 and agrees with the
   evidence columns on every single one (0 disagreements either way), so the
   SUBMITTED side is trustworthy. The SENT side is not recorded at all. There is
   no `case_study_sent_at` column, and `public.candidate_communications` holds
   16 typed rows in the whole table: per job it reports 0 sends against 4 to 17
   submissions. Case studies go out by email from Ayesha's mailbox, so the send
   is in Gmail and nowhere else.

   Everything below follows from that. A candidate with no submission is
   `NO_RECORD_OF_A_SEND`, never "not sent": we cannot see the send, so absence
   of a record is not evidence of absence (CLAUDE.md Rule 18). Only a mailbox
   probe can promote that to `AWAITING`. A status vocabulary that let a reader
   say "43 were not sent one" from database fields alone would be inventing the
   number.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, Optional

# --------------------------------------------------------------------------
# Submission status
# --------------------------------------------------------------------------

#: A submission exists: Markaz holds text, a file, or both.
SUBMITTED = "submitted"
#: A send was FOUND in the mailbox and no submission has arrived.
AWAITING = "awaiting"
#: No submission, and no send found either. NOT the same as "not sent" -- the
#: send is invisible to the database, so this is a statement about our records.
NO_RECORD_OF_A_SEND = "no_record_of_a_send"
#: A submission exists but no send was found. Worth surfacing rather than
#: hiding: either the mailbox probe missed it, or it went out another way.
SUBMITTED_WITHOUT_SEND_RECORD = "submitted_without_send_record"

STATUSES = (SUBMITTED, AWAITING, NO_RECORD_OF_A_SEND, SUBMITTED_WITHOUT_SEND_RECORD)

#: Statuses a reader may NOT report as "this candidate was not sent a case
#: study". Kept as data so the UI and any report can check membership rather
#: than reimplementing the caveat.
UNPROVEN_ABSENCE = (NO_RECORD_OF_A_SEND,)

#: Markaz's four submission channels, in the order the SOP checks them.
CHANNELS = ("submission_text", "word_file", "excel_file", "video_file")


def channels_present(row: dict) -> list[str]:
    """Which of Markaz's four case-study channels actually hold something.

    A candidate may use one, both or neither, so the SOP says to check every
    one for every candidate rather than stopping at the first hit.
    """
    mapping = {
        "submission_text": row.get("case_study_submission"),
        "word_file": row.get("case_study_word_file"),
        "excel_file": row.get("case_study_excel_file"),
        "video_file": row.get("case_study_video_file"),
    }
    return [k for k in CHANNELS if (mapping.get(k) or "").strip()]


def submission_status(row: dict, *, send_found: Optional[bool] = None) -> str:
    """Reconcile what Markaz holds against whether a send was found.

    `send_found=None` means the mailbox has not been probed for this candidate.
    That is deliberately NOT treated as "no send": an unprobed candidate with no
    submission is `NO_RECORD_OF_A_SEND`, the same as a probed one that found
    nothing, because in both cases all we can honestly say is that we have no
    record. The difference is recorded by the probe timestamp, not by inventing
    a fifth status that reads like a stronger claim than it is.
    """
    if channels_present(row):
        return SUBMITTED if send_found else SUBMITTED_WITHOUT_SEND_RECORD
    return AWAITING if send_found else NO_RECORD_OF_A_SEND


def summarise(statuses: Iterable[str]) -> dict:
    """Counts per status, plus the caveat a report must carry.

    `unproven_absence` is the number of candidates a reader must NOT describe as
    "not sent a case study".
    """
    counts = Counter(statuses)
    unknown = sorted(set(counts) - set(STATUSES))
    if unknown:
        raise ValueError(f"unknown submission status: {unknown}")
    return {
        "total": sum(counts.values()),
        **{s: counts.get(s, 0) for s in STATUSES},
        "unproven_absence": sum(counts.get(s, 0) for s in UNPROVEN_ABSENCE),
    }


# --------------------------------------------------------------------------
# Completeness
# --------------------------------------------------------------------------


def completeness(corpus_text: str, required_parts: Optional[list[str]]) -> dict:
    """Which required parts of the assignment appear in the submission.

    `required_parts` are the assignment's own section names, supplied per job.
    With none configured this returns `known=False` and NO verdict: the SOP asks
    whether a required section is missing, and that question is unanswerable
    without knowing what was required. Guessing the sections from the
    submission's own headings would mark every submission complete by
    construction.
    """
    if not required_parts:
        return {"known": False, "present": [], "missing": [], "note":
                "No required parts configured for this job, so completeness "
                "cannot be assessed. Configure the assignment's section names "
                "to enable it."}

    haystack = " ".join(corpus_text.lower().split())
    present, missing = [], []
    for part in required_parts:
        (present if part.strip().lower() in haystack else missing).append(part)
    return {"known": True, "present": present, "missing": missing, "note": None}


# --------------------------------------------------------------------------
# AI / effort flags (the SOP's "content dump" signals)
# --------------------------------------------------------------------------

_EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿]"
)
# Markdown that survived a paste out of a chat window. A submitted document
# should not still be carrying "**" or "###".
_MARKDOWN_ARTEFACT = re.compile(r"(^|\n)\s{0,3}#{2,6}\s|\*\*\S|\n\s*[-*]\s{2,}")
# Phrasing that belongs to an assistant answering a prompt, not to a candidate
# writing a submission.
_ASSISTANT_VOICE = (
    "as an ai", "i cannot browse", "as a language model", "i don't have access to",
    "here's a comprehensive", "here is a comprehensive", "in conclusion,",
    "it's important to note", "it is important to note", "certainly!",
    "let me know if you'd like", "i hope this helps",
)
# Filler that says nothing about this case in particular.
_GENERIC = (
    "leverage synergies", "best practices", "cutting-edge", "game-changer",
    "holistic approach", "robust framework", "key stakeholders",
    "moving forward", "at the end of the day", "paradigm shift",
)

#: A flag is a SIGNAL FOR A HUMAN, never a verdict. The SOP's own integrity
#: checks are things to look at, not things to reject on, and none of these
#: proves anything on its own.
FLAG_MEANINGS = {
    "emoji": "Emoji in a work submission. Common in pasted assistant output.",
    "markdown_artefacts": "Markdown headings or bold markers left in the document.",
    "assistant_voice": "Phrasing that reads as an assistant answering a prompt.",
    "generic_language": "Filler that would fit any case study, not this one.",
}


def _hits(text: str, needles: tuple[str, ...]) -> list[str]:
    low = text.lower()
    return [n for n in needles if n in low]


def content_dump_flags(text: str) -> list[dict]:
    """The SOP's content-dump signals, each with the evidence that raised it.

    Evidence is always included, because a flag a human cannot check is an
    accusation rather than a signal.
    """
    flags: list[dict] = []

    emoji = _EMOJI.findall(text)
    if emoji:
        flags.append({"flag": "emoji", "count": len(emoji),
                      "evidence": "".join(sorted(set(emoji))[:10])})

    md = _MARKDOWN_ARTEFACT.findall(text)
    if md:
        flags.append({"flag": "markdown_artefacts", "count": len(md), "evidence": ""})

    voice = _hits(text, _ASSISTANT_VOICE)
    if voice:
        flags.append({"flag": "assistant_voice", "count": len(voice),
                      "evidence": ", ".join(voice[:5])})

    generic = _hits(text, _GENERIC)
    if len(generic) >= 3:  # one stock phrase is normal writing; several is filler
        flags.append({"flag": "generic_language", "count": len(generic),
                      "evidence": ", ".join(generic[:5])})

    for f in flags:
        f["meaning"] = FLAG_MEANINGS[f["flag"]]
    return flags


# --------------------------------------------------------------------------
# The mirror problem -- only visible across a cohort
# --------------------------------------------------------------------------

#: Long enough that a shared run is not ordinary phrasing. Measured on the
#: SMG round, twelve-word runs do not recur between independently written
#: submissions; shorter windows match on quotes from the assignment itself.
MIRROR_WINDOW = 12
#: Fewer shared runs than this is a coincidence or a quoted prompt.
MIRROR_MIN_SHARED = 3

_WORD = re.compile(r"[a-z0-9']+")


def _shingles(text: str, n: int = MIRROR_WINDOW) -> set[str]:
    words = _WORD.findall(text.lower())
    if len(words) < n:
        return set()
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def mirror_pairs(
    corpora: dict[int, str], *, min_shared: int = MIRROR_MIN_SHARED
) -> list[dict]:
    """Pairs of submissions sharing long verbatim runs.

    The SOP's "mirror problem": identical stats or phrases across candidates
    usually means the same prompt into the same assistant. It is invisible from
    one submission, which is why tracking -- the only component that sees the
    whole pool -- is where it belongs.

    Returns the shared runs themselves so a human can look. It never names a
    cause: two candidates quoting the same paragraph of the assignment look
    identical to two candidates sharing an assistant, and only a person reading
    both can tell which.
    """
    shingled = {app_id: _shingles(t) for app_id, t in corpora.items() if t}
    out: list[dict] = []
    ids = sorted(shingled)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            shared = shingled[a] & shingled[b]
            if len(shared) >= min_shared:
                out.append({
                    "application_ids": [a, b],
                    "shared_runs": len(shared),
                    "examples": sorted(shared)[:3],
                })
    return sorted(out, key=lambda x: -x["shared_runs"])


# --------------------------------------------------------------------------
# Finding the send -- the only place it exists
# --------------------------------------------------------------------------

#: Subject wording our own case-study invites have used. Matched against a
#: WHITESPACE-NORMALISED subject: Markaz subjects carry double spaces
#: ("Growth  Manager") and our own vary, so a raw substring test misses them
#: (CLAUDE.md Rule 18).
SEND_SUBJECT_TERMS = (
    "case study",
    "case-study",
    "next step in your application",
)

#: Gmail's all-mail folder. Searching by RECIPIENT rather than by subject is
#: the reliable half: a subject can be reworded between batches, an address
#: cannot.
_ALL_MAIL_FOLDER = '"[Gmail]/All Mail"'


def _normalise(subject: str) -> str:
    return " ".join((subject or "").split()).lower()


def subject_looks_like_a_send(subject: str, terms: tuple[str, ...] = SEND_SUBJECT_TERMS) -> bool:
    """True if this subject reads as a case-study invite.

    Whitespace is normalised first. "Your Case  Study | Growth  Manager" must
    match, and it does not with a naive `"case study" in subject`.
    """
    normalised = _normalise(subject)
    return any(term in normalised for term in terms)


def find_send(
    candidate_email: str,
    *,
    terms: tuple[str, ...] = SEND_SUBJECT_TERMS,
    imap_factory=None,
) -> Optional[dict]:
    """Look in the mailbox for a case-study invite sent to this candidate.

    Returns `{subject, date}` for the EARLIEST matching message, or None. The
    earliest is what a deadline is counted from, and a later nudge on the same
    thread would otherwise reset the clock.

    Read-only throughout: the folder is selected `readonly=True` and bodies are
    fetched with BODY.PEEK so nothing is marked as read
    (memory/reference_ayesha_mailbox_imap_2026_08_10.md).
    """
    import email as email_lib
    from email.utils import parsedate_to_datetime

    from . import submissions

    if not candidate_email or "@" not in candidate_email:
        return None

    client = (imap_factory or submissions._default_imap_client)()
    best: Optional[dict] = None
    try:
        client.select(_ALL_MAIL_FOLDER, readonly=True)
        typ, data = client.search(None, f'(TO "{candidate_email}")')
        message_ids = data[0].split() if typ == "OK" and data and data[0] else []

        for msg_id in message_ids:
            typ, msg_data = client.fetch(msg_id, "(BODY.PEEK[HEADER])")
            if typ != "OK" or not msg_data or not msg_data[0]:
                continue
            header = email_lib.message_from_bytes(msg_data[0][1])
            subject = header.get("Subject") or ""
            if not subject_looks_like_a_send(subject, terms):
                continue
            try:
                sent_at = parsedate_to_datetime(header.get("Date"))
            except (TypeError, ValueError):
                continue
            if best is None or (sent_at and sent_at < best["date"]):
                best = {"subject": " ".join(subject.split()), "date": sent_at}

        submissions._log_gmail_read(
            f'TO "{candidate_email}"',
            len(message_ids),
            context="case_study_tracking.find_send",
        )
    finally:
        try:
            client.logout()
        except Exception:  # noqa: BLE001 - logout failure must never mask a result
            pass
    return best
