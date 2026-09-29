"""Turning a generated .docx into the PDF a candidate actually receives.

Contract attachments are PDF and never Word (Skill 07 joining-emails rule 10,
blocked by the send harness), and Google Drive is the only converter available
on any machine here. There is no Word and no LibreOffice.

🔴 `drive.file` ONLY. The server's Google token reaches files THIS app creates
   and nothing else. It uploads the .docx, converts, exports the PDF and
   deletes the temporary Drive copy in a finally block, so a failure mid-way
   does not leave a contract containing a CNIC and a salary sitting in Drive.

🔴 DRIVE RE-FLOWS THE DOCUMENT. The PDF is not a screenshot of the Word file;
   Drive lays it out again and has its own ideas about page breaks. It ignores
   `keep_with_next` outright, which is how a heading ends up stranded at the
   foot of a page (memory/opl_permanent_contract_and_joining_email_2026_09_12).
   Nothing here can see a page, so `CAVEAT` travels with every result and is
   not softened.
"""

from __future__ import annotations

import io
import json
import logging
from typing import Optional

log = logging.getLogger("webapp.pdf_convert")

DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive.file",
]

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

CAVEAT = (
    "Drive lays the document out again when it converts, so the PDF is not a "
    "picture of the Word file. Nothing here can see a page. Open the PDF and "
    "look at it before it goes to anyone."
)


class PdfUnavailable(RuntimeError):
    """Conversion is not possible with the credentials this server has."""


def _credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    from ..config import get_settings

    settings = get_settings()
    if settings.gmail_oauth_token_json:
        info = json.loads(settings.gmail_oauth_token_json)
        creds = Credentials.from_authorized_user_info(info, DRIVE_SCOPES)
    else:
        creds = Credentials.from_authorized_user_file(
            settings.gmail_token_file, DRIVE_SCOPES)

    # A token minted before the Drive scope was added will authenticate and
    # then fail on the first Drive call with a confusing 403. Say the real
    # thing instead.
    have = set(creds.scopes or [])
    if "https://www.googleapis.com/auth/drive.file" not in have:
        raise PdfUnavailable(
            "The server's Google token has no Drive permission, so a .docx "
            "cannot be converted to PDF. Re-run "
            "scripts/auth/setup_gmail_sync_token.py and update "
            "GMAIL_OAUTH_TOKEN_JSON."
        )
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def available() -> tuple[bool, Optional[str]]:
    """Whether conversion can run, without doing one."""
    try:
        _credentials()
        return True, None
    except PdfUnavailable as exc:
        return False, str(exc)
    except Exception as exc:  # pragma: no cover - credential shape problems
        return False, f"{type(exc).__name__}: {exc}"


def to_pdf(data: bytes, name: str = "document") -> bytes:
    """Convert .docx bytes to PDF bytes. Leaves nothing behind in Drive."""
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload

    creds = _credentials()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    created = drive.files().create(
        body={"name": f"coco-temp-{name}",
              # Uploading AS a Google Doc is what performs the conversion.
              "mimeType": "application/vnd.google-apps.document"},
        media_body=MediaIoBaseUpload(
            io.BytesIO(data), mimetype=DOCX_MIME, resumable=False),
        fields="id",
    ).execute()
    file_id = created["id"]

    try:
        pdf = drive.files().export(
            fileId=file_id, mimeType="application/pdf").execute()
    finally:
        # 🔴 Always, even on failure. The temporary copy is a filled contract
        #    carrying a CNIC and a salary.
        try:
            drive.files().delete(fileId=file_id).execute()
        except Exception:
            log.warning("pdf_convert: could not delete temp Drive file %s", file_id)

    if not pdf.startswith(b"%PDF-"):
        raise PdfUnavailable(
            "Drive returned something that is not a PDF. The document has not "
            "been converted."
        )
    return pdf
