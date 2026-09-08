# Case Study Outcome Email, Below the Benchmark (Skill 01, Type 8)

**Added:** 2026-09-08 (requested by Ayesha)
**Status:** LOCKED structure, per-candidate content
**Audience:** External candidates who reached the case-study stage
**First cohort:** Job 42, Senior Manager Growth, 5 candidates below 70

---

## What This Type Is

A decision email to a candidate who was invited to the case-study stage, **submitted the case
study**, and scored **below the 70% benchmark that gates final interviews**. The letter states
the rule, explains the decision against the candidate's own submission, and closes the process.

It is a **rejection**, so the full candidate-communication rule set applies. It is not the
Case Study Update, Debrief-Pending type (#6), which communicates a *pending* decision.

**Do not use this type for:**

| Situation | Use instead |
|---|---|
| Sent the case study, never submitted | Case-Study Submission Nudge (Skill 06), or a non-submitter note |
| Submitted, decision still pending | Case Study Update, Debrief-Pending (type #6) |
| Submitted, cleared the bar, debrief to book | Case Study Debrief Invite (Skill 06 type #2) |
| Rejected after the debrief conversation | GWC rejection (type #4) or warm bench (type #3) |
| Rejected at CV stage | CV rejection (type #1) |

---

## The Two Evidence Sources, and Nothing Else

Every substantive claim in the letter traces to one of exactly two places:

1. **The candidate's own submission.** Their figures, their sentences, their deliverables.
2. **The benchmark answer key**, written and QA'd *before* any submission was opened.

Nothing else. No scorecard language, no panel opinion, no inference about why they did
something. The benchmark supplies the standard; the submission supplies the evidence.
See [case-study-scoring-rubric.md](../02_candidate-evaluation/case-study-scoring-rubric.md).

**Declared per candidate in the send script and gated at runtime:**

- `BENCHMARK_SOURCE` : path to the answer key. Must exist on disk.
- `SUBMISSION_SOURCE` : path to the evaluation record that quotes the submission, plus the
  candidate's Drive folder link. Must exist on disk.
- `ANCHORS` : at least **three** exact strings lifted from that candidate's own submission
  (a figure, a quoted phrase, a named deliverable). Each must appear verbatim in the rendered
  body. This is the mechanical guard against a generic letter.

---

## The 70% Rule Is Stated, the Individual Score Is Not

**State the rule** (Ayesha 2026-09-08): we set a 70% benchmark on the case study, and only
candidates who meet it move to final interviews. This goes in the opening paragraph, so the
outcome reads as a threshold applied evenly rather than a verdict on the person.

**Never print the candidate's own number.** No "you scored 46", no "46/100", no band label.
The rule gives the transparency. The number invites an argument about the marking and reads
as unkind. Gated: a `NN/100` pattern or "you scored" in the body is a HARD BLOCK.

⚠️ **Only claim a bar that was actually published to that cohort.** For Job 42 SMG the rubric
bands were 80+ / 65-79 / 50-64 / <50; the 70% figure is the hiring bar Ayesha applies, and all
five below-70 candidates sit below 65 too, so nothing turns on the difference. If a future
cohort was told a different number, write the number they were told.

---

## No Conversation References

Every one of the first cohort had a Zero In Call **booked**, but a booking is not a held
interview, and this letter does not need one. Ground everything in the written submission.

`INTERVIEW_REFERENCE_ALLOWED = False` by default, which HARD BLOCKS "we spoke", "our
conversation", "when we met", "our call", "our discussion", "our time together". Referencing
the **stage** they did not reach is fine. A conversation that occurred is not, unless it is
verified and the flag is deliberately set.

---

## Structure

```
Dear [First],

This is not a yes for now.                          <- Rule 10, exact, first line

[Opening: they submitted, we read it fully against a benchmark written before any
 submission was opened, we set a 70% bar and only candidates who meet it move to final
 interviews, their submission came in below it, so the application stops here. Then one
 honest line acknowledging the work the submission took.]

H  What Your Work Showed Us                         <- their real strengths, exact figures
H  Here Is the Honest Part                          <- the gap, against the benchmark standard
H  Where We Want to Leave This                      <- close, no future promise

PS [one specific thing from their submission worth remembering]

feedback_widget(...)
FOOTER
```

**Word count: 800 minimum**, 800-1100 target. Same as types 1-4.

---

## Rules That Apply Without Exception

- **Rule 10 opening line**, exact, first line after the salutation
- **Rule 11 no future-promise.** Job 42 is a live role, so the close must NOT invite a fresh
  application to the same requisition. Disposition only, candidate-initiated
- **Rule 12 collective "we"**, never "I"
- **Rule 1 no intent inference.** Never why they did something. "The submission measured
  coaching through `audio_coaching_sessions`, a field that sums to 1 across all 546 users" is
  a fact. "You assumed the column was right" is a HARD BLOCK
- **Rule 4 role-fit over personal shortcoming.** "The role puts this in front of a district
  officer, where a figure that cannot be sourced ends the relationship" beats "you failed to"
- **Rule 9** explain the decision, not the person
- **NO em dashes.** The evaluation records this content comes from are full of `&mdash;`.
  Strip every one
- **NO candidate comparisons.** The evaluation reports rank the pool ("the most rigorous in
  the pool", "the weakest of the fifteen"). That framing is internal. Write "unusually
  rigorous", never a placing
- No interviewer names, no scorecard language, no internal jargon
- v8 layout imported from `scripts/utils/v8_template.py`, `EYEBROW["case_study_outcome"]`
- `safe_sendmail()` only, pilot to Ayesha alone first, clean subject live

**Permitted for this type:** the phrase **"case study"** as candidate-facing language, as for
type #6. It is the candidate's own deliverable and we invited them to produce it.

---

## Send Mechanics

- **Script:** `scripts/send_case_study_outcome_pilot.py`
- **⚠️ SCRIPT NAMING:** keep `case_study_outcome` in the filename. Never let it contain
  `warm_bench`, `gwc`, `values` or `announcement`, which route to other validators.
- **The gate runs inside the script**, before any SMTP connection, and raises `SystemExit`.
  This is deliberate: the Layer 3 `PreToolUse` send hook is **inert** (it matches `tool_name`
  against `"send"` but is registered on `"Bash"`, so it never fires). Do not rely on it.
- Also checkable from the CLI:
  `python scripts/evals/run_eval.py --file draft.html --type case_study_outcome --subject "..."`
- **PILOT:** `TO = ayesha.khan@taleemabad.com` only, no CC (Rule 4).
- **LIVE:** candidate + the CC list Ayesha confirms for the batch. Never inherit a CC list
  from another role's script.

---

## Self-QA Before Piloting

- [ ] Benchmark written before submissions were opened, and it is the one this cohort was scored against
- [ ] Every strength and every gap traceable to that candidate's own submission
- [ ] At least 3 anchors present verbatim
- [ ] No other candidate's name anywhere in the letter
- [ ] No score, no band, no ranking, no pool comparison
- [ ] 70% rule stated
- [ ] "This is not a yes for now." is the first line after the salutation
- [ ] No em dashes, no "I", no intent-words, no conversation references
- [ ] Greeting name verified from the candidate's OWN most recent evidence (Rule 22)
- [ ] Per-recipient IMAP scan of Sent Mail BEFORE drafting, proving nobody already got one
- [ ] Word count 800+
- [ ] Pilot to Ayesha alone

---

## Send Log

| Date | Cohort | Candidates | Status |
|---|---|---|---|
| 2026-09-08 | Job 42 SMG, below 70 | Kanooz Siddiqui 62, Irfan Siddiqui 53, Ali Wajdan Khan 49, Basit Hussain 46, Rimsha Taj 45 | Pilot sent to Ayesha |
