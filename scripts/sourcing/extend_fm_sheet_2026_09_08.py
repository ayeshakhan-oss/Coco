"""
Clean up the FM Sourcing Master sheet in place, then extend it with the 2026-09-08
Fundraising & Partnerships (2-4 yr band) sourcing run.

Ayesha's instructions 2026-09-08:
  band = 2-4 years - Islamabad-first - clean up in place then extend
  "check there should be no fabrication"
  "how would i know the profiles are new? Shouldn't have any older profiles"

THREE GATES, all must pass before a row is appended:

  GATE 1  NO FABRICATION.  Only rows whose LinkedIn slug is CONFIRMED by an independent
          source are written as real profiles. Source is one of: an official org page, a
          verbatim search result, or the raw SearXNG capture files. Everything else is
          held back. Context: one sweep agent invented 12 candidates with plausible URLs,
          then produced a retraction that was itself partly wrong, so neither an agent's
          claim nor its confession is taken on trust.

  GATE 2  GENUINELY NEW.  Excluded if the person appears anywhere in the cross-sheet index:
          both FM tabs (including the live outreach tracker) and every other sourcing sheet
          in the master Roles tracker. Slug match, or a name match on 2+ distinctive tokens.
          Single-token name matches are treated as POSSIBLE duplicates and also held back,
          because "Muhammad Bilal" collapses to one token and over-matches.

  GATE 3  NOT ALREADY CONTACTED.  Anyone with Reached Out = TRUE on the Top picks tab is
          excluded, so nobody gets a second cold approach.

NON-DESTRUCTIVE. Out-of-band rows are TAGGED, never deleted: the 8+ and 5-7 cohorts are a
real asset for a future Head of Fundraising search. Snapshot at
output/sourcing/FM_sheet_snapshot_2026_09_08.json is required before any write.

Usage:
    python scripts/sourcing/extend_fm_sheet_2026_09_08.py --dry-run
    python scripts/sourcing/extend_fm_sheet_2026_09_08.py --apply
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = r"c:\Agent Coco\tools\agent-coco-914edff20dde.json"
SID = "18oUr_4rcKJOEp3JRd2sY3GbhtMIbG92Xyr619IPkcLo"
TAB = "FM-50-Candidates"
SNAPSHOT = r"c:\Agent Coco\output\sourcing\FM_sheet_snapshot_2026_09_08.json"
CLUSTER_DIR = r"c:\Agent Coco\output\sourcing\clusters"
CONFIRM = r"c:\Agent Coco\output\sourcing\confirmation_final.json"
SEEN = r"c:\Agent Coco\output\sourcing\seen_index.json"

NEW_HEADERS = ["Band", "Data Flag", "Tier", "Verification", "Evidence / Source", "Sourced By", "Status"]
FIRST_NEW_COL = 12  # column M
RUN_TAG = "NEW - Coco 2026-09-08"

STOP = {"dr", "mr", "ms", "mrs", "syed", "syeda", "muhammad", "mohammad", "bin", "obe", "prof", "the"}


def toks(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return [t for t in re.split(r"[^a-z]+", s) if len(t) > 2 and t not in STOP]


def norm_name(s):
    return " ".join(sorted(toks(s)))


def slug_of(u):
    m = re.search(r"linkedin\.com/in/([^/?\s\"]+)", u or "")
    return m.group(1).lower().rstrip("/") if m else ""


def band_of(years):
    m = re.findall(r"\d+", years or "")
    if not m:
        return "UNKNOWN"
    lo = int(m[0])
    return "2-4 IN BAND" if lo <= 4 else ("5-7" if lo <= 7 else "8+")


def url_flag(name, url):
    if not url or url.strip().startswith("["):
        return "URL-PLACEHOLDER"
    m = re.search(r"linkedin\.com/in/([^/?\s]+)", url)
    if not m:
        return "URL-NOT-LINKEDIN"
    flat = re.sub(r"[^a-z]", "", m.group(1).lower())
    t = toks(name)
    return "URL-UNVERIFIED-MISMATCH" if t and not any(x in flat for x in t) else ""


def svc():
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    return build("sheets", "v4", credentials=creds, cache_discovery=False).spreadsheets()


def load_clusters():
    rows = []
    for path in sorted(glob.glob(os.path.join(CLUSTER_DIR, "*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        for r in d.get("rows", []) + d.get("verified_rows", []):
            r = dict(r)
            r["_cluster"] = d.get("cluster", os.path.basename(path))
            rows.append(r)
    return rows


def audit_existing(values):
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
        nm, org, yrs, url, email = (cell("Name"), cell("Organization"), cell("Years"),
                                    cell("LinkedIn"), cell("Email"))
        if not nm:
            audits.append(None)
            continue
        flags = []
        if "taleemabad" in org.lower() or "taleemabad.com" in email.lower():
            flags.append("OWN-STAFF not a candidate")
        d = [x for x in seen[nm.lower()] if x != n]
        if d:
            flags.append("DUPLICATE of row " + ",".join(map(str, d)))
        uf = url_flag(nm, url)
        if uf:
            flags.append(uf)
        audits.append({"row": n, "name": nm, "band": band_of(yrs),
                       "flag": "; ".join(flags) or "OK"})
    return audits


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(SNAPSHOT):
        sys.exit("ABORT: snapshot missing. Never write to this sheet without one.")
    if not os.path.exists(CONFIRM):
        sys.exit("ABORT: %s missing. Run verify_sourced_profiles.py then confirm_by_slug.py "
                 "first - GATE 1 cannot be enforced without it." % CONFIRM)

    confirm = json.load(open(CONFIRM, encoding="utf-8"))
    seen = json.load(open(SEEN, encoding="utf-8"))
    s = svc()

    values = s.values().get(spreadsheetId=SID, range=TAB).execute().get("values", [])
    audits = audit_existing(values)
    live = [a for a in audits if a]
    print("EXISTING ROWS: %d   BANDS: %s   FLAGGED: %d"
          % (len(live), dict(Counter(a["band"] for a in live)),
             sum(1 for a in live if a["flag"] != "OK")))

    # GATE 3 source: the live outreach tracker.
    contacted = set()
    tp = s.values().get(spreadsheetId=SID, range="Top picks").execute().get("values", [])
    if tp:
        th = {h.strip(): i for i, h in enumerate(tp[0])}
        for r in tp[1:]:
            def tc(k):
                i = th.get(k, -1)
                return r[i].strip() if 0 <= i < len(r) else ""
            if tc("Name") and tc("Reached Out").upper() == "TRUE":
                contacted.add(norm_name(tc("Name")))

    rows = load_clusters()
    keep, rejected = [], defaultdict(list)
    for r in rows:
        nm, nk, sk = r["name"], norm_name(r["name"]), slug_of(r.get("url", ""))
        c = confirm.get(nm, {})
        status = c.get("status", "UNCONFIRMED")

        if status != "CONFIRMED":
            rejected["GATE1 not confirmed (%s)" % status].append(nm)
            continue
        if nk in contacted:
            rejected["GATE3 already contacted"].append(nm)
            continue
        if sk and sk in seen["slugs"]:
            rejected["GATE2 slug already in a sourcing sheet"].append(nm)
            continue
        if nk in seen["names"]:
            n_tok = len(nk.split())
            label = ("GATE2 duplicate name" if n_tok >= 2
                     else "GATE2 POSSIBLE duplicate, single common token")
            rejected["%s (%s)" % (label, "; ".join(sorted(set(seen["names"][nk])))[:60])].append(nm)
            continue
        r["_proof"] = c.get("proof", "")
        keep.append(r)

    print("\nSOURCED ROWS: %d" % len(rows))
    for reason in sorted(rejected):
        print("  REJECTED %-58s %d  %s" % (reason[:58], len(rejected[reason]),
                                           rejected[reason][:4]))
    print("\n>>> PASSING ALL THREE GATES: %d" % len(keep))
    for r in keep:
        print("     %-28s %-34s %-14s %s" % (r["name"][:28], r.get("org", "")[:34],
                                             r.get("city", "")[:14], r.get("url", "")[:52]))

    if args.dry_run:
        print("\nDRY RUN - no writes performed.")
        return

    col = chr(ord("A") + FIRST_NEW_COL)
    s.values().update(spreadsheetId=SID, range="%s!%s1" % (TAB, col),
                      valueInputOption="RAW", body={"values": [NEW_HEADERS]}).execute()

    block = []
    for a in audits:
        if a is None:
            block.append([""] * len(NEW_HEADERS))
        else:
            block.append([a["band"], a["flag"], "", "", "", "FM sheet 2026-05 (pre-existing)", ""])
    s.values().update(spreadsheetId=SID, range="%s!%s2" % (TAB, col),
                      valueInputOption="RAW", body={"values": block}).execute()
    print("wrote audit columns for %d existing rows" % len(block))

    start_rank = len(live) + 1
    append = []
    for i, r in enumerate(keep):
        yrs = r.get("yrs", "")
        band = "2-4 CLAIMED (tenure unverified)" if "UNVERIFIED" in yrs.upper() else band_of(yrs)
        append.append([
            start_rank + i, r["name"], r.get("org", ""), r.get("title", ""), r.get("city", ""),
            yrs, "", r.get("url", ""), "", "", r.get("conf", ""), r.get("why", ""),
            band, r.get("flag", "") or "OK", "TBD", "CONFIRMED", r["_proof"],
            RUN_TAG + " / " + r["_cluster"], "Identified",
        ])
    if append:
        s.values().append(spreadsheetId=SID, range="%s!A1" % TAB, valueInputOption="RAW",
                          insertDataOption="INSERT_ROWS", body={"values": append}).execute()
        print("appended %d NEW rows at sheet rows %d-%d"
              % (len(append), len(values) + 1, len(values) + len(append)))


if __name__ == "__main__":
    main()
