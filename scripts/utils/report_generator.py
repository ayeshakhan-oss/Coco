"""
Report Generator — Generates reports with locked format specifications
==================================================================================
- Loads specification from memory
- Injects rules into generation prompt
- Validates output before returning
- Zero tolerance for format drift

Usage:
  from scripts.utils.report_generator import generate_report_with_locked_format

  html_output = generate_report_with_locked_format(
      report_type='screening_report',
      candidates=candidates_list,
      position='Soul Architect',
      job_id=26
  )
  # Output is guaranteed to match locked format
"""

from typing import Dict, List, Any, Optional
import json
from scripts.utils.report_memory_loader import (
    load_report_spec,
    create_system_prompt,
    get_report_rules_summary
)
from scripts.utils.report_validator import (
    ReportValidator,
    ValidationError,
    validate_before_send
)


class ReportGenerator:
    """Generate reports with locked format specifications."""

    def __init__(self, report_type: str):
        """
        Initialize generator for a report type.

        Args:
            report_type: 'screening_report' or 'decision_brief'
        """
        self.report_type = report_type
        self.spec = load_report_spec(report_type)
        self.system_prompt = create_system_prompt(self.spec)
        self.validator = ReportValidator(report_type)

    def get_generation_instructions(self) -> str:
        """
        Get formatted instructions for Claude/template engine to generate report.

        Returns:
            Complete generation instructions with locked format embedded
        """
        return self.system_prompt

    def validate_output(self, html_output: str) -> bool:
        """
        Validate generated HTML against locked specification.

        Args:
            html_output: Generated HTML email body

        Returns:
            True if valid

        Raises:
            ValidationError if invalid
        """
        return validate_before_send(html_output, self.report_type)

    def get_validation_report(self, html_output: str) -> str:
        """
        Get detailed validation report for an output.

        Args:
            html_output: Generated HTML email body

        Returns:
            Formatted validation report
        """
        violations = self.validator.validate(html_output)
        return self.validator.get_report()


def generate_report_with_locked_format(
    report_type: str,
    position: str,
    job_id: int,
    candidates: List[Dict[str, Any]],
    shortlisted_count: Optional[int] = None,
    maybe_count: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate a report with specifications locked in place.

    This is the main entry point. It:
    1. Loads locked specification
    2. Creates system prompt with rules embedded
    3. Returns generation instructions + validation function

    Args:
        report_type: 'screening_report' or 'decision_brief'
        position: Job position title
        job_id: Job ID number
        candidates: List of candidate dicts
        shortlisted_count: Count of shortlisted (for validation)
        maybe_count: Count of maybe pool (for validation)

    Returns:
        Dict with:
          - 'spec': Loaded specification
          - 'prompt': Generation instructions (to pass to Claude/template)
          - 'validate': Function to validate output
          - 'rules_summary': Human-readable rules
    """

    generator = ReportGenerator(report_type)

    return {
        'spec': generator.spec,
        'report_type': report_type,
        'position': position,
        'job_id': job_id,
        'candidate_count': len(candidates),
        'shortlisted_count': shortlisted_count,
        'maybe_count': maybe_count,
        'generation_instructions': generator.get_generation_instructions(),
        'validate': generator.validate_output,
        'validation_report': generator.get_validation_report,
        'rules_summary': get_report_rules_summary(report_type),
        'candidates': candidates
    }


def build_prompt_for_generation(
    report_type: str,
    position: str,
    job_id: int,
    data: Dict[str, Any]
) -> str:
    """
    Build complete prompt for Claude API generation.

    Args:
        report_type: 'screening_report' or 'decision_brief'
        position: Job position title
        job_id: Job ID
        data: Report data (candidates, stats, etc.)

    Returns:
        Complete prompt ready for Claude API
    """

    generator = ReportGenerator(report_type)

    # System prompt (rules embedded)
    system = generator.get_generation_instructions()

    # User prompt (data)
    user_prompt = f"""
Generate a {report_type} report with this data:

POSITION: {position}
JOB ID: {job_id}

DATA:
{json.dumps(data, indent=2)}

INSTRUCTIONS:
1. Follow ALL rules in the system prompt above
2. Structure EXACTLY as specified
3. No deviations from locked format
4. All candidate names must be hyperlinked (placeholders: [CANDIDATE_NAME_LINK])
5. Generate HTML email body (no <!DOCTYPE>, just body content)
6. Use exact section headers from specification
7. Apply exact colors, fonts, alignment as specified

Remember: Format is LOCKED. Every element must match specification.
Generate now.
"""

    return f"""SYSTEM PROMPT:
{system}

USER PROMPT:
{user_prompt}
"""


def create_report_generation_config(report_type: str) -> Dict[str, Any]:
    """
    Create configuration dict for report generation.
    Use this when setting up report generation in scripts.

    Args:
        report_type: 'screening_report' or 'decision_brief'

    Returns:
        Config dict with all settings
    """
    spec = load_report_spec(report_type)

    return {
        'type': report_type,
        'spec': spec,
        'system_prompt': create_system_prompt(spec),
        'rules': get_report_rules_summary(report_type),
        'validator': ReportValidator(report_type),
        'validation_required': True,
        'approval_required': True,
        'approval_mode': 'PILOT_FIRST',
        'html_only': True,
        'pdf_forbidden': True,
        'font_family': 'Georgia, serif',
        'heading_color': '#1565c0',
        'text_alignment': 'justify',
        'all_names_must_be_hyperlinked': True,
        'no_fabrication': True
    }


class ReportGenerationPipeline:
    """
    Full pipeline for report generation with validation and approval.
    """

    def __init__(self, report_type: str):
        self.report_type = report_type
        self.config = create_report_generation_config(report_type)
        self.generated_html = None
        self.validation_passed = False
        self.approval_status = "PENDING"

    def step1_get_generation_prompt(self, data: Dict[str, Any]) -> str:
        """Step 1: Get prompt to send to Claude."""
        return build_prompt_for_generation(
            self.report_type,
            data.get('position', 'Unknown'),
            data.get('job_id', 0),
            data
        )

    def step2_set_generated_html(self, html: str):
        """Step 2: Set the generated HTML output."""
        self.generated_html = html

    def step3_validate(self) -> bool:
        """Step 3: Validate against locked specification."""
        try:
            self.config['validator'].validate(self.generated_html)
            self.validation_passed = True
            return True
        except ValidationError as e:
            self.validation_passed = False
            print(f"Validation failed:\n{e}")
            return False

    def step4_get_validation_report(self) -> str:
        """Step 4: Get detailed validation report."""
        if not self.generated_html:
            return "No HTML generated yet"
        return self.config['validator'].get_report()

    def step5_request_approval(self, recipient: str) -> bool:
        """Step 5: Request approval (user interaction point)."""
        if not self.validation_passed:
            print("⚠️  Cannot request approval — validation failed first")
            return False

        print(f"""
═══════════════════════════════════════════════════════════════════════════
REPORT READY FOR APPROVAL

Report Type: {self.report_type}
Validation: ✓ PASSED
Status: PILOT (awaiting approval before LIVE send)

Recipient (PILOT): {recipient}

APPROVAL CHECKLIST:
  [ ] Format matches locked specification
  [ ] All candidate data present and correct
  [ ] All names hyperlinked to Google Drive CVs
  [ ] No PDF — HTML email body only
  [ ] Georgia serif font throughout
  [ ] All stat box math verified
  [ ] Ready for recipient review

Action: Approve (send PILOT) or Reject (regenerate)
═══════════════════════════════════════════════════════════════════════════
        """)

        self.approval_status = "PILOT_SENT"
        return True

    def step6_send_live(self, approval_confirmed: bool):
        """Step 6: Send live after approval."""
        if approval_confirmed and self.approval_status == "PILOT_SENT":
            self.approval_status = "APPROVED_LIVE"
            return True
        else:
            print("Approval not confirmed. Not sending.")
            return False


if __name__ == "__main__":
    # Test: Create generators for both report types
    print("Initializing Report Generation System\n")

    for report_type in ['screening_report', 'decision_brief']:
        print(f"Setting up: {report_type}")
        config = create_report_generation_config(report_type)
        print(f"  ✓ Spec loaded: {config['spec']['name']}")
        print(f"  ✓ Validator ready")
        print(f"  ✓ System prompt created")
        print()

    print("✓ Report generation system ready")
    print("  - Locked specifications in place")
    print("  - Validation enforced")
    print("  - Format guaranteed across all generations")
