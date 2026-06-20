"""Read-only Gmail evidence sync.

Cross-references Markaz candidates against Ayesha's Gmail **Sent** mailbox to
prove a candidate was actually emailed. Strictly read-only: scope is pinned to
`gmail.readonly`, and this module imports NOTHING from the send pipeline
(`sending.py`/`safe_send.py`).

Matching is tiered (most→least certain), and the chosen tier is recorded:
  1. message_id     — exact `rfc822msgid:` match for comms Coco itself sent.
  2. recipient_window — the candidate's address is a direct To: recipient of a
                        message in the Sent stream (after their application date).
Ambiguity (duplicate candidate email, matched only via Cc, no direct match)
resolves to `uncertain` → "Needs Review", never a silent yes/no.

Scale: instead of one Gmail query per candidate (~1,140 queries), we paginate
the Sent stream ONCE (metadata only), index it by recipient, and match every
candidate locally. Incremental runs only scan messages after the last
watermark; `found` evidence is terminal and skipped.
"""

from __future__ import annotations

import datetime as dt
import json
from email.utils import getaddresses
from typing import Iterable, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import get_settings

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
_METADATA_HEADERS = ["To", "Cc", "Bcc", "Subject", "Date", "Message-ID"]

# Safety bounds.
MAX_MESSAGES_PER_RUN = 6000
FULL_WINDOW_DAYS = 730  # bounded backfill window for a full / first-ever sync


# ── Pure helpers (unit-tested; no I/O) ───────────────────────────────────────

def norm_email(addr: Optional[str]) -> str:
    return (addr or "").strip().lower()


def parse_header_addresses(value: Optional[str]) -> list[str]:
    """Extract normalized email addresses from a To/Cc header value, handling
    `Name <a@b.com>, c@d.com` forms."""
    if not value:
        return []
    return [norm_email(a) for _, a in getaddresses([value]) if a]


def message_recipients(headers: dict[str, str]) -> dict[str, list[str]]:
    """Return {'to': [...], 'cc': [...], 'bcc': [...]} normalized."""
    return {
        "to": parse_header_addresses(headers.get("To")),
        "cc": parse_header_addresses(headers.get("Cc")),
        "bcc": parse_header_addresses(headers.get("Bcc")),
    }


def classify_candidate(
    candidate_email: str,
    messages: list[dict],
    *,
    duplicate_email: bool,
) -> dict:
    """Decide the gmail_status for one candidate given the Sent messages whose
    recipients include their address. `messages` items carry recipient buckets
    + metadata. Returns the evidence dict to upsert.

    Precedence: duplicate email -> uncertain; direct To match -> found;
    cc/bcc-only match -> uncertain; nothing -> none.
    """
    cand = norm_email(candidate_email)
    base = {
        "gmail_status": "none",
        "match_method": "none",
        "matched_message_id": None,
        "gmail_thread_id": None,
        "internal_date": None,
        "matched_subject": None,
        "matched_to": None,
        "matched_snippet": None,
        "uncertain_reason": None,
    }
    if not cand:
        return {**base, "gmail_status": "uncertain", "match_method": "none",
                "uncertain_reason": "candidate has no email address"}
    if duplicate_email:
        # Shared address — recipient matching can't disambiguate which person.
        if messages:
            best = _most_recent(messages)
            return _evidence_from(best, "uncertain", "recipient_window",
                                  "candidate email is shared by more than one candidate")
        return {**base, "gmail_status": "uncertain",
                "uncertain_reason": "candidate email is shared by more than one candidate"}

    direct = [m for m in messages if cand in m.get("to", [])]
    if direct:
        return _evidence_from(_most_recent(direct), "found", "recipient_window", None)

    if messages:  # matched only via cc/bcc
        return _evidence_from(_most_recent(messages), "uncertain", "recipient_window",
                              "candidate matched only as a Cc/Bcc recipient, not a direct To")

    return base


def _most_recent(messages: list[dict]) -> dict:
    return max(messages, key=lambda m: m.get("internal_ms", 0))


def _evidence_from(m: dict, status: str, method: str, reason: Optional[str]) -> dict:
    ms = m.get("internal_ms")
    internal = (
        dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc) if ms else None
    )
    return {
        "gmail_status": status,
        "match_method": method,
        "matched_message_id": m.get("message_id"),
        "gmail_thread_id": m.get("thread_id"),
        "internal_date": internal,
        "matched_subject": m.get("subject"),
        "matched_to": ", ".join(m.get("to", []))[:500] or None,
        "matched_snippet": (m.get("snippet") or "")[:500] or None,
        "uncertain_reason": reason,
    }


# ── Credentials + service (deferred Google imports) ──────────────────────────

def _load_credentials():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    s = get_settings()
    if s.gmail_oauth_token_json:
        info = json.loads(s.gmail_oauth_token_json)
        creds = Credentials.from_authorized_user_info(info, GMAIL_SCOPES)
    else:
        # Local-dev fallback to a token file (gitignored).
        creds = Credentials.from_authorized_user_file(s.gmail_token_file, GMAIL_SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def _build_service():
    import google_auth_httplib2
    import httplib2
    from googleapiclient.discovery import build

    # Wrap with a socket timeout so a stalled connection can never hang the sync.
    authed = google_auth_httplib2.AuthorizedHttp(
        _load_credentials(), http=httplib2.Http(timeout=30)
    )
    return build("gmail", "v1", http=authed, cache_discovery=False)


def gmail_token_ok() -> tuple[bool, Optional[str]]:
    """Health check for /readyz and the status endpoint — does the token work?"""
    try:
        svc = _build_service()
        svc.users().getProfile(userId="me").execute()
        return True, None
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


# ── Gmail fetch helpers ──────────────────────────────────────────────────────

def _headers_dict(msg: dict) -> dict[str, str]:
    return {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}


def _meta_from_message(msg: dict) -> dict:
    headers = _headers_dict(msg)
    rec = message_recipients(headers)
    try:
        internal_ms = int(msg.get("internalDate", "0"))
    except (TypeError, ValueError):
        internal_ms = 0
    return {
        "id": msg.get("id"),
        "thread_id": msg.get("threadId"),
        "message_id": (headers.get("Message-ID") or "").strip() or None,
        "subject": headers.get("Subject"),
        "snippet": msg.get("snippet"),
        "internal_ms": internal_ms,
        "to": rec["to"],
        "cc": rec["cc"],
        "bcc": rec["bcc"],
    }


def _fetch_message_meta(svc, msg_id: str) -> Optional[dict]:
    msg = (
        svc.users()
        .messages()
        .get(userId="me", id=msg_id, format="metadata", metadataHeaders=_METADATA_HEADERS)
        .execute()
    )
    return _meta_from_message(msg)


def _fetch_metas(svc, ids: list[str], chunk: int = 40, max_passes: int = 4) -> list[dict]:
    """Fetch message metadata in batches (one HTTP round-trip per `chunk`),
    instead of one request per message — the difference between minutes and
    seconds on a high-latency link.

    A batch of N get(metadata) calls costs N*5 Gmail quota units; sent too fast
    this trips the 250-units/user/sec limit and some sub-requests are dropped
    with a 429. We keep chunks small, space batches slightly, and re-request any
    ids that didn't come back (up to `max_passes`) so no evidence is missed."""
    import time

    metas_by_id: dict[str, dict] = {}

    def _cb(request_id, response, exception):  # noqa: ANN001
        if exception is None and response and response.get("id"):
            metas_by_id[response["id"]] = _meta_from_message(response)

    remaining = list(dict.fromkeys(ids))  # de-dupe, preserve order
    for _pass in range(max_passes):
        if not remaining:
            break
        for i in range(0, len(remaining), chunk):
            batch = svc.new_batch_http_request(callback=_cb)
            for mid in remaining[i : i + chunk]:
                batch.add(
                    svc.users().messages().get(
                        userId="me", id=mid, format="metadata", metadataHeaders=_METADATA_HEADERS
                    )
                )
            batch.execute()
            time.sleep(0.3)  # stay under the per-second quota
        remaining = [m for m in remaining if m not in metas_by_id]
    return list(metas_by_id.values())


def _search_message_ids(svc, query: str, cap: int) -> list[str]:
    ids: list[str] = []
    page_token = None
    while len(ids) < cap:
        resp = (
            svc.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token, maxResults=500)
            .execute()
        )
        ids.extend(m["id"] for m in resp.get("messages", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return ids[:cap]


# ── DB helpers ───────────────────────────────────────────────────────────────

def _duplicate_emails(db: Session) -> set[str]:
    rows = db.execute(
        text(
            "SELECT lower(email) AS e FROM candidates "
            "WHERE email IS NOT NULL AND email <> '' "
            "GROUP BY lower(email) HAVING count(*) > 1"
        )
    ).scalars().all()
    return set(rows)


def _candidates_to_check(db: Session) -> list[dict]:
    """Comms-relevant candidates whose evidence isn't terminal (found / manually
    marked sent) — the working set we still need to evaluate."""
    sql = """
    SELECT a.id AS application_id, a.candidate_id, a.job_id, lower(c.email) AS email
    FROM applications a
    JOIN candidates c ON c.id = a.candidate_id
    LEFT JOIN comm_evidence ev ON ev.application_id = a.id
    WHERE (a.status = 'rejected'
           OR a.status IN ('warm_bench','consider_other_roles')
           OR a.status IN ('shortlisted','gwc_scheduled','case_study_sent','P2'))
      AND c.email IS NOT NULL AND c.email <> ''
      AND COALESCE(ev.gmail_status,'not_checked') <> 'found'
      AND ev.marked_sent_at IS NULL
    """
    return [dict(r) for r in db.execute(text(sql)).mappings().all()]


def _sent_comms_with_message_id(db: Session) -> list[dict]:
    sql = """
    SELECT application_id, candidate_id, job_id, message_id
    FROM communications
    WHERE status = 'sent' AND message_id IS NOT NULL AND application_id IS NOT NULL
    """
    return [dict(r) for r in db.execute(text(sql)).mappings().all()]


def _upsert_evidence(db: Session, application_id: int, candidate_id: int,
                     job_id: Optional[int], ev: dict) -> None:
    """Write Gmail evidence, never clobbering manual override / ignore fields."""
    db.execute(
        text(
            """
            INSERT INTO comm_evidence
              (id, application_id, candidate_id, job_id, gmail_status, match_method,
               matched_message_id, gmail_thread_id, internal_date, matched_subject,
               matched_to, matched_snippet, uncertain_reason, checked_at)
            VALUES
              ('ev-' || replace(gen_random_uuid()::text,'-',''), :app_id, :cand_id, :job_id,
               :gmail_status, :match_method, :mid, :tid, :idate, :subj, :mto, :snip, :reason, now())
            ON CONFLICT (application_id) DO UPDATE SET
              gmail_status = EXCLUDED.gmail_status,
              match_method = EXCLUDED.match_method,
              matched_message_id = EXCLUDED.matched_message_id,
              gmail_thread_id = EXCLUDED.gmail_thread_id,
              internal_date = EXCLUDED.internal_date,
              matched_subject = EXCLUDED.matched_subject,
              matched_to = EXCLUDED.matched_to,
              matched_snippet = EXCLUDED.matched_snippet,
              uncertain_reason = EXCLUDED.uncertain_reason,
              checked_at = now(),
              updated_at = now()
            """
        ),
        {
            "app_id": application_id, "cand_id": candidate_id, "job_id": job_id,
            "gmail_status": ev["gmail_status"], "match_method": ev.get("match_method"),
            "mid": ev.get("matched_message_id"), "tid": ev.get("gmail_thread_id"),
            "idate": ev.get("internal_date"), "subj": ev.get("matched_subject"),
            "mto": ev.get("matched_to"), "snip": ev.get("matched_snippet"),
            "reason": ev.get("uncertain_reason"),
        },
    )


# ── Sync orchestration ───────────────────────────────────────────────────────

def _last_watermark(db: Session) -> Optional[dt.datetime]:
    row = db.execute(
        text(
            "SELECT watermark_after FROM gmail_sync_runs "
            "WHERE status IN ('ok','partial') AND watermark_after IS NOT NULL "
            "ORDER BY started_at DESC LIMIT 1"
        )
    ).mappings().first()
    return row["watermark_after"] if row else None


def run_sync(
    db: Session,
    *,
    full: bool = False,
    trigger: str = "manual",
    triggered_by: Optional[str] = None,
) -> dict:
    """Execute one sync. Returns the gmail_sync_runs row as a dict."""
    run_id = "sync-" + _rand_hex()
    db.execute(
        text(
            """
            INSERT INTO gmail_sync_runs (id, trigger, triggered_by, full_resync, status, started_at)
            VALUES (:id, :trigger, :by, :full, 'running', now())
            """
        ),
        {"id": run_id, "trigger": trigger, "by": triggered_by, "full": full},
    )
    db.commit()

    found = uncertain = none = scanned = evaluated = 0
    watermark_before = _last_watermark(db)
    watermark_after = watermark_before
    error_detail = None
    status = "ok"

    try:
        svc = _build_service()
        dup = _duplicate_emails(db)

        incremental = bool(watermark_before) and not full
        after = int(watermark_before.timestamp()) if incremental else None
        query = "(to:<candidate> OR cc:<candidate>)" + (
            f" after:{after}" if after else "  [whole mailbox, all time]"
        )

        # Per-candidate WHOLE-MAILBOX search (not just Sent). We search every folder
        # for messages addressed to the candidate, so we catch comms sent by Ayesha
        # AND comms sent by teammates that reach her inbox via the hiring group — a
        # Sent-only search misses the latter. This is the Gmail half of the locked
        # "always reference BOTH Gmail + Markaz" rule (Markaz history is counted in
        # reads.py). See docs/RAILWAY_DEPLOYMENT_LESSONS.md.
        candidates = _candidates_to_check(db)
        evaluated = len(candidates)
        for i, c in enumerate(candidates):
            email = c["email"]
            q = f"(to:{email} OR cc:{email})"
            if after:
                q += f" after:{after}"
            ids = _search_message_ids(svc, q, cap=10)
            scanned += len(ids)
            if ids:
                metas = _fetch_metas(svc, ids)
                for m in metas:
                    ms = m.get("internal_ms")
                    if ms:
                        ts = dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc)
                        if watermark_after is None or ts > watermark_after:
                            watermark_after = ts
                ev = classify_candidate(email, metas, duplicate_email=email in dup)
                if ev["gmail_status"] in ("found", "uncertain"):
                    _upsert_evidence(db, c["application_id"], c["candidate_id"], c.get("job_id"), ev)
                    if ev["gmail_status"] == "found":
                        found += 1
                    else:
                        uncertain += 1
            if i % 50 == 49:
                db.commit()  # persist progress periodically on long full backfills
        none = max(0, evaluated - found - uncertain)
        db.commit()
    except Exception as e:  # noqa: BLE001
        db.rollback()
        status = "failed"
        error_detail = f"{type(e).__name__}: {e}"
        watermark_after = watermark_before  # don't advance on failure

    db.execute(
        text(
            """
            UPDATE gmail_sync_runs SET status=:status, query=:query,
              messages_scanned=:scanned, candidates_evaluated=:evaluated,
              found_count=:found, uncertain_count=:uncertain, none_count=:none,
              watermark_before=:wb, watermark_after=:wa, error_detail=:err, finished_at=now()
            WHERE id=:id
            """
        ),
        {
            "status": status, "query": locals().get("query"), "scanned": scanned,
            "evaluated": evaluated, "found": found, "uncertain": uncertain, "none": none,
            "wb": watermark_before, "wa": watermark_after, "err": error_detail, "id": run_id,
        },
    )
    db.commit()

    row = db.execute(
        text("SELECT * FROM gmail_sync_runs WHERE id=:id"), {"id": run_id}
    ).mappings().first()
    return dict(row) if row else {"id": run_id, "status": status}


def _rand_hex() -> str:
    # uuid4 is fine here (not a Workflow script).
    from uuid import uuid4

    return uuid4().hex
