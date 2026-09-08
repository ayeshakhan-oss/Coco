"""
Publish the RM re-mark report (the 2 Sep email body) as a Google Doc in the documentation folder.

Ayesha, 2026-09-08: pointed at the email "RM Case Study - full re-mark of all 25, and why the
first pass was wrong" and said "im talking about this one".

She is right and this is why I kept linking the wrong artefact. THE REPORT SHE MEANS ONLY EVER
EXISTED AS AN EMAIL BODY. The 2 Sep email carried the whole thing inline: the headline, why the
first pass inflated, the three causes, what changed in the marking, and the NOW / WAS / delta
table for all 25. The only attachment was the per-candidate detail PDF, so nothing I could find
on Drive was ever the report itself.

This pulls that email's HTML body from the mailbox, strips the mail-client scaffolding, and
publishes it as a Google Doc inside the documentation folder so it has a stable link.

Content is kept VERBATIM. It is written in the first person to Ayesha and says plainly that the
first pass was a marking failure rather than a strong pool. That candour is the point of the
document and is not softened for republication.
"""

import email
import imaplib
import io
import os
import re
import sys
from email.header import decode_header, make_header

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaIoBaseUpload

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT, ".env"))
TOKEN = os.path.join(ROOT, ".claude", "config", "token_sheets_broad.json")
KEEP = os.path.join(ROOT, "output", "rm_marking")
DOC_FOLDER = "1hIhLcu9TSLVptef9STFKZQ6CQ6lMebVn"
INDEX = "1_-H0hLYj0pujY-9Jfw8zEhXtPTdhGFBuJGMtfQhZ-bo"
SUBJECT = "RM Case Study - full re-mark of all 25, and why the first pass was wrong"
DOC_NAME = "RM Case Study - Re-mark of all 25, and why the first pass was wrong"


def fetch_body():
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login("ayesha.khan@taleemabad.com", os.environ["EMAIL_PASSWORD"])
    M.select('"[Gmail]/All Mail"', readonly=True)
    typ, d = M.uid("search", None, "SINCE", "01-Sep-2026", "SUBJECT", '"full re-mark of all 25"')
    best = None
    for u in d[0].split():
        t, dd = M.uid("fetch", u, "(BODY.PEEK[])")
        msg = email.message_from_bytes(b"".join(p[1] for p in dd if isinstance(p, tuple)))
        subj = re.sub(r"\s+", " ", str(make_header(decode_header(msg.get("Subject") or ""))))
        if subj.lower().startswith("fwd:") or subj.lower().startswith("re:"):
            continue
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                html = (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset() or "utf-8", "replace")
                if "re-mark" in html.lower() and (best is None or len(html) > len(best[1])):
                    best = (subj, html)
    M.logout()
    if not best:
        raise SystemExit("could not find the re-mark email body")
    return best


def clean(html):
    """Drop the mail wrapper and anything that only makes sense inside an inbox."""
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # the feedback widget and any tracking pixels are email-only furniture
    html = re.sub(r'<img[^>]+width="1"[^>]*>', "", html, flags=re.I)
    body = re.search(r"<body[^>]*>(.*)</body>", html, flags=re.S | re.I)
    inner = body.group(1) if body else html
    return ("<html><head><meta charset='utf-8'></head>"
            "<body style=\"font-family:Georgia,serif\">" + inner + "</body></html>")


def main():
    subj, html = fetch_body()
    print(f"found email: {subj}")
    print(f"  html body: {len(html):,} chars")
    doc_html = clean(html)
    open(os.path.join(KEEP, "rm_remark_report.html"), "w", encoding="utf-8").write(doc_html)

    c = Credentials.from_authorized_user_file(TOKEN)
    if c.expired and c.refresh_token:
        c.refresh(Request())
    drive = gbuild("drive", "v3", credentials=c)
    sheets = gbuild("sheets", "v4", credentials=c)

    ex = drive.files().list(
        q=f"'{DOC_FOLDER}' in parents and name='{DOC_NAME}' and trashed=false",
        fields="files(id)").execute()["files"]
    media = MediaIoBaseUpload(io.BytesIO(doc_html.encode("utf-8")),
                              mimetype="text/html", resumable=False)
    if ex:
        fid = ex[0]["id"]
        drive.files().update(fileId=fid, media_body=media,
                             body={"mimeType": "application/vnd.google-apps.document"}).execute()
        print(f"  updated in place: {fid}")
    else:
        fid = drive.files().create(
            body={"name": DOC_NAME, "parents": [DOC_FOLDER],
                  "mimeType": "application/vnd.google-apps.document"},
            media_body=media, fields="id").execute()["id"]
        print(f"  created: {fid}")

    txt = drive.files().export(fileId=fid, mimeType="text/plain").execute().decode(
        "utf-8", "replace")
    checks = {
        "headline present": "They were not all that good" in txt,
        "eight below the line": "Eight of them now fall below" in txt,
        "NOW/WAS table": "WAS" in txt and "Rida Abbas" in txt,
        "mean 75.0": "75.0" in txt,
        "lowest score 56": "56" in txt,
    }
    for k, v in checks.items():
        print(f"  {'OK ' if v else 'FAIL'} {k}")
    if not all(checks.values()):
        raise SystemExit("verification failed")

    # ---- point the index's evaluation-report row at this Doc ----
    meta = sheets.spreadsheets().get(spreadsheetId=INDEX).execute()
    rd = [s["properties"]["sheetId"] for s in meta["sheets"]
          if s["properties"]["title"] == "Round Documents"][0]
    g = sheets.spreadsheets().get(spreadsheetId=INDEX, ranges=["'Round Documents'"],
                                  includeGridData=True).execute()
    rows = g["sheets"][0]["data"][0].get("rowData", [])

    def sv(r, i):
        v = r.get("values", [])
        return ((v[i].get("userEnteredValue") or {}).get("stringValue") or "") if len(v) > i else ""

    def cell(s):
        return {"userEnteredValue": {"stringValue": s},
                "userEnteredFormat": {"textFormat": {"fontSize": 10, "fontFamily": "Georgia"},
                                      "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}}

    def lk(u, l):
        return {"userEnteredValue": {"formulaValue": f'=HYPERLINK("{u}","{l}")'},
                "userEnteredFormat": {"textFormat": {"fontSize": 10, "fontFamily": "Georgia"},
                                      "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}}

    rep_i = next(i for i, r in enumerate(rows)
                 if sv(r, 0).startswith("Case study evaluation report"))
    reqs = [
        {"updateCells": {
            "range": {"sheetId": rd, "startRowIndex": rep_i, "endRowIndex": rep_i + 1,
                      "startColumnIndex": 0, "endColumnIndex": 3},
            "rows": [{"values": [
                cell("CASE STUDY EVALUATION REPORT - the re-mark of all 25, and why the first "
                     "pass was wrong (mean 75, 8 below the 70% bar)"),
                cell("Google Doc"),
                lk(f"https://docs.google.com/document/d/{fid}/edit", "Open")]}],
            "fields": "userEnteredValue,userEnteredFormat"}},
        {"insertDimension": {"range": {"sheetId": rd, "dimension": "ROWS",
                                       "startIndex": rep_i + 1, "endIndex": rep_i + 2},
                             "inheritFromBefore": False}},
        {"updateCells": {
            "range": {"sheetId": rd, "startRowIndex": rep_i + 1, "endRowIndex": rep_i + 2,
                      "startColumnIndex": 0, "endColumnIndex": 3},
            "rows": [{"values": [
                cell("Evaluation report, per-candidate write-up for all 25 (same scores, "
                     "fuller detail)"),
                cell("Google Doc"),
                lk("https://docs.google.com/document/d/"
                   "1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc/edit", "Open")]}],
            "fields": "userEnteredValue,userEnteredFormat"}},
    ]
    sheets.spreadsheets().batchUpdate(spreadsheetId=INDEX, body={"requests": reqs}).execute()
    print(f"\nindex updated at row {rep_i + 1}")
    print(f"https://docs.google.com/document/d/{fid}/edit")


if __name__ == "__main__":
    sys.exit(main())
