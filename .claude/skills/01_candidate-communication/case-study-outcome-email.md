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
- `corpus` : the candidate's name in `output/smg_submission_corpora/CORPUS_<Name>.txt`, the
  text of their **actual submitted files**, fetched by
  `scripts/evals/fetch_submission_corpora.py`.

🔴 **An evaluation record is evidence of a reading, not a substitute for the source.** Before a
letter quotes or cites a submission, **fetch the submission and check the letter against it.**
Doing this on the first cohort, after two pilots had gone out, found **five defects in five
letters**: one factual (a field true for 541 of 546 users, not 540, which belongs to the
neighbouring field) and four quotes that had drifted (a silently corrected typo, an em dash
normalised to a comma, our own gloss inside quotation marks, a reordered sentence).

**Gated:** `_quotes_are_verbatim()` HARD BLOCKS any phrase in quotation marks that does not
appear verbatim in that candidate's corpus. If their wording cannot be reproduced exactly,
**paraphrase without quotation marks** rather than tidying it inside the quotes.

⚠️ SMG submissions arrive as **Markaz Drive links, not email attachments** (a mailbox scan
returns only logos and `invite.ics`). Open the folder IDs recorded in the evaluation scripts
with `token_sheets_broad.json`, not the MCP connector.

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

[Opening: thank them for the work first. Then: we read it in full against a benchmark
 written before any submission was opened, so submissions were measured against a fixed
 standard and never against each other. Candidates who meet the bar move to the final
 interviews. "Your submission did not meet the 70% benchmark on this occasion, and so we
 won't be moving forward with your application for this role."]

H  What Your Work Showed Us                         <- their real strengths, exact figures
H  Where the Submission Could Have Been Stronger    <- the gap, against the benchmark standard
H  What We Would Encourage You to Look at Differently  <- OPTIONAL, only if a real lesson
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
- **LIVE:** `--live`. CC defaults to `LIVE_CC` (Ayesha 2026-09-08): `waqas.tanveer@` ·
  `ali.sipra@` · `hiring@` · `ayesha.khan@`. Override with `--cc`. Never inherit a CC list
  from another role's script.
- 🔑 **`safe_sendmail()` refuses external domains** unless `allow_candidate_addresses([...])`
  runs first, and candidates are on gmail/outlook/live.com. The script allowlists **exactly
  the one candidate being written to**, immediately before that send, so a loop bug cannot
  reach an address it was not meant to.

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

---

## 🔒 TONE STANDARD (Ayesha 2026-09-08) — HARNESSED

**The letter exists to be useful to the candidate, never to justify or defend the decision.**
They invested real hours; they should finish reading feeling their effort was seen and their
work carefully reviewed. Warmth comes from respect and constructive language, **not** from
withholding the feedback: never over-soften to the point where they cannot understand why they
missed the benchmark.

**Order:** clear decision → appreciation for the effort → genuine recognition of strengths →
gently explain the key gaps → what would strengthen the approach → dignity and encouragement
grounded in their actual work.

### HARD BLOCKS, enforced in `candidate_communication_eval.py` (so the CLI eval **and** the Railway app both apply them)

`HARSH_LANGUAGE` — "failure" · "wrong" · "the honest part" · "you failed" · "the problem with
your" · "went wrong" · "blame" · "sloppy" · "careless" · "you cannot" · "incapable" ·
**"deliberately" · "reverse-engineer" · "selecting assumptions" · "until the arithmetic"**

`CORPORATE_BOILERPLATE` — "we regret to inform" · "after careful consideration" · "impressive
candidate pool" · "strong field of candidates" · "we wish you the best in your future"

### PREFER
"the main gap we identified" · "where the analysis could have been stronger" · "one area that
affected the conclusions" · "an opportunity to strengthen the analysis" · "what we would
encourage you to look at differently"

### The framing sentence, use it
> There were two areas in the analysis that ultimately affected the overall score, and we want
> to walk you through them because we think the context will be more useful than simply sharing
> the result.

Never "here is where you went wrong".

### The decision sentence, locked wording
> Your submission did not meet the 70% benchmark on this occasion, and so we won't be moving
> forward with your application for this role.

**"On this occasion"** is doing real work: it signals that this is not a permanent judgment.
Put "Candidates who meet the bar move to the final interviews" before it, so the benchmark is
not named twice in consecutive sentences.

### Describing a technical error
State **what happened in the analysis and its effect on the conclusion**. Never the candidate's
ability, judgment or motive. Hedge the description of the document rather than asserting a
verdict on the person:

| Prefer | Not |
|---|---|
| "The analysis appears to have been built using the first field." | "The analysis rests on the first." |
| "With two nearly identically named columns sitting in the same file, this is an understandable thing to get caught by." | "Two near identically named columns is a genuinely easy thing to be caught by." |
| "The main gap we identified sits in the email to the district officer." | "This is where the submission ran into trouble." |

Give credit where the reasoning on top of an error held together. Say so explicitly.

🔴 **The loop-coefficient trap.** Never imply the candidate chose assumptions to reach a desired
answer. Correct framing: each rate is a reasonable planning assumption, **what is missing is a
link back to the dataset**, so the target could not be validated confidently.

🔴 **Never imply they cannot do analysis.** State it positively ("it is not a statement about
your analytical ability"), not as a double negative ("nothing suggests you cannot"). The
`you cannot` pattern blocks the negative form, which is the point.

### The final check, required before every send
Read the letter once from the candidate's perspective, immediately after a rejection. **If any
sentence could reasonably make them feel accused, embarrassed, belittled, defensive, or as
though we are arguing our case against them, rewrite it.** This pass catches what the harness
cannot: it caught "learnable in an afternoon" (implies they missed something easy) and a close
that pigeonholed a candidate into process work.

### Section headings
Required, with the gap slot accepting alternatives so the wording can be count-specific:

1. What Your Work Showed Us
2. Where the Submission Could Have Been Stronger *(or "Two Areas That Shaped the Outcome" / "The Main Gap We Identified")*
3. Where We Want to Leave This

Optional: **What We Would Encourage You to Look at Differently** — include it only when there is
a genuinely portable lesson to give.

---

## 🚀 Deployed in the Coco web app (Railway) — 2026-09-08

This type is selectable and validated in the web app, not only in the CLI. Five touch points:

| File | Change |
|---|---|
| `scripts/evals/candidate_communication_eval.py` | `SECTION_HEADINGS['case_study_outcome']` (a heading slot may be a **list of accepted alternatives**; `optional` slots are allowed but never demanded) + `HARSH_LANGUAGE` + `CORPORATE_BOILERPLATE` |
| `webapp/reuse.py` | added to `EMAIL_TYPES`, so the API accepts it |
| `webapp/prompts/tone_rules.py` | tone hard-rules in the output contract, `_CASE_STUDY_OUTCOME_NOTE`, and the "case study" jargon exemption scoped to this type |
| `webapp/prompts/draft_prompt.py` | the type's intent line for the drafter |
| `scripts/send_case_study_outcome_pilot.py` | the batch sender, with its own gate |

**Why the eval harness and not just the send script:** `webapp/reuse.py` imports the validator
and `SECTION_HEADINGS` from the eval harness on purpose, so the drafting prompt and the
validator can never disagree. Tone rules added to the harness are therefore enforced in **both**
surfaces automatically. **Put shared rules in the harness; keep only batch-specific mechanics
(anchors, corpora, allowlisting) in the send script.**

⚠️ The four existing types are unaffected: "case study" is still blocked for them, and all four
`system_prompt()` calls still build. Verified by re-running the CLI eval over all five sent
letters after the change, all PASS.
