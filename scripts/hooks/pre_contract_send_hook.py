#!/usr/bin/env python3
"""
PreToolUse hook — blocks contract/NDA sends that fail the Skill 07 docx eval.

Fires on Bash commands that run a contract send script. Validates the most
recently built package under output/contracts/ and blocks the send if any HARD
BLOCK is present.

Every rule it enforces comes from a defect that actually reached Ayesha in a
pilot (Muhammad Shayan Fellow package, 2026-08-13 — three review rounds).

Exit codes:
    0 = allow (clean, warnings only, or not a contract send)
    2 = HARD BLOCK — send blocked
"""

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "evals"))

OUTPUT_DIR = ROOT / "output" / "contracts"
LOG = ROOT / "logs" / "email_audit.log"

# Commands that mean "a contract package is about to go out"
TRIGGERS = ("send_contract", "contract_package", "contracts/send_")


def log(msg, level="INFO"):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] [{level}] {msg}\n")
    except Exception:
        pass


def newest_package():
    """The package directory containing the most recently written .docx."""
    if not OUTPUT_DIR.exists():
        return None
    docs = list(OUTPUT_DIR.glob("*/*.docx"))
    if not docs:
        return None
    return max(docs, key=lambda p: p.stat().st_mtime).parent


def infer_type(package: Path) -> str:
    names = " ".join(p.name.lower() for p in package.glob("*.docx"))
    if "fellow" in names:
        return "fellow"
    if "addendum" in names:
        return "addendum"
    if "project" in names:
        return "project"
    return "fulltime"


def main():
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        return 0  # never block on a malformed hook payload

    command = (hook_input.get("tool_input") or {}).get("command", "") or ""
    if not any(t in command for t in TRIGGERS):
        return 0

    try:
        from contract_docx_eval import evaluate_contract
    except ImportError as e:
        log(f"contract hook could not import evaluator: {e}", "WARN")
        return 0

    package = newest_package()
    if package is None:
        return 0

    doc_type = infer_type(package)
    all_blocks, all_warns = [], []
    for doc in sorted(package.glob("*.docx")):
        try:
            blocks, warns = evaluate_contract(doc, doc_type)
        except Exception as e:
            log(f"contract eval error on {doc.name}: {e}", "WARN")
            continue
        all_blocks += [f"{doc.name}: {b}" for b in blocks]
        all_warns += [f"{doc.name}: {w}" for w in warns]

    # PDF page-placement: no heading may be stranded away from its content.
    # Property checks alone gave a false pass on this once ("OFFER ACCEPTANCE:").
    try:
        from verify_pdf_layout import verify as verify_layout

        for docx in sorted(package.glob("*.docx")):
            pdf = docx.with_suffix(".pdf")
            if pdf.exists():
                _, problems, _ = verify_layout(docx, pdf)
                all_blocks += [f"{pdf.name}: split section — {p}" for p in problems]
    except Exception as e:
        log(f"pdf layout check skipped: {e}", "WARN")

    # Joining-email rules: read the send script being run and check the email
    # body against the locked Fellow templates (paid vs volunteer package rule).
    try:
        from contract_docx_eval import evaluate_joining_email
        import re

        # Pick the SEND script specifically. A command can name several .py files
        # (e.g. running the validator first); scanning the wrong one reads the
        # validator's own marker strings as if they were email body text.
        candidates = [
            c for c in re.findall(r"([\w/\\.\-]+\.py)", command)
            if "send" in Path(c).name.lower()
        ]
        if candidates:
            script = (ROOT / candidates[0]).resolve()
            if script.exists():
                raw = script.read_text(encoding="utf-8", errors="ignore")

                # BEST CASE: if the script can render its own email, check the real
                # output. Static source scanning cannot connect a value held in a
                # dict to bold styling applied in a separate function.
                rendered = None
                try:
                    import importlib.util

                    spec = importlib.util.spec_from_file_location(
                        "_send_mod", str(script))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "render") and hasattr(mod, "COACHES"):
                        rendered = mod.render(next(iter(mod.COACHES)))
                    elif hasattr(mod, "build_html") and hasattr(mod, "COACHES"):
                        rendered = mod.build_html(next(iter(mod.COACHES.values())))
                    elif hasattr(mod, "BODY"):
                        rendered = mod.BODY
                except (Exception, SystemExit) as e:  # noqa: BLE001
                    # A render failure must never take the hook down — fall back
                    # to scanning the source.
                    log(f"could not render {script.name} for eval: {e}", "WARN")

                if rendered:
                    raw = rendered
                    # Mobile check runs on the RENDERED html: a fixed width
                    # attribute pins the layout and phones just zoom out.
                    try:
                        from verify_email_responsive import check as resp_check

                        rp, _ = resp_check(rendered, script.name)
                        all_blocks += [f"{script.name}: {p}" for p in rp]
                    except Exception as e:  # noqa: BLE001
                        log(f"responsive check skipped: {e}", "WARN")
                # Strip python comments and the module docstring so developer
                # notes are not mistaken for email body text.
                raw = re.sub(r'^\s*""".*?"""', "", raw, flags=re.S)
                body = "\n".join(
                    ln for ln in raw.splitlines() if not ln.lstrip().startswith("#")
                )
                # only count files the script actually attaches
                attachments = [
                    d.name
                    for d in list(package.glob("*.docx")) + list(package.glob("*.pdf"))
                    if d.name in body
                ]
                # An internal package-review note to Ayesha is NOT a candidate
                # email, so the candidate-email content rules (no meta-commentary,
                # locked links, bold key details) do not apply. The script must
                # declare itself, and it must not address anyone outside
                # taleemabad.com — the document checks above still run either way.
                # A script may render an external .html template — the markup (and
                # therefore the bolding) lives there, not in the .py. Append any
                # referenced template so the content checks see the real email.
                for tpl in re.findall(r'["\']([^"\']+\.html)["\']', raw):
                    tpl_path = Path(tpl)
                    if not tpl_path.is_absolute():
                        tpl_path = ROOT / tpl
                    if tpl_path.exists():
                        raw += "\n" + tpl_path.read_text(
                            encoding="utf-8", errors="ignore")

                # Resolve simple module-level string constants and f-string tag
                # shorthands so the scanned text approximates the RENDERED email.
                # Without this, `<{B}>{START_DATE}</b>` looks unbolded to the
                # content checks even though it renders bold.
                consts = dict(
                    re.findall(r'^([A-Z][A-Z0-9_]*)\s*=\s*"([^"\n]*)"', body, re.M)
                )
                for _ in range(2):   # constants can reference constants
                    for k, v in consts.items():
                        body = body.replace("{" + k + "}", v)
                body = body.replace("<{B}>", "<b>").replace("<{S}>", "<span>")

                declared_internal = "INTERNAL_REVIEW = True" in body
                external = re.findall(r"[\w.+-]+@(?!taleemabad\.com)[\w.-]+\.\w+", body)
                if declared_internal and not external:
                    log("internal review email — candidate-email rules skipped")
                else:
                    eb, ew = evaluate_joining_email(body, attachments)
                    all_blocks += eb
                    all_warns += ew
    except Exception as e:
        log(f"joining-email eval skipped: {e}", "WARN")

    if all_blocks:
        print(
            "\nCONTRACT SEND BLOCKED — Skill 07 docx eval failed\n"
            f"  package: {package}\n",
            file=sys.stderr,
        )
        for b in all_blocks:
            print(f"  HARD BLOCK: {b}", file=sys.stderr)
        print(
            "\n  Fix the document and rebuild before sending. See "
            ".claude/skills/07_contract-drafting/fellow-contracts.md\n",
            file=sys.stderr,
        )
        log(f"CONTRACT BLOCKED | {package.name} | {len(all_blocks)} violations", "ERROR")
        return 2

    for w in all_warns:
        print(f"  contract warning: {w}", file=sys.stderr)
    log(f"CONTRACT EVAL PASSED | {package.name} | {len(all_warns)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
