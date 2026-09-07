# RM Internal Case Study Round (2026-09-02)

Regional Manager, internal-only round. 25 staff submitted a case study + updated resume
to hr@ (deadline extended 27 Aug -> 28 Aug). All 25 read, anonymised, scored.

## Artefacts
- Benchmark answer key (Rev 2, QA'd by Ayesha BEFORE any submission was opened):
  `docs/case_studies/benchmarks/rm_regional_manager_benchmark.md`
- Evaluation report markdown: `docs/case_studies/rm_evaluation_report_2026_09_02.md`
- Google Doc report: https://docs.google.com/document/d/1suHQOhKzAjjBe26uPjSpHkl0EoSVBGqkhtReqjs8QMc
- Artifact report: https://claude.ai/code/artifact/4087b35c-19a1-469e-a257-19ec051fe1f2
- Tracker sheet (Submissions + Scores tabs): `1xtQxfblMXmA5IpnvnABkK5bvmhPMK5_Q6Z1wDiI59A8`
- Drive: "RM Internal Hiring 2026" > Case Studies (Anonymised) + Resumes (NAMED)

## Headline result — AFTER THE STRICT RE-MARK (this is the live result)
🔴 The FIRST pass was wrong. It put all 25 above 70 (mean 88.3) because the marking scale
had a 20% floor and never used its bottom half. Ayesha challenged it; a strict re-mark on the
full 0-5 scale against the SAME benchmark gives **mean 75.0, range 56-100, 8 of 25 below the
70% line**. Spread widened 30 -> 44 points. See
[[lesson_scoring_anchor_floor_inflation_2026_09_02]] for the cause and the standing rule.

**Top five (89+, the only clean break):** Syed Ateeb Ali 100 · Danish Iqbal 100 · Moiz Khan 95 · Warda Kiani 92 · Meerab Din 89
**Below the 70% line (8):** Muhammad Salman, Javeria Nayyab, Toseef ur Rehman, Sana Nawaz, Hafsa Bashir, Areej Noshad, Khadija Akbar, Rida Abbas
The 70% was announced to staff and now does real work — apply it as published.
Report + candidate-detail PDF emailed to Ayesha 2026-09-02; script
`scripts/reports/send_rm_case_study_remark_report.py`; strict scores in scratchpad
`strict_scores.json` (with per-candidate anchors, caps fired, notes, strengths, gaps).

## Rules this round confirmed
1. **Anonymisation is harder than it looks.** Names split across docx runs
   (`S|hafaq T|ahir`) - JOIN runs before replacing, never replace tag-by-tag with a space
   (that re-breaks the words and produces false "clean" verdicts).
2. **python-docx `.paragraphs` does NOT reach text boxes** (`w:txbxContent`). Iterate
   `doc.element.body.iter(qn('w:t'))`. A real leak (RM-04 cover page) hid exactly there.
3. **Never deny-list a surname out of the scan** because it collides with a common word
   ("Din"). Scan it, then review contexts. Second real leak found this way.
4. `(?![a-z])` under `re.IGNORECASE` also matches uppercase - use `(?!(?-i:[a-z]))`.
5. **Verify by plain substring first, review contexts by hand.** Clever regex produced
   three compounding false negatives before the two real leaks surfaced.
6. Residual limit worth stating to the hiring manager: candidates self-identify through
   the SUBSTANCE of answers (region, tenure, their own experiments). Stripping that would
   destroy the evidence that makes the answer strong. Anonymity is partial by design.
7. **Codes assigned by md5-of-name** so code order carries no signal; names attached to
   scores only AFTER every score was final.

## Scoring craft
- Score writer must be atomic + utf-8 + `ensure_ascii=True`: a `UnicodeEncodeError` on
  cp1252 `write_text` TRUNCATED scores.json to 0 bytes and lost 7 records. Pattern:
  write to `mkstemp` in the same dir, `os.replace`.
- Q10 was banded (Standout/Meets), NOT scored - it is in no total. Open decision.
- Where a candidate reached a DIFFERENT conclusion and defended it with case data, it
  scored as high as agreement.
- Flagged my own calibration risk: mean 88 is high and I am a single unmoderated marker.
  Recommended a second reader re-score the 83-86 shelf and the one sitting on 70.

## Open decisions for Ayesha
1. Where the shortlist cut falls. 17 clear 70; the only honest break is at 89+ (five people).
   85 down to 70 is a continuous slope.
2. Two integrity items flagged to Ayesha, both HER call, neither affecting scores:
   RM-09/RM-15 share distinctive phrasing in matching positions and identical derived figures
   (21 not 15, 91%, 98%); RM-23 quotes internal Slack/RUMI with channel names and dates.
3. Whether Q10 carries points (totals would need rebuilding).
4. Two benchmark items: the `+25%` denominator (HITL-only 6.25pp vs HITL+DC 11pp), and
   adding RM-09's region-as-allocation-variable distinction.
5. Still outstanding: chase RM-04 Shafaq Tahir for her missing resume.

See also [[feedback_benchmark_and_report_hygiene_2026_08_17]] - benchmark before
submissions, no candidate names in the answer key, reports carry candidate assessment
not internal-process narrative.

## Debrief invites sent (2026-09-07)
17 invites live to everyone at or above the published 70% bar on the STRICT re-mark
(Ayesha rejected the first, inflated marking; see
[[lesson_scoring_anchor_floor_inflation_2026_09_02]]). Script:
`scripts/send_case_study_debrief_rm_internal_pilot.py` - Skill 06 type #2, locked design,
body copy cloned verbatim from the SMG batch-2 send with ONE substitution: that batch linked
a role walkthrough VIDEO, this one links the RM **job description** (the doc from the
2026-08-20 internal announcement), because no video exists for RM.

- Booking link `calendar.app.google/w8WJ3GEmVNYUQztL8` supplied fresh by Ayesha. NOT reused
  from either SMG batch - Rule 22.
- CC (Ayesha, verbatim, and NOT the SMG list - Waqas out, NIETE people in):
  ali.sipra@taleemabad.com, asma.zaheer@niete.edu.pk, bilal@niete.edu.pk,
  hiring@taleemabad.com, ayesha.khan@taleemabad.com
- Deliberately NOT in the email because she never supplied them: duration, panel names,
  booking deadline. The locked "at your earliest convenience" line needs none of them.
- Batch spans 100 down to exactly 70 and every email is byte-identical except the first
  name, so nothing signals a placing.

**Name lesson (extends Rule 22).** We held "Syed Ateeb Ali"; he signs "Ateeb Ali" on all 10
of his own emails. Syed is a patronymic, not part of the name he uses. Greeting went out as
"Hi Ateeb," with the full formal name kept in the subject. Flagged to Ayesha twice, no
objection. **Check the From display name on the person's OWN mail before any batch greeting.**

**Verification pattern that worked** (do this every batch): per-recipient IMAP scan of
ayesha.khan@ Sent Mail BEFORE drafting (0 prior debrief invites to any of the 17) and AGAIN
after (exactly 1 live each, correct CC on all 17, no PILOT prefix leaked, 0 of the 8
below-70 wrongly invited). Console output alone cannot prove either.
