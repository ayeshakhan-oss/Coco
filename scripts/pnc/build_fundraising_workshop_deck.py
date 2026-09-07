"""Build the Fundraising Capability Workshop deck (.pptx) from the agreed outline.

Source of the content: docs/pnc_buddy/FUNDRAISING_WORKSHOP_DECK_OUTLINE.md
Facilitator notes from the outline go into each slide's speaker notes.

No personal names anywhere. No invented Taleemabad figures: placeholders read
"[To be added/validated with ...]".

Usage:
    python scripts/pnc/build_fundraising_workshop_deck.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

OUT = Path(r"c:\Agent Coco\docs\pnc_buddy\Fundraising_Capability_Workshop.pptx")
LOGO = Path(r"c:\Agent Coco\assets\logo_taleemabad.png")

NAVY = RGBColor(0x2F, 0x4F, 0xA2)
BLUE = RGBColor(0x3C, 0x78, 0xD8)
INK = RGBColor(0x1F, 0x24, 0x2E)
GREY = RGBColor(0x5A, 0x61, 0x6E)
LIGHT = RGBColor(0xEE, 0xF2, 0xFA)
LINE = RGBColor(0xD5, 0xDC, 0xEA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Calibri"
W, H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------- helpers
def textbox(slide, l, t, w, h, text, size=18, color=INK, bold=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=10,
            line_spacing=1.15, italic=False):
    """Add a textbox. `text` may be a string or a list of paragraph strings."""
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        f = run.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), bold, italic
        f.color.rgb = color
    return box


def bullets(slide, l, t, w, h, items, size=18, color=INK, gap=14):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        p.line_spacing = 1.2
        dot = p.add_run()
        dot.text = "\u2022   "
        dot.font.name, dot.font.size = FONT, Pt(size)
        dot.font.color.rgb = BLUE
        run = p.add_run()
        run.text = item
        run.font.name, run.font.size = FONT, Pt(size)
        run.font.color.rgb = color
    return box


def box_shape(slide, l, t, w, h, text, fill, fontcolor, size=11, bold=False,
              shape=MSO_SHAPE.ROUNDED_RECTANGLE, outline=None):
    sh = slide.shapes.add_shape(shape, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if outline is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = outline
        sh.line.width = Pt(1)
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.line_spacing = 1.0
    r = p.add_run()
    r.text = text
    r.font.name, r.font.size, r.font.bold = FONT, Pt(size), bold
    r.font.color.rgb = fontcolor
    return sh


def chrome(slide, number, dark=False):
    """Accent rule under the title, logo, slide number."""
    if LOGO.exists():
        slide.shapes.add_picture(str(LOGO), Inches(11.95), Inches(6.72),
                                 height=Inches(0.34))
    textbox(slide, Inches(0.72), Inches(6.78), Inches(0.6), Inches(0.3),
            str(number), size=11, color=WHITE if dark else GREY)


def title_block(slide, title, kicker=None, dark=False):
    y = Inches(0.62)
    if kicker:
        textbox(slide, Inches(0.72), y, Inches(11.9), Inches(0.3), kicker.upper(),
                size=11, color=BLUE if not dark else RGBColor(0x9E, 0xB8, 0xE8),
                bold=True, space_after=0)
        y = Inches(0.95)
    textbox(slide, Inches(0.72), y, Inches(11.9), Inches(0.8), title,
            size=32, color=WHITE if dark else NAVY, bold=True, space_after=0)
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.72),
                                  y + Inches(0.72), Inches(1.1), Pt(3))
    rule.fill.solid()
    rule.fill.fore_color.rgb = BLUE
    rule.line.fill.background()
    rule.shadow.inherit = False


def new_slide(dark=False):
    s = prs.slides.add_slide(BLANK)
    if dark:
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
        bg.fill.solid()
        bg.fill.fore_color.rgb = NAVY
        bg.line.fill.background()
        bg.shadow.inherit = False
    return s


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------------------------------------------------------------- slide 1
s = new_slide(dark=True)
if LOGO.exists():
    s.shapes.add_picture(str(LOGO), Inches(0.72), Inches(0.6), height=Inches(0.5))
textbox(s, Inches(0.72), Inches(2.35), Inches(10.5), Inches(1.2),
        "Fundraising Capability Workshop", size=44, color=WHITE, bold=True,
        space_after=0)
rule = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(3.5),
                          Inches(1.4), Pt(3))
rule.fill.solid(); rule.fill.fore_color.rgb = BLUE; rule.line.fill.background()
rule.shadow.inherit = False
textbox(s, Inches(0.72), Inches(3.85), Inches(9.5), Inches(1.4),
        ["A working session on how fundraising moves, and where our work sits in it",
         "People and Culture, with the Fundraising team"],
        size=17, color=RGBColor(0xC7, 0xD5, 0xF0), space_after=6)
textbox(s, Inches(0.72), Inches(6.6), Inches(6), Inches(0.4),
        "Roughly 2.5 hours   |   Mostly exercises, using our own material",
        size=12, color=RGBColor(0x9E, 0xB8, 0xE8))
notes(s, "Say what prompted this and be honest that it started as a P&C piece of "
         "work. Set the expectation that the session will surface things we cannot "
         "answer yet, and that this is the point rather than a problem. Mention that "
         "individual development plans come later and separately, so nobody sits "
         "through this wondering if they are being assessed.\n\n"
         "Keep this slide short.")

# ---------------------------------------------------------------- slide 2
s = new_slide()
title_block(s, "How fundraising moves", "The sequence")
stages = ["Research", "Qualify", "Cultivate", "Design\nthe Ask", "Proposal",
          "Budget", "Due\nDiligence", "Close", "Deliver\nand Report",
          "Steward", "Renew"]
n = len(stages)
left0, total_w, gap = Inches(0.72), Inches(11.9), Inches(0.06)
bw = int((total_w - gap * (n - 1)) / n)
for i, st in enumerate(stages):
    fill = LIGHT if i % 2 == 0 else RGBColor(0xE3, 0xEA, 0xF7)
    box_shape(s, left0 + i * (bw + gap), Inches(2.55), bw, Inches(1.15),
              st, fill, NAVY, size=11, bold=True, outline=LINE)
    if i < n - 1:
        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                left0 + i * (bw + gap) + bw - Inches(0.02),
                                Inches(3.02), Inches(0.1), Inches(0.2))
        ar.fill.solid(); ar.fill.fore_color.rgb = LINE
        ar.line.fill.background(); ar.shadow.inherit = False
bullets(s, Inches(0.72), Inches(4.35), Inches(11.9), Inches(1.6), [
    "Proposal writing is one stage. Most of what decides the outcome happens before it.",
    "This is a shared vocabulary, not a process to comply with.",
], size=17)
textbox(s, Inches(0.72), Inches(5.55), Inches(11.9), Inches(0.4),
        "Stage by stage detail is in the facilitator guide.", size=12,
        color=GREY, italic=True)
notes(s, "Walk it once, quickly. The one point worth making is that proposal "
         "writing is one stage, and most of what decides the outcome happens "
         "before it. Do not explain every stage, they will ask about the ones "
         "they do not recognise.\n\n"
         "DISCUSSION: Where do we currently spend most of our time? Which stage "
         "do we do least well? Mark both on the slide as they answer.")

# ---------------------------------------------------------------- slide 3
s = new_slide()
title_block(s, "Can we answer these?", "Eleven questions")
qs_left = ["Who should fund us?", "Why are we a fit?",
           "What exactly are we asking them to fund?",
           "What problem are we solving?", "Does our solution work?",
           "How do we know?"]
qs_right = ["What does it cost?", "Can it scale?",
            "What would additional funding enable?", "Why Taleemabad?",
            "How do we build and maintain that relationship?"]
bullets(s, Inches(0.72), Inches(2.4), Inches(5.7), Inches(3.6), qs_left, size=19, gap=18)
bullets(s, Inches(6.9), Inches(2.4), Inches(5.7), Inches(3.6), qs_right, size=19, gap=18)
notes(s, "Ask them cold, one at a time, and let the silences sit. Write down what "
         "we cannot answer on a flipchart.\n\n"
         "Separate two kinds of gap as they come up: things the person does not "
         "know, and things the organisation has never written down. The second "
         "kind is not their failure and should be recorded as an action for us.\n\n"
         "The whole slide is the discussion. Allow at least 10 minutes.")

# ---------------------------------------------------------------- slide 4
s = new_slide()
title_block(s, "How well do we know Taleemabad?", "Rapid fire, no notes")
bullets(s, Inches(0.72), Inches(2.45), Inches(11.9), Inches(3.2), [
    "What problem do we solve, and for whom?",
    "Where do we work, and how many people do we reach?",
    "What is our evidence, and how strong is it?",
    "What does it cost, and who funds us today?",
    "What is different about us, and what are we scaling?",
], size=20, gap=20)
band = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.72),
                          Inches(5.55), Inches(11.9), Inches(0.85))
band.fill.solid(); band.fill.fore_color.rgb = LIGHT
band.line.color.rgb = LINE; band.line.width = Pt(1); band.shadow.inherit = False
textbox(s, Inches(1.0), Inches(5.72), Inches(11.4), Inches(0.6),
        "Then, separately: 60 seconds on what Taleemabad is. 60 seconds on why "
        "someone should fund us.", size=16, color=NAVY, bold=True)
notes(s, "Run the five questions fast, no notes allowed. Then slow down for the "
         "one that matters: 60 seconds each on what Taleemabad is, and then "
         "separately 60 seconds on why someone should fund us. These come out as "
         "the same answer the first time, and separating them is the useful part.\n\n"
         "Do not put our reach, cost or evidence figures on this slide until they "
         "have been confirmed. [To be added/validated with Programmes and Finance.]\n\n"
         "DISCUSSION: Which of these could you answer confidently in front of a "
         "donor tomorrow?")

# ---------------------------------------------------------------- slide 5
s = new_slide()
title_block(s, "Finding a donor is not the same as having an opportunity",
            "Research, then qualification")
dims = ["Mission fit", "Geography fit", "Programme fit", "Evidence fit",
        "Scale fit", "Ticket size", "Relationship", "Timing", "Effort"]
cols, cw, ch, gx, gy = 3, Inches(3.85), Inches(0.7), Inches(0.12), Inches(0.12)
for i, d in enumerate(dims):
    r, c = divmod(i, cols)
    box_shape(s, Inches(0.72) + c * (cw + gx), Inches(2.5) + r * (ch + gy),
              cw, ch, d, WHITE, INK, size=15, outline=LINE)
textbox(s, Inches(0.72), Inches(5.2), Inches(11.9), Inches(0.4),
        "Score each 1 to 5, then make the call.", size=15, color=GREY)
calls = ["Pursue", "Cultivate", "Monitor", "Decline"]
for i, c_ in enumerate(calls):
    box_shape(s, Inches(0.72) + i * Inches(2.0), Inches(5.7), Inches(1.85),
              Inches(0.6), c_, NAVY, WHITE, size=15, bold=True)
textbox(s, Inches(9.0), Inches(5.78), Inches(3.6), Inches(0.5),
        "Record why we said no.", size=14, color=GREY, italic=True)
notes(s, "Give each person one funder from Mulago, Vitol, GiveWell or DIV, and 20 "
         "minutes. The question they answer is whether we should pursue, and why.\n\n"
         "Watch for the Vitol case. Vitol does not take unsolicited applications, "
         "they invite organisations through a programme manager. If someone "
         "recommends writing a proposal, that is a good moment to draw out the "
         "difference between research and qualification.\n\n"
         "When reviewing, focus on the quality of the recommendation rather than "
         "how much was found.\n\n"
         "DISCUSSION: What would change your mind about this funder?")

# ---------------------------------------------------------------- slide 6
s = new_slide()
title_block(s, "Building the funding case", "Six blocks")
blocks = ["Problem", "Intervention", "Evidence", "Economics", "Ask", "Scale"]
bw6 = Inches(1.85)
gap6 = (Inches(11.9) - bw6 * 6) / 5
for i, b in enumerate(blocks):
    box_shape(s, Inches(0.72) + i * (bw6 + gap6), Inches(2.7), bw6, Inches(1.3),
              b, NAVY if i % 2 == 0 else BLUE, WHITE, size=16, bold=True)
bullets(s, Inches(0.72), Inches(4.5), Inches(11.9), Inches(1.8), [
    "The story on its own does not survive a donor conversation.",
    "The numbers on their own do not give anyone a reason to care.",
    "Output: a one page case, plus a list of what is missing and who owns getting it.",
], size=17)
notes(s, "Use one real Taleemabad intervention. [To be added/validated with "
         "Fundraising and Programmes.]\n\n"
         "Ask for a one page case covering the six blocks, plus a separate list of "
         "what information is missing and who owns getting it. The missing "
         "information list is the output worth pressing on. Saying 'Finance needs "
         "to confirm this' is the right instinct.\n\n"
         "DISCUSSION: What is the weakest block for this intervention right now?")

# ---------------------------------------------------------------- slide 7
s = new_slide()
title_block(s, "Understanding the numbers", "Finance and evidence")
bullets(s, Inches(0.72), Inches(2.45), Inches(6.4), Inches(3.4), [
    "Programme cost, direct and indirect",
    "Cost per child, per school, per teacher",
    "Cost per outcome, where we have the data",
    "Restricted and unrestricted, co-funding, funding gap",
], size=17, gap=16)
panel = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5),
                           Inches(2.45), Inches(5.12), Inches(2.7))
panel.fill.solid(); panel.fill.fore_color.rgb = LIGHT
panel.line.color.rgb = LINE; panel.line.width = Pt(1); panel.shadow.inherit = False
textbox(s, Inches(7.8), Inches(2.62), Inches(4.6), Inches(2.4),
        ["WORKED EXAMPLE", "Programme budget:  ____________",
         "Children reached:  ____________",
         "Cost per child:  ____________",
         "[To be added/validated with Finance]"],
        size=13, color=NAVY, space_after=9)
band = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.72), Inches(5.45),
                          Inches(11.9), Inches(0.85))
band.fill.solid(); band.fill.fore_color.rgb = WHITE
band.line.color.rgb = BLUE; band.line.width = Pt(1.25); band.shadow.inherit = False
textbox(s, Inches(1.0), Inches(5.62), Inches(11.4), Inches(0.6),
        "We are not replacing Finance. We need to explain the case, and know when "
        "to bring them in.", size=16, color=NAVY, bold=True)
notes(s, "Have them calculate cost per child from the real budget, then ask what "
         "else they would need in order to calculate cost per outcome. Then the "
         "donor questions: why does it cost this much, what would another PKR 10M "
         "enable, what happens if we get half, what changes at scale.\n\n"
         "If the real budget is not cleared in time, cut this section short rather "
         "than running it on invented numbers.\n\n"
         "DISCUSSION: Which numbers would you want Finance to confirm before you "
         "sat in front of a donor?")

# ---------------------------------------------------------------- slide 8
s = new_slide(dark=True)
title_block(s, "Let us meet the donor", "Role play, 25 minutes", dark=True)
textbox(s, Inches(0.72), Inches(2.6), Inches(11.9), Inches(1.0),
        "No pitching for the first five minutes.", size=36, color=WHITE, bold=True,
        space_after=0)
textbox(s, Inches(0.75), Inches(3.5), Inches(11.9), Inches(0.5),
        "Your job at the start is to understand them.", size=19,
        color=RGBColor(0xC7, 0xD5, 0xF0))
qbox = ["Why Taleemabad?", "How do you know this works?", "What does it cost?",
        "What would my funding enable?", "What happens when my grant ends?",
        "How could this scale, and who pays?"]
for i, q in enumerate(qbox):
    r, c = divmod(i, 3)
    box_shape(s, Inches(0.72) + c * Inches(4.06), Inches(4.5) + r * Inches(0.78),
              Inches(3.9), Inches(0.66), q,
              RGBColor(0x3E, 0x5F, 0xB5), WHITE, size=13)
notes(s, "Play the donor. Hold the five minute rule firmly, people will try to "
         "pitch. Then move to the harder questions on the slide.\n\n"
         "Afterwards, ask each person what they would pitch differently based on "
         "what they heard, not on what they prepared.\n\n"
         "DISCUSSION: Which question was hardest, and what would we need in order "
         "to answer it properly next time?")

# ---------------------------------------------------------------- slide 9
s = new_slide()
title_block(s, "The capabilities we want to build", "Twelve, proposed")
caps = [
    ("Understanding our organisation", "Explains us, and why to fund us, without notes"),
    ("Donor research", "Knows what they fund, where, how much, and the route in"),
    ("Donor qualification", "Reaches a clear call, and can defend a no"),
    ("Stakeholder mapping", "Knows who decides, and how we get in front of them"),
    ("Donor engagement and listening", "Comes out knowing what the funder cares about"),
    ("Storytelling and pitching", "Story, evidence and economics in one case"),
    ("Proposal and grant development", "Works from their requirements, flags what is missing"),
    ("Financial literacy", "Explains the costs, knows when to bring Finance in"),
    ("Evidence and M&E literacy", "Clear about what our data does not show"),
    ("Cost-effectiveness and scale", "Value for money, and a realistic route to scale"),
    ("Pipeline management", "Owner, next action, value and status kept current"),
    ("Stewardship and ethics", "Reports accurately, does not overstate to win funding"),
]
cw9, ch9 = Inches(2.87), Inches(1.05)
gx9, gy9 = Inches(0.145), Inches(0.16)
for i, (cap, practice) in enumerate(caps):
    r, c = divmod(i, 4)
    l9 = Inches(0.72) + c * (cw9 + gx9)
    t9 = Inches(2.45) + r * (ch9 + gy9)
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l9, t9, cw9, ch9)
    sh.fill.solid(); sh.fill.fore_color.rgb = LIGHT
    sh.line.color.rgb = LINE; sh.line.width = Pt(1); sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.11)
    tf.margin_top, tf.margin_bottom = Inches(0.13), Inches(0.06)
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.LEFT
    p1.space_after = Pt(4)
    p1.line_spacing = 1.0
    r1 = p1.add_run(); r1.text = cap
    r1.font.name, r1.font.size, r1.font.bold = FONT, Pt(12), True
    r1.font.color.rgb = NAVY
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    p2.line_spacing = 1.0
    r2 = p2.add_run(); r2.text = practice
    r2.font.name, r2.font.size = FONT, Pt(9.5)
    r2.font.color.rgb = GREY
textbox(s, Inches(0.72), Inches(6.18), Inches(11.9), Inches(0.5),
        "The second line in each box is what we would expect to see in practice. "
        "A proposed list, not a finalised framework.", size=13, color=GREY)
notes(s, "This is a proposed list, not a finalised competency framework, and it is "
         "worth saying so. The second line in each box is what we would expect to "
         "see in practice, which is the more useful half of the conversation. Work "
         "through four or five of them properly rather than all twelve.\n\n"
         "Do not present any split of responsibilities between the two team "
         "members here. That is a conversation for the Senior Manager Fundraising "
         "with each of them afterwards, and putting it on a slide would make it "
         "look decided.\n\n"
         "DISCUSSION: Which four or five of these matter most for us over the next "
         "six months? Which are we already fine on?")

# ---------------------------------------------------------------- slide 10
s = new_slide()
title_block(s, "From workshop to actual work", "What happens next")
steps = ["Workshop", "Real assignments", "Feedback", "Individual\ndevelopment plans",
         "Review at\n30 to 60 days"]
bw10 = Inches(2.24)
gap10 = (Inches(11.9) - bw10 * 5) / 4
for i, st in enumerate(steps):
    box_shape(s, Inches(0.72) + i * (bw10 + gap10), Inches(2.7), bw10, Inches(1.25),
              st, NAVY if i in (0, 4) else LIGHT, WHITE if i in (0, 4) else INK,
              size=14, bold=(i in (0, 4)), outline=None if i in (0, 4) else LINE)
bullets(s, Inches(0.72), Inches(4.5), Inches(11.9), Inches(1.8), [
    "The assignments are where the development happens, not the session.",
    "Each person's plan is agreed separately.",
    "At 30 to 60 days: what can someone now do that they could not before, and "
    "what piece of work shows it?",
], size=17)
notes(s, "Close by naming two or three concrete assignments coming out of the "
         "session, with owners and dates, so it does not end on an intention. "
         "Examples: scoring our current prospects against the qualification "
         "dimensions, building a compliance matrix from a live RFP, or agreeing "
         "with Finance which cost figures we are allowed to quote.\n\n"
         "Say plainly that at 30 to 60 days the question will be what someone can "
         "now do that they could not before, and what piece of work shows it.\n\n"
         "DISCUSSION: What is each person taking away as their first assignment?")

# ---------------------------------------------------------------- chrome + save
for i, slide in enumerate(prs.slides, start=1):
    if i == 1:
        continue
    dark = i == 8
    chrome(slide, i, dark=dark)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(str(OUT))
print(f"saved: {OUT}")
print(f"slides: {len(prs.slides.__iter__.__self__._sldIdLst)}")
