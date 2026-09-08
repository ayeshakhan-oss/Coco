"""
RM internal case study - MARKED SCRIPTS sheet for the 8 candidates below the 70% bar.

Ayesha, 2026-09-08: "can you do it like you're checking an exam? Like score them on their case
study? For candidates below 70%. This will give more visibility and transparency ... make a copy
of those and score them on the case study and mention under it what is missing and whats good and
then score them?"

WHAT THIS BUILDS
  A NEW spreadsheet (the tracker is left untouched), laid out like a marked exam script:
    - "Summary" tab: the 8, per-question marks out of the case's own point values, total vs the
      70 bar, Q10 band, and which mechanical caps fired.
    - One tab per candidate: name, total, verdict, the examiner's overall comment, then an
      explicit "What's good" block and "What's missing" block, then a per-question marking table
      (Q1-Q10) with max, awarded, the 0-5 anchor, what they wrote and what would have scored
      higher. Each tab links to that candidate's anonymised script on Drive.

SOURCE OF TRUTH - nothing is re-scored or re-worded here
  strict_scores.json  marks, 0-5 anchors, caps, overall notes, strengths, gaps  (strict re-mark)
  qbq.json            per-question "answered" / "better" from the full read of all 8
  Both live in the 2026-09-02 session scratchpad; copied into output/rm_marking/ by this script
  so the sheet can be rebuilt without depending on a temp directory.

Marks convert the 0-5 anchor pro-rata to the case's printed point values
(Q1 10, Q2 15, Q3 10, Q4 15, Q5 10, Q6 10, Q7 10, Q8 10, Q9 10 = 100), exactly as the benchmark
specifies. Q10 carries no printed points and is banded only.

🔴 NOTE FOR AYESHA: the tracker's own "Scores" tab still holds the SUPERSEDED first pass
(mean 88.3, nobody below 70). The strict re-mark (mean 75.0, 8 below 70) never got written back
to it. This script does not touch it - see the console warning it prints.
"""

import json
import os
import shutil
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TOKEN = os.path.join(ROOT, ".claude", "config", "token_sheets_broad.json")
SRC = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
       r"\7a2e7743-8713-4f95-9dd1-44dbccb04afa\scratchpad")
KEEP = os.path.join(ROOT, "output", "rm_marking")
TRACKER = "1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8"

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
    "C1": "Q2 capped - below-grade-level figures misread as composition shares",
    "C1a": "Q2 capped at 2 - misread the below-grade-level figures as composition shares AND the "
           "misreading drives the verdict",
    "C1b": "Q2 dropped one anchor - misread the below-grade-level figures, but the verdict stands "
           "on the other five axes",
    "C2": "Q4 capped at 1 - no arithmetic shown, or percentages that do not sum",
    "C3": "Q4 capped at 2 - pauses or drops a Very High activity",
    "C4": "Q4 capped at 3 - cuts exactly 15pp and never prices the +25% demand",
    "C5": "Q7 capped at 2 - refuses to choose one option",
    "C6": "Question capped at 3 - a required structural element is absent across the answer",
    "C7": "Not attempted - 0",
}

NAVY = {"red": 0.102, "green": 0.169, "blue": 0.298}
WHITE = {"red": 1, "green": 1, "blue": 1}
GREEN = {"red": 0.106, "green": 0.498, "blue": 0.302}
RED = {"red": 0.702, "green": 0.149, "blue": 0.118}
LIGHT = {"red": 0.961, "green": 0.969, "blue": 0.980}
AMBER = {"red": 0.992, "green": 0.965, "blue": 0.925}
GREENBG = {"red": 0.933, "green": 0.969, "blue": 0.945}
REDBG = {"red": 1.0, "green": 0.961, "blue": 0.961}


def load():
    os.makedirs(KEEP, exist_ok=True)
    data = {}
    for fn in ("strict_scores.json", "qbq.json"):
        src, dst = os.path.join(SRC, fn), os.path.join(KEEP, fn)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        if not os.path.exists(dst):
            raise SystemExit(f"missing {fn} in both {SRC} and {KEEP}")
        data[fn] = json.load(open(dst, encoding="utf-8"))
    roster = json.load(open(os.path.join(
        r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
        r"\eaaa3c0c-acd7-4d18-9dfc-96577ff44593\scratchpad", "rm_roster.json"), encoding="utf-8"))
    json.dump(roster, open(os.path.join(KEEP, "roster.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    return data["strict_scores.json"], data["qbq.json"], roster


def svc():
    c = Credentials.from_authorized_user_file(TOKEN)
    if c.expired and c.refresh_token:
        c.refresh(Request())
    return gbuild("sheets", "v4", credentials=c), gbuild("drive", "v3", credentials=c)


def txt(s, bold=False, size=10, colour=None, wrap=True, bg=None, halign=None):
    fmt = {"textFormat": {"bold": bold, "fontSize": size,
                          "fontFamily": "Georgia"},
           "wrapStrategy": "WRAP" if wrap else "OVERFLOW_CELL",
           "verticalAlignment": "TOP"}
    if colour:
        fmt["textFormat"]["foregroundColor"] = colour
    if bg:
        fmt["backgroundColor"] = bg
    if halign:
        fmt["horizontalAlignment"] = halign
    return {"userEnteredValue": {"stringValue": str(s)}, "userEnteredFormat": fmt}


def num(v, bold=False, bg=None, colour=None):
    fmt = {"textFormat": {"bold": bold, "fontSize": 10, "fontFamily": "Georgia"},
           "horizontalAlignment": "CENTER", "verticalAlignment": "TOP"}
    if bg:
        fmt["backgroundColor"] = bg
    if colour:
        fmt["textFormat"]["foregroundColor"] = colour
    return {"userEnteredValue": {"numberValue": v}, "userEnteredFormat": fmt}


def row(cells):
    return {"values": cells}


def build():
    st, qbq, roster = load()
    codes = sorted(qbq, key=lambda k: st[k]["total"])
    sheets, drive = svc()

    # ---------- Summary tab ----------
    hdr = ["Code", "Name", "Total /100", "vs 70 bar", "Q10 band"] + \
          [f"{q} /{PTS[q]}" for q in PTS] + ["Caps applied"]
    srows = [row([txt(h, bold=True, colour=WHITE, bg=NAVY, halign="CENTER") for h in hdr])]
    for cd in codes:
        r = st[cd]
        gap = round(r["total"] - 70, 1)
        srows.append(row(
            [txt(cd, bold=True), txt(roster[cd]["name"], bold=True),
             num(r["total"], bold=True, bg=REDBG, colour=RED),
             txt(f"{gap:+.1f}", halign="CENTER", colour=RED),
             txt(r.get("q10band", ""), halign="CENTER")] +
            [num(r["q"][q]) for q in PTS] +
            [txt(", ".join(r["caps"]) or "-")]))
    summary = {
        "properties": {"title": "Summary", "gridProperties": {
            "rowCount": len(srows) + 6, "columnCount": len(hdr), "frozenRowCount": 1}},
        "data": [{"startRow": 0, "startColumn": 0, "rowData": srows}],
    }

    # ---------- one tab per candidate ----------
    tabs = [summary]
    for cd in codes:
        r, qa = st[cd], qbq[cd]
        nm = roster[cd]["name"]
        link = roster[cd].get("link", "")
        rows = [
            row([txt(f"{nm}   ({cd})", bold=True, size=15, colour=WHITE, bg=NAVY)]),
            row([txt(f"Total {r['total']:.0f}/100   ·   {r['total'] - 70:+.0f} against the "
                     f"published 70% bar   ·   Q10: {r.get('q10band', '')}   ·   "
                     f"Result: below the bar", bold=True, size=11, colour=RED, bg=REDBG)]),
            row([txt("Marked against docs/case_studies/benchmarks/rm_regional_manager_benchmark.md "
                     "(Rev 2). Each question's 0-5 anchor converts pro-rata to the point value "
                     "printed in the case. Q10 carries no printed points and is banded only.",
                     size=9)]),
        ]
        if link:
            rows.append(row([{"userEnteredValue": {
                "formulaValue": f'=HYPERLINK("{link}","Open {cd} case study (anonymised)")'},
                "userEnteredFormat": {"textFormat": {"fontSize": 10, "fontFamily": "Georgia"}}}]))
        rows += [
            row([]),
            row([txt("EXAMINER'S OVERALL COMMENT", bold=True, size=9, colour=WHITE, bg=NAVY)]),
            row([txt(r["notes"], size=10)]),
            row([]),
            row([txt("WHAT'S GOOD", bold=True, size=9, colour=WHITE, bg=GREEN)]),
        ]
        for s in r.get("strengths", []) or ["-"]:
            rows.append(row([txt(f"+   {s}", size=10, bg=GREENBG)]))
        rows += [row([]), row([txt("WHAT'S MISSING", bold=True, size=9, colour=WHITE, bg=RED)])]
        for g in r.get("gaps", []) or ["-"]:
            rows.append(row([txt(f"-   {g}", size=10, bg=REDBG)]))
        if r["caps"]:
            rows += [row([]),
                     row([txt("MARKING CAPS THAT FIRED (applied mechanically from the "
                              "benchmark, not by feel)", bold=True, size=9, colour=WHITE,
                              bg=NAVY)])]
            for c in r["caps"]:
                rows.append(row([txt(f"{c}   {CAP_TEXT.get(c, '')}", size=10, bg=AMBER)]))
        rows += [
            row([]),
            row([txt(h, bold=True, colour=WHITE, bg=NAVY,
                     halign="CENTER" if h in ("Max", "Awarded", "Anchor /5") else None)
                 for h in ["Question", "Max", "Awarded", "Anchor /5",
                           "What they wrote, and what worked",
                           "What was missing / would have scored higher"]]),
        ]
        for q in list(PTS) + ["Q10"]:
            a = qa["qa"].get(q, {})
            if q == "Q10":
                rows.append(row([
                    txt(TITLE[q], bold=True), txt("-", halign="CENTER"),
                    txt(r.get("q10band", ""), bold=True, halign="CENTER"),
                    txt("-", halign="CENTER"),
                    txt(a.get("answered", "-")), txt(a.get("better", "-"))]))
            else:
                aw, mx = r["q"][q], PTS[q]
                bg = REDBG if aw / mx < 0.5 else (AMBER if aw / mx < 0.7 else None)
                rows.append(row([
                    txt(TITLE[q], bold=True), num(mx), num(aw, bold=True, bg=bg),
                    num(r["anchors"][q]),
                    txt(a.get("answered", "-")), txt(a.get("better", "-"))]))
        tabs.append({
            "properties": {"title": f"{cd} {nm}"[:99],
                           "gridProperties": {"rowCount": len(rows) + 6, "columnCount": 6,
                                              "frozenRowCount": 0}},
            "data": [{"startRow": 0, "startColumn": 0, "rowData": rows}],
        })

    ss = sheets.spreadsheets().create(body={
        "properties": {"title": "RM Case Study - Marked Scripts (below 70%)"},
        "sheets": tabs}).execute()
    sid = ss["spreadsheetId"]
    ids = {s["properties"]["title"]: s["properties"]["sheetId"] for s in ss["sheets"]}

    # ---------- widths, merges, alternating question rows ----------
    reqs = []
    sumid = ids["Summary"]
    for col, w in [(0, 70), (1, 150), (2, 80), (3, 80), (4, 90)]:
        reqs.append({"updateDimensionProperties": {"range": {
            "sheetId": sumid, "dimension": "COLUMNS", "startIndex": col,
            "endIndex": col + 1}, "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    reqs.append({"updateDimensionProperties": {"range": {
        "sheetId": sumid, "dimension": "COLUMNS", "startIndex": 5, "endIndex": 14},
        "properties": {"pixelSize": 62}, "fields": "pixelSize"}})
    reqs.append({"updateDimensionProperties": {"range": {
        "sheetId": sumid, "dimension": "COLUMNS", "startIndex": 14, "endIndex": 15},
        "properties": {"pixelSize": 200}, "fields": "pixelSize"}})

    for cd in codes:
        nm = roster[cd]["name"]
        tid = ids[f"{cd} {nm}"[:99]]
        for col, w in [(0, 250), (1, 50), (2, 70), (3, 70), (4, 430), (5, 470)]:
            reqs.append({"updateDimensionProperties": {"range": {
                "sheetId": tid, "dimension": "COLUMNS", "startIndex": col,
                "endIndex": col + 1}, "properties": {"pixelSize": w}, "fields": "pixelSize"}})
        # merge the single-column banner/comment rows across all six columns
        n_head = 4 if roster[cd].get("link") else 3
        merge_rows = list(range(0, n_head))
        merge_rows += [n_head + 1, n_head + 2]                      # comment header + body
        st_r = st[cd]
        cur = n_head + 4                                            # WHAT'S GOOD header
        merge_rows.append(cur)
        n_s = len(st_r.get("strengths", []) or ["-"])
        merge_rows += list(range(cur + 1, cur + 1 + n_s))
        cur = cur + 1 + n_s + 1
        merge_rows.append(cur)                                      # WHAT'S MISSING header
        n_g = len(st_r.get("gaps", []) or ["-"])
        merge_rows += list(range(cur + 1, cur + 1 + n_g))
        cur = cur + 1 + n_g
        if st_r["caps"]:
            cur += 1
            merge_rows.append(cur)
            merge_rows += list(range(cur + 1, cur + 1 + len(st_r["caps"])))
        for rr in merge_rows:
            reqs.append({"mergeCells": {"range": {
                "sheetId": tid, "startRowIndex": rr, "endRowIndex": rr + 1,
                "startColumnIndex": 0, "endColumnIndex": 6}, "mergeType": "MERGE_ALL"}})

    sheets.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": reqs}).execute()
    drive.permissions().create(fileId=sid, body={"role": "writer", "type": "anyone"}).execute()

    url = f"https://docs.google.com/spreadsheets/d/{sid}/edit"
    print(f"BUILT: {url}")
    print(f"  tabs: Summary + {len(codes)} marked scripts")
    for cd in codes:
        print(f"    {cd}  {roster[cd]['name']:20} {st[cd]['total']:5.0f}/100  "
              f"caps={','.join(st[cd]['caps']) or '-'}")
    print("\n  Source data copied to output/rm_marking/ so this is rebuildable.")
    print("  WARNING: the tracker's 'Scores' tab still holds the superseded first pass "
          "(mean 88.3, nobody below 70). Not touched by this script.")
    return url


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
