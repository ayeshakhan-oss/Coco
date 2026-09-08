"""
Repair the Band and Tier columns on the rows added 2026-09-08.

The first classifier took the first integer it found in a free-text tenure note. That is
wrong in both directions and produced an actively misleading column:
  - calendar years read as tenure  -> Javaria Abbas "8+" (her post is dated 2023)
  - connection counts read as tenure -> Sadaf Gul "8+" (from "26 connections")
  - hedged figures read as solid   -> "likely 4+" and "~4-6 MAY EXCEED CAP" read as IN BAND,
                                      which wrongly promoted two people to Tier 1

The replacement refuses to guess. It only calls a band when the note actually says so, and
otherwise says UNVERIFIED, optionally noting that seniority grade is the only proxy we have.
A column that admits it does not know beats one that quietly invents a number.
"""
import re
import sys

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

OAUTH = r"c:\Agent Coco\.claude\config\token_sheets_broad.json"
SID = "18oUr_4rcKJOEp3JRd2sY3GbhtMIbG92Xyr619IPkcLo"
TAB = "FM-50-Candidates"
FIRST_NEW_ROW = 117

OVER = re.compile(r"may exceed|likely over|over cap|over the cap|over band|against the cap|"
                  r"\b\d+\+|exceed the cap|breach", re.I)
BELOW = re.compile(r"below band|under 2 ?yrs|under two years", re.I)
ATCAP = re.compile(r"at the cap|at cap", re.I)
# "3 years", "3 yrs", "nearly 3 years", "1 year 10 months". Deliberately requires the WORD
# year/yr, so bare calendar years (2023) and "26 connections" cannot match.
TENURE = re.compile(r"(\d+)\s*(?:\+\s*)?(?:yrs?|years?)\b", re.I)
GRADE = re.compile(r"junior grade|entry grade|entry-level|graduate-entry|trainee|"
                   r"consultant development programme|management trainee|mt grade|"
                   r"assistant grade|junior consultant|jr\.", re.I)

FUNC_STRONG = re.compile(
    r"fundrais|partnership|resource mobilis|resource mobiliz|grant|donor|proposal|"
    r"philanthrop|bid\b|business development|resource development|sponsorship", re.I)
ISB = re.compile(r"islamabad|rawalpindi", re.I)


def band_of(note):
    n = note or ""
    if BELOW.search(n):
        return "BELOW BAND (<2 yrs)"
    if OVER.search(n):
        return "OVER-CAP RISK"
    if ATCAP.search(n):
        return "AT CAP (4 yrs)"
    yrs = [int(x) for x in TENURE.findall(n)]
    if yrs:
        lo = min(yrs)
        if lo <= 4:
            return "IN BAND (evidenced %dy)" % lo
        return "OVER-CAP RISK (%dy stated)" % lo
    if GRADE.search(n):
        return "UNVERIFIED (junior grade proxy)"
    return "UNVERIFIED"


def tier_of(band, title, why, org):
    blob = " ".join([title or "", why or "", org or ""])
    strong = bool(FUNC_STRONG.search(blob))
    if band.startswith("BELOW BAND") or band.startswith("OVER-CAP"):
        return "4"  # out of band on current evidence
    solid = band.startswith("IN BAND") or band.startswith("AT CAP")
    if solid and strong:
        return "1"
    if strong or (solid and not strong):
        return "2"
    return "3"


def main():
    apply = "--apply" in sys.argv
    creds = Credentials.from_authorized_user_file(
        OAUTH, ["https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/spreadsheets"])
    if not creds.valid:
        creds.refresh(Request())
        open(OAUTH, "w", encoding="utf-8").write(creds.to_json())
    sv = build("sheets", "v4", credentials=creds, cache_discovery=False).spreadsheets()

    vals = sv.values().get(spreadsheetId=SID,
                           range="%s!A%d:S200" % (TAB, FIRST_NEW_ROW)).execute().get("values", [])
    out, changed = [], 0
    for r in vals:
        def c(i):
            return r[i] if i < len(r) else ""
        nb = band_of(c(5))
        nt = tier_of(nb, c(3), c(11), c(2))
        if nb != c(12) or nt != c(14):
            changed += 1
            print("  %-26s %-30s -> %-30s  T%s->T%s" % (c(1)[:26], c(12)[:30], nb[:30], c(14), nt))
        out.append([nb, nt])

    print("\nrows %d  changed %d" % (len(out), changed))
    from collections import Counter
    print("NEW BANDS:", dict(Counter(b for b, t in out)))
    print("NEW TIERS:", dict(Counter(t for b, t in out)))
    if not apply:
        print("\nDRY RUN - pass --apply to write.")
        return

    sv.values().update(spreadsheetId=SID, range="%s!M%d" % (TAB, FIRST_NEW_ROW),
                       valueInputOption="RAW",
                       body={"values": [[b] for b, t in out]}).execute()
    sv.values().update(spreadsheetId=SID, range="%s!O%d" % (TAB, FIRST_NEW_ROW),
                       valueInputOption="RAW",
                       body={"values": [[t] for b, t in out]}).execute()
    print("wrote Band (M) and Tier (O) for %d rows" % len(out))


if __name__ == "__main__":
    main()
