---
name: nugget-repo-vs-nugget-web-two-different-codebases
description: "Nugget's GitHub repo is aymenabid-HR/Nugget (private, the CLI toolkit + method). The live wizard nugget-web is a SEPARATE unversioned folder on another laptop with no GitHub link and no backup."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7ebbd6b4-eec1-46e1-8ce7-b66c58d70a9f
  modified: 2026-09-24T19:37:01.457Z
---

Nugget is **two codebases**, and conflating them cost most of a session on 2026-09-25.

**1. `aymenabid-HR/Nugget`** — private, single branch `master`, HEAD `5996d51`. Cloned to `C:\Nugget`.
The GitHub API and `raw.githubusercontent.com` both return **404 unauthenticated**, but
`git ls-remote` **succeeds** with this machine's stored credentials, so it is reachable here.
(Supersedes the earlier dead end: `Jaw901/Nugget` 404s because the owner is wrong, not because
no repo exists.)

Contents: a **Node CLI toolkit**, not a web app. 54 one-off scripts, 14 skill docs, 8 reference
docs, 8 utils. `package.json` is still named `my-first-agent`. The two that matter:
- `scripts/generic-screening-orchestrator.js` — the 9-step pipeline, run as
  `node scripts/generic-screening-orchestrator.js <job_id> [--from] [--to] [--send-email]`.
  Email is **disabled unless `--send-email`** is passed.
- `utils/rubric-generator.js` — builds the rubric from the JD; `detectRole()` → engineer / pm / data.

The documented rubric (`skills/generic-screening-workflow.md`) is what the live wizard shows:
weights **40 / 25 / 20 / 10 / 5** = 100 points; **P1 ≥ 85, P2 ≥ 70, P3 ≥ 50, Reject < 50**; hard
filters = university tier, salary over budget, unwilling to relocate to Islamabad, missing years
or certifications.

**2. `nugget-web`** — the live 4-step wizard (Pick the job → Review the rubric → Check the pool and
cost → Confirm), Railway project **Nugget** `2a3f3943-24eb-48cc-8956-4e549c017289`, service
`nugget-web`, `https://nugget-web-production.up.railway.app`. Server-rendered, inline CSS, Google
SSO, purple gradient top nav (Screening / Interviewers / Roles / New Evaluation).

🔴 **Its source is in no repository.** `railway status --json` reports
`source: {image: null, repo: null}`; it is deployed by `railway up` from a local folder, which
Railway does not retain. The wizard's UI strings appear in **zero commits** of
`aymenabid-HR/Nugget`. Railway's local link history (`~/.railway/config.json`) records exactly one
folder on this machine, `C:\Agent Coco` → *Ayesha Coco*, so nugget-web has only ever been deployed
from a different laptop. **A live app screening real candidates exists as one unversioned folder
with no backup and no rollback.**

Evidence it descends from the same repo: its Railway build installs Playwright/Puppeteer system
libraries (xvfb, mesa, gtk) matching that `package.json`, and its runtime logs show a background
worker polling `UPDATE nugget_screening_runs SET status='running', worker_id=$1, claimed_at=now()…`
— so Confirm enqueues a run and a worker claims it.

**Do not confuse either with Coco's own CV screening**, which is live in `C:\Agent Coco`
(`webapp/routers/cv_screening.py`, `frontend/src/pages/CVScreeningPage.tsx`), has no wizard, and
uses tiers `shortlist / maybe / no_hire`. Coco reads `public.nugget_screening_*` READ-ONLY and that
stays true. See [[nugget_technical_screening_adopted_2026_09_15]].

🔑 **Railway reads that need no link and write nothing:**
`railway status -p <project_id> -e production [--json]`, `railway list --json`,
`railway logs --build|--deployment --lines N -p <id> -e production -s <service> [deployment_id]`.

---

## Confirmed by deployment history, and with a control (2026-09-25, later)

Two sessions checked this independently after the technical-screening fix, and
the finding is stronger than "the current deployment has no repo".

**Every deployment, not just the latest.** The parallel session read all
**eleven** deployments of `nugget-web`, 2026-09-08 to 2026-09-16: `repo=None`
and `commitHash=None` on all of them, and **six carry `reason=deploy` rather
than `redeploy`** — so this is not one repoint of an older git-backed build.
**It has never had a source.**

**My own check, via `railway api` GraphQL** (`me { workspaces }` →
`workspace(workspaceId:)` → projects → services → deployments; `me { projects }`
is EMPTY because the projects belong to the *People & Culture - Zeshan*
workspace, not the personal account):

| project | service | deployments seen | built from a repo |
|---|---|---|---|
| Nugget `2a3f3943` | `nugget-web` | 1 | **0** — `repo=None sha=None branch=None` |
| Ayesha Coco `0cccea38` | `elegant-benevolence` | 6 | 3 — `repo='ayeshakhan-oss/Coco' branch='main'` |

🔑 **The Coco row is the control, and it is the point.** Without it,
`repo=None` could just mean the API does not expose that field. Coco's
deployments populate `repo`, `commitHash` and `branch` from the same query, so
the null on `nugget-web` is a real absence. **Never read a null as a finding
without a case where the same field is populated.**

⚠️ My query returned 1 deployment where the other session saw 11 — different
query shape, probably only the retained/active one. Not a contradiction, and
worth stating rather than quietly reporting the larger number.

## Why this matters more than it looks

🔴 **`nugget-web` is the engine behind the runs that WORKED.** Deployment
`ccad5673` on 14 Sep scored **669 candidates on job 38** with the same rubric
and the same `claude-haiku-4-5` that failed in Coco's own path. So the
unversioned service is not a legacy curiosity to be tidied away later: it is
the only implementation that has ever scored a full position successfully,
and its source exists on one laptop.

🔴 **It also cannot be audited.** When the webapp's structured-output bug was
found (a forced tool answered in several `tool_use` blocks, and code reading
`content[0]` gets a partial result that looks like a refusal to score), both
readable codebases came back clean: Coco's `webapp/` has no `content[0]`
indexing, and the `C:\Nugget` CLI clone cannot have the bug at all because its
`package.json` carries **no Anthropic SDK** (axios, pg, playwright, puppeteer,
pdf-parse, mammoth, tesseract, exceljs, nodemailer). The one codebase where it
could plausibly be latent is the one nobody can read.

**Report this as "unreadable", never as "clean".** Two paths to fix it: ask
Aymen for the source, or pull it out of the running container.
