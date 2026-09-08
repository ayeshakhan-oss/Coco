"""
Second-pass confirmation for candidates the first verification pass could not confirm.

Why this exists: the first pass queries '"Name" org linkedin'. That phrasing produces false
negatives - Savera Bokhari came back NOT_FOUND even though her exact slug sits verbatim in
the raw SearXNG captures. A single query failing to surface someone is NOT evidence that the
person was invented, and treating it that way would throw away real candidates.

This pass asks a different question: does the CLAIMED SLUG itself resolve to a real profile?
It also folds in two corroborating sources that do not need the network at all:
  - the raw SearXNG capture files left by the cluster-5 sweep
  - official org pages already fetched and confirmed (OPM, i2i)

Final status per person:
  CONFIRMED    at least one independent source carries the slug verbatim
  UNCONFIRMED  no source does; do not write to the sheet as a real profile
"""
import glob
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_sourced_profiles as V  # noqa: E402

RESULTS = r"c:\Agent Coco\output\sourcing\verification_results.json"
CAPTURES = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
            r"\69fa597f-4a56-4d21-b9b8-2815d826ffe0\scratchpad")
OUT = r"c:\Agent Coco\output\sourcing\confirmation_final.json"

# Slugs read directly off an official organisation page during this session.
# These need no further proof - the employer published them.
ORG_PAGE_CONFIRMED = {
    "saroshsultan": "opml.co.uk/people/sarosh-sultan",
    "faaiz-gilani": "opml.co.uk/people/faaiz-gilani",
    "sabakalsoom": "invest2innovate.com/about/",
    "farwa--zahid": "invest2innovate.com/about/",
    "laiba-ahmad-a98313224": "invest2innovate.com/about/",
    "umar-farooq-86b19166": "invest2innovate.com/about/",
    "syeda-ayesha-faisal": "invest2innovate.com/about/",
    "sharissa-sebastian-aa3b9a193": "WebSearch result title, verbatim",
    "adil-sattar": "WebSearch result title, verbatim",
}


def load_captures():
    blob = ""
    for p in glob.glob(os.path.join(CAPTURES, "sx_*.txt")):
        try:
            blob += open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            pass
    return blob


def main():
    res = json.load(open(RESULTS, encoding="utf-8"))
    caps = load_captures()
    print("raw capture corpus: %d chars" % len(caps))

    final = {}
    need_net = []
    for name, r in res.items():
        slug = r.get("claimed", "")
        if not slug:
            final[name] = dict(r, status="NO_URL", proof="row carried no URL")
            continue
        if r["verdict"] == "VERIFIED":
            final[name] = dict(r, status="CONFIRMED", proof="pass-1 name query returned the slug")
        elif slug in ORG_PAGE_CONFIRMED:
            final[name] = dict(r, status="CONFIRMED", proof="official org page: " + ORG_PAGE_CONFIRMED[slug])
        elif ("in/" + slug) in caps:
            final[name] = dict(r, status="CONFIRMED", proof="verbatim in raw SearXNG capture files")
        else:
            need_net.append((name, slug, r))

    print("confirmed without network: %d | needing slug query: %d" % (len(final), len(need_net)))

    for i, (name, slug, r) in enumerate(need_net, 1):
        hits = V.search('"linkedin.com/in/%s"' % slug)
        found = [u for (t, u, s) in hits if slug in u.lower()]
        if not found:
            hits2 = V.search("%s linkedin profile" % slug.replace("-", " "))
            found = [u for (t, u, s) in hits2 if slug in u.lower()]
        if found:
            final[name] = dict(r, status="CONFIRMED", proof="pass-2 slug query resolved: " + found[0])
        else:
            final[name] = dict(r, status="UNCONFIRMED", proof="no source carries this slug")
        print("[%d/%d] %-12s %-28s %s" % (i, len(need_net), final[name]["status"], name, slug),
              flush=True)
        json.dump(final, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(2)

    json.dump(final, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print("\nFINAL:", dict(Counter(v["status"] for v in final.values())))
    print("written:", OUT)


if __name__ == "__main__":
    main()
