# draw.py -- pure-stdlib newspaper renderer for news-image-20261121 v3.
# Draws "Saturday 21 November 2026" as a one-page broadsheet: giant serif-style
# masthead, THE DAY IN UTC strip, big-number strip, region bars, 3 large hero
# cards with drawn illustrations, 10 small stories, a WHERE IT HAPPENED world
# map, an ALSO list, a DATE CHECK box and a HOW WE CHECKED footer.
# Everything is drawn from code (no image assets, no network, deterministic).
import struct
import zlib

W, H = 1024, 1024

# ---------------- palette ----------------
PAPER = (247, 243, 232)
PAPER2 = (241, 235, 220)
INK = (26, 26, 26)
INK_SOFT = (74, 74, 74)
BLACK = (17, 17, 17)
RED = (178, 34, 34)
RED_DARK = (139, 0, 0)
GREEN = (46, 125, 50)
GREEN_DARK = (27, 94, 32)
BLUE = (31, 78, 121)
SKY = (191, 217, 232)
SAND = (232, 220, 192)
GOLD = (180, 120, 20)
GREY = (120, 120, 115)
LIGHT_GREY = (225, 222, 210)
WHITE = (255, 255, 255)

REGION_COLORS = {
    "EUROPE": (46, 90, 136),
    "AMERICAS": (123, 45, 38),
    "ASIA": (46, 125, 50),
    "MIDDLE EAST": (194, 65, 12),
    "GLOBAL": (87, 83, 78),
    "AFRICA": (109, 40, 217),
    "OCEANIA": (14, 116, 144),
}

# ---------------- 5x7 bitmap font ----------------
# Each glyph: 7 rows of 5 bits, written as 5-char strings of 0/1.
FONT = {
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01000", "01000", "11100", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "·": ("00000", "00000", "00000", "01100", "01100", "00000", "00000"),
    "/": ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "°": ("00110", "01001", "01001", "00110", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "•": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
}
# Normalise fancy punctuation to glyphs we carry.
NORMALISE = {
    "–": "-", "—": "-", "’": "'", "‘": "'", "“": '"', "”": '"',
    "…": ".", "×": "x", "~": "-", "…": ".",
}
BLANK = ("00000", "00000", "00000", "00000", "00000", "00000", "00000")


def glyph(ch):
    ch = NORMALISE.get(ch, ch)
    return FONT.get(ch, BLANK)


# ---------------- canvas ----------------
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = color[0]
                self.px[i + 1] = color[1]
                self.px[i + 2] = color[2]

    def hline(self, x, y, w, color):
        self.fill_rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.fill_rect(x, y, 1, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def dashed_line(self, x0, y0, x1, y1, color, dash=4, gap=3):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        if steps == 0:
            return
        on = True
        count = 0
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // steps
            y = y0 + (y1 - y0) * i // steps
            if on:
                self.set(x, y, color)
            count += 1
            if count >= (dash if on else gap):
                on = not on
                count = 0

    def circle(self, cx, cy, r, color, filled=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if filled:
                    if d2 <= r * r:
                        self.set(xx, yy, color)
                else:
                    if r * r - 2 * r <= d2 <= r * r:
                        self.set(xx, yy, color)

    def ellipse(self, cx, cy, rx, ry, color, filled=True):
        for yy in range(cy - ry, cy + ry + 1):
            for xx in range(cx - rx, cx + rx + 1):
                v = ((xx - cx) * (xx - cx)) / (rx * rx) + ((yy - cy) * (yy - cy)) / (ry * ry)
                if filled:
                    if v <= 1.0:
                        self.set(xx, yy, color)
                else:
                    if 0.85 <= v <= 1.0:
                        self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.polygon([(x0, y0), (x1, y1), (x2, y2)], color)

    def polygon(self, pts, color):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    if y1 != y0:
                        xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = int(round(xs[k]))
                xb = int(round(xs[k + 1]))
                self.fill_rect(xa, y, xb - xa + 1, 1, color)

    def rect_outline(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    # ---- text ----
    def text(self, s, x, y, scale, color, bold=False):
        cx = x
        for ch in s:
            g = glyph(ch)
            for r in range(7):
                row = g[r]
                for c in range(5):
                    if row[c] == "1":
                        self.fill_rect(cx + c * scale, y + r * scale, scale, scale, color)
                        if bold:
                            self.fill_rect(cx + c * scale + max(1, scale // 2), y + r * scale,
                                         scale, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def text_center(self, s, cx, y, scale, color, bold=False):
        w = self.text_w(s, scale)
        return self.text(s, cx - w // 2, y, scale, color, bold)

    def wrap(self, s, max_w, scale):
        words = s.split(" ")
        lines = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def paragraph(self, s, x, y, max_w, scale, color, leading=None, bold=False):
        if leading is None:
            leading = 7 * scale + (2 if scale > 1 else 1)
        yy = y
        for line in self.wrap(s, max_w, scale):
            self.text(line, x, yy, scale, color, bold)
            yy += leading
        return yy


# ---------------- PNG writer (stdlib only, deterministic) ----------------
def _chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += _chunk(b"IHDR", ihdr)
    data += _chunk(b"IDAT", comp)
    data += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


# ---------------- illustrations ----------------
def starburst(cv, cx, cy, r, color):
    for k in range(8):
        ang = k * 3.14159 / 4
        x1 = int(cx + r * 0.4 * _cos(ang))
        y1 = int(cy + r * 0.4 * _sin(ang))
        x2 = int(cx + r * _cos(ang))
        y2 = int(cy + r * _sin(ang))
        cv.line(x1, y1, x2, y2, color)
    cv.circle(cx, cy, max(2, r // 3), color)


def _cos(a):
    return _trig(a, True)


def _sin(a):
    return _trig(a, False)


def _trig(a, is_cos):
    # small-angle-free cosine/sine via Taylor around 0..2pi (a in radians)
    while a > 3.14159:
        a -= 2 * 3.14159
    while a < -3.14159:
        a += 2 * 3.14159
    x = a * a
    if is_cos:
        return 1 - x / 2 + x * x / 24 - x * x * x / 720
    return a - a * x / 6 + a * x * x / 120 - a * x * x * x / 5040


def draw_gulf(cv, x, y, w, h):
    """Simplified Gulf map: sand land, blue sea, Bahrain, tankers, Hormuz."""
    cv.fill_rect(x, y, w, h, SKY)
    # land: top band + right peninsula
    cv.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + int(w * 0.62), y + 52),
                (x + int(w * 0.55), y + 88), (x + int(w * 0.40), y + 66),
                (x + int(w * 0.30), y + 40), (x, y + 30)], (232, 220, 192))
    # Qatar peninsula jutting down
    cv.polygon([(x + int(w * 0.60), y + 50), (x + int(w * 0.66), y + 50),
                (x + int(w * 0.68), y + 78), (x + int(w * 0.62), y + 82),
                (x + int(w * 0.60), y + 62)], (232, 220, 192))
    # Oman coast bottom-right
    cv.polygon([(x + w, y + h), (x + w, y + 92), (x + int(w * 0.82), y + 100),
                (x + int(w * 0.78), y + h)], (222, 208, 172))
    # Bahrain island
    bx, by = x + int(w * 0.34), y + 62
    cv.ellipse(bx, by, 10, 7, (250, 244, 224), filled=True)
    cv.ellipse(bx, by, 10, 7, INK, filled=False)
    cv.circle(bx, by, 4, RED)
    cv.text("BAHRAIN", bx - 24, by + 12, 1, INK, bold=True)
    cv.text("IRAN", x + 14, y + 8, 1, INK_SOFT, bold=True)
    cv.text("QATAR", x + w - 52, y + 64, 1, INK_SOFT)
    cv.text("HORMUZ", x + w - 52, y + 44, 1, INK_SOFT, bold=True)
    cv.text("OMAN", x + w - 44, y + h - 16, 1, INK_SOFT, bold=True)
    # missile arrows from Iran toward Bahrain
    cv.dashed_line(x + 60, y + 18, bx - 4, by - 6, RED, dash=5, gap=3)
    cv.dashed_line(x + 150, y + 16, bx + 8, by - 4, RED, dash=5, gap=3)
    # tankers in the sea
    for tx, ty in ((x + int(w * 0.52), y + h - 34), (x + int(w * 0.74), y + h - 44)):
        cv.fill_rect(tx, ty, 34, 9, (60, 60, 60))
        cv.fill_rect(tx + 22, ty - 6, 6, 6, (60, 60, 60))
        cv.fill_rect(tx + 4, ty - 4, 8, 4, RED)
        starburst(cv, tx + 17, ty - 12, 9, (230, 120, 20))
    cv.text("2 TANKERS HIT", x + int(w * 0.52), y + h - 20, 1, RED_DARK, bold=True)
    # red banner
    cv.fill_rect(x, y, w, 16, RED)
    cv.text("2 AIR BASES  ·  2 TANKERS HIT", x + 8, y + 4, 1, WHITE, bold=True)


def draw_quake(cv, x, y, w, h):
    """Cross-section of a deep quake: sky, mountains, strata, epicentre."""
    cv.fill_rect(x, y, w, h, (233, 228, 210))
    ground = y + 34
    cv.fill_rect(x, ground, w, h - 34, (196, 164, 120))
    cv.fill_rect(x, ground + 26, w, h - ground - 26, (168, 132, 90))
    cv.fill_rect(x, ground + 56, w, h - ground - 56, (140, 106, 70))
    cv.hline(x, ground, w, INK)
    cv.hline(x, ground + 26, w, (120, 92, 58))
    cv.hline(x, ground + 56, w, (100, 76, 46))
    # mountains
    cv.triangle(x + 18, ground, x + 44, ground - 22, x + 70, ground, (120, 110, 90))
    cv.triangle(x + 62, ground, x + 92, ground - 30, x + 122, ground, (140, 128, 104))
    cv.triangle(x + 108, ground, x + 128, ground - 18, x + 148, ground, (120, 110, 90))
    # surface labels
    cv.text("LIMA", x + 10, ground - 12, 1, INK, bold=True)
    cv.text("ONDORES", x + w - 62, ground - 12, 1, INK, bold=True)
    # epicentre deep below Ondores
    ex, ey = x + w - 62, y + h - 22
    cv.dashed_line(ex, ground + 2, ex, ey - 8, RED, dash=4, gap=3)
    for r in (26, 18, 10):
        cv.circle(ex, ey, r, RED, filled=False)
    starburst(cv, ex, ey, 10, RED)
    cv.text("108 km", ex - 70, ey - 6, 1, RED_DARK, bold=True)
    cv.text("00:09 UTC", x + 8, y + 6, 1, INK, bold=True)
    cv.text("DEEP - NO DEATHS", x + 8, y + h - 14, 1, INK, bold=True)


def draw_cop31(cv, x, y, w, h):
    """Thermometer at 1.5C plus a Nov 9-21 calendar running one day over."""
    cv.fill_rect(x, y, w, h, (238, 244, 238))
    # thermometer
    tx = x + 34
    cv.fill_rect(tx - 5, y + 14, 10, h - 44, WHITE)
    cv.rect_outline(tx - 5, y + 14, 10, h - 44, INK)
    cv.circle(tx, y + h - 22, 12, RED)
    cv.circle(tx, y + h - 22, 8, (220, 60, 40))
    cv.fill_rect(tx - 3, y + 26, 6, h - 52, RED)
    cv.text("1.5 C", tx + 12, y + 22, 1, RED_DARK, bold=True)
    # calendar
    cx0 = x + 78
    cy0 = y + 12
    cv.text("NOV 9 - 20 SCHEDULED", cx0, cy0, 1, INK_SOFT, bold=True)
    cell = 15
    for i in range(13):
        cx = cx0 + (i % 7) * (cell + 2)
        cy = cy0 + 14 + (i // 7) * (cell + 2)
        day = 9 + i
        if day == 21:
            cv.fill_rect(cx, cy, cell, cell, RED)
            cv.text("21", cx + 2, cy + 4, 1, WHITE, bold=True)
        else:
            cv.fill_rect(cx, cy, cell, cell, WHITE)
            cv.rect_outline(cx, cy, cell, cell, GREY)
            cv.text(str(day), cx + 2, cy + 4, 1, INK)
    cv.text("+1 DAY", cx0 + 7 * (cell + 2) + 2, cy0 + 14, 1, RED, bold=True)
    cv.text("DAY 13 OF 12", cx0, cy0 + 14 + 2 * (cell + 2) + 4, 1, INK, bold=True)
    cv.text("NO DEAL YET", cx0, cy0 + 14 + 2 * (cell + 2) + 16, 1, RED_DARK, bold=True)


# ---- small-story icons (each ~196x44) ----
def icon_chapo(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (30, 30, 34))
    cv.text("$5M", x + 10, y + 6, 3, (255, 210, 60), bold=True)
    cv.fill_rect(x + 108, y + 8, 78, 16, RED)
    cv.text("FBI TOP TEN", x + 112, y + 11, 1, WHITE, bold=True)
    cv.text("GUASAVE", x + 10, y + h - 12, 1, (200, 200, 200))


def icon_trade(cv, x, y, w, h):
    hw = w // 2
    cv.fill_rect(x, y, hw, h, (0, 51, 153))
    for k in range(8):
        ang = k * 3.14159 / 4
        cv.set(x + hw // 2 + int(13 * _cos(ang)), y + h // 2 + int(13 * _sin(ang)), (255, 204, 0))
    cv.fill_rect(x + hw, y, hw, h // 2, (200, 30, 30))
    cv.fill_rect(x + hw, y + h // 2, hw, h - h // 2, WHITE)
    cv.fill_rect(x + hw - 24, y + 6, 48, 26, WHITE)
    cv.rect_outline(x + hw - 24, y + 6, 48, 26, INK)
    cv.line(x + hw - 18, y + 24, x + hw + 18, y + 12, BLUE)
    cv.text("90.4% DUTY-FREE", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_robot(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (226, 230, 234))
    cx = x + w // 2
    cv.fill_rect(cx - 16, y + 6, 32, 16, (90, 100, 110))
    cv.rect_outline(cx - 16, y + 6, 32, 16, INK)
    cv.circle(cx - 7, y + 14, 2, RED)
    cv.circle(cx + 7, y + 14, 2, RED)
    cv.line(cx, y + 6, cx, y + 2, INK)
    cv.circle(cx, y + 2, 2, RED)
    cv.fill_rect(cx - 20, y + 24, 40, 16, (120, 130, 140))
    cv.rect_outline(cx - 20, y + 24, 40, 16, INK)
    cv.text("128 NATIONS", x + 8, y + h - 12, 1, INK, bold=True)


def icon_ship(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, SKY)
    cv.fill_rect(x, y + 30, w, h - 30, (70, 110, 150))
    cv.polygon([(x + 60, y + 30), (x + 140, y + 30), (x + 128, y + 14), (x + 72, y + 14)],
               (50, 50, 55))
    cv.fill_rect(x + 96, y + 4, 8, 10, (50, 50, 55))
    starburst(cv, x + 78, y + 8, 7, (230, 120, 20))
    cv.circle(x + 150, y + 8, 3, INK)
    cv.circle(x + 166, y + 12, 3, INK)
    cv.text("16 SAFE", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_space(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (12, 14, 30))
    cv.circle(x + w - 34, y + h // 2, 13, (170, 165, 155))
    cv.circle(x + w - 34, y + h // 2, 13, (120, 115, 108), filled=False)
    cv.ellipse(x + w // 2, y + h // 2, 52, 14, (200, 200, 220), filled=False)
    cv.fill_rect(x + 34, y + h // 2 - 4, 26, 8, (220, 220, 230))
    cv.fill_rect(x + 24, y + h // 2 - 8, 10, 16, (90, 140, 220))
    cv.triangle(x + 60, y + h // 2 - 4, x + 72, y + h // 2, x + 60, y + h // 2 + 4, (255, 180, 60))
    cv.text("MERCURY", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_fire(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (40, 34, 30))
    cv.fill_rect(x + 30, y + 22, 130, h - 22, (70, 60, 52))
    cv.triangle(x + 52, y + 22, x + 66, y + 2, x + 80, y + 22, (255, 140, 20))
    cv.triangle(x + 84, y + 22, x + 98, y + 8, x + 112, y + 22, (255, 200, 40))
    cv.triangle(x + 116, y + 22, x + 128, y + 10, x + 140, y + 22, (255, 140, 20))
    cv.text("4 DEAD IN FIRE", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_chart(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, WHITE)
    bars = [30, 26, 28, 20, 22, 14, 16, 8]
    bw = w // len(bars)
    for i, v in enumerate(bars):
        bh = v
        cv.fill_rect(x + i * bw + 3, y + h - 10 - bh, bw - 6, bh,
                     (40, 160, 80) if i < 3 else (200, 40, 40))
    cv.line(x + 4, y + 6, x + w - 4, y + h - 12, RED)
    cv.text("-18% TAIEX, WEEK", x + 8, y + h - 12, 1, RED_DARK, bold=True)


def icon_rugby(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (34, 120, 60))
    cv.hline(x, y + h // 2, w, WHITE)
    cv.fill_rect(x + 30, y + 6, 4, h - 12, WHITE)
    cv.fill_rect(x + w - 34, y + 6, 4, h - 12, WHITE)
    cv.fill_rect(x + 30, y + 6, w - 60, 4, WHITE)
    cv.ellipse(x + w // 2, y + h // 2, 12, 8, (240, 235, 220))
    cv.text("ENG 37-12 NZL", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_football(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (34, 120, 60))
    cv.hline(x, y + h // 2, w, WHITE)
    cv.circle(x + w // 2, y + h // 2, 13, WHITE)
    cv.circle(x + w // 2, y + h // 2, 13, INK, filled=False)
    cv.polygon([(x + w // 2 - 4, y + h // 2 - 5), (x + w // 2 + 4, y + h // 2 - 5),
                (x + w // 2 + 6, y + h // 2 + 3), (x + w // 2, y + h // 2 + 7),
                (x + w // 2 - 6, y + h // 2 + 3)], INK)
    cv.text("54/54", x + 8, y + h - 12, 1, WHITE, bold=True)


def icon_f1(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (24, 24, 28))
    for r in range(3):
        for c in range(12):
            if (r + c) % 2 == 0:
                cv.fill_rect(x + 8 + c * 8, y + 4 + r * 8, 8, 8, WHITE)
    cv.fill_rect(x + 30, y + 28, 110, 8, (200, 30, 30))
    cv.fill_rect(x + 44, y + 22, 60, 6, (200, 30, 30))
    cv.circle(x + 52, y + 36, 5, INK)
    cv.circle(x + 118, y + 36, 5, INK)
    cv.text("P1 VERSTAPPEN", x + 8, y + h - 12, 1, WHITE, bold=True)


# ---------------- world map ----------------
# Coarse continent outlines in (lon, lat); projected equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73), (-75, 72),
     (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 21), (-97, 16), (-94, 17), (-87, 13), (-83, 9), (-79, 9), (-92, 15),
     (-105, 20), (-110, 23), (-114, 29), (-125, 40), (-124, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    # South America
    [(-79, 9), (-75, 11), (-72, 12), (-64, 10), (-60, 8), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35),
     (-65, -41), (-68, -50), (-70, -54), (-73, -50), (-73, -40), (-72, -30),
     (-70, -18), (-77, -12), (-80, -5), (-81, 0)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70), (15, 70),
     (10, 64), (5, 60), (5, 58), (0, 55), (-5, 50), (-9, 48), (-10, 43)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 20), (-17, 15), (-15, 11), (-12, 8),
     (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (13, 0), (12, -5), (13, -12),
     (12, -18), (15, -27), (18, -34), (20, -35), (26, -34), (32, -29), (35, -24),
     (38, -18), (40, -15), (40, -10), (42, -4), (46, -1), (51, 2), (51, 10),
     (48, 11), (44, 11), (40, 15), (38, 18), (35, 20), (33, 27), (32, 31),
     (25, 32), (19, 33), (11, 34), (10, 37)],
    # Asia
    [(30, 62), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (150, 60),
     (142, 55), (140, 45), (135, 43), (130, 38), (127, 35), (122, 32), (120, 28),
     (115, 22), (110, 20), (108, 18), (105, 10), (103, 8), (100, 8), (98, 12),
     (95, 16), (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15),
     (77, 8), (75, 12), (72, 20), (68, 23), (65, 25), (62, 25), (58, 26),
     (56, 27), (54, 26), (52, 25), (50, 29), (48, 30), (44, 29), (40, 30),
     (36, 36), (33, 36), (30, 36), (28, 38), (27, 40), (30, 42), (35, 45),
     (38, 47), (40, 50), (42, 52), (45, 55), (48, 58), (50, 60), (45, 62), (40, 62),
     (35, 62)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
     (117, -20)],
]

# (number, lon, lat, region) for heroes + small stories that fit on a map.
MAP_PINS = [
    (1, 50.5, 26.2, "MIDDLE EAST"),
    (2, -76.0, -11.0, "AMERICAS"),
    (3, 30.7, 36.9, "EUROPE"),
    (4, -108.5, 25.6, "AMERICAS"),
    (5, 4.4, 50.8, "EUROPE"),
    (6, 6.1, 46.2, "EUROPE"),
    (7, 24.0, 59.8, "EUROPE"),
    (9, 47.8, 30.5, "MIDDLE EAST"),
    (10, 121.5, 25.0, "ASIA"),
    (11, -0.1, 51.5, "EUROPE"),
    (12, 7.5, 9.0, "AFRICA"),
    (13, -115.1, 36.2, "AMERICAS"),
]


def draw_world_map(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (214, 230, 238))
    lon0, lon1 = -170.0, 190.0
    lat0, lat1 = 75.0, -55.0

    def proj(lon, lat):
        px = x + int((lon - lon0) / (lon1 - lon0) * w)
        py = y + int((lat0 - lat) / (lat0 - lat1) * h)
        return (px, py)

    for cont in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in cont]
        cv.polygon(pts, (216, 204, 160))
    # nudge table for the crowded Europe cluster
    nudge = {5: (-4, -3), 6: (5, 4), 11: (-8, -4), 7: (4, -2), 9: (6, 4), 1: (-3, 3)}
    for num, lon, lat, region in MAP_PINS:
        px, py = proj(lon, lat)
        dx, dy = nudge.get(num, (0, 0))
        px += dx
        py += dy
        col = REGION_COLORS[region]
        cv.circle(px, py, 8, col)
        cv.circle(px, py, 8, WHITE, filled=False)
        label = str(num)
        tx = px - (3 if len(label) == 1 else 6)
        cv.text(label, tx, py - 3, 1, WHITE, bold=True)


# ---------------- content (all summaries written here, in our own words) ----------------
UTC_EVENTS = [
    ("00:09", "Peru quake M6.7"),
    ("02:15", "Finland shuts Gulf airspace"),
    ("04:00", "Verstappen P1, Las Vegas"),
    ("05:00", "Tanker hit off Khasab"),
    ("05:50", "2nd tanker hit"),
    ("15:30", "EU pact signed"),
    ("17:30", "Newcastle 2-2 Arsenal"),
]

BIG_NUMBERS = [
    ("6.7", "Peru quake magnitude (USGS)"),
    ("2", "tankers hit off Khasab (UKMTO)"),
    ("128", "nations backing Geneva robot-arms talks"),
    ("90.4%", "Indonesian tariff lines duty-free"),
    ("82,500", "marchers in France (ministry)"),
    ("37-12", "England over New Zealand"),
]

REGIONS = [
    ("EUROPE", 9), ("AMERICAS", 7), ("ASIA", 7), ("MIDDLE EAST", 6),
    ("GLOBAL", 4), ("AFRICA", 1), ("OCEANIA", 1),
]

HEROES = [
    {
        "num": 1, "kicker": "1 - BAHRAIN - HORMUZ - IRAN WAR", "badge": "CONFIRMED",
        "region": "MIDDLE EAST",
        "headline": "Iran hits Bahrain; tankers struck off Oman",
        "summary": "Iran says it hit radar at two bases; a plant burned, two tankers hit off Oman.",
        "sources": "Al Jazeera - Anadolu - Reuters - UKMTO",
        "art": "gulf",
    },
    {
        "num": 2, "kicker": "2 - JUNIN, PERU - EARTHQUAKE", "badge": "CONFIRMED",
        "region": "AMERICAS",
        "headline": "A deep 6.7 quake shakes central Peru",
        "summary": "Quake 6.7 near Ondores, 108 km deep; felt in Lima. No deaths, no tsunami.",
        "sources": "USGS - IGP - AFP - Anadolu",
        "art": "quake",
    },
    {
        "num": 3, "kicker": "3 - ANTALYA, TURKIYE - CLIMATE", "badge": "CONFIRMED",
        "region": "GLOBAL",
        "headline": "Climate talks in Antalya run past deadline",
        "summary": "Day 13 of a 12-day summit; no deal on fossil fuels. Vote set for Sunday.",
        "sources": "Reuters - AFP - Anadolu",
        "art": "cop31",
    },
]

SMALL = [
    {"num": 4, "kicker": "4 - MEXICO - CRIME", "badge": "CONFIRMED",
     "headline": "Mexico seizes 'Chapo Isidro'",
     "summary": "FBI most-wanted Fausto Isidro Meza Flores was taken in Guasave; 11 died in clashes.",
     "sources": "AP - Al Jazeera", "art": "chapo"},
    {"num": 5, "kicker": "5 - EU - TRADE", "badge": "OFFICIAL",
     "headline": "EU-Indonesia trade pact",
     "summary": "Signed in Brussels; duties fall on 98.5% of EU lines and 90.4% of Indonesia's.",
     "sources": "Antara - European Commission", "art": "trade"},
    {"num": 6, "kicker": "6 - GENEVA - ARMS", "badge": "CONFIRMED",
     "headline": "Nations back AI-arms talks",
     "summary": "A two-year path to AI-weapons rules; the US, Russia and Israel oppose binding limits.",
     "sources": "AFP - Anadolu - Al Jazeera", "art": "robot"},
    {"num": 7, "kicker": "7 - FINLAND - SECURITY", "badge": "CONFIRMED",
     "headline": "Drones hit Russian ship",
     "summary": "Sixteen crew were taken off the burning cargo ship; Helsinki suspects Kyiv.",
     "sources": "Reuters - BBC", "art": "ship"},
    {"num": 8, "kicker": "8 - SPACE", "badge": "OFFICIAL",
     "headline": "BepiColombo orbits Mercury",
     "summary": "The ESA probe's 37-minute burn began at 18:24 UTC, eight years after launch.",
     "sources": "ESA", "art": "space"},
    {"num": 9, "kicker": "9 - BASRA - DISASTER", "badge": "CONFIRMED",
     "headline": "Basra plant fire kills four",
     "summary": "The 800 MW Hartha plant shut down; 35 people were hurt.",
     "sources": "INA - Anadolu - Al Jazeera", "art": "fire"},
    {"num": 10, "kicker": "10 - TAIPEI - MARKETS", "badge": "OFFICIAL",
     "headline": "Taiwan curbs short-selling",
     "summary": "The regulator acted after the worst week since 1991; the TAIEX fell 18% on the week.",
     "sources": "FSC - Taipei Times", "art": "chart"},
    {"num": 11, "kicker": "11 - LONDON - RUGBY", "badge": "OFFICIAL",
     "headline": "England beat All Blacks 37-12",
     "summary": "New Zealand's heaviest loss to England, at Twickenham.",
     "sources": "RNZ - match result", "art": "rugby"},
    {"num": 12, "kicker": "12 - ABUJA - FOOTBALL", "badge": "OFFICIAL",
     "headline": "All 54 CAF back Infantino",
     "summary": "Africa's football body backs the FIFA president; its vote is set for March 2027 in Rabat.",
     "sources": "CAF - AFP", "art": "football"},
    {"num": 13, "kicker": "13 - LAS VEGAS - F1", "badge": "OFFICIAL",
     "headline": "Verstappen on pole in Vegas",
     "summary": "Verstappen takes pole; Antonelli docked five places and Russell starts second.",
     "sources": "AP - Al Jazeera - F1 timing", "art": "f1"},
]

ALSO = [
    ("Gaza City", "drone strike on a food-aid van kills three", "AJ, Reuters"),
    ("Hormuz", "IRGC says it shot down a US MQ-9 drone; no US comment", "AJ, Reuters"),
    ("Tehran", "Iran says 168 people were killed in a US strike on a school", "Anadolu"),
    ("Paris", "82,500 march in cost-of-living protests", "ministry"),
    ("Riyadh", "coalition says three missiles aimed at the capital were shot down after 2 a.m. local", "Arab News"),
    ("Kyiv", "ballistic missiles hit the capital at 5:47; two homes ablaze", "Kyiv Post"),
    ("Ust-Luga", "Ukrainian drones hit the Russian port; Estonia scrambles NATO jets", "Kyiv Post, ERR"),
    ("Banda Sea", "M6.8 quake felt in Darwin; no tsunami", "USGS"),
    ("Mastung", "Pakistan says 15 militants killed in a Balochistan raid", "Dawn"),
    ("Bitcoin", "falls to its lowest since 2024: $55,789 at 05:56 UTC, down 9.9%", "Investing.com"),
    ("Taiwan", "21 Chinese jets hold a patrol; 15 cross the median line", "Taipei"),
    ("Brazil", "Bolsonaro moved to intensive care with a bowel obstruction", "Reuters"),
    ("Wellington", "India 486 for 4 against New Zealand; Rahul hits 136", "ICC"),
    ("Dublin", "Ireland beat world champions South Africa 20-17", ""),
    ("Newcastle", "Arsenal held 2-2; Leeds win 4-1 at Chelsea", "BBC"),
    ("Melbourne", "Australia beat England by three wickets in a T20", "AJ"),
    ("Cleveland", "Harden passes Bryant on the NBA all-time points list", "AJ, AP"),
    ("Washington", "Trump appears to confirm an FBI database breach", "AJ, NBC"),
    ("US", "Trump backs a 10% cap on credit-card rates", ""),
    ("Manipur", "toxic liquor kills at least 16", ""),
    ("Fukushima", "snow strands about 1,500 people; 700 homes lose power", "Kyodo"),
    ("Pas-de-Calais", "floods swamp 850 homes; 85 roads shut", "Anadolu"),
]

DATE_CHECK = (
    "DATE CHECK - Left out (other day): the Kyiv bridge barrage and missiles in Poland, "
    "the Kryvyi Rih strike, Denmark's expulsion of a Russian attache, the EU-UK summit "
    "and the Riemann proof claim all happened on Friday 20 November; the World Court's "
    "Rohingya ruling was Thursday 19 November. Not yet known when drawn: the COP31 final "
    "text, the Las Vegas Grand Prix result, and the Copa Sudamericana final score."
)

FOOTER = (
    "HOW WE CHECKED - CONFIRMED = 2+ major outlets - OFFICIAL = on the record "
    "(officials, results) - REPORTED = one major outlet. Every story here happened, or was "
    "first reported, on Saturday 21 November 2026 (UTC). Sources: AP, Reuters, AFP, BBC, "
    "USGS, ESA, UKMTO, Anadolu, Al Jazeera."
)

HERO_ART = {"gulf": draw_gulf, "quake": draw_quake, "cop31": draw_cop31}
SMALL_ART = {
    "chapo": icon_chapo, "trade": icon_trade, "robot": icon_robot,
    "ship": icon_ship, "space": icon_space, "fire": icon_fire,
    "chart": icon_chart, "rugby": icon_rugby, "football": icon_football,
    "f1": icon_f1,
}


def badge(cv, x, y, text, color):
    w = len(text) * 6 + 8
    cv.fill_rect(x, y, w, 12, color)
    cv.text(text, x + 4, y + 2, 1, WHITE, bold=True)
    return w


def build_entry(path):
    cv = Canvas(W, H, PAPER)
    mx = 12  # page margin

    # ---- top black bar ----
    cv.fill_rect(0, 0, W, 26, BLACK)
    cv.text("THE WORLD IN ONE DAY", 12, 6, 2, WHITE, bold=True)
    right = "35 STORIES - 7 REGIONS - EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    cv.text(right, W - 12 - cv.text_w(right, 1), 9, 1, (220, 220, 210), bold=True)

    # ---- giant masthead ----
    title = "Saturday 21 November 2026"
    cv.text(title, (W - cv.text_w(title, 6)) // 2, 30, 6, INK, bold=True)
    cv.hline(mx, 76, W - 2 * mx, INK)
    cv.hline(mx, 79, W - 2 * mx, INK)

    # ---- sub-headline ----
    sub = "Iran strikes Bahrain - Peru quake - COP31 runs past deadline"
    cv.text_center(sub, W // 2, 85, 2, INK, bold=True)

    # ---- THE DAY IN UTC strip ----
    y0 = 105
    cv.fill_rect(mx, y0, 92, 34, BLACK)
    cv.text("THE DAY", mx + 8, y0 + 5, 2, WHITE, bold=True)
    cv.text("IN UTC", mx + 8, y0 + 20, 2, WHITE, bold=True)
    col_w = (W - 2 * mx - 92) / 7
    for i, (t, label) in enumerate(UTC_EVENTS):
        cx = int(mx + 92 + i * col_w) + 6
        if i > 0:
            cv.vline(int(mx + 92 + i * col_w), y0 + 3, 28, LIGHT_GREY)
        cv.text(t, cx, y0 + 2, 2, RED, bold=True)
        cv.paragraph(label, cx, y0 + 17, int(col_w) - 10, 1, INK, leading=7)
    cv.hline(mx, y0 + 36, W - 2 * mx, INK)

    # ---- big-number strip ----
    y0 = 145
    cell_w = (W - 2 * mx) / 6
    for i, (num, label) in enumerate(BIG_NUMBERS):
        cx = int(mx + i * cell_w)
        if i > 0:
            cv.vline(cx, y0 + 2, 34, LIGHT_GREY)
        cv.text(num, cx + 8, y0 + 2, 4, RED, bold=True)
        cv.paragraph(label, cx + 8, y0 + 30, int(cell_w) - 12, 1, INK_SOFT, leading=8)
    cv.hline(mx, y0 + 46, W - 2 * mx, INK)

    # ---- region bars ----
    y0 = 193
    seg_w = (W - 2 * mx) / len(REGIONS)
    for i, (name, count) in enumerate(REGIONS):
        cx = int(mx + i * seg_w)
        cv.fill_rect(cx, y0, int(seg_w) - 2, 16, REGION_COLORS[name])
        cv.text("%s %d" % (name, count), cx + 8, y0 + 4, 1, WHITE, bold=True)
    # ---- heroes ----
    hy = 217
    hw = 328
    gap = 8
    for i, hero in enumerate(HEROES):
        hx = mx + i * (hw + gap)
        cv.rect_outline(hx, hy, hw, 280, INK)
        HERO_ART[hero["art"]](cv, hx + 1, hy + 1, hw - 2, 122)
        ky = hy + 124
        cv.fill_rect(hx + 1, ky, hw - 2, 16, REGION_COLORS[hero["region"]])
        cv.text(hero["kicker"], hx + 8, ky + 4, 1, WHITE, bold=True)
        bw = len(hero["badge"]) * 6 + 8
        cv.fill_rect(hx + hw - bw - 6, ky + 2, bw, 12, GREEN_DARK)
        cv.text(hero["badge"], hx + hw - bw - 2, ky + 4, 1, WHITE, bold=True)
        yy = ky + 20
        yy = cv.paragraph(hero["headline"], hx + 8, yy, hw - 16, 3, INK, leading=22, bold=True)
        yy += 2
        yy = cv.paragraph(hero["summary"], hx + 8, yy, hw - 16, 2, INK, leading=16)
        cv.text(hero["sources"], hx + 8, hy + 280 - 14, 1, INK_SOFT)

    # ---- small stories: 2 rows x 5 ----
    sy = 503
    sw = 196
    sgap = 5
    for row in range(2):
        for col in range(5):
            s = SMALL[row * 5 + col]
            sx = mx + col * (sw + sgap)
            syy = sy + row * 130
            cv.rect_outline(sx, syy, sw, 124, GREY)
            SMALL_ART[s["art"]](cv, sx + 1, syy + 1, sw - 2, 42)
            yy = syy + 46
            cv.text(s["kicker"], sx + 6, yy, 1, RED, bold=True)
            badge(cv, sx + sw - 62, yy - 1, s["badge"], GREEN_DARK)
            yy += 13
            yy = cv.paragraph(s["headline"], sx + 6, yy, sw - 12, 2, INK, leading=15, bold=True)
            yy = cv.paragraph(s["summary"], sx + 6, yy + 1, sw - 12, 1, INK, leading=8)
            cv.text(s["sources"], sx + 6, syy + 124 - 10, 1, INK_SOFT)

    # ---- divider ----
    cv.hline(mx, 763, W - 2 * mx, INK)

    # ---- WHERE IT HAPPENED map (left) ----
    my = 769
    cv.text("WHERE IT HAPPENED", mx, my, 2, RED_DARK, bold=True)
    draw_world_map(cv, mx, my + 18, 330, 118)
    cv.text("Pins carry each story's number; colour = region.", mx, my + 140, 1, INK_SOFT)
    cv.text("8 - in space (BepiColombo). Drawings made in code.", mx, my + 150, 1, INK_SOFT)

    # ---- ALSO list (right) ----
    ax = mx + 342
    cv.text("ALSO ON SATURDAY 21 NOVEMBER 2026 - 22 MORE", ax, my, 2, RED_DARK, bold=True)
    col_w = 324
    for idx, (place, what, src) in enumerate(ALSO):
        col = idx // 11
        row = idx % 11
        xx = ax + col * (col_w + 10)
        yy = my + 18 + row * 16
        num = 14 + idx
        line = "%d %s: %s" % (num, place, what)
        if src:
            line += " (%s)" % src
        cv.paragraph(line, xx, yy, col_w, 1, INK, leading=8)

    # ---- DATE CHECK ----
    dy = 965
    cv.rect_outline(mx, dy, W - 2 * mx, 36, RED, t=2)
    cv.fill_rect(mx, dy, 92, 36, RED)
    cv.text("DATE", mx + 8, dy + 8, 2, WHITE, bold=True)
    cv.text("CHECK", mx + 8, dy + 24, 2, WHITE, bold=True)
    cv.paragraph(DATE_CHECK, mx + 100, dy + 5, W - 2 * mx - 108, 1, INK, leading=9)

    # ---- footer ----
    cv.paragraph(FOOTER, mx, 1003, W - 2 * mx, 1, INK_SOFT, leading=9)

    write_png(path, cv)
    return path
