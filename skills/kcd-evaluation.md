# Skill: KCD Case Study Evaluation

KCD = Knowledge, Capability, Design. Second-to-last filter before the GWC/technical interview.
Pipeline position: Values Call → **KCD Case Study** → GWC Interview.
Never send a case study to someone who failed values.

## Agent Collaboration — Coco + Noah (confirmed 2026-03-31)

Coco (Ayesha's agent) and Noah (Jawwad's agent) are peer agents on the same talent acquisition team. They will independently evaluate the same KCD cohorts and must produce reconcilable outputs. Neither is senior to the other. Both serve the same hiring process.

**The goal is not identical scores — it is aligned verdicts and shared reasoning.**

### Shared evaluation standards (both agents, every KCD)
| Standard | Rule |
|---|---|
| Scoring scale | 1–5 per criterion. Fractional scores (4.5, 3.5, 1.5) required where a candidate sits between whole numbers. |
| Verdict thresholds | 85%+ STRONG HIRE · 70–84% HIRE · 55–69% CONDITIONAL · 40–54% BORDERLINE · <40% NOT RECOMMENDED |
| GWC threshold | 60%+ advances. State explicitly in About section and Pipeline Recommendations. |
| Incomplete submissions | Excluded from main ranking. Separate section. Score asterisked. Supplementary assessment recommended. |
| Transferable skills | Always named explicitly (what transfers, what doesn't) before scoring. No flat sector-gap penalties. |
| Evidence standard | Quote exact lines from submissions. Name specific techniques. Flag what this candidate did that others did NOT. |
| Narrative lead | Lead with the candidate's strongest signal, not their score. |
| Gap note | Separate clearly labelled paragraph. Names the specific gap and what it means for the role. |
| GWC probe questions | Targeted and specific — fill evaluation gaps or verify claims. Not generic interview questions. |
| Integrity check | Mandatory for every candidate. Name the exact signal if flagged. "Clean" if not. |

### Cross-check protocol (when both evaluate the same cohort)
1. If Noah's preview/pilot is available: read it before finalising Coco's scores
2. Document score deltas per candidate in chat before sending
3. **Aligned (≤5% delta):** proceed to send
4. **Diverging (>10% on any candidate):** flag to Ayesha before going live. Describe the specific disagreement and its source.
5. Do NOT blend or average scores. Both evaluations stand independently. Divergences are useful signal — surface them, don't hide them.

---

## Core Philosophy

The case study is not a test of intelligence. It is a test of honesty of method.

We are not evaluating outputs. We are evaluating how the candidate arrived at those outputs.

Taleemabad roles, especially design and research roles, require people who will use AI tools iteratively, synthesize for themselves, verify what they find, and tell us what they actually found — not what sounds impressive.

**Thinking with data means:**
- Starting from specific observations, not conclusions
- Building testable hypotheses, not narratives
- Checking outputs against raw data before trusting them
- Naming concrete IDs, values, or patterns from the dataset
- Cross-referencing multiple datasets where needed
- Being willing to say "I don't know" where data is insufficient
- Making recommendations specific enough to implement

---

## Prerequisites — What You Need Before Starting

| # | Document | Location | Why |
|---|----------|----------|-----|
| 1 | Case Study Assignment | `temp/case-studies/[Role]/CaseStudy.md` | What were candidates actually asked to do? |
| 2 | Datasets | `temp/case-studies/[Role]/datasets/*.csv` | Read these yourself — you need to know what good answers look like |
| 3 | Evaluation Framework | `temp/case-studies/[Role]/CLAUDE.md` | Criteria, weights, key flags, what a 5 looks like per criterion |
| 4 | Ideal Answer | `temp/case-studies/[Role]/[Role]_Case_Study_Analysis.md` | Calibration benchmark — read BEFORE candidate submissions |
| 5 | Candidate Submissions | Markaz platform + Gmail (hiring@ inbox) | The actual files (.docx / .pdf / .xlsx) — check both, some candidates submit on Markaz, others email directly |
| 6 | Markaz candidate list | MCP query | Application IDs, statuses, contact info |

---

## Step-by-Step Workflow

### Step 1 — Pull the candidate list from Markaz DB

Query the applications table for the role to get application IDs, emails, and current status. Do NOT filter by status alone — DB status is often stale. Some candidates who have submitted still show `shortlisted` instead of `case_study_sent`.

Use Gmail (Step 2) as the authoritative source for who has actually submitted. Use the DB to get contact info and application IDs.

Status reference for KCD stage:
- `shortlisted` — passed values call (may or may not have submitted — verify via Gmail)
- `case_study_sent` — case study sent (may or may not have submitted — verify via Gmail)
- `gwc_scheduled` — KCD already evaluated, moved to GWC interview

### Step 2 — Collect submissions from both sources

Submissions arrive via two channels. Check both before proceeding — some candidates submit on Markaz, others email directly.

**Source A — Gmail (primary check + file download):**
Search using this pattern (no quotes around full phrase):
`subject:New Case Study Submission [Role Name]`
Example: `subject:New Case Study Submission Field Coordinator`

This returns automated Markaz notification emails sent to hiring@taleemabad.com. Each email has the submission files **attached directly** — download using `gmail.users.messages.attachments().get()`. Do NOT use the download links inside the email body — those require Markaz authentication and return 401.

**Source B — DB `case_study_submission` field:**
Query the applications table. The `case_study_submission` field contains the full written text for candidates who typed answers into Markaz. Pull this first — often sufficient for written evaluation without the Word file. `case_study_word_file` and `case_study_excel_file` columns have the server-side file paths (not directly accessible, but the same files are attached to the Gmail notification).

**Google Sheet trackers:** Some candidates submit their tracker as a Google Sheet link instead of an xlsx file. The URL appears in the `case_study_submission` text. Read via Google Sheets API (token: token_sheets.json). Sheet ID is the string between `/d/` and `/edit` in the URL.

Cross-reference both. If a candidate was told to submit but appears in neither source, note as "awaiting submission" — do not evaluate yet.
Do not open or read any submission content yet.

### Step 3 — Extract text from submissions

Parse each file to readable plain text. Preserve structure (headings, lists, tables) where possible.
Name each extracted file clearly by candidate name.
Still do not evaluate anything yet.

### Step 4 — Read all evaluation materials (before touching candidate files)

In this exact order:

1. **Read the Assignment** — understand precisely what candidates were asked to do, what questions they had to answer, what datasets they were given, what the deliverable was.
2. **Read the Datasets yourself** — open every CSV. Understand the shape of the data: what columns exist, what IDs appear, what patterns are visible, what anomalies are present. Form your own hypotheses about what a rigorous analyst would find.
3. **Read the Framework** — if `temp/case-studies/[Role]/CLAUDE.md` exists, this is your primary scoring framework. Use its criteria and weights. If it does not exist, use the default six criteria (see below). If the role file exists but is incomplete, use the default as a drafting scaffold to fill gaps.
4. **Read the Ideal Answer** — this is your calibration benchmark. Understand what the gold standard looks like for this specific assignment before you see any candidate's work.

This sequence is non-negotiable. The philosophy is that you must do the same intellectual work the candidate was asked to do before you are qualified to judge their work. You cannot evaluate honesty of method without first knowing what honest method looks like on this data.

### Step 5 — Read candidate submissions

Only after completing Step 4, open submissions one at a time.
Read each submission in full. Do not skim. Do not skip sections.
While reading, note:
- Whether specific IDs, values, or rows from the dataset are cited
- Whether the candidate shows their path from observation to conclusion
- Whether claims can be traced back to actual data
- Whether AI-generated content signals are present
- Whether conclusions match what you found in the datasets yourself

Annotate your reading notes per candidate before scoring anything.

### Step 5b — Identify incomplete submissions before scoring

Before touching any scores, scan all submissions for completeness. A candidate who submitted 2 of 5 exercises is NOT scored the same way as a candidate who submitted all 5.

**Rule (non-negotiable):** Do not score missing exercises as 0 and include the candidate in the main ranking. A 0 on an unsubmitted exercise looks identical to a genuine 0 (absent/wrong) — the reader cannot tell them apart. This corrupts the ranking.

Pull any incomplete candidate out immediately. Note which exercises are missing. Evaluate only what was submitted. They go in a separate section — see Step 7b.

### Step 6 — Score each candidate (1–5 per criterion)

| Score | Meaning |
|-------|---------|
| 5 | Exceptional — original insight grounded in specific data evidence |
| 4 | Strong — correct and thoughtful, minor gaps |
| 3 | Adequate — correct but surface-level or generic |
| 2 | Weak — missed key patterns, or used AI as content generator |
| 1 | Absent or fundamentally wrong |
| 0 | Not submitted — only valid for incomplete submissions |

**Scoring rules:**
- Strong reasoning + minor data errors → score high (4–5)
- Weak reasoning + correct outputs → score lower (2–3)
- Insight without evidence → cap at 3
- Evidence without interpretation → cap at 3
- **Use fractional scores (e.g. 4.5, 3.5) where a candidate is genuinely between two whole numbers** — fractional scores give more accurate final percentages and prevent compression of meaningful differences between candidates
- **When a criterion exercise is missing:** score 0 only for that criterion. Do NOT average or extrapolate from other exercises to fill the gap.

**Calibration — what a 5 looks like in a fundraising/BD context:**
- Not just correct prioritization, but naming the right stakeholder, the right framing, and the right deliverable for each funder in one move
- Not just a good email, but a close that turns a vague non-answer into a targeted, specific next step
- Commercially sophisticated reasoning that goes beyond frameworks — e.g. spotting a time-sensitive co-branding angle no other candidate saw

Apply weights from the role-specific framework (or default weights if none exists). Calculate final weighted percentage.

### Step 7 — Integrity check (mandatory, every candidate)

Cross-check all candidates in the batch against these three flags:

1. **Content dump** — emoji in body, `###` markdown headers, parenthetical citations like (SpringerLink), off-topic research, generic language that does not map to the actual dataset. Early sections may look fine; later sections usually collapse. Flag and note.
2. **Mirror problem** — identical statistics, phrases, or conclusions across two candidates in the same cohort. Both likely ran similar AI prompts without independent verification. Still issue scores for both, but attach explicit flag and recommend debrief before advancing either.
3. **Foundational misread** — candidate gets a key anchor figure, archetype, or variable wrong early on. All downstream reasoning is therefore built on a false premise. This signals they did not read closely. Flag as serious signal.

Additional anti-gaming signals to watch for:
- Consulting-style voice: over-structured, low substance
- Narrative inflation: strong claims without data anchors
- Overfitting: a neat story that ignores contradictory data
- Evidence theater: references to "the data" without exact rows, IDs, or values

**Rule:** If it sounds impressive but cannot be traced back to specific rows, values, IDs, or observable patterns in the dataset — penalize it.

### Step 7b — Incomplete submission handling (MANDATORY)

Before building the report, identify any candidates with incomplete submissions.

**Rule: a partial score cannot be ranked alongside full submissions.**

An incomplete candidate must:
1. Be **excluded from the main ranking** entirely
2. Appear in a **separate section** titled "Incomplete Submission — [Name]"
3. Have their score marked with an asterisk and a footnote: `52%* — incomplete submission, not a capability read`
4. Have a **supplementary assessment recommendation** instead of a GWC/no-GWC verdict

The note "their score is a floor, not a ceiling" must appear in the section header or tagline when the partial submission shows strong signals.

**Never rank a candidate with 2/5 exercises above someone who submitted all 5**, even if the raw math produces a higher number. The math is not comparable — it is measuring different amounts of information.

### Step 8 — Build and send the evaluation report

**Format:** HTML email (rich inline report — not a PDF attachment for KCD reports).

**Per-candidate output block (mandatory structure, every ranked candidate):**
1. Verdict label + final weighted score (%)
2. **Confidence level** — state explicitly with a one-line reason. Example: "High confidence in direction, some uncertainty in magnitude given limited track record data." This is more useful than a bare verdict. Noah does not do this yet — keep it.
3. 1-line tagline — lead with the candidate's strongest signal, not their score
4. Narrative — per-exercise evidence (see standard below)
5. Gap — clearly labelled, separate paragraph. One gap per paragraph. Names the specific dimension and what it means for the role.
6. **Conditional verdict clause** — if verdict is CONDITIONAL, this is mandatory: "Condition: [specific thing that must happen before this candidate proceeds]." Name the exercise if supplementary. Name the topic if a GWC probe. "CONDITIONAL" with no stated condition is not actionable — do not send it.
7. **GWC conversation guide** — 3 to 4 probing questions per candidate, tied directly to their case study. Not generic interview questions. The panel must be able to walk into GWC and use these directly. Format per question: "[Gap observed] — [probe question that surfaces whether this is a real weakness or a submission artefact]."
8. Integrity flag — name the exact signal if present. "Clean" if not.

**Narrative standard — per-exercise evidence (non-negotiable):**
- Tie every observation to a specific exercise by number: "E2 (cold room) — she refused the vague 'send me an email' close and reframed to a targeted 2-pager deliverable."
- This makes the narrative verifiable. The panel can re-read the submission and find the exact moment being described.
- Quote exact lines where the signal is strong. Paraphrase loses the evidence.
- Name the specific technique, not just the conclusion.
- Name what this candidate did that others in the cohort did NOT do. Comparative signals are more informative than isolated praise.

**Cross-candidate comparative analysis (Coco strength — keep this):**
- After all individual blocks, add 2–3 sentences comparing candidates in aggregate: where strengths concentrate, where the cohort as a whole is weak, where one candidate clearly outperforms another on a specific dimension.
- Example: "Maria's strength is concentrated in E2 and E3 while Amina shows broader instincts across the full exercise set — different risk profiles for the same role."
- This gives the hiring manager a faster read on cohort shape than individual scores alone.

**Email recipients:**
- Pilot mode (user says "pilot"): TO = ayesha.khan@taleemabad.com, CC = jawwad.ali@taleemabad.com
- Live mode (user says "make it live"): TO = ayesha.khan@taleemabad.com + hiring manager, CC = hiring@taleemabad.com

Always address the hiring manager by first name — query the users table, never use a generic name.

---

## Verdict Labels

| Score | Verdict |
|-------|---------|
| 85–100% | STRONG HIRE |
| 70–84% | HIRE |
| 55–69% | CONDITIONAL |
| 40–54% | BORDERLINE |
| <40% | NOT RECOMMENDED |

---

## Default Scoring Criteria (fallback only)

Use these **only** if no role-specific framework exists in `temp/case-studies/[Role]/CLAUDE.md`.

| Criterion | Weight |
|-----------|--------|
| AI Tool Fluency | 25% |
| Anthropological/Domain Insight | 20% |
| Psychological Depth | 15% |
| Ethical Reasoning | 15% |
| Cross-Cultural Thinking | 15% |
| Design Clarity | 10% |

---

## Coco + Noah Calibration Standard (confirmed 2026-03-31 — Jawwad Ali brief)

### What Coco adopts from Noah


Noah's report structure is already the template. These are the specific writing and scoring behaviours to match:

- **Fractional scores** (4.75, 3.5, 1.5) — whole numbers compress meaningful differences
- **Score 0 only for missing exercises** — never use 0 as a penalty for weak work (use 1)
- **Quote exact lines** — do not paraphrase when the signal is in the exact wording
- **Name specific techniques**, not just conclusions: "E2 — she reframed the vague close to a targeted 2-pager" not "her cold room was strong"
- **Comparative signals** — name what this candidate did that others did NOT do
- **Transferable skills named explicitly** — what carries over, what doesn't, before scoring

### What Noah adopts from Coco (Jawwad's brief, confirmed 2026-03-31)
- **Explicit confidence levels per verdict** — "High confidence in direction, some uncertainty in magnitude" — Noah does not do this yet; Coco continues it
- **Cross-candidate comparative analysis** — aggregate cohort read after individual blocks
- **Explicit numeric advancement threshold (60%)** — cleaner than verdict labels alone
- **Conditional verdict clauses** — every CONDITIONAL must state: "Condition: [specific thing that must happen before proceeding]" — name the exercise or GWC probe topic explicitly
- **GWC conversation guide per candidate** — 3 to 4 specific probing questions tied to case study gaps; not generic; format: "[gap observed] — [probe question]"
- **Per-exercise evidence in narratives** — tie every observation to E1/E2/E3/E4/E5 by number so the panel can verify

### What stays the same (Coco's core — do not change)
- HTML email format and visual design (colour tokens, section headers, chip styling)
- Verdict label thresholds (85%+ STRONG HIRE / 70–84% HIRE / 55–69% CONDITIONAL / 40–54% BORDERLINE / <40% NOT RECOMMENDED)
- Integrity flags section (consolidated, after all candidate blocks)
- Pipeline recommendations table as final section
- GWC advancement threshold: 60%+
- Pilot → live send workflow
- Pushing back when asked to apply the wrong benchmark — do not let the panel compare criteria across different roles (e.g. FM criteria vs Soul Architect criteria — different roles, different frameworks)

---

## Framework Override Rule

The framework is a guide, not a cage. If a candidate demonstrates exceptional thinking but does not fit neatly into the scoring structure, override the mechanical score with clear written justification. Judgment is more important than rigid box-checking.

---

## Correct vs Trustworthy

A correct answer is not enough. We are hiring for trustworthiness of judgment.

| Type | Signals |
|------|---------|
| Correct but weak | Gets right answers, cannot explain how, limited verification, AI-dependent |
| Strong but imperfect | May miss minor details, but shows reasoning discipline, verifies claims, transparent about uncertainty |

**Always prefer the second.**

---

## Final Test Before Submitting a Verdict

Before finalising any verdict, ask:

> "Would I trust this person to analyze a messy real-world problem without supervision?"

- Yes, strong evidence → HIRE / STRONG HIRE
- Maybe, meaningful gaps → CONDITIONAL / BORDERLINE
- No → NOT RECOMMENDED

---

## Transferable Skills — When to Credit vs Penalise

When a candidate's track record comes from a different sector, do not flat-penalise it. Assess what genuinely transfers and what does not, then score accordingly.

| Scenario | How to score |
|---|---|
| Corporate IT / commercial BD → development sector fundraising | Credit: positioning, relationship access, compliance navigation, deal structuring. Do NOT credit: funder psychology, bilateral/foundation cultivation, grant cycles, donor stewardship. Score 3/5 if strong commercial BD, no development sector experience. |
| Constructed hypothetical in track record exercise | Do not score it as if it were real. Score 2/5 maximum — flag for GWC verification. If verified at GWC: upgrade. If constructed: capability still real, but no verified track record. |
| Missing exercise due to documented circumstances (illness, access failure) | Score 0 for that criterion. Do NOT infer from other exercises. Handle as incomplete submission (see Step 7b above). |

**Rule:** Penalising someone for a sector gap they can articulate clearly and bridge thoughtfully is worse than crediting them for it. The question at GWC is: "Can you make this transition?" — not "Have you already made it?"

---

## Gold Standard Benchmarks (Soul Architect Pilot, March 2026)

Use these for calibration on what strong work looks like.

**Aaqib Khan — 94% — Gold standard: AI Tool Fluency + Data Rigor**
Named T073, T092, T099 by teacher_id with exact scores. Calculated 7.4x correlation between voice messages and coaching uptake. Wrote actual system prompt code with before/after test cases. Proposed A/B testing as validation methodology.

**Zikra Fiaz — 93% — Gold standard: Anthropological Insight + Ethics**
"Complete Professional Threat" hypothesis: Sri Lankan NCE teachers hold credential-backed identities — an AI coaching tool implies their training was insufficient. This is an identity-level challenge, not a missing feature. Best dignity-preserving messages in the cohort.

**Nain Tara — 88% — Gold standard: Writing + Soul Design**
Named teacher archetypes with human labels: "The Reluctant Confessor", "The Throughput Machine", "The Polite Distancer". Closing line: "The most important decisions in a product like Rumi are not interface decisions. They are character decisions."

**Danyal Haroon — 88% — Gold standard: Cross-Dataset Investigation**
Found a dataset pipeline anomaly: T099 listed as Sri Lankan but has Urdu coaching sessions. Identified T073's very first interaction was a late-night burnout voice note — before any coaching began. Built a 6-signal burnout predictor framework.

---

## Gold Standard Benchmarks (Fundraising & Partnerships Manager, Job 32, March 2026)

**Mizhgan Kirmani — 83% — Gold standard: Cold Room Execution + Funder Brief Positioning**
E2 cold room: opens with curiosity not information, listens before bridging, handles each objection with specific evidence pivots. Her close refuses the vague "send me an email" brush-off and reframes to a targeted deliverable ("a 2-pager specifically on how we work with government at scale"). That is a practitioner technique, not textbook advice. E4 funder brief adds an "Insight" layer before the solution — diagnosing why scale fails (delivery model, not intent) before positioning Taleemabad as the answer.
Flag: E5 track record is a constructed hypothetical. $350K Punjab grant named but no real funder or timeline. Must verify at GWC.

**Hamdan Ahmad — 52% (incomplete, floor not ceiling) — Gold standard: Pipeline Intelligence + Donor Writing**
Only candidate to identify Funder F's 3-week CSR deadline as a structural urgency signal and reframe Rumi as a co-branded connectivity layer through the telco's own mobile infrastructure. Named the right stakeholder (CSR decision-maker, not comms team) and the right deliverable in one move. E3 re-engagement email: "the ground has shifted considerably" as the opening line, specific milestone sequencing, genuine exit offered ("if the fit isn't right, I'd value knowing that too"), no pressure close. Writing quality noticeably above cohort average. 3 of 5 exercises missing due to hospitalisation — not a capability verdict.

**Zain Ul Abideen — 74% — Sector Transition Candidate**
Correctly identified that Funder E's prior objection (no government integration) was resolved by the Punjab 6,000-school partnership. That is a specific, astute strategic read. Full submission, consistent quality. Track record is $10M Microsoft Enterprise Licence Agreement — corporate IT procurement, not development fundraising. Transferable skills are real; sector gap is material. One credibility error: fabricated prior relationship warmth in E3 re-engagement email.
