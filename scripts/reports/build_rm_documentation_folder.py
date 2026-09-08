"""
RM internal hiring 2026 - single documentation folder for the whole round.

Ayesha, 2026-09-08: "make a folder with all the submissions of the case study and in that folder
add a sheet... add the benchmark case study evaluation, answer by answer evaluation and also the
case study evaluation report? Like their links in the sheet." And: NAMED originals, all 25, not
the anonymised copies. "we're doing it to have all the documentation at one place."

WHAT THIS BUILDS
  Drive folder "RM Internal Hiring 2026 - Full Documentation"
    - one subfolder per candidate, NAMED, holding their original submitted files exactly as
      they arrived (case study + resume, and any second file or superseded version)
    - "RM Internal Hiring 2026 - Documentation Index" spreadsheet:
        Tab "Round Documents" - the benchmark answer key, the answer-by-answer evaluation, the
            evaluation report, the marked-scripts sheet and the tracker, each hyperlinked
        Tab "Submissions"     - all 25: name, code, final score, outcome against the 70% bar,
            and a hyperlink to every file they submitted

🔴 THIS FOLDER IS NAMED, NOT ANONYMISED. It is the hiring record, not an evaluator pack. The
anonymised set stays where it is and is what an evaluator should ever be given.

Originals were re-pulled from the mailbox by SENDER ADDRESS with no subject filter (a subject
filter is how a second file was nearly missed on the first pass), into
output/rm_marking/originals/. Bushra Karim submitted Drive links rather than attachments, so
hers were fetched from Drive.
"""

import json
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaFileUpload

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = os.path.join(ROOT, ".claude", "config", "token_sheets_broad.json")
KEEP = os.path.join(ROOT, "output", "rm_marking")
ORIG = os.path.join(KEEP, "originals")
FOLDER_NAME = "RM Internal Hiring 2026 - Full Documentation"

# Round-level documents that already exist. Nothing here is created or renamed.
ROUND_DOCS = [
    ("Benchmark answer key (the standard every submission was marked against)",
     "Google Doc",
     "https://docs.google.com/document/d/1pCwMsjq6RY6jhTZubTdif6np5jsboocBVk-2pZIE9_g/edit"),
    # 🔴 Do NOT link 1D_CTT66MCw8rx4ilja_50s2Im4mkaWGZ here: that file is
    # "Benchmark Answer Key (Rev 2, DRAFT for QA).pdf", a superseded draft. Ayesha caught
    # it in the index 2026-09-08. Below is the current export, the exact PDF the 8
    # candidates received as an attachment.
    ("Benchmark answer key, PDF (the exact file attached to the candidate emails)", "PDF",
     "https://drive.google.com/file/d/1ouFEBtT_OQrm-TolbnxAKZBzTOnD5piD/view"),
    ("Case study evaluation report (all 25 scored, method and findings)", "Google Doc",
     "https://docs.google.com/document/d/1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc/edit"),
    ("Marked scripts, answer by answer, for the 8 below the 70% bar", "Google Sheet",
     "https://docs.google.com/spreadsheets/d/1tSl69wejsDdOBHppfqQXOpCC1HEdhCXNTBltcaNBt8k/edit"),
    ("Individual feedback workbooks sent to the 8 below the bar", "Drive folder",
     "https://drive.google.com/drive/folders/1eqrwZerEU6fj8cuibHqXWgJLvF1jJQrx"),
    ("Case study tracker (Master Key, Evaluation, Scores)", "Google Sheet",
     "https://docs.google.com/spreadsheets/d/1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8/edit"),
    ("Case studies, ANONYMISED (this is the set to give an evaluator)", "Drive folder",
     "https://drive.google.com/drive/folders/1itkyxaIabK54IdKw7fJU5dMbXznQjlom"),
    ("All 25 case study submissions, NAMED originals (this folder)", "Drive folder",
     "https://drive.google.com/drive/folders/1hIhLcu9TSLVptef9STFKZQ6CQ6lMebVn"),
]

NAVY = {"red": 0.102, "green": 0.169, "blue": 0.298}
WHITE = {"red": 1, "green": 1, "blue": 1}
GREENBG = {"red": 0.933, "green": 0.969, "blue": 0.945}
REDBG = {"red": 1.0, "green": 0.961, "blue": 0.961}
AMBER = {"red": 0.992, "green": 0.965, "blue": 0.925}
MIME = {".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}


def svc():
    c = Credentials.from_authorized_user_file(TOKEN)
    if c.expired and c.refresh_token:
        c.refresh(Request())
    return gbuild("sheets", "v4", credentials=c), gbuild("drive", "v3", credentials=c)


def txt(s, bold=False, size=10, colour=None, bg=None, halign=None):
    fmt = {"textFormat": {"bold": bold, "fontSize": size, "fontFamily": "Georgia"},
           "wrapStrategy": "WRAP", "verticalAlignment": "TOP"}
    if colour:
        fmt["textFormat"]["foregroundColor"] = colour
    if bg:
        fmt["backgroundColor"] = bg
    if halign:
        fmt["horizontalAlignment"] = halign
    return {"userEnteredValue": {"stringValue": str(s)}, "userEnteredFormat": fmt}


def link(url, label, bg=None):
    fmt = {"textFormat": {"fontSize": 10, "fontFamily": "Georgia"}, "wrapStrategy": "WRAP",
           "verticalAlignment": "TOP"}
    if bg:
        fmt["backgroundColor"] = bg
    lab = label.replace('"', "'")
    return {"userEnteredValue": {"formulaValue": f'=HYPERLINK("{url}","{lab}")'},
            "userEnteredFormat": fmt}


def num(v, bold=False, bg=None):
    return {"userEnteredValue": {"numberValue": v},
            "userEnteredFormat": {"textFormat": {"bold": bold, "fontSize": 10,
                                                 "fontFamily": "Georgia"},
                                  "horizontalAlignment": "CENTER", "backgroundColor": bg}
            if bg else {"textFormat": {"bold": bold, "fontSize": 10, "fontFamily": "Georgia"},
                        "horizontalAlignment": "CENTER"}}


def R(cells):
    return {"values": cells}


def find_or_make(drive, name, parent=None):
    q = (f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' "
         "and trashed = false")
    if parent:
        q += f" and '{parent}' in parents"
    got = drive.files().list(q=q, fields="files(id,name)").execute()["files"]
    if got:
        return got[0]["id"]
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent:
        body["parents"] = [parent]
    return drive.files().create(body=body, fields="id").execute()["id"]


def main():
    pulled = json.load(open(os.path.join(ORIG, "_pulled.json"), encoding="utf-8"))
    strict = json.load(open(os.path.join(KEEP, "strict_scores.json"), encoding="utf-8"))
    below = set(json.load(open(os.path.join(KEEP, "qbq.json"), encoding="utf-8")))
    sheets, drive = svc()

    root = find_or_make(drive, FOLDER_NAME)
    print(f"Folder: https://drive.google.com/drive/folders/{root}\n")

    uploaded, subfolder = {}, {}
    for code in sorted(pulled, key=lambda c: pulled[c]["name"]):
        nm = pulled[code]["name"]
        d = os.path.join(ORIG, code)
        if not os.path.isdir(d):
            print(f"  {code} {nm}: NO LOCAL FILES")
            uploaded[code] = []
            continue
        sub = find_or_make(drive, f"{code} {nm}", root)
        have = {f["name"]: f["id"] for f in drive.files().list(
            q=f"'{sub}' in parents and trashed = false",
            fields="files(id,name)", pageSize=200).execute()["files"]}
        rows = []
        for fn in sorted(os.listdir(d)):
            path = os.path.join(d, fn)
            ext = os.path.splitext(fn)[1].lower()
            if not os.path.isfile(path) or ext not in MIME:
                continue
            if fn in have:
                fid = have[fn]
            else:
                fid = drive.files().create(
                    body={"name": fn, "parents": [sub]},
                    media_body=MediaFileUpload(path, mimetype=MIME[ext], resumable=False),
                    fields="id").execute()["id"]
            rows.append((fn, f"https://drive.google.com/file/d/{fid}/view"))
        uploaded[code] = rows
        subfolder[code] = f"https://drive.google.com/drive/folders/{sub}"
        print(f"  {code}  {nm[:24]:24} {len(rows)} file(s)")

    # ---------- Round Documents tab ----------
    d1 = [R([txt("RM Internal Hiring 2026 - Round Documents", bold=True, size=14,
                 colour=WHITE, bg=NAVY)]),
          R([txt("Everything that defines how this round was run and judged. The benchmark was "
                 "written and reviewed before any submission was opened.", size=10)]),
          R([]),
          R([txt("Document", bold=True, colour=WHITE, bg=NAVY),
             txt("Type", bold=True, colour=WHITE, bg=NAVY),
             txt("Open", bold=True, colour=WHITE, bg=NAVY)])]
    for label, kind, url in ROUND_DOCS:
        d1.append(R([txt(label), txt(kind), link(url, "Open")]))
    d1 += [R([]),
           R([txt("Note: the submissions in this folder are the NAMED originals. If a set is "
                  "needed for an evaluator, use the anonymised folder linked above instead.",
                  size=10, bg=AMBER)])]

    # ---------- Submissions tab ----------
    maxf = max((len(v) for v in uploaded.values()), default=1)
    hdr = ["Name", "Code", "Score /100", "Outcome", "Folder"] + \
          [f"File {i + 1}" for i in range(maxf)]
    d2 = [R([txt(h, bold=True, colour=WHITE, bg=NAVY,
                 halign="CENTER" if h in ("Code", "Score /100") else None) for h in hdr])]
    for code in sorted(uploaded, key=lambda c: -strict[c]["total"]):
        nm = pulled[code]["name"]
        tot = strict[code]["total"]
        cleared = code not in below
        cells = [txt(nm, bold=True), txt(code, halign="CENTER"),
                 num(tot, bold=True, bg=GREENBG if cleared else REDBG),
                 txt("Met the 70% benchmark" if cleared else "Below the 70% benchmark",
                     bg=GREENBG if cleared else REDBG),
                 link(subfolder[code], "Open folder") if subfolder.get(code)
                 else txt("")]
        for fn, url in uploaded[code]:
            cells.append(link(url, fn))
        cells += [txt("")] * (maxf - len(uploaded[code]))
        d2.append(R(cells))

    ss = sheets.spreadsheets().create(body={
        "properties": {"title": "RM Internal Hiring 2026 - Documentation Index"},
        "sheets": [
            {"properties": {"title": "Round Documents",
                            "gridProperties": {"rowCount": len(d1) + 4, "columnCount": 3}},
             "data": [{"startRow": 0, "startColumn": 0, "rowData": d1}]},
            {"properties": {"title": "Submissions",
                            "gridProperties": {"rowCount": len(d2) + 4,
                                               "columnCount": len(hdr),
                                               "frozenRowCount": 1}},
             "data": [{"startRow": 0, "startColumn": 0, "rowData": d2}]},
        ]}).execute()
    sid = ss["spreadsheetId"]
    ids = {s["properties"]["title"]: s["properties"]["sheetId"] for s in ss["sheets"]}
    reqs = []
    for col, w in [(0, 520), (1, 110), (2, 90)]:
        reqs.append({"updateDimensionProperties": {"range": {
            "sheetId": ids["Round Documents"], "dimension": "COLUMNS",
            "startIndex": col, "endIndex": col + 1},
            "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    for col, w in [(0, 190), (1, 70), (2, 85), (3, 190), (4, 110)]:
        reqs.append({"updateDimensionProperties": {"range": {
            "sheetId": ids["Submissions"], "dimension": "COLUMNS",
            "startIndex": col, "endIndex": col + 1},
            "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    reqs.append({"updateDimensionProperties": {"range": {
        "sheetId": ids["Submissions"], "dimension": "COLUMNS",
        "startIndex": 5, "endIndex": 5 + maxf},
        "properties": {"pixelSize": 300}, "fields": "pixelSize"}})
    for rr in (0, 1):
        reqs.append({"mergeCells": {"range": {
            "sheetId": ids["Round Documents"], "startRowIndex": rr, "endRowIndex": rr + 1,
            "startColumnIndex": 0, "endColumnIndex": 3}, "mergeType": "MERGE_ALL"}})
    reqs.append({"mergeCells": {"range": {
        "sheetId": ids["Round Documents"], "startRowIndex": len(d1) - 1,
        "endRowIndex": len(d1), "startColumnIndex": 0, "endColumnIndex": 3},
        "mergeType": "MERGE_ALL"}})
    sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": reqs}).execute()
    drive.files().update(fileId=sid, addParents=root, fields="id,parents").execute()

    total_files = sum(len(v) for v in uploaded.values())
    print(f"\nIndex sheet: https://docs.google.com/spreadsheets/d/{sid}/edit")
    print(f"Folder:      https://drive.google.com/drive/folders/{root}")
    print(f"{len(uploaded)} candidates, {total_files} files uploaded, "
          f"{len(ROUND_DOCS)} round documents linked.")
    print("NOT link-shared. These are named originals: share deliberately.")


if __name__ == "__main__":
    sys.exit(main())
