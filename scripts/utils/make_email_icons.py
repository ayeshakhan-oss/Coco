from PIL import Image, ImageDraw
from pathlib import Path

OUT = Path(r"c:\Agent Coco\assets\email_icons")
OUT.mkdir(parents=True, exist_ok=True)
SS = 8                      # supersample
S  = 40 * SS                # canvas
STROKE = 2.0 * SS           # thin, restrained
NAVY  = (47, 79, 162, 255)
SLATE = (100, 116, 139, 255)

def new():
    img = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    return img, ImageDraw.Draw(img)

def save(img, name):
    img.resize((40, 40), Image.LANCZOS).save(OUT / f"{name}.png")

def rrect(d, box, r, color, w=STROKE):
    d.rounded_rectangle(box, radius=r, outline=color, width=int(w))

def line(d, a, b, color, w=STROKE):
    d.line([a, b], fill=color, width=int(w))

U = SS  # unit helper (1px at final scale)

def briefcase(c):
    img, d = new()
    rrect(d, [7*U, 14*U, 33*U, 32*U], 3*U, c)
    rrect(d, [15*U, 8*U, 25*U, 14*U], 2*U, c)
    line(d, (7*U, 21*U), (33*U, 21*U), c)
    save(img, "role")

def calendar(c, name="calendar", dot=False):
    img, d = new()
    rrect(d, [7*U, 10*U, 33*U, 32*U], 3*U, c)
    line(d, (7*U, 17*U), (33*U, 17*U), c)
    line(d, (14*U, 6*U), (14*U, 12*U), c)
    line(d, (26*U, 6*U), (26*U, 12*U), c)
    if dot:
        d.ellipse([18*U, 22*U, 22*U, 26*U], fill=c)
    save(img, name)

def wallet(c):
    img, d = new()
    rrect(d, [7*U, 12*U, 33*U, 30*U], 3*U, c)
    rrect(d, [23*U, 18*U, 33*U, 24*U], 2*U, c)
    save(img, "wallet")

def clock(c):
    img, d = new()
    d.ellipse([8*U, 8*U, 32*U, 32*U], outline=c, width=int(STROKE))
    line(d, (20*U, 20*U), (20*U, 13*U), c)
    line(d, (20*U, 20*U), (25*U, 23*U), c)
    save(img, "clock")

def doc(c):
    img, d = new()
    rrect(d, [11*U, 7*U, 29*U, 33*U], 3*U, c)
    for y in (15, 20, 25):
        line(d, (16*U, y*U), (24*U, y*U), c)
    save(img, "doc")

def shield(c):
    img, d = new()
    d.polygon([(20*U, 7*U), (32*U, 12*U), (32*U, 22*U), (20*U, 33*U),
               (8*U, 22*U), (8*U, 12*U)], outline=c, width=int(STROKE))
    line(d, (15*U, 20*U), (19*U, 24*U), c)
    line(d, (19*U, 24*U), (26*U, 16*U), c)
    save(img, "shield")

def hourglass(c):
    img, d = new()
    line(d, (13*U, 8*U), (27*U, 8*U), c)
    line(d, (13*U, 32*U), (27*U, 32*U), c)
    line(d, (13*U, 8*U), (27*U, 32*U), c)
    line(d, (27*U, 8*U), (13*U, 32*U), c)
    save(img, "probation")

def bus(c):
    img, d = new()
    rrect(d, [7*U, 11*U, 33*U, 27*U], 3*U, c)
    line(d, (7*U, 19*U), (33*U, 19*U), c)
    d.ellipse([10*U, 26*U, 16*U, 32*U], outline=c, width=int(STROKE))
    d.ellipse([24*U, 26*U, 30*U, 32*U], outline=c, width=int(STROKE))
    save(img, "commute")

briefcase(NAVY); calendar(NAVY); calendar(SLATE, "calendar_end", dot=True)
wallet(NAVY); clock(NAVY); doc(NAVY)
shield(NAVY); hourglass(NAVY); bus(NAVY)
print("icons:", sorted(p.name for p in OUT.glob('*.png')))
