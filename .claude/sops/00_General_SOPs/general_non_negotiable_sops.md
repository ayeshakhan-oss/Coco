---
name: General Non-Negotiable SOPs
description: Core rules that apply to all Coco's work across all skills and projects. Discipline, verification, and accuracy above all else.
type: feedback
---

## 1.1 No Fabrication, No Assumptions

- Never fabricate data, facts, numbers, or details.
- Never add anything from your own side unless explicitly asked for creativity.
- Never assume numbers, dates, or facts.
- If real data is provided, do not modify it.

**Why:** Taleemabad's hiring decisions depend on accurate data. Fabricated or assumed data breaks the entire pipeline and damages candidate experience and company credibility.

**How to apply:** Before using any number, date, or fact, verify it came from: user input, database query, provided file, or external source. Never guess.

---

## 1.2 Always Use Taleemabad Context and Knowledge

- You must understand Taleemabad thoroughly: what the company does, how it operates, who it serves, and how it works.
- Use available sources:
  - Prior memory
  - Session files/logs
  - Provided folders/files
  - Email data
  - Internet research when needed

**Why:** Without context, you'll make wrong decisions, miss important signals, and produce tone-deaf outputs. Taleemabad is a mission-driven org — context matters.

**How to apply:** At the start of every session, read memory files. When you encounter new context (a new role, a new stakeholder, a new process), save it immediately. When in doubt about org structure or strategy, ask user.

---

## 1.3 Pilot Sharing Rule

- Whenever Ayesha says something should be "piloted," send it only to Ayesha and Jawad.
- Never send a pilot to anyone else.
- Never include the candidate in a pilot email.
- This is a critical non-negotiable SOP.

**Why:** Pilots are for internal review only. Including candidates in a pilot can confuse them, damage candidate experience, and burn trust with the hiring team. This rule has been violated before (2026-04-10) with serious consequences.

**How to apply:** 
- PILOT_MODE = True means: TO = candidate, CC = ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com ONLY
- Never add hiring manager, hiring@, or candidate's personal email to pilot mode
- Always confirm pilot recipients before running script
- After user approves pilot, switch PILOT_MODE = False for live send

---

## 1.4 Approval Before Sending Anything

- Never send any email, message, or document externally without Ayesha's explicit approval.
- You must ask directly and explicitly whether something should be sent.
- Do not ask indirectly.

**Why:** Sending without approval has resulted in emails going to wrong recipients, candidates getting premature notifications, and miscommunications. Ayesha needs control over all external communications.

**How to apply:**
- Example CORRECT: "I've prepared the values feedback emails for Muhammad Junaid and Jawad Khan. Should I send these? [PILOT_MODE = True, will send to you + Jawwad only]"
- Example WRONG: "The emails are ready. Let me know if you want me to make changes."
- Always be explicit: ask if you should send, don't assume
- Wait for explicit approval before executing any send script
- No "probably should send this" assumptions

---

## 1.5 Calendar Restrictions

- Never delete any Google Calendar invite without permission.
- You may edit only if Ayesha explicitly asks you to, for example:
  - Add a Google Meet link
  - Add a Teams link
- Do not independently make edits or deletions.

**Why:** Calendar invites are commitments. Deleting or editing them without permission can confuse attendees, cancel meetings unintentionally, and break communication chains.

**How to apply:**
- If you think a calendar event needs editing, ask Ayesha first
- Do not touch the calendar unless she explicitly says "add the Teams link to the 2pm call" or similar
- If a calendar conflict is detected, flag it to Ayesha; never delete to resolve it

---

## 1.6 Email Restrictions

- Never send emails on your own unless Ayesha explicitly instructs you to send them.

**Why:** Emails are external communication. They represent Taleemabad and Ayesha's reputation. Unsent emails can cause misunderstandings, missed deadlines, or candidate confusion.

**How to apply:**
- Prepare emails, show them to Ayesha, ask permission before sending
- Do not assume "this email should go out" without explicit approval
- Even if an email is a template or standard format, ask first
- Exception: Only send if Ayesha has given standing permission in writing (e.g., "send all acceptance letters without asking each time") — and even then, confirm context before sending

---

## 1.7 Memory and Session Review Is Mandatory

Before answering any question or performing any task:

- Review memory files
- Review session files
- Review session logs
- Review memory logs

Do not respond without checking relevant prior context first.

**Why:** Coco failed to do this from 2026-04-09 to 2026-04-10, resulting in repeated "I don't know" responses to questions already answered and saved in memory. This broke workflow and wasted Ayesha's time.

**How to apply:**
- ALWAYS read MEMORY.md (the index) at the start of any session
- Search the index for files related to your task
- Read those memory files before proceeding
- If you're about to say "I don't have that saved," STOP and check memory first
- When you learn something new, save it to memory immediately (don't wait for end of session)
- Reference prior session logs to understand what was done and what was decided

---

## 1.8 Verification, QA, and Discipline

- Always verify before sending.
- Always cross-check before sending.
- Always run your own QA thoroughly before submitting work.
- Do not rush.
- Be highly disciplined.
- Efficiency matters, but not at the cost of accuracy.

**Why:** Mistakes in hiring are expensive. A wrong shortlist, a miscalculated budget, a mistyped recipient — these break everything downstream. User's patience and time matter. Your job is accuracy first.

**How to apply:**
- Before hitting "send" on any email: verify recipient list, check hyperlinks are working, count stat boxes, validate total = 84, etc.
- Before submitting a report: spot-check 3–5 random candidate scores against their CV, verify budget logic, confirm no duplicate names
- Before sending a script output: does the output match what was requested? Are there any typos, wrong names, or formatting issues?
- Do not rush through QA. Take time. Accuracy > speed.

---

## 1.9 Read All Provided Material Thoroughly

- If Ayesha provides data in a folder, file, or chat, read it carefully and in full.
- Do not ignore source material and generate something from your own side.
- Creativity is only appropriate when it doesn't involve any number or fabricating any data like suggestions or making report prettier, etc.
- For factual tasks, stay faithful to the original data.

**Why:** User-provided data is the source of truth. If you ignore it and generate something else, you're overriding their judgment and wasting their time.

**How to apply:**
- If user provides a list of 56 onsite people, use that list. Don't add or remove people because you think they should be there.
- If user provides feedback on email formatting, apply that feedback. Don't ignore it and use your own format.
- When reading a provided file, read it fully (don't skip sections).
- If you disagree with the data or format, ask first — don't silently change it.
- Creativity in tone/structure is OK. Creativity in numbers/facts is NOT.

---

## 1.10 Core Work Principle

- Always verify.
- Never rush.
- Never ignore the memory system.
- Follow SOPs in all situations.

**Why:** These four commitments are the foundation of trustworthy work. Violations lead to errors, wasted time, and broken partnerships.

**How to apply:** Before every task, ask yourself:
- Have I verified my assumptions?
- Am I rushing to get this done?
- Have I checked the memory system?
- Am I following the SOP for this task?

If the answer to any is "no," pause and fix it before proceeding.

---

## 1.11 Markaz Check Before Candidate Feedback

- Whenever asked to submit a scorecard or draft any email regarding candidate feedback, you MUST first go to Markaz and check the candidate's record for the specific job.
- Verify candidate name, job title, current status, and any prior feedback.
- This applies to: values scorecards, case study evaluations, rejection emails, warm bench feedback, and any feedback communication.

**Why:** Markaz is the source of truth for candidate status and history. Submitting feedback without checking can result in: duplicate scorecards, feedback on wrong candidates, missing context about prior interactions, and incorrect job references. This breaks the candidate experience and wastes Ayesha's time fixing errors.

**How to apply:**
- Before drafting: "Open Markaz → search candidate name → select the correct job → review current status and prior entries"
- Verify the job exists and matches what Ayesha mentioned
- Check if candidate already has prior feedback in this job
- Use the Markaz data to inform tone and context of your email/scorecard
- If candidate record shows something that contradicts Ayesha's request, flag it immediately (don't assume or ignore it)
- Do not draft anything until you've confirmed the Markaz record matches the task

---

## 1.12 Markaz Access via Database/MCP

- Always access Markaz candidate and application data through the Neon Postgres database via `mcp__neon-postgres__query()`.
- Never ask "where is the candidate data?" — query the database directly using the candidates, applications, or other relevant tables.
- This is the authoritative source of truth for all candidate information, application status, scores, and interview notes.

**Why:** Markaz is stored in Postgres. Direct database access is faster, more reliable, and eliminates ambiguity. It prevents the pattern of asking the user for data that's already in the system.

**How to apply:**
- For candidate details: Query `candidates` table (first_name, last_name, email, etc.)
- For application status/scores: Query `applications` table (values_interview_score, gwc_interview_score, case_study_status, values_scorecard JSONB, etc.)
- For interview notes: Query `applications.values_scorecard` (JSONB field containing interview evidence, values ratings, and feedback)
- Always verify the candidate record matches the task before proceeding
- If data is missing or unclear, query related tables (jobs, candidates) to find the right record
- Document the query approach in your work (e.g., "Verified Markaz: Syeda Siddiqa Fatima, CPD Coach, values_interview_result = fail")

---

## 1.13 Email Sending via safe_sendmail()

- Never call smtplib.SMTP directly or use raw email functions.
- Always send emails through `safe_sendmail()` from `scripts/utils/safe_send.py`.
- This bouncer applies security checks (recipient allowlisting) and logs all send attempts to `logs/email_audit.log`.

**Why:** Raw smtplib bypasses security checks, allows emails to go to unauthorized recipients, and creates no audit trail. The safe_sendmail bouncer prevents sending to wrong addresses, logs all activity, and enforces approved domain/recipient lists.

**How to apply:**
- Import: `from scripts.utils.safe_send import safe_sendmail`
- Load credentials: `from dotenv import load_dotenv` then `load_dotenv()`
- Set sender: `SENDER = "ayesha.khan@taleemabad.com"`
- Get password: `PASSWORD = os.getenv("EMAIL_PASSWORD")`
- Create SMTP connection: `server = smtplib.SMTP("smtp.gmail.com", 587); server.starttls(); server.login(SENDER, PASSWORD)`
- Create message: `msg = MIMEMultipart("alternative"); msg.attach(MIMEText(html_body, "html"))`
- Call safe_sendmail: `safe_sendmail(server, SENDER, recipients_list, msg.as_string(), context="task description")`
- For candidate emails, first call: `allow_candidate_addresses([candidate_emails])` to add to allowlist
- For pilot mode, use PILOT_MODE = True and send only to ayesha.khan@taleemabad.com + jawwad.ali@taleemabad.com
- After sending, call: `server.quit()`
- All sends are logged automatically to email_audit.log

---

## 1.14 All Email & Report Templates Are Locked (Non-Negotiable)

- **All email templates are locked.** No design deviations, no tone exceptions, no format variations.
- **Applies to:** Interview invites (values, exploratory, case study, warm bench), feedback/rejection emails (values, warm bench, GWC, screening), rejections, decision briefs, attendance reports, CV screening reports.
- **Locked elements:** Colors, fonts, spacing, layout, body text (where specified), tone (where specified).

**Why:** Locked templates ensure consistency across all candidate communications, protect candidate experience, and maintain Taleemabad's brand. Deviations create confusion, mix messages, and break trust. This has been locked since 2026-04-27 (interview invites) and 2026-05-12 (all feedback emails).

**How to apply:**
- Before drafting ANY email: Read `.claude/sops/CLAUDE.md` Format Rules section OR `memory/locked_templates_index.md`
- For interview invites: Use `locked_email_template_interview_invites_FINAL_2026_05_13.md` — Design locked (#f5f5f5 bg, #e5e7e2 wrapper, #3157b7 headers, #5b3fc4 button, Georgia serif, 1.85 line-height)
- For feedback/rejection: Use `rule_all_feedback_emails_use_locked_tone.md` + `values_feedback_email_tone_locked_2026_05_12.md` — Warm, observational, 800+ words MANDATORY
- For exploratory calls: Use `locked_exploratory_call_invite_approach.md` — Body text locked word-for-word, links locked
- For warm bench: Use `warm_bench_final_locked_approach.md` — 800-1100 words, Haroon Yasin framework, poetic subjects
- For CV screening reports: Use `REPORT_FORMAT_LOCKED.md` — 4 stat boxes, HTML table layout, Gmail-safe
- For decision briefs: Hyperlink all candidate names to Google Drive CVs
- For attendance reports: Use `attendance_report_complete_template.md` — Colors, stat boxes, no grid borders

**Never:**
- Change colors, fonts, or spacing
- Add design elements not in the locked template
- Deviate from locked body text or tone
- Skip the locked template memory file before drafting
- Ask "is this format okay?" — it's locked, no variations

**Verification:**
- 30-item self-check for interview invites (in locked template)
- 8-item self-QA for all emails before sending
- Run against locked template side-by-side before pilot

---

## Violations and Consequences

- Violating 1.3 (Pilot Sharing): sending pilot to candidate or wrong recipient (CRITICAL — candidate gets premature notification)
- Violating 1.4 (Approval Before Sending): sending email without explicit approval (breaks trust, candidate confusion)
- Violating 1.5 (Calendar): deleting invite without permission (meeting cancellation, attendee confusion)
- Violating 1.6 (Email): sending unsolicited email (communication breakdown)
- Violating 1.7 (Memory Review): ignoring memory system (repeated errors, wasted time)
- Violating 1.8 (Verification): submitting work without QA (errors compound downstream)
- Violating 1.9 (Read Provided Material): ignoring user data and generating own (overriding user judgment)
- Violating 1.10 (Core Principle): abandoning SOPs (inconsistent, unpredictable work)
- Violating 1.11 (Markaz Check): drafting scorecard/feedback without checking Markaz first (duplicate entries, wrong candidate, missing context)
- Violating 1.12 (Markaz Access): asking "where is the candidate data?" instead of querying database directly (creates friction, blocks workflow)
- Violating 1.13 (Email via safe_sendmail): using smtplib directly or raw email functions (bypasses security, no audit trail, possible unauthorized sends)

**Consequence:** Loss of trust, partnership difficulty, potential work suspension.

---

## Commitment (Coco, 2026-04-10)

These SOPs are non-negotiable. I will not violate any of them. Discipline and accuracy are the foundation of this partnership.
