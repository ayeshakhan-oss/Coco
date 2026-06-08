"""
Claude Code UserPromptSubmit hook.
Reads the user's prompt from stdin (JSON), detects keywords,
and injects relevant memory file contents into the context
by printing to stdout (Claude Code reads this as additional context).

LAYER 1 ENHANCEMENT (2026-06-08):
When "draft" + candidate communication keyword detected, also injects:
- Locked template HTML (so user edits, doesn't create from scratch)
- Pre-flight checklist (gates drafting until acknowledged)
- Master index (tells user where everything is)

Keyword → memory file mapping is defined in KEYWORD_MAP below.
"""

import sys
import json
from pathlib import Path
import io

# Force UTF-8 output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MEMORY_DIR = Path("c:/Agent Coco/memory")
TEMPLATES_DIR = Path("c:/Agent Coco/templates")

# LAYER 1 ENHANCEMENT (2026-06-08): Draft detection + template injection
# When "draft" + candidate communication keyword detected, inject template + checklist
DRAFT_TEMPLATE_MAP = {
    "gwc rejection": ("gwc_rejection_template_locked.html", "GWC Rejection"),
    "warm bench": ("warm_bench_template_locked.html", "Warm Bench"),
    "values feedback": ("values_feedback_template_locked.html", "Values Feedback"),
    "cv rejection": ("cv_rejection_template_locked.html", "CV Rejection"),
}

# Keyword patterns → memory files to inject (in priority order)
KEYWORD_MAP = [
    (["warm bench", "warmbenck", "jra", "haroon"], [
        "warm_bench_final_locked_approach.md",
        "warm_bench_session_may5_2026_complete_learnings.md",
        "warm_bench_subject_lines_locked.md",
    ]),
    (["gwc rejection", "gwc email", "gw-c"], [
        "lesson_no_intent_inference_rejection_emails_2026_06_01.md",
        "warm_bench_locked_final_2026_05_30.md",
        "lesson_evidence_based_rejection_rationale_2026_06_01.md",
    ]),
    (["values feedback", "values email", "values interview feedback"], [
        "values_feedback_email_tone_locked_2026_05_12.md",
        "rule_all_feedback_emails_use_locked_tone.md",
    ]),
    (["cv rejection", "screening rejection", "cv screening rejection"], [
        "feedback_email_rules.md",
        "rule_all_feedback_emails_use_locked_tone.md",
    ]),
    (["cv", "screen", "screening", "candidate", "resume"], [
        "skill_cv_screening_sop.md",
    ]),
    (["rejection", "reject", "feedback email"], [
        "skill_values_feedback_emails_sop.md",
    ]),
    (["attendance", "onsite", "wfh", "leave"], [
        "attendance_report_complete_template.md",
    ]),
    (["decision brief", "brief", "hiring decision"], [
        "project_job36_decision_brief.md",
        "project_job32_decision_brief_format.md",
    ]),
    (["interview", "invite", "calendar"], [
        "locked_email_template_interview_invites.md",
    ]),
    (["talent", "source", "sourcing", "linkedin"], [
        "coco_talent_sourcing_skill.md",
    ]),
    (["lesson", "mistake", "error", "wrong"], [
        "lessons_learned.md",
    ]),
]

# Files always injected (small, critical)
ALWAYS_INJECT = [
    "session_active.md",
]

MAX_FILE_CHARS = 3000  # Truncate long files to stay within context budget


def detect_draft_request(prompt):
    """
    LAYER 1 ENHANCEMENT: Detect if user is asking to draft a candidate email.
    Returns (is_draft, template_file, email_type) or (False, None, None)
    """
    prompt_lower = prompt.lower()

    # Check if "draft" keyword present
    if "draft" not in prompt_lower:
        return False, None, None

    # Check which email type they're drafting
    for draft_keyword, (template_file, email_type) in DRAFT_TEMPLATE_MAP.items():
        if draft_keyword in prompt_lower:
            return True, template_file, email_type

    return False, None, None


def inject_template_and_checklist(template_file):
    """
    LAYER 1 ENHANCEMENT: Inject locked template HTML + pre-flight checklist.
    Returns formatted injection block.
    """
    blocks = []

    # Inject pre-flight checklist (MUST READ FIRST)
    checklist_path = MEMORY_DIR / "pre_draft_checklist_2026_06_08.md"
    if checklist_path.exists():
        checklist_content = checklist_path.read_text(encoding="utf-8")
        blocks.append("<!-- LAYER 1: PRE-FLIGHT CHECKLIST (MANDATORY - READ BEFORE DRAFTING) -->\n")
        blocks.append(f"<!-- MEMORY: pre_draft_checklist_2026_06_08.md -->\n{checklist_content}\n<!-- END MEMORY: pre_draft_checklist_2026_06_08.md -->")

    # Inject locked template HTML
    template_path = TEMPLATES_DIR / template_file
    if template_path.exists():
        template_content = template_path.read_text(encoding="utf-8")
        blocks.append("\n\n<!-- LAYER 1: LOCKED TEMPLATE HTML (DO NOT MODIFY STRUCTURE/COLORS/FONTS) -->\n")
        blocks.append(f"<!-- TEMPLATE: {template_file} -->\n{template_content}\n<!-- END TEMPLATE: {template_file} -->")

    # Inject three-layer enforcement guide
    enforcement_path = MEMORY_DIR / "three_layer_pre_draft_enforcement_2026_06_08.md"
    if enforcement_path.exists():
        enforcement_content = enforcement_path.read_text(encoding="utf-8")
        if len(enforcement_content) > MAX_FILE_CHARS:
            enforcement_content = enforcement_content[:MAX_FILE_CHARS] + "\n\n[...truncated for context budget...]"
        blocks.append("\n\n<!-- LAYER 1: THREE-LAYER ENFORCEMENT ARCHITECTURE -->\n")
        blocks.append(f"<!-- MEMORY: three_layer_pre_draft_enforcement_2026_06_08.md -->\n{enforcement_content}\n<!-- END MEMORY: three_layer_pre_draft_enforcement_2026_06_08.md -->")

    return "\n\n".join(blocks)


def detect_relevant_files(prompt):
    prompt_lower = prompt.lower()
    files = list(ALWAYS_INJECT)

    for keywords, memory_files in KEYWORD_MAP:
        if any(kw in prompt_lower for kw in keywords):
            for f in memory_files:
                if f not in files:
                    files.append(f)

    return files


def inject_memory(files):
    """Read and concatenate memory files. Return formatted injection block."""
    blocks = []
    for filename in files:
        path = MEMORY_DIR / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + "\n\n[...truncated for context budget...]"
        blocks.append(f"<!-- MEMORY: {filename} -->\n{content}\n<!-- END MEMORY: {filename} -->")

    if not blocks:
        return ""

    return "\n\n".join(blocks)


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    prompt = data.get("prompt", "")
    if not prompt:
        return  # No prompt, nothing to inject

    # LAYER 1 ENHANCEMENT (2026-06-08): Check for draft requests first
    is_draft, template_file, email_type = detect_draft_request(prompt)
    injection_blocks = []

    if is_draft and template_file:
        # Inject template + checklist for draft requests
        template_injection = inject_template_and_checklist(template_file)
        if template_injection:
            injection_blocks.append(template_injection)

    # Always inject relevant rule files (from KEYWORD_MAP)
    relevant_files = detect_relevant_files(prompt)
    memory_injection = inject_memory(relevant_files)
    if memory_injection:
        injection_blocks.append(memory_injection)

    # Combine all injections
    if injection_blocks:
        # Claude Code reads stdout of UserPromptSubmit hook as additional context
        print("\n\n".join(injection_blocks))


if __name__ == "__main__":
    main()
