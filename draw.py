"""Draw the front page for Saturday 21 November 2026.

A single-image newspaper: masthead, dateline, standfirst, stats strip,
region strip, eight drawn hero cards and six regional brief blocks.
Everything is fixed text and fixed geometry, so the output bytes are
identical on every run. No network, no clock, no randomness.

Run:  python3 draw.py            -> writes entry.png next to this file
"""

from PIL import Image, ImageDraw, ImageFont
import math

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 26
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (24, 24, 22)
SOFT_INK = (74, 70, 64)
RULE = (24, 24, 22)
ACCENT = (178, 32, 44)
GOLD = (176, 124, 28)
MUTED_LINE = (198, 190, 175)

REGION_COLOURS = {
    "EUROPE": (31, 78, 121),
    "AMERICAS": (178, 32, 44),
    "ASIA-PACIFIC": (15, 118, 110),
    "MIDDLE EAST": (146, 96, 20),
    "AFRICA": (46, 125, 50),
    "SPACE": (88, 62, 140),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def load_typefaces():
    """Return the typefaces used on the page, with a safe fallback."""
    try:
        return {
            "serif": ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", 14),
            "serif_bold": ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", 14),
            "sans": ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 10),
            "sans_bold": ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 10),
        }
    except OSError:
        fallback = ImageFont.load_default()
        return {
            "serif": fallback,
            "serif_bold": fallback,
            "sans": fallback,
            "sans_bold": fallback,
        }


FONTS = load_typefaces()


def sized(name, size):
    """A typeface at a given size (fresh object, keeps the code simple)."""
    path = {
        "serif": FONT_DIR + "DejaVuSerif.ttf",
        "serif_bold": FONT_DIR + "DejaVuSerif-Bold.ttf",
        "sans": FONT_DIR + "DejaVuSans.ttf",
        "sans_bold": FONT_DIR + "DejaVuSans-Bold.ttf",
    }[name]
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit_words(text, font, width, max_lines):
    """Wrap text to fit a width, keeping at most max_lines lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and words:
        joined = " ".join(lines)
        if len(joined) < len(text):
            lines[-1] = lines[-1].rstrip()
            while font.getlength(lines[-1] + " ...") > width and lines[-1]:
                lines[-1] = lines[-1][:-1].rstrip()
            lines[-1] += " ..."
    return lines


def text_block(draw, x, y, lines, font, fill, leading):
    """Draw stacked lines, return the y just below the last one."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
# Each scene paints a small drawn illustration inside the given box.
# All coordinates are fixed; nothing here reads the clock or the network.

def scene_kryvyi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    draw.rectangle([x, y, x + w, y + int(h * 0.45)], fill=(18, 28, 54))
    # blast
    cx, cy = x + w - 52, y + 36
    for r, colour in ((30, (255, 157, 0)), (20, (255, 210, 63)), (11, (255, 240, 180))):
        pts = []
        for i in range(12):
            ang = math.pi * i / 6
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=colour)
    # smoke
    draw.ellipse([x + w - 108, y + 8, x + w - 66, y + 34], fill=(107, 114, 128))
    draw.ellipse([x + w - 88, y + 2, x + w - 52, y + 24], fill=(154, 163, 173))
    # rooftops
    base = y + h
    for bx, bw, bh in ((0, 62, 30), (66, 46, 40), (116, 58, 26)):
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(12, 16, 30))
    for wx, wy in ((14, base - 22), (30, base - 14), (78, base - 30), (128, base - 18), (150, base - 12)):
        draw.rectangle([x + wx, wy, x + wx + 4, wy + 5], fill=(255, 210, 63))


def scene_poland(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 242, 245))
    # rough landmass
    draw.polygon([
        (x + 30, y + 12), (x + 150, y + 8), (x + 205, y + 30),
        (x + 215, y + 58), (x + 170, y + 80), (x + 90, y + 82),
        (x + 28, y + 62), (x + 18, y + 34),
    ], fill=(207, 224, 234), outline=(31, 78, 121))
    # flight paths
    draw.arc([x + 150, y - 6, x + 250, y + 60], start=200, end=320, fill=(178, 32, 44), width=2)
    draw.arc([x + 120, y + 10, x + 220, y + 78], start=190, end=300, fill=(178, 32, 44), width=2)
    # impact points
    for px, py in ((x + 66, y + 34), (x + 132, y + 56), (x + 176, y + 28)):
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], outline=(178, 32, 44), width=2)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(178, 32, 44))
    # jets
    for jx, jy in ((x + 196, y + 14), (x + 214, y + 30)):
        draw.polygon([(jx, jy), (jx + 14, jy + 4), (jx, jy + 8)], fill=(24, 24, 22))


def scene_cop(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 239, 232))
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(244, 236, 216))
    # sun
    sx, sy = x + w - 52, y + 26
    for dx, dy in ((-34, 0), (34, 0), (0, -30), (0, 30), (-24, -24), (24, -24)):
        draw.line([sx, sy, sx + dx, sy + dy], fill=(217, 158, 43), width=3)
    draw.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(232, 178, 44))
    # cloud
    draw.ellipse([x + 96, y + 12, x + 150, y + 34], fill=(255, 255, 255))
    draw.ellipse([x + 122, y + 4, x + 172, y + 28], fill=(255, 255, 255))
    # thermometer
    tx = x + 26
    draw.rounded_rectangle([tx, y + 14, tx + 16, y + h - 22], radius=8,
                           fill=(255, 255, 255), outline=(74, 70, 64))
    draw.rectangle([tx + 4, y + 26, tx + 12, y + h - 26], fill=(178, 32, 44))
    draw.ellipse([tx - 3, y + h - 28, tx + 19, y + h - 6], fill=(178, 32, 44))
    # leaf
    draw.polygon([(x + 150, y + h - 8), (x + 178, y + h - 30),
                  (x + 200, y + h - 6)], fill=(46, 125, 50))


def scene_bepi(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(11, 15, 26))
    for sx, sy in ((14, 10), (52, 22), (96, 8), (150, 16), (196, 8),
                   (30, 46), (120, 40), (210, 44), (70, 62), (170, 60)):
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # orbit, kept inside the illustration box
    draw.ellipse([x + 108, y - 6, x + w - 10, y + h + 6], outline=(127, 168, 201), width=2)
    # Mercury
    mx, my, mr = x + w - 62, y + h - 34, 30
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(185, 179, 168))
    for cx, cy, cr in ((-14, -8, 6), (8, 6, 8), (2, -16, 4), (14, -2, 3)):
        draw.ellipse([mx + cx - cr, my + cy - cr, mx + cx + cr, my + cy + cr],
                     fill=(150, 144, 132))
    # probe
    px, py = x + 34, y + 30
    draw.rectangle([px, py, px + 18, py + 12], fill=(217, 158, 43))
    draw.rectangle([px - 22, py + 2, px - 2, py + 10], fill=(63, 105, 160))
    draw.rectangle([px + 18, py + 2, px + 38, py + 10], fill=(63, 105, 160))
    draw.line([px + 9, py + 12, px + 9, py + 20], fill=(217, 158, 43), width=2)


def scene_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(251, 250, 247))
    for gy in range(4):
        yy = y + 12 + gy * 20
        draw.line([x + 8, yy, x + w - 8, yy], fill=(229, 224, 213))
    bars = [(20, 26), (52, 34), (84, 44), (116, 54), (148, 62), (180, 70)]
    for i, (bx, bh) in enumerate(bars):
        colour = (46, 125, 50) if i == 0 else (192, 57, 43)
        draw.rectangle([x + bx, y + h - 10 - bh, x + bx + 22, y + h - 10], fill=colour)
    draw.line([(x + 18, y + 22), (x + 70, y + 40), (x + 120, y + 52),
               (x + 175, y + 66), (x + 214, y + 76)], fill=(142, 31, 22), width=3)


def scene_gta(draw, x, y, w, h):
    bands = [(255, 140, 66), (255, 107, 157), (123, 94, 167), (72, 66, 130)]
    for i, colour in enumerate(bands):
        draw.rectangle([x, y + i * h // 4, x + w, y + (i + 1) * h // 4], fill=colour)
    sx, sy = x + 118, y + 30
    draw.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=(255, 236, 170))
    # skyline
    base = y + h
    for bx, bw, bh in ((0, 40, 26), (44, 30, 38), (78, 36, 22), (118, 44, 34),
                       (166, 30, 26), (200, 37, 40)):
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(46, 38, 84))
    # palms
    for px in (x + 16, x + w - 22):
        draw.line([px, base - 6, px + 4, base - 34], fill=(52, 36, 20), width=3)
        for fx, fy in ((-12, -38), (12, -40), (-8, -46), (10, -48)):
            draw.line([px + 4, base - 34, px + 4 + fx, base - 34 + fy // 2],
                      fill=(36, 94, 52), width=2)


def scene_f1(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(35, 39, 46))
    # chequered strip, contained in the illustration width
    sq = (w - 2) // 14
    for i in range(14):
        for j in range(2):
            if (i + j) % 2 == 0:
                draw.rectangle([x + 1 + i * sq, y + j * 8,
                                x + 1 + (i + 1) * sq, y + (j + 1) * 8],
                               fill=(255, 255, 255))
    # wet sheen
    for sx in (20, 90, 160):
        draw.line([x + sx, y + h - 12, x + sx + 40, y + h - 12], fill=(96, 140, 180), width=2)
    # car
    cx, cy = x + 78, y + 44
    draw.polygon([(cx, cy + 12), (cx + 12, cy), (cx + 84, cy - 2), (cx + 108, cy + 8),
                  (cx + 104, cy + 14), (cx, cy + 16)], fill=(178, 32, 44))
    draw.polygon([(cx + 30, cy + 2), (cx + 44, cy - 8), (cx + 66, cy - 8),
                  (cx + 72, cy + 2)], fill=(24, 24, 22))
    for wx in (cx + 16, cx + 82):
        draw.ellipse([wx, cy + 8, wx + 18, cy + 26], fill=(12, 12, 12))
        draw.ellipse([wx + 6, cy + 14, wx + 12, cy + 20], fill=(180, 180, 180))
    # speed lines
    for lx, ly in ((x + 8, y + 52), (x + 22, y + 62), (x + 4, y + 68)):
        draw.line([lx, ly, lx + 34, ly], fill=(255, 255, 255), width=2)


def scene_tennis(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(63, 143, 79))
    draw.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], fill=(88, 168, 102))
    # court lines
    draw.rectangle([x + 26, y + 14, x + w - 26, y + h - 14], outline=(255, 255, 255), width=2)
    draw.line([x + w // 2, y + 14, x + w // 2, y + h - 14], fill=(255, 255, 255), width=2)
    draw.line([x + 26, y + h // 2, x + w - 26, y + h // 2], fill=(24, 24, 22), width=3)
    # racket, kept inside the illustration box
    rx, ry = x + 42, y + 34
    draw.ellipse([rx, ry, rx + 24, ry + 30], outline=(240, 230, 210), width=3)
    draw.line([rx + 12, ry + 30, rx + 4, ry + 48], fill=(120, 84, 40), width=3)
    # ball
    bx, by = x + w - 52, y + 26
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(205, 220, 57))
    draw.arc([bx - 9, by - 9, bx + 9, by + 9], start=300, end=60, fill=(255, 255, 255), width=2)


SCENES = {
    "kryvyi": scene_kryvyi,
    "poland": scene_poland,
    "cop": scene_cop,
    "bepi": scene_bepi,
    "markets": scene_markets,
    "gta": scene_gta,
    "f1": scene_f1,
    "tennis": scene_tennis,
}

# ---------------------------------------------------------------- content

HEROES = [
    ("EUROPE · UKRAINE", "kryvyi",
     "Double-tap strike kills a boy of 7 in Kryvyi Rih",
     "A boy of 7 and a paramedic, 20, die; 42 are hurt as drones hit rescuers."),
    ("EUROPE · NATO", "poland",
     "Russian missiles land in Poland",
     "Two missiles and a drone land in Poland; Tusk calls it deliberate provocation."),
    ("EUROPE · CLIMATE", "cop",
     "COP31 runs into overtime with no deal",
     "Talks run past their deadline with no deal; the draft drops fossil fuels."),
    ("SPACE", "bepi",
     "BepiColombo reaches Mercury",
     "Eight years out, the probe fires its thrusters for 37 minutes and enters orbit."),
    ("AMERICAS · MARKETS", "markets",
     "Wall Street slides into correction",
     "AI shares lead a rout: the S&P 500 falls 3.7% into correction; Nasdaq -5.3%."),
    ("AMERICAS · CULTURE", "gta",
     "GTA VI: critics 99, players 5.3",
     "Critics give it 99 of 100 - but players drag the user score down to 5.3."),
    ("AMERICAS · SPORT", "f1",
     "Norris on pole; Hamilton last in Vegas",
     "Norris takes a wet pole in Vegas; Hamilton qualifies last in his Ferrari."),
    ("EUROPE · SPORT", "tennis",
     "Alcaraz, Zverev into Turin semis",
     "Alcaraz and Zverev reach the semis; Sinner is out with a knee injury."),
]

# region -> list of (headline, body)
BRIEFS = {
    "EUROPE": [
        ("Estonia to shut its Russian border",
         "All crossings close from 1 Dec for at least six months."),
        ("UK and EU strike three deals",
         "Food, carbon and youth mobility: 100,000 places a year."),
        ("Denmark expels Russian diplomat",
         "Copenhagen acts over an alleged plot on a Ukrainian rapper."),
        ("EU agrees 1bn euros in arms aid for Kyiv",
         "Joint buys via the Peace Facility; delivery by end-2027."),
        ("Britain pledges 1,000 drones for Ukraine",
         "A 260m-pound package of long-range drones for Kyiv."),
        ("Italy walks out over living costs",
         "Workers and students walk out over the cost of living."),
    ],
    "AMERICAS": [
        ("19 years for the Pannun plot",
         "Nikhil Gupta gets 235 months for a murder-for-hire plot."),
        ("Blast kills two Salvadoran troops in Haiti",
         "A camp blast kills two soldiers and wounds two more."),
        ("Palisades fire starter convicted",
         "A jury convicts the man who started the deadly blaze."),
        ("Rikers Island to close by 2032",
         "New York's mayor-elect sets 2032 to shut the jail complex."),
        ("Trump pardons Pete Rose",
         "The late baseball great is pardoned posthumously."),
        ("Magnitude 6.9 quake shakes Peru",
         "A magnitude 6.9 tremor shakes the Andes; no casualties."),
        ("Hyundai unveils a new Elantra",
         "The eighth-generation sedan debuts at the LA Auto Show."),
    ],
    "ASIA-PACIFIC": [
        ("Cyclone Akvan ebbs in Odisha",
         "370,000 evacuated in Odisha; no deaths as the storm ebbs."),
        ("World court: Myanmar committed genocide",
         "The court rules 9-6 the 2016-17 operations were genocide."),
        ("Trump, Xi and Putin meet in Shenzhen",
         "The first Trump-Xi-Putin summit ends with few results."),
        ("Nikkei slides 5.1% in the rout",
         "Tokyo slides 5.1% as the AI rout spreads across Asia."),
        ("Sensex rises 2.3% against the tide",
         "Indian shares rise 2.3% while Brent holds near $90."),
        ("900,000 AI chips sold to China",
         "Nearly 900,000 advanced chips were approved for China."),
        ("Xi warns US on Taiwan",
         "Xi tells Washington to do 'the right thing' on Taiwan."),
    ],
    "MIDDLE EAST": [
        ("Houthi missiles downed over Riyadh",
         "Three missiles are downed over Riyadh; Hodeidah is struck."),
        ("Iran war nears its ninth month",
         "Trump says he is in no rush to decide on strikes."),
        ("Tanker hit by fire near Hormuz",
         "A tanker is hit eight miles north of Khasab."),
        ("US sanctions four Iranians",
         "Treasury lists four men linked to Iranian oil money."),
    ],
    "AFRICA": [
        ("Sudanese army retakes ground in Kordofan",
         "The army says it broke RSF strongholds in West Kordofan."),
        ("Africa's new ratings agency",
         "Can a home-grown rater change how Africa is assessed?"),
    ],
    "SPACE": [
        ("Falcon 9 lofts a secret payload",
         "A Falcon 9 lofts the classified Space Force mission."),
        ("Spy satellites next: NROL-136",
         "Reconnaissance satellites follow on Saturday, 12:30 UTC."),
    ],
}

REGION_ORDER_ROW1 = ["EUROPE", "AMERICAS", "ASIA-PACIFIC"]
REGION_ORDER_ROW2 = ["MIDDLE EAST", "AFRICA", "SPACE"]

STAND_FIRST = (
    "Missiles fall in Poland and a boy dies in Kryvyi Rih as the war widens. "
    "Wall Street slides into correction, COP31 runs past its deadline with no "
    "deal - and, eight years out, a European probe reaches Mercury."
)

STATS = [
    ("S&P 500 -3.7%", "INTO CORRECTION"),
    ("GTA VI 99 / 5.3", "CRITICS VS PLAYERS"),
    ("42 HURT", "KRYVYI RIH DOUBLE-TAP"),
    ("370,000", "EVACUATED IN ODISHA"),
]

FOOTER = (
    "Sources: Reuters, BBC, AP, ESA, Human Rights Watch, UN News, Spaceflight Now, "
    "Metacritic. Every story happened on, or was first reported on, Saturday 21 November 2026."
)

# ---------------------------------------------------------------- painting

def paint_masthead(draw):
    title_font = sized("serif_bold", 44)
    draw.text((MARGIN, 22), "THE WORLD IN ONE DAY", font=title_font, fill=INK)
    right_font = sized("sans_bold", 10)
    small_font = sized("sans", 9)
    draw.text((PAGE_W - MARGIN, 28), "ONE DAY - ONE PAGE",
              font=right_font, fill=INK, anchor="ra")
    draw.text((PAGE_W - MARGIN, 46), "SATURDAY EDITION",
              font=small_font, fill=SOFT_INK, anchor="ra")
    draw.rectangle([MARGIN, 78, PAGE_W - MARGIN, 80], fill=RULE)
    draw.rectangle([MARGIN, 83, PAGE_W - MARGIN, 84], fill=RULE)


def paint_dateline(draw):
    date_font = sized("serif_bold", 21)
    draw.text((MARGIN, 92), "SATURDAY, 21 NOVEMBER 2026", font=date_font, fill=INK)
    count_font = sized("sans_bold", 11)
    draw.text((PAGE_W - MARGIN, 98), "36 STORIES  -  6 REGIONS",
              font=count_font, fill=ACCENT, anchor="ra")


def paint_standfirst(draw):
    font = sized("serif", 14)
    lines = fit_words(STAND_FIRST, font, CONTENT_W, 2)
    text_block(draw, MARGIN, 118, lines, font, SOFT_INK, 17)


def paint_stats(draw, y):
    box_w = (CONTENT_W - 3 * 8) // 4
    value_font = sized("sans_bold", 16)
    label_font = sized("sans_bold", 8)
    for i, (value, label) in enumerate(STATS):
        x = MARGIN + i * (box_w + 8)
        draw.rectangle([x, y, x + box_w, y + 28], outline=MUTED_LINE, width=1)
        draw.rectangle([x, y, x + 4, y + 28], fill=ACCENT if i % 2 == 0 else GOLD)
        draw.text((x + 12, y + 2), value, font=value_font, fill=INK)
        draw.text((x + 12, y + 17), label, font=label_font, fill=SOFT_INK)
    return y + 28


def paint_region_strip(draw, y):
    font = sized("sans_bold", 11)
    counts = {"EUROPE": 10, "AMERICAS": 10, "ASIA-PACIFIC": 7,
              "MIDDLE EAST": 4, "AFRICA": 2, "SPACE": 3}
    x = MARGIN
    for region in ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA", "SPACE"]:
        colour = REGION_COLOURS[region]
        draw.rectangle([x, y + 3, x + 10, y + 13], fill=colour)
        label = "%s %d" % (region, counts[region])
        draw.text((x + 14, y), label, font=font, fill=INK)
        x += 14 + int(font.getlength(label)) + 22
    draw.line([MARGIN, y + 20, PAGE_W - MARGIN, y + 20], fill=MUTED_LINE, width=1)
    return y + 20


def paint_hero(draw, x, y, w, h, kicker, scene, headline, deck):
    if kicker.startswith("AMERICAS"):
        colour = REGION_COLOURS["AMERICAS"]
    elif kicker.startswith("SPACE"):
        colour = REGION_COLOURS["SPACE"]
    else:
        colour = REGION_COLOURS["EUROPE"]
    draw.rectangle([x, y, x + w, y + h], outline=MUTED_LINE, width=1)
    SCENES[scene](draw, x + 1, y + 1, w - 2, 86)
    draw.line([x + 1, y + 87, x + w - 1, y + 87], fill=MUTED_LINE, width=1)
    kicker_font = sized("sans_bold", 9)
    draw.text((x + 8, y + 92), kicker, font=kicker_font, fill=colour)
    head_font = sized("sans_bold", 13)
    head_lines = fit_words(headline, head_font, w - 16, 2)
    text_block(draw, x + 8, y + 105, head_lines, head_font, INK, 15)
    deck_font = sized("sans", 10)
    deck_lines = fit_words(deck, deck_font, w - 16, 2)
    text_block(draw, x + 8, y + 105 + len(head_lines) * 15 + 2,
               deck_lines, deck_font, SOFT_INK, 12)


def paint_brief_block(draw, x, y, w, h, region, extra_note=None):
    colour = REGION_COLOURS[region]
    items = BRIEFS[region]
    head_font = sized("sans_bold", 12)
    draw.rectangle([x, y + 2, x + 10, y + 12], fill=colour)
    draw.text((x + 14, y), region, font=head_font, fill=INK)
    count_font = sized("sans_bold", 10)
    draw.text((x + w, y + 1), str(len(items)), font=count_font,
              fill=colour, anchor="ra")
    draw.line([x, y + 19, x + w, y + 19], fill=MUTED_LINE, width=1)
    by = y + 26
    item_font = sized("sans_bold", 11)
    body_font = sized("sans", 10)
    for headline, body in items:
        head_lines = fit_words(headline, item_font, w, 1)
        text_block(draw, x, by, head_lines, item_font, INK, 13)
        by += 13
        body_lines = fit_words(body, body_font, w, 1)
        text_block(draw, x, by, body_lines, body_font, SOFT_INK, 12)
        by += 12 + 5
    if extra_note:
        note_font = sized("sans", 9)
        draw.line([x, by + 2, x + w, by + 2], fill=MUTED_LINE, width=1)
        note_lines = fit_words(extra_note, note_font, w, 2)
        text_block(draw, x, by + 7, note_lines, note_font, SOFT_INK, 12)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    paint_masthead(draw)
    paint_dateline(draw)
    paint_standfirst(draw)
    stats_bottom = paint_stats(draw, 154)
    strip_bottom = paint_region_strip(draw, stats_bottom + 8)

    # hero grid: 4 columns x 2 rows
    card_w = (CONTENT_W - 3 * 8) // 4
    card_h = 160
    hero_y = strip_bottom + 8
    for i, (kicker, scene, headline, deck) in enumerate(HEROES):
        col = i % 4
        row = i // 4
        cx = MARGIN + col * (card_w + 8)
        cy = hero_y + row * (card_h + 8)
        paint_hero(draw, cx, cy, card_w, card_h, kicker, scene, headline, deck)
    briefs_y = hero_y + 2 * card_h + 8 + 10

    # brief blocks: 3 columns x 2 rows
    block_w = (CONTENT_W - 2 * 12) // 3
    block_h = 216
    for i, region in enumerate(REGION_ORDER_ROW1):
        bx = MARGIN + i * (block_w + 12)
        paint_brief_block(draw, bx, briefs_y, block_w, block_h, region)
    row2_y = briefs_y + block_h + 10
    for i, region in enumerate(REGION_ORDER_ROW2):
        bx = MARGIN + i * (block_w + 12)
        note = None
        if region == "MIDDLE EAST":
            note = "ALSO: Brent crude holds near $90 a barrel."
        if region == "SPACE":
            note = "NEXT UP: the ATP final is Sunday in Turin; NROL-136 lifts off Sunday, 12:30 UTC."
        paint_brief_block(draw, bx, row2_y, block_w, block_h, region,
                          extra_note=note)

    footer_font = sized("sans", 9)
    footer_lines = fit_words(FOOTER, footer_font, CONTENT_W, 1)
    text_block(draw, MARGIN, PAGE_H - 22, footer_lines, footer_font, SOFT_INK, 12)
    return page


def main():
    page = build_page()
    page.save("entry.png", format="PNG")
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
