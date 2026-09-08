"""
RM internal case study - ONE private workbook per candidate, for the 8 below the 70% bar.

Ayesha, 2026-09-08: "can you now make separate sheets for each? so when we send emails to them,
we can give them the visibility."

WHY SEPARATE FILES
  The master marked-scripts sheet has all 8 on tabs side by side. That file can never be sent to
  a candidate: internal staff would see each other's marks. This builds one standalone workbook
  per person containing ONLY their own script, and asserts that no other candidate's code or name
  appears anywhere in it before the file is written.

EACH WORKBOOK
  Tab 1 "Your Case Study"  - result against the 70% bar, examiner's comment, What's good /
                             What's missing, then Q1-Q10 with max, awarded, the 0-5 anchor,
                             what they wrote and what would have scored higher.
  Tab 2 "How this was marked" - the anchor-to-points conversion, the point value of every
                             question, and the plain-English wording of any marking cap that
                             applied to them. Nothing hidden.

OUTPUT
  - A Google Sheet per candidate inside a private Drive folder (NOT link-shared: sharing is
    left to Ayesha, or the .xlsx is attached to the email instead).
  - An .xlsx export per candidate in output/rm_marking/individual/ ready to attach.

Source of truth is unchanged: output/rm_marking/{strict_scores,qbq,roster}.json. Nothing is
re-scored or re-worded here.
"""

import io
import json
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaIoBaseDownload

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = os.path.join(ROOT, ".claude", "config", "token_sheets_broad.json")
KEEP = os.path.join(ROOT, "output", "rm_marking")
OUTX = os.path.join(KEEP, "individual")
FOLDER_NAME = "RM Case Study - Individual Feedback (below 70)"

PTS = {"Q1": 10, "Q2": 15, "Q3": 10, "Q4": 15, "Q5": 10,
       "Q6": 10, "Q7": 10, "Q8": 10, "Q9": 10}
TITLE = {
    "Q1": "Q1 - The 10 pieces of information you would want",
    "Q2": "Q2 - Is Urban outperforming Rural?",
    "Q3": "Q3 - Three root causes + how you would test each",
    "Q4": "Q4 - Forced prioritisation of the activity table",
    "Q5": 'Q5 - The Director says "everything is a priority"',
    "Q6": "Q6 - Coach leadership: A, B, C and D",
    "Q7": "Q7 - The experiment decision",
    "Q8": "Q8 - Stakeholder conflict plan",
    "Q9": "Q9 - Your first 72 hours",
    "Q10": "Q10 - The five-minute executive response",
}
CAP_TEXT = {
    "C1": "Question 2: the below-grade-level figures were read as shares of the whole student "
          "population rather than as a pass rate within a subgroup.",
    "C1a": "Question 2: the below-grade-level figures were read as shares of the whole student "
           "population rather than as a pass rate within a subgroup, and that reading drove the "
           "verdict.",
    "C1b": "Question 2: the below-grade-level figures were read as shares of the whole student "
           "population rather than as a pass rate within a subgroup. The verdict still held on "
           "the other dimensions, so this cost one band rather than the question.",
    "C2": "Question 4: no arithmetic was shown, or the percentages did not sum. This is the "
          "question whose whole point is that the numbers close and can be checked.",
    "C3": "Question 4: a Very High activity was paused or dropped. Those are redesigned, "
          "never removed.",
    "C4": "Question 4: exactly 15 points were cut, and the +25% observation demand was never "
          "priced, so the real gap was left unaddressed.",
    "C5": "Question 7: the answer did not choose one option.",
    "C6": "A structural element the question explicitly names was absent across the answer "
          "(for example Q1 'where from', one of Q8's five columns, Q6's escalation trigger, "
          "or Q9's deprioritisation).",
    "C7": "Question not attempted.",
}
ANCHOR_SCALE = [
    ("5", "Meets or beats the benchmark answer on every part the question names"),
    ("4", "Strong, with one part thin or missing"),
    ("3", "Sound but conventional, or a required element absent"),
    ("2", "Partial. Addresses the question but leaves most of it unevidenced"),
    ("1", "Named the area without answering it"),
    ("0", "Not attempted"),
]

NAVY = {"red": 0.102, "green": 0.169, "blue": 0.298}
WHITE = {"red": 1, "green": 1, "blue": 1}
GREEN = {"red": 0.106, "green": 0.498, "blue": 0.302}
RED = {"red": 0.702, "green": 0.149, "blue": 0.118}
AMBER = {"red": 0.992, "green": 0.965, "blue": 0.925}
GREENBG = {"red": 0.933, "green": 0.969, "blue": 0.945}
REDBG = {"red": 1.0, "green": 0.961, "blue": 0.961}
GREYBG = {"red": 0.961, "green": 0.969, "blue": 0.980}


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


def num(v, bold=False, bg=None):
    fmt = {"textFormat": {"bold": bold, "fontSize": 10, "fontFamily": "Georgia"},
           "horizontalAlignment": "CENTER", "verticalAlignment": "TOP"}
    if bg:
        fmt["backgroundColor"] = bg
    return {"userEnteredValue": {"numberValue": v}, "userEnteredFormat": fmt}


def R(cells):
    return {"values": cells}


def main():
    st = json.load(open(os.path.join(KEEP, "strict_scores.json"), encoding="utf-8"))
    qbq = json.load(open(os.path.join(KEEP, "qbq.json"), encoding="utf-8"))
    roster = json.load(open(os.path.join(KEEP, "roster.json"), encoding="utf-8"))
    codes = sorted(qbq, key=lambda k: st[k]["total"])
    os.makedirs(OUTX, exist_ok=True)
    sheets, drive = svc()

    q = (f"name = '{FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' "
         "and trashed = false")
    got = drive.files().list(q=q, fields="files(id,name)").execute()["files"]
    folder = got[0]["id"] if got else drive.files().create(
        body={"name": FOLDER_NAME, "mimeType": "application/vnd.google-apps.folder"},
        fields="id").execute()["id"]

    others = {c: roster[c]["name"] for c in roster}
    out = {}
    for cd in codes:
        r, qa, nm = st[cd], qbq[cd], roster[cd]["name"]

        rows = [
            R([txt(f"{nm} - Regional Manager case study", bold=True, size=15,
                   colour=WHITE, bg=NAVY)]),
            R([txt("Result: below the 70% benchmark, so this application does not move to the "
                   "next stage.", bold=True, size=11, colour=RED, bg=REDBG)]),
            R([txt(f"Your total: {r['total']:.0f} out of 100.    The benchmark to move forward "
                   f"was 70.", bold=True, size=11)]),
            R([txt("Marked against the published Regional Manager benchmark answer key, which was "
                   "written and reviewed before any submission was opened. Every question below "
                   "shows the marks available, the marks awarded, what your answer did, and what "
                   "would have scored higher.", size=9)]),
            R([]),
            R([txt("OVERALL", bold=True, size=9, colour=WHITE, bg=NAVY)]),
            R([txt(r["notes"], size=10)]),
            R([]),
            R([txt("WHAT WAS GOOD", bold=True, size=9, colour=WHITE, bg=GREEN)]),
        ]
        for s in r.get("strengths", []) or ["-"]:
            rows.append(R([txt(s, size=10, bg=GREENBG)]))
        rows += [R([]), R([txt("WHAT WAS MISSING", bold=True, size=9, colour=WHITE, bg=RED)])]
        for g in r.get("gaps", []) or ["-"]:
            rows.append(R([txt(g, size=10, bg=REDBG)]))
        rows += [
            R([]),
            R([txt(h, bold=True, colour=WHITE, bg=NAVY,
                   halign="CENTER" if h in ("Marks available", "Marks awarded", "Band /5")
                   else None)
               for h in ["Question", "Marks available", "Marks awarded", "Band /5",
                         "What your answer did", "What would have scored higher"]]),
        ]
        for qq in list(PTS) + ["Q10"]:
            a = qa["qa"].get(qq, {})
            if qq == "Q10":
                rows.append(R([txt(TITLE[qq], bold=True), txt("not scored", halign="CENTER"),
                               txt(r.get("q10band", ""), bold=True, halign="CENTER"),
                               txt("-", halign="CENTER"),
                               txt(a.get("answered", "-")), txt(a.get("better", "-"))]))
            else:
                aw, mx = r["q"][qq], PTS[qq]
                bg = REDBG if aw / mx < 0.5 else (AMBER if aw / mx < 0.7 else None)
                rows.append(R([txt(TITLE[qq], bold=True), num(mx), num(aw, bold=True, bg=bg),
                               num(r["anchors"][qq]),
                               txt(a.get("answered", "-")), txt(a.get("better", "-"))]))

        m2 = [
            R([txt("How this was marked", bold=True, size=14, colour=WHITE, bg=NAVY)]),
            R([txt("Each question was given a band from 0 to 5 against the benchmark answer, then "
                   "converted to the point value the case itself prints for that question. "
                   "Question 10 carries no printed points in the case, so it is described but "
                   "not scored and is not part of the total.", size=10)]),
            R([]),
            R([txt("Band", bold=True, colour=WHITE, bg=NAVY, halign="CENTER"),
               txt("What it means", bold=True, colour=WHITE, bg=NAVY)]),
        ]
        for b, meaning in ANCHOR_SCALE:
            m2.append(R([txt(b, halign="CENTER", bold=True), txt(meaning)]))
        m2 += [
            R([]),
            R([txt("Question", bold=True, colour=WHITE, bg=NAVY),
               txt("Marks available", bold=True, colour=WHITE, bg=NAVY, halign="CENTER")]),
        ]
        for qq in PTS:
            m2.append(R([txt(TITLE[qq]), num(PTS[qq])]))
        m2.append(R([txt("Total", bold=True), num(100, bold=True)]))
        if r["caps"]:
            m2 += [R([]),
                   R([txt("Marking rules that applied to your answer", bold=True, size=9,
                          colour=WHITE, bg=NAVY)]),
                   R([txt("These are fixed rules in the benchmark, applied the same way to every "
                          "submission.", size=9)])]
            for c in r["caps"]:
                m2.append(R([txt(CAP_TEXT.get(c, c), size=10, bg=AMBER)]))

        body = {"properties": {"title": f"RM Case Study Feedback - {nm}"},
                "sheets": [
                    {"properties": {"title": "Your Case Study",
                                    "gridProperties": {"rowCount": len(rows) + 4,
                                                       "columnCount": 6}},
                     "data": [{"startRow": 0, "startColumn": 0, "rowData": rows}]},
                    {"properties": {"title": "How this was marked",
                                    "gridProperties": {"rowCount": len(m2) + 4,
                                                       "columnCount": 2}},
                     "data": [{"startRow": 0, "startColumn": 0, "rowData": m2}]},
                ]}

        # ---- privacy assert: nobody else's name or code may appear ----
        blob = json.dumps(body, ensure_ascii=False)
        for oc, on in others.items():
            if oc == cd:
                continue
            assert oc not in blob, f"{cd}: leaked code {oc}"
            assert on not in blob, f"{cd}: leaked name {on}"

        ss = sheets.spreadsheets().create(body=body).execute()
        sid = ss["spreadsheetId"]
        ids = {s["properties"]["title"]: s["properties"]["sheetId"] for s in ss["sheets"]}
        reqs = []
        for col, w in [(0, 250), (1, 110), (2, 110), (3, 70), (4, 430), (5, 470)]:
            reqs.append({"updateDimensionProperties": {"range": {
                "sheetId": ids["Your Case Study"], "dimension": "COLUMNS",
                "startIndex": col, "endIndex": col + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"}})
        for col, w in [(0, 300), (1, 620)]:
            reqs.append({"updateDimensionProperties": {"range": {
                "sheetId": ids["How this was marked"], "dimension": "COLUMNS",
                "startIndex": col, "endIndex": col + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"}})
        n_s = len(r.get("strengths", []) or ["-"])
        n_g = len(r.get("gaps", []) or ["-"])
        merge = [0, 1, 2, 3, 5, 6, 8] + list(range(9, 9 + n_s))
        gh = 9 + n_s + 1
        merge += [gh] + list(range(gh + 1, gh + 1 + n_g))
        for rr in merge:
            reqs.append({"mergeCells": {"range": {
                "sheetId": ids["Your Case Study"], "startRowIndex": rr, "endRowIndex": rr + 1,
                "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}})
        for rr in [0, 1]:
            reqs.append({"mergeCells": {"range": {
                "sheetId": ids["How this was marked"], "startRowIndex": rr, "endRowIndex": rr + 1,
                "startColumnIndex": 0, "endColumnIndex": 2}, "mergeType": "MERGE_ALL"}})
        sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": reqs}).execute()

        drive.files().update(fileId=sid, addParents=folder, fields="id,parents").execute()

        xlsx = os.path.join(OUTX, f"RM Case Study Feedback - {nm}.xlsx")
        req = drive.files().export_media(
            fileId=sid,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
        with open(xlsx, "wb") as fh:
            fh.write(buf.getvalue())

        out[cd] = {"name": nm, "total": r["total"],
                   "url": f"https://docs.google.com/spreadsheets/d/{sid}/edit", "xlsx": xlsx}
        print(f"  {cd}  {nm:20} {r['total']:5.0f}/100   {os.path.getsize(xlsx)/1024:6.1f} KB   "
              f"{out[cd]['url']}")

    json.dump(out, open(os.path.join(KEEP, "individual_links.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(f"\nFolder: https://drive.google.com/drive/folders/{folder}")
    print("NOT link-shared. Attach the .xlsx to the email, or share per person deliberately.")
    print(f"xlsx: {OUTX}")


if __name__ == "__main__":
    sys.exit(main())
