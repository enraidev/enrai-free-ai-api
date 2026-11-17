#!/usr/bin/env python3
"""Chat completion sederhana dengan API AI gratis Enrai (kompatibel OpenAI).

Pemakaian:
    export ENRAI_API_KEY="YOUR_API_KEY"
    python chat.py "Halo, apa kabar?"

Dokumentasi: https://enrai.web.id/docs
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
        print("Belum punya key? Daftar gratis di https://enrai.web.id/register", file=sys.stderr)
        return 2

    prompt = " ".join(sys.argv[1:]) or "Halo! Apa itu API yang kompatibel OpenAI?"

    client = OpenAI(base_url=BASE_URL, api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # noqa: BLE001 - contoh: tampilkan pesan apa adanya
        status = getattr(exc, "status_code", None)
        if status == 401:
            print("401: API key tidak valid. Periksa ENRAI_API_KEY.", file=sys.stderr)
        elif status == 429:
            print("429: rate limit tercapai (20 request/menit). Tunggu lalu ulangi.", file=sys.stderr)
        elif status == 502:
            print("502: provider upstream gagal. Ulangi setelah beberapa saat.", file=sys.stderr)
        else:
            print(f"Permintaan gagal: {exc}", file=sys.stderr)
        return 1

    content = (response.choices[0].message.content or "").strip()
    if not content:
        # Balasan 200 dengan isi kosong tetap dianggap gagal.
        print("Jawaban kosong dari upstream — perlakukan sebagai kegagalan.", file=sys.stderr)
        return 1

    print(content)

    usage = getattr(response, "usage", None)
    if usage is not None:
        print(
            f"\n[model={MODEL} prompt_tokens={usage.prompt_tokens} "
            f"completion_tokens={usage.completion_tokens}]",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
