#!/usr/bin/env python3
"""
Mobile-responsiveness checker for candidate emails — Skill 07.

Written after Design 3 shipped looking fine on desktop and broken on mobile: the
outer table carried width="880" AND width:880px, which pins the layout so phones
just zoom out. max-width never gets a chance.

Fixed widths inside <!--[if mso]> conditional comments are IGNORED — those are
Outlook-only ghost tables and are the correct way to do this.

Usage:
    python scripts/evals/verify_email_responsive.py <file.html> [more.html ...]
    python scripts/evals/verify_email_responsive.py --script scripts/contracts/send_x.py

Exit codes: 0 = responsive · 2 = would break on mobile
"""

import argparse
import re
import sys
from pathlib import Path

MSO_BLOCK = re.compile(r"<!--\[if [^\]]*\]>.*?<!\[endif\]-->", re.S | re.I)
SAFE_PX = 320          # anything wider than a small phone is suspect


def strip_mso(html):
    """Remove Outlook-only conditional blocks; fixed widths there are fine."""
    return MSO_BLOCK.sub("", html)


def check(html, label):
    body = strip_mso(html)
    problems, notes = [], []

    # 1 — fixed width="NNN" attributes on structural elements
    for m in re.finditer(r"<(table|td|div)\b[^>]*\bwidth=\"(\d+)\"", body, re.I):
        tag, w = m.group(1).lower(), int(m.group(2))
        if w > SAFE_PX:
            problems.append(
                f'<{tag} width="{w}"> — a fixed width attribute pins the layout; '
                f'use width="100%" with max-width in CSS')

    # 2 — fixed width:NNNpx in style (max-width is fine)
    for m in re.finditer(r"(?<!max-)width:\s*(\d+)px", body, re.I):
        w = int(m.group(1))
        if w > SAFE_PX:
            problems.append(f"width:{w}px in a style — use max-width:{w}px instead")

    # 3 — images must be able to shrink
    for m in re.finditer(r"<img\b[^>]*>", body, re.I):
        tag = m.group(0)
        wm = re.search(r'width="(\d+)"', tag)
        if wm and int(wm.group(1)) > 200 and "max-width" not in tag:
            problems.append(
                f'<img width="{wm.group(1)}"> without max-width — will overflow')

    # 4 — a media query is expected, but must not be the ONLY stacking mechanism
    has_mq = "@media" in html
    has_fluid = "display:inline-block" in body and "max-width" in body
    multi_col = body.count("display:inline-block;width:100%;max-width") >= 2
    if multi_col and not has_fluid:
        problems.append("multi-column layout with no fluid-hybrid fallback")
    if not has_mq:
        notes.append("no @media block — fine only if the layout is fully fluid")
    if multi_col and has_fluid:
        notes.append("columns stack via fluid-hybrid (survives stripped <style>)")

    # 5 — tap targets
    for m in re.finditer(r"padding:\s*(\d+)(?:\.\d+)?px\s+\d+", body):
        pass  # informational only; button padding is asserted below
    if "btn" in body and "display:block !important" not in html:
        notes.append("buttons may not go full-width on mobile")

    return problems, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--script", help="python send script exposing render()/build_html()")
    args = ap.parse_args()

    targets = []
    for f in args.files:
        targets.append((Path(f).name, Path(f).read_text(encoding="utf-8")))

    if args.script:
        import importlib.util

        spec = importlib.util.spec_from_file_location("_m", args.script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "render"):
            html = mod.render(next(iter(mod.COACHES)))
        elif hasattr(mod, "build_html"):
            html = mod.build_html(next(iter(mod.COACHES.values())))
        elif hasattr(mod, "body_for"):
            html = mod.body_for(next(iter(mod.COACHES.values())))
        elif hasattr(mod, "BODY"):
            html = mod.BODY
        else:
            raise SystemExit(f"{args.script}: no render()/build_html()/body_for()/BODY")
        targets.append((Path(args.script).name + " (rendered)", html))

    if not targets:
        ap.error("pass an html file or --script")

    total = 0
    for label, html in targets:
        problems, notes = check(html, label)
        total += len(problems)
        print(f"\n[{'BREAKS' if problems else 'OK'}] {label}")
        for p in problems:
            print(f"   MOBILE BREAK: {p}")
        for n in notes:
            print(f"   note: {n}")
        if not problems:
            print("   no fixed widths outside Outlook conditionals")

    print("\n" + "=" * 58)
    if total:
        print(f"RESULT: {total} issue(s) that would break on mobile")
        return 2
    print("RESULT: responsive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
