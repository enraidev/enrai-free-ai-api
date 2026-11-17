#!/usr/bin/env python3
"""Streaming (Server-Sent Events) dengan API AI gratis Enrai.

Pemakaian:
    export ENRAI_API_KEY="YOUR_API_KEY"
    python stream.py "Tulis pantun tentang kopi."

Dokumentasi streaming: https://enrai.web.id/docs
"""

from __future__ import annotations

import os
import sys

from openai import OpenAI

BASE_URL = "https://enrai.web.id/v1"
MODEL = os.environ.get("ENRAI_MODEL", "Chatgpt")


def main() -> int:
    api_key = os.environ.get("ENRAI_API_KEY")
    if not api_key:
        print("ENRAI_API_KEY belum di-set. Jalankan: export ENRAI_API_KEY='YOUR_API_KEY'", file=sys.stderr)
        return 2

    prompt = " ".join(sys.argv[1:]) or "Tulis paragraf singkat tentang API."

    client = OpenAI(base_url=BASE_URL, api_key=api_key)

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        got_text = False
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            piece = getattr(delta, "content", None)
            if piece:
                got_text = True
                print(piece, end="", flush=True)
    except Exception as exc:  # noqa: BLE001 - contoh
        status = getattr(exc, "status_code", None)
        hints = {
            401: "API key tidak valid.",
            429: "rate limit tercapai (20 request/menit).",
            502: "provider upstream gagal, ulangi nanti.",
        }
        hint = hints.get(status, "permintaan gagal.") if isinstance(status, int) else "permintaan gagal."
        print(f"\n[{status or 'error'}] {hint} ({exc})", file=sys.stderr)
        return 1

    print()
    if not got_text:
        print("Stream selesai tanpa teks — perlakukan sebagai kegagalan.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
