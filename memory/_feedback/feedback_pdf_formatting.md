---
name: PDF Formatting — Justified Text
description: All ReportLab PDFs must use TA_JUSTIFY for body text — confirmed by user 2026-04-02
type: feedback
---

Always use `alignment=TA_JUSTIFY` on body paragraph styles in all ReportLab PDFs.

**Why:** User flagged that left-aligned body text in the Job 36 rejection pilot PDF looked unpolished. Justified text is the standard.

**How to apply:** In every script that builds a PDF with ReportLab, ensure the body `ParagraphStyle` includes `alignment=TA_JUSTIFY`. Import `TA_JUSTIFY` from `reportlab.lib.enums`. Applies to all PDF types: screening reports, pilot drafts, rejection email compilations, KCD reports, anything with body text paragraphs.
