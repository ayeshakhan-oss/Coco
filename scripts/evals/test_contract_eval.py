#!/usr/bin/env python3
"""
Regression test for the contract .docx validator.

Guards the guard: proves contract_docx_eval still catches every defect family
from the 2026-08-13 Muhammad Shayan session. If someone loosens a rule, this
fails loudly.

Run:  python scripts/evals/test_contract_eval.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from contract_docx_eval import evaluate_contract  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "Contracts" / "Fellow" / "Template - Project-based Employment Contract.docx"
NDA_MASTER = ROOT / "Contracts" / "Fellow" / "Template - NDA Fellow Employee.docx"

# Each defect family that reached Ayesha in a pilot must still be detected.
MUST_CATCH = [
    ("unresolved placeholder", "placeholders left unfilled"),
    ("yellow highlighting", "leftover highlight runs"),
    ("Mr./Mrs.", "unresolved salutation option"),
    ("NEW_PAGE", "forced page breaks between clauses"),
    ("empty auto-numbered paragraph", "stray orphan bullet"),
    ("right indent", "Annexure-A narrow-column defect"),
    ("two lines", "heading not split"),
    ("business-travel clause", "Fellow clause removal"),
    ("13-week / 3-month probation", "Fellow probation removal"),
    ("Base Salary line", "Fellow salary-split removal"),
    ("annual-leave entitlement", "required Fellow leave terms"),
]

failures = []


def check(condition, message):
    if condition:
        print(f"  PASS  {message}")
    else:
        print(f"  FAIL  {message}")
        failures.append(message)


def main():
    print("Contract validator regression test\n")

    if not MASTER.exists():
        print(f"SKIP — master not found at {MASTER}")
        return 0

    print("1. Raw master must be rejected (it is a template, not a contract):")
    blocks, _ = evaluate_contract(MASTER, "fellow")
    joined = " | ".join(blocks)
    check(len(blocks) > 0, f"master produces hard blocks ({len(blocks)} found)")
    for needle, label in MUST_CATCH:
        check(needle.lower() in joined.lower(), f"detects: {label}")

    print("\n2. NDA rules:")
    nda_blocks, _ = evaluate_contract(NDA_MASTER, "fellow")
    check(
        any("placeholder" in b for b in nda_blocks),
        "NDA master flagged for unfilled placeholders",
    )

    print("\n3. A finished package must pass (if one exists):")
    built = sorted((ROOT / "output" / "contracts").glob("*/Contract - * - Fellow.docx"))
    if not built:
        print("  SKIP  no built package on disk")
    else:
        target = built[0]
        b, w = evaluate_contract(target, "fellow")
        check(not b, f"{target.name} has zero hard blocks")

    print("\n" + "=" * 58)
    if failures:
        print(f"REGRESSION FAILURES: {len(failures)}")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All validator rules intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
