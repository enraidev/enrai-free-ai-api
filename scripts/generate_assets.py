#!/usr/bin/env python3
"""Membuat aset raster repo (social preview 1280x640) tanpa dependensi internet.

Jalankan dari root repo:
    python scripts/generate_assets.py

Output: assets/social-preview.png
Tidak ada data produk yang dikarang di sini: teks diambil dari fakta yang
dipublikasikan di https://enrai.web.id (base URL, nama model, status beta).
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

    # panel halus di kanan (dekorasi, bukan informasi)
    draw.rounded_rectangle([790, 96, 1200, 300], radius=20, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([790, 336, 986, 432], radius=16, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([1004, 336, 1200, 432], radius=16, fill=PANEL, outline=STROKE, width=2)
    draw.rounded_rectangle([790, 468, 1200, 540], radius=16, fill=PANEL, outline=STROKE, width=2)

    # bar aksen atas
    gradient_bar(draw, 0, 8, W)

    # mark
    draw.ellipse([80, 104, 152, 176], outline=ACCENT, width=5)
    draw.ellipse([102, 126, 130, 154], fill=ACCENT)

    draw.text((184, 92), "Enrai", font=font("bold", 88), fill=FG)
    draw.text((186, 196), "API AI gratis · kompatibel OpenAI", font=font("regular", 32), fill=(165, 180, 252))
    draw.text((186, 244), "Satu API key · streaming SSE · public beta", font=font("regular", 24), fill=MUTED)

    # domain
    draw.text((822, 128), "Base URL", font=font("regular", 20), fill=MUTED)
    draw.text((822, 160), "https://enrai.web.id/v1", font=font("mono", 24), fill=(214, 214, 231))

    draw.text((822, 200), "Model", font=font("regular", 20), fill=MUTED)
    draw.text((822, 232), "Chatgpt · Deepseek · GLM", font=font("regular", 22), fill=FG)

    draw.text((816, 362), "Batas laju", font=font("regular", 19), fill=MUTED)
    draw.text((816, 392), "20/menit chat", font=font("regular", 22), fill=FG)
    draw.text((1030, 362), "Harga", font=font("regular", 19), fill=MUTED)
    draw.text((1030, 392), "Gratis $0", font=font("regular", 22), fill=(134, 239, 172))

    draw.text((816, 490), "Status", font=font("regular", 19), fill=MUTED)
    draw.text((816, 514), "Public beta · tanpa kartu kredit", font=font("regular", 21), fill=FG)

    draw.text((80, 500), "enrai.web.id", font=font("bold", 62), fill=FG)
    draw.text((82, 580), "Dokumentasi, contoh kode, dan daftar model", font=font("regular", 26), fill=MUTED)

    # chip fitur terverifikasi di bawah tagline
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
