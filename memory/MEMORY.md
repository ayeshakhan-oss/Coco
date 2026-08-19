# MEMORY INDEX — Coco (Real Files Only)

**Last Updated:** 2026-08-10  
**Status:** HOOKS & HARNESS COMPLETE — Automated validation harness implemented for all 4 email types. 5 phases complete, all code live, settings.json wired. Prevents 5 historical regressions. 300-600x faster validation. Production ready.

---

## 🆕 NEW — AUDIO MONITORING 15-DAY RE-ENGAGEMENT, LIVE TO 6 (2026-08-19)
- **[Audio Monitoring Officer — 15-Day Re-Engagement (LIVE 2026-08-19)](project_audio_monitoring_extension_2026_08_19.md)** — 6 in-thread extension confirmations sent live (Fareeda, Kainat, Laraib, Gul Rukh, Arshad, Muddasir): **20 Aug → 3 Sep 2026, 15 days inclusive, PKR 50,000 each**. Establishes the **"Project Extension / Re-Engagement Confirmation"** email type — ~150w, threads onto the original "Welcome to Taleemabad" conversation, 3 bolded elements, NOT a decision email and NOT Design 3, no `[PILOT – ]` prefix (it breaks threading). Ayesha's **reusable signature HTML** captured in the script. 🔴 Three verified traps: (1) **Gmail thread IDs are mailbox-specific** — the MCP connector is authed as jawwad.ali@ while `token_gmail.json` is ayesha.khan@, so a borrowed threadId 404s; RFC822 Message-IDs are global, resolve threads in the mailbox you send FROM. (2) **Muddasir's 8 May welcome went to a typo'd `@gamil.com` and never landed** — unnoticed for 3 months; a thread with zero candidate replies is a signal. Real address recovered from his own calendar RSVP. (3) `newer_than:1h` is unreliable — verify sends with `newer_than:2d` + presence of a `Cc` header to tell live from pilot. Standing rule from Ayesha: **"go live" = keep the CC list the thread already has.**

## 🔴 CRITICAL LEARNING — PILOT RECIPIENTS (2026-06-08)
- **[CRITICAL: PILOT RECIPIENTS ONLY AYESHA (2026-06-08)](CRITICAL_LEARNING_pilot_recipients_only_ayesha_2026_06_08.md)** — 🔒 **ABSOLUTE RULE:** When sending [PILOT – ] emails, TO = ayesha.khan@taleemabad.com ONLY. No CC. No hiring@. No other recipients. This was a discipline failure on 2026-06-08. Add HARD BLOCK to harness. Never deviate.

## 🔒 LOCKED — OPENING LINE + NO FUTURE-PROMISE (2026-06-18)
- **[Mandatory Opening Line + No Future-Promise (2026-06-18)](mandatory_opening_line_no_future_promise_2026_06_18.md)** — All 4 candidate-comms emails MUST open with `This is not a yes for now.` (first line after salutation; harness HARD BLOCK). No future-outreach promises ("we will reach out / keep your name on file") — express welcome as disposition + candidate-initiated (harness WARNING). Wired into harness, templates, CLAUDE.md Rule 10, master philosophy Rules 10-11, SKILL.md, RULES.md, webapp.

## 🆕 NEW — JOB 41 GM-KARACHI: NEW-BATCH SCREENING (2026-08-10)
- **[Job 41 — GM-Karachi New-Batch Screening (2026-08-10)](project_job41_gmk_screening_2026_08_10.md)** — 84 'new' apps: 69 CVs read fully, 15 LinkedIn stubs (no CV). **8 shortlist / 7 maybe / 54 no-hire.** Honest verdict: strong partnership profiles exist but ask 350–800k vs the 210–270k band; only in-band true fits **Syed Zubair Ali** (250k, convening specialist, no B2G) + **Khizran Zehra Baloch** (200–230k, ~3 yrs); Amsal Malik standout junior (225k). ⚠️ Rida Fatima (GIZ/CERP, worked with Taleemabad on TIP Balochistan) is Lahore-based — maybe route to GM-Lahore. Drive CV folder 1xbiqpkci-F8c8h6JrOxzapxdOV_VbsTV. Pilot sent to Ayesha; **NO Markaz statuses changed** — ID-whitelist rule on approval.

## 🆕 NEW — VALUES SCORECARD: HUDA SHAIKH, GM-KARACHI (2026-08-10)
- **[Values Scorecard — Huda Shaikh (GM-Karachi, 2026-08-10)](values_scorecard_huda_shaikh_gm_karachi_2026_08_10.md)** — Zero In 2026-08-10 (50 min). **PASS 6+/0±/0− — cleanest evidence pattern in the GM-Karachi pool.** Filled onto app 3803 (candidate 3075), status stays `shortlisted`, score 6, proceedToRightSeat Yes. GWC: Gets-it YES-leaning (mission-drift question), Wants-it PROBE (recently interviewing elsewhere), Capacity PROBE (health research/grants background — **no BD/partnerships track; case study must test JD pillars**). Salary not discussed. GM-KHI passers now 5: Muneeb, Waqas Hassan, Zirghaam, Zubair Hussain, Huda.

## 🆕 NEW — SMG CASE-STUDY BENCHMARK + ALL-8 EVALUATION, GM PIPELINE SWEEP (2026-08-17)
- **[SMG Case Study Evaluation + GM Pipeline State (2026-08-17)](project_smg_case_study_evaluation_2026_08_17.md)** — Built the **benchmark answer key** ([docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md](../docs/case_studies/benchmarks/smg_execution_sprint_benchmark.md)) + **6-dimension scoring rubric** ([case-study-scoring-rubric.md](../.claude/skills/02_candidate-evaluation/case-study-scoring-rubric.md), Data 20 / **Execution 25** / Stakeholder 20 / Commercial 15 / Discipline 10 / Signal 10), then scored **all 8** Job-42 submissions: Shahmir Hashmat 98* · Arshan Bilal 94 · Yusra Amjad 89 · Umar Zahid 78 · Junaid Ali 74 · Arooj Khalid 70 · Irfan Siddiqui 53 · Basit Hussain 46. **No candidate fabricated data** (every figure recomputed from the CSVs). Order is non-negotiable: **benchmark → QA → then read submissions** (rubric Rule 0). **Never force a fixed shortlist size.** 🔴 Two correction lessons: (1) Umar's tracker looked missing because I'd only seen a **PDF of one sheet** — it existed, 5 tabs, best in pool (73→78); (2) Irfan's "missing" experiments were in his workbook — packaging failure ≠ missing work. Candidates found 6 things the answer key missed (coaching 22.9% failure rate; no Sinhala/Tamil passages; SL = 52% university-only teachers = *causal* reason for zero coaching; SL registrations complete in 4.2 min median vs PK 37.2; lesson-plan→coaching 2× bridge; PK registration failure states) — deliberately kept OUT of the benchmark per Ayesha. **GM sweep same day:** nudges LIVE → Zubair + Zirghaam; debrief invites LIVE → Muneeb, Marzia, Huda (booking link extracted from the live 7 Aug send, never fabricated). 🔴 **Markaz `case_study_status` stays null on send and `gwc_interview_date` is null for all 8 GM submitters — these fields are unreliable, always cross-check the mailbox.**
- **[🔒 Markaz submissions ALWAYS arrive by email (2026-08-17)](markaz_submissions_arrive_by_email_2026_08_17.md)** — Ayesha: "when someone submits the case study response on markaz in document, we always receive it in the email." The **"New Case Study Received"** notification carries the files as attachments. **Check the mailbox FIRST** — the `/api/case-study-file/<app>/<word|excel>` 401 wall is NOT a blocker. Cost of not knowing: an evaluation ranked 5 of 8, and the 3 missing included **2 of the top 3**.
- **[🔒 Benchmark + report hygiene (2026-08-17)](feedback_benchmark_and_report_hygiene_2026_08_17.md)** — (1) A benchmark answer key contains **NO candidate names or responses** — it must calibrate against the case, not this cohort, or it dies as a reusable key. (2) Evaluation reports carry **candidate assessment, not internal-process narrative** — Ayesha cut the whole "Pool Verdict" block because reports get forwarded. Blunt pool verdicts still wanted, **in chat**.

## 🆕 NEW — CASE-STUDY SUBMISSION NUDGE (Skill 06 family) + OUTSTANDING SUBMISSIONS (2026-08-10)
- **[Case-Study Submission Nudge — locked pattern (2026-08-10)](case_study_nudge_type_2026_08_10.md)** — Gentle reminder for sent-but-not-submitted case studies. Locked wording (approved 2026-08-06; Muneeb + Waqas Hassan both submitted after it), no CTA button, reply-to-help flow; sent-day MUST come from Markaz `communication_history` `sentAt` (UTC→PKT); pilot → per-candidate approval (Ayesha may approve a subset). **2026-08-10: Arooj Khali (SMG) nudge LIVE → she submitted by email the same evening (19:17); Zubair Hussain (GM-KHI) piloted but held.** Track record: 3 nudges sent, 3 submissions. Still outstanding end of 2026-08-10: Hafiz Osama (GM-LHR, sent Aug 4 — longest wait), Zubair + Zirghaam + Syeda Masooma (GM-KHI), M. Zeshan + M. Bilal 4051 + Yusra Amjad 4061 (SMG). ⚠️ Flags: Zirghaam was sent the SMG case-study template (not GM); Arooj's Markaz status still `applied` despite values pass.

## 🆕 NEW — VALUES SCORECARD: SALMAN AHMAD, SMG (2026-08-10) — OUT
- **[Values Scorecard — Salman Ahmad (SMG, 2026-08-10)](values_scorecard_salman_ahmad_smg_2026_08_10.md)** — Zero In 2026-08-10 (38 min). **OUT 2+/4±/0−** (≥3 ± rule; near-miss, zero minuses). Filled onto app 3943 (candidate 3189), status → `rejected`, proceedToRightSeat No — approved by Ayesha. Pattern: pivoted hard behavioral questions to adjacent safer stories. ⚠️ Flags recorded verbatim: two "I'm not racist, but…" framings in 38 min; 550k ask vs 350–400k band. **Values feedback email pending** (locked tone, v8, pilot first).

## 🆕 NEW — CASE-STUDY DRIVE FOLDERS + GM-LAHORE EVALUATION (2026-08-10)
- **[Case-Study Folders (KHI + SMG) & GM-Lahore Evaluation (2026-08-10)](case_study_folders_and_gm_lahore_eval_2026_08_10.md)** — Built Drive submission folders mirroring Noah's structure: **GM-Karachi** (1xHkwebowKnb2GnQsFFe5HqbKeAYxbeGD) + **SMG** (1mkrVspKtD1QLFK277dmPPirCP_lHglJA). Muneeb CV added to Markaz+Drive; Waqas Hassan's emailed submission archived + Markaz marked submitted (⚠️ his CV still missing). **GM-Lahore case-study evaluation done** (all 4 read in full): Salman Tariq STRONG PLUS (A4 benchmark, verify research figures) · Abdul Wahab STRONG (best A1) · M. Waqas STRONG (best A2; ⚠️ reflective missing) · Ahmad Wajahat SOLID (A4 chain issues). Report piloted to Ayesha (`send_gm_lahore_case_study_eval_pilot.py`); live send + Markaz score-fill pending. **Later same day:** all 16 shortlisted SMG candidates given Drive subfolders + CVs (keep-all vs prune-to-6 pending Ayesha); SMG submissions archived — Arooj Khalid FULLY (emailed links → real copies), Arshan + Junaid via note+links (files behind Markaz staff-login API, 401 to automation — staff download pending). ⚠️ Lesson: filter email attachments by MIME not filename ("noname" logo archived then corrected); read body for links when no real attachments.

## 🆕 NEW — VALUES SCORECARD: ZUBAIR HUSSAIN, GM-KARACHI (2026-08-07)
- **[Values Scorecard — Zubair Hussain / Hafiz Zubair (GM-Karachi, 2026-08-07)](values_scorecard_zubair_hussain_gm_karachi_2026_08_07.md)** — Zero In 2026-08-07 (35 min). **PASS 5+/1±** (single ± on All for One — vacancies-not-mistake; most-garbled answer). Filled onto existing app 3792 (candidate 699). ⚠️ Worst transcript garble of pool — fairness rule applied. Flags: based ~6 hrs from Karachi (family Islamabad) — confirm relocation; current employer Teach the World Foundation overlaps Sindh govt counterparts; separate CPD Coach app 3793 open. GWC: Gets-it YES-leaning, Wants-it probe, Capacity YES.

## 🆕 NEW — VALUES SCORECARD: MUHAMMAD ARSHAN BILAL, SMG (2026-08-07)
- **[Values Scorecard — Muhammad Arshan Bilal (SMG, 2026-08-07)](values_scorecard_arshan_bilal_smg_2026_08_07.md)** — Zero In 2026-08-07 (35 min). **PASS 4+/2± via ADJUDICATION**: raw count 3+/3± = OUT; Ayesha upgraded Don't Walk Away from Hard Things to + — recorded transparently in scorecard. Filled onto existing app 3884 (candidate 3139). GWC CONDITIONAL (Gets-it probe; capacity B2G untested; ⚠️ short-contracts stability flag). **Available immediately** — fits mid-Sept replacement window. 🔒 New rule this session: NO cross-candidate comparisons in values evaluations (Ayesha).

## 🆕 NEW — VALUES SCORECARD: JAM ZESHAN NAWAZ / MUHAMMAD ZESHAN, SMG (2026-08-07)
- **[Values Scorecard — Jam Zeshan Nawaz (SMG, 2026-08-07)](values_scorecard_zeshan_nawaz_smg_2026_08_07.md)** — Zero In 2026-08-07 (30 min). **PASS 4+/2± via ADJUDICATION**: Coco's raw count was 3+/3± = OUT; Ayesha upgraded Don't Hold On Too Tight to + on the GTM-engine build-and-release evidence — recorded transparently in the scorecard. Filled onto existing app 3921 (candidate 3169, "Muhammad Zeshan"). ⚠️ Two emails, one person: xeshan.nawaz@ (Markaz/invite) + xishan.nawaz@ (his correspondence). GWC: Gets/Wants YES, Capacity YES-leaning (B2G untested). Salary 370k, matchable. Debrief retests: upward feedback (V4), advocacy (V2).

## 🆕 NEW — 🔑 AYESHA MAILBOX VIA IMAP + GROWTH PIPELINE SNAPSHOT (2026-08-10)
- **[🔑 Ayesha mailbox via IMAP app-password (2026-08-10)](reference_ayesha_mailbox_imap_2026_08_10.md)** — Calendar OAuth token re-verified DEAD (`deleted_client`); the working calendar-evidence path is **read-only IMAP into ayesha.khan@ with the `.env` SMTP app password** (booking subjects carry candidate + slot; some arrive from her niete.edu.pk alias — search by SUBJECT). Ayesha authorized 2026-08-10. Always readonly+PEEK, log to read_audit.log.
- **[Growth roles pipeline snapshot (2026-08-10)](growth_roles_pipeline_snapshot_2026_08_10.md)** — All 3 growth pipelines verified: 5 debrief invites ever sent (4 GM-LHR all BOOKED Mon–Thu; Waqas Hassan GM-KHI NOT booked → nudge); Muneeb Arif debrief invite pending; SMG batch-3 screening (76 read, 5 shortlist-grade incl. Ahmad Taj 76%) awaiting Ayesha; parallel direct-send SMG values track discovered (6 invites, 4 Zero-In bookings); 3 SMG case studies submitted. Open actions listed.

## 🆕 NEW — JOB 42 SMG: SCREENING + VALUES INVITES (2026-08-05)
- **[Job 42 — Senior Manager Growth: Screening + Values Invites (2026-08-05)](project_job42_smg_screening_2026_08_05.md)** — 79 CVs read across 2 batches (honest verdict: moderate-to-thin, top ~75%). **10 shortlisted + values-invited LIVE** (CC: Ayesha, hiring@, Waqas Tanveer=HM, Ali Sipra); 77 rejected (statuses only, NO emails); Kamran Ali (3930, Orenda alum) left 'new' per Ayesha. Job open to 15 Aug — batch-3 sweep due at close; 9+ arrivals already unscreened. ⚠️ Contains two reusable learnings: **Neon HTTPS SQL API workaround** (port 5432 blocked → POST /sql w/ Neon-Connection-String header) and **live-job bulk-update rule** (ID whitelist + row-count assert, never status-filter — first bulk reject swept 10 unscreened arrivals, caught & reverted).

## 🆕 NEW — VALUES SCORECARD: HAFIZ OSAMA, GM-LAHORE (2026-08-04)
- **[Values Scorecard — Hafiz Osama, Growth Manager – Lahore (2026-08-04)](values_scorecard_hafiz_osama_gm_lahore_2026_08_04.md)** — Zero In 2026-07-29 (35 min). **PASS boundary** (4 plus, 2 plus-minus: Continuously Improve + Don't Hold On Too Tight). Filled onto existing app 3601 (candidate 2900). ⚠️ Worst transcript in pool (garbled mixed-language) — fairness rule applied, spot-check recording for Courageous Conversations + Practice Joy. **Ex-Taleemabad (his claim — verify): ~3 yrs, growth work Lahore, reported to Faisal.** GWC CONDITIONAL (Wants-it probe). No salary captured.

## 🆕 NEW — VALUES SCORECARD: ZIRGHAAM AHMAD, GM-KARACHI (2026-08-04)
- **[Values Scorecard — Zirghaam Ahmad, Growth Manager – Karachi (2026-08-04)](values_scorecard_zirghaam_ahmad_gm_karachi_2026_08_04.md)** — Zero In 2026-07-27, 68 min. **PASS 6+/0± — strongest card in the GM pool**; GWC **all three YES** (first in pool) → Right Seat ready. Filled onto existing app 3830 (candidate 3100); status `new`→`shortlisted`. Scored from Fathom recap (single source — caveat in scorecard). ⚠️ Also holds GM-Lahore app 3831 (untouched). On vacation to mid-Aug — debrief after return; 48-hr case study to be sent.

## 🆕 NEW — VALUES SCORECARD: ABDUL WAHAB, GM-LAHORE (2026-08-03)
- **[Values Scorecard — Abdul Wahab, Growth Manager – Lahore (2026-08-03)](values_scorecard_abdul_wahab_gm_lahore_2026_08_03.md)** — Zero In call 2026-07-27. **PASS boundary** (4 plus, 2 plus-minus: All for One + Don't Hold On Too Tight). Filled onto EXISTING app 3614 (candidate 2911) via UPDATE. ⚠️ Scored from Fathom recap + Read AI report (no full transcript — Ayesha's instruction); summaries conflict on management style, flagged + excluded. **Prior Taleemabad employee** → GWC Gets-it YES (rare); Wants-it probe at debrief. NOT the same person as Waqas Hassan (GM-Karachi).

## 🆕 NEW — VALUES SCORECARD: WAQAS HASSAN, GM-KARACHI (2026-08-03)
- **[Values Scorecard — Waqas Hassan, Growth Manager – Karachi (2026-08-03)](values_scorecard_waqas_hassan_gm_karachi_2026_08_03.md)** — Zero In call 2026-07-24. **PASS at the exact boundary** (4 plus, 2 plus-minus: Don't Walk Away + Continuously Improve; zero minuses); GWC CONDITIONAL (Gets it untested, Wants it mixed via Lahore openness, Capacity yes). ✅ Submitted to Markaz 2026-08-03 — no record existed, created candidate 3130 + app 3870 (job 41, `shortlisted`, `pass`, score 4). ⚠️ NOT the same person as Muhammad Waqas (GM-Lahore, app 3651). Open: possible 2nd app row for GM-Lahore (Ayesha agreed verbally on the call, unconfirmed); salary 425–450k ask vs 350k current.

## 🆕 NEW — VALUES SCORECARD: MUNEEB ARIF, GM-KARACHI (2026-07-31)
- **[Values Scorecard — Muneeb Arif, Growth Manager – Karachi (2026-07-31)](values_scorecard_muneeb_arif_gm_karachi_2026_07_31.md)** — Zero In call 2026-07-30. **PASS** (5 plus, 1 plus-minus on Continuously Improve, zero minuses); GWC CONDITIONAL (Gets it / Wants it not probed — ask "why Taleemabad?" at case-study debrief). ✅ **Submitted to Markaz 2026-08-03** — no record existed (verified incl. duplicate-record Step 0 + Gmail email match), so on Ayesha's approval created candidate 3129 + application 3869 (job 41, status `shortlisted`, result `pass`, score 5). Candidate promised detailed feedback by Mon Aug 3.

## 🆕 NEW — CASE STUDY UPDATE / DEBRIEF-PENDING EMAIL (Skill 01 type #6, 2026-08-13)
- **[Case Study Update — Debrief-Pending (Skill 01 type #6, 2026-08-13)](case_study_update_email_type_2026_08_13.md)** — Short status note to a candidate who **already submitted their case study** and is waiting on a debrief decision. Lives under **Skill 01 (candidate communication)** as a sibling of the Warm Hold Decision-Pending Update (type #5), created at Ayesha's request 2026-08-13. Says three things only: thanks for the work, we are still mid-interviews so nothing is decided, and **"we expect to share an update with you on the case study debrief interview call by [timeline]"** (Ayesha's exact wording — say "case study debrief interview call", NEVER just "debrief"). **EXEMPTIONS (inherited from type #5):** no "This is not a yes for now." opener, the dated promise is REQUIRED (future-promise ban inverted), 800-word minimum does not apply → target **120-250 words**. **NEW exemption scoped to THIS TYPE ONLY:** "case study" is permitted candidate-facing language (it is the candidate's own deliverable, and Ayesha names it on the values call) — this does NOT loosen the jargon ban anywhere else. **BANS:** no evaluation of the submission, no direction hints, no apology theatrics, no new asks, no mention of other candidates. Subject 🔒 `A Quick Update from Our Side` (deliberately a sibling of type #5's "A Quick Note from Our Side"). Layout: v8 via `EYEBROW["case_study_update"]`. Script: `scripts/send_case_study_update_pilot.py`. **⚠️ NEVER rename that script to contain `warm_bench`/`gwc`/`values`/`rejection`** — the send-time hook infers type from the filename and would HARD BLOCK this 133-word note as an under-length 800-word feedback letter. **Default CC (Ayesha 2026-08-13):** ayesha.khan@ + waqas.tanveer@ + ali.sipra@ + hiring@. First live use 2026-08-13: 4 Job-42 SMG case-study submitters (Arshan Bilal, Junaid Ali, Arooj Khalid, Yusra Amjad). **Guardrail:** if the promised timeline will slip, send a fresh note BEFORE it passes. Skill file: [case-study-update-email.md](../.claude/skills/01_candidate-communication/case-study-update-email.md).

## 🆕 NEW — CASE STUDIES: SMG + GROWTH MANAGER, DERIVED FROM HOG (2026-07-31)
- **[SMG + GM Case Studies from HOG (2026-07-31)](case_studies_smg_gm_from_hog_2026_07_31.md)** — Two role-calibrated case studies derived from the HOG "Growth Flywheel Stress Test": SMG "The Execution Sprint" (2.5–3h, execution-level: scoped Alpha dataset analysis, run-the-given-growth-loop plan w/ K-factor 0.2, stalled B2G deal) + GM "The Story, the Room, and the Deal" (2–2.5h: policy storytelling, convening design, partnership pipeline). Delivered as Google Docs matching HOG layout (Quicksand, blue #3C78D8, per-page logo). Sources: `docs/case_studies/`, generator: `scripts/case_studies/make_growth_case_study_docs.py`. **⚠️ SMG "Data Access: Here" links still need Ayesha to attach the Alpha Platform dataset URLs.**

## 🆕 NEW — CASE STUDY: PROJECT EXTENSION/RENEWAL (2026-07-31)
- **[Case Study — Project Extension/Renewal (2026-07-31)](case_study_project_extension_renewal_2026_07_31.md)** — Growth/Govt-Partnerships case-study question: how will you get a government-funded institute program extended or renewed (FD → Ministry → Planning Commission, PC-1). **Locked rules:** "How will you get the project extended?" leads; NEVER the word "award"; no real figures; institute anonymized. Full text: `docs/case_studies/case_study_project_extension_renewal.md`.

## 🆕 NEW — ASSESSMENT CENTER ACTIVITY (invite type #7, 2026-07-31)
- **[Assessment Center Activity — invite type #7 (2026-07-31)](assessment_center_invite_type_2026_07_31.md)** — Onsite full-day assessment center invite. Lives under **Skill 06 (candidate invites)**, locked invite design. **HARD RULES:** NO booking button/link — candidates REPLY to confirm and the Google Calendar invitation follows to confirmed candidates; venue address + Maps link in the email ONLY as Ayesha provides them (no plus codes); dates re-confirmed per batch; signature adds Ayesha Raza Khan (LinkedIn-hyperlinked) + 03354288844. Scripts: `send_assessment_center_pilot.py` (reference) + `send_assessment_center_cpd_coach_batch.py` (gitignored, PII). First live use 2026-07-31: all 12 CPD Coach (JOB-0017) candidates for the Aug-6 assessment day (11 in first batch, Hajra Sajjad added later same day).

## 🆕 NEW — INTERVIEW REMINDER (invite type #6, 2026-07-23)
- **[Interview Reminder — invite type #6 (2026-07-23)](interview_reminder_note_type_2026_07_23.md)** — Day-before nudge for an ALREADY-BOOKED interview. Lives under **Skill 06 (candidate invites)**, NOT candidate-communication — no "This is not a yes for now." opener, no 800-word rule, locked invite design. **HARD RULES:** verified calendar/Gmail data only (calendar token is dead → use Gmail booking/invitation emails); check for cancellations first; Meet-link button ONLY with a verified link (else "link in your calendar invitation" line); never guess a candidate's name from their email address. Script: `scripts/send_interview_reminder_pilot.py` (gitignored, PII). First live use 2026-07-23 for the Jul-24 GM-Lahore zero-in calls.

## 🆕 KEEP-IN-TOUCH NOTE (invite type #5, 2026-06-19)
- **[Keep-in-Touch Note — invite type #5 (2026-06-19)](keep_in_touch_note_type_2026_06_19.md)** — Post-conversation warm hold: we already spoke, the role is being revisited, the candidate is still in our thinking. Lives under **Skill 06 (candidate invites)**, NOT rejection/feedback — so the "This is not a yes for now." opener does NOT apply. **TWO HARD RULES:** (1) NO booking button / no links — we are not asking them to schedule anything yet; (2) NO promise or commitment — no "we will reach out", no hard date, no outcome mention; honest + conditional only (a soft "hopefully in July" hope is OK if the user asks). Script: `scripts/send_keep_in_touch_pilot.py` (parameterized `CANDIDATES` list, pilots to Ayesha, sends individual live emails). First use: 5 Job 32 fundraising exploratory-call candidates (Falah, Kanooz, Nirmal, Mushahid, Saadia), sent live 2026-06-19.

---

## 🔴 MUST READ THESE FIRST (Session Start + Every Task)

### Core Discipline (_core/)
- [CORE_DISCIPLINE.md](_core/CORE_DISCIPLINE.md) — **SINGLE SOURCE:** All 10 rules + execution protocol. Read before any task.
- [SELF_QA_CHECKLIST.md](_core/SELF_QA_CHECKLIST.md) — **8 ITEMS REQUIRED:** Run before submitting ANY work.
- [TASK_SOP_MAP.md](_core/TASK_SOP_MAP.md) — **TASK REFERENCE:** Maps each task to its SOP + template + checklist.
- [Session Startup Checklist](_core/session_startup_checklist.md) — 7-step check (run at session start)

### Non-Negotiable Rules (2026-05-12 + 2026-05-30 UPDATES)
- **[RULE — All Feedback Emails Use Locked Tone](rule_all_feedback_emails_use_locked_tone.md)** — 🔒 VALUES FEEDBACK + WARM BENCH + GWC REJECTIONS + ALL CANDIDATE EMAILS must follow locked tone. No exceptions. Read before ANY rejection/feedback email.
- **[WARM BENCH EMAILS — LOCKED RULES (2026-05-30)](warm_bench_locked_rules_2026_05_30.md)** — 🔒 CRITICAL CORRECTIONS. Never mention interviewer names. Never use internal jargon (GWC, values, scorecard). Use exact heading format. Start with "This is not a yes for now." Reference: Fatima Saeed email (May 15). **READ BEFORE EVERY WARM BENCH EMAIL.**
- **[CANDIDATE COMMUNICATION QUALITY REVIEW PROTOCOL (2026-05-30)](candidate_communication_quality_review_protocol_2026_05_30.md)** — 🔒 10-point checklist + Haroon Yasin balance rule. Balance praise specificity with decision specificity. Avoid generic labels. No "good candidate"—use character observations. **RUN BEFORE SENDING ANY CANDIDATE EMAIL.**
- **[AVOID RECRUITING ABSTRACTIONS (2026-05-30)](candidate_communication_avoid_recruiting_abstractions_2026_05_30.md)** — 🔒 CRITICAL. Replace all generic recruiting phrases ("good candidate", "strong profile", "not a good fit") with observed behaviors and concrete realities. Candidate must feel "They SAW me" not "They SCORED me." **APPLIES TO ALL CANDIDATE EMAILS.**
- **[NO INTENT INFERENCE IN REJECTION EMAILS (2026-06-01)](lesson_no_intent_inference_rejection_emails_2026_06_01.md)** — 🔒 CRITICAL PRINCIPLE. Never tell candidates what they assumed, believed, thought, preferred, or were energized by. Use observations + unanswered questions instead. Replace "you assumed X" with "what left us uncertain was X". Eliminates mind-reading, keeps emails mentoring not prosecutorial. **SCAN FOR INTENT-WORDS BEFORE EVERY REJECTION EMAIL.**
- **[CV REJECTION = APPLICATION ONLY + "WE" VOICE (2026-07-09)](lesson_cv_rejection_no_interaction_2026_07_09.md)** — 🔒 CRITICAL. Rule 13: a `cv_rejection` had NO interview/call/conversation — never fabricate one ("conversations and assessments", "we spoke", "what we observed"); ground everything in the written application. Rule 12: collective "we" voice, never "I"/"my"/"me". Both harness HARD BLOCKS + drafting prompt. **APPLIES TO EVERY CV REJECTION.**
- **[EVIDENCE-BASED REJECTION RATIONALE — HAROON YASIN BALANCE RULE (2026-06-01)](lesson_evidence_based_rejection_rationale_2026_06_01.md)** — 🔒 COMPLEMENTARY TO INTENT-INFERENCE RULE. Praise specificity must approximately equal decision specificity. For every detailed praise example, provide equally detailed gap example. Use "Can you show me?" test: if candidate can't point to exact moment that led to decision, rationale is too abstract. Rewrite with concrete behaviors, not mental state assumptions.

---

## SESSION TRACKING (Per-Session)

### Active Session & Lessons (_session/)
- [Lessons Learned Log](_session/lessons_learned.md) — Structured append-only log: date, task, mistake, correction, rule. Updated by Stop hook. Max 50 entries.
- [Active Session Scratchpad](_session/session_active.md) — Live notes for current session: task, decisions, mistakes, files modified. Wiped at session start.
- **[Session — CPD Coach Warm Bench COMPLETE (2026-05-15)](_session/session_cpd_coach_warmBench_complete_2026_05_15.md)** — All 3 emails processed: Hajra (values+GWC) + Unzeela (values+GWC, jargon corrected) + Fatima (GWC-only). Hajra live sent successfully. Unzeela pilot already sent (prior session). Fatima ready for live send. Subject lines locked: "The Principal's Expressions Changed When Data Spoke" (Hajra), "When Difficult Things Become Safer" (Unzeela), "When Personal Experience Becomes Professional Calling" (Fatima). Key learning: remove internal jargon (GWC terminology, scorecard language) from warm bench emails — use observational tone only. All locked formatting enforced. Status: ✅ PRODUCTION READY.

---

## 🎯 SKILLS (Production Ready)

### Candidate Communication — MASTER INDEX (2026-06-08) 🔒
- **[CANDIDATE COMMUNICATION LOCKED INDEX (2026-06-08)](CANDIDATE_COMMUNICATION_LOCKED_INDEX_2026_06_08.md)** — 🔒 **START HERE FOR ALL CANDIDATE EMAILS.** Single source of truth for GWC rejections, warm bench, values feedback, all candidate communication. Points to correct locked versions ONLY. Supersedes all old/duplicate versions. Clarifies potential confusion points (where does P.S. go? which template? what colors?). Reference case: Hira Abbasi (2026-06-08). **No more confusion. No more back-and-forth.**

### 🔒 LOCKED LAYOUT (2026-06-10) — applies to ALL candidate communication
- **[v8 Candidate Comms Layout — LOCKED (2026-06-10)](v8_candidate_comms_layout_LOCKED.md)** — 🔒 **THE visual layout for every candidate communication email** (CV rejection, values feedback, warm bench, GWC, + any future type). Single shared module `scripts/utils/v8_template.py` (H/SUB/P/PS/FOOTER/wrap/attach_logo/EYEBROW). Never redefine inline. Spec: #f0f4f0 canvas, 620px card, Georgia 15px/1.8 justified, #1565c0 blue + #1b5e20 green, embedded cid logo, P.S. box. Ayesha approved via Syeda values feedback (2026-06-10). NOT for Skill 06 invites. Reference impl: send_cpd_coach_values_feedback_syeda_2026_06_10_pilot.py.

### Sub-Resources (Use via Master Index Above)
- **[GWC REJECTION LOCKED APPROACH (2026-06-08)](gwc_rejection_locked_approach_2026_06_08.md)** — Complete locked approach for GWC rejections using warm bench structure.
- **[WARM BENCH LOCKED RULES (2026-05-30)](warm_bench_locked_rules_2026_05_30.md)** — 13 locked rules for warm bench emails.
- **[P.S. SECTION STYLING LOCKED (2026-06-08)](ps_section_styling_locked_2026_06_08.md)** — Premium personal styling for postscript sections (ALL candidate emails).

### Individual Skills
- **[06_candidate-invites (2026-05-14)](../skills/06_candidate-invites/SKILL.md)** — Universal skill for ALL interview invites + opportunity emails. 4 types: Values Interview Invite, Case Study Debrief Invite, Exploratory Call Invite, Warm Bench Opportunity Invite. Design 100% locked (see locked templates). Reference scripts: send_values_interview_pilot.py, send_case_study_debrief_pilot.py, send_exploratory_call_pilot.py, send_warm_bench_invite_pilot.py. Workflow: customize script → pilot to Ayesha → approval → live send.
- **🔒 [07_contract-drafting (2026-08-12)](../.claude/skills/07_contract-drafting/SKILL.md)** — Contracts/NDAs/addendums from approved masters in `Contracts\` (gitignored) ONLY. Orchestrator + 9 sub-skills (one per entity + doc family): opl/owt/inc/niete-contracts, fellow-contracts, addendum-promotion, team-move-new-contract, ndas, joining-emails. 4 entities OPL/OWT/Inc./NIETE — never assume entity or type; fill yellow-highlighted fields only (OWT: XYZ spots); never touch legal wording; Fellow → Fellow NDA never Permanent; same-team promotion → Addendum, team move → new contract; JD asked every time → Annexure-A in-document; contract+NDA packaged together; pilot to Ayesha before any send. Template matrix: [TEMPLATE_MAP.md](../.claude/skills/07_contract-drafting/TEMPLATE_MAP.md). ⏳ 5 joining-email templates pending from Ayesha. Full record: [skill07_contract_drafting_locked_2026_08_12.md](skill07_contract_drafting_locked_2026_08_12.md).
- **🔒 [NIETE CPD Coach contracts + 2 REMOVED clauses (2026-08-19)](niete_cpd_coach_contracts_2026_08_19.md)** — Ayesha: the **in-house-lunch** and **business-travel** clauses are stripped from **EVERY NIETE contract** at build time (`P_DROP_CLAUSES` in `build_niete_cpd_coaches.py`; capture paragraph objects BEFORE the index-based fills, delete after, assert the master's wording first). Batch sent: Mariam Naqvi (24 Aug, 116k, → Abdul Waheed, **returning member**) · Naima Javed (26 Aug, 127k, → Anam Masood) · Hafiza Iqra Bashir (1 Sep, 108k, → Abdul Waheed). Split 90/9/1 of gross. 🔴 **The salary is the NEGOTIATED figure — read the offer thread to the end**; Mariam and Hafiza both countered and were held. 🔴 `contract_docx_eval.py --type` defaults to `fellow` → pass `--type project` or get 11 FALSE hard blocks. 🔴 The claude.ai Gmail connector may be authed as **another user** (was `salman.iqbal@`) — offer letters live in ayesha.khan@ via IMAP; a null result there is not evidence. ⚠️ Hina + Noor Ul Ain still hold pre-change contracts; all three new hires still `shortlisted` in Markaz. ⚠️ **`.gitignore` `Contracts/` is unanchored and also hides `scripts/contracts/`** — the whole Skill 07 toolchain is untracked, and can't just be committed because it hardcodes CNICs (fix needs Ayesha's call).

### Third-Party Skills
- **[UI/UX Pro Max — Install Notes (2026-06-15)](ui_ux_pro_max_skill_install.md)** — General UI/UX design-intelligence skill (NextLevelBuilder, MIT). Installed at `.claude/skills/ui-ux-pro-max/`, **vendored local-only (gitignored)** — reinstall via `npx uipro-cli init --ai claude`. 🔴 CRITICAL: every reinstall wipes the Windows `python3`→`python` + path patch in `SKILL.md` — re-apply it. Locked v8/invite designs OVERRIDE it (CLAUDE.md Rule 9). Local CSV engine, no network calls.

---

## 🎯 MASTER REFERENCE (NEW — 2026-05-08)

### Consolidated Rules & Skills
- **[RULES.md](../RULES.md)** — **MASTER REFERENCE** (20.8 KB). Consolidates all 7 skills, locked approaches, discipline rules, and integration requirements into single authoritative source. Read this instead of scattered files. Includes:
  - 7 Core Discipline Rules
  - 7 Skill-Specific Rules (CV Screening, Rejection Emails, Warm Bench, Attendance Reports, Interview Invites, Decision Briefs, Talent Sourcing)
  - Locked Approaches (exact specs for each skill)
  - Integration & Testing Rules
  - Discrepancy Minimization table

---

## 🛡️ AUTOMATION & VALIDATION (2026-06-08 — THREE-LAYER SYSTEM)

### Three-Layer Pre-Draft Enforcement (Solves Ayesha's Feedback)
- **[THREE-LAYER PRE-DRAFT ENFORCEMENT (2026-06-08)](three_layer_pre_draft_enforcement_2026_06_08.md)** — ✅ COMPLETE. Prevents bad drafts at SOURCE, not at send time. **LAYER 1 (Draft Time):** UserPromptSubmit hook auto-injects locked template HTML + pre-flight checklist when "draft gwc rejection" detected. Can't create custom HTML (template is right there). **LAYER 2 (Pre-Draft Gate):** Mandatory checklist blocks drafting until all items acknowledged (master index read, template read, locked approach understood, 7 BLOCKs acknowledged). **LAYER 3 (Send Time):** PreToolUse hook catches violations. 4 locked templates created (GWC, warm bench, values, CV). Prevents deviation by design. **[Enhanced Hook](scripts/memory/prompt_submit_hook.py)** | **[Pre-Flight Checklist](pre_draft_checklist_2026_06_08.md)**

### Send-Time Validation (Layer 3)
- **[HOOKS & HARNESS IMPLEMENTATION (2026-06-08)](hooks_and_harness_implementation_2026_06_08.md)** — ✅ PHASE 1. Automated validation for all 4 email types (GWC, CV, warm bench, values). 5 phases: eval engine (10 checks), pre-send hook, memory injection (4 new triggers), missing lesson file, CLI tool. 7 HARD BLOCKs block sends. 3 WARNINGs logged. PreToolUse hook wired in settings.json. Prevents 5 historical regressions (PILOT prefix, intent-words, em dashes, word count, names). 300-600x faster validation. **[Impact Analysis](scripts/evals/BEFORE_AND_AFTER_REPORT.md)** | **[Technical Docs](scripts/evals/EVAL_HARNESS_IMPLEMENTATION.md)**

---

## PRODUCTION RULES (Locked & Reference)

### Locked Approaches & Templates (_locked/)
- [Warm Bench Final Locked Approach](_locked/warm_bench_final_locked_approach.md) — Haroon Yasin framework, 800-1100 words, poetic subjects, locked approach.
- **[🔒 Warm Bench Subject Lines - Locked Pattern (2026-05-15)](_locked/warm_bench_subject_lines_locked.md)** — CRITICAL. Subject lines must be poetic, story-based, tied to specific interview moment. Examples: "The Principal's Expressions Changed When Data Spoke" (✅) vs "Hajra Sajjad - CPD Coach Position Update" (❌). Pattern: [MOMENT] + [ACTION/REALIZATION] + [CONSEQUENCE]. Status: 🔒 LOCKED IN.
- [Attendance Report Complete Template](_locked/attendance_report_complete_template.md) — Stat boxes, colors, table structure, PDF/HTML format locked.
- **[🔒 Locked Exploratory Call Invite (2026-05-15)](locked_exploratory_call_invite_approach.md)** — 30-minute calls for candidates without immediate role fit. Body text locked word-for-word. Links (booking + Fundraising Overview doc) locked. Design locked to universal template. Scripts: send_exploratory_call_batch_pilot.py + send_exploratory_call_batch_live.py. Tested with 4 candidates 2026-05-15. Status: ✅ PRODUCTION READY.
- **[🔒 LOCKED Email Template — INTERVIEW INVITES / Skill 06 (2026-05-13, scope narrowed 2026-06-10)](locked_email_template_interview_invites_FINAL_2026_05_13.md)** — INVITES & opportunity emails ONLY (values/case-study/GWC/exploratory invites, round/final/offer, warm bench OPPORTUNITY invites). Design: 775px white card in #e5e7e2 wrapper on #f5f5f5 bg, 34px logo, 17px body, 1.85 line-height. **No longer covers rejections/feedback** — those use the v8 layout (see v8_candidate_comms_layout_LOCKED.md). Conflict resolved by Ayesha 2026-06-10.
- [Values Feedback Email Tone — LOCKED (2026-05-12)](values_feedback_email_tone_locked_2026_05_12.md) — Complete tone guide. Warm, observational, deeply human. NO life-coach language. No internal jargon. 800+ words mandatory. Self-QA checklist included.
- [Locked Templates Index](_locked/locked_templates_index.md) — Quick reference to all locked formats.

---

## SYSTEM ARCHITECTURE & OPTIMIZATION

### Progressive Disclosure Documentation
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — Final architecture after Phase 3. Before/after file counts, context loading flow, single source of truth hierarchy.

### Project Cleanup & Consolidation
- [Project Cleanup Complete (2026-05-08)](../CLEANUP_COMPLETE_2026_05_08.md) — *(DELETED — superseded by RULES.md)* 
- [System Consolidation Complete](_project/system_consolidation_2026_04_28.md) — Major refactor: consolidated discipline docs, extracted templates to code, created task mapping. (April 28 snapshot)

---

## DISCIPLINE & FEEDBACK RULES (_feedback/)

### Problems Identified & Fixed
- [Coco Core Problems Identified](_feedback/coco_core_problems_identified.md) — 10 systemic discipline issues + solutions locked in (Session 002 analysis).
- [Teams API Incompleteness](_feedback/discipline_failure_teams_api_incomplete.md) — When APIs return suspiciously small results, verify with ground truth.
- [Discipline Enforcement Lockdown](_feedback/discipline_enforcement_lockdown.md) — 5 non-negotiable rules to stop leakage (memory-first, verification, templates, single-pass, no delegation).
- [Coco Delegation Discipline](_feedback/coco_delegation_discipline.md) — Never delegate tasks back to user. Check memory FIRST.

### Format & Integration Rules
- [Decision Brief CV Hyperlinks](_feedback/feedback_decision_brief_hyperlinks.md) — Every candidate name must link to Google Drive CV.
- [Gmail Thread Replies](_feedback/feedback_gmail_thread_reply.md) — In-Reply-To + References headers required for proper threading.
- [PDF Formatting](_feedback/feedback_pdf_formatting.md) — All ReportLab PDFs must use TA_JUSTIFY on body text.
- [Terminology Standards](_feedback/feedback_terminology.md) — Never "KCD" in reports; never "TBC/Pending" — use specific language.
- [Bulk Rejection CV Truncation](_feedback/feedback_bulk_rejection_cv_truncation.md) — Minimum 10k chars, never cv_text[:4500], flag long CVs.
- [DB Status vs Pipeline Reality](_feedback/feedback_db_status_vs_pipeline.md) — status='offer' is a stage, NOT a sent offer. Never assert without verification.
- [Values Scorecard Schema](_feedback/feedback_values_scorecard_schema.md) — Markaz JSON schema exact format required.
- [Values Scorecard Duplicate Applications (2026-05-12)](_feedback/values_scorecard_duplicate_applications.md) — **MANDATORY Step 0:** Query all app records before submitting. Markaz UI shows most recent. Submit to correct record or form stays blank. SOP + SQL pattern included.

---

## PROJECT CONTEXT (_project/)

### Infrastructure & Integration
- [Teams Integration](_project/project_teams_integration.md) — Microsoft Graph API setup, Presence channel reading, known issues.
- [Project Security Hardening](_project/project_security_hardening.md) — safe_sendmail bouncer, read audit, token monitor, scope auditor, git data cleanup.

### Content & Articles
- [Rejection Feedback Article](_project/project_article_rejection_feedback.md) — LinkedIn/Medium article on personalized rejections (draft complete, awaiting publication).

### Completed Work
- [Soul Architect Talent Sourcing (Phase 3)](_project/project_soul_architect_sourcing_final.md) — 47 verified candidates sourced, Excel sent to Ayesha.

### Job-Specific Context
- [Job 32 Fundraising Links](_project/project_job32_links.md) — JD Google Doc + Calendar booking link for values invites.
- [Job 17 CPD Coach](_project/project_job17_cpd_coach.md) — Warm bench candidate context.
- [Job 26 Soul Architect Final](_project/project_job26_soul_architect_final.md) — 42 candidates screened, 15 top-tier, complete report.
- [Job 36 Decision Brief](_project/project_job36_decision_brief.md) — Final candidates & decision view approved format.
- [Job 36 New Batch](_project/project_job36_new_batch.md) — 19 screened, 15 emails generated, pilot sent.

### Hiring & Pipeline
- [Hiring Pipeline Monitor](_project/project_hiring_pipeline_monitor.md) — Proactive system runs Mon 10:30am + Fri 3pm, monitors all open positions, flags candidates stuck 3+ days.

---

## OPERATIONAL DUTIES

- [Proactive SOP Maintenance](_feedback/proactive_sop_maintenance_duty.md) — Automatic duty: copy new SOPs to SOPs folder, update README, commit to git.

---

## HOW TO USE THIS INDEX

### Navigation by Purpose

**At Session Start:**
1. Load CORE_DISCIPLINE.md from _core/
2. Run Session Startup Checklist (also in _core/)
3. Check Active Session Scratchpad for current task

**When Starting a Task:**
1. Check TASK_SOP_MAP in _core/ → Find your task type
2. Go to RULES.md (root) → Find skill section
3. Read exact locked specifications for that skill
4. Load SOPs/CLAUDE.md (L2 context if needed)
5. Load relevant locked template from _locked/ (if applicable)
6. Check _feedback/ for relevant rules/lessons (feedback docs)
7. Run SELF_QA_CHECKLIST before sending

**When Writing Code:**
1. Load scripts/CLAUDE.md (L2 context)
2. Read relevant data/systems section from RULES.md
3. Load _project/ context (if task-specific)
4. Check scripts/utils/ and scripts/jobs/ for similar code

**When Stuck:**
1. Search _feedback/ for discipline rules / lessons learned
2. Search _project/ for prior work on similar task
3. Check _locked/ for locked approaches that might apply
4. Check RULES.md discrepancy table for common issues

### Folder Structure (Organized by Purpose)

```
memory/
├── _core/              (ALWAYS LOAD) — 4 files
│   ├── CORE_DISCIPLINE.md
│   ├── SELF_QA_CHECKLIST.md
│   ├── TASK_SOP_MAP.md
│   └── session_startup_checklist.md
├── _session/           (PER-SESSION) — 2 files
│   ├── session_active.md (live scratchpad)
│   └── lessons_learned.md (mistake log)
├── _locked/            (REFERENCE) — 5 files
│   ├── warm_bench_final_locked_approach.md
│   ├── attendance_report_complete_template.md
│   ├── locked_email_template_interview_invites.md
│   ├── locked_templates_index.md
│   └── locked_skill_warm_bench_interview_invite.md
├── _feedback/          (DISCIPLINE + RULES) — 15 files
│   ├── feedback_*.md (7 files)
│   ├── discipline_*.md (3 files)
│   ├── coco_*.md (3 files)
│   └── proactive_sop_maintenance_duty.md
├── _project/           (PROJECT CONTEXT) — 12 files
│   ├── project_*.md (all project-specific context)
│   └── system_consolidation_2026_04_28.md
└── MEMORY.md           (THIS FILE — Master Index)
```

---

## SINGLE SOURCE OF TRUTH

**PRIMARY: RULES.md (root)** — All 7 skills, locked specs, discipline rules consolidated.

**SECONDARY: SOPs/** — Skill procedure definitions (reference material).

**TERTIARY: memory/** — Project context, feedback, lessons learned.

After Phase 3 consolidation:
- ✅ RULES.md created (20.8 KB master reference)
- ✅ 21 irrelevant files deleted (audit docs, drafts, duplicates)
- ✅ Zero regressions: all Python scripts compile, integrations tested
- ✅ Single source of truth hierarchy established

---

## HOW TO ADD TO MEMORY

When learning something new:
1. Decide which category it belongs to (_core, _session, _locked, _feedback, _project)
2. Create new file with clear name
3. Add entry to relevant section of this MEMORY.md
4. Commit with message explaining why it's stored
5. If it's a duplicate of existing file, consolidate instead of creating new

**Rule:** Every entry in this index points to a REAL file in memory/. No phantoms. No duplicates.

---

**Owner:** Coco  
**Status:** ACTIVE — Phase 3 COMPLETE. RULES.md created. Consolidated all skills. Deleted 21 irrelevant files. Single source of truth established (RULES.md). Zero regressions.  
**Last Action:** Commit 2 (docs: delete irrelevant audit and draft files). Phase 3 testing complete.

