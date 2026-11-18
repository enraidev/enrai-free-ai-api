#!/usr/bin/env python3
"""Chat completion with the official `openai` SDK against the free Enrai AI API.

Usage:
    export ENRAI_API_KEY="YOUR_API_KEY"
    python chat.py "Hello, how are you?"
    python chat.py --stream "Count from 1 to 10."

Environment variables:
    ENRAI_API_KEY  required, API key from https://enrai.web.id/register
    ENRAI_MODEL    optional, defaults to Chatgpt (Deepseek, GLM)

Documentation: https://enrai.web.id/docs
"""

from __future__ import annotations

import os
import sys

from openai import OpenAI

BASE_URL = "https://enrai.web.id/v1"
DEFAULT_MODEL = "Chatgpt"
DEFAULT_PROMPT = "Hello! What is an OpenAI-compatible API?"

ERROR_HINTS = {
    401: "Invalid or missing API key. Check ENRAI_API_KEY.",
    429: "Rate limit reached (20 requests/minute, burst 5). Wait and retry.",
    500: "Server error. Retry after a pause; report it if it keeps happening.",
    502: "Every provider behind the combo is failing. Retry in a moment.",
}


def explain(exc: Exception) -> str:
    status = getattr(exc, "status_code", None)
    if isinstance(status, int) and status in ERROR_HINTS:
        return f"[{status}] {ERROR_HINTS[status]}"
    if isinstance(status, int):
        return f"[{status}] Request failed: {exc}"
    return f"Request failed: {exc}"


def main() -> int:
    api_key = os.environ.get("ENRAI_API_KEY")
    if not api_key:
        print(
            "ENRAI_API_KEY is not set. Run: export ENRAI_API_KEY='YOUR_API_KEY'\n"
            "No key yet? Sign up free at https://enrai.web.id/register",
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
        except Exception as exc:  # noqa: BLE001 - example: show it as-is
            print(f"\n{explain(exc)}", file=sys.stderr)
            return 1

        print()
        if not got_text:
            print("Stream finished without text \u2014 treat it as a failure.", file=sys.stderr)
            return 1
        return 0

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # noqa: BLE001 - example: show it as-is
        print(explain(exc), file=sys.stderr)
        return 1

    content = (response.choices[0].message.content or "").strip()
    if not content:
        # A 200 with an empty body is still a failure.
        print("Empty answer from upstream \u2014 treat it as a failure.", file=sys.stderr)
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
