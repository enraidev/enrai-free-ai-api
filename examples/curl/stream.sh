#!/usr/bin/env bash
# SSE streaming with curl against the free Enrai AI API.
# Usage:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./stream.sh "Count from 1 to 10."
# Documentation: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set it first: export ENRAI_API_KEY='YOUR_API_KEY' (sign up free at https://enrai.web.id/register)}"

MODEL="${ENRAI_MODEL:-Chatgpt}"
prompt="${*:-Write a short paragraph about APIs.}"

escaped="$(printf '%s' "$prompt" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')"

curl -sS -N https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer ${ENRAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "{\"model\":\"${MODEL}\",\"stream\":true,\"messages\":[{\"role\":\"user\",\"content\":\"${escaped}\"}]}"
