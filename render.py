#!/usr/bin/env python3
"""Render the 21 November 2026 world-news front page (1024x1024 PNG).

Drawn entirely with Pillow primitives: no photos, no downloaded assets.
Layout: navy masthead with the date, a night-sky Kyiv illustration,
a lead headline, two secondary stories, a summit/Riyadh row, a briefs
band and a sources footer. Run: python3 render.py [out.png]
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (16, 35, 63)
NAVY2 = (24, 52, 88)
RED = (178, 32, 44)
GOLD = (201, 162, 39)
GREY = (90, 88, 82)
LIGHT = (233, 228, 216)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines; returns y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.22)


def burst(draw, cx, cy, r_out, r_in, spikes, fill):
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def skyline(draw, x0, x1, base, colour, rng, min_h=40, max_h=150):
    """Black city silhouette with a few lit windows."""
    x = x0
    while x < x1:
        bw = rng.randint(34, 70)
        bh = rng.randint(min_h, max_h)
        draw.rectangle([x, base - bh, min(x + bw, x1), base], fill=colour)
        for wy in range(base - bh + 8, base - 8, 16):
            for wx in range(x + 6, min(x + bw, x1) - 6, 14):
                if rng.random() < 0.22:
                    draw.rectangle([wx, wy, wx + 5, wy + 7],
                                   fill=(255, 214, 130))
        x += bw + rng.randint(2, 10)


def main(out_path):
    rng = random.Random(20261121)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.rectangle([0, 124, W, 130], fill=GOLD)
    centered(d, W // 2, 12, "THE WORLD IN ONE PAGE",
             font(SERIF, 58), (255, 255, 255))
    centered(d, W // 2, 76, "SATURDAY  \u00b7  21 NOVEMBER 2026",
             font(SANS_B, 30), (255, 214, 130))

    # ---- lead illustration: Kyiv at night under attack -----------------
    ax0, ax1, ay0, ay1 = 36, 988, 140, 336
    for i in range(ay1 - ay0):
        t = i / (ay1 - ay0)
        d.line([(ax0, ay0 + i), (ax1, ay0 + i)],
               fill=(int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t),
                     int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t),
                     int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)))
    for _ in range(70):
        sx = rng.randint(ax0 + 4, ax1 - 4)
        sy = rng.randint(ay0 + 4, ay1 - 120)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(255, 255, 255, rng.randint(90, 220)))
    # missile arcs: bright trails streaking down toward the city
    for (sx, sy, ex, ey) in [(120, 165, 300, 300), (420, 158, 560, 310),
                             (700, 170, 830, 295), (880, 160, 950, 285)]:
        mx, my = (sx + ex) / 2, min(sy, ey) - 55
        pts = []
        for t in [k / 40 for k in range(41)]:
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey
            pts.append((px, py))
        d.line(pts, fill=(255, 236, 170), width=3)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 190))
    # explosion bursts above the skyline, drawn after it so they show
    skyline(d, ax0, ax1, ay1, (8, 12, 22), rng)
    burst(d, 300, 300, 36, 14, 12, (255, 140, 40))
    burst(d, 300, 300, 22, 9, 12, (255, 214, 90))
    burst(d, 830, 295, 38, 13, 12, (255, 140, 40))
    burst(d, 830, 295, 22, 8, 12, (255, 214, 90))
    # caption inside the art
    d.rectangle([ax0, ay1 - 34, ax1, ay1], fill=(0, 0, 0, 150))
    d.text((ax0 + 12, ay1 - 30),
           "KYIV, OVERNIGHT \u2014 air defences fire as missiles streak in; "
           "NATO jets scrambled",
           font=font(SANS_B, 17), fill=(255, 255, 255))

    # ---- lead headline -------------------------------------------------
    y = 360
    d.text((36, y), "LEAD  \u00b7  UKRAINE WAR", font=font(SANS_B, 20), fill=RED)
    y += 30
    head = wrap(d, "RUSSIA\u2019S BIGGEST STRIKES OF THE YEAR HIT KYIV",
                font(SERIF, 40), 952)
    y = text_block(d, 36, y, head, font(SERIF, 40), INK, leading=50)
    y += 6
    deck = wrap(d, "More than 400 drones and 110 missiles overnight; at least "
                "eight killed in Kyiv. A missile also fell in Poland \u2014 no "
                "injuries.",
                font(SANS, 21), 952)
    y = text_block(d, 36, y, deck, font(SANS, 21), (40, 40, 40), leading=27)

    d.line([(36, y + 8), (988, y + 8)], fill=INK, width=2)
    y += 12

    # ---- two secondary stories ----------------------------------------
    col_w = 464
    # left: markets, with a falling chart
    x = 36
    d.text((x, y), "MARKETS", font=font(SANS_B, 19), fill=RED)
    y2 = y + 28
    mh = wrap(d, "AI SELL-OFF SENDS STOCKS INTO CORRECTION",
              font(SERIF, 27), col_w)
    y2 = text_block(d, x, y2, mh, font(SERIF, 27), INK, leading=32)
    # mini chart: label above the box, falling line inside
    d.text((x, y2 + 2), "S&P 500  \u22123.7%  \u00b7  NASDAQ  \u22125.3%",
           font=font(SANS_B, 17), fill=RED)
    cx0, cy0, cx1, cy1 = x, y2 + 26, x + col_w, y2 + 70
    d.rectangle([cx0, cy0, cx1, cy1], outline=GREY, width=1)
    pts = [(cx0 + 8, cy0 + 8), (cx0 + 110, cy0 + 14), (cx0 + 200, cy0 + 12),
           (cx0 + 300, cy0 + 26), (cx0 + 400, cy0 + 24), (cx1 - 8, cy1 - 6)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(cx1 - 8, cy1 - 6), (cx1 - 26, cy1 - 12), (cx1 - 20, cy1 + 2)],
              fill=RED)
    y2 = cy1 + 8
    mb = wrap(d, "Wall Street\u2019s Friday rout erases the year\u2019s gains; "
              "the SEC is probing Nvidia\u2019s accounting.",
              font(SANS, 20), col_w)
    y2 = text_block(d, x, y2, mb, font(SANS, 20), (40, 40, 40), leading=24)

    # right: ICJ, with scales of justice
    x = 524
    d.text((x, y), "JUSTICE  \u00b7  THE HAGUE", font=font(SANS_B, 19), fill=RED)
    y3 = y + 28
    jh = wrap(d, "MYANMAR GUILTY OF GENOCIDE, WORLD COURT RULES",
              font(SERIF, 27), col_w)
    y3 = text_block(d, x, y3, jh, font(SERIF, 27), INK, leading=32)
    # scales icon
    ix, iy = x + 8, y3 + 10
    d.line([(ix + 40, iy), (ix + 40, iy + 52)], fill=INK, width=4)
    d.line([(ix + 4, iy + 10), (ix + 76, iy + 10)], fill=INK, width=4)
    d.arc([ix - 2, iy + 10, ix + 22, iy + 34], 0, 180, fill=INK, width=3)
    d.arc([ix + 58, iy + 10, ix + 82, iy + 34], 0, 180, fill=INK, width=3)
    d.line([(ix + 18, iy + 56), (ix + 62, iy + 56)], fill=INK, width=4)
    d.text((ix + 100, iy + 14), "9\u20136",
           font=font(SERIF, 34), fill=RED)
    y3 = y3 + 56
    jb = wrap(d, "Judges rule over the Rohingya \u2014 the first time the "
              "court has ever held a state responsible.",
              font(SANS, 20), col_w)
    y3 = text_block(d, x, y3, jb, font(SANS, 20), (40, 40, 40), leading=24)

    y = max(y2, y3) + 10
    d.line([(36, y), (988, y)], fill=GREY, width=1)
    y += 12

    # ---- summit / Riyadh row ------------------------------------------
    d.text((36, y), "SUMMIT \u2014 SHENZHEN",
           font=font(SANS_B, 19), fill=RED)
    y4 = y + 28
    s1 = wrap(d, "Trump defends his ties to Putin and Xi; Zelenskyy calls "
              "Putin \u201ca killer\u201d.",
              font(SANS, 20), col_w)
    y4 = text_block(d, 36, y4, s1, font(SANS, 20), (40, 40, 40), leading=24)
    d.text((524, y), "RIYADH", font=font(SANS_B, 19), fill=RED)
    y5 = y + 28
    s2 = wrap(d, "Saudi intercepts three Houthi missiles aimed at Riyadh, "
              "the third night running.",
              font(SANS, 20), col_w)
    y5 = text_block(d, 524, y5, s2, font(SANS, 20), (40, 40, 40), leading=24)
    y = max(y4, y5) + 8

    # ---- briefs band ----------------------------------------------------
    d.rectangle([0, y, W, y + 88], fill=NAVY)
    by = y + 6
    d.text((36, by), "ALSO TODAY", font=font(SANS_B, 19), fill=(255, 214, 130))
    by += 22
    briefs_l = [
        "UK\u2013EU seal post-Brexit deals; youth mobility for 100,000",
        "COP31 talks stall in Antalya; draft drops fossil fuels",
        "Gen Z protests sweep 25 European countries",
    ]
    briefs_r = [
        "Pancreatic-cancer pill: tumours undetectable in 1 in 12",
        "Van Gogh sells for a record $190m at auction",
        "Voyager 1: first object one light-day from Earth",
    ]
    for items, bx in ((briefs_l, 36), (briefs_r, 524)):
        yy = by
        for b in items:
            d.text((bx, yy), "\u2022  " + b, font=font(SANS, 14),
                   fill=(255, 255, 255))
            yy += 19
    y = y + 88

    # ---- footer ---------------------------------------------------------
    centered(d, W // 2, y + 8,
             "Sources: BBC \u00b7 Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 FT \u00b7 The Guardian",
             font(SANS, 15), GREY)
    img.save(out_path, "PNG", optimize=True)
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
