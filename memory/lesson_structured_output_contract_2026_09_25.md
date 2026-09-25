---
name: A stored schema is not a sent schema, and Haiku answers a forced tool in SEVEN blocks (2026-09-25)
description: Technical screening failed all 20 candidates and blamed their CVs. The rubric's output_schema was loaded, hashed and never transmitted; then the first fix read content[0].input and reproduced the identical error, because Haiku returns one tool_use block per top-level property.
type: project
---

# A stored schema is not a sent schema

**2026-09-25, job 38 AI Engineer Lead, run `aef6ed75`.** Ayesha screened 20
candidates. All 20 failed and the page told her every CV "could not be read".
Not one of those statements was true.

## Cause 1 — the contract was stored, hashed, and never transmitted

`screening_runs._call_model` went through `drafting.draft()`, the candidate
**letter** path, passing the rubric's system prompt and nothing else. The
rubric's `output_schema` — which names `dimensions` and every key inside it —
was loaded, hashed into `system_prompt_hash`, written to the run row, and never
sent to the model. The 11,287-character prompt never states an output format
either.

🔑 **A hash of a contract nobody transmitted looks exactly like enforcement.**
The run row said which schema it was scored against. Nothing was.

So the model invented a shape. Reproduced against the live model **before**
writing any fix:

```
stop_reason  : end_turn      <- finished cleanly. NOT truncation.
output_tokens: 2912          <- nowhere near the 4096 ceiling
returned     : must_have_skills, responsibility_alignment, stack_match,
               technical_breadth, experience_depth, strengths, gaps, ...
code read    : parsed["dimensions"]  ->  {}
```

All five dimensions were scored. They were top-level instead of nested.
`must_have_skills` happens to be the **first** dimension, so the error read
`model did not score the dimension 'must_have_skills'` and looked like a model
that had stopped early. It had not.

## Cause 2 — 🔴 HAIKU ANSWERS A FORCED TOOL IN SEVEN SEPARATE BLOCKS

Measured, not reasoned. Against the real screening schema, Haiku 4.5 replied
with **one `tool_use` block per top-level property**: `extracted`, then
`dimensions`, `strengths`, `gaps`, `hard_filters`, `confidence`, `verdict`.

The first version of the fix read `content[0].input`, got `{"extracted": ...}`
alone, and **reproduced the identical "did not score the dimension
'must_have_skills'"**. A single-block read looks exactly like a model refusing
to score.

**Merge every `tool_use` block. `content[0]` is a trap.** This will reappear
the next time anyone adds a structured call anywhere in this codebase.

## Cause 3 — nothing in the codebase checked `stop_reason`

`drafting._parse_json` falls back to a regex that grabs the outermost `{...}`.
On a reply cut off at the token ceiling that yields a **parseable, incomplete,
plausible, wrong** object. Same shape as several defects this week: a silent
failure dressed as a result. `structured()` now refuses on `max_tokens`.

## And three reporting defects, each of which misled her separately

| Shown | True |
|---|---|
| 20 "could not be read" | Our screener broke. The CVs were fine |
| FAILED 0 | 20 items were `failed` in the DB; the counter was never bumped |
| SPENT $0.00 | 20 calls made and billed; cost was only recorded on success |

🔴 **A screener that broke is not a CV that would not open.** One needs an
engineer, the other needs a person to open a document. Merging them sent Ayesha
to chase 20 perfectly readable files while the defect was ours. `failed` is now
its own channel end to end: service → schema → `screenAll.ts` → page.

Separately, one of the 20 died on **NUL (0x00) bytes in extracted CV text** —
a PostgreSQL `text` column cannot hold them, so the resume-cache INSERT raised
`DataError`. Stripped, not replaced, so offsets in verbatim evidence do not
shift.

## Rules

- **Send the schema, do not merely store it.** Force it as a tool
  (`tool_choice={"type":"tool","name":...}`), never `auto`. A schema in a
  column enforces nothing.
- **Merge every `tool_use` block**, never `content[0]`.
- **Check `stop_reason`.** Refuse a truncated reply rather than parsing it.
- **A lenient JSON salvage hides truncation.** `_parse_json`'s regex is fine
  for prose, dangerous for a contract.
- **The offline stub must RAISE for a score, not return filler.** A fake letter
  is a draft nobody sends; a fake score is a decision about a person written to
  `nugget_screening_evals`.
- **Reproduce against the live model before fixing.** Both real causes here
  were invisible to reasoning and obvious the moment the response was printed.
  The second one was found only because the first fix was re-run end to end
  instead of being trusted.
- **Keep "could not be read" and "failed" apart everywhere**, including the
  counters and the cost.

## Notes

- Same rubric, same model (`claude-haiku-4-5`), scored **669 candidates on
  14 Sep** through Nugget's own engine, which does enforce the schema. Not a
  model regression — the webapp path reimplemented the call without the
  contract. Always check the model column before blaming the model.
- ⚠️ **Two sessions share this working tree.** A broad `git add` in the other
  session swept this session's then-untracked test file into its commit. It was
  the passing version and nothing broke, but **read `git diff --cached
  --name-only` before every commit while two agents are in here.**
- The three Neon-over-HTTPS test files take ~26 min; the other 949 run in under
  4 seconds. See [[lesson_untracked_module_outage_2026_09_25]].
