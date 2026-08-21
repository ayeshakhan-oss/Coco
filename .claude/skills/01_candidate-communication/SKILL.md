---
name: candidate-communication
description: Handle all candidate rejection, feedback, and status-update emails. Covers CV rejections, values interview feedback, warm bench feedback, GWC rejections, and warm-hold decision-pending updates (interviewed, decision pending, dated follow-up promised). All emails require 800+ words (if feedback; decision-pending updates are 120-250 words), evidence-based feedback, v8 HTML design, and pilot approval before sending.
compatibility: Requires memory/feedback_email_rules.md, locked templates, RULES.md
---

# Candidate Communication

Send personalized rejection and feedback emails to candidates across all interview stages.

---

## Architecture

**This skill is an orchestration layer** that references the detailed SOPs in `SOPs/01_Candidate_Communication/`. 

- **SKILL.md (this file):** Master orchestration, universal rules, execution discipline
- **SOPs folder (source of truth):** Detailed procedures for each email type

When you use this skill, you get:
1. Universal rules and checklist (from this SKILL.md)
2. Detailed procedures (from linked SOPs — the source of truth)

**Important:** SOPs are maintained as the single source of truth. If procedures change, they update in SOPs/ and are automatically reflected here.

---

## When to Use This Skill

Trigger this skill when:
- User asks to "send rejection email to [candidate]"
- User wants to "write feedback for [candidate]"
- User requests "warm bench email" or "values feedback"
- User needs "GWC rejection" or interview stage feedback
- Any candidate communication requiring evidence-based, personalized feedback

---

## Related SOPs (Source of Truth)

**Location:** `SOPs/01_Candidate_Communication/`

This skill orchestrates the following detailed procedures:

All these SOPs fall under this skill:

1. **CV Rejection Emails** — `SOPs/01_Candidate_Communication/cv_rejection_emails.md`
   - 800+ words, CV-based evidence
   - Structure: opening → impressed → gap → close
   - Format: v8 HTML template

2. **Values Feedback Emails** — `SOPs/01_Candidate_Communication/values_feedback_emails.md`
   - 800-1100 words MANDATORY
   - 3 sections: What We Liked / Questions / Next Steps
   - Interview evidence required, no em dashes

3. **Warm Bench Feedback** — `SOPs/01_Candidate_Communication/warm_bench_feedback_email.md` / `memory/warm_bench_locked_rules_2026_05_30.md`
   - 800-1100 words MANDATORY (Haroon Yasin framework)
   - 4 sections + P.S.: "What Stayed With Us" / "Here's the Honest Part" / "Where We Want to Leave This"
   - Poetic subject line tied to specific interview moment
   - NO interviewer names, NO internal jargon (GWC/values/scorecard), NO comparative language
   - Avoid recruiting abstractions (see memory/candidate_communication_avoid_recruiting_abstractions_2026_05_30.md)

4. **GWC Rejection Emails** — `SOPs/01_Candidate_Communication/gwc_rejection_emails.md`
   - Warm-tone rejections for GWC-cleared candidates
   - Interview transcript analysis
   - No "GWC" or "KCD" terminology

5. **Warm Hold — Decision-Pending Updates** — `warm-hold-decision-pending-email.md` (this folder) — ADDED 2026-08-12
   - Candidate interviewed, decision NOT yet made (still collecting panel notes); we commit to an update BY A STATED DATE (e.g. "next week")
   - SHORT: 120-250 words. NOT a feedback email — no verdict, no evaluation, no direction-hints
   - 🔓 TYPE-SPECIFIC EXEMPTIONS (Ayesha 2026-08-12): NO "This is not a yes for now." opening (no decision exists); the dated "we will reach out by [date]" promise is REQUIRED here (the one type where the future-promise ban is inverted); 800-word minimum does not apply
   - Only commit to dates we will honour; if no reliable date exists, use the Keep-in-Touch Note (Skill 06 #5) instead
   - Everything else unchanged: "we" voice, no em dashes, no jargon, no interviewer names, v8 layout, pilot to Ayesha first

6. **Case Study Update — Debrief-Pending** — `case-study-update-email.md` (this folder) — ADDED 2026-08-13
   - Case study SUBMITTED, debrief decision pending. 120-250 words, dated promise REQUIRED, same exemptions as type 5
   - "case study" is permitted candidate-facing language for THIS type only

7. **Internal Announcement** — `internal-announcement-email.md` (this folder) — ADDED 2026-08-20
   - 🔴 **AUDIENCE IS TALEEMABAD STAFF, NOT CANDIDATES.** Internal broadcast: internal job openings, new joiners, new programmes, org changes
   - SHORT: 150-400 words. Content varies per send (written or approved by Ayesha); the LAYOUT is what is locked
   - 🔓 DISAPPLIED (internal audience): 800-word minimum · "This is not a yes for now." opening · future-promise ban · no-names ban · candidate-jargon ban · feedback widget
   - ✅ STILL ENFORCED: no em dashes · v8 layout imported from `v8_template.py` · collective voice · `safe_sendmail()` · pilot to Ayesha first · clean subject live · no fabricated facts, no guessed distribution lists
   - Eyebrow `EYEBROW["announcement"]` reads "INTERNAL ANNOUNCEMENT" as a visible tripwire if it ever reaches an external inbox
   - Script: `scripts/send_internal_announcement_pilot.py` (keep `announcement` in the filename; never `warm_bench`/`gwc`/`values`/`rejection`)

---

## Universal Rules (All Communication)

**Word Count:**
- Minimum: 800 words (non-negotiable for feedback/rejection types 1-4)
- Target: 800-1100 words (optimal)
- Exception: Warm Hold decision-pending updates (type 5) target 120-250 words — they carry no feedback
- Verify count before sending

**Tone & Voice:**
- "We" voice (never "I")
- They/them pronouns (gender-neutral)
- Emotionally careful, warm
- Specific evidence from interview (never generic)
- **NO EM DASHES (—)** — Replace with periods, commas, colons, or hyphens only

**Opening Line & Future-Promise (LOCKED 2026-06-18 — ALL 4 decision types; type 5 Warm Hold is EXEMPT per Ayesha 2026-08-12, see its file):**
- **MANDATORY first line** after `Dear [Name],`: `This is not a yes for now.` Harness HARD BLOCK if missing or buried after a heading. Honest because of "now" (today's no, not never). Master philosophy Rule 10.
- **NO future-outreach promise.** Express welcome as disposition + candidate-initiated ("if a closer-fit role opens, we would welcome a fresh application from you"). NEVER "we will reach out / be in touch / contact you / keep your name on file / expect to hear from us." Harness WARNING. Master philosophy Rule 11.

**Format:**
- v8 HTML design (blue headings, Georgia serif, justified)
- No em dashes (replace with period/comma/colon)
- Feedback widget required
- Logo, header block, footer with signature

**Pilot Rule (STRICT):**
- Always pilot to Ayesha first
- For values feedback: pilot to Ayesha + Jawad ONLY
- Never include candidate in pilot
- Wait for approval before going live
- Subject line (PILOT ONLY): "[PILOT – Candidate Name] [Original Subject]"
- **CRITICAL:** Remove "[PILOT – ]" prefix BEFORE sending live email to candidate
- **NEVER send live email with [PILOT – ] in subject line to candidate**

**Self-QA Before Sending:**
- [ ] Memory checked (MEMORY.md)
- [ ] Locked template read side-by-side
- [ ] Word count verified (800+ for all types)
- [ ] Every claim cited from CV or interview
- [ ] Format matches locked standard
- [ ] Pilot sent to Ayesha (never direct)
- [ ] All special characters as HTML entities
- [ ] No discrepancies vs RULES.md

---

## WARM BENCH EMAILS — LOCKED RULES (2026-05-30)

**Reference:** Fatima Saeed warm bench email (May 15, 2026) — This is the gold standard for tone and structure

**Critical Requirements:**

### 1. OPENING LINE (MANDATORY)
```
This is not a yes for now.

But we need to tell you something about what we saw in your interview 
that the panel kept discussing afterward...
```
Never deviate from this opening.

### 2. NEVER MENTION INTERVIEWER NAMES
- ❌ "During your values conversation with Jawwad Ali on April 6..."
- ✅ "You described a moment in your interview where..."
- ✅ "When we asked about X, you said..."

**Why:** Keeps focus on candidate, not on who interviewed them. More universal.

### 3. HEADING STRUCTURE (EXACT — UPDATED May 15, 2026)
```
What Stayed With Us
Here's the Honest Part
Where We Want to Leave This
```
Use these three headings exactly. No variations.

### 4. NEVER USE INTERNAL JARGON
❌ FORBIDDEN: "values interview", "GWC interview", "values scorecard", "case study", "KCD", "warm bench"
✅ ALLOWED: "your interview", "when we asked you about...", "the moment you described...", "during our conversation"

**Why:** Jargon feels internal. Candidates don't know these terms. Use human language.

### 5. AVOID RECRUITING ABSTRACTIONS (CRITICAL)
See `memory/candidate_communication_avoid_recruiting_abstractions_2026_05_30.md` for complete guidance.

❌ Never use: "good candidate", "strong candidate", "impressive profile", "strong background", "capable person", "excellent fit"

✅ Instead describe: Observed behaviors, character traits, demonstrated strengths
- Instead of: "Your profile and background are genuinely strong"
- Say: "The way you identify gaps, take initiative without being asked, and follow through even when it's hard—that showed up consistently"

### 6. DON'T QUOTE FEEDBACK DIRECTLY
❌ "The hiring manager feedback states: 'Communication could be more energetic and proactive.'"
✅ "What showed up was someone who sees problems clearly, cares about people inside the resistance, and doesn't let discomfort be an excuse to stop."

**Pattern:** Take the feedback intent, reframe it as observation of WHO THEY ARE, use positive language that affirms character.

### 7. NEVER MENTION "ANOTHER CANDIDATE"
- ❌ "Another candidate's background was a tighter fit"
- ❌ "Someone else's experience profile matched better"
- ✅ "We're moving into a specific phase where we need X capability"
- ✅ "It's about fit between your strengths and our immediate strategic need"

**Why:** Demotivates candidates. Makes them feel they "lost" to someone.

### 8. DECISION RATIONALE MUST BE CONCRETE
- ❌ Vague: "situational, narrow, timing, specific moment needed"
- ✅ Concrete: "These decisions are sometimes incredibly narrow and situational. We have one role. We made a choice that reflected something very specific about what we thought this moment needed. It wasn't about you not being right for the position. It was about us making a decision that, in the end, pointed somewhere else."

### 9. TONE CHECKLIST
- [ ] "We" voice (never "I")
- [ ] Warm + observational (not clinical)
- [ ] Specific interview moments (never generic)
- [ ] No prescriptive advice ("You should...")
- [ ] No life-coach language
- [ ] Vulnerable (show company's perspective, not just candidate's gap)
- [ ] Poetic (P.S. ties back to powerful moment)

### 10. LOGO EMBEDDING (REQUIRED — LOCKED 2026-05-30)
**Never use external URL for logo.** Always embed directly using cid: content ID, **centered in the middle of the header**.

**HTML (EXACT):**
```html
<img src="cid:logo_taleemabad" width="48" height="48" alt="Taleemabad" style="display:block; margin:0 auto 20px auto; border-radius:0;" />
```

**Styling Requirements:**
- `display:block; margin:0 auto` — Centers logo horizontally
- `width:48; height:48` — 48x48px size (full visibility, no clipping)
- `border-radius:0` — No rounding (preserves complete logo)
- `margin-bottom:20px` — Space from title

**Python:** Attach logo from `assets/logo_taleemabad.png` using MIMEImage with Content-ID header.

**Why:** External URLs fail in Gmail, Outlook, corporate networks. Embedded images render reliably everywhere. Centering ensures proper header alignment.

### 11. SIGNATURE FORMAT (EXACT — LOCKED 2026-05-30)
```
Warm regards,
People and Culture Team
Taleemabad

hiring@taleemabad.com | www.taleemabad.com
```
*(The "Sent on behalf of Talent Acquisition Team by Coco" line was REMOVED from all emails per locked rule 2026-07-29 — never re-add it.)*
**Never deviate.** Use exact HTML structure and CSS classes from memory/warm_bench_final_locked_approach.md. Blue links (#2f4fa2). Simple <div> structure with class-based styling.

### 12. SECTION STRUCTURE
**Section 1: What Stayed With Us**
- 2-3 specific interview moments
- Show what impressed the panel
- Use "the panel kept discussing this afterward"
- Affirm character, not just competence

**Section 2: Here's the Honest Part**
- Acknowledge the interview was strong
- Include positive observations from scorecard (warmly integrated, not quoted)
- Explain the decision was narrow/situational
- Don't apologize; be matter-of-fact
- Frame as "timing didn't align" not "you weren't good enough"

**Section 3: Where We Want to Leave This**
- Warm bench positioning (genuine, not obligatory)
- Express interest in future connection
- Affirm the kind of person they are
- End with warmth, not finality

**P.S.: The Powerful Echo**
- Reference ONE powerful moment from interview
- Tie it back to who they are
- Emotional, brief, memorable
- Candidate should screenshot this part

### 13. HAROON YASIN BALANCE RULE (CRITICAL)
See `memory/candidate_communication_quality_review_protocol_2026_05_30.md` for complete guidance.

**Count specific praise examples vs. specific decision rationale examples.**
- These counts should be equal or nearly equal
- If praise examples = 3 stories, decision explanation should have ~3 equally concrete details
- **Prevents the paradox:** "If you valued all this, why wasn't I selected?"

**Test:** Could the candidate reasonably conclude "If they believed all this, why wasn't I selected?"
- If yes: Your praise-to-decision ratio is imbalanced. Rebalance by increasing decision specificity.

---

## CANDIDATE COMMUNICATION QUALITY REVIEW (10-Point Checklist)

Before sending ANY rejection, warm bench, GWC, or feedback email, run this checklist:

**See `memory/candidate_communication_quality_review_protocol_2026_05_30.md` for detailed guidance.**

- [ ] **Balance of Evidence:** Is praise specificity equal to decision specificity?
- [ ] **Avoid Generic Labels:** Replace "good candidate", "strong profile" with observed character
- [ ] **Concrete Feedback:** Is any feedback vague? Make concrete or remove.
- [ ] **Endorsement Level Test:** Would candidate think "if you valued all this, why wasn't I selected?"
- [ ] **Evidence Support:** Is every compliment earned through specific observations, not generic praise?
- [ ] **Emotional Arc:** Does email flow through all 4 elements? (understand decision / why / what was valued / dignity)
- [ ] **Character Over Assessment:** Replace evaluative labels with character observations
- [ ] **Haroon Yasin Balance:** Praise examples ≈ Decision examples (count them)
- [ ] **Concrete Decision Rationale:** Is the "why not" as specific as the "what we saw"?
- [ ] **Final Test:** "Would I feel SEEN (not SCORED) if I received this?"

**If any item fails:** Do not send. Fix and re-check before piloting to Ayesha.

---

## Execution Discipline

**STEP 1: IDENTIFY EMAIL TYPE**
- Ask if unclear: "What type of feedback email?"
- Options: CV rejection, values feedback, warm bench, GWC rejection, warm-hold decision-pending update

**STEP 2: READ LOCKED RESOURCES**
- RULES.md: Core Discipline Rules 1-7
- RULES.md: Skill-Specific Rules (Skill 2 or 3)
- MEMORY.md: Specific SOP for that email type
- Locked template: v8 design or Haroon framework

**STEP 3: READ SOURCE MATERIAL**
- Full CV (for CV rejections)
- Full values interview notes (for values feedback)
- Full GWC interview transcript (for GWC rejections)
- Find specific moments/quotes to cite

**STEP 4: WRITE ONCE, CORRECTLY**
- Single-pass correctness (no iteration)
- Evidence in every section (not generic)
- No fabrication (quote actual text)
- Maintain "we" voice, they/them pronouns

**STEP 5: RUN 8-ITEM CHECKLIST**
- All 8 items must pass
- If any fail: fix and re-check
- Don't send without all 8 passing

**STEP 6: PILOT & APPROVE**
- Send pilot to Ayesha (+ Jawad for values feedback)
- Wait for explicit approval
- Switch PILOT_MODE = False
- Send live to candidate (TO) + hiring@taleemabad.com (CC)

---

## Common Mistakes (Do Not Repeat)

| Mistake | Why It's Wrong | Fix |
|---------|---|---|
| Word count <800 | Lacks depth, feels generic | Expand with specific moments, reach 800 |
| Generic praise | "You showed good skills" without evidence | Quote actual CV or interview moment |
| No interview citations | Looks AI-generated | Include specific quotes, timestamps, moments |
| "I" voice | Breaks consistency | Use "we" (People & Culture team) |
| Em dashes in body | Looks AI-generated | Replace with period, comma, or colon |
| Missing sections | Incomplete feedback | Include all 3 (likes/questions/next) |
| Sending to candidate in pilot | Violates approval process | Pilot ONLY to Ayesha/Jawad |
| Wrong HTML format | Misaligned with locked design | Print template, match exactly |
| Prescriptive advice | "You should take a course..." | Frame as observation, not prescription |
| No feedback widget | Missing engagement mechanism | Add widget code before final send |
| Mentioning interviewer names (warm bench) | Makes email about interviewer, not candidate | Remove names; use "during your interview" |
| Using internal jargon (GWC, values, scorecard) | Candidate doesn't know these terms | Replace with "your interview" or "our conversation" |
| Quoting scorecard feedback directly | Feels clinical, not warm | Integrate warmly as observations |
| Comparing to other candidates | Demotivates, makes candidate feel like they "lost" | Focus on YOUR needs, not their vs. another |
| Recruiting abstractions ("strong candidate") | Sounds generic, not personal | Describe observed behaviors and character traits |
| Imbalanced praise-to-decision ratio | Candidate feels "if you valued all this, why not me?" | Make decision rationale as specific as praise |
| Vague decision explanation | Candidate doesn't understand why | Use Fatima-style concrete: "We have one role. We made a choice that reflected something very specific..." |
| Em dashes (—) in email | Violates SOP, looks AI-generated | Replace ALL em dashes with periods, commas, colons, or hyphens only |

---

## Success Criteria

✅ Email is 800+ words (verified count)  
✅ Every observation cites CV or interview moment  
✅ "We" voice, they/them pronouns throughout  
✅ No em dashes (replace with period/comma/colon)  
✅ HTML matches v8 locked design  
✅ Pilot sent to Ayesha first  
✅ All 8-item checklist items pass  
✅ No generic language or assumptions  
✅ Feedback widget included  

---

## Resources & Templates

**Locked Templates:**
- v8 Email Design: `memory/_locked/locked_templates_index.md`
- Warm Bench Framework: `memory/_locked/warm_bench_final_locked_approach.md` (May 5, 2026 — SUPERSEDED by May 15 rules below)
- Interview Invite Design: `memory/_locked/locked_email_template_interview_invites.md`

**CRITICAL WARM BENCH RULES (2026-05-30 — LATEST):**
- `memory/warm_bench_locked_rules_2026_05_30.md` — 10 locked rules + Fatima Saeed reference (May 15, 2026)
- `memory/candidate_communication_quality_review_protocol_2026_05_30.md` — 10-point checklist + Haroon Yasin balance rule
- `memory/candidate_communication_avoid_recruiting_abstractions_2026_05_30.md` — Critical guidance on character-focused language

**Reference Scripts:**
- Job 36 values feedback: `scripts/jobs/job36/send_job36_values_feedback_junaid_jawad_formatted.py`
- Warm bench: `scripts/warm_bench_locked.py`
- Huma Mumtaz warm bench (reference): `scripts/warm_bench_huma_mumtaz_pilot.py`

**Rules:**
- Core Discipline: `RULES.md` (Rules 1-7)
- Skill 2 (Rejection Emails): `RULES.md` (lines 170-201)
- Skill 3 (Warm Bench): `RULES.md` (lines 204-251)
- Candidate Communication Quality Review: `memory/candidate_communication_quality_review_protocol_2026_05_30.md`

---

## Commit to Discipline

I will send candidate communication emails with:
- ✅ 800+ words (verified count)
- ✅ Specific interview or CV evidence (never generic)
- ✅ "We" voice, they/them pronouns
- ✅ v8 HTML design (locked format)
- ✅ Pilot to Ayesha first (never direct)
- ✅ All 10-item checklist items passing (quality review protocol)
- ✅ Haroon Yasin balance rule applied (praise ≈ decision specificity)
- ✅ No recruiting abstractions (character-focused language only)
- ✅ Warm bench: No interviewer names, no jargon, no comparative language, correct headings
- ✅ No em dashes, no fabrication, no prescriptive advice

**Status:** ✅ PRODUCTION READY — Updated 2026-05-30 with Fatima Saeed (May 15) locked rules, quality review protocol, and recruiting abstraction guidance
