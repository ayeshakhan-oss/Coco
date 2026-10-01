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

---

# Part 2: the fix was verified at the wrong boundary, twice

Both of these were found AFTER the note above was written, and both are sharper
than the original bug.

## (a) The caller never supplied the schema

`d53c216` forced the schema as a tool, and I proved it by calling `_call_model`
with a schema and watching it work. **Nobody checked that `work()` SUPPLIES
one.** Its rubric SELECT listed nine columns and `output_schema` was not among
them, so `rubric.get("output_schema")` was `None` on every real run, for every
job, and scoring fell straight back to the prose path — while the column sat
populated in the database the whole time.

Run `1b44a642` then scored **67 candidates that way and looked healthy**,
because `normalise_dimensions` lifted the flattened dimensions exactly as
designed. **The defence in depth hid the thing it was defending against.** One
candidate whose prose happened to be malformed JSON failed, and that single
thread is the only reason any of it surfaced.

🔑 **A function that works when called correctly proves nothing about the code
that calls it.** Verify at the boundary the production path actually crosses.

Fixed in `1105e81`: the SELECT became `_RUBRIC_FOR_RUN_SQL` with
`RUBRIC_COLUMNS_SCORING_NEEDS` asserted against it as a column set, and
`score_one` now **REFUSES** a rubric arriving without its schema rather than
scoring it in prose. That fallback is invisible by construction — it produces
plausible evaluations, writes them to `nugget_screening_evals`, and nothing in
the output says the contract changed.

## (b) Verified against a sample that could not show the defect

The API requires `additionalProperties: false` on **every** object in a tool
schema, not just the root:

```
400 invalid_request_error
output_config.format.schema: For 'object' type,
'additionalProperties' must be explicitly set to false
```

Run `4b3a144f` lost **66 of 76 candidates**, every one to that 400.

🔴 **Why my verification missed it.** I proved the forced-schema fix end to end
against job 38's rubric. Jobs 13, 37 and 38 are all `human_edited` and already
carried the flag. **Job 24's was the only rubric a MODEL had written**, and it
was missing the flag on nine nodes including the root. Three of four rubrics
would have passed my check; the fourth is the one she ran. **One sample of a
population is not a sample.** When a population has a distinguishing attribute
(here: `source = human_edited` vs `llm_drafted`), test one of EACH.

Fixed in `cba5408`, in both places on purpose:
- `AnthropicDrafter._strict_schema` repairs at **send** time, so rubrics already
  published stay screenable without a migration. Guarded on `type == "object"`
  so the `properties` MAP never gets the flag by mistake; an explicit `true` is
  respected, not overwritten.
- `rubric_drafting.output_schema` emits it, so new rubrics are correct at birth,
  delegating to the same implementation so the two cannot drift.

Neither alone is enough: one fixes history, the other fixes the future.

## Also fixed in this pass

- **`failed` is its own channel**, separate from "could not be read", all the
  way from the service through `screenAll.ts` to the page. They were merged, so
  a run where every candidate failed on OUR defect told Ayesha that 20 CVs were
  unreadable and sent her to chase perfectly good documents.
- The failure path now **bumps `failed_count` and records cost**. It did
  neither, so a fully-failing run displayed `FAILED 0` and `SPENT $0.00` for 20
  calls we were billed for.
- `_strip_nul` — PostgreSQL `text` cannot hold `0x00`, and one stray NUL from a
  PDF parser made the resume-cache INSERT raise `DataError` and took that
  candidate down as "could not be read".

## Where the results are read

Scored candidates are at **`/evaluations`** ("Screening Results" in the sidebar,
under Technical Screening) — tier filter, candidate list, per-candidate detail.
⚠️ The wizard's finish screen does **not** link to it, which is why Ayesha asked
four times where to look. Worth adding.
