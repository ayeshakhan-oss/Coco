---
name: Warm Bench Feedback Email LOCKED (2026-05-04)
description: Generic locked script + template for warm bench rejection emails. Parameterized for any position. Design specification frozen.
type: feedback
status: LOCKED & PRODUCTION READY
originSessionId: b6db7e16-8b9a-492c-9573-abe2f11c03cd
---
## Status: LOCKED & PRODUCTION READY (2026-05-04)

Warm bench feedback emails are now fully locked with a generic, reusable script and frozen design template.

## Locked Assets

### 1. Script: `scripts/warm_bench_locked.py`

**Location:** `c:\Agent Coco\scripts\warm_bench_locked.py`

**Status:** PRODUCTION READY

**Features:**
- Generic/parameterized (works for ANY position)
- No hardcoded role, candidate name, or content
- Accepts: candidate_name, candidate_email, position, body_html
- Logo attachment via MIME Content-ID
- Supports pilot mode + live send
- CLI interface + programmatic usage
- Error handling for logo attachment

**Programmatic Usage:**
```python
from scripts.warm_bench_locked import send_warm_bench_email

send_warm_bench_email(
    candidate_name="Dur E Nayab",
    candidate_email="email@domain.com",
    position="Junior Research Associate",
    body_html="<p>Hi Dur E Nayab,...</p>",
    pilot_mode=True,
    pilot_recipients=["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
)
```

**CLI Usage:**
```bash
python scripts/warm_bench_locked.py \
  --candidate "Dur E Nayab" \
  --email "email@domain.com" \
  --position "Junior Research Associate" \
  --body-file path/to/body.html \
  --pilot
```

### 2. Template: `templates/warm_bench_email.html`

**Location:** `c:\Agent Coco\templates\warm_bench_email.html`

**Status:** DESIGN LOCKED (do not modify)

**Locked Design Specification:**

| Element | Value |
|---------|-------|
| **Background** | #f3f4f6 (light gray) |
| **Card** | #ffffff (white, 620px wide) |
| **Logo** | 48x48px, centered, Content-ID embedded |
| **Header Label** | #5B8DBE, 12px, uppercase, letter-spacing 2px |
| **Candidate Name** | #1565C0, 32px, Georgia serif, bold |
| **Position** | #7986CB, 14px, Georgia serif |
| **Divider** | #1565C0, 2px height |
| **Body Text** | 16px, Georgia serif, 1.75 line-height, justified |
| **Padding** | 70px sides, 60px top/bottom |

**Template Variables:**
- `{candidate_name}` - Candidate full name
- `{position}` - Job position title
- `{body_content}` - HTML body paragraphs

**Format:**
- Uses nested HTML tables (email-safe layout)
- Logo embedded via `cid:logo_taleemabad` Content-ID
- MIME structure: related/alternative/text-html + image attachment

### 3. Skill Definition: `skills/warm-bench-feedback-email.md`

**Location:** `c:\Agent Coco\skills\warm-bench-feedback-email.md`

**Status:** UPDATED with locked asset references

**Non-Negotiables (LOCKED):**
1. No em dashes anywhere
2. "We" voice only (never "I")
3. They/them pronouns for all candidates
4. Specific interview evidence required (quote or paraphrase)
5. GWC transparency (explain what their GWC was/means)
6. Warm welcome for future applications (no specific role promises)
7. Feedback widget mandatory (for personalized emails)
8. Recipients: TO = candidate email, CC = hiring@ + ayesha.khan@
9. Pilot mode ALWAYS first (PILOT_MODE = True)
10. Safe_sendmail bouncer required

## When to Use

Send warm bench feedback emails when:
- ✅ Candidate cleared values interview (Values PASS)
- ✅ Had strong GWC (YES or CONDITIONAL on relevant condition)
- ✅ NOT selected for current role
- ✅ May fit future roles

Do NOT send if:
- ❌ Candidate failed values (send CV-stage rejection instead)
- ❌ Candidate permanently out-of-consideration
- ❌ No realistic future role for them

## How to Use (Step-by-Step)

1. **Prepare body HTML** - Write 5 sections in HTML format:
   - Opening greeting
   - What We Saw (values interview evidence)
   - GWC Assessment
   - Warm Welcome (future opportunities)
   - Closing + sign-off

2. **Call the script:**
   ```python
   from scripts.warm_bench_locked import send_warm_bench_email
   
   send_warm_bench_email(
       candidate_name="Dur E Nayab",
       candidate_email="email@domain.com",
       position="Junior Research Associate",
       body_html=body_html_string,
       pilot_mode=True,
       pilot_recipients=["ayesha.khan@taleemabad.com", "jawwad.ali@taleemabad.com"]
   )
   ```

3. **Verify in inbox:**
   - Pilot emails go to Ayesha + Jawwad for review
   - Once approved, set `pilot_mode=False` to send live

## Recent Session (2026-05-04)

**Work Done:**
- Parameterized script (removed hardcoded "Junior Research Associate")
- Created generic, reusable template
- Extracted HTML design to separate locked template file
- Design colors/fonts/spacing LOCKED
- Logo embedded via MIME Content-ID (proper email client support)
- Added CLI + programmatic interfaces
- Updated skill definition with locked asset references
- Added to memory as production-ready resource

**Result:**
- Generic script works for ANY position
- Design is frozen and cannot drift
- Logo displays correctly across email clients
- Ready for production use

## Commitment (Coco, 2026-05-04 LOCKED)

I will use the locked script and template for all warm bench feedback emails. I will not modify colors, fonts, spacing, or layout. I will parameterize all candidate/position/content inputs. I will pilot emails to Ayesha + Jawwad before sending live. I will quote actual values interview examples. I will reference GWC assessment. I will extend warm welcome for future applications without specific role promises. All non-negotiables locked in script + template. No deviation allowed.
