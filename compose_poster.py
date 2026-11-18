#!/usr/bin/env python3
"""Compose the final news poster: masthead + caption chips over the artwork.

The artwork (artwork.webp) is a five-vignette editorial collage with no text.
This script burns in the masthead and one caption per vignette so the single
image reads as a complete summary of the day's world news:

  * Shenzhen: Trump, Xi and Putin gather for the APEC summit and the first
    US-China-Russia trilateral meeting.
  * Ukraine strikes the Kerch (Crimean) Bridge again; a span collapses.
  * The US strikes Iran's Qeshm Island; a tanker burns near Hormuz.
  * Washington tightens global AI chip export controls; stocks slide.
  * The United States loses its measles elimination status.

Run at build time only:  python3 compose_poster.py
Output: poster.png (the image main.py ships to the grader's output dir).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ARTWORK = HERE / "artwork.webp"
OUTPUT = HERE / "poster.png"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

INK = (245, 239, 226)       # warm off-white for the masthead
GOLD = (217, 164, 65)       # date line
CHIP_BG = (8, 10, 16, 178)  # translucent near-black caption chip
CHIP_FG = (250, 248, 242)

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "TUESDAY · 17 NOVEMBER 2026"

# (caption, x, y) — bottom-left inside each vignette of the 1920x1280 art.
CAPTIONS = [
    ("SHENZHEN SUMMIT — TRUMP, XI & PUTIN MEET", 48, 402),
    ("KERCH BRIDGE STRUCK — SPAN COLLAPSES", 48, 776),
    ("HORMUZ TANKER ABLAZE — U.S. STRIKES IRAN", 986, 776),
    ("AI CHIP CURBS TIGHTEN — STOCKS SLIDE", 48, 1168),
    ("U.S. LOSES MEASLES-FREE STATUS", 986, 1168),
]


def centered(draw: ImageDraw.ImageDraw, text: str, font, y: int, fill) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    draw.text(((1920 - width) // 2, y), text, font=font, fill=fill)


def main() -> None:
    img = Image.open(ARTWORK).convert("RGB")
    if img.size != (1920, 1280):
        img = img.resize((1920, 1280), Image.LANCZOS)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    chip_font = ImageFont.truetype(SANS_BOLD, 30)
    for text, x, y in CAPTIONS:
        box = od.textbbox((0, 0), text, font=chip_font)
        tw, th = box[2] - box[0], box[3] - box[1]
        od.rounded_rectangle(
            [x - 14, y - 10, x + tw + 14, y + th + 12],
            radius=12,
            fill=CHIP_BG,
        )

    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    centered(draw, MASTHEAD, ImageFont.truetype(SERIF_BOLD, 86), 12, INK)
    centered(draw, DATELINE, ImageFont.truetype(SANS_BOLD, 30), 108, GOLD)

    for text, x, y in CAPTIONS:
        draw.text((x, y), text, font=chip_font, fill=CHIP_FG)

    img.convert("RGB").save(OUTPUT, format="PNG", optimize=True)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
