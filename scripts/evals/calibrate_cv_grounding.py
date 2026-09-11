"""Measure the CV-grounding hard block against two REAL corpora.

Run this before changing `min_anchors` in candidate_communication_eval.py. A
threshold is only defensible against letters we actually wrote:

  GOOD  output/job42/rejection_emails/*.html  - 103 letters written by the CLI
        path, each grounded in a CV that was genuinely read. A correct gate
        passes these.
  BAD   the 27 cv_rejections sent live 2026-06-30..07-09, generated before the
        CV was ever loaded. A useful gate catches these.

Calibrated 2026-09-11: threshold 25 -> 0 of 98 GOOD blocked, 56% of BAD caught.

Needs DB access (.env DATABASE_URL) and the neon helper used by the scratch
tooling; run from the repo root.

    python scripts/evals/calibrate_cv_grounding.py
"""
import os, re, sys, glob, json
sys.path.insert(0, r'C:\Agent Coco'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neon
from webapp.services import cv_text
from scripts.evals.candidate_communication_eval import check_cv_grounding, check_cv_particulars

files = sorted(glob.glob(r'C:\Agent Coco\output\job42\rejection_emails\*.html'))
ids = {}
for f in files:
    m = re.match(r'(\d+)_', os.path.basename(f))
    if m:
        ids[int(m.group(1))] = f

rows = neon.q('''select a.id, c.first_name, c.resume_data, c.resume_file_name, c.resume_mime_type,
 a.cover_letter, a.custom_answers, a.canned_answers, j.title
 from applications a join candidates c on c.id=a.candidate_id left join jobs j on j.id=a.job_id
 where a.id in (%s)''' % ",".join(str(i) for i in ids))['rows']

def answers(raw):
    if not raw: return []
    try: data = json.loads(raw) if isinstance(raw, str) else raw
    except ValueError: return [raw]
    out = []
    src = data.values() if isinstance(data, dict) else data
    for v in src:
        a = v.get('answer', v.get('value')) if isinstance(v, dict) else v
        if isinstance(a, str) and a.strip(): out.append(a.strip())
    return out

passed = blocked = nocv = 0
reasons = {}
for r in rows:
    f = ids[int(r['id'])]
    try:
        corpus = cv_text.extract(r['resume_data'], mime_type=r['resume_mime_type'],
                                 file_name=r['resume_file_name'])
    except Exception:
        nocv += 1; continue
    corpus = "\n".join([corpus, r['cover_letter'] or ""] + answers(r['custom_answers']) + answers(r['canned_answers']))
    html = open(f, encoding='utf-8', errors='ignore').read()
    ok, detail = check_cv_grounding(html, 'cv_rejection', corpus,
                                    candidate_name=r['first_name'] or '', role=r['title'] or '')
    warn_ok, warn = check_cv_particulars(html, 'cv_rejection', corpus,
                                         candidate_name=r['first_name'] or '', role=r['title'] or '')
    if not warn_ok:
        reasons['WARNED'] = reasons.get('WARNED', 0) + 1
    if ok:
        passed += 1
    else:
        blocked += 1
        if blocked <= 6:
            print('HARD BLOCK', os.path.basename(f)[:40].ljust(42), ' '.join(detail.split())[:110])

total = passed + blocked
print()
print('GOLD-STANDARD LETTERS: %d pass / %d blocked  (%.0f%% false-positive rate)  [%d CVs unreadable]'
      % (passed, blocked, 100.0 * blocked / max(total, 1), nocv))
print('block reasons:', reasons)
