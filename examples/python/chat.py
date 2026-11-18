#!/usr/bin/env python3
"""Simple chat completion with the free Enrai AI API (OpenAI-compatible).

Usage:
    export ENRAI_API_KEY="YOUR_API_KEY"
    python chat.py "Hello, how are you?"

Documentation: https://enrai.web.id/docs
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
        print("ENRAI_API_KEY is not set. Run: export ENRAI_API_KEY='YOUR_API_KEY'", file=sys.stderr)
        print("No key yet? Sign up free at https://enrai.web.id/register", file=sys.stderr)
        return 2

    prompt = " ".join(sys.argv[1:]) or "Hello! What is an OpenAI-compatible API?"

    client = OpenAI(base_url=BASE_URL, api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # noqa: BLE001 - example: show the message as-is
        status = getattr(exc, "status_code", None)
        if status == 401:
            print("401: invalid API key. Check ENRAI_API_KEY.", file=sys.stderr)
        elif status == 429:
            print("429: rate limit reached (20 requests/minute). Wait and retry.", file=sys.stderr)
        elif status == 502:
            print("502: upstream provider failed. Retry after a short pause.", file=sys.stderr)
        else:
            print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    content = (response.choices[0].message.content or "").strip()
    if not content:
        # A 200 with an empty body is still a failure.
        print("Empty answer from upstream - treat it as a failure.", file=sys.stderr)
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
