"""Draw the one-page front page for Saturday 21 November 2026.

Every pixel is painted with Pillow primitives from the facts listed in
STORIES below. No photos, no downloads, no network, no clock reads, so
running this script twice yields the same PNG byte for byte.

Layout (1024 x 1024): masthead, big serif date headline, italic
standfirst, six-number statistics strip, region bar, three hero cards
with drawn scenes, ten smaller drawn cards, a numbered world map beside
the day's remaining briefs, a date-check box and a footer.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 22                      # outer margin
CW = W - 2 * M              # content width

PAPER = (247, 241, 228)
INK = (28, 28, 30)
FAINT = (96, 96, 92)
BRICK = (158, 48, 38)
BRICK_SOFT = (226, 196, 188)
NAVY = (18, 42, 74)
NAVY_SOFT = (36, 68, 108)
TEAL = (24, 104, 96)
GOLD = (176, 128, 32)
GOLD_SOFT = (238, 214, 150)
SKY = (148, 184, 208)
SKY_SOFT = (214, 230, 238)
LAND = (216, 202, 158)
LAND_LINE = (150, 132, 88)
SEA = (222, 232, 236)
CARD = (255, 253, 247)
RULE = (120, 110, 96)
NIGHT = (13, 22, 46)
PURPLE = (58, 32, 92)
GREEN = (34, 110, 60)
RED = (178, 34, 34)

DJV = "/usr/share/fonts/truetype/dejavu/"
NOTO = "/usr/share/fonts/truetype/noto/"


def face(path, size):
    """Load a face; fall back to Pillow's built-in bitmap face."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def serif_b(size):
    return face(DJV + "DejaVuSerif-Bold.ttf", size)


def serif(size):
    return face(NOTO + "NotoSerif-Regular.ttf", size)


def serif_i(size):
    return face(NOTO + "NotoSerif-Italic.ttf", size)


def sans(size):
    return face(DJV + "DejaVuSans.ttf", size)


def sans_b(size):
    return face(DJV + "DejaVuSans-Bold.ttf", size)


def wrap(d, text, font, width):
    """Greedy word wrap using the font's real metrics."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = font.size + 4
    lines = wrap(d, text, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def card_frame(d, x, y, w, h, fill=CARD):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=fill,
                        outline=RULE, width=1)


def kicker(d, x, y, num, place, topic, color=BRICK, size=11):
    f = sans_b(size)
    d.text((x, y), "%d · %s · %s" % (num, place, topic), font=f, fill=color)


def headline(d, x, y, text, font, width, fill=INK, max_lines=3):
    lines = wrap(d, text, font, width)[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + 3
    return y


def burst(d, cx, cy, r, fill, spikes=8):
    """A small explosion star centred on (cx, cy)."""
    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def dashed(d, p0, p1, fill, dash=5, gap=4, width=2):
    """A dashed straight line between two points."""
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist == 0:
        return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    s = 0.0
    while s < dist:
        e = min(s + dash, dist)
        d.line([(x0 + ux * s, y0 + uy * s), (x0 + ux * e, y0 + uy * e)],
               fill=fill, width=width)
        s = e + gap

# ---------------------------------------------------------------------------
# Drawn scenes: one small original illustration per featured story.
# Each takes the card's picture box (x, y, w, h) and paints inside it.
# ---------------------------------------------------------------------------

def pic_kyiv(d, x, y, w, h):
    """Night skyline under missile trails."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(14, 22), (60, 12), (110, 26), (160, 14), (210, 20),
                   (260, 10), (290, 24)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    for bx, bw, bh in [(0, 46, 58), (52, 30, 78), (88, 40, 52), (134, 34, 86),
                       (174, 44, 62), (224, 30, 80), (260, 42, 66),
                       (308, 26, 54)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(8, 14, 30))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            d.rectangle([x + bx + 6, wy, x + bx + 10, wy + 5], fill=(240, 200, 90))
    dashed(d, (x + 20, y + 8), (x + 90, y + h - 46), (250, 200, 120), width=2)
    dashed(d, (x + 150, y + 6), (x + 210, y + h - 52), (250, 200, 120), width=2)
    dashed(d, (x + 250, y + 10), (x + 290, y + h - 40), (250, 200, 120), width=2)
    burst(d, x + 90, y + h - 46, 13, (255, 170, 40))
    burst(d, x + 210, y + h - 52, 11, (255, 170, 40))
    burst(d, x + 290, y + h - 40, 12, (255, 120, 30))
    d.text((x + 8, y + h - 18), "OVERNIGHT STRIKES", font=sans_b(9),
           fill=(255, 255, 255))


def pic_cop(d, x, y, w, h):
    """Globe, thermometer and a stalled clock for the climate talks."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_SOFT)
    cx, cy, r = x + 62, y + h // 2 + 4, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 144, 190))
    d.ellipse([cx - 26, cy - 30, cx + 2, cy - 6], fill=(96, 176, 110))
    d.ellipse([cx + 4, cy + 8, cx + 30, cy + 32], fill=(96, 176, 110))
    d.ellipse([cx - 8, cy - 4, cx + 14, cy + 12], fill=(96, 176, 110))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 330, fill=(255, 255, 255), width=2)
    tx = x + w - 52
    d.rounded_rectangle([tx, y + 14, tx + 16, y + h - 26], radius=8,
                        fill=(255, 255, 255), outline=BRICK, width=2)
    d.rectangle([tx + 2, y + h - 48, tx + 14, y + h - 28], fill=RED)
    d.ellipse([tx - 3, y + h - 34, tx + 19, y + h - 12], fill=RED)
    d.rectangle([x + w - 108, y + 8, x + w - 8, y + 28], fill=BRICK)
    d.text((x + w - 102, y + 11), "NO DEAL", font=sans_b(11), fill=(255, 255, 255))
    d.text((x + 8, y + h - 18), "OVERTIME · 3RD DRAFT DUE SAT", font=sans_b(9),
           fill=NAVY)


def pic_mercury(d, x, y, w, h):
    """Mercury, its craters, and the arriving twin orbiters."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(10, 14), (40, 30), (90, 10), (140, 22), (200, 12),
                   (250, 28), (290, 14), (180, 40), (310, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    cx, cy, r = x + w - 88, y + h // 2 + 2, 46
    d.ellipse([cx - r - 30, cy - r - 10, cx + r + 30, cy + r + 10],
              outline=(120, 140, 180), width=1)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 164, 132))
    for ox, oy, orr in [(-18, -12, 9), (12, -20, 6), (20, 10, 11), (-8, 16, 7),
                        (2, -2, 5), (-26, 8, 5)]:
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(168, 134, 102))
    dashed(d, (x + 16, y + 22), (cx - r - 14, cy - 6), (240, 200, 120), width=2)
    px, py = cx - r - 34, cy - 16
    d.rectangle([px, py, px + 26, py + 12], fill=(220, 220, 220))
    d.rectangle([px - 16, py + 2, px, py + 10], fill=(150, 180, 210))
    d.rectangle([px + 26, py + 2, px + 42, py + 10], fill=(150, 180, 210))
    d.text((x + 8, y + h - 18), "BURN 19:24 CET · 37 MIN", font=sans_b(9),
           fill=(255, 255, 255))


def pic_cyclone(d, x, y, w, h):
    """Spiral storm over a coastline."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_SOFT)
    d.polygon([(x + w - 46, y + h), (x + w, y + h), (x + w, y + 14),
               (x + w - 24, y + 30)], fill=(196, 178, 130))
    cx, cy = x + 118, y + h // 2 + 2
    for i, rr in enumerate([20, 15, 10, 5]):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 20 + i * 40, 300 + i * 40,
              fill=NAVY, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BRICK)
    for rx in range(x + 8, x + 58, 14):
        d.line([(rx, y + 22), (rx - 3, y + 32)], fill=(90, 130, 170), width=2)
    d.text((x + 8, y + 5), "209 MM", font=sans_b(9), fill=NAVY)


def pic_cricket(d, x, y, w, h):
    """Pitch, stumps, bat and ball."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 170))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 160, 90))
    d.rectangle([x + 30, y + 12, x + w - 30, y + h - 22], fill=(222, 200, 150))
    for sx in (x + w - 52, x + w - 47, x + w - 42):
        d.line([(sx, y + 26), (sx, y + 44)], fill=(240, 210, 120), width=3)
    d.line([(x + w - 54, y + 24), (x + w - 40, y + 24)], fill=(240, 210, 120),
           width=2)
    d.polygon([(x + 44, y + 16), (x + 58, y + 12), (x + 52, y + 44),
               (x + 40, y + 48)], fill=(190, 150, 90))
    d.line([(x + 56, y + 13), (x + 66, y + 2)], fill=(120, 90, 50), width=4)
    d.ellipse([x + 108, y + 18, x + 122, y + 32], fill=RED)
    d.rectangle([x + 8, y + 6, x + 74, y + 22], fill=NAVY)
    d.text((x + 12, y + 8), "IND 239/1", font=sans_b(10), fill=(255, 255, 255))


def pic_gta(d, x, y, w, h):
    """Two score bars: critics love it, users do not."""
    d.rectangle([x, y, x + w, y + h], fill=PURPLE)
    d.text((x + 8, y + 8), "VI", font=serif_b(22), fill=(255, 255, 255))
    bx = x + 64
    d.text((bx, y + 6), "CRITICS  99", font=sans_b(8), fill=(255, 255, 255))
    d.rectangle([bx, y + 17, bx + 112, y + 23], fill=(255, 255, 255))
    d.rectangle([bx, y + 17, bx + 111, y + 23], fill=(60, 180, 90))
    d.text((bx, y + 27), "USERS  5.3", font=sans_b(8), fill=(255, 255, 255))
    d.rectangle([bx, y + 38, bx + 112, y + 44], fill=(255, 255, 255))
    d.rectangle([bx, y + 38, bx + 59, y + 44], fill=(220, 70, 60))


def pic_f1(d, x, y, w, h):
    """Night circuit, chequered flag and a car."""
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    d.arc([x + 10, y - 30, x + w - 10, y + 40], 25, 155, fill=(240, 200, 90),
          width=3)
    d.arc([x + 18, y - 22, x + w - 18, y + 48], 25, 155, fill=(200, 200, 200),
          width=1)
    for i in range(3):
        for j in range(2):
            fill = (255, 255, 255) if (i + j) % 2 == 0 else INK
            d.rectangle([x + w - 26 + i * 6, y + 5 + j * 6,
                         x + w - 20 + i * 6, y + 11 + j * 6], fill=fill)
    d.rounded_rectangle([x + 52, y + h - 22, x + 112, y + h - 8], radius=5,
                        fill=(200, 40, 40))
    d.ellipse([x + 62, y + h - 14, x + 74, y + h - 6], fill=INK)
    d.ellipse([x + 94, y + h - 14, x + 106, y + h - 6], fill=INK)
    d.text((x + 8, y + 5), "1:47.272", font=sans_b(9), fill=(255, 255, 255))


def pic_atp(d, x, y, w, h):
    """Indoor hard court, net and ball."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 96, 168))
    d.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], fill=(96, 140, 200))
    d.line([(x + 14, y + h // 2), (x + w - 14, y + h // 2)], fill=(255, 255, 255),
           width=2)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)], fill=(255, 255, 255),
           width=1)
    d.ellipse([x + w - 34, y + 10, x + w - 14, y + 30], fill=(210, 230, 60))
    d.arc([x + w - 34, y + 10, x + w - 14, y + 30], 200, 340, fill=(255, 255, 255),
          width=1)
    d.text((x + 8, y + 6), "SF · TODAY", font=sans_b(9), fill=(255, 255, 255))


def pic_car(d, x, y, w, h):
    """A saloon in profile under show lights."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    d.polygon([(x + 22, y + h - 22), (x + 34, y + h - 34), (x + 62, y + h - 40),
               (x + 108, y + h - 40), (x + 128, y + h - 30), (x + 152, y + h - 22)],
              fill=(40, 60, 110))
    d.polygon([(x + 44, y + h - 38), (x + 62, y + h - 38),
               (x + 58, y + h - 28), (x + 46, y + h - 28)], fill=(180, 210, 230))
    d.polygon([(x + 70, y + h - 38), (x + 102, y + h - 38),
               (x + 100, y + h - 28), (x + 70, y + h - 28)], fill=(180, 210, 230))
    d.ellipse([x + 40, y + h - 22, x + 58, y + h - 8], fill=INK)
    d.ellipse([x + 116, y + h - 22, x + 134, y + h - 8], fill=INK)
    d.ellipse([x + 150, y + h - 30, x + 156, y + h - 24], fill=(255, 220, 100))
    d.text((x + 8, y + 6), "LA AUTO SHOW", font=sans_b(9), fill=NAVY)


def pic_border(d, x, y, w, h):
    """A closed crossing: barrier stripes on a dashed border."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 214))
    d.rectangle([x, y, x + w // 2 - 2, y + h], fill=(168, 196, 168))
    d.rectangle([x + w // 2 + 2, y, x + w, y + h], fill=(196, 214, 196))
    dashed(d, (x + w // 2, y + 4), (x + w // 2, y + h - 4), BRICK, dash=4,
           gap=3, width=2)
    for i in range(5):
        xx = x + w // 2 - 26 + i * 11
        d.polygon([(xx, y + 12), (xx + 6, y + 12), (xx + 2, y + 24),
                   (xx - 4, y + 24)], fill=BRICK if i % 2 == 0 else (255, 255, 255))
    d.text((x + 8, y + h - 16), "FROM 1 DEC", font=sans_b(9), fill=BRICK)


def pic_court(d, x, y, w, h):
    """Courthouse pediment and columns."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.polygon([(x + 20, y + 14), (x + w // 2, y + 2), (x + w - 20, y + 14)],
              fill=(120, 110, 90))
    for cx in (x + 34, x + 74, x + 114, x + 148):
        d.rectangle([cx, y + 16, cx + 10, y + h - 10], fill=(245, 240, 225),
                    outline=(120, 110, 90))
    d.rectangle([x + 16, y + h - 10, x + w - 16, y + h - 4], fill=(120, 110, 90))
    d.text((x + 6, y + 3), "19 YRS 7 MOS", font=sans_b(9), fill=BRICK)


def pic_haiti(d, x, y, w, h):
    """Blast lines over a map pin."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 220, 200))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=BRICK)
    d.polygon([(cx, cy + 26), (cx - 12, cy + 6), (cx + 12, cy + 6)], fill=BRICK)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    for ang in (200, 250, 290, 340, 30, 80):
        a = math.radians(ang)
        d.line([(cx + 22 * math.cos(a), cy + 22 * math.sin(a)),
                (cx + 32 * math.cos(a), cy + 32 * math.sin(a))],
               fill=BRICK, width=2)
    d.text((x + 8, y + 6), "PORT-AU-PRINCE", font=sans_b(9), fill=BRICK)


def pic_chip(d, x, y, w, h):
    """A processor under a magnifier."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 44, 66))
    cx, cy = x + w // 2, y + h // 2
    for i in range(-2, 3):
        d.line([(cx - 26, cy + i * 10), (cx - 16, cy + i * 10)], fill=GOLD, width=2)
        d.line([(cx + 16, cy + i * 10), (cx + 26, cy + i * 10)], fill=GOLD, width=2)
        d.line([(cx + i * 10, cy - 26), (cx + i * 10, cy - 16)], fill=GOLD, width=2)
        d.line([(cx + i * 10, cy + 16), (cx + i * 10, cy + 26)], fill=GOLD, width=2)
    d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], fill=(60, 90, 120),
                outline=GOLD, width=2)
    d.text((cx - 8, cy - 8), "AI", font=sans_b(11), fill=(255, 255, 255))
    d.text((x + 8, y + 6), "SUBPOENA", font=sans_b(9), fill=(255, 220, 120))

# ---------------------------------------------------------------------------
# The day's stories. Every fact below was reported on Saturday 21 November
# 2026 (or is a scheduled event of that day, flagged as such). Sources are
# named beside each story on the page and listed in full in README.md.
# ---------------------------------------------------------------------------

HEROES = [
    dict(num=1, place="KYIV", topic="WAR", pic=pic_kyiv,
         head="Russian strikes kill two in Kryvyi Rih; missiles land in Poland",
         body=("A double-tap strike on Kryvyi Rih killed two, among them a "
               "seven-year-old, and hurt 42. Two more died at Lviv's railway "
               "station; two missiles landed in Poland as Putin ruled out an "
               "energy ceasefire."),
         src="AppiSToS · Reuters"),
    dict(num=2, place="ANTALYA", topic="CLIMATE", pic=pic_cop,
         head="COP31 runs into overtime with no deal",
         body=("Two weeks of talks ended on Friday with no final text. A third "
               "draft is due Saturday morning; the last one drops fossil fuels "
               "and the $120bn figure. \u201cWe are close to the finish line but "
               "not there yet,\u201d said president Kurum."),
         src="AP · UN News · Asia Today"),
    dict(num=3, place="MERCURY", topic="SPACE", pic=pic_mercury,
         head="BepiColombo reaches Mercury tonight",
         body=("After eight years and 10 billion km, the twin orbiters fire "
               "their thrusters at 19:24 CET for a 37-minute burn to be caught "
               "by Mercury's gravity \u2014 the first two spacecraft there at once. "
               "Science starts in April 2027."),
         src="ESA · Sky & Telescope"),
]

MEDIUM = [
    dict(num=4, place="ODISHA", topic="STORM", pic=pic_cyclone,
         head="Akvan leaves no dead; 372,000 moved",
         body=("No deaths, no major damage; Patrapur took 209 mm of rain."),
         src="IMD · Reuters"),
    dict(num=5, place="WELLINGTON", topic="CRICKET", pic=pic_cricket,
         head="Rahul's hundred leads India's reply",
         body=("Rahul's century on day three; India 239/1 at lunch, "
               "chasing 368."),
         src="Reuters · AP"),
    dict(num=6, place="WORLDWIDE", topic="GAMES", pic=pic_gta,
         head="GTA VI: critics 99, users 5.3",
         body=("User score sank to 3.7 in a bombing wave, then climbed "
               "to 5.3."),
         src="ComicBook"),
    dict(num=7, place="LAS VEGAS", topic="F1", pic=pic_f1,
         head="Russell fastest; qualifying tonight",
         body=("Russell led wet FP2 in 1:47.272; qualifying at 04:00 UTC "
               "Saturday."),
         src="RacingNews365"),
    dict(num=8, place="TURIN", topic="TENNIS", pic=pic_atp,
         head="Top four seeds reach Turin semis",
         body=("Medvedev beat Tiafoe 6-3, 6-4 to complete the semi-final "
               "line-up."),
         src="ATP Tour"),
    dict(num=9, place="LOS ANGELES", topic="MOTORS", pic=pic_car,
         head="Hyundai shows off new Elantra",
         body=("Eighth-gen Elantra debuts at the LA Auto Show, with hybrid "
               "options."),
         src="Jagran Josh"),
    dict(num=10, place="TALLINN", topic="BORDERS", pic=pic_border,
         head="Estonia to shut Russia crossings",
         body=("Estonia will close its crossings with Russia from "
               "1 December."),
         src="AppiSToS"),
    dict(num=11, place="NEW YORK", topic="COURTS", pic=pic_court,
         head="19 years for Pannun murder plot",
         body=("Gupta jailed 19 years 7 months over the foiled Pannun "
               "murder plot."),
         src="AppiSToS"),
    dict(num=12, place="HAITI", topic="SECURITY", pic=pic_haiti,
         head="Two Salvadorans killed in Haiti blast",
         body=("Two Salvadorans killed handling explosives, military says."),
         src="AppiSToS"),
    dict(num=13, place="CALIFORNIA", topic="TECH", pic=pic_chip,
         head="California subpoenas Nvidia",
         body=("California subpoenaed Nvidia over alleged chip sales to "
               "China."),
         src="AppiSToS"),
]

BRIEFS = [
    (14, "Trump team seeks Ukraine peace deal by January", "AppiSToS"),
    (15, "US defence chief limits military ties with Canada", "AppiSToS"),
    (16, "Houthi strike hits Riyadh tower, no injuries", "AppiSToS"),
    (17, "Iraqi forces to enter Hezbollah stronghold", "AppiSToS"),
    (18, "22,000 children killed in Gaza, ministry says", "AppiSToS"),
    (19, "Yemen's displaced hit ~357,000 since August", "AppiSToS"),
    (20, "Ebola in DRC hits children; ~100 schools affected", "AppiSToS"),
    (21, "Taiwan tells Meta China-linked accounts sway votes", "AppiSToS"),
    (22, "Hungary lifts block on EU talks with Ukraine", "AppiSToS"),
    (23, "Morocco pledges \u20ac366m to build defence industry", "AppiSToS"),
    (24, "Switzerland backs ICJ ruling on Myanmar", "AppiSToS"),
    (25, "China seeks full Rohingya solution after ICJ verdict", "AppiSToS"),
    (26, "Four students killed in Afghan munitions blast", "AppiSToS"),
    (27, "Zelensky: Ukraine hit three Russian launchers", "AppiSToS"),
    (28, "Croatia charges three in daycare subsidy fraud", "AppiSToS"),
    (29, "Palestinian shot dead by settler guard in West Bank", "AppiSToS"),
    (30, "North Korea, Laos vow closer ties in Pyongyang", "AppiSToS"),
    (31, "Tata Group faces criminal trial in Netherlands", "AppiSToS"),
    (32, "US allows Pacific seabed mining exploration", "AppiSToS"),
    (33, "US, Israel weigh fresh strike on Tehran: sources", "AppiSToS"),
    (34, "Europe's leaders call for winter ceasefire", "AppiSToS"),
    (35, "Bessent: humans must stay in charge of AI weapons", "AppiSToS"),
    (36, "Johnson urges Republicans to stay in Capitol", "AppiSToS"),
]

STATS = [
    ("2", "killed in Kryvyi Rih"),
    ("372,000", "people moved from Akvan's path"),
    ("5.3", "GTA VI user score (critics: 99)"),
    ("209 mm", "rain at Patrapur, Odisha"),
    ("19:24", "CET: BepiColombo's Mercury burn"),
    ("8 yrs", "BepiColombo's journey to Mercury"),
]

REGIONS = [
    ("EUROPE", 11, (36, 68, 108)),
    ("AMERICAS", 9, (158, 48, 38)),
    ("ASIA-PACIFIC", 6, (176, 128, 32)),
    ("MIDDLE EAST", 6, (24, 104, 96)),
    ("AFRICA", 2, (90, 130, 60)),
    ("SPACE", 2, (90, 90, 100)),
]

# (lon, lat) of the drawn stories' places, for the numbered map.
PINS = [
    (1, 30.5, 50.5), (2, 30.7, 36.9), (4, 84.9, 19.3),
    (5, 174.8, -41.3), (6, -80.2, 25.8), (7, -115.1, 36.2),
    (8, 7.7, 45.1), (9, -118.2, 34.1), (10, 24.7, 59.4),
    (11, -74.0, 40.7), (12, -72.3, 18.5), (13, -122.0, 37.4),
]

CONTINENTS = {
    "n_america": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73),
                  (-65, 62), (-55, 52), (-60, 45), (-75, 35), (-80, 26),
                  (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
                  (-125, 49), (-145, 60)],
    "s_america": [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5),
                  (-35, -10), (-40, -20), (-50, -30), (-60, -38), (-70, -50),
                  (-75, -40), (-70, -20), (-80, -5)],
    "europe": [(-10, 36), (-10, 43), (0, 48), (-5, 50), (5, 58), (10, 58),
               (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60),
               (40, 50), (30, 46), (28, 40), (23, 36), (15, 38), (8, 38),
               (0, 36)],
    "africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
               (35, 28), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10),
               (35, -20), (32, -29), (25, -34), (18, -35), (15, -27),
               (12, -18), (9, -1), (9, 4), (-8, 5)],
    "asia": [(40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (170, 67),
             (178, 65), (162, 60), (158, 52), (142, 45), (135, 35),
             (127, 33), (122, 30), (120, 22), (110, 20), (105, 10),
             (100, 8), (95, 15), (90, 22), (80, 15), (77, 8), (72, 20),
             (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (43, 35),
             (40, 40)],
    "oceania": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
                (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
                (150, -22), (146, -19), (142, -15), (142, -11), (136, -12),
                (132, -12), (126, -14), (122, -17), (118, -20)],
}


def draw_map(d, x, y, w, h):
    """Simplified world map with numbered pins for stories 1-13."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    lon0, lon1, lat0, lat1 = -170, 190, -56, 84

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat1 - lat) / (lat1 - lat0) * h
        return (px, py)

    for poly in CONTINENTS.values():
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, lon, lat in PINS:
        cx, cy = proj(lon, lat)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=BRICK,
                  outline=(255, 255, 255), width=1)
        d.text((cx - 3 if num < 10 else cx - 6, cy - 6), str(num),
               font=sans_b(9), fill=(255, 255, 255))
    d.text((x + 4, y + h - 14),
           "3 is in space: Mercury. Pins 1-13 mark the drawn stories.",
           font=sans(8), fill=FAINT)

# ---------------------------------------------------------------------------
# Page assembly.
# ---------------------------------------------------------------------------

def draw_hero(d, x, y, w, h, s):
    card_frame(d, x, y, w, h)
    s["pic"](d, x + 1, y + 1, w - 2, 92)
    kicker(d, x + 12, y + 100, s["num"], s["place"], s["topic"])
    ty = headline(d, x + 12, y + 114, s["head"], serif_b(16), w - 24,
                  max_lines=3)
    para(d, x + 12, ty + 2, s["body"], sans(9), w - 24, leading=12,
         max_lines=4)
    d.text((x + 12, y + h - 14), "\u2014 " + s["src"], font=sans(9), fill=FAINT)


def draw_medium(d, x, y, w, h, s):
    card_frame(d, x, y, w, h)
    s["pic"](d, x + 1, y + 1, w - 2, 48)
    kicker(d, x + 8, y + 54, s["num"], s["place"], s["topic"], size=8)
    src = s["src"]
    d.text((x + w - 8 - d.textlength(src, font=sans(8)), y + 55), src,
           font=sans(8), fill=FAINT)
    ty = headline(d, x + 8, y + 66, s["head"], serif_b(12), w - 16, max_lines=2)
    para(d, x + 8, ty + 2, s["body"], sans(9), w - 16, leading=11,
         max_lines=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.text((M, 10), "THE WORLD IN ONE DAY", font=sans_b(13), fill=BRICK)
    right = "36 STORIES \u00b7 SIX REGIONS \u00b7 ALL FROM THIS ONE DAY"
    d.text((W - M - d.textlength(right, font=sans(11)), 12), right,
           font=sans(11), fill=FAINT)
    rule(d, M, W - M, 30, fill=INK, width=2)

    # Date headline and standfirst.
    d.text((M, 34), "Saturday 21 November 2026", font=serif_b(52), fill=INK)
    d.text((M, 90), "Russian strikes hit Ukraine overnight \u00b7 COP31 runs into "
           "overtime with no deal \u00b7 BepiColombo reaches Mercury tonight",
           font=serif_i(15), fill=BRICK)
    rule(d, M, W - M, 112, fill=INK, width=1)

    # Statistics strip.
    cell = CW // 6
    for i, (big, small) in enumerate(STATS):
        cx = M + i * cell
        d.text((cx + 8, 118), big, font=serif_b(25), fill=NAVY)
        para(d, cx + 8, 146, small, sans(9), cell - 16, fill=FAINT,
             leading=11, max_lines=2)
        if i:
            d.line([(cx, 116), (cx, 166)], fill=RULE, width=1)
    rule(d, M, W - M, 170, fill=INK, width=1)

    # Region bar: small regions get a fixed floor, the rest share the rest.
    rx = M
    fixed = {"AFRICA": 76, "SPACE": 76}
    flex_total = sum(n for name, n, _ in REGIONS if name not in fixed)
    flex_w = CW - sum(fixed.values())
    for name, n, color in REGIONS:
        if name in fixed:
            seg = fixed[name]
        else:
            seg = int(flex_w * n / flex_total)
        d.rectangle([rx, 176, rx + seg - 2, 194], fill=color)
        label = "%s %d" % (name, n)
        d.text((rx + 6, 180), label, font=sans_b(10), fill=(255, 255, 255))
        rx += seg

    # Hero cards.
    hw = (CW - 20) // 3
    for i, s in enumerate(HEROES):
        draw_hero(d, M + i * (hw + 10), 202, hw, 228, s)

    # Medium cards, two rows of five.
    mw = (CW - 40) // 5
    for row in range(2):
        for i, s in enumerate(MEDIUM[row * 5:(row + 1) * 5]):
            draw_medium(d, M + i * (mw + 10), 438 + row * 138, mw, 130, s)

    # Map and briefs.
    by = 714
    d.text((M, by), "WHERE IT HAPPENED", font=sans_b(11), fill=BRICK)
    d.text((312, by), "ALSO ON SATURDAY 21 NOVEMBER \u2014 23 MORE STORIES",
           font=sans_b(11), fill=BRICK)
    draw_map(d, M, by + 18, 278, 190)
    col_w = 335
    for j, (num, text, src) in enumerate(BRIEFS):
        col = j // 12
        row = j % 12
        bx = 312 + col * (col_w + 10)
        yy = by + 20 + row * 16
        line = "%d %s (%s)" % (num, text, src)
        d.text((bx, yy), line, font=sans(10), fill=INK)

    # Date check: yesterday's news, deliberately left out.
    d.rounded_rectangle([M, 930, W - M, 980], radius=3, outline=BRICK, width=2)
    para(d, M + 10, 936,
         "DATE CHECK \u2713 \u2014 Not Saturday's news, so not on this page: the "
         "Kyiv bridges barrage \u00b7 Cyclone Akvan's landfall \u00b7 the COP31 draft "
         "that dropped fossil fuels \u00b7 the ICJ's Myanmar ruling \u00b7 the "
         "Trump\u2013Xi\u2013Putin summit \u00b7 the Senate's war-powers vote \u00b7 GTA "
         "VI's launch \u00b7 Anthropic's market debut \u00b7 the UK\u2013EU deal \u00b7 "
         "Voyager 1's light-day \u00b7 the bank vendor-breach disclosures \u00b7 the "
         "EU's \u20ac1bn Ukraine aid \u00b7 the Pete Rose pardon \u2014 19\u201320 November.",
         sans(10), CW - 20, fill=INK, leading=13, max_lines=3)

    # Footer.
    para(d, M, 986,
         "Every story here happened, or was first reported, on Saturday "
         "21 November 2026. Disputed claims are attributed, not stated as fact.",
         sans(9), CW, fill=FAINT, leading=12, max_lines=1)
    para(d, M, 1000,
         "Sources: Reuters, AP, AFP, IMD, ESA, ATP Tour, UN News, Asia Today, "
         "Sky & Telescope, ComicBook, Fextralife, RacingNews365, ESPN, "
         "Jagran Josh, AppiSToS \u00b7 Original drawings",
         sans(9), CW, fill=FAINT, leading=12, max_lines=1)
    return img


def main():
    img = build()
    img.save("entry.png", format="PNG", optimize=True)
    print("Wrote entry.png (%d bytes, %dx%d)"
          % (len(open("entry.png", "rb").read()), W, H))


if __name__ == "__main__":
    main()
