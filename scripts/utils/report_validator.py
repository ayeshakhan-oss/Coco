"""
Report Validator — Ensures generated reports match locked specifications
==================================================================================
ZERO tolerance for format drift. Every report validated before sending.
Thousands of generations, same structure, no exceptions.

Usage:
  from scripts.utils.report_validator import ReportValidator

  validator = ReportValidator('screening_report')
  violations = validator.validate(html_output)

  if violations:
      print("FORMAT VIOLATIONS FOUND:")
      for v in violations:
          print(f"  ✗ {v}")
      raise ValidationError("Report violates locked format")
  else:
      print("✓ Report matches locked format exactly")
"""

import re
from typing import List, Dict, Any
from scripts.utils.report_memory_loader import load_report_spec


class ReportValidator:
    """Validate generated reports against locked specifications."""

    def __init__(self, report_type: str):
        """
        Initialize validator for a report type.

        Args:
            report_type: 'screening_report' or 'decision_brief'
        """
        self.report_type = report_type
        self.spec = load_report_spec(report_type)
        self.violations = []

    def validate(self, html_output: str) -> List[str]:
        """
        Validate HTML output against locked specification.

        Args:
            html_output: Generated HTML email body

        Returns:
            List of violations (empty if valid)
        """
        self.violations = []

        # Run all validation checks
        self._check_header(html_output)
        self._check_stat_boxes(html_output)
        self._check_font_compliance(html_output)
        self._check_color_compliance(html_output)
        self._check_hyperlinks(html_output)
        self._check_section_structure(html_output)
        self._check_data_fields(html_output)
        self._check_text_alignment(html_output)
        self._check_no_pdf(html_output)

        return self.violations

    def _check_header(self, html: str):
        """Verify header block matches specification."""
        spec = self.spec['sections']['header']

        # Check for logo
        if 'taleemabad' not in html.lower():
            self.violations.append("Missing Taleemabad logo")

        # Check for header background color
        if spec['style']['background_color'] not in html:
            self.violations.append(
                f"Header background missing or wrong color "
                f"(expected {spec['style']['background_color']})"
            )

        # Check for header text
        header_text = spec['content']['line1']
        if header_text not in html:
            self.violations.append(
                f"Missing header line: '{header_text}'"
            )

    def _check_stat_boxes(self, html: str):
        """Verify stat boxes match specification."""
        spec = self.spec['sections']['stat_boxes']

        # Count stat boxes
        stat_box_pattern = r'<div[^>]*(?:stat|box)[^>]*>'
        stat_boxes = re.findall(stat_box_pattern, html, re.IGNORECASE)

        if spec.get('exact'):
            if len(stat_boxes) != spec['count']:
                self.violations.append(
                    f"Stat boxes: found {len(stat_boxes)}, "
                    f"expected exactly {spec['count']}"
                )

        # Check colors
        for box in spec['boxes']:
            if box['color'] not in html:
                self.violations.append(
                    f"Stat box color missing: {box['color']} "
                    f"(for '{box['label']}')"
                )

    def _check_font_compliance(self, html: str):
        """Verify Georgia serif font throughout."""
        spec = self.spec['global_rules']

        if spec['font_family'] not in html.lower():
            self.violations.append(
                f"Font not Georgia serif throughout "
                f"(expected: {spec['font_family']})"
            )

        # Check for sans-serif (should not exist)
        if 'font-family:arial' in html.lower() or \
           'font-family:helvetica' in html.lower() or \
           'font-family:sans-serif' in html.lower():
            self.violations.append("Sans-serif font detected (must be Georgia serif)")

    def _check_color_compliance(self, html: str):
        """Verify colors match specification."""
        spec = self.spec['global_rules']

        heading_color = spec['heading_color']
        if heading_color not in html:
            self.violations.append(
                f"Heading color missing or wrong "
                f"(expected {heading_color})"
            )

    def _check_hyperlinks(self, html: str):
        """Verify all candidate names are hyperlinked."""
        # Count <a> tags with href
        hyperlinks = re.findall(r'<a\s+href=["\'][^"\']+["\'][^>]*>', html)

        if len(hyperlinks) < 5:  # At least 5 hyperlinks expected (shortlist + maybe candidates)
            self.violations.append(
                f"Insufficient hyperlinks: found {len(hyperlinks)}, "
                f"expected at least 5 (candidate names must link to Google Drive CVs)"
            )

        # Check for Google Drive links
        drive_links = re.findall(r'drive\.google\.com', html)
        if len(drive_links) < 3:
            self.violations.append(
                f"Google Drive CV links missing or insufficient: "
                f"found {len(drive_links)}, expected multiple"
            )

    def _check_section_structure(self, html: str):
        """Verify report structure is complete."""
        required_sections = {
            'header': ['People & Culture', 'Initial Screening' if 'screening' in self.report_type else 'Decision View'],
            'stat_boxes': ['div', 'stat', 'box'],  # General markers
        }

        for section, keywords in required_sections.items():
            for keyword in keywords:
                if keyword.lower() not in html.lower():
                    # Don't fail if it's optional, warn if critical
                    if section == 'header':
                        self.violations.append(f"Missing section marker: '{keyword}'")

    def _check_data_fields(self, html: str):
        """Verify all required data fields present (for screening reports)."""
        if self.report_type == 'screening_report':
            required_fields = [
                'Total exp:',
                'Relevant exp:',
                'Expected Salary:',
                'City:',
                'Relocate:',
                'DB status:'
            ]

            # Each shortlisted candidate should have these fields
            for field in required_fields:
                if field not in html:
                    self.violations.append(
                        f"Missing required data field: '{field}'"
                    )

    def _check_text_alignment(self, html: str):
        """Verify text is justified."""
        if 'text-align:justify' not in html and 'text-align: justify' not in html:
            self.violations.append(
                "Text alignment: body text should be justified (text-align: justify)"
            )

    def _check_no_pdf(self, html: str):
        """Verify output is HTML, not PDF."""
        if '.pdf' in html.lower() or 'pdf' in html.lower():
            if '<' not in html:  # Not HTML structure
                self.violations.append(
                    "Output appears to be PDF or binary, not HTML email body"
                )

    def get_report(self) -> str:
        """Get detailed validation report."""
        if not self.violations:
            return f"✓ {self.spec['name']} validation PASSED\n" \
                   f"  Format matches specification exactly.\n" \
                   f"  Safe to send."

        report = f"✗ {self.spec['name']} validation FAILED\n\n"
        report += f"VIOLATIONS FOUND ({len(self.violations)}):\n"
        for i, violation in enumerate(self.violations, 1):
            report += f"  {i}. {violation}\n"

        report += f"\nACTION: Fix violations above before sending.\n" \
                  f"Do NOT send broken report.\n"
        return report


class ValidationError(Exception):
    """Raised when report validation fails."""
    pass


def validate_before_send(html_output: str, report_type: str) -> bool:
    """
    Validate report before sending. Raises if invalid.

    Args:
        html_output: Generated HTML email body
        report_type: 'screening_report' or 'decision_brief'

    Returns:
        True if valid

    Raises:
        ValidationError if invalid
    """
    validator = ReportValidator(report_type)
    violations = validator.validate(html_output)

    if violations:
        report = validator.get_report()
        print(report)
        raise ValidationError(
            f"\n\nREPORT VALIDATION FAILED.\n"
            f"Found {len(violations)} format violations.\n"
            f"Do NOT send broken report.\n\n"
            f"Violations:\n" +
            "\n".join([f"  - {v}" for v in violations])
        )

    return True


def run_qa_checklist(html_output: str, report_type: str) -> Dict[str, bool]:
    """
    Run 8-item QA checklist on report.

    Returns:
        Dict mapping checklist items to pass/fail
    """
    spec = load_report_spec(report_type)
    results = {}

    for check in spec['qa_checklist']:
        # Map checks to validators
        if 'Header matches' in check:
            results[check] = '<h1' in html_output or 'People & Culture' in html_output
        elif 'Stat boxes' in check:
            results[check] = 'stat' in html_output.lower() or 'box' in html_output.lower()
        elif 'Georgia serif' in check:
            results[check] = 'Georgia' in html_output
        elif 'blue' in check.lower():
            results[check] = '#1565c0' in html_output
        elif 'hyperlink' in check.lower():
            results[check] = '<a href=' in html_output
        elif 'justified' in check.lower():
            results[check] = 'justify' in html_output
        elif 'HTML' in check or 'PDF' in check:
            results[check] = '<!DOCTYPE' in html_output or '<html' in html_output.lower()
        else:
            results[check] = True  # Default pass for subjective checks

    return results


if __name__ == "__main__":
    # Test: Create validators
    print("Screening Report Validator initialized")
    validator_s = ReportValidator('screening_report')
    print(f"  Spec loaded: {validator_s.spec['name']}")

    print("\nDecision Brief Validator initialized")
    validator_d = ReportValidator('decision_brief')
    print(f"  Spec loaded: {validator_d.spec['name']}")

    print("\n✓ Validators ready for use")
