"""Line art for the Design 3 joining email. Regenerate rather than hand-editing."""
from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path(r"c:\Agent Coco\assets\email_icons")
OUT.mkdir(parents=True, exist_ok=True)
SS = 8
NAVY = (47, 79, 162, 255)
GREEN = (76, 154, 91, 255)
LILAC = (124, 108, 184, 255)


def canvas(w, h):
    img = Image.new("RGBA", (w * SS, h * SS), (255, 255, 255, 0))
    return img, ImageDraw.Draw(img)


def save(img, w, h, name):
    img.resize((w, h), Image.LANCZOS).save(OUT / f"{name}.png")


def icon_users(color, name):
    img, d = canvas(40, 40)
    U = SS
    st = int(2 * SS)
    d.ellipse([11*U, 10*U, 21*U, 20*U], outline=color, width=st)
    d.arc([6*U, 20*U, 26*U, 36*U], 180, 360, fill=color, width=st)
    d.ellipse([23*U, 13*U, 31*U, 21*U], outline=color, width=st)
    d.arc([21*U, 21*U, 36*U, 34*U], 200, 340, fill=color, width=st)
    save(img, 40, 40, name)


def icon_heart(color, name):
    img, d = canvas(40, 40)
    U = SS
    st = int(2 * SS)
    d.arc([9*U, 10*U, 21*U, 24*U], 150, 350, fill=color, width=st)
    d.arc([19*U, 10*U, 31*U, 24*U], 190, 30, fill=color, width=st)
    d.line([(10*U, 19*U), (20*U, 31*U)], fill=color, width=st)
    d.line([(30*U, 19*U), (20*U, 31*U)], fill=color, width=st)
    save(img, 40, 40, name)


def journey(name):
    """Minimal hill/path leading to a small flag."""
    W, H = 260, 120
    img, d = canvas(W, H)
    U = SS
    st = int(1.6 * SS)
    soft = (200, 212, 233, 255)
    # hills
    d.arc([10*U, 46*U, 150*U, 150*U], 200, 340, fill=soft, width=st)
    d.arc([110*U, 30*U, 250*U, 150*U], 200, 345, fill=soft, width=st)
    # winding path
    d.arc([50*U, 74*U, 130*U, 116*U], 200, 350, fill=(214, 224, 240, 255), width=st)
    d.arc([96*U, 58*U, 176*U, 100*U], 190, 340, fill=(214, 224, 240, 255), width=st)
    # ground line
    d.line([(6*U, 104*U), (254*U, 104*U)], fill=soft, width=st)
    # flag pole + pennant
    d.line([(186*U, 34*U), (186*U, 72*U)], fill=NAVY, width=int(2*SS))
    d.polygon([(186*U, 36*U), (212*U, 44*U), (186*U, 52*U)], fill=GREEN)
    save(img, W, H, name)


def hero_pattern(name):
    """Barely-visible open-book line motif for the navy hero."""
    W, H = 300, 200
    img, d = canvas(W, H)
    U = SS
    faint = (255, 255, 255, 26)
    st = int(1.6 * SS)
    # open book: two facing pages
    d.line([(40*U, 150*U), (148*U, 128*U)], fill=faint, width=st)
    d.line([(160*U, 128*U), (268*U, 150*U)], fill=faint, width=st)
    d.line([(40*U, 150*U), (44*U, 96*U)], fill=faint, width=st)
    d.line([(268*U, 150*U), (264*U, 96*U)], fill=faint, width=st)
    d.line([(44*U, 96*U), (150*U, 76*U)], fill=faint, width=st)
    d.line([(158*U, 76*U), (264*U, 96*U)], fill=faint, width=st)
    d.line([(154*U, 76*U), (154*U, 128*U)], fill=faint, width=st)
    for k, y in enumerate((88, 100, 112)):
        d.line([(58*U, (y+6)*U), (140*U, y*U)], fill=faint, width=int(1.2*SS))
        d.line([(168*U, y*U), (250*U, (y+6)*U)], fill=faint, width=int(1.2*SS))
    save(img, W, H, name)


icon_users(NAVY, "users")
icon_heart(LILAC, "heart")
icon_users(GREEN, "users_green")
journey("journey")
hero_pattern("hero_pattern")
print("generated:", sorted(p.name for p in OUT.glob("*.png")))
