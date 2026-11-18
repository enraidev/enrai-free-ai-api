#!/usr/bin/env python3
"""Generate the repository raster assets (1280x640 social preview) with no internet dependency.

Run from the repo root:
    python scripts/generate_assets.py

Output: assets/social-preview.png
No invented product data: every string comes from facts published at
https://enrai.web.id (base URL, model names, beta status).
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG = (10, 10, 13)
PANEL = (18, 18, 26)
STROKE = (43, 43, 69)
FG = (244, 244, 247)
MUTED = (161, 161, 179)
ACCENT = (99, 102, 241)
ACCENT_2 = (34, 211, 238)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "social-preview.png"

FONT_CANDIDATES = {
    "bold": [r"C:\Windows\Fonts\segoeuib.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": [r"C:\Windows\Fonts\segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "mono": [r"C:\Windows\Fonts\consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"],
}


def font(kind: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES[kind]:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def gradient_bar(draw: ImageDraw.ImageDraw, top: int, height: int, width: int) -> None:
    for x in range(width):
        t = x / max(width - 1, 1)
        color = tuple(int(ACCENT[i] + (ACCENT_2[i] - ACCENT[i]) * t) for i in range(3))
        draw.line([(x, top), (x, top + height)], fill=color)


def main() -> int:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # soft panels on the right (decoration only, no information)
    draw.rounded_rectangle([790, 96, 1200, 300], radius=20, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([790, 336, 986, 432], radius=16, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([1004, 336, 1200, 432], radius=16, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([790, 468, 1200, 540], radius=16, fill=PANEL, outline=STROKE, width=2)

    # top accent bar
    gradient_bar(draw, 0, 8, W)

    # mark
    draw.ellipse([80, 104, 152, 176], outline=ACCENT, width=5)
    draw.ellipse([102, 126, 130, 154], fill=ACCENT)

    draw.text((184, 92), "Enrai", font=font("bold", 88), fill=FG)
    draw.text((186, 196), "Free AI API · OpenAI-compatible", font=font("regular", 32), fill=(165, 180, 252))
    draw.text((186, 244), "One API key · SSE streaming · public beta", font=font("regular", 24), fill=MUTED)

    # domain
    draw.text((822, 128), "Base URL", font=font("regular", 20), fill=MUTED)
    draw.text((822, 160), "https://enrai.web.id/v1", font=font("mono", 24), fill=(214, 214, 231))

    draw.text((822, 200), "Model", font=font("regular", 20), fill=MUTED)
    draw.text((822, 232), "Chatgpt · Deepseek · GLM", font=font("regular", 22), fill=FG)

    draw.text((816, 362), "Rate limit", font=font("regular", 19), fill=MUTED)
    draw.text((816, 392), "20/min chat", font=font("regular", 22), fill=FG)
    draw.text((1030, 362), "Price", font=font("regular", 19), fill=MUTED)
    draw.text((1030, 392), "Free $0", font=font("regular", 22), fill=(134, 239, 172))

    draw.text((816, 490), "Status", font=font("regular", 19), fill=MUTED)
    draw.text((816, 514), "Public beta · no credit card", font=font("regular", 21), fill=FG)

    draw.text((80, 500), "enrai.web.id", font=font("bold", 62), fill=FG)
    draw.text((82, 580), "Docs, code examples, and the model list", font=font("regular", 26), fill=MUTED)

    # verified feature chips below the tagline
    chips = [("chat completions", 80, 264), ("streaming SSE", 356, 172), ("failover combo", 540, 200)]
    for label, x, width in chips:
        draw.rounded_rectangle([x, 304, x + width, 352], radius=10, fill=PANEL, outline=STROKE, width=2)
        draw.text((x + 16, 316), label, font=font("regular", 20), fill=(165, 180, 252))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
