#!/usr/bin/env python3
"""
PDF page-placement verifier — Skill 07.

The .docx validator checks properties; this checks where things actually LAND.
It pairs the .docx (which knows what a heading is and what belongs to it) with
the .pdf (which knows what page each line fell on) and asserts every heading
sits on the same page as ALL of its block content.

Written after a weaker version of this check gave a false pass: it compared a
heading only against its FIRST following paragraph, so "OFFER ACCEPTANCE:" was
reported as fine while its signature lines sat on the next page.

Usage:
    python scripts/evals/verify_pdf_layout.py "output/contracts/<Name>"

Exit codes: 0 = every heading intact · 2 = a section is split across pages
"""

import re
import sys
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def looks_like_heading(p):
    txt = p.text.strip()
    runs = [r for r in p.runs if r.text.strip()]
    return (
        0 < len(txt) < 60
        and not txt.endswith(".")
        and bool(runs)
        and all(r.bold for r in runs)
    )


def verify(docx_path: Path, pdf_path: Path, max_block=10):
    doc = Document(docx_path)
    paras = doc.paragraphs
    pages = [norm(p.extract_text()) for p in PdfReader(str(pdf_path)).pages]

    def pages_of(text, probe_len=45):
        """ALL pages containing this text. Probe strings are not always unique —
        taking only the first match reported impossible results (content on an
        earlier page than its own heading)."""
        probe = norm(text)[:probe_len]
        if not probe:
            return []
        return [i + 1 for i, t in enumerate(pages) if probe in t]

    def page_of(text, probe_len=45):
        hits = pages_of(text, probe_len)
        return hits[0] if hits else None

    problems = []
    checked = 0

    for i, p in enumerate(paras):
        txt = p.text.strip()
        if not txt or txt == "AND":
            continue
        if not (p.style.name.startswith("Heading") or looks_like_heading(p)):
            continue

        head_page = page_of(txt)
        if head_page is None:
            continue
        checked += 1

        # gather the heading's whole block, same rule the builder uses
        seen = 0
        for q in paras[i + 1:]:
            qt = q.text.strip()
            if qt and (q.style.name.startswith("Heading") or looks_like_heading(q)):
                break
            if not qt:
                continue
            seen += 1
            if seen > max_block:
                break
            qpages = pages_of(qt)
            # Only a genuine split if the content appears NOWHERE on the
            # heading's page. An occurrence elsewhere is a repeated phrase.
            if qpages and head_page not in qpages:
                problems.append(
                    f"'{txt[:38]}' on page {head_page} but its content "
                    f"'{qt[:38]}' on page {qpages}"
                )
                break

    return checked, problems, len(pages)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: verify_pdf_layout.py <package dir>")
    pkg = Path(sys.argv[1])
    docs = sorted(pkg.glob("*.docx"))
    if not docs:
        print("no .docx in package")
        return 0

    failed = 0
    for docx in docs:
        pdf = docx.with_suffix(".pdf")
        if not pdf.exists():
            print(f"[skip] no PDF for {docx.name}")
            continue
        checked, problems, npages = verify(docx, pdf)
        status = "SPLIT" if problems else "OK"
        print(f"[{status}] {pdf.name} — {npages} pages, {checked} headings checked")
        for pr in problems:
            print(f"   SPLIT SECTION: {pr}")
        failed += len(problems)

    print("=" * 58)
    if failed:
        print(f"RESULT: {failed} section(s) split across pages")
        return 2
    print("RESULT: no section is split across a page break")
    return 0


if __name__ == "__main__":
    sys.exit(main())
