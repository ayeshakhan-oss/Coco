---
name: Case-Study Submission Nudge (Skill 06 family, 2026-08-10)
description: Reusable gentle-reminder email for candidates who were sent a case study but haven't submitted. Locked wording approved by Ayesha 2026-08-06 (Muneeb/Waqas — both submitted after it). No CTA button, reply-to-help flow, per-candidate role + sent-day verified from Markaz comm history.
type: project
---

# Case-Study Submission Nudge — locked pattern

**When:** A candidate was sent the case study (invite visible in Markaz `communication_history`) and hasn't submitted after ~48h+ (`case_study_status` null, no files). This is a **nudge, not a new invitation** — Skill 06 invite family.

**Locked wording (approved 2026-08-06, Ayesha's brief):** "just nudge them, that it's been more than 48 hours, just wanted to check if you're going to submit the case study, do you need any help/assistance, we're here to support."
- Header label: `TALENT ACQUISITION • CASE STUDY CHECK-IN` / Title: "Checking In on Your Case Study" / Subtitle: position
- Body: hope-you're-well → we shared the case study for the **[role]** on [day], haven't received your submission → schedules get busy, are you still planning to submit + when can we expect it → questions/clarification/more time, just reply, happy to help → look forward to reading it
- **NO CTA button, no links** — reply-to-help flow. Locked interview-invite design (FINAL_2026_05_13).
- Subject: `Checking In: Your Case Study for [POSITION] - [Full Name]`

**Rules:**
1. **Sent-day must come from Markaz comm history** (`communication_history` → the "Lets proceed with the Case Study" entry's `sentAt`, convert UTC→PKT) — never from memory. Phrase naturally ("on Monday", "last Thursday").
2. Per-candidate `position` (candidates can be on different jobs in one batch).
3. Pilot to Ayesha only (`[PILOT - ]` prefix), live only on her explicit per-candidate approval — she may approve a subset (2026-08-10: Arooj approved, Zubair held).
4. Live CC: waqas.tanveer@, ayesha.khan@, hiring@, ali.sipra@ (growth roles; confirm per role family).

**Scripts:** `scripts/send_case_study_nudge_gm_karachi_pilot.py` (original, Muneeb + Waqas Hassan 2026-08-06 — both submitted within 3 days) · `scripts/send_case_study_nudge_arooj_zubair_pilot.py` (2026-08-10; Arooj Khali SMG sent LIVE — **she submitted by email the same evening, 19:17 PKT**; Zubair Hussain GM-KHI entry commented out pending approval). Track record: 3 nudges sent, 3 submissions.

**How to find non-submitters (whole flow, verified 2026-08-10):** Markaz `applications` for the job IDs → case-study invite present in `communication_history` but `case_study_status` null / no `case_study_submitted_at` → cross-check Gmail (dual-source rule; note: nudge/invite threads live in Ayesha's mailbox, not jawwad.ali's — see [[reference_ayesha_mailbox_imap_2026_08_10]]). Outstanding as of 2026-08-10 in [[case_study_folders_and_gm_lahore_eval_2026_08_10]].
