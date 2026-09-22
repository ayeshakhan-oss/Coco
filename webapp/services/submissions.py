"""Assemble a candidate's case-study submission into text the scorer can read.

Retrieval is not one path, and every branch below is a documented, already-paid-for
lesson in this repo (CLAUDE.md Rule 18, Rule 26):

  - Markaz mirrors every document submission to email as an attachment ("New Case
    Study Received"), so the MAILBOX is the first place to look, not the last.
    Attachments are named `case-study-<appId>-<word|excel>-<ts>-<name>.<ext>` --
    filtered by the APPLICATION ID inside the filename, never by subject keyword
    (Markaz subjects carry double spaces, "Growth  Manager", that break naive
    matching) and never by MIME type (the same notification carries both the
    Word/PDF and the Excel).
  - SMG submissions arrive as Markaz DRIVE LINKS, not attachments, inside the
    candidate's own application text.
  - `markaz.taleemabad.com/uploads/...` answers HTTP 200 for a MISSING file too,
    serving the SPA's own index.html -- so every fetch checks `content-type`,
    never the status code alone.
  - `/api/case-study-file/<app>/<word|excel>` returns 401 to automation (staff
    Google SSO only). That wall is real but NOT a blocker: the same files are
    almost always already sitting in the mailbox, so a 401 here is logged (at
    INFO) and, when `corpus_for` is doing the calling, recorded in ITS
    diagnostic list too -- so a total refusal can say "hit the documented 401
    wall" rather than the indistinguishable "found nothing" (see
    `markaz_case_study_api`'s `diagnostics` parameter and `corpus_for`'s
    `_bind_diagnostics`). The fetcher itself still returns an empty list
    rather than raising -- a 401 is never an error.

Extraction (docx text boxes and tables, pptx notes, xlsx values AND formulas, pdf
via PyMuPDF) is delegated to `scripts/evals/fetch_submission_corpora.py` -- this
module does not reimplement a fourth retriever/extractor, only the RETRIEVAL
(mailbox / Drive-link / Markaz-API) that decides which bytes to hand it.

Mirrors `cv_text.py`'s refusal pattern: `corpus_for` returns a usable corpus or
raises `SubmissionUnreadable`, never an empty string. A silent empty string is
what lets a model invent the submission it was never shown, and the core rule of
this evaluation pipeline is that an unreadable submission is refused, never
scored as a weak one.
"""

from __future__ import annotations

import functools
import inspect
import json
import logging
import os
import re
import tempfile
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

from sqlalchemy import text as sql_text
from sqlalchemy.orm import Session

from scripts.evals import fetch_submission_corpora as extraction

log = logging.getLogger("webapp.submissions")

# Below this, whatever was assembled is not a readable submission: a notification
# email with no real attachment, a Drive link that resolved to the SPA shell, or a
# genuinely empty/near-empty document. Mirrors cv_text.MIN_USABLE_CHARS -- the
# floor that separates "text" from "no text", not the skill's fuller read-quality
# bar. The caller (a scoring run) decides what to do with the refusal.
MIN_USABLE_CHARS = 400

MARKAZ_BASE_URL = "https://markaz.taleemabad.com"
_CASE_STUDY_API_KINDS = ("word", "excel")

_MAILBOX_HOST = "imap.gmail.com"
_MAILBOX_USER = "ayesha.khan@taleemabad.com"
_ALL_MAIL = '"[Gmail]/All Mail"'
_NOTIFICATION_SUBJECT = "Case Study"

_DRIVE_TOKEN_FILE = ".claude/config/token_sheets_broad.json"
_DRIVE_ID_RE = re.compile(r"/d/([a-zA-Z0-9_-]{20,})|[?&]id=([a-zA-Z0-9_-]{20,})")
_URL_RE = re.compile(r"https?://\S+")


class SubmissionUnreadable(Exception):
    """A submission exists (or should) but no usable text could be assembled."""


@dataclass(frozen=True)
class RawAttachment:
    """One retrieved file, not yet turned into text."""

    origin: str  # human-readable provenance, logged as a "source actually read"
    filename: str
    content: bytes


@dataclass(frozen=True)
class SubmissionContext:
    """Everything a fetcher needs to go find one application's submission."""

    application_id: int
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    job_title: Optional[str] = None
    # Candidate-facing URLs already found in their own application text (cover
    # letter / custom answers / communication log) -- Drive share links or a
    # direct markaz.taleemabad.com/uploads/... link most often.
    links: tuple[str, ...] = field(default_factory=tuple)


# ── Source resolvers (fetch RAW BYTES; extraction happens afterwards) ─────────
# Each takes a SubmissionContext and returns whatever it could retrieve. Every
# low-level client is an injectable keyword argument with a lazy-imported real
# default, so tests exercise the real control flow with fakes and never touch
# the network or a mailbox.


def mailbox_attachments(
    ctx: SubmissionContext,
    *,
    imap_factory: Optional[Callable[[], "object"]] = None,
) -> list[RawAttachment]:
    """The Markaz "New Case Study Received" notification, mirrored to email.

    Filtered by the application ID embedded in the attachment filename (Rule 18):
    subject-keyword matching breaks on Markaz's double-spaced subjects, and
    MIME-type filtering misses half the notification (it carries the Word/PDF
    AND the Excel together).
    """
    import email as email_lib

    client = (imap_factory or _default_imap_client)()
    found: list[RawAttachment] = []
    try:
        client.select(_ALL_MAIL, readonly=True)
        typ, data = client.search(None, f'(SUBJECT "{_NOTIFICATION_SUBJECT}")')
        message_ids = data[0].split() if typ == "OK" and data and data[0] else []
        needle = f"case-study-{ctx.application_id}-".lower()

        for msg_id in message_ids:
            typ, msg_data = client.fetch(msg_id, "(BODY.PEEK[])")
            if typ != "OK" or not msg_data or not msg_data[0]:
                continue
            raw = msg_data[0][1]
            message = email_lib.message_from_bytes(raw)
            for part in message.walk():
                filename = part.get_filename()
                if not filename or needle not in filename.lower():
                    continue
                payload = part.get_payload(decode=True)
                if not payload:
                    continue
                found.append(
                    RawAttachment(
                        origin=f"Gmail attachment: {filename}",
                        filename=filename,
                        content=payload,
                    )
                )

        _log_gmail_read(
            f'SUBJECT "{_NOTIFICATION_SUBJECT}"',
            len(message_ids),
            context=f"submissions.mailbox_attachments app={ctx.application_id}",
        )
    finally:
        try:
            client.logout()
        except Exception:  # noqa: BLE001 - logout failure must never mask a result
            pass
    return found


def markaz_linked_documents(
    ctx: SubmissionContext,
    *,
    http_get: Optional[Callable[..., "object"]] = None,
    drive_download: Optional[Callable[[str], tuple[str, bytes]]] = None,
) -> list[RawAttachment]:
    """Follow Drive or direct Markaz-upload links from the candidate's own text.

    SMG submissions arrive this way, not as attachments (Rule 26). A
    `markaz.taleemabad.com/uploads/...` link answers HTTP 200 even when the file
    is gone, serving the SPA's index.html -- so `content-type` is checked on
    every fetch, never the status code alone.
    """
    get = http_get or _default_http_get
    out: list[RawAttachment] = []
    for url in ctx.links:
        drive_id = _drive_file_id(url)
        if drive_id:
            try:
                filename, content = (drive_download or _default_drive_download)(drive_id)
            except Exception:  # noqa: BLE001 - one bad link must not abort the rest
                continue
            if content:
                out.append(RawAttachment(origin=f"Drive: {url}", filename=filename, content=content))
            continue

        try:
            resp = get(url, timeout=15)
        except Exception:  # noqa: BLE001 - network error on a best-effort link
            continue
        if getattr(resp, "status_code", None) != 200:
            continue
        content_type = (resp.headers.get("content-type") or "").lower()
        if "text/html" in content_type:
            continue  # the SPA-shell trap: HTTP 200 but not the document
        filename = _filename_from_response(resp, fallback=url.rsplit("/", 1)[-1] or "submission")
        out.append(RawAttachment(origin=f"URL: {url}", filename=filename, content=resp.content))
    return out


def markaz_case_study_api(
    ctx: SubmissionContext,
    *,
    http_get: Optional[Callable[..., "object"]] = None,
    diagnostics: Optional[list[str]] = None,
) -> list[RawAttachment]:
    """Markaz's own case-study-file API, for completeness.

    Automation gets 401 here (staff Google SSO only) -- a documented, non-fatal
    wall, not evidence the submission doesn't exist. It is logged at INFO (this
    was previously claimed in the module docstring but not actually done), and
    when the caller passes `diagnostics` (a list `corpus_for` owns and reads
    back after every fetcher runs -- see `_bind_diagnostics`), a line naming
    the wall is appended there too, so a total-failure refusal message can say
    "hit the documented 401 wall" rather than the indistinguishable "found
    nothing". The fetcher itself still returns an empty list rather than
    raising either way -- a 401 is never an error, and never silently
    swallowed either.
    """
    get = http_get or _default_http_get
    out: list[RawAttachment] = []
    for kind in _CASE_STUDY_API_KINDS:
        url = f"{MARKAZ_BASE_URL}/api/case-study-file/{ctx.application_id}/{kind}"
        try:
            resp = get(url, timeout=10)
        except Exception:  # noqa: BLE001 - network error on an expected-to-fail path
            continue
        status = getattr(resp, "status_code", None)
        if status == 401:
            log.info(
                "markaz_case_study_api: 401 (staff Google SSO only) for %s -- "
                "documented, non-fatal wall, not evidence the submission doesn't "
                "exist; trying other sources", url,
            )
            if diagnostics is not None:
                diagnostics.append(
                    f"Markaz API: {url}: 401 (documented staff-SSO-only wall, not a "
                    "blocker -- the same file is almost always already in the mailbox)"
                )
            continue
        if status != 200:
            continue  # nothing there -- not a blocker either
        content_type = (resp.headers.get("content-type") or "").lower()
        if "text/html" in content_type:
            continue
        filename = _filename_from_response(
            resp, fallback=f"case-study-{ctx.application_id}-{kind}"
        )
        out.append(RawAttachment(origin=f"Markaz API: {url}", filename=filename, content=resp.content))
    return out


DEFAULT_FETCHERS: tuple[Callable[[SubmissionContext], list[RawAttachment]], ...] = (
    mailbox_attachments,
    markaz_linked_documents,
    markaz_case_study_api,
)


# ── Extraction (delegates to fetch_submission_corpora, does not reimplement it) ─


def _extract_text(attachment: RawAttachment) -> str:
    """Write the bytes to a temp file (named so the extension dispatch in
    `fetch_submission_corpora.extract` picks the right parser) and delegate."""
    suffix = os.path.splitext(attachment.filename)[1] or ""
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(attachment.content)
        return extraction.extract(path)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


# ── Orchestration ───────────────────────────────────────────────────────────


def _fetch_display_name(fetch) -> str:
    """A readable name for a fetcher, whether it's a plain function or one
    `_bind_diagnostics` wrapped in `functools.partial` (which has no
    `__name__` of its own) to inject this call's `problems` list."""
    name = getattr(fetch, "__name__", None)
    if name:
        return name
    inner = getattr(fetch, "func", None)
    if inner is not None:
        return getattr(inner, "__name__", repr(fetch))
    return repr(fetch)


def _bind_diagnostics(fetch, problems: list[str]):
    """If `fetch` accepts a `diagnostics` keyword (currently only
    `markaz_case_study_api`, for its documented, non-fatal 401 -- Rule 18),
    bind THIS call's `problems` list into it, so that fetcher's own logged-
    but-not-raised failure surfaces in the eventual refusal message even
    though the fetcher itself still returns normally rather than raising.
    Any fetcher that doesn't accept `diagnostics` (a caller's plain lambda,
    most of this module's own tests) is returned unchanged."""
    try:
        params = inspect.signature(fetch).parameters
    except (TypeError, ValueError):
        return fetch
    if "diagnostics" in params:
        return functools.partial(fetch, diagnostics=problems)
    return fetch


def corpus_for(
    application_id: int,
    *,
    db: Optional[Session] = None,
    context: Optional[SubmissionContext] = None,
    fetchers: Optional[Iterable[Callable[[SubmissionContext], list[RawAttachment]]]] = None,
) -> dict:
    """Assemble one application's case-study submission text, or refuse.

    Returns `{text, sources, chars, usable}` on success. `usable` is always True
    in a returned dict -- below `MIN_USABLE_CHARS` this raises
    `SubmissionUnreadable` instead of returning a thin result, exactly like
    `cv_text.extract` raises `CVUnreadable` rather than handing back an empty
    string. `sources` lists every origin that was actually opened and yielded
    text, so a report's method note can say what was verified.
    """
    if context is None:
        if db is None:
            raise ValueError("corpus_for needs either context= or db= to look one up")
        context = _context_from_db(db, application_id)

    resolved_fetchers = tuple(fetchers) if fetchers is not None else DEFAULT_FETCHERS

    sources: list[str] = []
    text_parts: list[str] = []
    problems: list[str] = []
    # ACTUAL extracted text only -- never the injected "===== {origin} ====="
    # provenance headers below. Several degraded sources each yielding a few
    # real characters must not pad past MIN_USABLE_CHARS on header boilerplate.
    extracted_chars = 0

    for raw_fetch in resolved_fetchers:
        fetch_name = _fetch_display_name(raw_fetch)
        # Give a fetcher that supports it (markaz_case_study_api) a way to
        # report a non-fatal, documented failure (a 401) into THIS call's
        # diagnostics without raising -- see _bind_diagnostics.
        fetch = _bind_diagnostics(raw_fetch, problems)
        try:
            attachments = fetch(context)
        except Exception as exc:  # noqa: BLE001 - one channel failing tries the next
            problems.append(f"{fetch_name}: {type(exc).__name__}: {exc}")
            continue
        for attachment in attachments:
            try:
                extracted = _extract_text(attachment)
            except Exception as exc:  # noqa: BLE001 - a bad file must not abort the rest
                problems.append(f"{attachment.origin}: {type(exc).__name__}: {exc}")
                continue
            if extracted and extracted.strip():
                text_parts.append(f"\n===== {attachment.origin} =====\n{extracted}")
                sources.append(attachment.origin)
                extracted_chars += len(extracted)
            else:
                problems.append(f"{attachment.origin}: extracted 0 usable chars")

    combined = "\n".join(text_parts).strip()
    chars = len(combined)

    if extracted_chars < MIN_USABLE_CHARS:
        tried = ", ".join(_fetch_display_name(f) for f in resolved_fetchers)
        detail = "; ".join(problems) if problems else "no source returned any content"
        raise SubmissionUnreadable(
            f"no usable case-study text for application {application_id} "
            f"(needs {MIN_USABLE_CHARS}+ chars of extracted text, got {extracted_chars}). "
            f"Tried: {tried}. {detail}. "
            "If the submission exists but is a scan or an inaccessible link, it must be "
            "fetched by hand."
        )

    return {"text": combined, "sources": sources, "chars": chars, "usable": True}


# ── DB context lookup ───────────────────────────────────────────────────────


def _context_from_db(db: Session, application_id: int) -> SubmissionContext:
    from .reads import answer_texts  # reuse, don't reimplement the Markaz answers shape

    row = db.execute(
        sql_text(
            """
            SELECT a.cover_letter, a.custom_answers, a.canned_answers,
                   a.communication_history,
                   c.first_name, c.last_name, c.email,
                   j.title AS job_title
            FROM applications a
            JOIN candidates c ON c.id = a.candidate_id
            JOIN jobs j ON j.id = a.job_id
            WHERE a.id = :app_id
            """
        ),
        {"app_id": application_id},
    ).mappings().first()

    if not row:
        raise SubmissionUnreadable(f"no application found for id {application_id}")

    name = " ".join(p for p in (row["first_name"], row["last_name"]) if p).strip() or None

    blob_parts: list[str] = [row.get("cover_letter") or ""]
    blob_parts.extend(answer_texts(row.get("custom_answers")))
    blob_parts.extend(answer_texts(row.get("canned_answers")))
    history = row.get("communication_history")
    if history:
        try:
            blob_parts.append(json.dumps(history))
        except TypeError:
            pass

    links = tuple(dict.fromkeys(_extract_links("\n".join(blob_parts))))

    return SubmissionContext(
        application_id=application_id,
        candidate_name=name,
        candidate_email=row["email"],
        job_title=row["job_title"],
        links=links,
    )


def _extract_links(blob: str) -> list[str]:
    """Candidate-facing URLs worth following (Drive shares, Markaz uploads).
    Pure and side-effect-free -- unit-tested on its own."""
    return [
        url.rstrip('.,;)"\'')
        for url in _URL_RE.findall(blob or "")
        if "drive.google.com" in url or "docs.google.com" in url or "markaz.taleemabad.com" in url
    ]


# ── Lazy-imported real defaults for the injectable clients ─────────────────


def _default_imap_client():
    import imaplib

    from ..config import get_settings

    password = get_settings().email_password
    if not password:
        raise SubmissionUnreadable("EMAIL_PASSWORD is not configured; cannot search the mailbox")
    client = imaplib.IMAP4_SSL(_MAILBOX_HOST)
    client.login(_MAILBOX_USER, password)
    return client


def _default_http_get(url: str, timeout: int = 15):
    import requests

    return requests.get(url, timeout=timeout)


def _default_drive_download(file_id: str) -> tuple[str, bytes]:
    import io

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build as gbuild
    from googleapiclient.http import MediaIoBaseDownload

    creds = Credentials.from_authorized_user_file(_DRIVE_TOKEN_FILE)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    drive = gbuild("drive", "v3", credentials=creds)

    meta = drive.files().get(fileId=file_id, fields="name", supportsAllDrives=True).execute()
    filename = meta.get("name", file_id)

    request = drive.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return filename, buf.getvalue()


def _drive_file_id(url: str) -> Optional[str]:
    match = _DRIVE_ID_RE.search(url)
    if not match:
        return None
    return match.group(1) or match.group(2)


def _filename_from_response(resp, *, fallback: str) -> str:
    disposition = resp.headers.get("content-disposition", "") if hasattr(resp, "headers") else ""
    match = re.search(r'filename="?([^";]+)"?', disposition)
    if match:
        return match.group(1)
    return fallback


def _log_gmail_read(query: str, message_count: int, *, context: str) -> None:
    try:
        from scripts.utils.audit_log import log_gmail_read

        log_gmail_read(query, message_count, context=context)
    except Exception:  # noqa: BLE001 - audit logging must never break retrieval
        pass
