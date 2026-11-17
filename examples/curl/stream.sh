#!/usr/bin/env bash
# Streaming SSE via curl ke API AI gratis Enrai.
# Pemakaian:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./stream.sh "Hitung 1 sampai 10."
# Dokumentasi: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set dulu: export ENRAI_API_KEY='YOUR_API_KEY' (daftar gratis di https://enrai.web.id/register)}"

MODEL="${ENRAI_MODEL:-Chatgpt}"
prompt="${*:-Tulis paragraf singkat tentang API.}"

escaped="$(printf '%s' "$prompt" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')"

curl -sS -N https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer ${ENRAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "{\"model\":\"${MODEL}\",\"stream\":true,\"messages\":[{\"role\":\"user\",\"content\":\"${escaped}\"}]}"
