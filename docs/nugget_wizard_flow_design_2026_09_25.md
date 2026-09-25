# Nugget screening wizard: notes on the flow

**Drafted 2026-09-25.** Internal working notes, not addressed to anyone outside the team.

## What this is based on, and what it is not

We wanted to work on the flow of the four step run wizard. The wizard's own source is not in
`aymenabid-HR/Nugget`, and `nugget-web` is deployed by `railway up` from a folder that is not in
any repository, so nothing below is written from reading its code.

What it is written from:

- `skills/generic-screening-workflow.md` and `scripts/generic-screening-orchestrator.js` in the
  Nugget repo, which document the pipeline the wizard is a front end for.
- Screenshots of the live wizard, which show every control on each step.
- The live runtime, where a worker repeatedly claims runs out of `nugget_screening_runs`.
- `docs/nugget_screening_defects_2026_09_15.md`, three issues found in the live screening data.

So the observations are about **what the flow asks a person to decide and what it tells them**,
which is visible from the outside. Anything that turns out to be already handled in the code, we
should just strike. Each point below says what would confirm or kill it.

---

## The flow as it stands

A jobs list showing, per job, how many applications are not yet actioned by a human (142/410 on
CPD Coach), how many arrived in the last 30 days, and when the most recent one came in. A Screen
button on each row opens a four step wizard:

| Step | What it decides |
|---|---|
| 1. Pick the job | Which job, its JD source |
| 2. Review the rubric | Continue with the published rubric, or write a new version |
| 3. Check the pool and cost | Who, applied within, model, batch API. Shows people, duplicates merged, no CV, estimated cost |
| 4. Confirm | Starts the run |

Underneath, the documented pipeline is: validate the job, fetch and parse the JD with a Neon
fallback, generate or load the rubric, apply hard filters, score what survives, categorise into
P1 / P2 / P3 / Reject, report. Weights are 40 / 25 / 20 / 10 / 5 to 100 points, thresholds
P1 at or above 85, P2 at or above 70, P3 at or above 50.

---

## 1. People are removed from the pool before anyone scores them

This is the one we would look at first.

Step 4 of the CLI pipeline applies six initial filters and the instruction is explicit: *hard
reject if any filter fails, move to next candidate*. Two of those six are university tier and
current location, with Islamabad as priority, and a third is salary above budget.

**Corrected 2026-09-25 against the live rubric, which is better than the CLI doc implies.** An
earlier draft of this note said people could be dropped on which university they attended. Read
back from the published rubric v1 on job 13 (Full Stack Developer), that is not what is
configured:

| Hard filter | Action |
|---|---|
| On-site: Islamabad | **reject** |
| At least 3 years of relevant experience | flag |
| University tier (preference, not a requirement) | flag |

So university tier only flags, which is the right call and already matches where we landed with
CV screening. **Location is the one that removes people**, and it removes them before anyone
reads a word they wrote. That is the filter worth a deliberate decision, especially on a role
that may not truly be on-site only.

It also makes the number on step 3 misleading whenever any filter is set to reject. We approve a
spend against a headline figure, but some unknown portion will be dropped before a single CV is
scored. The number we approved and the number that gets read are not the same number, and the
flow does not say by how much they differ.

There is direct evidence this class of filter is risky. Coco calibrated its own CV screen against
the 16 people Taleemabad actually hired or made an offer to, and at the threshold originally
chosen it would have rejected 8 of them. That is why in Coco a bottom tier means *read last* and
never *rejected*, and it is written into the code rather than left as an understanding.

What we could do instead: let the hard filters **sort and flag** rather than remove, so a human can
still see the person and overrule. If they must remove, then step 3 should show two numbers, how
many will be scored and how many will be excluded, with the reasons and a way to look at them.

*Still to confirm:* whether a rejected candidate gets an eval row recording why, or no row at all.
The wizard now shows the filters and their actions on the rubric step, and says in plain words
that a reject-type filter means nobody reads that person, so the choice is at least visible where
it can still be changed.

## 2. "NO CV: 0" is probably not knowable when it is shown

The pool screen reports `0 NO CV` for 369 people. From the defects write up, Job 13 had 48 of 67
evaluations with `resume_type` null and `resume_chars` 0, meaning the CV was never retrieved, and
on Job 38 ten `pdf-vision` rows averaged `resume_health` 85.5 on 21 extracted characters.

That points at `NO CV` counting whether a resume record exists, not whether it can be read. Those
are very different, and the second is only knowable once extraction is attempted, which happens
during the run.

The consequence is the one already recorded: a CV that failed to extract is indistinguishable, in
the tier column, from a candidate who was read and found unsuitable.

What we could do: say what the number actually measures, something like "no file on record", and
report the unreadable count in the run view where it is genuinely discovered. Coco's phrasing for
this, which we could borrow, is that a CV that will not open is a document problem and not a weak
candidate, so it stays counted as unscreened rather than scored.

*Confirm by:* the query behind the `NO CV` figure.

## 3. The recommended model is recommended partly because the others fail

The picker offers Claude Haiku 4.5 as recommended, with honest guidance that it is materially
weaker at weighing evidence and worth thinking about before it decides who gets interviewed.

From the live runs table:

| Model | Runs | Items failed | Recorded cost |
|---|---|---|---|
| `claude-opus-5` | 3 | 245 of 269, 602 of 645, 377 of 436 | $0.000000 each |
| `claude-haiku-4-5` | 3 | 0 | real spend |

Zero cost alongside mass failure means the calls died before anything billable happened, so this
looks like the model id or the API call rather than screening quality. Until that is settled, the
dropdown is asking someone to choose between a cheap model and a model that does not work, while
presenting it as a quality and cost tradeoff.

What we could do, in order of effort: check what `ANTHROPIC_MODEL` is actually set to on that
service, since a variable set by hand has silently overridden a code default here before. Then
either remove a model that is currently failing from the picker, or show the last run's success
rate beside each option so the choice is made on evidence.

## 4. Confirm commits money, and the control on that is not in the flow

The estimate text says the cost cap and the recorded actuals are the real controls, and
`nugget_screening_runs` carries a cost cap column. But the cap does not appear on the pool screen
or, as far as the screenshots show, on Confirm.

There is a second order effect. The newest applications are scored first, which is sensible, but
combined with a cap it means the flow quietly decides **who does not get screened** when the money
runs out. Whoever confirms should be told that, and told which end of the pool it falls on.

## 5. There is no run view, and the run is the long part

Confirm is the last step, but the work starts there. A 669 item Haiku run cost $5.36 and took real
time, and the run is asynchronous: the wizard enqueues, and a worker claims it with an
`UPDATE nugget_screening_runs SET status = 'running', worker_id = ...`.

Two failure modes are already on record. Job 13 is recorded as `completed` having lost 377 of its
436 items, so downstream it reads as a finished job. And on Coco's side, a fifty minute run died
at 236 of 410 when Railway redeployed underneath it, while the page still displayed 67, because
the counters only refreshed on the success path.

What we could do: make step 4 the run itself rather than a confirmation page. Live progress, the
count that could not be read kept separate from the count that scored badly, and a terminal state
that cannot say completed when most items failed. Coco's version of this retries through a
redeploy and commits each candidate as it finishes, so stopping loses nothing, which is worth
copying if the worker does not already do it.

## 6. Writing a rubric version sits inside a run launch

Step 2 offers "Write a new version" beside "Continue with v1". Freezing on publish and versioning
so earlier scores stay explainable is the right design. The question is only whether authoring
belongs here.

Launching a run is an operational act. Changing the rubric changes the standard every candidate on
that role is judged against, including people already scored. Putting them in the same flow makes
the second one feel like a step rather than a decision.

One option is that rubric authoring lives under Roles, and the wizard only picks among published
versions, with a link out. Genuinely open question though: how often does someone actually need to
write a version at the moment of launching, because if that is the normal path then this is fine
as it is.

## 7. Smaller things

- **One definition of actioned.** The jobs list explains new over total as not yet actioned by a
  human. The pool selector then offers "Not yet actioned (recommended)". If they are the same
  query, say it once and link the second to the first. If they are not, they need different names.
- **32 duplicates merged, with nowhere to look.** The merge is shown as a number with no way to
  see which records were merged or to undo one that is wrong.
- **"Applied within: any time"** on a pool running 2025-10-28 to 2026-07-08 is eight months of
  applicants, many of whom will have moved on. Worth considering whether the default should be
  narrower, with any time available.

---

## A shape we could try

Keeping four steps, but moving what each one carries:

1. **Job and pool.** Picking the job and choosing who gets screened is one decision, not two. Show
   the pool with both numbers, how many will be scored and how many excluded, and why.
2. **Rubric.** Choose among published versions. Authoring moves out to Roles.
3. **Cost and commit.** Model with its recent success rate, batch option, estimate, and the cap.
   State that the cap decides who is not reached. Confirm lives here.
4. **The run.** Live progress, unreadable kept separate from low scoring, honest terminal state.

That is three decisions and a run view, rather than four screens where the last one is a button.

## What to check against the source before acting on any of this

- Does the wizard apply the CLI's six hard filters, and does a hard rejected candidate get a row?
- What query produces `NOT YET ACTIONED`, and is it the same one behind the pool's `Who`?
- What does `NO CV` count?
- Where is the cost cap set, and what happens to the unreached remainder when it is hit?
- What does Confirm write, and what does the worker do when it finds a run it cannot finish?
