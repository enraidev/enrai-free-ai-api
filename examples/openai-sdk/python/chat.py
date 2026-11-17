#!/usr/bin/env python3
"""Chat completion dengan SDK resmi `openai` untuk API AI gratis Enrai.

Pemakaian:
    export ENRAI_API_KEY="YOUR_API_KEY"
    python chat.py "Halo, apa kabar?"
    python chat.py --stream "Hitung 1 sampai 10."

Variabel lingkungan:
    ENRAI_API_KEY  wajib, API key dari https://enrai.web.id/register
    ENRAI_MODEL    opsional, default Chatgpt (Deepseek, GLM)

Dokumentasi: https://enrai.web.id/docs
"""

from __future__ import annotations

import os
import sys

from openai import OpenAI

BASE_URL = "https://enrai.web.id/v1"
DEFAULT_MODEL = "Chatgpt"
DEFAULT_PROMPT = "Halo! Apa itu API yang kompatibel OpenAI?"

ERROR_HINTS = {
    401: "API key tidak valid atau hilang. Periksa ENRAI_API_KEY.",
    429: "Rate limit tercapai (20 request/menit, burst 5). Tunggu lalu ulangi.",
    500: "Galat server. Ulangi setelah jeda; laporkan bila terus berulang.",
    502: "Seluruh provider di balik combo sedang gagal. Ulangi beberapa saat lagi.",
}


def explain(exc: Exception) -> str:
    status = getattr(exc, "status_code", None)
    if isinstance(status, int) and status in ERROR_HINTS:
        return f"[{status}] {ERROR_HINTS[status]}"
    if isinstance(status, int):
        return f"[{status}] Permintaan gagal: {exc}"
    return f"Permintaan gagal: {exc}"


def main() -> int:
    api_key = os.environ.get("ENRAI_API_KEY")
    if not api_key:
        print(
            "ENRAI_API_KEY belum di-set. Jalankan: export ENRAI_API_KEY='YOUR_API_KEY'\n"
            "Belum punya key? Daftar gratis di https://enrai.web.id/register",
            file=sys.stderr,
        )
        return 2

    args = sys.argv[1:]
    use_stream = "--stream" in args
    prompt = " ".join(a for a in args if a != "--stream") or DEFAULT_PROMPT
    model = os.environ.get("ENRAI_MODEL", DEFAULT_MODEL)

    client = OpenAI(base_url=BASE_URL, api_key=api_key)

    if use_stream:
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            got_text = False
            for chunk in stream:
                if not chunk.choices:
                    continue
                piece = getattr(chunk.choices[0].delta, "content", None)
                if piece:
                    got_text = True
                    print(piece, end="", flush=True)
        except Exception as exc:  # noqa: BLE001 - contoh: tampilkan apa adanya
            print(f"\n{explain(exc)}", file=sys.stderr)
            return 1

        print()
        if not got_text:
            print("Stream selesai tanpa teks \u2014 perlakukan sebagai kegagalan.", file=sys.stderr)
            return 1
        return 0

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # noqa: BLE001 - contoh: tampilkan apa adanya
        print(explain(exc), file=sys.stderr)
        return 1

    content = (response.choices[0].message.content or "").strip()
    if not content:
        # 200 dengan isi kosong tetap dianggap gagal.
        print("Jawaban kosong dari upstream \u2014 perlakukan sebagai kegagalan.", file=sys.stderr)
        return 1

    print(content)

    usage = getattr(response, "usage", None)
    if usage is not None:
        print(
            f"\n[model={model} prompt_tokens={usage.prompt_tokens} "
            f"completion_tokens={usage.completion_tokens}]",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
