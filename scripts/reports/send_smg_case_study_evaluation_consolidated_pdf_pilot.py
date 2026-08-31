"""
SMG Case Study Evaluation - CONSOLIDATED, SINGLE PDF (Job 42) - PILOT to Ayesha.

Ayesha 2026-08-31: "send me a pdf of the report on ayesha.khan".

CONTENT IS THE SAME EVALUATION as send_smg_case_study_evaluation_combined_pilot.py, imported
from it so there is ONE source of truth for all nine candidates. Nothing is re-scored here;
the three-part email and this PDF are the same words.

Formatting per memory/feedback_pdf_formatting.md: ReportLab, TA_JUSTIFY on all body text.
Georgia registered from C:\\Windows\\Fonts so that arrows, em dashes and symbols render.

NOTE (CLAUDE.md Rule 14): there is no Word/LibreOffice/PDF viewer on this machine. Page
counts, fonts and flow are verified structurally with PyMuPDF - that is NOT visual proof.
Ayesha must eyeball the PDF before it goes to the hiring manager.
"""

import importlib.util
import os
import re
import smtplib
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                               PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from scripts.utils.safe_send import safe_sendmail  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SENDER = "ayesha.khan@taleemabad.com"
RECIPIENTS = ["ayesha.khan@taleemabad.com"]
SUBJECT = "[PILOT - ] SMG Case Study - Consolidated Evaluation Report, 9 candidates (single PDF) | Job 42"
OUT_PDF = os.path.join(ROOT, "output", "reports",
                       "SMG_Case_Study_Evaluation_Consolidated_2026-08-31.pdf")

# ---- single source of truth: import the evaluated content ----
_spec = importlib.util.spec_from_file_location(
    "_comb", os.path.join(os.path.dirname(__file__),
                          "send_smg_case_study_evaluation_combined_pilot.py"))
_v2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v2)
CANDS, DIMS = _v2.CANDS, _v2.DIMS

NAVY = colors.HexColor("#1a2b4c")
BLUE = colors.HexColor("#2f4fa2")
MIDBLUE = colors.HexColor("#2f6fb5")
GREEN = colors.HexColor("#1b7f4d")
RED = colors.HexColor("#b3261e")
BROWN = colors.HexColor("#7b341e")
PURPLE = colors.HexColor("#5b3fc4")
GREY = colors.HexColor("#6b7a90")
LIGHT = colors.HexColor("#f5f7fa")
RULE = colors.HexColor("#dfe3ea")

FONTS = r"C:\Windows\Fonts"
for name, fn in [("Georgia", "georgia.ttf"), ("Georgia-Bold", "georgiab.ttf"),
                 ("Georgia-Italic", "georgiai.ttf"), ("Georgia-BoldItalic", "georgiaz.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, fn)))
pdfmetrics.registerFontFamily("Georgia", normal="Georgia", bold="Georgia-Bold",
                              italic="Georgia-Italic", boldItalic="Georgia-BoldItalic")

BODY = ParagraphStyle("body", fontName="Georgia", fontSize=9.4, leading=14.6,
                      alignment=TA_JUSTIFY, textColor=colors.HexColor("#22303f"),
                      spaceAfter=0)
LABEL = ParagraphStyle("label", fontName="Georgia-Bold", fontSize=7.4, leading=10,
                       alignment=TA_LEFT, spaceBefore=7, spaceAfter=3)
H1 = ParagraphStyle("h1", fontName="Georgia-Bold", fontSize=14, leading=18,
                    textColor=NAVY, spaceBefore=4, spaceAfter=6)
CARDNAME = ParagraphStyle("cardname", fontName="Georgia-Bold", fontSize=13, leading=17,
                          textColor=colors.white)
CARDMETA = ParagraphStyle("cardmeta", fontName="Georgia", fontSize=8.6, leading=12,
                          textColor=colors.HexColor("#e4ecf8"))
DOCNAME = ParagraphStyle("docname", fontName="Georgia-Bold", fontSize=8.6, leading=12,
                         textColor=NAVY)
DOCTYPE = ParagraphStyle("doctype", fontName="Georgia", fontSize=8.2, leading=12,
                         textColor=MIDBLUE)
DOCDESC = ParagraphStyle("docdesc", fontName="Georgia", fontSize=8.6, leading=12.4,
                         textColor=colors.HexColor("#3d4c5c"), alignment=TA_JUSTIFY)
VERDICT = ParagraphStyle("verdict", fontName="Georgia-Bold", fontSize=9.6, leading=13,
                         textColor=colors.white)
PROBE = ParagraphStyle("probe", fontName="Georgia", fontSize=9.2, leading=13.8,
                       alignment=TA_JUSTIFY, textColor=colors.HexColor("#22303f"),
                       leftIndent=12, bulletIndent=0, spaceAfter=4)
TCELL = ParagraphStyle("tcell", fontName="Georgia", fontSize=8.4, leading=11.6)
THEAD = ParagraphStyle("thead", fontName="Georgia-Bold", fontSize=8.2, leading=11,
                       textColor=colors.white)

ENT = {"&mdash;": "\u2014", "&ndash;": "\u2013", "&middot;": "\u00b7", "&nbsp;": " ",
       "&amp;": "&", "&quot;": '"', "&#39;": "'"}


def rl(s):
    """HTML fragment -> ReportLab inline markup. Leaves &lt;/&gt; intact."""
    s = re.sub(r"\s+", " ", s).strip()
    for k, v in ENT.items():
        s = s.replace(k, v)
    s = s.replace("<strong>", "<b>").replace("</strong>", "</b>")
    s = s.replace("<em>", "<i>").replace("</em>", "</i>")
    s = re.sub(r"<br\s*/?>", "<br/>", s)
    return s


def label(text, colour):
    return Paragraph(f'<font color="{colour.hexval()}">{text.upper()}</font>', LABEL)


def banner(text, bg, style=VERDICT, pad=6):
    t = Table([[Paragraph(text, style)]], colWidths=[168 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), pad),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]))
    return t


def stat_boxes():
    data = [("9", "Scored", NAVY), ("29", "Documents read", MIDBLUE),
            ("6", "Recommended", GREEN), ("2", "Still blocked", RED)]
    cells = []
    for n, l, c in data:
        inner = Table([[Paragraph(f'<font color="white" size="17"><b>{n}</b></font>', TCELL)],
                       [Paragraph(f'<font color="#dbe5f5" size="7">{l.upper()}</font>', TCELL)]],
                      colWidths=[38 * mm])
        inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), c),
                                   ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                   ("TOPPADDING", (0, 0), (-1, 0), 7),
                                   ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
                                   ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
                                   ("TOPPADDING", (0, -1), (-1, -1), 0)]))
        cells.append(inner)
    outer = Table([cells], colWidths=[42 * mm] * 4)
    outer.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return outer


def ranking_table():
    head = [Paragraph("Candidate", THEAD), Paragraph("Total", THEAD)]
    head += [Paragraph(d, THEAD) for d in DIMS]
    head += [Paragraph("Band", THEAD)]
    rows = [head]
    for c in CANDS:
        nm = (f'<a href="{c["link"]}" color="#2f4fa2">{c["name"]}</a><br/>'
              f'<font size="7" color="#6b7a90">App {c["app"]} \u00b7 '
              f'{len(c["docs"])} doc{"s" if len(c["docs"]) > 1 else ""}</font>')
        row = [Paragraph(nm, TCELL),
               Paragraph(f'<b><font size="11">{c["total"]}</font></b>', TCELL)]
        row += [Paragraph(str(s), TCELL) for s in c["scores"]]
        row += [Paragraph(f'<font size="7" color="white"><b>{c["band"]}</b></font>', TCELL)]
        rows.append(row)
    widths = [43 * mm, 12 * mm] + [14 * mm] * 6 + [25 * mm]
    t = Table(rows, colWidths=widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("ALIGN", (1, 0), (-1, -1), "CENTER"),
             ("GRID", (0, 0), (-1, -1), 0.4, RULE),
             ("TOPPADDING", (0, 0), (-1, -1), 4),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i, c in enumerate(CANDS, start=1):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
        style.append(("BACKGROUND", (-1, i), (-1, i), c["colour"]))
    t.setStyle(TableStyle(style))
    return t


def doc_block(c):
    rows = [[Paragraph(f"Submitted \u2014 {len(c['docs'])} document"
                       f"{'s' if len(c['docs']) > 1 else ''}",
                       ParagraphStyle("dh", parent=DOCNAME, fontSize=7.6, textColor=NAVY)),
             "", ""]]
    for n, t, d in c["docs"]:
        rows.append([Paragraph(rl(n), DOCNAME), Paragraph(rl(t), DOCTYPE),
                     Paragraph(rl(d), DOCDESC)])
    rows.append([Paragraph(rl(c["docs_note"]), DOCDESC), "", ""])
    t = Table(rows, colWidths=[42 * mm, 34 * mm, 92 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("SPAN", (0, 0), (-1, 0)),
        ("SPAN", (0, len(rows) - 1), (-1, len(rows) - 1)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBEFORE", (0, 0), (0, -1), 1.6, MIDBLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return t


SECTIONS = [
    ("Assignment 1 \u2014 what the analysis actually says", "a1", GREEN),
    ("Assignment 1 \u2014 what they called noise", GREY, None),
    ("Assignment 1 \u2014 the two priorities they chose", "a1_pri", GREEN),
    ("Assignment 1 \u2014 the three experiments", "a1_exp", BLUE),
    ("Assignment 2 \u2014 the growth loop", "a2", BLUE),
    ("Assignment 2 \u2014 how they measure K", "a2_k", BLUE),
    ("Assignment 2 \u2014 where they say it breaks", "a2_breaks", BLUE),
    ("Assignment 3 \u2014 the five-week plan", "a3", BROWN),
    ("Assignment 3 \u2014 the email to the DEO", "a3_email", BROWN),
    ("Assignment 3 \u2014 the internal update", "a3_internal", BROWN),
    ("Reflective response", "reflection", PURPLE),
    ("What I verified against the raw data", "verified", GREEN),
    ("What is thin, missing or wrong", "thin", RED),
]


def candidate_flow(c):
    f = [banner(f'<font size="12"><b>{c["name"]}</b></font>'
                f'<font size="8.6" color="#e4ecf8">   \u00b7   App {c["app"]}'
                f'   \u00b7   {c["total"]}/100   \u00b7   {c["band"]}</font>',
                c["colour"], style=CARDNAME, pad=7),
         Spacer(1, 5), doc_block(c), Spacer(1, 2)]
    f.append(label("Assignment 1 \u2014 what the analysis actually says", GREEN))
    f.append(Paragraph(rl(c["a1"]), BODY))
    f.append(label("Assignment 1 \u2014 what they called noise", GREY))
    f.append(Paragraph(rl(c["a1_noise"]), BODY))
    for title, key, col in SECTIONS[2:]:
        if key == "a3":
            f.append(Spacer(1, 5))
            f.append(banner(f'<font color="#1a2b4c" size="9"><b>Assignment 3 \u2014 their stated '
                            f'probability:</b> {rl(c["a3_prob"])}</font>',
                            colors.HexColor("#eef3fb"), style=TCELL, pad=5))
            f.append(Spacer(1, 2))
        f.append(label(title, col))
        f.append(Paragraph(rl(c[key]), BODY))
    f.append(Spacer(1, 7))
    f.append(banner("PROCEED to case study debrief" if c["proceed"]
                    else "DO NOT proceed to debrief", GREEN if c["proceed"] else RED))
    f.append(label("Debrief probes", BLUE))
    for i, p in enumerate(c["probes"], 1):
        f.append(Paragraph(rl(p), PROBE, bulletText=f"{i}."))
    return f


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 26 * mm, w, 26 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#93a7c9"))
    canvas.setFont("Georgia", 7.4)
    canvas.drawString(21 * mm, h - 11 * mm, "TALEEMABAD  \u00b7  TALENT ACQUISITION")
    canvas.setFillColor(colors.white)
    canvas.setFont("Georgia-Bold", 13)
    canvas.drawString(21 * mm, h - 17.5 * mm, "SMG Case Study \u2014 Consolidated Evaluation Report")
    canvas.setFillColor(colors.HexColor("#c3d0e6"))
    canvas.setFont("Georgia", 8)
    canvas.drawString(21 * mm, h - 22.5 * mm,
                      "Job 42  \u00b7  Senior Manager Growth  \u00b7  31 August 2026")
    canvas.setStrokeColor(RULE)
    canvas.line(21 * mm, 15 * mm, w - 21 * mm, 15 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Georgia", 7.4)
    canvas.drawString(21 * mm, 10.5 * mm,
                     "Taleemabad Talent Acquisition  \u00b7  hiring@taleemabad.com")
    canvas.drawRightString(w - 21 * mm, 10.5 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build_pdf(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=21 * mm, rightMargin=21 * mm,
                          topMargin=31 * mm, bottomMargin=19 * mm,
                          title="SMG Case Study - Consolidated Evaluation Report, 9 candidates (Job 42)",
                          author="Taleemabad Talent Acquisition")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])

    intro = (
        "All nine Senior Manager Growth case studies from this batch, in one document, "
        "written so that reading it replaces reading the submissions. Every deliverable was "
        "read end to end \u2014 narrative pages, slides and every spreadsheet tab with "
        "formulas preserved \u2014 and every headline figure was recomputed from the raw "
        "546-row master dataset rather than checked against our own summary table. "
        "<b>Nobody fabricated data.</b> Each candidate is covered assignment by assignment, "
        "with what they found, the numbers they used, the experiments they designed, how they "
        "would measure the loop, their stalled-deal probability, and what is thin. "
        "<b>No previously reported score has moved</b> \u2014 this is the same evaluation as "
        "the three-part email, in one artefact. <b>Khushal Kakar enters at the top on 98</b>, "
        "and did so after losing two days unable to open the brief.")

    story = [stat_boxes(), Spacer(1, 10), Paragraph(intro, BODY), Spacer(1, 12),
             Paragraph("Ranking", H1), ranking_table(), Spacer(1, 4),
             Paragraph('<font size="7.6" color="#6b7a90">Dimensions scored 1\u20135. Weights: '
                       'Data 20% \u00b7 Execution 25% \u00b7 Stakeholder 20% \u00b7 Commercial '
                       '15% \u00b7 Discipline 10% \u00b7 Signal 10%. Bands: 80+ strong yes '
                       '\u00b7 65\u201379 yes \u00b7 50\u201364 borderline \u00b7 under 50 no. '
                       'Six of the nine are recommended for debrief.</font>', TCELL),
             Spacer(1, 12), Paragraph("What separates them", H1)]

    for para in _v2.SEPARATES.split("<p ")[1:]:
        txt = para.split(">", 1)[1].rsplit("</p>", 1)[0]
        story += [Paragraph(rl(txt), BODY), Spacer(1, 6)]

    for c in CANDS:
        story.append(PageBreak())
        story += candidate_flow(c)

    story.append(PageBreak())
    story.append(Paragraph("Outstanding", H1))
    for para in _v2.BLOCKED.split("<p ")[1:]:
        txt = para.split(">", 1)[1].rsplit("</p>", 1)[0]
        story += [Paragraph(rl(txt), BODY), Spacer(1, 6)]

    story.append(Spacer(1, 10))
    story.append(Paragraph("Method &amp; limits", H1))
    for para in _v2.METHOD.split("<p ")[1:]:
        txt = para.split(">", 1)[1].rsplit("</p>", 1)[0]
        story += [Paragraph(rl(txt), BODY), Spacer(1, 6)]

    doc.build(story)
    return path


def main():
    load_dotenv(os.path.join(ROOT, ".env"))
    pw = os.getenv("EMAIL_PASSWORD")
    if not pw:
        raise SystemExit("EMAIL_PASSWORD missing")
    path = build_pdf(OUT_PDF)

    import fitz
    d = fitz.open(path)
    txt = "".join(p.get_text() for p in d)
    for c in CANDS:
        assert c["name"] in txt, f"MISSING from PDF: {c['name']}"
    assert "Method & limits" in txt or "Method &" in txt, "method section missing"
    assert "Outstanding" in txt, "outstanding section missing"
    print(f"PDF built: {path}\n  pages={len(d)}  size={os.path.getsize(path):,} bytes  "
          f"chars={len(txt):,}")
    for c in CANDS:
        assert c["probes"][0][:40] in txt, f"probes missing for {c['name']}"
    print(f"  structural checks passed: all {len(CANDS)} candidates, probes, "
          f"outstanding and method present")
    print("  NOTE: structural != visual. Ayesha must eyeball the PDF (CLAUDE.md Rule 14).")

    body = (
        "Hi Ayesha,\n\n"
        "The consolidated SMG case study evaluation as one PDF - all nine candidates, "
        f"covered assignment by assignment. {len(d)} pages.\n\n"
        "Same content as the three-part email sent today, in one forwardable artefact. "
        "No previously reported score has moved.\n\n"
        "Ranking: Khushal Kakar 98, Furqan Afzal 93, Hania Khan 90, Vaneeza Baig 82, "
        "Shafaq Syed 75, Lamis Maniar 73, Kanooz Siddiqui 62, Ali Wajdan Khan 49, "
        "Rimsha Taj 45. Six of the nine are recommended for debrief.\n\n"
        "Every headline figure was recomputed from the raw 546-row dataset rather than "
        "checked against our own summary table. Nobody fabricated data.\n\n"
        "Still outstanding and stated in the report: Ahmad Taj (12 days, the ZIP never "
        "arrived anywhere), and Zeshan Nawaz and Bilal Sadiq, sent the case study on "
        "7 August and never nudged.\n\n"
        "Please eyeball the layout before this goes to the hiring manager - I have no PDF "
        "viewer here, so I can verify the contents structurally but not how the pages "
        "look.\n\n"
        "Coco")

    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = ", ".join(RECIPIENTS)
    msg.attach(MIMEText(body, "plain"))
    with open(path, "rb") as fh:
        att = MIMEApplication(fh.read(), _subtype="pdf")
    att.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
    msg.attach(att)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(SENDER, pw)
    safe_sendmail(s, SENDER, RECIPIENTS, msg.as_string(),
                  context="smg_case_study_evaluation_consolidated_pdf")
    s.quit()
    print(f"Sent to {RECIPIENTS} with {os.path.basename(path)} attached")


if __name__ == "__main__":
    main()
