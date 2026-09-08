"""
Clean up the FM Sourcing Master sheet in place, then extend it with the 2026-09-08
Fundraising & Partnerships (2-4 yr band) sourcing run.

Ayesha's instruction 2026-09-08: band = 2-4 years, Islamabad-first, clean up in place then extend.

NON-DESTRUCTIVE BY DESIGN. Out-of-band rows are TAGGED, never deleted: the 8+ and 5-7 cohorts
are a real asset for a future Head of Fundraising search, and deleting them is not reversible.
Snapshot lives at output/sourcing/FM_sheet_snapshot_2026_09_08.json before any write.

Usage:
    python scripts/sourcing/extend_fm_sheet_2026_09_08.py --dry-run
    python scripts/sourcing/extend_fm_sheet_2026_09_08.py --apply
"""
import argparse
import json
import glob
import os
import re
import sys
import unicodedata
from collections import defaultdict

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = r"c:\Agent Coco\tools\agent-coco-914edff20dde.json"
SID = "18oUr_4rcKJOEp3JRd2sY3GbhtMIbG92Xyr619IPkcLo"
TAB = "FM-50-Candidates"
SNAPSHOT = r"c:\Agent Coco\output\sourcing\FM_sheet_snapshot_2026_09_08.json"
CLUSTER_DIR = r"c:\Agent Coco\output\sourcing\clusters"

# Existing columns A-L, then the audit/extension columns we add.
NEW_HEADERS = ["Band", "Data Flag", "Tier", "Evidence / Source URL", "Sourced By", "Status"]
FIRST_NEW_COL = 12  # 0-indexed -> column M

STOP = {"dr", "mr", "ms", "mrs", "syed", "syeda", "muhammad", "mohammad", "bin", "obe", "prof", "the"}


def name_tokens(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return [t for t in re.split(r"[^a-z]+", s) if len(t) > 2 and t not in STOP]


def band_of(years):
    """Classify a Years cell into a band. Returns (band, in_band_bool)."""
    m = re.findall(r"\d+", years or "")
    if not m:
        return "UNKNOWN", False
    lo = int(m[0])
    if lo <= 4:
        return "2-4 IN BAND", True
    if lo <= 7:
        return "5-7", False
    return "8+", False


def url_flag(name, url):
    """Return a data flag for the LinkedIn cell, or '' if it looks sound."""
    if not url or url.strip().startswith("["):
        return "URL-PLACEHOLDER"
    m = re.search(r"linkedin\.com/in/([^/?\s]+)", url)
    if not m:
        return "URL-NOT-LINKEDIN"
    flat = re.sub(r"[^a-z]", "", m.group(1).lower())
    toks = name_tokens(name)
    if toks and not any(t in flat for t in toks):
        return "URL-UNVERIFIED-MISMATCH"
    return ""


def svc():
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    return build("sheets", "v4", credentials=creds, cache_discovery=False).spreadsheets()


def load_clusters():
    """Load every cluster JSON produced by the sourcing sweeps."""
    rows = []
    for path in sorted(glob.glob(os.path.join(CLUSTER_DIR, "*.json"))):
        data = json.load(open(path, encoding="utf-8"))
        # c3 was restructured to "verified_rows" after its fabrication purge, so that only
        # independently corroborated rows survive. Accept both key names.
        for r in data.get("rows", []) + data.get("verified_rows", []):
            r = dict(r)
            r["_cluster"] = data.get("cluster", os.path.basename(path))
            rows.append(r)
    return rows


def audit_existing(values):
    """Return (header, rows, per-row audit dicts) for the existing sheet."""
    hdr, data = values[0], values[1:]
    idx = {h.strip(): i for i, h in enumerate(hdr)}
    seen = defaultdict(list)
    for n, r in enumerate(data, start=2):
        nm = (r[idx["Name"]].strip() if idx["Name"] < len(r) else "")
        if nm:
            seen[nm.lower()].append(n)

    audits = []
    for n, r in enumerate(data, start=2):
        def cell(k):
            i = idx[k]
            return r[i].strip() if i < len(r) else ""

        nm, org, yrs, url, email = cell("Name"), cell("Organization"), cell("Years"), cell("LinkedIn"), cell("Email")
        if not nm:
            audits.append(None)
            continue
        band, _ = band_of(yrs)
        flags = []
        if "taleemabad" in org.lower() or "taleemabad.com" in email.lower():
            flags.append("OWN-STAFF - not a candidate")
        dupe_rows = [x for x in seen[nm.lower()] if x != n]
        if dupe_rows:
            flags.append("DUPLICATE of row " + ",".join(map(str, dupe_rows)))
        uf = url_flag(nm, url)
        if uf:
            flags.append(uf)
        audits.append({"row": n, "name": nm, "band": band,
                       "flag": "; ".join(flags) or "OK",
                       "source": "FM sheet 2026-05"})
    return hdr, data, audits


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(SNAPSHOT):
        sys.exit("ABORT: snapshot missing at %s. Never write to this sheet without one." % SNAPSHOT)

    s = svc()
    values = s.values().get(spreadsheetId=SID, range=TAB).execute().get("values", [])
    hdr, data, audits = audit_existing(values)
    live = [a for a in audits if a]

    print("EXISTING ROWS: %d" % len(live))
    from collections import Counter
    print("BANDS:", dict(Counter(a["band"] for a in live)))
    print("FLAGGED:", sum(1 for a in live if a["flag"] != "OK"))

    new_rows = load_clusters()
    print("\nNEW SOURCED ROWS: %d" % len(new_rows))
    print("  with verbatim URL: %d" % sum(1 for r in new_rows if r.get("url", "") != "NO_URL_FOUND"))
    by_c = Counter(r["_cluster"] for r in new_rows)
    for k, v in by_c.items():
        print("  %-40s %d" % (k, v))

    # The "Top picks" tab is a LIVE OUTREACH TRACKER for this exact role.
    # Anyone with Reached Out = TRUE has already been messaged by Ayesha. Re-sourcing
    # them risks a second cold approach to someone who already said no or already replied.
    contacted = {}
    tp = s.values().get(spreadsheetId=SID, range="Top picks").execute().get("values", [])
    if tp:
        th = {h.strip(): i for i, h in enumerate(tp[0])}
        for r in tp[1:]:
            def tc(k):
                i = th.get(k, -1)
                return r[i].strip() if 0 <= i < len(r) else ""
            nm = tc("Name")
            if nm and tc("Reached Out").upper() == "TRUE":
                contacted[nm.lower()] = tc("Comment") or tc("Responded") or "contacted, no note"
    print("\nALREADY CONTACTED (Top picks tracker): %d people" % len(contacted))

    # Dedupe new rows against BOTH the main tab and the outreach tracker.
    existing_names = {a["name"].lower() for a in live}
    fresh, dupes, already = [], [], []
    for r in new_rows:
        key = r["name"].lower()
        if key in contacted:
            already.append(r)
        elif key in existing_names:
            dupes.append(r)
        else:
            fresh.append(r)
    print("  DO NOT RE-CONTACT (already messaged): %d %s" % (len(already), [d["name"] for d in already]))
    print("  already in sheet, not yet contacted: %d %s" % (len(dupes), [d["name"] for d in dupes]))
    print("  genuinely new: %d" % len(fresh))

    if args.dry_run:
        print("\nDRY RUN - no writes performed.")
        return

    # ---- WRITE 1: header for the new audit columns
    s.values().update(
        spreadsheetId=SID,
        range="%s!%s1" % (TAB, chr(ord("A") + FIRST_NEW_COL)),
        valueInputOption="RAW",
        body={"values": [NEW_HEADERS]},
    ).execute()

    # ---- WRITE 2: audit columns for every existing row
    audit_block = []
    for a in audits:
        if a is None:
            audit_block.append([""] * len(NEW_HEADERS))
        else:
            tier = "" if a["band"] != "2-4 IN BAND" else "TBD"
            audit_block.append([a["band"], a["flag"], tier, "", a["source"], ""])
    s.values().update(
        spreadsheetId=SID,
        range="%s!%s2" % (TAB, chr(ord("A") + FIRST_NEW_COL)),
        valueInputOption="RAW",
        body={"values": audit_block},
    ).execute()
    print("wrote audit columns for %d rows" % len(audit_block))

    # ---- WRITE 3: append the newly sourced candidates
    start_rank = len(live) + 1
    append = []
    for i, r in enumerate(fresh):
        url = r.get("url", "")
        flag = r.get("flag", "")
        if url == "NO_URL_FOUND":
            flag = ("NO VERIFIED URL - do not contact until resolved; " + flag).strip("; ")
            url = ""
        append.append([
            start_rank + i, r["name"], r.get("org", ""), r.get("title", ""), r.get("city", ""),
            r.get("yrs", ""), "", url, "", "", r.get("conf", ""), r.get("why", ""),
            "2-4 CLAIMED (unverified)" if "UNVERIFIED" in r.get("yrs", "").upper() else "2-4 IN BAND",
            flag or "OK", "TBD", r.get("source", ""), "Coco 2026-09-08 " + r["_cluster"], "Identified",
        ])
    if append:
        s.values().append(
            spreadsheetId=SID,
            range="%s!A1" % TAB,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": append},
        ).execute()
    print("appended %d new candidate rows" % len(append))


if __name__ == "__main__":
    main()
