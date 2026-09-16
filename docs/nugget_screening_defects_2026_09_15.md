# Nugget screening engine: three defects found in the live data

**Found:** 2026-09-15 · **Method:** read-only SQL against `public.nugget_screening_*`.
Nothing was written, no run was started, no rubric was touched.

Context: Coco was documenting Nugget's screening method in order to read its results, and these
turned up while checking the data. The rubric design itself is sound. Scores use the full 0 to
100 range with real zeros, the hard filters are carefully written so that silence is never read
as a refusal, and P1 carries dimension gates rather than relying on an aggregate. These three
items are operational, not methodological.

---

## 1. Every `claude-opus-5` run failed in bulk, at zero recorded cost

| Job | Model | Items | OK | Failed | Recorded cost | Status |
|---|---|---|---|---|---|---|
| 38 | `claude-opus-5` | 269 | 24 | **245** | $0.000000 | failed |
| 38 | `claude-opus-5` | 645 | 43 | **602** | $0.000000 | failed |
| 13 | `claude-opus-5` | 436 | 59 | **377** | $0.000000 | completed |
| 13 | `claude-haiku-4-5` | 8 | 8 | 0 | $0.085363 | completed |
| 38 | `claude-haiku-4-5` | 669 | 669 | 0 | $5.362871 | completed |
| 37 | `claude-haiku-4-5` | 60 | 60 | 0 | $0.618590 | completed |

Every Opus run failed most of its items and recorded **$0.00**. Every Haiku run completed every
item and recorded real spend.

Zero cost alongside mass failure means the calls died **before** anything billable happened,
which points at the model identifier or the API call itself rather than at screening quality or
rate limits. A quality problem or a timeout would still have been billed.

Worth checking what model id the runner sends for `claude-opus-5` and what the API returned.
Coco hit a related class of problem in September, where an `ANTHROPIC_MODEL` environment
variable on Railway silently overrode the intended model, so the value the code sends is worth
confirming against what the environment actually supplies.

The third row is the one to look at first: Job 13 is recorded as **`completed`** while 377 of
436 items failed. A run that loses 86 percent of its items probably should not report success,
because downstream anyone reading Job 13's results sees a finished run.

---

## 2. Job 13 (Full Stack Developer) never got most of its CVs

| Job | `resume_type` null (CV never fetched) | PDFs parsed | Avg chars on parsed PDFs |
|---|---|---|---|
| 38 | 57 | 583 | **5,312** |
| 37 | 6 | 52 | **5,341** |
| 13 | **48 of 67** | 18 | **1,313** |

Two distinct problems on Job 13:

- **48 of 67 evaluations have `resume_type = null` and `resume_chars = 0`.** The CV was never
  retrieved, so 71.6 percent of that job is `UNUSABLE` against 8.5 percent on Job 38.
- **The CVs that did parse are a quarter the size of everyone else's**, 1,313 characters against
  roughly 5,300 on Jobs 37 and 38. A 1,313-character CV is about a third of a page, so those 18
  were probably truncated too.

The net effect is a 10.2 percent average score on Job 13 against 44.0 percent on Job 38. That
reads as a retrieval failure rather than a weak pool, so **Job 13's numbers should not be used
for any hiring decision until this is settled.**

Job 13 is an older job than 37 and 38, so the likeliest causes are resumes stored in a different
place or a different format, or links that have since expired.

---

## 3. `resume_health` reports a healthy CV when almost nothing was extracted

On Job 38 there are 10 evaluations with `resume_type = 'pdf-vision'`:

- average `resume_health`: **85.5**
- average `resume_chars`: **21**

Twenty-one characters is not a CV. But health of 85.5 sits well above the
`min_resume_health: 60` floor, so these pass the manual-review gate and get scored as though the
document was read.

The clearest example is application 2271, tier `MANUAL_REVIEW`, score 0.00 percent,
`resume_health` 85. Its `tier_reason` says:

> "The CV had no extractable text and scored zero on every dimension when read as an image,
> which usually means the page was illegible rather than the candidate unsuitable. Worth opening
> by hand."

while its `verdict` on the same row describes the candidate's actual background in detail, as an
architectural engineering student with no AI experience, and lists five specific gaps.

So the row contradicts itself: the tiering logic believes nothing was read, and the verdict
clearly read something (most likely the application answers rather than the CV). One of the two
is wrong, and as written a reader cannot tell which.

Counts of current scored evaluations with a score of 0 but a resume recorded as healthy
(health at or above 60): **Job 13: 11 · Job 38: 7 · Job 37: 2.**

**Suggestion:** make `resume_health` a function of what was actually extracted, so that the
vision fallback returning 21 characters scores near zero rather than 85 and is routed to a human
instead of being scored. A zero score should be reachable only when a readable document genuinely
evidences nothing.

---

## Why this matters beyond the numbers

A candidate whose CV failed to extract is indistinguishable, in the tier column, from a candidate
who was read and found unsuitable. If screening output ever feeds rejection letters, the first
group would be rejected for a document nobody managed to open. Keeping `UNUSABLE` and the
health-versus-extraction mismatch visible is what stops that happening.
