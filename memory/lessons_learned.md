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

## 2026-05-12 — Values Scorecard Submission (Laiba Ahmad, Job 20)
- **Mistake:** Submitted scorecard to Application 1389, but Markaz UI displayed Application 2708 (more recently updated). Form showed empty despite successful database submission.
- **Correction:** Queried for all application records for candidate+job, identified most recent (2708), created new submission script targeting correct record.
- **Rule:** ALWAYS query for duplicate application records before submitting values scorecard. Markaz UI displays most recently updated record. Submit to that one, not an older record.

## 2026-05-30 — Warm Bench Live Email Subject Line (Huma Mumtaz)
- **Mistake:** Sent LIVE email to huma.mumtaz3@gmail.com with subject "[PILOT – Huma Mumtaz] When You Stop a Meeting to Protect Your Team". The [PILOT – ] prefix should ONLY appear in pilot emails sent to Ayesha, NOT in live emails to candidates.
- **Correction:** Cannot undo (email already sent). Must add validation logic to prevent in future.
- **Rule:** Before switching PILOT_MODE = False, VERIFY subject line construction. Subject must be cleaned of "[PILOT – Candidate Name]" prefix for live sends. Add explicit subject line variable validation. [PILOT – ] prefix must ONLY exist when PILOT_MODE = True.

---

## Archived Rules
<!-- Condensed from entries older than 60 days -->
- Never use cv_text[:4500] — minimum 10k chars for CV truncation (2026-04-08)
- Every name in every decision brief section must have a Drive CV hyperlink (2026-04-08)
- Replying in-thread requires In-Reply-To + References headers (2026-04-08)
- status='offer' in DB is a pipeline stage, NOT a sent offer — never assert (2026-04-08)
- ALL ReportLab PDFs must use TA_JUSTIFY on body paragraph styles (2026-04-03)

## 2026-08-13 — Contract Drafting (Muhammad Shayan Fellow package)
- **Mistake:** Claimed "formatting fixed" three times on structural evidence (placeholder scans, master diffs, indent values) without ever seeing a rendered page. There is no Word/LibreOffice on this machine. Ayesha caught every layout defect by screenshot; the package took 6 review rounds.
- **Correction:** Diagnosed each defect in the XML (heading right-indent ~5.3", empty auto-numbered paragraph, in-body NEW_PAGE section breaks, deepcopy duplicating sectPr, style-inherited bold lost in PDF conversion, missing keep_with_next), fixed the causes, and built a validator + blocking send hook encoding all of them.
- **Rule:** Structural verification is NOT visual verification. Never claim a layout fix is done without a human eye on the page — state the limitation and ask Ayesha to look. See CLAUDE.md Rule 14 and .claude/sops/07_Contract_Documents/CONTRACT_DOCX_BUILD_SOP.md.

## 2026-08-13 — Contract Drafting (pilot email hygiene)
- **Mistake:** Put a pilot banner, flags and open questions inside the candidate email body, and sent the pilot as a standalone email instead of threading it into the conversation Ayesha had with the candidate.
- **Correction:** Removed all meta-commentary; pilot and live now share one body and both thread onto the original via In-Reply-To/References. Mirrored the original email's formatting and signature by pulling it from Ayesha's Sent folder over IMAP.
- **Rule:** The pilot IS the email — byte-identical to what the candidate receives, only the recipient differs. Notes to Ayesha go in chat. Harness blocks meta-commentary in email bodies.

## 2026-08-13 — Contract Drafting (package composition)
- **Mistake:** Locked a rule that "contract + NDA always ship together", which was wrong — volunteer/unpaid Fellows receive the NDA only, and an unpaid-to-paid transition receives the contract only.
- **Correction:** Corrected the rule everywhere and added a send-time block that refuses a volunteer email carrying a contract, or a transition email carrying an NDA.
- **Rule:** Confirm paid vs volunteer BEFORE building anything; never infer engagement type from a role title.
