"""
Claude Code UserPromptSubmit hook.
Reads the user's prompt from stdin (JSON), detects keywords,
and injects relevant memory file contents into the context
by printing to stdout (Claude Code reads this as additional context).

Keyword → memory file mapping is defined in KEYWORD_MAP below.
"""

import sys
import json
from pathlib import Path
import io

# Force UTF-8 output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MEMORY_DIR = Path("c:/Agent Coco/memory")

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

    relevant_files = detect_relevant_files(prompt)
    injection = inject_memory(relevant_files)

    if injection:
        # Claude Code reads stdout of UserPromptSubmit hook as additional context
        print(injection)


if __name__ == "__main__":
    main()
