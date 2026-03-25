# Memory — Accumulated Learnings

This file grows over time. After every successful task, save what you learned here.
The agent reads this file at the start of every session (right after CLAUDE.md).

---

## Database Patterns
- `resume_data` in candidates table is **Base64-encoded PDF**, NOT plain text. Must decode → parse PDF to read CV content.
- `hiring_manager` in jobs table is a **user ID string** (e.g. "user-1751134178698-xxx"). Always JOIN to users table to get actual email.
- Most jobs have NULL `min_budget` / `max_budget` — skip budget scoring for these jobs, flag in report as "budget not set".
- If `jobs.jd_text` is NULL, fall back to `jobs.description` for JD content.
- Existing `ai_overall_score = 0.0` rows in applications were from a broken prior implementation — treat as unscreened.
- Filter active jobs with: WHERE job_status = 'Active'
- AI screening results are written to applications table: ai_jd_score, ai_jd_analysis, ai_budget_fit, ai_overall_score, ai_recommendation, ai_screening_summary, ai_screened_at

---

## Email HTML — Critical Rules (learned from Job 32 chart failure)
Gmail strips SVG and CSS flexbox entirely — charts using these simply disappear.
Safe email HTML rules:
- **NO SVG** — stripped by Gmail. Bar charts, pie charts, radar charts all vanish.
- **NO `display:flex`** — stripped. Use `<table>` for all layout instead.
- **NO `position:absolute/relative`** — stripped. No CSS-based bar fill tricks.
- **NO CSS gradients on divs** — unreliable. Use solid `bgcolor` colours instead.
- **Always use inline styles** — `<style>` blocks can be stripped. Use `style="..."` on every element.
- **Use `bgcolor="..."` attribute** in addition to `style="background-color:..."` for max compatibility.

### Email-safe chart replacements:
| Wanted | Use instead |
|---|---|
| Bar chart | Nested `<table>` — coloured `<td>` with explicit `width:%` as the bar fill |
| Pie chart | Stacked single-row `<table>` — coloured `<td>` cells sized by percentage |
| Radar/star chart | Comparison `<table>` — coloured cells with ★ star ratings per dimension |
| Heatmap | Standard `<table>` with inline `bgcolor` per cell — this works fine |

---

## Taleemabad Organisation Context (saved 2026-03-03)
See full detail in context/project-background.md. Key facts for screening:

**What they are:**
- Pakistani EdTech company. K-5 SNC-aligned digital curriculum. Islamabad HQ.
- CEO: Haroon Yasin (Georgetown University Qatar). CPO: Sabeena Abbasi.
- Scale: 170 schools, 1.5M app users, 8.5M students/week via TV+radio.
- Mission: 23M out-of-school children in Pakistan. Impact-driven, NOT commercial-first.
- Funding: $2.3M seed (Sep 2023) — Malala Fund, Sorenson Ventures, Careem CEO, 100x Impact.
- Gov partnerships: MoE + SNC endorsement. Pilot 6 Islamabad public schools → 310 planned.

**Critical screening lenses for ALL Taleemabad roles:**
1. Education system literacy — school/MED/SED experience. Not generic public sector.
2. Government navigation — MoU, government procurement, SED relationships. Not corporate sales.
3. Mission alignment — evidence beyond slogans. Education sector commitment.
4. Lean org mentality — ~50 people. "Built from scratch" evidence required.
5. For fundraising: EdTech/education donor landscape, NOT WASH/humanitarian donors.
6. Pakistan-specific: SNC, NEMIS, district systems. International experience is bonus, not substitute.

**Budget reality:** $2.3M seed for this reach = lean salaries. Flag salary mismatches early.
**Competitor orgs (high-signal in CVs):** TCF, READ Foundation, Teach For Pakistan, Sabaq Foundation, Tele-Taleem, CERP, UNICEF Pakistan, FCDO Pakistan, USAID education programs.

## Competitor Flagging Rule (saved 2026-03-04)
When a candidate has experience at a DIRECT Taleemabad competitor, flag explicitly in report as
"⚡ Competitor Experience — High Strategic Signal" and highlight their profile separately.
Tier 1 direct competitors (always flag): Abwaab, Maqsad, Sabaq Foundation, Knowledge Platform,
The Orenda Project, Tele-Taleem, Edkasa, Nearpeer, DigiSkills, Ilmkidunya.
Full competitor list with context: see context/project-background.md → Competitor Intelligence section.

---

## Common Mistakes to Avoid
- **Do NOT use SVG in HTML emails** — Gmail strips it, charts disappear silently.
- **Do NOT use CSS flexbox in emails** — same problem.
- **Flag unreadable CVs in chat BEFORE sending report** — do not bury them only in the email. Raise in conversation first so user can decide on a fix (e.g. install OCR).

---

## Screening Framework — CURRENT (updated 2026-03-03 v2)
12-step framework. Core: 7-dimension scoring + Organisation Signal + CV Quality. See skills/cv-screening.md.

7 Dimensions (score 0–4): Functional Match 25% · Outcomes 20% · Environment 15% · Ownership 15% · Stakeholder 10% · Hard Skills 10% · Growth 5%
Formula: normalised = (raw/4.0)×100 · penalty: ×0.85 per missing must-have
Decision tiers: 85+ Tier A · 70–84 Tier B · 55–69 Tier C · <55 No-Hire

Organisation Signal (flag but does NOT change score):
- EdTech/Competitor: TCF, READ Foundation, Teach For Pakistan, EdTech startups → High Strategic Signal
- Research/Impact: CERP, World Bank, policy think tanks → High Strategic Signal
- Donor/Dev: UN agencies, FCDO, USAID, GIZ → High Strategic Signal
- Scholarships: Erasmus, Chevening, Fulbright → High Strategic Signal

CV Quality Rating: High / Moderate / Low effort (2-line justification, does not affect score)

Shortlist size rules (UPDATED):
- 20–40 applications → Top 7–10
- 50–100 applications → Top 15–20
- 100–200 applications → Top 25–30
- < 20 applications → All viable candidates

Report sections (7): Summary → JD Scorecard → Ranked Shortlist → Deep Compare Top 3 → Out-of-Budget flags → Visual Analytics (heatmap + bar + star grid) → Why Others Didn't Make It

## User Preferences Learned
- **PDF report section order (CONFIRMED 2026-03-05 final):**
  1. Deep Comparative Analysis — DCA master table (ALL candidates)
  2. Visual Analytics — Charts (bar chart + radar chart, top 10 only)
  3. Strong Match but Out of Budget
  4. Visual Analytics — Heatmap (top 10 only)
  5. Why Others Did Not Make the Cut → Next Steps
  **PDF removed sections (do NOT add back to PDF):** Screening Summary · JD Scorecard · individual profile cards

- **Email HTML report DCA structure (v9 confirmed 2026-03-11):**
  - Part A: Master Ranking Summary table — ALL candidates (#1 to #N), columns: # · Candidate · Score · Tier · Experience · Background · Org Signal · Budget · Key Strength · Key Gap · Verdict
  - Part B: Detailed profile cards for shortlist + extended review (#1–#10) — USP, dimension scores, strengths, risks, org signals, CV quality, interview questions (expandable)
  - Part C: No-hire compact profiles (#11–#N) — grouped by elimination category (Sector-Adjacent / No Impact Ownership / Wrong Sector or Geo / Junior Profile / Unrelated Background), table per group with what was good + why not progressed
  - Charts: placed at TOP of email (before sections) for Gmail 102KB clip protection. CID method only.
  - Reference script: send_job32_report_v9.py
- Charts: top 10 candidates only in both bar chart and heatmap. Confirmed correct.
- Flagging: strong-but-over-budget candidates must be shown separately, never silently excluded.
- Salary: never infer — state "Expected salary not mentioned" if absent.
- USP: each shortlisted candidate must have a Unique Value Proposition statement.
- Competitor candidates: flag explicitly as "⚡ Competitor Experience" in report and highlight separately.

## Workflow — DB Completeness Check (learned 2026-03-05)
Before finalising any report, always query the DB for total application count for the job.
Scripts can miss candidates who applied after the original screening run.
If new candidates found: create a supplemental script (e.g. screen_job32_new_candidates.py),
keyword-score them, assess manually from CV text, fold into main report script as new entries.

## Report Delivery Format — CONFIRMED FINAL (2026-03-05)
All reports are now delivered as **PDF attachment + brief email body**. Never embed the full analysis in the email body.

### Email body (brief only):
- 3 stat boxes: Profiles Screened · Profiles Shortlisted · Strong Matches Over Budget
- One line: "open the attached PDF for full analysis"
- Subject format: `Screening Report- [Position Name]`
- **Greeting: always address the hiring manager by first name** — query `users` table to get name, use "Hi [First Name]," not "Hi Ayesha" generically. When sending to Ayesha only (test), use "Hi Ayesha,".

### PDF (full analysis, landscape A4):
- Generated with `reportlab` + `matplotlib` (already installed)
- **Landscape A4** is mandatory — portrait A4 is too narrow for the master table
- **ALL cells must be `Paragraph` objects** — plain strings NEVER wrap in reportlab tables; they overflow
- 5 sections in PDF: DCA → Visual Analytics (bar+radar) → Out of Budget → Heatmap → Why Others Didn't Make It → Next Steps

### Master table columns (10) — CONFIRMED:
`# · Candidate · Score · Tier · Budget · Exp. Salary · Experience · Current Role · Key Strength/Note · Verdict`
- Column widths (mm): `[6, 24, 11, 13, 20, 22, 14, 44, 93, 20]` = 267mm (landscape usable width)
- Budget column is colour-coded: **In Budget** (green) · **Borderline** (amber) · **Out of Budget** (red)
- Exp. Salary column shows candidate's stated salary or "Not mentioned"
- Score + Tier cells: white bold text on tier colour (green/blue/amber/red)
- Master table has 3 banded groups with coloured separator rows: Shortlisted (green) · Over Budget (pink) · No-Hire (black)

### PDF generation pattern:
- Use `reportlab.platypus`: `SimpleDocTemplate`, `Table`, `TableStyle`, `Paragraph`, `HRFlowable`, `RLImage`
- Charts: matplotlib → `io.BytesIO` PNG → `RLImage(buf, width=..., height=...)`
- `nonlocal row_idx, tbl_rows, tbl_style` needed if modifying these inside nested helper functions
- Reference script: `send_job36_report_pdf.py`

## CV-Stage Rejection Email Rules (confirmed 2026-03-25)

Reference script: `scripts/jobs/job36/send_job36_rejection_live.py`
Pilot one-off: `scripts/jobs/job36/send_job36_misbah_pilot.py`

- **Minimum 500 words** per email
- **"We" voice** throughout — never "I"
- **They/them pronouns** for candidates — never "he/she/his/her" — gender-neutral always
- **Tone:** considerate, warm, open-handed, never harsh or dismissive
- **Not over-diagnostic** — we read a CV, not the whole person. Use reflective language: "we did not yet see enough evidence of…", not "you do not have this skill"
- **Genuine strengths acknowledged** — specific to their actual CV, not generic praise
- **Mismatch explained** with care — focus on the gap between their demonstrated experience and the role demands
- **Closing:** encouraging, open-handed — where their strengths may be better suited, invitation to apply to future roles
- **Simpler subject lines** for CV-stage rejections (not story-driven like values emails): e.g. "Your Application for Field Coordinator, Research & Impact Studies"
- **Sign-off (exact format):** Warm regards, / People and Culture Team / Taleemabad / hiring@taleemabad.com | www.taleemabad.com / Sent on behalf of Talent Acquisition Team by Coco
- **Never mention Coco or AI in the email body**
- **Same HTML design** as values feedback emails (confirmed template)
- **CC:** hiring@taleemabad.com + ayesha.khan@taleemabad.com on every send
- **Always verify CV content** from DB before finalising any role-specific suggestions in closing (do not rely on old AI-generated drafts)

## Values Feedback Email — Confirmed Design & Rules (2026-03-25)

Reference script: `scripts/jobs/job36/send_job36_values_feedback_pilot.py` (v8)

### Writing Rules (all mandatory, apply to every values feedback email)
1. **No interviewer names** — never name who conducted the call. Date is fine.
2. **No personal-vs-professional framing** — assess depth and stakes of the example, not its context.
3. **No em dashes " —"** — replace with period, comma, or colon. Dashes look AI-generated.
4. **No "letter"** — do not refer to the email as a letter in the body. Internal framing only.
5. **Tone: considerate, open-handed, emotionally careful** — no absolute/harsh phrases. Use reflective language ("we found ourselves wondering", not "this disqualifies"). Add emotional cushioning before the gap section. Write WITH the candidate, not AT them.
6. **Subject lines: story-driven** — pull 2-3 evocative threads from the candidate's own conversation. Never label the email generically (not "Values Interview Feedback"). End on neutral/reflective language, never on absence or gap. Examples: "Sehri, Iftari, and what stayed with us" · "The Punjab handover, the honest answer, and where it left us"
7. **Warm bench vs values-failed closing**: values-failed candidates get "door is open if you grow and come back" — NOT a warm bench promise. Warm bench = we proactively reach out.

### Confirmed HTML Design (v8 final)
- Header: white background, blue text (#1565c0), blue bottom border, Taleemabad logo (CID inline)
- Header subtitle line: "PEOPLE & CULTURE · APPLICATION UPDATE" in small caps blue
- Subject line displayed in header as bold blue title
- Role name as smaller subtitle below
- Main headings (H): bold, blue (#1565c0)
- Subheadings (SUB): bold, green (#1b5e20)
- Body: Georgia serif, 15px, line-height 1.8, text-align justify
- P.S. block: light green background (#f1f8e9), green left border
- Footer: "Taleemabad" in blue, hiring@taleemabad.com, www.taleemabad.com
- Full pre-send checklist: memory/feedback_email_rules.md

### Job 36 Values Feedback Status (2026-03-25)
- Muhammad Omer Khan: values FAIL (All for One: -, Practice Joy: -) · feedback email SENT 2026-03-25
- Faryal Afridi: values FAIL (4x +/-, 0 minus but exceeds max +/- threshold) · feedback email SENT 2026-03-25
- Reference script: scripts/jobs/job36/send_job36_values_feedback_pilot.py (final v8)

## Job Status Log
- **Job 17** (CPD Coach): Zero In invites sent 2026-03-25 to 6 female TFP Fellows (Islamabad + Gilgit).
  Hiring manager: Hasnat Tariq (Hasnat@niete.edu.pk). CC: hiring@taleemabad.com + Hasnat only (no jawwad/ayesha).
  Subject format: "Zero In Call for CPD Coach - [Candidate Name]" (user confirmed — differs from standard invite subject).
  Candidates: Syeda Siddiqa Fatima · Fatima Saeed · Zara Bhayo · Irum Afzal · Hajra Sajjad · Shazia Sahat.
  Filter: female name inference + TFP keyword scan across Base64 PDFs (all structured fields NULL for Job 17).
  Scripts: scripts/jobs/job17/send_job17_values_invite.py · screen_job17_tfp_filter.py
- **Job 32** (Fundraising & Partnerships Manager): PDF report sent 2026-03-05 to sabeena.abbasi@taleemabad.com (hiring manager), CC hiring@taleemabad.com.
  64 total applications · 48 assessed · 10 shortlisted · 3 out of budget. Scripts: send_job32_report_pdf.py · send_job32_report_v9.py
  v9 email HTML report also sent 2026-03-11 to ayesha.khan@taleemabad.com — DCA format (Part A + B + C), charts embedded at top via CID.
- **Job 36** (Field Coordinator, Research & Impact Studies): PDF report sent 2026-03-05 to muzzammil.patel@taleemabad.com, CC hiring@taleemabad.com.
  172 screened · 15 shortlisted · 5 over-budget flagged. Scripts: send_job36_report_pdf.py
  **Candidate emails SENT 2026-03-25:**
  - Values feedback: Omer Khan + Faryal Afridi (FAIL) — scripts/jobs/job36/send_job36_values_feedback_pilot.py
  - CV-stage rejections: 146 candidates sent, 15 skipped (10 no-CV + 5 duplicates) — scripts/jobs/job36/send_job36_rejection_live.py
  - Send log: output/job36_rejection_send_log.json
  - 10 flagged candidates (no CV / unreadable) — PENDING, decision deferred
- **Job 35** (Junior Research Associate – Impact & Policy): PDF report sent 2026-03-05 to muzzammil.patel@taleemabad.com, CC hiring@taleemabad.com.
  291 screened (keyword-scored from scratch) · 30 shortlisted (all Tier A) · 0 over-budget (no salaries stated).
  Budget: PKR 150K–200K. Scripts: screen_job35_fetch.py · enrich_job35_top30.py · send_job35_report_pdf.py

## DB Constraints — CRITICAL (learned Job 35)
- `applications.ai_recommendation` only accepts `'shortlist'` or `'discard'` — NOT tier names
- `applications.ai_overall_score` and `applications.ai_jd_score` are **0–10 scale** (not 0–100)
  → Always divide 0–100 score by 10 before writing to DB
- `applications.ai_jd_analysis` (text) — safe to store tier label (e.g. "Tier A") here

## Large-Pool Screening Pattern (291 candidates — confirmed working)
Three-script approach for unscreened jobs:
1. `screen_job##_fetch.py` — fetch CVs, parse PDFs (PyPDF2 + OCR fallback), keyword-score all candidates, write to DB
2. `enrich_job##_top30.py` — fetch top N candidates, re-parse CVs to extract university, degree, current role, orgs
3. `send_job##_report_pdf.py` — build PDF report with hardcoded enriched data, send email
Keyword scoring covers: tools (Stata/R/Python > SPSS > Excel), methods (regression, RCT, ToC etc.),
RA work, thesis, org signals (CERP, J-PAL, World Bank, IFPRI, PIDE etc.), university prestige, degree field.

## Email Greeting Rule (confirmed 2026-03-05)
Always address the hiring manager by first name: "Hi [First Name],"
Query `users` table (first_name, last_name) joined to jobs.hiring_manager to get name.
Never use generic "Hi Ayesha," when sending to a different hiring manager.

## Gmail 102KB Clip Rule — CRITICAL
Gmail silently clips HTML emails over ~102KB. Everything after the clip is hidden behind "Message clipped [View entire message]".
- Charts MUST be placed at the very top of the email HTML (before any section headers) so they stay within the first ~5KB
- If charts are in Section 5/6 of a long email, they will NEVER be visible — the email body is too large
- This applies to all HTML email reports — keep charts at top regardless of desired section order

## Chart Implementation Pattern (v8 confirmed working — CID method)
Gmail blocks data:image/... base64 URIs — images simply don't appear.
CORRECT approach: matplotlib PNG → attach as MIMEImage with Content-ID → reference via cid: in HTML.

Email structure:
  msg = MIMEMultipart("related")       ← outer container MUST be "related"
  alt = MIMEMultipart("alternative")   ← HTML body goes inside alt
  msg.attach(alt)
  alt.attach(MIMEText(html, "html"))
  img = MIMEImage(png_bytes, 'png')
  img.add_header('Content-ID', '<chart_name>')
  img.add_header('Content-Disposition', 'inline', filename='chart.png')
  msg.attach(img)

HTML reference: <img src="cid:chart_name" ...>   (no angle brackets in src)
Chart functions: return raw bytes (buf.getvalue()), NOT base64 string.

---

## Tool & Environment Notes
- Python 3.14.3 installed on Windows 11
- Node.js v24.14.0 installed
- Neon DB accessible directly via MCP tool in Claude Code sessions
- Email: Gmail (SMTP) — sender address TBD, will use App Password method
- Install Python packages before first run: cd "c:/My First Agent" && pip install -r requirements.txt

## Environments — CRITICAL
Two separate Neon PostgreSQL databases exist:
- **Markaz** = PRODUCTION. Real job postings, real candidates, real applications. Use this for ALL screening.
  - Host: ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech | Password: npg_kBQ10OASHEmd
- **Replit** = DEV/TEST. Where Taleemabad builds and tests before deploying to Markaz. Contains dummy data only. Do NOT use for screening.
  - Host: ep-ancient-band-ady57xpe.c-2.us-east-1.aws.neon.tech | Password: npg_rw9lYPcevjt7

---

## How to Add an Entry
After completing a task, tell the agent:
> "Save this to memory.md: [what you learned]"

Or ask:
> "What did we learn today? Update memory.md."
