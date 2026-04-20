"""
Report Memory Loader — Loads locked report specifications from memory
==================================================================================
Ensures all report generation uses memory-injected specifications.
No drift. No format regression. Structure locked forever.

Usage:
  from scripts.utils.report_memory_loader import load_report_spec, create_system_prompt

  spec = load_report_spec('screening_report')
  system_prompt = create_system_prompt(spec)
  # Pass system_prompt to Claude API or template engine
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

# Memory location
MEMORY_ROOT = Path.home() / ".claude" / "projects" / "C--Agent-Coco" / "memory"

# Lock the report specifications (HARD-CODED from memory, survives forever)
SCREENING_REPORT_SPEC = {
    "type": "initial_screening",
    "name": "Initial Screening Report",
    "purpose": "Evaluate candidate CVs against Job Description. Manual review of all profiles.",
    "locked_format": True,
    "sections": {
        "header": {
            "required": True,
            "style": {
                "background_color": "#1a2a3a",
                "text_color": "white",
                "alignment": "center",
                "text_transform": "uppercase",
                "font_family": "Georgia, serif"
            },
            "content": {
                "logo": "Taleemabad",
                "line1": "PEOPLE & CULTURE · INITIAL SCREENING REPORT",
                "line2": "[JOB_TITLE]",
                "line3": "Job [X] · Taleemabad"
            }
        },
        "stat_boxes": {
            "required": True,
            "count": 4,
            "exact": True,
            "boxes": [
                {
                    "position": 1,
                    "color": "#f44336",
                    "label": "Total Screened",
                    "data_key": "total_screened"
                },
                {
                    "position": 2,
                    "color": "#1565c0",
                    "label": "Shortlisted",
                    "data_key": "shortlisted_count"
                },
                {
                    "position": 3,
                    "color": "#fbc02d",
                    "label": "Maybe / Consider",
                    "data_key": "maybe_count"
                },
                {
                    "position": 4,
                    "color": "#9e9e9e",
                    "label": "No Hire",
                    "data_key": "no_hire_count"
                }
            ]
        },
        "key_observation": {
            "required": True,
            "heading_color": "#1565c0",
            "font_family": "Georgia, serif",
            "font_size": "15px",
            "text_align": "justify",
            "line_height": "1.8",
            "word_count": {
                "min": 40,
                "max": 150,
                "ideal": 80
            },
            "sentences": {
                "min": 2,
                "max": 3
            }
        },
        "shortlisted_candidates": {
            "required": True,
            "count_typical": 5,
            "per_candidate": {
                "name": {
                    "required": True,
                    "hyperlinked": True,
                    "must_link_to": "google_drive_cv"
                },
                "ranking": {
                    "required": True,
                    "allowed_values": ["#1 TOP PICK", "#2 TOP PICK", "#3 TOP PICK", "SHORTLIST"],
                    "color_top_pick": "#c62828",
                    "color_shortlist": "#1565c0"
                },
                "match_percentage": {
                    "required": True,
                    "format": "##%",
                    "range": [78, 95]
                },
                "app_id": {
                    "required": True,
                    "format": "App ID: ####"
                },
                "total_experience": {
                    "required": True,
                    "format": "Total exp: ~X yrs",
                    "note": "State TOTAL years, not relevant"
                },
                "relevant_experience": {
                    "required": True,
                    "format": "Relevant exp: ~X yrs",
                    "note": "State RELEVANT years separately from total"
                },
                "expected_salary": {
                    "required": True,
                    "format": "Expected Salary: [amount or 'Not mentioned']"
                },
                "city": {
                    "required": True,
                    "format": "City: [location]"
                },
                "willing_to_relocate": {
                    "required": True,
                    "format": "Relocate: Y/N"
                },
                "db_status": {
                    "required": True,
                    "format": "DB status: [status]",
                    "allowed_values": ["shortlisted", "gwc_scheduled", "interview_pending", "values_passed", "rejected"]
                },
                "description": {
                    "required": True,
                    "sentences": {
                        "min": 3,
                        "max": 4
                    },
                    "font_family": "Georgia, serif",
                    "font_size": "15px",
                    "text_align": "justify",
                    "line_height": "1.8"
                },
                "gap": {
                    "required": True,
                    "sentences": {
                        "min": 1,
                        "max": 2
                    },
                    "font_family": "Georgia, serif",
                    "font_size": "15px",
                    "text_align": "justify"
                }
            }
        },
        "maybe_table": {
            "required": True,
            "count_typical": 7,
            "columns": [
                {
                    "name": "Candidate",
                    "width": "40%",
                    "hyperlinked": True,
                    "must_link_to": "google_drive_cv"
                },
                {
                    "name": "Match %",
                    "width": "20%",
                    "format": "##%",
                    "range": [40, 75]
                },
                {
                    "name": "Note",
                    "width": "40%",
                    "sentences": {
                        "min": 1,
                        "max": 2
                    }
                }
            ]
        },
        "footer": {
            "required": True,
            "format": "Taleemabad Talent Acquisition | hiring@taleemabad.com | [DATE]",
            "font_family": "Georgia, serif",
            "font_size": "13px",
            "text_color": "#555555"
        }
    },
    "global_rules": {
        "font_family": "Georgia, serif",
        "heading_color": "#1565c0",
        "text_alignment": "justify",
        "line_height": "1.8",
        "no_pdf": True,
        "html_only": True,
        "all_names_hyperlinked": True,
        "no_fabrication": True,
        "no_assumptions": True,
        "approval_required": True,
        "approval_mode": "PILOT_FIRST"
    },
    "qa_checklist": [
        "Header matches reference exactly (logo, navy bg, uppercase title)",
        "Stat boxes are 4, colored correctly, math verified",
        "Key Observation is 2-3 sentences, blue heading",
        "Shortlisted candidates: each has all 5 data fields",
        "Shortlisted candidates: each has description + gap paragraph",
        "Shortlisted candidates: names hyperlinked to Google Drive",
        "Maybe table: 3 columns (name, match %, note)",
        "Maybe candidates: names hyperlinked",
        "Footer with date added",
        "Georgia serif font throughout",
        "All section headings in blue (#1565c0)",
        "Body text is justified",
        "No PDF — HTML email only",
        "Ready for PILOT review"
    ]
}

DECISION_BRIEF_SPEC = {
    "type": "decision_brief",
    "name": "Decision Brief Report",
    "purpose": "Summarize final candidates after interviews. Decision-ready pipeline view.",
    "locked_format": True,
    "sections": {
        "header": {
            "required": True,
            "style": {
                "background_color": "#1a2a3a",
                "text_color": "white",
                "alignment": "center",
                "font_family": "Georgia, serif"
            },
            "content": {
                "logo": "Taleemabad",
                "line1": "Final Candidates & Decision View",
                "line2": "[POSITION_TITLE]"
            }
        },
        "stat_boxes": {
            "required": True,
            "count": 4,
            "min": 4,
            "max": 5,
            "flexible": True,
            "typical_boxes": [
                {"label": "Total Applied", "data_key": "total_applied"},
                {"label": "Values Completed", "data_key": "values_completed"},
                {"label": "Cleared / Values", "data_key": "values_cleared"},
                {"label": "Debriefs This Week", "data_key": "debriefs_this_week"}
            ]
        },
        "where_we_are": {
            "required": True,
            "heading_color": "#1565c0",
            "sentences": {
                "min": 2,
                "max": 4
            },
            "font_family": "Georgia, serif",
            "text_align": "justify"
        },
        "debrief_schedule": {
            "required": True,
            "type": "table",
            "columns": [
                {
                    "name": "Candidate",
                    "width": "30%",
                    "hyperlinked": True,
                    "must_link_to": "google_drive_cv"
                },
                {
                    "name": "Date",
                    "width": "20%",
                    "format": "YYYY-MM-DD (no relative dates)",
                    "rule": "actual_dates_only"
                },
                {
                    "name": "Status",
                    "width": "25%",
                    "allowed_values": [
                        "DEBRIEF CONFIRMED",
                        "DEBRIEF TODAY",
                        "CASE STUDY IN",
                        "CASE STUDY SENT",
                        "PANEL DECISION",
                        "VALUES PASS",
                        "OVERDUE",
                        "NOT INTERVIEWED"
                    ]
                },
                {
                    "name": "Notes",
                    "width": "25%"
                }
            ]
        },
        "leading_candidates": {
            "required": True,
            "count_typical": 2,
            "per_candidate": {
                "name": {
                    "required": True,
                    "hyperlinked": True,
                    "must_link_to": "google_drive_cv"
                },
                "verdict": {
                    "required": True,
                    "allowed_values": [
                        "DEBRIEF CONFIRMED",
                        "DEBRIEF TODAY",
                        "PANEL DECISION",
                        "VALUES PASS",
                        "CASE STUDY IN"
                    ]
                },
                "debrief_info": {
                    "required": True,
                    "format": "Debrief: [DATE], [TIME] or [STATUS]",
                    "dates_only": True
                },
                "tagline": {
                    "required": True,
                    "italic": True,
                    "length": {
                        "min": 5,
                        "max": 15,
                        "words": True
                    }
                },
                "signal_paragraph": {
                    "required": True,
                    "sentences": {
                        "min": 3,
                        "max": 4
                    },
                    "font_family": "Georgia, serif",
                    "text_align": "justify",
                    "content": "Evidence from interview/case study, no fabrication"
                },
                "probing_questions": {
                    "required": True,
                    "label": "At debrief, probe:",
                    "label_color": "#7b341e",
                    "count": {
                        "min": 2,
                        "max": 4
                    },
                    "format": "- Question about [specific gap]?",
                    "content": "Based on interview/case study gaps"
                }
            }
        },
        "discussion_candidates": {
            "required": False,
            "per_candidate": "Same as leading_candidates"
        },
        "also_in_pipeline": {
            "required": False,
            "type": "table",
            "columns": [
                {
                    "name": "Candidate",
                    "hyperlinked": True,
                    "must_link_to": "google_drive_cv"
                },
                {
                    "name": "Status"
                }
            ]
        },
        "footer": {
            "required": True,
            "format": "Compiled by Coco | Taleemabad Talent Acquisition | [DATE]",
            "font_family": "Georgia, serif",
            "font_size": "13px"
        }
    },
    "global_rules": {
        "font_family": "Georgia, serif",
        "heading_color": "#1565c0",
        "text_alignment": "justify",
        "line_height": "1.8",
        "no_scores": True,
        "no_fabrication": True,
        "all_names_hyperlinked": True,
        "actual_dates_only": True,
        "no_relative_dates": True,
        "no_pdf": True,
        "html_only": True,
        "judgment_led": True,
        "approval_required": True,
        "approval_mode": "PILOT_FIRST"
    },
    "qa_checklist": [
        "Header matches reference exactly (navy bg, position title)",
        "Stat boxes: 4-5 boxes, correct count, math verified",
        "Where We Are: 2-4 sentences, blue heading, justified text",
        "Debrief Schedule: table complete, dates are actual (not relative)",
        "Leading Candidates: each has name (linked), verdict, date, signal, probes",
        "Discussion Candidates: same format as Leading (if applicable)",
        "Also in Pipeline: table complete (if applicable)",
        "ALL candidate names hyperlinked to Google Drive CVs",
        "No scores or ratings present",
        "No PDF — HTML email only",
        "Georgia serif font throughout",
        "All headings in blue (#1565c0)",
        "Body text justified",
        "Footer with date added",
        "Ready for PILOT review"
    ]
}


def load_report_spec(report_type: str) -> Dict[str, Any]:
    """
    Load locked report specification by type.

    Args:
        report_type: 'screening_report' or 'decision_brief'

    Returns:
        Complete specification dict

    Raises:
        ValueError if report_type not recognized
    """
    specs = {
        'screening_report': SCREENING_REPORT_SPEC,
        'decision_brief': DECISION_BRIEF_SPEC,
    }

    if report_type not in specs:
        raise ValueError(
            f"Unknown report type: {report_type}\n"
            f"Allowed: {list(specs.keys())}"
        )

    return specs[report_type]


def create_system_prompt(spec: Dict[str, Any]) -> str:
    """
    Create system prompt with locked format embedded.
    This prompt will be injected into Claude API calls.

    Args:
        spec: Report specification dict

    Returns:
        Complete system prompt with all locked rules
    """

    prompt = f"""
You are generating a Coco {spec['name']}.

LOCKED FORMAT SPECIFICATION
═══════════════════════════════════════════════════════════════════════════

REPORT TYPE: {spec['type'].upper()}
PURPOSE: {spec['purpose']}
STATUS: FORMAT LOCKED — Do NOT deviate. ZERO tolerance for format drift.

CRITICAL RULE: Every generation must match this specification EXACTLY.
Thousands of generations, same format, no exceptions.

SECTIONS (in order):
"""

    for section_name, section_spec in spec['sections'].items():
        if section_spec.get('required'):
            prompt += f"\n{section_name.upper()}:\n"
            prompt += f"  Required: YES\n"

            if section_name == 'stat_boxes':
                prompt += f"  Count: EXACTLY {section_spec['count']} boxes\n"
                prompt += f"  Order:\n"
                for box in section_spec['boxes']:
                    prompt += f"    {box['position']}. {box['label']} ({box['color']})\n"

            elif section_name == 'shortlisted_candidates':
                prompt += f"  Per Candidate (ALL REQUIRED):\n"
                for field, rules in section_spec['per_candidate'].items():
                    if rules.get('required'):
                        prompt += f"    • {field}: {rules.get('format', rules.get('allowed_values', 'required'))}\n"

            elif section_name == 'maybe_table':
                prompt += f"  Columns: {', '.join([c['name'] for c in section_spec['columns']])}\n"
                prompt += f"  Typical Count: {section_spec['count_typical']} candidates\n"

            elif section_name == 'debrief_schedule':
                prompt += f"  Type: TABLE\n"
                prompt += f"  Columns: {', '.join([c['name'] for c in section_spec['columns']])}\n"
                prompt += f"  Rule: ACTUAL DATES ONLY (no 'Today', 'Tomorrow', 'This week')\n"

            elif section_name == 'leading_candidates':
                prompt += f"  Per Candidate (ALL REQUIRED):\n"
                prompt += f"    • Name (hyperlinked to Google Drive CV)\n"
                prompt += f"    • Verdict badge (from allowed values)\n"
                prompt += f"    • Debrief info (actual date, no relative dates)\n"
                prompt += f"    • Italic tagline (5-15 words)\n"
                prompt += f"    • Signal paragraph (3-4 sentences, evidence-based)\n"
                prompt += f"    • Probing questions (2-4 specific probes, no generic questions)\n"

    prompt += f"""

GLOBAL RULES (Non-Negotiable):
─────────────────────────────────────────────────────────────────────────────
"""
    for rule_name, rule_value in spec['global_rules'].items():
        prompt += f"  • {rule_name}: {rule_value}\n"

    prompt += f"""

CRITICAL REQUIREMENTS:
─────────────────────────────────────────────────────────────────────────────
1. FORMAT LOCK: Every element MUST match specification above. No exceptions.
2. ALL NAMES HYPERLINKED: Every candidate name must link to Google Drive CV.
3. NO FABRICATION: Only data from verified sources (CVs, interviews, case studies).
4. NO ASSUMPTIONS: If data missing, state "Not mentioned" (never assume).
5. GEORGIA SERIF: Font family throughout (no sans-serif, no exceptions).
6. JUSTIFIED TEXT: All body paragraphs use text-align: justify.
7. BLUE HEADINGS: All section headings in #1565c0 (no exceptions).
8. HTML ONLY: Email HTML body, never PDF (no PDF attachments).
9. COLORS LOCKED: Use exact colors specified (stat boxes, headings, verdict badges).
10. APPROVAL REQUIRED: Ask Ayesha for PILOT approval before LIVE send.

QA CHECKLIST (BEFORE SENDING):
─────────────────────────────────────────────────────────────────────────────
Before you output anything, verify ALL items:
"""
    for i, check in enumerate(spec['qa_checklist'], 1):
        prompt += f"  {i}. {check}\n"

    prompt += f"""

COMMAND: Generate the {spec['name'].lower()} following this specification EXACTLY.

If ANY element deviates from specification → STOP and regenerate.
If ANY name is not hyperlinked → STOP and add link.
If ANY rule is unclear → Ask for clarification (do not guess).

Your output must be valid HTML email body (no PDF, no plain text).
Structure must match specification for EVERY generation, forever.

═══════════════════════════════════════════════════════════════════════════
"""

    return prompt


def create_audit_checklist(spec: Dict[str, Any]) -> str:
    """
    Create a checklist for validating generated reports.
    """
    checklist = f"QA CHECKLIST FOR {spec['name'].upper()}\n"
    checklist += "=" * 70 + "\n\n"

    for i, check in enumerate(spec['qa_checklist'], 1):
        checklist += f"[ ] {i}. {check}\n"

    checklist += f"\nStatus: PASS only if ALL items checked\n"
    return checklist


def get_report_rules_summary(report_type: str) -> str:
    """
    Get a human-readable summary of locked rules for a report type.
    """
    spec = load_report_spec(report_type)

    summary = f"\n{'='*70}\n"
    summary += f"LOCKED FORMAT RULES: {spec['name'].upper()}\n"
    summary += f"{'='*70}\n\n"

    summary += "REQUIRED SECTIONS:\n"
    for section_name, section_spec in spec['sections'].items():
        if section_spec.get('required'):
            summary += f"  ✓ {section_name.replace('_', ' ').title()}\n"

    summary += "\nFONT & COLOR RULES:\n"
    for rule, value in spec['global_rules'].items():
        if rule in ['font_family', 'heading_color', 'text_alignment']:
            summary += f"  • {rule}: {value}\n"

    summary += "\nCRITICAL: This format is LOCKED. Every generation must match exactly.\n"
    return summary


if __name__ == "__main__":
    # Test: Load specs and print summaries
    print(get_report_rules_summary('screening_report'))
    print(get_report_rules_summary('decision_brief'))
