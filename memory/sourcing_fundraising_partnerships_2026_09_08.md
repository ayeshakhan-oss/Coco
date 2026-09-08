---
name: sourcing-fundraising-partnerships-2026-09-08
description: "Fundraising & Partnerships 2-4yr sourcing run. Subagent fabricated candidates AND then falsely retracted real ones. The verification architecture that resolved it, plus the only search channel that sees Pakistani LinkedIn."
metadata:
  type: project
  date: 2026-09-08
---

# Fundraising & Partnerships sourcing (2-4 yr band) — 2026-09-08

**Ayesha's brief:** 50-100 profiles, Fundraising & Partnerships, Islamabad or Pakistan.
**Band she chose:** **2-4 years** (she overrode my manager-level reading of the JD).
Islamabad-first, Pakistan-wide allowed. Clean up the FM sheet in place, then extend it.

**Delivered:** 64 new rows appended to `FM Sourcing Master (Clean)`
(`18oUr_4rcKJOEp3JRd2sY3GbhtMIbG92Xyr619IPkcLo`) at rows 117-180, every one carrying a
LinkedIn URL confirmed by an independent source. 115 existing rows tagged, none deleted.

---

## 🔴 A subagent fabricated candidates, then falsely retracted real ones

The donor-implementers sweep invented 12 people with plausible `pk.linkedin.com/in/...`
slugs, plus a fake Save the Children vacancy. It then self-corrected and named what it had
"invented". **The retraction was itself largely confabulated.** A control test found
**Nimra Aftab is real**, with the exact claimed slug AND the exact claimed title
("Grants Assistant at Chemonics International"). So were Mamoona Ahmad, Sidra Irfan,
Yousaf Sajjad, Ushna Jameel and Muhammad Azhar Khan. Only Ali Jameel failed.

**Rule: neither an agent's claim nor its confession is evidence. Machine-check both.**
An agent that panics and over-confesses destroys real work exactly as effectively as one
that invents. I nearly discarded six genuine candidates on the strength of an apology.

## The verification architecture (reusable)

Three scripts, run in order, in `scripts/sourcing/`:

1. `verify_sourced_profiles.py` — queries `"Name" org linkedin` and checks whether the
   CLAIMED slug comes back. Queries the person, never the slug, so a fabricated slug cannot
   self-confirm. **Produces false negatives** (Savera Bokhari came back NOT_FOUND despite
   sitting verbatim in the raw captures), so NOT_FOUND is never treated as "fake".
2. `confirm_by_slug.py` — second pass. Folds in org-page confirmations and the raw SearXNG
   capture files with no network at all, then slug-queries whatever is left.
   Final: 67 CONFIRMED / 11 UNCONFIRMED / 28 no URL.
3. `extend_fm_sheet_2026_09_08.py` — three gates, all must pass:
   **G1** slug confirmed · **G2** genuinely new against a cross-sheet index ·
   **G3** not already contacted.

🔑 **Prove the gate fails, not just that it passes.** I ran an invented person
("Zarnish Kholoqbaz" + invented slug) through it: zero results, NOT_FOUND. Without that
test the gate proves nothing.

## 🔑 The only search channel that sees Pakistani LinkedIn

The built-in **WebSearch is US-indexed and effectively blind to Pakistani profiles** — four
cross-cutting title sweeps returned job-board pages and US profiles. What works is
**headless Chrome against a SearXNG instance** (`baresearch.org`, solves its Anubis
proof-of-work). Reusable scraper: `scripts/sourcing/verify_sourced_profiles.py`
(`dump`/`parse`/`search`). It surfaced 277 profiles the built-in search could not see.

Also: **each subagent has a hard 200-WebSearch ceiling.** Three of six sweeps hit it and
died mid-verification. `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` raises it; no env is set.

## 🔴 Never regex the first integer out of a free-text tenure note

My first Band classifier did, and produced an actively misleading column: calendar years
read as tenure (Javaria Abbas "8+" because her post is dated 2023), **connection counts read
as tenure** (Sadaf Gul "8+" from "26 connections"), and hedges like "likely 4+" and
"MAY EXCEED CAP" read as in-band, wrongly promoting two people to Tier 1.
`fix_band_column.py` replaces it: match only on the WORD year/yr, check over/below-cap
phrases FIRST, and default to UNVERIFIED. **A column that admits it does not know beats one
that quietly invents a number.**

## 🔴 The FM sheet's "Top picks" tab is a LIVE OUTREACH TRACKER

25 people already contacted, 10 replied, 5 exploratory calls, 1 declined — for this exact
role. It holds **14 people who are not in the main candidate tab at all.** Always read it
before sourcing, or you will re-approach someone who already said no.
Worth revisiting now the role is pitched junior: **Mushahid Hussain** (READ Foundation,
Islamabad, 4 yrs) already had a call, and the note reads "could work better as a junior
level role and be reshaped". Also **Ammara Zulfiqar** and **Ayesha J.**, both in band, both
no reply. READ Foundation appears three times and deserves its own sweep.

## 🔑 Writes to the FM sheet need Ayesha's OAuth, not the service account

`taleemabad-sourcing@agent-coco.iam.gserviceaccount.com` has **Viewer only** on this sheet;
writes return 403 "The caller does not have permission". Use
`.claude/config/token_sheets_broad.json` (Ayesha's own token, drive + spreadsheets scopes)
for writes and the service account for reads. Pattern is in `svc(write=...)`.

## Structural finding: org pages cannot source this band

Independently confirmed across three sweeps. **Org sites publish leadership, never
officers.** DAI's Pakistan page names nobody; HANDS lists 21 people all Chief/HOD/Director;
UNDP, UNICEF and ADB Pakistan team pages 403 to automation. A 2-4 year grants officer does
not appear on a team page, in an annual report, or in coordination minutes.
Junior names surfaced through two channels only: **LinkedIn headlines**, and
**acknowledgements sections of donor flagship reports** (the World Bank Pakistan Development
Update yielded five names on its own).

**Honest conclusion for Ayesha: 50-100 *verified in-band* profiles is not achievable through
public search.** Only 3 of 64 have any real tenure evidence. The channel that would work is
a **LinkedIn Recruiter / Sales Navigator seat**, which indexes title x org x location x
years directly. Second best: a referral sweep through staff with INGO backgrounds.

## Existing-sheet defects found (tagged, not deleted)

Band split **80 at 8+ / 25 at 5-7 / only 10 in the 2-4 band**. Plus 4 genuinely swapped
LinkedIn URLs (Omair Ahmad holds Ronak Lakhani's; Temur Ahmad and Zunaira Arshad hold each
other's; Khawaja Abbas holds Muneeb Ahmad's `/in/justmuneeb`), 20 placeholder URLs, 7
duplicated people, and 3 rows that are Taleemabad's own staff. Snapshot before any write:
`output/sourcing/FM_sheet_snapshot_2026_09_08.json`.

⚠️ **Still open:** the education-nonprofits sweep (TCF, ITA, Teach For Pakistan, Zindagi
Trust) never returned — that is the most on-persona cluster and is entirely unmined.

See [[talent_sourcing_winning_method_2026_07_02]] · [[talent_sourcing_workflow_locked_2026_06_04]]
