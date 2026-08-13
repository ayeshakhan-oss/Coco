"""
Convert a .docx to PDF using Google Drive.

There is no Word or LibreOffice on this machine, so Drive's converter is the only
available renderer: upload the .docx as a Google Doc, export it as PDF, then delete
the temporary Doc.

⚠️ Drive re-flows the document. The PDF is a CONVERSION, not a faithful render of
Word's own layout — headers, letterhead images and indents can shift. Per Rule 1
(structural checks are not visual proof), the PDF must be eyeballed before it goes
to a candidate.

Usage:
    python scripts/utils/docx_to_pdf_drive.py "path/to/file.docx"
"""

import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN = Path(r"c:\Agent Coco\.claude\config\token_sheets_broad.json")
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def convert(docx_path: Path, pdf_path: Path = None) -> Path:
    docx_path = Path(docx_path)
    if pdf_path is None:
        pdf_path = docx_path.with_suffix(".pdf")

    creds = Credentials.from_authorized_user_file(str(TOKEN))
    drive = build("drive", "v3", credentials=creds)

    file_id = None
    try:
        media = MediaFileUpload(str(docx_path), mimetype=DOCX_MIME, resumable=False)
        created = (
            drive.files()
            .create(
                body={
                    "name": f"[temp-convert] {docx_path.stem}",
                    # asking for a Google Doc triggers the conversion
                    "mimeType": "application/vnd.google-apps.document",
                },
                media_body=media,
                fields="id",
            )
            .execute()
        )
        file_id = created["id"]

        pdf_bytes = (
            drive.files().export(fileId=file_id, mimeType="application/pdf").execute()
        )
        pdf_path.write_bytes(pdf_bytes)
    finally:
        if file_id:
            try:
                drive.files().delete(fileId=file_id).execute()
            except Exception as e:  # noqa: BLE001
                print(f"  warning: temp Doc {file_id} not deleted: {e}")

    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: docx_to_pdf_drive.py <file.docx>")
    out = convert(Path(sys.argv[1]))
    print(f"[pdf] {out}  ({out.stat().st_size:,} bytes)")
