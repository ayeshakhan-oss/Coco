"""
gen_locked_templates.py — regenerate the 4 Layer-1 locked HTML templates from v8.
================================================================================
The harness (scripts/memory/prompt_submit_hook.py) injects these templates at
draft time so Coco EDITS the locked layout instead of inventing HTML. They must
match the v8 layout exactly (scripts/utils/v8_template.py).

Run this whenever v8_template.py changes:
    python scripts/utils/gen_locked_templates.py

Output: templates/{cv_rejection,values_feedback,warm_bench,gwc_rejection}_template_locked.html
Layout: 100% v8. Content: [PLACEHOLDERS] for Coco to fill. Section headings + rules
differ per type (and are enforced by scripts/evals/candidate_communication_eval.py).
"""

import os
from scripts.utils.v8_template import H, SUB, P, PS, FOOTER, wrap, EYEBROW

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
DATE = "2026-06-10"

WIDGET_NOTE = "\n<!-- [FEEDBACK_WIDGET] — feedback_widget(name, role, app_id, 'Application Feedback') is auto-appended here by the send script. Do not hand-write it. -->"

TYPES = {
    "values_feedback": {
        "file": "values_feedback_template_locked.html",
        "title": "VALUES FEEDBACK",
        "scope": "Candidates who FAILED the values interview (did not clear values assessment)",
        "eyebrow": EYEBROW["values_feedback"],
        "headings": [
            "What We Liked Most About You",
            "Where We Found Ourselves Sitting With Questions",
            "What We Think You Should Do Next",
        ],
        "sub": "We share what follows with care, because we believe honest reflection is more useful than softness.",
        "rules": """VALUES FEEDBACK RULES:
1. Scope: candidates who FAILED the values interview only.
2. Source: values interview scorecard only (not CV, not other interviews).
3. Tone: warm, observational, deeply human (not analytical, not life-coach).
4. NO internal jargon (plus-minus ratings, "values scorecard", framework lingo).
5. NO intent inference ("you assumed/believed/seemed/lacked"). Use "what we found ourselves wanting...".
6. NO em dashes. NO interviewer names. NO asterisks in headings.
7. Door open IF they grow and return ("should you work through them...").
WORD COUNT: 800-1100 mandatory.""",
    },
    "warm_bench": {
        "file": "warm_bench_template_locked.html",
        "title": "WARM BENCH FEEDBACK",
        "scope": "Candidates who CLEARED values but were not selected (rejection-keep-warm)",
        "eyebrow": EYEBROW["warm_bench"],
        "headings": [
            "What Stayed With Us",
            "Here's the Honest Part",
            "Where We Want to Leave This",
        ],
        "sub": None,
        "rules": """WARM BENCH RULES:
1. Opening (mandatory): "This is not a yes for now." + panel-kept-discussing hook.
2. Headings exactly: What Stayed With Us / Here's the Honest Part / Where We Want to Leave This.
3. NO interviewer names. NO internal jargon (GWC/values/scorecard/case study/warm bench).
4. NO comparison to "another candidate". NO recruiting abstractions ("strong candidate").
5. Haroon balance: praise specificity ~= decision specificity.
6. NO em dashes. NO asterisks in headings. Poetic, story-based subject line.
7. P.S. ties back to ONE powerful interview moment.
WORD COUNT: 800-1100 mandatory.""",
    },
    "gwc_rejection": {
        "file": "gwc_rejection_template_locked.html",
        "title": "GWC REJECTION",
        "scope": "GWC-cleared candidates not moving forward (warm-tone rejection)",
        "eyebrow": EYEBROW["gwc_rejection"],
        "headings": [
            "What Stayed With Us",
            "Here's the Honest Part",
            "Where We Want to Leave This",
        ],
        "sub": None,
        "rules": """GWC REJECTION RULES:
1. Headings exactly: What Stayed With Us / Here's the Honest Part / Where We Want to Leave This.
2. NEVER use "GWC" or "KCD" terminology (internal jargon).
3. Evidence-based rationale: observable behaviors, not abstractions (hunger/energy/confidence).
4. NO intent inference. NO interviewer names. NO comparison to other candidates.
5. Decision rationale as concrete as the praise (Haroon balance).
6. NO em dashes. NO asterisks in headings.
WORD COUNT: 800-1100 mandatory.""",
    },
    "cv_rejection": {
        "file": "cv_rejection_template_locked.html",
        "title": "CV REJECTION",
        "scope": "CV-stage rejections (screened out before interview)",
        "eyebrow": EYEBROW["cv_rejection"],
        "headings": [
            "What we appreciated",
            "Where we found questions",
            "What we think you should do next",
        ],
        "sub": None,
        "rules": """CV REJECTION RULES:
1. Source: the candidate's actual CV text only (no interview — there wasn't one).
2. Role-fit framing ("the role required...") not personal shortcoming ("you lacked...").
3. Never suggest a skill the candidate already has. Read >= 10k chars of CV.
4. NO intent inference. NO em dashes. NO asterisks in headings. NO jargon.
WORD COUNT: 800+ mandatory.""",
    },
}


def build(cfg):
    h = cfg["headings"]
    sec2 = H(h[1])
    if cfg["sub"]:
        sec2 += SUB(cfg["sub"])
    body = (
        P("Dear [CANDIDATE_FIRST_NAME],")
        + P("This is not a yes for now.")
        + P("[OPENING_PARAGRAPH: state the decision clearly + promise an honest, specific account. 'We have completed our evaluation of your ... We will not be moving you forward at this time...' Pair this with candidate-initiated reapplication language later, never a promise of proactive outreach.]")
        + H(h[0]) + P("[SECTION_1_CONTENT: 2-3 specific strengths, each tied to evidence from the source. Observable behaviors, not generic labels.]")
        + sec2 + P("[SECTION_2_CONTENT: 2-3 honest gaps, evidence-based. Frame as 'what we found ourselves wanting...' / 'the role required...' — never intent inference or personal shortcoming.]")
        + H(h[2]) + P("[SECTION_3_CONTENT: gentle, specific guidance. Door-open close where appropriate. Careers page link.]")
        + PS("<strong>P.S.</strong> [PS_CONTENT: one memorable, character-affirming line tied to a specific moment.]")
        + FOOTER
        + WIDGET_NOTE
    )
    html = wrap(subject_line="[SUBJECT_LINE]", role="[ROLE]", eyebrow=cfg["eyebrow"], body_html=body)
    header = (
        f"<!-- {cfg['title']} EMAIL TEMPLATE — LOCKED v8 LAYOUT ({DATE}) -->\n"
        f"<!-- Scope: {cfg['scope']} -->\n"
        f"<!-- LAYOUT IS LOCKED (v8 / scripts/utils/v8_template.py). Edit ONLY the [PLACEHOLDER] content. -->\n"
        f"<!-- Regenerate with: python scripts/utils/gen_locked_templates.py -->\n\n"
    )
    footer = f"\n\n<!--\n{cfg['rules']}\n-->\n"
    return header + html + footer


def main():
    for key, cfg in TYPES.items():
        out = os.path.join(TEMPLATES_DIR, cfg["file"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(cfg))
        print(f"  wrote {cfg['file']}")
    print("Done. 4 locked templates regenerated from v8.")


if __name__ == "__main__":
    main()
