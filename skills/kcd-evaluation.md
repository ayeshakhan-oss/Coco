# Skill: KCD Case Study Evaluation

KCD = Knowledge, Capability, Design. Second-to-last filter before the GWC/technical interview.
Pipeline position: Values Call → **KCD Case Study** → GWC Interview.
Never send a case study to someone who failed values.

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

### Step 6 — Score each candidate (1–5 per criterion)

| Score | Meaning |
|-------|---------|
| 5 | Exceptional — original insight grounded in specific data evidence |
| 4 | Strong — correct and thoughtful, minor gaps |
| 3 | Adequate — correct but surface-level or generic |
| 2 | Weak — missed key patterns, or used AI as content generator |
| 1 | Absent or fundamentally wrong |

**Partial credit rules:**
- Strong reasoning + minor data errors → score high (4–5)
- Weak reasoning + correct outputs → score lower (2–3)
- Insight without evidence → cap at 3
- Evidence without interpretation → cap at 3

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

### Step 8 — Build and send the evaluation report

**Format:** PDF attachment, same structure as the screening analysis report. Landscape A4, generated with reportlab + matplotlib.

**Per-candidate output block (in PDF):**
1. Verdict label (see below)
2. Final weighted score (%)
3. Confidence level: High / Medium / Low
4. Criterion-by-criterion scores with brief evidence per criterion
5. Candidate narrative — specific summary of how they think, where strong, where weak, whether method was trustworthy
6. Integrity flags — explicitly list any content dump signals, duplication concerns, foundational misreads, or "none" if clean

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
