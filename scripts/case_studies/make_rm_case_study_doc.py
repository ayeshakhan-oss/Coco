# -*- coding: utf-8 -*-
"""Generate the Regional Manager strategic case study as a Taleemabad-branded DOCX
(same locked layout as the SMG/GM/HOG case studies), then upload to Google Drive
as a native Google Doc.

Content is a faithful transcription of Ayesha's source document
"RM - Case Study .docx.pdf" — nothing added, nothing removed. Only obvious typos
in the source were cleaned ("A teachers using LPs" -> "Teachers using LPs").
"""
import re, os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

LOGO = r"c:\Agent Coco\assets\logo_taleemabad.png"
OUTDIR = r"c:\Agent Coco\output\case_studies"
FONT = "Quicksand"

BLUE = RGBColor(0x3C, 0x78, 0xD8)      # locked case-study accent
NAVY = RGBColor(0x2F, 0x4F, 0xA2)      # locked Taleemabad navy
BLACK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FILL_HEAD = "2F4FA2"   # table header
FILL_ALT = "F2F6FC"    # zebra row
FILL_CALL = "EEF3FB"   # callout box
RULE_CLR = "C9D6EE"

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


# ----------------------------------------------------------------- run styling
def style(run, size, color, bold, italic, underline):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.bold = bold
    run.italic = italic
    run.underline = underline
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = rPr.makeelement(qn('w:rFonts'), {})
        rPr.append(rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rFonts.set(qn(attr), FONT)


def add_runs(p, text, size=11, color=BLACK, italic=False, underline=False, bold_all=False):
    pos = 0
    for m in BOLD_RE.finditer(text):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()])
            style(r, size, color, bold_all, italic, underline)
        r = p.add_run(m.group(1))
        style(r, size, color, True, italic, underline)
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:])
        style(r, size, color, bold_all, italic, underline)


# ------------------------------------------------------------- xml decorations
def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexfill)
    tcPr.append(shd)


def cell_borders(cell, color=RULE_CLR, sz=6, edges=("top", "left", "bottom", "right")):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in edges:
        el = OxmlElement('w:' + edge)
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)
        borders.append(el)
    tcPr.append(borders)


def clear_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement('w:' + edge)
        el.set(qn('w:val'), 'nil')
        borders.append(el)
    tcPr.append(borders)


def accent_bar(cell, color="3C78D8", sz=24):
    """Thick left rule for callout boxes."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ("top", "bottom", "right"):
        el = OxmlElement('w:' + edge)
        el.set(qn('w:val'), 'nil')
        borders.append(el)
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), str(sz))
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), color)
    borders.append(left)
    tcPr.append(borders)


def cell_margins(cell, top=80, bottom=80, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement('w:' + name)
        el.set(qn('w:w'), str(val))
        el.set(qn('w:type'), 'dxa')
        mar.append(el)
    tcPr.append(mar)


def hrule(doc):
    """Thin full-width divider."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), RULE_CLR)
    borders.append(bottom)
    pPr.append(borders)


# ------------------------------------------------------------------ components
def make_table(doc, rows, widths):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = t.cell(ri, ci)
            cell.width = Inches(widths[ci])
            cell_margins(cell)
            cell_borders(cell)
            if ri == 0:
                shade(cell, FILL_HEAD)
            elif ri % 2 == 0:
                shade(cell, FILL_ALT)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 0 else WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, val, size=10.5,
                     color=WHITE if ri == 0 else BLACK,
                     bold_all=(ri == 0))
    return t


def make_callout(doc, lines, color="3C78D8", fill=FILL_CALL):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    cell = t.cell(0, 0)
    cell.width = Inches(6.5)
    cell_margins(cell, top=120, bottom=120, left=180, right=180)
    accent_bar(cell, color)
    shade(cell, fill)
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
    for i, (kind, text) in enumerate(lines):
        p = cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0 if i == 0 else 5)
        pf.space_after = Pt(0)
        if kind == "who":
            add_runs(p, text, size=10.5, color=NAVY, bold_all=True)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_runs(p, text, size=11, italic=True)
    return t


def qbanner(doc, question, points, prompt):
    """Question header: navy bar with the question number and its marks."""
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    left, right = t.cell(0, 0), t.cell(0, 1)
    left.width = Inches(4.9)
    right.width = Inches(1.6)
    for cell in (left, right):
        shade(cell, FILL_HEAD)
        clear_borders(cell)
        cell_margins(cell, top=90, bottom=90, left=160, right=160)
    lp = left.paragraphs[0]
    lp.paragraph_format.space_before = Pt(0); lp.paragraph_format.space_after = Pt(0)
    add_runs(lp, question, size=12.5, color=WHITE, bold_all=True)
    rp = right.paragraphs[0]
    rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rp.paragraph_format.space_before = Pt(0); rp.paragraph_format.space_after = Pt(0)
    add_runs(rp, points, size=11, color=WHITE, bold_all=True)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_runs(p, prompt)


# ---------------------------------------------------------------------- render
def build(spec, path):
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        hdr = section.header
        hp = hdr.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hp.add_run().add_picture(LOGO, width=Inches(1.15))

    for item in spec:
        kind = item[0]

        if kind == "rule":
            hrule(doc)
            continue
        if kind == "pagebreak":
            doc.add_page_break()
            continue
        if kind == "table":
            make_table(doc, item[1], item[2])
            continue
        if kind == "callout":
            make_callout(doc, item[1], *(item[2:]))
            continue
        if kind == "q":
            qbanner(doc, item[1], item[2], item[3])
            continue
        if kind == "spacer":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(item[1] if len(item) > 1 else 6)
            continue

        text = item[1] if len(item) > 1 else ""
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(6)
        if kind == "title":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.space_before = Pt(18); pf.space_after = Pt(4)
            add_runs(p, text, size=17, bold_all=True)
        elif kind == "subtitle":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.space_after = Pt(16)
            add_runs(p, text, size=15, color=BLUE, bold_all=True)
        elif kind == "meta":
            pf.space_after = Pt(2)
            add_runs(p, text)
        elif kind == "part":                      # PART banner
            pf.space_before = Pt(18); pf.space_after = Pt(2)
            add_runs(p, text, size=15, color=NAVY, bold_all=True)
        elif kind == "h1":
            pf.space_before = Pt(16); pf.space_after = Pt(8)
            add_runs(p, text, size=15, bold_all=True)
        elif kind == "h2":
            pf.space_before = Pt(14); pf.space_after = Pt(6)
            add_runs(p, text, size=12.5, color=BLUE, bold_all=True)
        elif kind == "h3":
            pf.space_before = Pt(8); pf.space_after = Pt(4)
            add_runs(p, text, bold_all=True)
        elif kind == "h3u":
            pf.space_before = Pt(8); pf.space_after = Pt(4)
            add_runs(p, text, bold_all=True, underline=True)
        elif kind == "para":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_runs(p, text)
        elif kind == "caption":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.space_before = Pt(4)
            add_runs(p, text, size=9.5, color=GREY, italic=True)
        elif kind == "bullet":
            p.style = doc.styles["List Bullet"]
            pf.space_after = Pt(3)
            add_runs(p, text)
        elif kind == "bullet2":
            p.style = doc.styles["List Bullet 2"]
            pf.space_after = Pt(3)
            add_runs(p, text)
        elif kind == "num":
            p.style = doc.styles["List Number"]
            pf.space_after = Pt(3)
            add_runs(p, text)
        elif kind == "footer":
            pf.space_before = Pt(14); pf.space_after = Pt(0)
            add_runs(p, text, italic=True)
    doc.save(path)
    print("built", path)


# ================================================================== CONTENT ===
RM = [
    ("title", "Regional Manager @ Taleemabad"),
    ("subtitle", "Strategic Case Study"),
    ("meta", "**Role:** Regional Manager (Urban & Rural regions)"),
    ("meta", "**Structure:** 6 parts \u00b7 10 questions"),
    ("meta", "**Submission Format:** Written document or slides, with an executive summary"),
    ("rule",),

    # ---------------------------------------------------------- Background
    ("h1", "Background"),
    ("para", "You are a **Regional Manager responsible for two regions: Urban and Rural**, covering:"),
    ("bullet", "**18 CPD Coaches**"),
    ("bullet", "**360+ teachers**"),
    ("bullet", "**90+ schools**"),
    ("bullet", "Primary, Middle & High schools"),
    ("bullet", "Multiple FDE/AEO stakeholders"),
    ("bullet", "HITL coaching"),
    ("bullet", "Digital Coach (DC)"),
    ("bullet", "Lesson Plans (LPs)"),
    ("bullet", "Teacher Training"),
    ("bullet", "Classroom Observations"),
    ("bullet", "Student Assessments"),
    ("para", "You have been managing the programme for **five months**."),
    ("para", "Senior leadership has now told you that the next **90 days are critical**, because the programme will be reviewed for potential expansion."),
    ("para", "However, the situation is becoming increasingly complex."),

    ("pagebreak",),

    # ------------------------------------------------------------- PART I
    ("part", "PART I \u2014 THE SITUATION"),
    ("h2", "1. The Dashboard Says One Thing. The Field Says Another."),
    ("para", "Your regional dashboard currently shows:"),
    ("table", [
        ["Indicator", "Urban", "Rural"],
        ["Training Completion", "94%", "71%"],
        ["LP Adoption", "76%", "39%"],
        ["DC Usage", "72%", "31%"],
        ["HITL Observation Completion", "91%", "67%"],
        ["Average FICO", "2.9", "2.6"],
        ["Student Dipstick", "64%", "58%"],
    ], [3.3, 1.6, 1.6]),
    ("spacer", 8),
    ("para", "At first glance, the Urban region appears to be performing significantly better. However, during your weekly RM review, coaches report:"),

    ("h3", "Urban"),
    ("callout", [
        ("quote", "\u201cTeachers are completing the LPs because they know adoption is being tracked, but many are not actually implementing the LP as intended.\u201d"),
        ("who", "Another coach says:"),
        ("quote", "\u201cFICO scores aren\u2019t improving despite high LP usage.\u201d"),
    ]),
    ("spacer", 8),

    ("h3", "Rural"),
    ("callout", [
        ("quote", "\u201cMany teachers want to use the platform, but connectivity is unreliable.\u201d"),
        ("who", "Another coach says:"),
        ("quote", "\u201cWhen we actually reach teachers consistently, their classroom practices improve.\u201d"),
    ]),
    ("spacer", 8),

    ("para", "You then discover that:"),
    ("bullet", "Some teachers\u2019 LP usage is not appearing correctly on the dashboard."),
    ("bullet", "Some completed training modules are still showing as incomplete."),
    ("bullet", "Some DC observations were recorded offline and have not synced."),
    ("bullet", "Some schools were closed during scheduled visits."),
    ("bullet", "Some coaches have been manually maintaining records because of system issues."),
    ("callout", [
        ("who", "The Programme Manager tells you:"),
        ("quote", "\u201cI don\u2019t want explanations. I need to know which region is performing better and what we should do next.\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("rule",),

    ("h2", "2. A Major Donor Visit Is Coming"),
    ("para", "A major donor delegation is scheduled to visit in **10 days**. They want to see:"),
    ("num", "A successful school."),
    ("num", "Teachers using LPs."),
    ("num", "Coaches conducting observations."),
    ("num", "Digital Coach usage."),
    ("num", "Evidence of improved teaching."),
    ("num", "Evidence of student learning."),
    ("callout", [
        ("who", "The Programme Manager says:"),
        ("quote", "\u201cPlease make sure the visit goes smoothly. We cannot afford to show them a school where things aren\u2019t working.\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "However, the school initially selected for the visit has:"),
    ("bullet", "Excellent LP adoption"),
    ("bullet", "High training completion"),
    ("bullet", "Weak FICO improvement"),
    ("bullet", "Teachers who privately report that they feel overwhelmed by the number of programme activities"),
    ("para", "Meanwhile, a rural school has:"),
    ("bullet", "Low digital adoption"),
    ("bullet", "Poor connectivity"),
    ("bullet", "Strong teacher engagement with the coach"),
    ("bullet", "Significant improvement in classroom practice"),
    ("bullet", "Positive teacher feedback"),
    ("para", "The donor specifically wants to understand **how the programme works in challenging contexts**. You cannot simply choose the easiest school."),
    ("rule",),

    ("h2", "3. The Coaches Are Reaching Their Limit"),
    ("para", "Your 18 coaches currently have to manage:"),
    ("bullet", "Classroom observations"),
    ("bullet", "HITL coaching"),
    ("bullet", "DC observations"),
    ("bullet", "Teacher training"),
    ("bullet", "LP implementation"),
    ("bullet", "LP feedback experiments"),
    ("bullet", "Student assessments"),
    ("para", "You calculate that the current workload requires approximately **115% of available coach capacity**. Senior management has nevertheless introduced another requirement:"),
    ("callout", [
        ("who", "Senior management:"),
        ("quote", "\u201cFor the next two months, increase classroom observation coverage by 25%.\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "At the same time:"),
    ("bullet", "Two coaches are considering resignation."),
    ("bullet", "Three coaches have requested school reassignment."),
    ("bullet", "One highly experienced coach is consistently exceeding targets but has poor team collaboration."),
    ("bullet", "One coach has excellent relationships with teachers but consistently misses reporting deadlines."),
    ("bullet", "Two new coaches require significant onboarding support."),
    ("para", "**You cannot hire additional coaches during the next three months.**"),
    ("rule",),

    ("h2", "4. A New Experiment Is Being Proposed"),
    ("para", "The Learning Engineering (LE) team wants to test a new AI-supported LP recommendation system. They need:"),
    ("bullet", "40 teachers"),
    ("bullet", "20 control teachers"),
    ("bullet", "20 intervention teachers"),
    ("bullet", "Baseline data"),
    ("bullet", "Weekly usage tracking"),
    ("bullet", "Teacher feedback"),
    ("bullet", "Classroom observations"),
    ("para", "They want to start **next Monday**."),
    ("callout", [
        ("who", "The Research team responds:"),
        ("quote", "\u201cIf you introduce additional coaching support to these teachers during the experiment, you may contaminate the results.\u201d"),
        ("who", "The coaches respond:"),
        ("quote", "\u201cWe already have too many activities. We cannot add another experiment.\u201d"),
        ("who", "The LE team says:"),
        ("quote", "\u201cThis experiment is strategically important and has already been approved.\u201d"),
    ]),
    ("spacer", 8),
    ("para", "You have to decide how to proceed."),
    ("rule",),

    ("h2", "5. AEO Has Raised a Serious Complaint"),
    ("para", "The Rural AEO contacts you directly:"),
    ("callout", [
        ("quote", "\u201cYour coaches are visiting schools irregularly. Some teachers haven\u2019t seen a coach for more than a month. Yet your dashboard shows reasonable implementation.\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "The AEO requests a written action plan within **48 hours**. At the same time, your rural Lead Coach tells you:"),
    ("callout", [
        ("quote", "\u201cThe schools haven\u2019t been visited because two routes became inaccessible after heavy rain, and one coach has been dealing with a device issue.\u201d"),
        ("who", "The AEO does not accept this explanation and says:"),
        ("quote", "\u201cIf your team cannot reach these schools, tell us what alternative you are providing.\u201d"),
    ]),
    ("spacer", 8),
    ("rule",),

    ("h2", "6. An Unexpected Student Learning Finding"),
    ("para", "The latest assessment shows:"),
    ("h3", "Urban \u2014 overall pass rate: 67%"),
    ("bullet", "Students already below grade level: **34%**"),
    ("bullet", "Students at grade level: **75%**"),
    ("h3", "Rural \u2014 overall pass rate: 56%"),
    ("bullet", "Students below grade level: **49%**"),
    ("bullet", "Students at grade level: **61%**"),
    ("callout", [
        ("who", "Senior leadership initially says:"),
        ("quote", "\u201cUrban is clearly performing better.\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "You believe the data requires deeper analysis."),

    ("pagebreak",),

    # ------------------------------------------------------------- PART A
    ("part", "PART A \u2014 Strategic Diagnosis"),
    ("q", "Question 1", "10 Points",
     "Before taking action, identify the **10 most important pieces of information** you would need. For each piece of information, explain:"),
    ("bullet", "Why you need it"),
    ("bullet", "Where you would get it"),
    ("bullet", "What decision it would influence"),
    ("spacer", 6),

    ("q", "Question 2", "15 Points",
     "Based on the information currently available: **can you conclude that the Urban region is performing better than Rural?** Explain your reasoning. Your answer must distinguish between:"),
    ("bullet", "Adoption"),
    ("bullet", "Implementation quality"),
    ("bullet", "Teacher practice"),
    ("bullet", "Student outcomes"),
    ("bullet", "Infrastructure"),
    ("bullet", "Data reliability"),
    ("spacer", 6),

    ("q", "Question 3", "10 Points",
     "Identify the **three most likely root causes** behind the rural region\u2019s low adoption. For each one, explain how you would test whether your assumption is correct before introducing an intervention."),

    ("pagebreak",),

    # ------------------------------------------------------------- PART B
    ("part", "PART B \u2014 Forced Prioritization"),
    ("para", "You have only **100% coach capacity**, but current demands require **115%**. You must reduce the workload by at least **15%**. You have the following options:"),
    ("table", [
        ["Activity", "Current Capacity", "Strategic Importance"],
        ["HITL observations", "25%", "Very High"],
        ["DC observations", "15%", "High"],
        ["Teacher training", "15%", "Very High"],
        ["LP implementation", "15%", "Very High"],
        ["LE experiments", "15%", "Medium/High"],
        ["Student assessments", "10%", "High"],
        ["Reporting / Data validation", "10%", "High"],
    ], [2.7, 1.9, 1.9]),
    ("spacer", 10),
    ("q", "Question 4", "15 Points",
     "What would you **Continue \u2192 Reduce \u2192 Pause \u2192 Delegate \u2192 Redesign**? You must justify every decision."),
    ("spacer", 4),
    ("q", "Question 5", "10 Points",
     "Senior management says: **\u201cEverything is a priority.\u201d** How would you respond? Your answer should demonstrate how an RM can **push back professionally without appearing resistant to organizational priorities**."),

    ("pagebreak",),

    # ------------------------------------------------------------- PART C
    ("part", "PART C \u2014 Coach Leadership"),
    ("para", "You have four different coach-performance situations:"),
    ("table", [
        ["Coach", "Situation"],
        ["Coach A", "High productivity, high target achievement, poor collaboration."],
        ["Coach B", "Excellent teacher relationships, poor reporting discipline."],
        ["Coach C", "Low productivity, but strong potential and positive attitude."],
        ["Coach D", "Strong technically, but increasingly showing signs of burnout."],
    ], [1.3, 5.2]),
    ("spacer", 10),
    ("q", "Question 6", "10 Points",
     "Create an individual management approach for each coach. For each, explain:"),
    ("bullet", "What you would discuss"),
    ("bullet", "What support you would provide"),
    ("bullet", "What expectation you would set"),
    ("bullet", "How you would measure improvement"),
    ("bullet", "When you would escalate"),

    ("pagebreak",),

    # ------------------------------------------------------------- PART D
    ("part", "PART D \u2014 Experiment Management"),
    ("para", "The LE team wants to start the LP experiment next Monday. You believe the coaches are already overloaded."),
    ("q", "Question 7", "10 Points", "Would you:"),
    ("bullet", "**A.** Approve it as planned"),
    ("bullet", "**B.** Delay it"),
    ("bullet", "**C.** Reduce its scope"),
    ("bullet", "**D.** Redesign the implementation"),
    ("bullet", "**E.** Run it only in one region"),
    ("para", "Choose one approach and justify it."),

    ("pagebreak",),

    # ------------------------------------------------------------- PART E
    ("part", "PART E \u2014 Stakeholder Conflict"),
    ("para", "You have four stakeholders:"),
    ("table", [
        ["Stakeholder", "What they want"],
        ["Programme Director", "Stronger adoption numbers."],
        ["AEO", "Consistent school visits."],
        ["LE Team", "Experiments implemented quickly."],
        ["Coaches", "Fewer simultaneous initiatives."],
    ], [2.1, 4.4]),
    ("spacer", 10),
    ("q", "Question 8", "10 Points",
     "Create a **stakeholder management plan**. For each stakeholder, explain:"),
    ("bullet", "What they need from you"),
    ("bullet", "What you need from them"),
    ("bullet", "What information you will share"),
    ("bullet", "What you will negotiate"),
    ("bullet", "What you will escalate"),

    ("pagebreak",),

    # ------------------------------------------------------------- PART F
    ("part", "PART F \u2014 The Hardest Decision"),
    ("para", "You receive the following information on Friday afternoon:"),
    ("bullet", "**The Ministry visit is in five days.**"),
    ("bullet", "**The AEO wants the rural action plan by Monday.**"),
    ("bullet", "**The LE experiment begins Monday.**"),
    ("bullet", "**Two coaches are absent.**"),
    ("bullet", "**The dashboard has unresolved data issues.**"),
    ("bullet", "**Your team is already at 115% capacity.**"),
    ("bullet", "**The Programme Director still expects the 25% increase in observations.**"),
    ("para", "You cannot complete everything."),
    ("q", "Question 9", "10 Points",
     "You have **72 hours to make the programme stable**. Identify your **top 5 actions** and rank them from **1\u20135**. For each action explain:"),
    ("bullet", "Why it comes first"),
    ("bullet", "Who will own it"),
    ("bullet", "What you will deprioritize"),
    ("bullet", "What risk it reduces"),
    ("bullet", "What evidence will tell you it worked"),

    ("pagebreak",),

    # --------------------------------------------------- Final challenge
    ("part", "Final Executive Challenge"),
    ("para", "Imagine the Programme Manager gives you **five minutes** and asks:"),
    ("callout", [
        ("quote", "\u201cIf I give you no additional staff and no additional budget, what three things will you change in the next 90 days that will have the greatest impact on teacher practice and student learning?\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("q", "Question 10", "", "Prepare your **five-minute executive response**."),
    ("para", "You will be evaluated not on how many ideas you provide, but on:"),
    ("bullet", "**Quality of diagnosis**"),
    ("bullet", "**Prioritization**"),
    ("bullet", "**Evidence-based thinking**"),
    ("bullet", "**People leadership**"),
    ("bullet", "**Stakeholder management**"),
    ("bullet", "**Understanding of implementation realities**"),
    ("bullet", "**Connection between teacher practice and student outcomes**"),
    ("rule",),

    ("h1", "Submission Instructions"),
    ("bullet", "Submit a written document or slides addressing each task separately."),
    ("bullet", "Include any relevant charts, graphs, or visuals to support your proposals."),
    ("bullet", "Provide a brief executive summary that highlights the key recommendations from each task."),
    ("footer", "Taleemabad is an equal-opportunity employer."),
    ("footer", "We hire for grit, learning velocity, and outcomes."),
]

os.makedirs(OUTDIR, exist_ok=True)
rm_path = os.path.join(OUTDIR, "RM_case_study.docx")
build(RM, rm_path)

if os.environ.get("UPLOAD") == "1":
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build as gbuild
    from googleapiclient.http import MediaFileUpload

    creds = Credentials.from_authorized_user_file(
        r"c:\Agent Coco\.claude\config\token_sheets_broad.json")
    drive = gbuild("drive", "v3", credentials=creds)
    title = "Regional Manager @ Taleemabad \u2014 Strategic Case Study"
    media = MediaFileUpload(
        rm_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    f = drive.files().create(
        body={"name": title, "mimeType": "application/vnd.google-apps.document"},
        media_body=media,
        fields="id, webViewLink",
    ).execute()
    print(title)
    print("  ->", f["webViewLink"])
