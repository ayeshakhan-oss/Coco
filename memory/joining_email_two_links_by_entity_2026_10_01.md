---
name: joining-email-two-links-by-entity
description: Every joining email carries BOTH links (signed-documents form + all-employee WhatsApp group); the form is chosen by ENTITY - NIETE/NIETE fellowship vs OPL/OWT/their fellowships. Inc. has no form.
metadata:
  type: project
---

# Joining emails: two links, always, form by entity (Ayesha 2026-10-01)

Every joining / contract email carries two links, whatever the engagement:
1. **Submit your signed documents** (the onboarding form for the signed contract, signed NDA and their documents)
2. **Join the WhatsApp group**: `https://chat.whatsapp.com/HglkfuENmLqEbaq8N5jSVq` (all employees)

**The form follows the ENTITY, not the programme:**
- NIETE + NIETE fellowships → `https://docs.google.com/forms/d/e/1FAIpQLSdVAYfCZZhusF_tNLn7mxzoK5BFXDa7xfj2FZifRlva-YDBHQ/viewform`
- OPL, OWT + OPL/OWT fellowships (incl. permanent hires) → `https://docs.google.com/forms/d/e/1FAIpQLSf70SM4jlx4muDMLlN1ZMqHqVEQjJQgCBga-oRM-M1OZXCePw/viewform?usp=sharing&ouid=108638480093303713396&urp=gmail_link`
- Inc. → none given. Ask; never borrow another entity's form.

**Why:** the old rule split forms by programme (Fellow vs NIETE), so permanent OPL hires got no form at all (Ahmad Wajahat, Marzia Khandwala, 2026-09-12 went out with neither link). The harness only checked links when the body said "click here", so Design 3 button emails were never checked.

**How to apply:**
- Both Design 3 templates now carry `{{ONBOARDING_FORM_URL}}` + `{{WHATSAPP_GROUP_URL}}` buttons; the form button reads "Submit your signed documents" (was "Complete the onboarding form").
- `contract_docx_eval.evaluate_joining_email` HARD BLOCKS a missing form, a missing WhatsApp link, or the wrong entity's form on every joining email. The entity is inferred from whether "niete" appears in the body.
- Web app: `joining_email.links_for(entity)` + `check_body(..., entity=)`; Inc. raises.
- ⚠️ `pre_contract_send_hook.py` fires on ANY Bash command naming `contracts/send_`, even a `sed` read. Read those scripts with the Read tool.

Related: [[opl-permanent-contract-and-joining-email]] · [[contract-email-design3-standard]]
