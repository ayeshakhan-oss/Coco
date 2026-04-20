# Coco Team Onboarding Checklist

**Project:** Taleemabad Talent Acquisition Agent  
**Agent:** Coco (AI assistant for CV screening, candidate evaluation, and hiring reports)  
**Duration:** 4 weeks (progressive ramp-up)  
**Owner:** Ayesha Khan (Talent Acquisition Lead)

---

## WEEK 1: Foundation & Orientation

### Monday: Project Context (2 hours)

**Goal:** Understand Taleemabad's mission, hiring context, and what Coco does.

- [ ] **Read CLAUDE.md** (10 min) — Project overview, current focus, key rules
- [ ] **Read context/project-background.md** (20 min) — Organization structure, hiring criteria, competitor intelligence
- [ ] **Read SESSIONS.md** (15 min) — Session history, what's been done, current status (skim Section 1-3)
- [ ] **Watch/Demo:** Ask to observe Ayesha doing a live hiring decision or screening task (15 min)
- [ ] **Q&A Session** (10 min) — Ask: "What's the biggest pain point in your hiring process right now?"

**Output:** Understand Taleemabad's mission, Coco's role, and hiring team's day-to-day challenges.

---

### Tuesday: Core Discipline & Memory System (2 hours)

**Goal:** Learn the discipline framework that ensures Coco produces reliable work.

- [ ] **Read memory/session_startup_checklist.md** (15 min) — 7-step startup ritual
- [ ] **Read memory/execution_discipline_protocol.md** (20 min) — No guessing, verified sources, self-QA checklist
- [ ] **Read memory/general_non_negotiable_sops.md** (15 min) — 10 foundation rules
- [ ] **Read memory/MEMORY.md** (5 min) — What this memory system tracks
- [ ] **Explore memory/ folder** (10 min) — Browse 11 memory files, get sense of what's documented
- [ ] **Ask:** Where would you go if you noticed Coco making the same mistake twice?

**Output:** Understand why discipline matters, how memory prevents regressions, what "locked" means.

---

### Wednesday: Skills & SOPs Navigation (2 hours)

**Goal:** Learn where to find how Coco does each job (CV screening, rejections, reports, etc.).

- [ ] **Read skills.md** (10 min) — Master index of all skills
- [ ] **Read SOPs/README.md** (10 min) — How SOPs are organized (5 categories)
- [ ] **Explore 3 key SOPs:**
  - [ ] [SOPs/02_Candidate_Evaluation/cv_screening.md](../SOPs/02_Candidate_Evaluation/cv_screening.md) (15 min) — How Coco screens CVs
  - [ ] [SOPs/01_Candidate_Communication/cv_rejection_emails.md](../SOPs/01_Candidate_Communication/cv_rejection_emails.md) (10 min) — How Coco writes rejection feedback
  - [ ] [SOPs/03_Hiring_Operations/hiring_decision_brief.md](../SOPs/03_Hiring_Operations/hiring_decision_brief.md) (10 min) — How Coco summarizes hiring decisions
- [ ] **Ask:** Which skill would you most want to see Coco improve?

**Output:** Fluent navigation of SOPs folder. Know that CV Screening is the entry point.

---

### Thursday: Database & Data Sources (2 hours)

**Goal:** Learn what data Coco has access to and how to verify it.

- [ ] **Read docs/schema.md** (20 min) — Neon PostgreSQL schema (candidates, applications, jobs, users)
- [ ] **Read [SOPs/04_Data_and_Systems/database_queries.md](../SOPs/04_Data_and_Systems/database_queries.md)** (15 min) — 6 common query types
- [ ] **Access Neon Database** (demo with Ayesha):
  - [ ] Connect to Neon via credentials in .env
  - [ ] Run: `SELECT COUNT(*) FROM candidates;` (verify you can query)
  - [ ] Run: `SELECT * FROM jobs WHERE status='Active';` (see open positions)
  - [ ] Run: `SELECT * FROM applications LIMIT 5;` (see application data)
- [ ] **Check tools available:**
  - [ ] Can you read a candidate's resume_data (Base64 PDF)?
  - [ ] Can you access job descriptions from jobs.jd_text?
  - [ ] Can you check application statuses and scores?
- [ ] **Ask:** What data quality issues do you notice? What's missing or wrong?

**Output:** Comfortable with Neon database. Know what candidate/job/application data looks like.

---

### Friday: First Live Observation (3 hours)

**Goal:** Sit with Ayesha and watch Coco work on a real task.

- [ ] **Observe a live CV screening** (if available):
  - [ ] Watch as Coco reads CVs, scores candidates, generates report
  - [ ] Ask: "Why did you score them that way?"
  - [ ] Notice: Format, tone, hyperlinks, stat boxes
- [ ] **OR: Observe a feedback email generation** (if no CVs ready):
  - [ ] Watch as Coco reads interview transcript, writes rejection/feedback
  - [ ] Notice: Word count, tone ("we" voice), specific evidence, feedback widget
- [ ] **Review one completed report together** (past work):
  - [ ] Job 26 screening report
  - [ ] Notice: Structure, stat boxes, candidate profiles, hyperlinks
  - [ ] Ask: "What changed from first draft to final?"
- [ ] **Debrief:** "What surprised you about how Coco works?"

**Output:** Real-world sense of Coco's process, quality level, and output format.

---

## WEEK 2: Core Skills Deep-Dive

### Monday: CV Screening Mastery (3 hours)

**Goal:** Learn Coco's 8-step CV screening process inside-out.

- [ ] **Study [SOPs/02_Candidate_Evaluation/cv_screening.md](../SOPs/02_Candidate_Evaluation/cv_screening.md)** (30 min, slow read):
  - [ ] Understand 8-step process
  - [ ] Understand multi-criterion evaluation framework (skills, experience, etc.)
  - [ ] Understand format locking (Google Drive hyperlinks, stat boxes, design)
- [ ] **Review Job 26 screening** — reference implementation:
  - [ ] Read: [scripts/jobs/job26/send_job26_screening_report_final.py](../scripts/jobs/job26/send_job26_screening_report_final.py)
  - [ ] See: `soul_architect_screening_pilot_2026-04-20_FINAL.html` (the output)
  - [ ] Notice: Hyperlinks, candidate descriptions, budget flags, "Maybe" table
- [ ] **Run through screening checklist** — from SOP:
  - [ ] 8-item pre-send checklist
  - [ ] Format lock verification
  - [ ] 45-item detailed QA checklist
- [ ] **Ask:** If we got 50 CVs for a new role, could you prepare a draft screening report?

**Output:** Understand CV screening workflow, format, QA expectations. Ready to draft your first screening.

---

### Tuesday: Candidate Communication (Rejections) (2 hours)

**Goal:** Learn Coco's approach to warm, evidence-based candidate rejections.

- [ ] **Study [SOPs/01_Candidate_Communication/cv_rejection_emails.md](../SOPs/01_Candidate_Communication/cv_rejection_emails.md)** (20 min):
  - [ ] Understand 3-section structure: What We Liked / Where We Found Questions / What Next
  - [ ] Understand v8 design (blue headings, Georgia serif, justified text)
  - [ ] Understand tone: warm, reflective, NOT diagnostic
- [ ] **Study [SOPs/01_Candidate_Communication/values_feedback_emails.md](../SOPs/01_Candidate_Communication/values_feedback_emails.md)** (20 min):
  - [ ] Same structure + design, but based on values interview transcript
  - [ ] 800-1100 words mandatory
  - [ ] Why: candidate interviewed with us, we owe them detailed feedback
- [ ] **Study [SOPs/01_Candidate_Communication/warm_bench_feedback_email.md](../SOPs/01_Candidate_Communication/warm_bench_feedback_email.md)** (15 min):
  - [ ] For candidates who PASSED values but not selected for THIS role
  - [ ] Tone: affectionate, storytelling, signal future opportunity
  - [ ] Why: keep them engaged, signal warm bench status
- [ ] **Compare the three approaches:**
  - [ ] CV rejection: 800+w, specific CV evidence, reflective
  - [ ] Values rejection: 800-1100w, interview transcript evidence, reflective
  - [ ] Warm bench: 800-1000w, values + GWC evidence, storytelling + future signal
- [ ] **Ask:** If a candidate failed values on "Courageous Conversations", how would you structure the feedback?

**Output:** Understand why personalized rejection matters. Know the three rejection types and when to use each.

---

### Wednesday: Case Study & Values Evaluation (2 hours)

**Goal:** Learn how Coco evaluates case studies and values interviews.

- [ ] **Study [SOPs/02_Candidate_Evaluation/case_study_evaluation.md](../SOPs/02_Candidate_Evaluation/case_study_evaluation.md)** (20 min):
  - [ ] 8-step evaluation process
  - [ ] Check Markaz AND Gmail (never one source alone)
  - [ ] Auto-flag incomplete submissions
  - [ ] Weekly proactive reporting (don't wait to be asked)
- [ ] **Study [SOPs/02_Candidate_Evaluation/values_scorecard_scoring.md](../SOPs/02_Candidate_Evaluation/values_scorecard_scoring.md)** (20 min):
  - [ ] 7-step SOP with key rule: ASK AYESHA BEFORE SUBMITTING
  - [ ] 6 values (Don't Walk Away, All for One, etc.)
  - [ ] PASS/OUT logic (zero minuses AND ≤2 +/-, or OUT)
  - [ ] Why: Markaz schema must be exact or data invisible on UI
- [ ] **Study [SOPs/02_Candidate_Evaluation/kcd_evaluation.md](../SOPs/02_Candidate_Evaluation/kcd_evaluation.md)** (15 min):
  - [ ] Full case study evaluation pipeline (longer skill)
  - [ ] 4 mandatory additions (incomplete section, GWC conversation guide, conditional verdicts, per-exercise evidence)
  - [ ] When to use: multi-round hiring with case studies
- [ ] **Ask:** What's the difference between an incomplete submission that's fixable vs. one that should be rejected?

**Output:** Understand case study / values evaluation workflows. Know why "ask before submitting" matters.

---

### Thursday: Hiring Operations (Briefs & Reports) (2 hours)

**Goal:** Learn how Coco creates decision briefs and attendance reports.

- [ ] **Study [SOPs/03_Hiring_Operations/hiring_decision_brief.md](../SOPs/03_Hiring_Operations/hiring_decision_brief.md)** (20 min):
  - [ ] 10-step SOP
  - [ ] Check 3 sources: Markaz + Gmail + Calendar (never one alone)
  - [ ] 10 stat boxes showing pipeline flow
  - [ ] CV hyperlink completeness requirement (audit all sections)
  - [ ] Why: hiring manager needs 1-click access to all candidate CVs
- [ ] **Study [SOPs/03_Hiring_Operations/attendance_reports.md](../SOPs/03_Hiring_Operations/attendance_reports.md)** (15 min):
  - [ ] 6-step workflow (payroll list, Markaz, Teams, cross-check, flag silent)
  - [ ] 7 sections + 8 stat boxes
  - [ ] Total must = 84 (static OPL+OWT payroll)
  - [ ] Flag silent cases (people absent/remote without notification)
- [ ] **See real examples:**
  - [ ] Review a past decision brief (ask Ayesha)
  - [ ] Review past attendance report (ask Ayesha)
  - [ ] Notice: Exact format, stat box colors, table structure
- [ ] **Ask:** If a candidate wasn't invited to values but appeared in Markaz as "values_passed", how would you flag this?

**Output:** Understand decision brief & attendance report workflows. Know 3-source verification rule.

---

### Friday: Talent Sourcing (Proactive) (2 hours)

**Goal:** Learn Coco's approach to finding passive candidates.

- [ ] **Study [SOPs/05_Talent_Sourcing/talent_sourcing.md](../SOPs/05_Talent_Sourcing/talent_sourcing.md)** (30 min):
  - [ ] 7-step SOP (Intake → Platform Selection → 3-Layer Searches → Extract → Present → Draft DMs → Add to Markaz)
  - [ ] 3-layer search strategy (Org pages → Google → LinkedIn via Google)
  - [ ] Why: LinkedIn API fails, Google site: queries work reliably
  - [ ] CRITICAL: Never add to Markaz before confirmed interest (core rule)
  - [ ] CRITICAL: Ayesha sends DMs manually, Coco drafts only
- [ ] **Review Phase 3 end-to-end test:**
  - [ ] [memory/project_soul_architect_sourcing_final.md](../memory/project_soul_architect_sourcing_final.md)
  - [ ] 47 verified candidates sourced in 1 day
  - [ ] Methodology: 100+ Google searches, all links verified
  - [ ] Output: Excel sheet with tiers + DM templates
- [ ] **Understand infrastructure:**
  - [ ] Audit logging: `log_sourcing_action()` in scripts/utils/audit_log.py
  - [ ] Database insertion: `scripts/sourcing/insert_sourced_candidate.py`
  - [ ] Main runner: `scripts/sourcing/source_candidates.py`
- [ ] **Ask:** If you wanted to source 30 Product Managers, how would you start?

**Output:** Understand sourcing workflow. Know 3-layer search strategy. Understand infrastructure.

---

## WEEK 3: Advanced Topics & Edge Cases

### Monday: Data Quality & Verification (2 hours)

**Goal:** Learn how Coco handles data gaps, inconsistencies, and when to ask for clarification.

- [ ] **Read memory/general_non_negotiable_sops.md** — Rule #1: No Fabrication
  - [ ] Understand: "Not mentioned" is better than guessing
  - [ ] Understand: Verify before asserting
  - [ ] Understand: Ask instead of assume
- [ ] **Case Study: Job 26 Re-Assessment** (memory/coco_delegation_discipline.md):
  - [ ] Context: Candidates looked perfect on paper but lacked depth
  - [ ] Learning: Checkbox matching ≠ genuine expertise
  - [ ] Action: Re-screen for DEPTH, not surface-level fit
- [ ] **Case Study: Teams API Incompleteness** (memory/discipline_failure_teams_api_incomplete.md):
  - [ ] Context: Teams API returned only 1 message instead of ≥3
  - [ ] Error: Assumed "no data" instead of flagging suspiciously small result
  - [ ] Fix: Verify with ground truth before reporting absence
- [ ] **Practice: Draft 3 scenarios:**
  - [ ] Candidate's CV is incomplete (missing dates, titles). What do you do?
  - [ ] Database shows "salary: NULL". What do you do?
  - [ ] Teams API returns 0 messages. What do you do?
- [ ] **Ask:** What's the difference between "data is missing" and "I didn't look hard enough"?

**Output:** Understand data verification discipline. Know when to flag vs. fill gaps.

---

### Tuesday: Format Locking & Quality Assurance (2 hours)

**Goal:** Learn Coco's format standards and the discipline required to maintain them.

- [ ] **Read REPORT_FORMAT_LOCKED.md** (20 min):
  - [ ] Why: Once format corrected, it applies to ALL future reports (no regression)
  - [ ] What: Exact HTML structure, colors, fonts, spacing (no variations)
  - [ ] Why: Gmail-safe (tables, not divs), no character encoding issues
- [ ] **Study 8-item self-QA checklist** (from execution_discipline_protocol.md):
  - [ ] File names/existence (correct? exist?)
  - [ ] Formatting (matches locked format exactly?)
  - [ ] Tone (matches project voice?)
  - [ ] Duplication (accidental copy-paste?)
  - [ ] Jargon removal (clear to non-expert?)
  - [ ] Encoding/artifacts (special chars correct? no garbled text?)
  - [ ] Consistency (matches other reports in batch?)
  - [ ] Factual grounding (everything verified, nothing guessed?)
- [ ] **Review a past report iteration:**
  - [ ] See: Initial draft → User feedback → Revised → Locked
  - [ ] Notice: What changed each time?
  - [ ] Notice: Why did it take multiple iterations?
- [ ] **Practice: Take a sample report and QA it:**
  - [ ] Read through self-QA checklist
  - [ ] Identify 3 things that could break it
  - [ ] What would you flag before sending?
- [ ] **Ask:** If format was locked today, what would you do differently tomorrow?

**Output:** Understand format locking discipline. Know self-QA checklist. No regressions.

---

### Wednesday: Memory System & Pattern Recognition (1.5 hours)

**Goal:** Learn why memory matters and how it prevents duplicate work.

- [ ] **Review 3 memory failures** (from coco_core_problems_identified.md):
  - [ ] Memory skip — not checking MEMORY.md first
  - [ ] Pattern non-recognition — treating repeat task as new work
  - [ ] Regression — same format error multiple times in same session
- [ ] **Understand memory hierarchy:**
  - [ ] CLAUDE.md (router) → memory/MEMORY.md (index) → memory/[topic].md (details)
  - [ ] Each memory file has: name, description, type (user/feedback/project/reference)
  - [ ] MEMORY.md is a 200-line index, not 5000-line monster
- [ ] **Practice: Scenario Testing**
  - [ ] "I need to write a rejection email. Where do I start?" (Answer: CLAUDE.md → task router → SOPs/01_Candidate_Communication/cv_rejection_emails.md)
  - [ ] "I see Coco making a typo I corrected last week. What happened?" (Answer: Check CLAUDE.md and memory for the rule, it should be enforced everywhere)
  - [ ] "I want to understand why we don't use LinkedIn API." (Answer: Check memory/discipline_failure_teams_api_incomplete.md or context)
- [ ] **Ask:** What's the difference between "Coco learned" and "format locked"?

**Output:** Understand memory system structure. Know memory prevents regressions.

---

### Thursday: Execution Discipline Protocol (2 hours)

**Goal:** Internalize the discipline framework that makes Coco reliable.

- [ ] **Deep read: memory/execution_discipline_protocol.md** (30 min):
  - [ ] BEFORE starting: Search for existing SOP/template (reuse, don't reinvent)
  - [ ] WHEN working: Use verified sources only (Markaz DB, Gmail, user data)
  - [ ] FORMAT locked: Once corrected, maintain exactly (no regression)
  - [ ] SELF-QA mandatory: All 8 items before sending (failsafe)
  - [ ] Failsafe behavior: STOP and ask instead of guessing
- [ ] **Deep read: memory/session_startup_checklist.md** (20 min):
  - [ ] 7-step ritual before any task:
    1. Memory load (read MEMORY.md + relevant files)
    2. Protocol confirmation (understand scope + SOPs)
    3. Execution discipline check (confirm it's active)
    4. Task type ID (recurring vs. new)
    5. Verify source material (data access available)
    6. Search prior work (find existing template/SOP)
    7. Lock-in check (verify format corrections locked)
- [ ] **Understand recurring vs. one-time:**
  - [ ] Recurring work (rejections, reports, scorecards): Full discipline protocol
  - [ ] One-time work (exploration, research): Lighter discipline, focus on verified sources
- [ ] **Ask:** Why is discipline more important than speed?

**Output:** Understand discipline framework. Know startup checklist. Know failsafe behavior.

---

### Friday: Live Shadowing + Q&A (3 hours)

**Goal:** Sit with Ayesha, watch Coco work, and ask clarifying questions.

- [ ] **Observe a full work session** (pick one):
  - [ ] CV screening (intake through sending report)
  - [ ] Rejection email generation (intake through approval)
  - [ ] Case study evaluation (check Markaz + Gmail, assess, flag)
  - [ ] Talent sourcing (search → slate → DM drafts → present to Ayesha)
- [ ] **During observation, notice:**
  - [ ] Session startup checklist in action (what does Coco check first?)
  - [ ] Execution discipline (where does Coco verify vs. assume?)
  - [ ] Format adherence (is output exactly as locked?)
  - [ ] Communication (how does Coco handle ambiguity?)
- [ ] **Ask live questions:**
  - [ ] "Why are you checking that file?"
  - [ ] "What would happen if you skipped this step?"
  - [ ] "How do you know that number is correct?"
  - [ ] "What would you do differently if [edge case]?"
- [ ] **Debrief:** "What's one thing you'd change about Coco's process?"

**Output:** Real-world understanding of Coco's discipline in action.

---

## WEEK 4: Independence & Ownership

### Monday: Take on a Small Task (2 hours)

**Goal:** Execute your first task end-to-end with Ayesha's guidance.

- [ ] **Pick task from current backlog** (ask Ayesha):
  - [ ] Screen 5-10 CVs for an open role
  - [ ] Write a rejection email for a candidate (draft, not send)
  - [ ] Evaluate 3 case study submissions
  - [ ] Source candidates for an open role
- [ ] **Execute with discipline:**
  - [ ] Run session startup checklist first
  - [ ] Use execution discipline protocol throughout
  - [ ] Complete 8-item self-QA before showing to Ayesha
  - [ ] Get approval before any external sends
- [ ] **Document your process:**
  - [ ] What did you do first?
  - [ ] Where did you get stuck?
  - [ ] What surprised you?
  - [ ] What would you do differently next time?
- [ ] **Debrief with Ayesha:**
  - [ ] Show work
  - [ ] Ask: "Where did I miss the discipline?"
  - [ ] Learn: "What should I lock this decision/format at?"

**Output:** Your first independent task. Feedback from Ayesha on execution.

---

### Tuesday: Review & Iterate (2 hours)

**Goal:** Refine your first task based on feedback.

- [ ] **Incorporate Ayesha's feedback:**
  - [ ] If corrections needed, re-do work (don't just patch)
  - [ ] If format feedback, lock it for next time
  - [ ] If tone feedback, understand the why
- [ ] **Run self-QA again:**
  - [ ] All 8 items passing?
  - [ ] Format matches locked standards?
  - [ ] Tone consistent across output?
- [ ] **Ask:** "Is this ready to send live or pilot first?"

**Output:** Refined task. Ready for live send (or pilot + approval).

---

### Wednesday: Autonomy on Second Task (3 hours)

**Goal:** Execute second task with minimal guidance.

- [ ] **Pick different task type** (if first was CV screening, do rejection email; if case study, do sourcing, etc.):
  - [ ] This expands your breadth
  - [ ] Use different SOP
  - [ ] Apply discipline to different domain
- [ ] **Execute independently:**
  - [ ] Startup checklist ✓
  - [ ] Execution discipline ✓
  - [ ] 8-item self-QA ✓
  - [ ] No external sends without approval ✓
- [ ] **Show Ayesha:**
  - [ ] Here's what I did
  - [ ] Here's my self-QA checklist (all passed)
  - [ ] Here's what I'd do differently next time
  - [ ] Here's where I'd want guidance
- [ ] **Minimal revision expected** (not multiple iterations)

**Output:** Second independent task. Process refined. Discipline internalized.

---

### Thursday: On-Boarding Review (2 hours)

**Goal:** Assess readiness and identify knowledge gaps.

- [ ] **Self-assessment:**
  - [ ] Which SOPs do I know cold? (scoring, rejections, briefing)
  - [ ] Which need more study? (edge cases, rare workflows)
  - [ ] Where do I still refer to memory? (normal! document these)
  - [ ] What surprised me most? (non-obvious discipline rules)
- [ ] **Knowledge check with Ayesha:**
  - [ ] Ask 10 questions you had during onboarding
  - [ ] Ask for 1-2 more advanced resources
  - [ ] Ask about ongoing learning (monthly refreshers? quarterly audits?)
- [ ] **Identify next growth areas:**
  - [ ] Am I ready to mentor someone else?
  - [ ] What would make me 10% more effective?
  - [ ] What edge cases haven't I seen?
- [ ] **Document your on-boarding:**
  - [ ] What worked best for you?
  - [ ] What was confusing?
  - [ ] What should change in on-boarding docs?

**Output:** Clear picture of your capabilities. Knowledge gaps identified. Path forward clear.

---

### Friday: Capstone + Handoff (3 hours)

**Goal:** Demonstrate mastery and become fully independent.

- [ ] **Capstone Task:**
  - [ ] Pick 1 moderately complex task (e.g., full CV screening → report generation)
  - [ ] Execute start-to-finish
  - [ ] Get Ayesha's approval
  - [ ] Handle live send (if appropriate)
- [ ] **Final Knowledge Transfer:**
  - [ ] Document anything Ayesha taught you that's not in SOPs
  - [ ] Suggest improvements to SOPs based on your learning
  - [ ] Identify any gaps in memory system (missing learnings?)
- [ ] **Sign-Off Meeting:**
  - [ ] Ayesha confirms readiness: "You're ready to work independently"
  - [ ] Discuss escalation path: "When do you ask me vs. figure it out?"
  - [ ] Schedule follow-up: "When do we check in again?"
- [ ] **Celebrate!**
  - [ ] You've completed 4-week on-boarding
  - [ ] You understand Coco's discipline and processes
  - [ ] You can execute major hiring operations tasks
  - [ ] You're part of the team

**Output:** Full independence. Ayesha's sign-off. You're ready to own hiring operations.

---

## Throughout All 4 Weeks

### Daily Habits

- [ ] **Morning:** Read 1 memory file (5 min) — rotate through MEMORY.md index
- [ ] **Before tasks:** Run session startup checklist (7 steps)
- [ ] **During work:** Reference relevant SOP as needed
- [ ] **Before sending:** 8-item self-QA + approval request
- [ ] **After feedback:** Update your mental model (what changed? why?)

### Weekly Touchpoints

- [ ] **Monday:** Week planning call with Ayesha (30 min) — what tasks this week?
- [ ] **Thursday:** Mid-week check-in (20 min) — any blockers? quick questions?
- [ ] **Friday:** Week review (30 min) — what did you learn? what's next week?

### Key Questions to Ask (Repeat Often)

1. "Where would you go if you needed to know how to do [task]?"
2. "How do you know that's correct?"
3. "What would happen if you skipped this step?"
4. "Where's the lock-in? What can't change?"
5. "If this failed, what would be the root cause?"
6. "Is this verified or assumed?"
7. "Have we done this before? (check SESSIONS.md)"
8. "What would surprise you if it went wrong?"

---

## Success Criteria

By end of Week 4, you should:

- [ ] **Know the discipline framework** (startup checklist, execution protocol, self-QA)
- [ ] **Navigate all SOPs** (can find any SOP and understand what it says)
- [ ] **Execute 3+ task types independently** (screening, rejections, reports, sourcing, etc.)
- [ ] **Get approval before external sends** (never send without checking)
- [ ] **Recognize patterns** (seen before = use existing SOP, don't reinvent)
- [ ] **Verify before asserting** (verified sources only, "not mentioned" if missing)
- [ ] **Lock formats & rules** (once corrected, applies everywhere)
- [ ] **Own your work end-to-end** (don't delegate back to Ayesha)

---

## Resources

- **CLAUDE.md** — Project overview and routing
- **memory/MEMORY.md** — Index of all learnings and standards
- **SOPs/README.md** — Navigation for all 14+ skills
- **skills.md** — Master index of all operational skills
- **SESSIONS.md** — History of work completed and lessons learned
- **docs/schema.md** — Database structure (Neon PostgreSQL)

---

## Contact & Escalation

- **Questions:** Ask Ayesha
- **Stuck on task:** Check memory/MEMORY.md, then ask Ayesha
- **Format question:** Read REPORT_FORMAT_LOCKED.md, then ask
- **Data question:** Check docs/schema.md, run query, then ask
- **Process question:** Check relevant SOP, re-read, then ask
- **Urgent:** Slack/email Ayesha directly

---

**Created:** 2026-04-20  
**For:** New Coco team members  
**Maintained by:** Ayesha Khan  
**Questions?** See CLAUDE.md or reach out to Ayesha.
