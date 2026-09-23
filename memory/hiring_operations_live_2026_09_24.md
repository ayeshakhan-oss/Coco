---
name: Hiring Operations live on Railway (2026-09-24)
description: "Attendance, Decision Briefs and the Hiring Decision Brief built and deployed. All three SOPs depended on a data source that no longer exists (Teams Presence channel, Google Calendar) and all three were solvable from Markaz and the mailbox. Records the 4 corrupt leave records, the one rule the three components share, and what is still not written down anywhere."
type: project
---

# Hiring Operations: three components live (2026-09-24)

Live at `https://coco-production-bcc8.up.railway.app`, commit `119bf49`.
603 tests, 25 SQL statements validated against the real schema, zero "soon"
pills left in the module.

| Component | Route | Source |
|---|---|---|
| Attendance | `/attendance` | Markaz `employee_profiles` + `leave_requests` |
| Decision Briefs | `/decision-brief` | Markaz + `coco.cv_screens` + `coco.case_study_evaluations` |
| Hiring Decision Brief | `/hiring-brief` | the above + `coco.comm_evidence` |

**Out of scope by Ayesha's decision:** the weekly Pipeline Monitor ("a skill
which is not completely developed, so lets not move it") and the Meeting Notes
Tracker, which stays in Claude Code so her personal Google token never sits on
a server.

**All three are read-only.** She chose "draft and show me, I press send", and a
single send path for all three is better than three; there is a test asserting
Operations exposes no write method at all.

---

## 🔴 Every SOP pointed at a data source that no longer exists

Two of three, and both were solvable without the thing they asked for.

**The Teams Presence channel is dead.** `attendance-reports.md` scrapes
presence announcements out of Mission Comms. Its last message is **2026-04-24**
and the whole team has been silent since **2026-06-21**. Absence moved into
Markaz, where `work_from_home` is a leave type with 360 records and
`leave_requests` is current to today. Reading Markaz is simpler AND correct.

**Google Calendar is dead** (OAuth client deleted, cannot refresh), and the
hiring-decision-brief SOP reads it for every booking count. It turns out not to
matter: **the booking system emails a confirmation** and those are already in
the synced mailbox evidence:

    "Appointment booked: Zero In Call For Senior Growth Manager (Name) @ ..."
    "Appointment booked: Case Study Debrief - Senior Manager Growth (Name) @ ..."
    "Lets proceed with the Case Study for Senior Manager Growth - Name"

🔑 **Check whether a dead dependency is actually needed before working around
it.** Both of these looked like blockers and neither was.

---

## 🔴 The one rule all three share: no record is not no event

This came up three separate times in one build, and each time the naive
version would have produced a confident, wrong claim.

| Component | The lie it would have told | What it says instead |
|---|---|---|
| Attendance | "129 onsite" | "129 with **no absence recorded**" |
| Decision Brief | "OVERDUE" on all 185 | "**NO DEBRIEF RECORDED**" |
| Hiring funnel | "0 case studies sent" | "**not visible**" |

A leave system cannot see who walked into the office. An empty debrief field is
a statement about our records, not a delay on the candidate's part. A stage
with no matching email means we did not recognise one, not that none was sent.
Each of the three has a test asserting the forbidden word never appears.

---

## 🔴 Four leave records in Markaz cannot be true

    Bushra        annual          start year 0026
    Bushra        work_from_home  end date 42026-02-01
    Fatima Khan   work_from_home  start year 2016
    Moiz Khan     annual          end date 20226-01-02

A plain `CURRENT_DATE BETWEEN start_date AND end_date` marks these people
absent **for ever**. On 2026-09-23 that reported 10 absences where the true
number was 8: a **20% error, silently, every single day**.

⚠️ **A SQL check on `EXTRACT(YEAR ...)` finds only the two Postgres can still
parse. Checking the date STRING finds all four.** They are excluded from the
counts and listed on the page with the **exact untruncated value**, because
somebody has to correct them in Markaz or tomorrow's report is wrong too. The
valid rows ARE truncated to 10 characters, so showing "42026-02-0" would send
someone looking for the wrong record.

---

## What the briefs can and cannot say

Measured on Job 42 (Senior Manager Growth, 185 applicants):

    values_interview_result   18        case_study_score     0
    values_scorecard          23        gwc_interview_result 0
    case_study_status         17        gwc_interview_date   0

**Case-study scores and debrief verdicts are not written down anywhere
machine-readable.** They live in Ayesha's head, her mailbox and the reports she
has sent. So the brief counts what is missing and prints it (185 debrief
verdicts, 17 case-study scores, 18 CVs absent) rather than leaving blanks a
reader would read as findings.

**The Leading section refuses to imply a ranking it cannot make.** All 17
leading candidates on Job 42 have no case-study score and no CV screen, so the
list is a set, not an order, and it says so and names the fix: scoring the case
studies sharpens it.

**Two sources for the values verdict and they can disagree.** The scorecard's
`proceedToRightSeat` wins over the `values_interview_result` column, because it
is what the interviewer filled in, and a disagreement is shown on the row.
"No values interview" is None and "interviewed, did not pass" is False;
collapsing them puts people in the wrong pipeline group.

**Gmail counts are a FLOOR.** `comm_evidence` holds one row per application by
construction and keeps only the most recent message, so somebody invited,
booked and later rejected shows only the rejection. Job 42 reads 3 values
bookings against 23 interviews actually held. The page prints "≥3" with its
source, never a number that looks exact, and says the evidence was last synced
2026-09-02.

---

## Two things worth reusing

- **Every candidate name links to their CV**, which the decision-brief SOP calls
  non-negotiable, via a new `GET /api/candidates/{id}/cv` that streams it out of
  Markaz behind the same Google sign-in. No manual Drive upload stands in the
  way any more. It sniffs the real file signature rather than trusting
  `resume_mime_type` (a .docx labelled application/pdf is common) and sends
  `Cache-Control: private, no-store`, because a CV is personal data.
- **The funnel checks itself.** Any stage whose exact count is higher than the
  one before it is reported on the page, because a funnel that widens means one
  of the two numbers is wrong. Gmail floors are excluded, since a floor
  exceeding an exact count says nothing.

## Still outstanding

1. **Nothing sends yet.** One send path for all three is the next piece.
2. **The four leave records** need correcting in Markaz by a person.
3. The payroll baseline in the SOP still says 84; it is 131 and the code reads
   it live per entity.

See [candidate_evaluation_all_six_subskills_2026_09_23.md](candidate_evaluation_all_six_subskills_2026_09_23.md)
for the same lessons on the evaluation side.
