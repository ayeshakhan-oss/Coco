---
name: Values Scorecard Scoring — Phase 2 Built (2026-09-17)
description: Coco can score a values interview transcript and submit it to Markaz behind an approver gate. Records the schema corrections verified against 219 live records (canonical names, string Yes/No, lowercase pass/fail, unpadded date), the four write-path criticals, the duplicate-application trap, and the fake-gate-test lesson.
type: project
---

# Values scorecard scoring, Phase 2 (2026-09-17)

**Branch:** `feat/candidate-evaluation`, **not merged, not deployed.** 206 tests, clean build.
**Plan:** [docs/plans/2026-09-17-candidate-evaluation-phase2-values-scoring.md](../docs/plans/2026-09-17-candidate-evaluation-phase2-values-scoring.md)

Paste a transcript, score it into the locked 6 values, review the full draft, and an **approver**
submits it to `public.applications`. Nothing was written to Markaz during development: it still
holds exactly 219 scorecards, last application update 2026-09-14.

---

## 🔴 The locked skill file's "NON-NEGOTIABLE" schema was wrong

The file warns that a wrong schema makes data invisible in Markaz's UI, and was itself documenting
the minority spellings. Verified against all 219 live records and corrected in `6bc60f1`:

| Skill file said | Markaz actually uses | count |
|---|---|---|
| Don't Walk Away | **Don't Walk Away from Hard Things** | 219 |
| All for One | **All for One & One for All** | 213 |
| Continuously Improve | **Continuously Improve Our Craft** | 212 |
| Courageous Conversations | **Have Courageous Conversations** | 214 |

`proceedToRightSeat` is the **string** `"Yes"`/`"No"` (215 of 219), not a boolean.

**Three more values that must be read from the data, never assumed:**
- `values_interview_result` is **lowercase** `"pass"` (101) / `"fail"` (23), plus one legacy
  `"strong_pass"`. Writing our computed `"PASS"`/`"OUT"` would have added a third spelling.
- The date format does **not** zero-pad: `"Nov 3, 2025"`, never `"Nov 03"`. `strftime("%b %d, %Y")`
  always pads, so use `f"{d:%b} {d.day}, {d:%Y}"`.
- Nested value objects use exactly `{name, deepDive, curveBall, microCase, rating}` across all 219.

🔑 **Rule: before writing a column in someone else's table, query its live values.** Every one of
these would have passed every test while quietly corrupting a convention.

## 🔴 The duplicate-application trap is live

`lessons_learned.md` records 2026-05-12: a scorecard written to application 1389 while Markaz's UI
displayed 2708, the newer duplicate, so the form looked empty. **Current risk: 298 duplicate
(candidate_id, job_id) pairs across 660 applications, worst case 8 for one pair.** My plan never
mentioned it; Coco's own incident log caught it, not a reviewer.

Submit now refuses (409) when the target is not the most recently updated application for its
candidate and job, naming the newer id. It refuses rather than redirecting: writing to a different
record than the one asked for is worse than refusing.
⚠️ `ORDER BY updated_at DESC` is **NULLS FIRST** in Postgres, so the first implementation would
have produced a permanent unforceable false 409. Compare against the target's own `updated_at`.

## 🔴 Four criticals in the one file that writes to Markaz

All found by review, all closed:
1. **Check-then-act race** — the 409 read status unlocked and the UPDATE was unconditional, so a
   double-click wrote twice. Now an atomic conditional status flip gates the write.
2. **An *editor* could force `proceedToRightSeat: "Yes"` onto an OUT scorecard** — the client's
   `proceed` was applied after the verdict recomputation. `proceed` is now derived, never supplied.
3. **`final_comments` was never recomputed**, so the permanent record could read "PASS - 6(+)"
   beside `proceedToRightSeat: "No"`.
4. **An existing scorecard was silently destroyed.** Now 409 unless `overwrite=true`, with all four
   prior column values preserved in `replaced_payload` so an overwrite stays reversible.

## 🔴 A gate test that asserted against the module docstring

`assert "require_approver" in src` matched the **docstring**, so it passed even with the wrong
dependency on the route. And every router test called the route function directly with a hand-made
user dict, bypassing dependency resolution, so **no test exercised any auth gate at all**. I
repeated the implementer's "mechanically tested" claim before a reviewer caught it.

Now asserted on `route.dependant.dependencies`, and **proven to bite** by flipping submit to
`require_editor` and watching it fail. 🔑 **A gate test that has only ever passed proves nothing.**

## What holds by construction

- The verdict is computed in code from the six ratings, never taken from the model. Cross-checked
  against an independently re-derived rule across all **729** combinations: 0 mismatches.
- A model claiming PASS on a scorecard containing a minus is overruled, and its GWC block dropped.
- GWC exists only on PASS. A malformed model response is retried once then raises; nothing is
  coerced or filled in. A transcript under 2,000 chars is refused.
- `values_prompt.py` deliberately does **not** copy `tone_rules.py`'s silent `except OSError:
  return ""`; it logs at ERROR and raises.

## ⚠️ Two process lessons

- **"Untracked and created during my session" does not mean "mine".** I moved another session's
  in-progress test file out of `webapp/tests/` believing it was our scaffolding. A parallel session
  had been committing candidate-communication work onto the same branch (`e40f6c8`). Restored.
  **Check provenance with `git log` on the branch before touching an unfamiliar file.**
- **Oversized dispatches stall.** Two subagents died on 12-finding fix waves and a 65KB/15-finding
  review. Split by layer and they complete. Neither left partial edits.

## Still outstanding before merge

The plan's own final verification, which needs a human:
1. Apply the migrations: `railway run --service elegant-benevolence alembic upgrade head` (the DB
   is still at 0005; 0006, 0007 and 0008 are unapplied).
2. Submit exactly one scorecard end to end against an application Ayesha picks, read it back, and
   confirm it matches the logged payload.
3. **Ayesha confirms in Markaz's own UI that it renders.** This is the only check that catches a
   schema problem for real and it cannot be done from here.
