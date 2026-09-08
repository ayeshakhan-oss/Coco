"""
Build the "have we seen this person before" index.

Ayesha's requirement 2026-09-08: the rows added to the FM sheet must be genuinely NEW.
Checking the destination tab alone is not enough - a person can already sit in the outreach
tracker, or in another role's sourcing sheet from an earlier run.

This walks every sourcing sheet in the master Roles tracker, plus both FM tabs, and records
every name and every LinkedIn slug seen anywhere. Output feeds the newness gate in
extend_fm_sheet_2026_09_08.py.
"""
import json
import re
import sys
import time
import unicodedata

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = r"c:\Agent Coco\tools\agent-coco-914edff20dde.json"
MASTER = "1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw"
FM = "18oUr_4rcKJOEp3JRd2sY3GbhtMIbG92Xyr619IPkcLo"
OUT = r"c:\Agent Coco\output\sourcing\seen_index.json"

STOP = {"dr", "mr", "ms", "mrs", "syed", "syeda", "muhammad", "mohammad", "bin", "obe", "prof", "the"}


def norm_name(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    t = [x for x in re.split(r"[^a-z]+", s) if len(x) > 2 and x not in STOP]
    return " ".join(sorted(t))


def slug_of(u):
    m = re.search(r"linkedin\.com/in/([^/?\s\"]+)", u or "")
    return m.group(1).lower().rstrip("/") if m else ""


def main():
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    sv = build("sheets", "v4", credentials=creds, cache_discovery=False).spreadsheets()

    # Every sourcing sheet we have ever built, from the master Roles tracker.
    roles = sv.values().get(spreadsheetId=MASTER, range="Roles!A1:F60").execute().get("values", [])
    targets = {}
    for r in roles[1:]:
        role = r[0] if r else ""
        link = r[2] if len(r) > 2 else ""
        m = re.search(r"/d/([A-Za-z0-9_-]{30,})", link)
        if m:
            targets[m.group(1)] = role
    targets[FM] = "Fundraising & Partnerships (destination)"

    names, slugs, per_sheet = {}, {}, {}
    for sid, role in targets.items():
        # Retry: a bare loop over many spreadsheets hits transient rate limits, and a
        # silently skipped sheet would make a person look "new" when they are not.
        meta, err = None, None
        for attempt in range(4):
            try:
                meta = sv.get(spreadsheetId=sid).execute()
                break
            except Exception as e:
                err = e
                time.sleep(2 * (attempt + 1))
        if meta is None:
            status = getattr(getattr(err, "resp", None), "status", None)
            per_sheet[role] = "UNREADABLE status=%s" % status
            print("  SKIP %-46s status=%s" % (role[:46], status), file=sys.stderr)
            continue
        n_here = 0
        for sh in meta["sheets"]:
            tab = sh["properties"]["title"]
            try:
                vals = sv.values().get(spreadsheetId=sid, range="'%s'" % tab).execute().get("values", [])
            except Exception:
                continue
            if not vals:
                continue
            hdr = [h.strip().lower() for h in vals[0]]
            ni = next((i for i, h in enumerate(hdr) if h == "name"), None)
            for row in vals[1:]:
                blob = " ".join(row)
                for sg in re.findall(r"linkedin\.com/in/([^/?\s\"]+)", blob):
                    slugs.setdefault(sg.lower().rstrip("/"), []).append(role)
                if ni is not None and ni < len(row):
                    k = norm_name(row[ni])
                    if k:
                        names.setdefault(k, []).append("%s :: %s" % (role, tab))
                        n_here += 1
        per_sheet[role] = "%d named rows" % n_here
        print("  read %-46s %d named rows" % (role[:46], n_here), file=sys.stderr)

    json.dump({"names": names, "slugs": slugs, "sheets": per_sheet},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nunique people seen before : %d" % len(names))
    print("unique linkedin slugs seen: %d" % len(slugs))
    print("written:", OUT)


if __name__ == "__main__":
    main()
