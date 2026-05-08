---
name: Lessons Learned Log
description: Structured append-only log of mistakes, corrections, and rules. Updated by Stop hook after each session.
type: project
max_entries: 50
---

# Lessons Learned — Agent Coco

> **Format:** `## YYYY-MM-DD — [Task Type]` then bullets: Mistake, Correction, Rule.
> **Limit:** 50 entries max. When exceeded, summarize oldest 25 into "Archived Rules" section below.

## 2026-04-14 — CV Screening
- **Mistake:** Fabricated candidate details not present in CV
- **Correction:** Halted, re-read CV, corrected report
- **Rule:** No claim about a candidate goes in the report without a direct quote or line from their CV

## 2026-04-15 — Teams API Query
- **Mistake:** Teams query returned 1 message; assumed "no data" and missed 2 leave announcements (Haya Abid, Sabeen Fatima)
- **Correction:** Cross-checked with Ayesha who confirmed the leaves
- **Rule:** Suspiciously small result sets (< 5 items from a team channel) must be verified with a second source before reporting

## 2026-04-20 — Attendance Report
- **Mistake:** Skipped reading attendance template memory; generated report with grid borders, wrong colors, wrong stat count
- **Correction:** Re-read `attendance_report_complete_template.md`, regenerated from scratch
- **Rule:** Read the locked template memory file BEFORE writing any code for attendance reports

## 2026-05-05 — Warm Bench Emails
- **Mistake:** Mahnoor's email deviated from locked template (word count, signature format)
- **Correction:** Re-ran against `warm_bench_final_locked_approach.md` side-by-side
- **Rule:** Print the locked template next to the draft before sending; never send from memory alone

---


## 2026-05-08 — General
- **Mistake:** Used wrong template
- **Correction:** Re-read locked template file before regenerating.
- **Rule:** [Coco: add rule summary here]

## Archived Rules
<!-- Condensed from entries older than 60 days -->
- Never use cv_text[:4500] — minimum 10k chars for CV truncation (2026-04-08)
- Every name in every decision brief section must have a Drive CV hyperlink (2026-04-08)
- Replying in-thread requires In-Reply-To + References headers (2026-04-08)
- status='offer' in DB is a pipeline stage, NOT a sent offer — never assert (2026-04-08)
- ALL ReportLab PDFs must use TA_JUSTIFY on body paragraph styles (2026-04-03)
