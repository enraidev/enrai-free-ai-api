#!/usr/bin/env bash
# Chat completion via curl ke API AI gratis Enrai.
# Pemakaian:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./chat.sh "Halo dari cURL!"
# Dokumentasi: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set dulu: export ENRAI_API_KEY='YOUR_API_KEY' (daftar gratis di https://enrai.web.id/register)}"

MODEL="${ENRAI_MODEL:-Chatgpt}"
prompt="${*:-Halo! Apa itu API yang kompatibel OpenAI?}"

# Escape untuk JSON: backslash lalu tanda kutip ganda.
escaped="$(printf '%s' "$prompt" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')"

response="$(curl -sS -w '\n%{http_code}' https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer ${ENRAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"${escaped}\"}]}")"

status="${response##*$'\n'}"
body="${response%$'\n'*}"

if [ "$status" != "200" ]; then
  echo "HTTP ${status}: ${body}" >&2
  case "$status" in
    401) echo "API key tidak valid." >&2 ;;
    429) echo "Rate limit tercapai (20 request/menit, burst 5)." >&2 ;;
    502) echo "Provider upstream gagal setelah failover — ulangi nanti." >&2 ;;
  esac
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  content="$(echo "$body" | jq -r '.choices[0].message.content // ""')"
  if [ -z "$content" ]; then
    echo "Jawaban kosong dari upstream — perlakukan sebagai kegagalan." >&2
    exit 1
  fi
  echo "$content"
else
  echo "$body"
fi
