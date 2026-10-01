---
name: niete-cpd-coaches-aliya-adnan-2026-10-01
description: Two NIETE CPD Coach packages built and sent live on 1 Oct 2026 (Aliya Fehmi, Adnan Ali Abid) through the shared NIETE pipeline; how the evidence was gathered, the CC lists Ayesha chose, and how CC addresses were verified.
metadata:
  type: project
---

# NIETE CPD Coaches: Aliya Fehmi + Adnan Ali Abid (LIVE 2026-10-01)

Both built with `scripts/contracts/niete_cpd_common.py` (`load_candidate(slug)` → `build_contract` / `build_nda` → `to_pdf`), sent with `scripts/contracts/send_niete_email_design3.py --who <slug>`. Candidate PII (CNIC, salary split, email) lives ONLY in gitignored `data/contracts/niete_cpd_candidates.json` under slugs `aliya` and `adnan`, with a full evidence note per person.

| | Aliya Fehmi | Adnan Ali Abid |
|---|---|---|
| Markaz | app 3858 / cand 3123 (Job 17) | app 4516 / cand 3652 (Job 17) |
| Term | 2 Oct → 31 Dec 2026 | 12 Oct → 31 Dec 2026 |
| Reports to | **Bushra Karim** (Ayesha changed it from Hasnat Tariq after pilot 1) | Abdul Waheed |
| Salutation | Ms. | Mr. |
| Acceptance | written, 1 Oct | **implicit only** (CNIC via Markaz form, no reply) |
| Live CC | hiring@, bushra.karim@niete.edu.pk, hr@ | hiring@, hr@, ayesha.khan@, ali.sipra@, abdul.waheed@niete.edu.pk |
| Returning | no | no |

Both: CPD - Coach, signed Ali Sipra COO, 90/9/1 split, lunch + business-travel clauses removed, standard CPD JD, Permanent NDA (no CNIC). Each had a pre-send AND post-send IMAP Sent scan: exactly one live send, correct Cc, two PDFs.

## How the evidence was found (repeatable)
1. **Markaz `contract_drafting_*` fields were NULL for both**, though both had submitted. The truth is the internal email "📋 Contract Information Submitted - <Name> - CPD Coach" in Ayesha's mailbox (Rule 18 again). Read it over read-only IMAP.
2. Offer letter = "Offer Letter CPD Coach - at Taleemabad | <Name>" from hr@; read the thread to the end for a counter (Rule 19). Neither countered.
3. Start date, line manager and salutation were **in no source**; asked Ayesha each time. The RM varies per region: Aliya's tech call CC'd Asma Zaheer, her pilot said Hasnat Tariq, and the final answer was Bushra Karim. **Never infer the RM from who CC'd an interview.**
4. Name check (Rule 22): Aliya's Gmail display name is "Aaleyah Baig", but she signs "Aliya Fehmi" and the CNIC form agrees.

## 🔴 Resolve every CC from the mailbox, never from a first name
Ayesha said "waheed". The mailbox holds **abdul.waheed@niete.edu.pk** (123 msgs, he sent 22, latest 28 Sep 2026) and a stale **abdul.waheed@niete.pk** (last Jan 2025), plus an unrelated Rizwan Waheed. Pick the address the person actually SENDS from most recently. Ali Sipra = ali.sipra@taleemabad.com.

## Mechanics learned
- `send_niete_email_design3.py --who` now takes any slug in the candidate file (the hand-kept choices list had to be edited for every new coach).
- `pre_contract_send_hook.py` fires on ANY Bash command containing `contracts/send_`, even `sed`. Read those files with the Read tool.
- Rendering the Drive PDF pages with PyMuPDF and reading the PNGs is real visual proof; do it before every pilot.
- `scripts/contracts/` is still gitignored by `.gitignore:76 Contracts/` (case-insensitive), so none of this code is in git.

Related: [[joining-email-two-links-by-entity]] · [[niete-cpd-coach-contracts]] · [[opl-permanent-contract-and-joining-email]]
