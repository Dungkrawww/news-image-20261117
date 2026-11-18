#!/usr/bin/env python3
"""Draw entry.png for news-image-20261117: a one-page newspaper front
summing up the world news of Tuesday 17 November 2026.

Layout: 1024x1024, dark navy masthead with the date, six story rows
(headline + one deck line each, tagged by region), thin footer.
Run: python3 tools/make_image.py  ->  writes entry.png next to main.ts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 247, 240)      # warm off-white
NAVY = (20, 33, 61)          # masthead
NAVY_LIGHT = (31, 48, 84)
INK = (24, 24, 24)
GREY = (90, 88, 82)
ROW_ALT = (241, 237, 228)
GOLD = (201, 162, 39)
RULE = (210, 204, 190)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
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


STORIES = [
    ("EUROPE · WAR", (176, 58, 46),
     "Ukraine hits Crimea bridge — again",
     "Kerch crossing badly damaged, Kyiv says; Russia struck Kyiv's bridges."),
    ("MIDDLE EAST", (178, 122, 26),
     "Tankers struck by mines near Hormuz",
     "Iran says tankers struck mines near the strait and caught fire."),
    ("DIPLOMACY", (26, 110, 138),
     "Xi, Trump and Putin to meet Thursday",
     "China confirms the first three-way summit, in Shenzhen on Thursday."),
    ("MIDDLE EAST", (178, 122, 26),
     "Third US carrier reaches Middle East",
     "USS Theodore Roosevelt joins two other carriers in the region."),
    ("UNITED STATES", (90, 90, 90),
     "Pentagon fails its audit, ninth year",
     "Auditors refuse to sign off books holding $4.8 trillion in assets."),
    ("ASIA-PACIFIC", (26, 110, 138),
     "Japan scrambles jets at Russian planes",
     "Tokyo says Russian aircraft entered its airspace; jets scrambled."),
]


def draw_globe(draw, cx, cy, r):
    """Simple line globe for the masthead."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(201, 162, 39), width=3)
    draw.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r],
                 outline=(201, 162, 39), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(201, 162, 39), width=2)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
             start=0, end=360, fill=(201, 162, 39), width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=GOLD)
    draw_globe(d, 945, 58, 36)
    kicker = font(BOLD, 25)
    d.text((36, 26), "MAKE.FUN  ·  ONE DAY, ONE IMAGE", font=kicker,
           fill=(201, 162, 39))
    date_f = font(BOLD, 56)
    d.text((34, 56), "TUESDAY 17 NOVEMBER 2026", font=date_f, fill=(255, 255, 255))
    sub_f = font(REG, 27)
    d.text((36, 128), "The world in one day — six stories that defined it",
           font=sub_f, fill=(205, 210, 222))

    # ---- Story rows ----
    top = 172
    row_h = 134
    tag_f = font(BOLD, 21)
    head_f = font(BOLD, 35)
    deck_f = font(REG, 24)
    for i, (tag, color, head, deck) in enumerate(STORIES):
        y0 = top + i * row_h
        if i % 2 == 1:
            d.rectangle([0, y0, W, y0 + row_h], fill=ROW_ALT)
        # number disc
        cx, cy = 66, y0 + row_h // 2
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=color)
        num_f = font(BOLD, 30)
        num = str(i + 1)
        d.text((cx - d.textlength(num, font=num_f) / 2, cy - 21),
               num, font=num_f, fill=(255, 255, 255))
        # tag
        d.text((112, y0 + 14), tag, font=tag_f, fill=color)
        # headline
        d.text((112, y0 + 42), head, font=head_f, fill=INK)
        # deck, one line (legible when the image is shown small)
        lines = wrap(d, deck, deck_f, W - 112 - 36)
        assert len(lines) == 1, f"deck too long: {deck!r} -> {lines}"
        d.text((112, y0 + 86), lines[0], font=deck_f, fill=GREY)
        if i < len(STORIES) - 1:
            d.line([36, y0 + row_h - 1, W - 36, y0 + row_h - 1], fill=RULE, width=1)

    # ---- Footer ----
    fy = top + 6 * row_h  # 976
    d.rectangle([0, fy, W, H], fill=NAVY_LIGHT)
    foot_f = font(REG, 22)
    d.text((36, fy + 13),
           "As reported on 17 November 2026  ·  Ukraine · Middle East · Asia-Pacific · United States",
           font=foot_f, fill=(205, 210, 222))

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {W}x{H} {size} bytes")
    assert size <= 1048576, "over 1 MiB!"


if __name__ == "__main__":
    main()
