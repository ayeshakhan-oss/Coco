# Technical Screening (Nugget's screening engine)

**Component of Skill 02 (Candidate Evaluation). Added 2026-09-15.**

Technical roles at Taleemabad are screened by **Nugget**, a separate agent run by
**Aymen Abid**. Its screening engine is live and writes to the shared Markaz Neon database.
Coco does **not** screen technical roles by hand and does **not** run a second screening system.

> 🔒 **READ ONLY. These are not Coco's tables.**
> Coco may SELECT from `nugget_screening_*` and cite the results. Coco must never INSERT,
> UPDATE or DELETE in them, never create a rubric, and never start a run. Anything that would
> change Nugget's data goes to Aymen, not through Coco.

---

## Where it lives

Eight tables in the **`public`** schema of the Markaz Neon database:

| Table | What it holds |
|---|---|
| `nugget_screening_rubrics` | The rubric per job: weighted dimensions, anchors, hard filters, thresholds, the full `system_prompt` and its hash. Versioned, with `status='active'` and `activated_at`. |
| `nugget_screening_runs` | One batch: model, effort, cost cap, planned vs done counts, worker heartbeat, cancel/pause. |
| `nugget_screening_run_items` | One row per candidate in a run. |
| `nugget_screening_evals` | The result per candidate: dimension scores with evidence, strengths, gaps, hard filter flags, verdict, confidence, tier. |
| `nugget_screening_reports` | Generated reports. |
| `nugget_screening_resume_cache` | Extracted CV text, reused across runs. |
| `nugget_screening_run_events` | Run audit trail. |
| `nugget_sessions` | Session records. |

There is also a **`nugget_deg`** schema holding the same 12 table names, **all empty**. It is a
mirror or staging schema. Always query `public`. Reading `nugget_deg` and reporting "no screening
exists" would be wrong.

---

## The rubric model

Each job gets one active rubric. Five dimensions, each scored **0 to 5**, each with a weight.
`score_pct` is the weighted total against `max_score` (100).

Example, Job 38 AI Engineer Lead:

| Dimension | Weight | Core |
|---|---|---|
| `must_have_skills` | 8 | yes |
| `responsibility_alignment` | 5 | yes |
| `stack_match` | 4 | yes |
| `technical_breadth` | 2 | no |
| `experience_depth` | 1 | no |

Every dimension carries three things Coco should read before citing a score:

- **`anchors`** for all six values 0 through 5, written behaviourally. The 0 anchor is real and
  means absence, for example *"The CV does not mention the must-have skills at all."*
- **`look_for`** — what evidence earns the higher anchors, for example *"Specifics that are
  costly to invent: system names, data volumes, user counts, latency."*
- **`common_gaps`** — the failure patterns, for example *"A long skills list with no project in
  the work history that uses any of it."*

### 🔑 Why this rubric does not have Coco's inflation problem

Coco's RM case-study round put all 25 submissions above the published bar because the anchors
started at 1 and created a floor of about 20 percent
([lesson_scoring_anchor_floor_inflation_2026_09_02.md](../../../memory/lesson_scoring_anchor_floor_inflation_2026_09_02.md)).

Nugget's rubric avoids that by construction, and the data confirms it. Its scoring rules state
*"An absent skill scores 0, not a middling guess"*, and on Job 38 the 612 scored candidates
average **44.0 percent** across the full **0 to 100** range, with 378 of 612 in the bottom tier.
The scale is genuinely used. **Do not "correct" these scores upward for looking harsh.**

---

## Tiering

`thresholds` is absolute, not a curve, and P1 and P2 carry **dimension gates** so a strong
aggregate cannot mask a critical weakness. Job 13:

```
p1: 85   gate: must_have_skills >= 4 AND stack_match >= 3
p2: 70   gate: must_have_skills >= 2
p3: 50
basis: absolute
```

Tiers seen in the data: `P1`, `P2`, `P3`, `P4`, `MANUAL_REVIEW`, `UNUSABLE`. Each eval carries a
`tier_reason` in plain words, for example *"Scored 100/100 (100%), at or above the P1 bar of 85."*

---

## Hard filters

`hard_filters` is a list, each with `key`, `label`, `rule`, `action` (`reject` or `flag`) and
`on_unknown`. Each is reported per candidate as **pass, fail or unknown**.

The wording is deliberately protective and Coco must preserve that when quoting it:

- *"Report fail only where the CV or the application answers say the candidate cannot or will not
  work there. Being currently located elsewhere is not a refusal."*
- *"Report fail only where relevant experience is clearly and substantially below 3 years. Judge
  relevant years, not total career length, and do not fail a CV whose dates cannot be totalled."*
- University tier: *"Never fail on this. It is a tie-breaker between comparable candidates and
  nothing more."*
- *"Report a hard filter as unknown when the CV is silent. Silence is not a refusal, and it must
  never read as one."*

The rubric also carries an explicit non-discrimination rule: *"You are scoring a document, not
ranking a person. Do not speculate about gender, age, ethnicity, religion, marital status or
nationality, and do not let a name, a photograph, or a university influence any score."*

---

## Resume health and manual review

`manual_review_rules` sets the floor, for example `min_resume_chars: 500`,
`min_resume_health: 60`. Below it the candidate is routed to `MANUAL_REVIEW` or `UNUSABLE`
rather than scored. Each eval records `resume_health`, `resume_issues`, `resume_chars`,
`resume_type` and `resume_truncated`.

🔴 **`UNUSABLE` means the CV could not be read. It does NOT mean the candidate is weak, and it
must never be reported as a rejection.** Those candidates still need a human to look at them.
This is the same class of defect as Coco's own pypdf letter-spacing problem, which made 12
percent of CVs unreadable and produced a 20,089-character "CV" containing 15 real words.

---

## What an eval gives Coco

Per candidate: `dimension_scores` (each with `raw`, `weight`, `weighted`, and a verbatim
`evidence` array quoted from the CV), `strengths`, `gaps`, `hard_filter_flags`, `verdict`,
`confidence`, `tier`, `tier_reason`, `score_pct`, plus model, cost and latency.

`is_current` and `superseded_by` handle re-marks natively. **Always filter `WHERE is_current`**,
or a superseded score will be reported as live. This is the failure Coco had to fix by hand on
the RM round, where a strict re-mark left old numbers standing in three other artefacts.

Note `status` is **`'scored'`** or **`'unusable'`**, not `'ok'`.

---

## How Coco reads it

Use `scripts/screening/read_nugget_screening.py`, which reuses the documented Neon HTTPS SQL
path (port 5432 is blocked, so POST to `https://{HOST}/sql` with a `Neon-Connection-String`
header, `DATABASE_URL` from `.env`).

```bash
python scripts/screening/read_nugget_screening.py --list
python scripts/screening/read_nugget_screening.py --job 38
python scripts/screening/read_nugget_screening.py --job 38 --tier P1 --detail
```

---

## Rules when Coco uses these results

1. **Attribute them.** In any report or brief, say the screening came from Nugget's engine and
   name the rubric version. Never present a Nugget score as Coco's own assessment.
2. **Never write.** Read only. Rubric changes, re-runs and tier changes are Aymen's.
3. **Filter `is_current`.** A superseded eval is not a result.
4. **Never report `UNUSABLE` as a rejection.** It is an extraction failure awaiting a human.
5. **Quote evidence verbatim.** The `evidence` arrays are quoted from the CV. Nothing inside
   quotation marks may be tidied, reordered or paraphrased
   (CLAUDE.md Rule 26).
6. **A screening tier is not a hiring decision.** It ranks a document against a rubric. It does
   not decide an outcome, and a rejection letter must still be grounded in the candidate's own
   CV, not in a tier label (CLAUDE.md Rules 12 and 29).
7. **Cross-check before reporting a pipeline state.** Markaz status and stage fields go stale,
   so a tier without a Markaz and mailbox cross-check is half the picture (CLAUDE.md Rule 18).
8. **If the numbers look wrong, say so rather than adjusting them.** Report the anomaly to
   Ayesha with the evidence. Do not re-score in Coco.

---

## Known state as of 2026-09-15

Three active rubrics, all created and activated by aymen.abid@taleemabad.com, all
`source='human_edited'`:

| Job | Role | Seniority | Min years | Scored | Unusable | Avg score |
|---|---|---|---|---|---|---|
| 38 | AI Engineer Lead | lead | 5 | 612 | 57 (8.5%) | 44.0% |
| 37 | Lead Analytics Engineer | lead | 5 | 54 | 6 (10.0%) | 32.7% |
| 13 | Full Stack Developer | mid | 3 | 19 | 48 (71.6%) | 10.2% |

🔴 **Job 13 is anomalous and its numbers should not be used without checking with Aymen.**
A 71.6 percent unusable rate against 8.5 percent on Job 38, and a 10.2 percent average, reads as
a CV extraction failure rather than a weak pool. See
[memory/nugget_technical_screening_adopted_2026_09_15.md](../../../memory/nugget_technical_screening_adopted_2026_09_15.md).
