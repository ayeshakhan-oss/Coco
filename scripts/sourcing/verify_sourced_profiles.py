"""
Independently verify every sourced candidate before anything is written to Ayesha's sheet.

Context (2026-09-08): one sweep agent fabricated 12 candidates with plausible-looking
LinkedIn URLs. After that, no subagent row is trusted on assertion. This script re-queries
each person through a working search channel and checks that the CLAIMED slug actually
belongs to the CLAIMED person.

Channel: headless Chrome against a SearXNG instance. The built-in WebSearch is US-indexed
and effectively blind to Pakistani LinkedIn profiles, so it cannot do this job.

Verdicts:
  VERIFIED        claimed slug appeared verbatim in results for this person's name
  SLUG_MISMATCH   the person exists but under a DIFFERENT slug -> claimed URL is wrong
  NOT_FOUND       no LinkedIn profile surfaced for this name at all -> treat as unproven
  NO_CLAIM        row had no URL to check (already marked NO_URL_FOUND)

Usage:
    python scripts/sourcing/verify_sourced_profiles.py            # verify all pending
    python scripts/sourcing/verify_sourced_profiles.py --limit 10
"""
import argparse
import glob
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
SCRATCH = (r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco"
           r"\69fa597f-4a56-4d21-b9b8-2815d826ffe0\scratchpad")
PROF = os.path.join(SCRATCH, "prof_bare")
HOST = "baresearch.org"
CLUSTER_DIR = r"c:\Agent Coco\output\sourcing\clusters"
OUT = r"c:\Agent Coco\output\sourcing\verification_results.json"

STOP = {"dr", "mr", "ms", "mrs", "syed", "syeda", "muhammad", "mohammad", "bin", "obe", "prof", "the"}


def dump(url, budget=45000):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--disable-blink-features=AutomationControlled", "--window-size=1920,1080",
           f"--user-agent={UA}", f"--user-data-dir={PROF}",
           f"--virtual-time-budget={budget}", "--dump-dom", url]
    try:
        return subprocess.run(cmd, capture_output=True, timeout=150).stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def clean(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x)).replace("\u200b", "").strip()


def parse(dom):
    out = []
    for m in re.finditer(r'<article class="result[^"]*">(.*?)</article>', dom, re.S):
        blk = m.group(1)
        hm = re.search(r'<h3><a href="([^"]+)"[^>]*>(.*?)</a></h3>', blk, re.S)
        if not hm:
            continue
        url, title = hm.group(1), clean(hm.group(2))
        cm = re.search(r'<p class="content">(.*?)</p>', blk, re.S)
        out.append((title, url, re.sub(r"\s+", " ", clean(cm.group(1)) if cm else "")))
    return out


def search(q):
    return parse(dump(f"https://{HOST}/search?q={urllib.parse.quote(q)}"))


def slug_of(url):
    m = re.search(r"linkedin\.com/in/([^/?\s]+)", url or "")
    return m.group(1).lower().rstrip("/") if m else ""


def toks(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return [t for t in re.split(r"[^a-z]+", s) if len(t) > 2 and t not in STOP]


def name_matches(name, blob):
    """At least half the distinctive name tokens must appear in the result text."""
    t = toks(name)
    if not t:
        return False
    hits = sum(1 for x in t if x in blob.lower())
    return hits >= max(1, (len(t) + 1) // 2)


def load_rows():
    rows = []
    for path in sorted(glob.glob(os.path.join(CLUSTER_DIR, "*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        for r in d.get("rows", []) + d.get("verified_rows", []):
            r = dict(r)
            r["_cluster"] = d.get("cluster", os.path.basename(path))
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    results = {}
    if os.path.exists(OUT):
        results = json.load(open(OUT, encoding="utf-8"))

    rows = load_rows()
    pending = [r for r in rows if r["name"] not in results]
    if args.limit:
        pending = pending[:args.limit]
    print(f"total rows {len(rows)} | already verified {len(results)} | this run {len(pending)}",
          flush=True)

    for i, r in enumerate(pending, 1):
        name, org, claimed = r["name"], r.get("org", ""), slug_of(r.get("url", ""))
        if not claimed:
            results[name] = {"verdict": "NO_CLAIM", "cluster": r["_cluster"],
                             "org": org, "claimed": "", "found": []}
            print(f"[{i}/{len(pending)}] NO_CLAIM     {name}", flush=True)
            continue

        # Query on the person, not the slug, so a fabricated slug cannot self-confirm.
        orgkey = " ".join(org.split()[:3])
        hits = search(f'"{name}" {orgkey} linkedin')
        found = [(t, u) for (t, u, s) in hits if "linkedin.com/in/" in u]
        found_slugs = [slug_of(u) for (t, u) in found]

        if claimed in found_slugs:
            verdict = "VERIFIED"
        else:
            # Did this person surface at all, under some other slug?
            person = [(t, u) for (t, u) in found if name_matches(name, t)]
            verdict = "SLUG_MISMATCH" if person else "NOT_FOUND"

        results[name] = {"verdict": verdict, "cluster": r["_cluster"], "org": org,
                         "claimed": claimed, "found": found_slugs[:8],
                         "titles": [t for (t, u) in found][:5]}
        print(f"[{i}/{len(pending)}] {verdict:<14} {name:<28} claimed={claimed}", flush=True)

        json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(2)

    from collections import Counter
    print("\nSUMMARY:", dict(Counter(v["verdict"] for v in results.values())), flush=True)
    print("written:", OUT, flush=True)


if __name__ == "__main__":
    main()
