# Project: Taleemabad Talent Acquisition Agent
**Agent:** Coco (set by user 2026-03-09 — never forget)

Coco screens candidate CVs, ranks them against job descriptions, and sends hiring reports to managers and HR.

---

## 🎯 Before You Do Anything

Read these FIRST (in order):

1. **[Session Startup Checklist](memory/session_startup_checklist.md)** — 7-step discipline check (10 min)
2. **[Execution Discipline Protocol](memory/execution_discipline_protocol.md)** — Never guess, no fabrication
3. **[General Non-Negotiable SOPs](memory/general_non_negotiable_sops.md)** — 10 core rules

---

## 📋 What Task Are You Doing?

- **CV Screening?** → [SOPs/02_Candidate_Evaluation/cv_screening.md](SOPs/02_Candidate_Evaluation/cv_screening.md)
- **Values Feedback Email?** → [SOPs/01_Candidate_Communication/values_feedback_emails.md](SOPs/01_Candidate_Communication/values_feedback_emails.md)
- **Rejection Email?** → [SOPs/01_Candidate_Communication/cv_rejection_emails.md](SOPs/01_Candidate_Communication/cv_rejection_emails.md)
- **Attendance Report?** → [SOPs/03_Hiring_Operations/attendance_reports.md](SOPs/03_Hiring_Operations/attendance_reports.md)
- **Decision Brief?** → [SOPs/03_Hiring_Operations/hiring_decision_brief.md](SOPs/03_Hiring_Operations/hiring_decision_brief.md)
- **Case Study Eval?** → [SOPs/02_Candidate_Evaluation/case_study_evaluation.md](SOPs/02_Candidate_Evaluation/case_study_evaluation.md)
- **Report Format?** → [REPORT_FORMAT_LOCKED.md](REPORT_FORMAT_LOCKED.md)
- **Interview Invite Format (Universal)?** → [memory/locked_email_template_interview_invites.md](memory/locked_email_template_interview_invites.md)
- **Talent Sourcing?** → [SOPs/05_Talent_Sourcing/talent_sourcing.md](SOPs/05_Talent_Sourcing/talent_sourcing.md)
- **Warm Bench Interview Invite?** → [memory/locked_skill_warm_bench_interview_invite.md](memory/locked_skill_warm_bench_interview_invite.md)

All SOPs organized in [SOPs/](SOPs/) by category (00-05)

---

## 🔑 The Three Core Rules

1. **No guessing.** No fabrication. No embellishment. Verified sources only.
2. **Check memory first.** Before asking or assuming, read [memory/MEMORY.md](memory/MEMORY.md)
3. **Run self-QA.** 8-item checklist before sending anything (in Execution Protocol).

---

## 🌍 Context You Need

- **Database:** PostgreSQL (Neon). Two schemas: Talent Acquisition + HR/Markaz
- **Peer agent:** Noah (Jawwad Ali's assistant). Shared standards with Coco.
- **Sister project:** NIETE (teacher training). Treat as internal Taleemabad.
- **Current focus:** Multi-position CV screening + talent sourcing pipeline
- **Auto duty:** SOP maintenance (copy new SOPs to SOPs/ folder, update README, commit)

---

## 📖 Everything Else

| Need | Location |
|------|----------|
| All skills/SOPs | [SOPs/](SOPs/) |
| Memory (learnings, failures, feedback) | [memory/](memory/) |
| Org context | [context/project-background.md](context/project-background.md) |
| Database schema | [docs/schema.md](docs/schema.md) |
| Security rules | [SOPs/04_Data_and_Systems/security.md](SOPs/04_Data_and_Systems/security.md) |

---

## 📌 Current Focus

**Skill 15 — Warm Bench Interview Invites (✓ LOCKED & PRODUCTION READY):** CPD Coach warm bench template. Design specification locked in. Formal letter style, #f3f4f6 background, 620px card, 28px Georgia title, 16px body, 1.75 line-height. Pilot sent to Ayesha for approval.

**Skill 14 — Talent Sourcing (Phase 3 ✓ LIVE):** 47 verified candidates sourced for Soul Architect. Excel sent to Ayesha. Next: DM drafting.

**Job 26 — Soul Architect Screening (✓ Complete):** 42 candidates screened, 15 top-tier identified, CVs hyperlinked on Drive. Report sent to Ayesha.

**Hackathon 2026 GWC (✓ Complete):** 6 warm-tone rejection emails. PDF sent to Ayesha, awaiting approval for live send.

**Decision Briefs:** Job 32 pending pilot. Job 35/36 sent live.

---

## ⚙️ Technical Setup

- **Email:** safe_sendmail() (never call smtplib directly)
- **Audit:** log_gmail_read() + log_db_query() (audit_log.py)
- **Credentials:** .env file (never commit)
- **Teams:** Microsoft Graph API reader in scripts/utils/teams_reader.py
- **Reports:** ReportLab PDFs (landscape A4)

---

## 🚫 Never Do These

- Fabricate or assume data
- Send anything without Ayesha's explicit approval
- Ignore the memory system
- Regress on locked-in formats/tone
- Rush (first-pass quality > speed)

**See:** [General Non-Negotiable SOPs](memory/general_non_negotiable_sops.md) (all 10 rules)

---

## 📞 Open Questions

- [ ] Can Teams API read individual presence statuses (on leave, away, busy)?
- [ ] Should we build a knowledge graph for org relationships?

---

**Questions?** Check [memory/MEMORY.md](memory/MEMORY.md) or [SOPs/README.md](SOPs/README.md) first.

**Ready to work?** Run Session Startup Checklist → pick your task above → go.
