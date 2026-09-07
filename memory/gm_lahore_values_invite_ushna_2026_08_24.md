---
name: GM-Lahore Values Invite (Ushna Fawad) + verified Lahore links + send-hook gap
description: Verified GM-Lahore values-interview invite links and CC list, the Karachi/Lahore booking-link trap, the duplicate-application pattern, and the discovery that Layer 3 send-time validation never actually fires.
type: project
---

# Values Interview Invite — Growth Manager - Lahore (Job 39) — Ushna Fawad

**Pilot** 2026-08-24 → **LIVE** 2026-08-31 to `ushna.fawad@gmail.com`
→ **she booked her Zero In call 2026-09-01.** Loop closed.
Script: `scripts/jobs/job39/send_gm_lahore_values_invite_ushna_pilot.py`

---

## 🔑 VERIFIED GM-LAHORE INVITE LINKS (reuse these, do not re-derive)

Each was fetched and its page `<title>` read on 2026-08-24 — this is how you prove
a link is the Lahore one and not the Karachi one:

| Var | URL | Verified title |
|---|---|---|
| `JD_LINK` | `https://drive.google.com/file/d/1ui-Y_jTr9xEkTHM3KH85q0ZvA16VreJJ/view?usp=sharing` | **Growth Manager Lahore** |
| `PREP_GUIDE_LINK` | `https://docs.google.com/document/d/1TBbBAimVX9PxSR6-rT13bLKf38itNdbp5v6EbWuDtkg/edit?tab=t.0` | Interview Prep Guide (role-agnostic) |
| `BOOKING_LINK` | `https://calendar.app.google/WMdp99dVmqPuuMvp9` | **Zero in Call for Growth Manager Lahore** |

**LIVE CC (same as the 8 Jul 2026 GM-Lahore batch):**
`ayesha.khan@` + `hiring@` + `waqas.tanveer@taleemabad.com`

## 🔴 TRAP — the repo's GM batch script is configured for KARACHI

`scripts/jobs/job39/send_growth_manager_invites_batch.py` lives in the **job39**
folder but its constants are **Job 41 / Karachi** (`POSITION = "Growth Manager -
Karachi"`, a different JD file and a different appointment schedule). Copying it
for a Lahore candidate silently books them into the Karachi schedule.

The correct Lahore reference is `scripts/send_growth_manager_values_invite_pilot.py`
(despite the generic filename — its docstring says JOB-0039). **Never trust the
folder or the filename; confirm the links by fetching them.** The 8 Jul 2026 live
batch is the ground truth for what GM-Lahore candidates actually received.

## Position label

The 8 Jul Lahore batch used bare **"Growth Manager"**. With two GM roles now live,
this send used **"Growth Manager - Lahore"** — matches the Markaz job title and the
Karachi convention. Ayesha did not object; treat "- Lahore" as current.

## 🔴 Duplicate application (the Kanooz pattern again)

Ushna existed **twice** on the same job 39:
- candidate **2987** / app **3703** — LinkedIn Quick Apply stub, no CV,
  **rejected 2026-07-09**, `rejection_reason` null.
- candidate **3349** / app **4141** — real application with CV, 2026-08-13, `new`.

Same person (identical LinkedIn URL `linkedin.com/in/ushnafawad/`). Always search
candidates by **name AND phone AND LinkedIn URL**, never just the invited email.
A prior silent rejection on the same job is worth flagging before inviting.

She was also still `status='new'` (never screened/shortlisted) when invited — every
other GM-Lahore invitee was `shortlisted`. Ayesha invited her deliberately; flag the
pipeline-state mismatch rather than blocking on it.

## 🔴 HARNESS GAP — Layer 3 send-time validation never fires

`scripts/hooks/pre_send_validation_hook.py:104`:

```python
if not ('safe_sendmail' in tool_name.lower() or 'send' in tool_name.lower()):
    return 0  # Not an email send
```

The hook is registered in `.claude/settings.json` under `PreToolUse` **matcher
"Bash"**, so `tool_name` is always literally `"Bash"` — which contains neither
"safe_sendmail" nor "send". **It returns 0 on every invocation and validates
nothing.** CLAUDE.md advertises this layer as "✅ ACTIVE"; it is not.

Consequence: the `[PILOT]`-prefix-in-live guard and every other send-time check are
dead for script-based sends. Layers 1 and 2 (template injection, pre-flight
checklist) still work. **Not yet fixed — raised with Ayesha 2026-08-24.**
The fix is to match on `tool_input.command` contents, not `tool_name`.

## Design self-check used

Diff the generated HTML against the locked reference's `build_html()` — the only
lines that should differ are the position label. Plus: 775px card, `#f5f5f5`
page / `#e5e7e2` wrapper / `#3157b7` header / `#3d63c8` links / `#5b3fc4` single
CTA, Georgia-only stack, 34px CID logo, recording-consent callout, table-based.
⚠️ A naive "no Inter font" grep false-positives on the word "Int**erview**".
