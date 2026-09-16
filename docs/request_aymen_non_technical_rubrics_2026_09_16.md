# Request to Aymen: screening rubric coverage

**Drafted for Ayesha to send. 2026-09-16.**
All figures below are read-only counts taken from the live database on 2026-09-16.

---

Hi Aymen,

We are building a Candidate Evaluation module into Coco's web app, and rather than stand up a
second screening engine next to yours we would like to lean on the one you already have.

## Where coverage sits today

Of 32 published jobs:

| | Jobs | Applications |
|---|---|---|
| Have a screening rubric | 3 | 1,509 |
| No rubric | **29** | **2,994** |

The three with rubrics are AI Engineer Lead, Full Stack Developer and Lead Analytics Engineer.

## Two asks, and the first one is easy

**1. Six roles already in your engine's wheelhouse have no rubric.** These are technical, so they
need no new capability, only a rubric each:

| Job | Role | Applications |
|---|---|---|
| 34 | Odoo Developer | 195 |
| 24 | Full Stack Lead | 86 |
| 9 | Head of Data & Impact | 25 |
| 12 | QA Lead | 19 |
| 11 | Head of Engineering and AI | 17 |
| 19 | Data Engineer | 3 |

That is 345 applications that could be screened with what you have built already.

**2. Would you be willing to extend the engine to non-technical roles?** The largest unscreened
pools are Senior Product Manager (529), CPD Coach (404), Junior Research Associate for Impact and
Policy (296), Field Coordinator for Research and Impact Studies (238), Senior Manager Growth
(185), and Growth Manager in Karachi (156) and Lahore (132).

We do not think this needs a different engine. The rubric structure you already use carries the
role-specific content in `dimensions`, `hard_filters` and the system prompt, so a Growth Manager
rubric would be a different set of dimensions in the same shape. The question is whether you want
to own that, or would rather it stayed technical only.

## What we will do either way

Coco will read your results rather than re-score anything you have covered, read-only, and will
always attribute a score to your engine and its rubric version. Where you do not have a rubric,
Coco will score using **the same rubric schema as yours**, so the two are interchangeable and a
single report can show both without the numbers meaning different things.

If you would rather own non-technical rubrics too, we will drop that half of our build.

## One thing worth a look first

While reading the data we found three operational issues in the existing runs, written up
separately with the evidence. The one that matters most: **Job 13 Full Stack Developer never
retrieved 48 of its 67 CVs** (`resume_type` null, `resume_chars` 0), and the 18 that did parse
average 1,313 characters against roughly 5,300 on Jobs 37 and 38. Its 10.2 percent average score
looks like a retrieval failure rather than a weak pool, so we have not used those numbers for
anything.

The other two: every `claude-opus-5` run failed in bulk at zero recorded cost while every
`claude-haiku-4-5` run completed clean, which points at the model id or the API call rather than
at quality; and `resume_health` can report 85 on a document that yielded 21 characters, so a few
unreadable CVs are being scored instead of routed to a human.

Happy to walk through any of it.

Ayesha
