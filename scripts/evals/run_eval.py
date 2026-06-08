#!/usr/bin/env python3
"""
CLI runner for candidate communication email evaluation.

Usage:
    python run_eval.py --file path/to/draft.html --type warm_bench [--subject "Subject Line"] [--pilot-mode]
    python run_eval.py --text "<html>...</html>" --type values_feedback
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path so we can import candidate_communication_eval
sys.path.insert(0, str(Path(__file__).parent))

from candidate_communication_eval import evaluate_email


def format_result(result):
    """Pretty-print evaluation result."""
    print("\n" + "=" * 80)
    print("CANDIDATE COMMUNICATION EMAIL EVALUATION REPORT")
    print("=" * 80)

    status = "PASS" if result['passed'] else "BLOCKED"
    print(f"\nOVERALL STATUS: {status}")
    print(f"  Word Count: {result['word_count']} words")

    if not result['violations']:
        print("\nAll checks passed!")
        return 0  # Exit code 0 = success

    print(f"\n  Total Violations: {len(result['violations'])}")

    # Group by severity
    hard_blocks = [v for v in result['violations'] if v['severity'] == 'HARD_BLOCK']
    warnings = [v for v in result['violations'] if v['severity'] == 'WARNING']

    if hard_blocks:
        print("\n[HARD BLOCKS - blocking send]:")
        for i, v in enumerate(hard_blocks, 1):
            print(f"\n  {i}. {v['rule']}")
            print(f"     {v['detail']}")

    if warnings:
        print("\n[WARNINGS - logged but allowed]:")
        for i, v in enumerate(warnings, 1):
            print(f"\n  {i}. {v['rule']}")
            print(f"     {v['detail']}")

    print("\n" + "=" * 80)

    # Exit code: 2 if hard blocks, 0 if warnings only
    if hard_blocks:
        print("RESULT: Email BLOCKED due to hard block violations.")
        return 2
    else:
        print("RESULT: Email allowed but has warnings. Review before sending.")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate candidate communication email drafts.'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Path to draft email HTML file'
    )
    parser.add_argument(
        '--text',
        type=str,
        help='Email HTML content as inline string'
    )
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        choices=['cv_rejection', 'values_feedback', 'warm_bench', 'gwc_rejection'],
        help='Email type'
    )
    parser.add_argument(
        '--subject',
        type=str,
        default='Draft Email',
        help='Email subject line (for PILOT prefix check)'
    )
    parser.add_argument(
        '--pilot-mode',
        action='store_true',
        default=True,
        help='Set PILOT_MODE=True (default)'
    )
    parser.add_argument(
        '--live-mode',
        action='store_true',
        help='Set PILOT_MODE=False (overrides --pilot-mode)'
    )

    args = parser.parse_args()

    # Get HTML content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                html_body = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return 1
    elif args.text:
        html_body = args.text
    else:
        print("Error: Must provide either --file or --text")
        return 1

    # Determine pilot mode
    pilot_mode = not args.live_mode

    # Run evaluation
    result = evaluate_email(
        html_body=html_body,
        subject=args.subject,
        email_type=args.type,
        pilot_mode=pilot_mode,
    )

    # Print and return
    exit_code = format_result(result)
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
