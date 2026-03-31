"""
Candidate Communication Showcase — TED-Ed style, banana accent
LinkedIn carousel (8 slides, 1080x1080)
WhatsApp PNG (portrait)
"""

import os
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
LOGO = os.path.join(BASE, "assets", "logo_taleemabad.png")
OUT  = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

W = H = 1080.0

# ── PALETTE ───────────────────────────────────────────────────────────────────
DARK   = HexColor('#111111')
BANANA = HexColor('#FFD600')
BAN_D  = HexColor('#B89E00')   # dark banana (text on yellow)
WHITE  = white
MID    = HexColor('#999999')
DIM    = HexColor('#444444')
WARM   = HexColor('#1a1a1a')   # slightly warm dark

QUOTES = [
    "\u201cI\u2019ll be honest, receiving a rejection is never easy, "
    "but the way you delivered this one made all the difference. "
    "Thank you for seeing me as more than just an application.\u201d",

    "\u201cThis is one of the best rejections I have ever received. "
    "This is one of the reasons which always encourages me "
    "to be part of Taleemabad.\u201d",

    "\u201cIt is genuinely rare to receive a response this considered. "
    "It speaks well of Taleemabad\u2019s culture.\u201d",
]


# ── HELPERS ───────────────────────────────────────────────────────────────────

def sw(t, f, s):  return stringWidth(t, f, s)
def cxp(t, f, s): return (W - sw(t, f, s)) / 2

def tc(c, t, y, f, s, col):
    c.setFont(f, s); c.setFillColor(col)
    c.drawString(cxp(t, f, s), y, t)

def tl(c, t, x, y, f, s, col):
    c.setFont(f, s); c.setFillColor(col)
    c.drawString(x, y, t)

def wrap(t, f, s, mw):
    words = t.split(); lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        if sw(test, f, s) <= mw: cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    return lines

def twl(c, t, x, y, f, s, col, mw, lh=None):
    if lh is None: lh = s * 1.5
    for ln in wrap(t, f, s, mw):
        c.setFont(f, s); c.setFillColor(col)
        c.drawString(x, y, ln); y -= lh
    return y

def twc(c, t, y, f, s, col, mw, lh=None):
    if lh is None: lh = s * 1.5
    for ln in wrap(t, f, s, mw):
        c.setFont(f, s); c.setFillColor(col)
        c.drawString(cxp(ln, f, s), y, ln); y -= lh
    return y

def dark_bg(c):
    c.setFillColor(DARK); c.rect(0, 0, W, H, stroke=0, fill=1)

def banana_bg(c):
    c.setFillColor(BANANA); c.rect(0, 0, W, H, stroke=0, fill=1)

def circle_deco(c, cx, cy, r, col, alpha=1.0):
    c.setFillColor(col)
    c.setStrokeColor(col)
    c.circle(cx, cy, r, stroke=0, fill=1)

def banana_bar(c, y, h=8):
    c.setFillColor(BANANA)
    c.rect(0, y, W, h, stroke=0, fill=1)

def banana_rule(c, x, y, ww, h=5):
    c.setFillColor(BANANA)
    c.rect(x, y, ww, h, stroke=0, fill=1)

def slide_counter(c, n, light=False):
    col = MID if light else HexColor('#555555')
    c.setFont("Helvetica", 14); c.setFillColor(col)
    c.drawRightString(W - 52, 46, f"{n}  /  8")

def logo_badge(c, x=52, y=52, h=36, light=False):
    """Draw logo bottom-left, or text fallback."""
    try:
        img = ImageReader(LOGO)
        iw, ih = img.getSize()
        w = h * iw / ih
        c.drawImage(LOGO, x, y, w, h, mask='auto')
    except Exception:
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(BANANA if not light else DARK)
        c.drawString(x, y + 10, "Taleemabad")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — HOOK
# ═══════════════════════════════════════════════════════════════════════════════
def slide1(c):
    dark_bg(c)

    # Big banana decorative circle — top right, partially off screen
    circle_deco(c, W + 60, H + 60, 380, HexColor('#FFD600'))
    # Smaller dark cutout circle inside it (creates ring effect)
    circle_deco(c, W + 60, H + 60, 260, DARK)

    # Second subtle circle bottom left
    circle_deco(c, -80, -80, 240, HexColor('#1e1e1e'))

    # Banana horizontal rule
    banana_rule(c, 88, 660, 120, h=6)

    # Eyebrow
    tl(c, "PEOPLE & CULTURE  \u00b7  TALEEMABAD",
       88, 632, "Helvetica", 13, MID)

    # Hero text — left aligned, large
    tl(c, "We changed", 88, 530, "Helvetica-Bold", 96, WHITE)
    tl(c, "how we say no.", 88, 412, "Helvetica-Bold", 96, BANANA)

    # Subline
    tl(c, "A story of craft, courage, and care.",
       88, 348, "Helvetica-Oblique", 22, MID)

    logo_badge(c, light=False)
    slide_counter(c, 1, light=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════
def slide2(c):
    dark_bg(c)

    # Top banana band
    c.setFillColor(BANANA)
    c.rect(0, H - 110, W, 110, stroke=0, fill=1)
    tl(c, "THE BEFORE", 88, H - 72, "Helvetica-Bold", 16, DARK)

    # Main statement
    twl(c, "Most rejection emails read the same.",
        88, 780, "Helvetica-Bold", 52, WHITE, 900, lh=66)

    # Strikethrough example
    c.setFillColor(DIM)
    c.rect(88, 584, 800, 56, stroke=0, fill=1)
    tl(c, '"We regret to inform you that..."',
       108, 602, "Helvetica-Oblique", 22, MID)
    # banana strikethrough line
    c.setStrokeColor(BANANA); c.setLineWidth(3)
    c.line(88, 612, 888, 612)

    # Body copy
    twl(c,
        "Generic. Vague. Forgettable. Candidates deserve better.",
        88, 500, "Helvetica", 26, MID, 880, lh=38)

    # Turn line
    c.setFillColor(BANANA)
    c.rect(88, 400, 6, 60, stroke=0, fill=1)
    tl(c, "We decided that wasn\u2019t good enough.",
       108, 424, "Helvetica-Bold", 28, BANANA)

    logo_badge(c)
    slide_counter(c, 2, light=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — OUR DECISION
# ═══════════════════════════════════════════════════════════════════════════════
def slide3(c):
    banana_bg(c)

    # Large dark decorative circle — bottom right
    circle_deco(c, W + 100, -100, 400, HexColor('#e6c200'))
    circle_deco(c, W + 100, -100, 280, BANANA)

    # Eyebrow
    tl(c, "OUR DECISION", 88, H - 110, "Helvetica-Bold", 16, DARK)
    c.setFillColor(DARK); c.rect(88, H - 122, 80, 5, stroke=0, fill=1)

    # Hero text
    twl(c, "We chose to continuously improve our craft.",
        88, 750, "Helvetica-Bold", 66, DARK, 900, lh=80)

    # Body
    twl(c,
        "Every rejection became an opportunity "
        "to leave someone better than we found them.",
        88, 556, "Helvetica", 26, HexColor('#333300'), 860, lh=38)

    # Three tags
    tags  = ["Honest", "Specific", "Human"]
    x_tag = 88
    y_tag = 318

    for tag in tags:
        tw = sw(tag, "Helvetica-Bold", 22)
        c.setFillColor(DARK)
        c.roundRect(x_tag, y_tag, tw + 36, 46, 6, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 22); c.setFillColor(BANANA)
        c.drawString(x_tag + 18, y_tag + 12, tag)
        x_tag += tw + 36 + 18

    logo_badge(c, light=True)
    slide_counter(c, 3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — WHAT WE CHANGED
# ═══════════════════════════════════════════════════════════════════════════════
def slide4(c):
    dark_bg(c)

    # Left banana vertical accent bar
    c.setFillColor(BANANA); c.rect(0, 0, 10, H, stroke=0, fill=1)

    tl(c, "WHAT CHANGED", 88, H - 110, "Helvetica-Bold", 16, BANANA)
    c.setFillColor(BANANA); c.rect(88, H - 122, 80, 5, stroke=0, fill=1)

    items = [
        ("01", "Read every CV before responding"),
        ("02", "Acknowledged what stood out"),
        ("03", "Named the gap \u2014 clearly and kindly"),
        ("04", "Gave direction, not just a decision"),
        ("05", "Treated every candidate as a professional"),
    ]
    y = 770

    for num, text in items:
        # Number in banana
        tl(c, num, 88, y, "Helvetica-Bold", 36, BANANA)
        # Item text in white
        tl(c, text, 168, y, "Helvetica", 28, WHITE)
        # Thin separator
        c.setStrokeColor(DIM); c.setLineWidth(0.5)
        c.line(88, y - 14, W - 88, y - 14)
        y -= 106

    logo_badge(c)
    slide_counter(c, 4, light=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CANDIDATE FEEDBACK
# ═══════════════════════════════════════════════════════════════════════════════
def slide5(c):
    dark_bg(c)

    # Giant watermark quote mark
    c.setFont("Helvetica-Bold", 400); c.setFillColor(HexColor('#1e1e1e'))
    c.drawString(-20, 500, "\u201c")

    tl(c, "WHAT CAME BACK", 88, H - 110, "Helvetica-Bold", 16, BANANA)
    c.setFillColor(BANANA); c.rect(88, H - 122, 80, 5, stroke=0, fill=1)

    margin = 88
    max_w  = W - margin - 60
    y      = 820

    for q in QUOTES:
        clean = q.strip('\u201c\u201d')
        # banana left border
        c.setFillColor(BANANA)
        c.rect(margin, y - 8, 5, 28, stroke=0, fill=1)
        y = twl(c, clean, margin + 22, y,
                "Helvetica-Oblique", 21, WHITE, max_w - 22, lh=30)
        y -= 34

    logo_badge(c)
    slide_counter(c, 5, light=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — VALUES BEHIND IT
# ═══════════════════════════════════════════════════════════════════════════════
def slide6(c):
    dark_bg(c)

    # Top banana band
    c.setFillColor(BANANA)
    c.rect(0, H - 110, W, 110, stroke=0, fill=1)
    tl(c, "THE VALUES BEHIND IT", 88, H - 72, "Helvetica-Bold", 16, DARK)

    pairs = [
        ("Courageous Conversations",
         "We say the hard thing \u2014 clearly and kindly."),
        ("Continuously Improve",
         "Every email made us better at our craft."),
        ("All for One",
         "The candidate\u2019s experience is part of our mission."),
        ("Practice Joy",
         "A well-written email is a small act of care."),
    ]
    y = 780

    for val, desc in pairs:
        # banana dot
        c.setFillColor(BANANA); c.circle(88 + 6, y + 8, 6, stroke=0, fill=1)
        tl(c, val, 110, y, "Helvetica-Bold", 24, BANANA)
        y -= 34
        tl(c, desc, 110, y, "Helvetica", 21, MID)
        y -= 60

    logo_badge(c)
    slide_counter(c, 6, light=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
def slide7(c):
    banana_bg(c)

    # Large dark circle top-left
    circle_deco(c, -120, H + 120, 380, HexColor('#e6c200'))
    circle_deco(c, -120, H + 120, 260, BANANA)

    tl(c, "WHAT HAPPENED NEXT", 88, H - 110, "Helvetica-Bold", 16, DARK)
    c.setFillColor(DARK); c.rect(88, H - 122, 80, 5, stroke=0, fill=1)

    # Bold dark statements
    statements = [
        "Dozens of candidates wrote back.",
        "Not to negotiate. Just to say thank you.",
    ]
    y = 720
    for s in statements:
        twl(c, s, 88, y, "Helvetica-Bold", 50, DARK, 860, lh=62)
        y -= 140

    # Featured quote on dark card
    c.setFillColor(DARK)
    c.roundRect(88, 168, W - 176, 170, 10, stroke=0, fill=1)
    twl(c, QUOTES[1].strip('\u201c\u201d'),
        110, 296, "Helvetica-Oblique", 22, BANANA, W - 220, lh=32)

    logo_badge(c, light=True)
    slide_counter(c, 7)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — CLOSING
# ═══════════════════════════════════════════════════════════════════════════════
def slide8(c):
    dark_bg(c)

    # Mirror of slide 1 — banana circle bottom-left
    circle_deco(c, -60, -60, 380, HexColor('#FFD600'))
    circle_deco(c, -60, -60, 260, DARK)

    # Top-right subtle circle
    circle_deco(c, W + 80, H + 80, 240, HexColor('#1e1e1e'))

    banana_rule(c, 88, 660, 120, h=6)
    tl(c, "PEOPLE & CULTURE  \u00b7  TALEEMABAD",
       88, 632, "Helvetica", 13, MID)

    tl(c, "How we say no", 88, 530, "Helvetica-Bold", 90, WHITE)
    tl(c, "defines who we are.", 88, 412, "Helvetica-Bold", 90, BANANA)

    # Divider + contact
    c.setStrokeColor(DIM); c.setLineWidth(1)
    c.line(88, 358, 500, 358)
    tl(c, "taleemabad.com", 88, 328, "Helvetica", 18, MID)
    tl(c, "hiring@taleemabad.com", 88, 302, "Helvetica", 18, MID)

    logo_badge(c)
    slide_counter(c, 8, light=True)


# ── GENERATE PDF ──────────────────────────────────────────────────────────────
pdf_path = os.path.join(OUT, "showcase_carousel.pdf")
c = rl_canvas.Canvas(pdf_path, pagesize=(W, H))

for fn in [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8]:
    fn(c)
    c.showPage()

c.save()
print(f"Carousel PDF: {pdf_path}")


# ── WHATSAPP PNG (matplotlib) ─────────────────────────────────────────────────
def hx(h): return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

DARK_M   = hx('111111')
BAN_M    = hx('FFD600')
BAN_D_M  = hx('B89E00')
WHITE_M  = (1, 1, 1)
GREY_M   = hx('888888')
DIM_M    = hx('333333')

fig, ax = plt.subplots(figsize=(10.8, 19.2))   # ~1080x1920
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor(tuple(DARK_M))

# Banana decorative circle top-right
circle_tr = plt.Circle((1.12, 1.08), 0.28,
                         color=BAN_M, zorder=1, clip_on=False)
ax.add_patch(circle_tr)
circle_tr2 = plt.Circle((1.12, 1.08), 0.19,
                          color=DARK_M, zorder=2, clip_on=False)
ax.add_patch(circle_tr2)

# Banana accent bar
ax.add_patch(patches.Rectangle((0.06, 0.885), 0.10, 0.006,
                                 color=BAN_M, zorder=3))

# Eyebrow
ax.text(0.06, 0.870, "PEOPLE & CULTURE  ·  TALEEMABAD",
        ha='left', va='top', fontsize=8, color=GREY_M, zorder=3)

# Hero
ax.text(0.06, 0.845, "We changed how we say no.",
        ha='left', va='top', fontsize=22, fontweight='bold',
        color=WHITE_M, zorder=3)
ax.text(0.06, 0.808,
        "A story of craft, courage, and care.",
        ha='left', va='top', fontsize=11, style='italic',
        color=GREY_M, zorder=3)

# Rule
ax.plot([0.06, 0.94], [0.790, 0.790], color=hx('333333'), lw=0.8)

# WHAT CHANGED
y = 0.774
ax.text(0.06, y, "WHAT CHANGED", ha='left', va='top',
        fontsize=9, fontweight='bold', color=BAN_M)
y -= 0.030

items = [
    "01  Read every CV before responding",
    "02  Acknowledged what stood out",
    "03  Named the gap — clearly and kindly",
    "04  Gave direction, not just a decision",
]
for item in items:
    ax.text(0.06, y, item, ha='left', va='top',
            fontsize=11, color=WHITE_M)
    y -= 0.036

ax.plot([0.06, 0.94], [y + 0.012, y + 0.012], color=hx('333333'), lw=0.8)
y -= 0.020

# QUOTES
ax.text(0.06, y, "WHAT CAME BACK", ha='left', va='top',
        fontsize=9, fontweight='bold', color=BAN_M)
y -= 0.032

wap_quotes_raw = [
    ("I\u2019ll be honest, receiving a rejection is never easy, but the way "
     "you delivered this one made all the difference. Thank you for seeing me "
     "as more than just an application."),
    ("This is one of the best rejections I have ever received. "
     "This is one of the reasons which always encourages me "
     "to be part of Taleemabad."),
    ("It is genuinely rare to receive a response this considered. "
     "It speaks well of Taleemabad\u2019s culture."),
]

for q in wap_quotes_raw:
    wrapped = textwrap.fill(q, width=58)
    line_count = wrapped.count('\n') + 1
    box_h = 0.018 + line_count * 0.033

    # banana left border
    ax.add_patch(patches.Rectangle(
        (0.06, y - box_h), 0.006, box_h,
        color=BAN_M, zorder=3))

    ax.text(0.076, y, wrapped,
            ha='left', va='top', fontsize=10.5, style='italic',
            color=WHITE_M, linespacing=1.5, zorder=3)
    y -= box_h + 0.022

ax.plot([0.06, 0.94], [y + 0.008, y + 0.008], color=hx('333333'), lw=0.8)
y -= 0.030

# Closing
ax.text(0.06, y, "How we say no defines who we are.",
        ha='left', va='top', fontsize=14, fontweight='bold',
        color=BAN_M, zorder=3)

# Bottom banana circle
circle_bl = plt.Circle((-0.08, -0.04), 0.22,
                         color=BAN_M, zorder=1, clip_on=False)
ax.add_patch(circle_bl)
circle_bl2 = plt.Circle((-0.08, -0.04), 0.15,
                          color=DARK_M, zorder=2, clip_on=False)
ax.add_patch(circle_bl2)

# Footer
ax.plot([0.04, 0.96], [0.028, 0.028], color=hx('333333'), lw=0.8)
ax.text(0.5, 0.018, "taleemabad.com  ·  People & Culture",
        ha='center', fontsize=9, color=GREY_M)

# Logo
try:
    from matplotlib.image import imread as mpl_imread
    img_arr = mpl_imread(LOGO)
    axin = fig.add_axes([0.06, 0.034, 0.25, 0.040])
    axin.imshow(img_arr)
    axin.axis('off')
except Exception:
    pass

png_path = os.path.join(OUT, "showcase_whatsapp.png")
plt.savefig(png_path, dpi=100, bbox_inches='tight',
            facecolor=tuple(DARK_M))
plt.close()
print(f"WhatsApp PNG: {png_path}")
