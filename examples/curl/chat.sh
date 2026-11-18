#!/usr/bin/env bash
# Chat completion with curl against the free Enrai AI API.
# Usage:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./chat.sh "Hello from cURL!"
# Documentation: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set it first: export ENRAI_API_KEY='YOUR_API_KEY' (sign up free at https://enrai.web.id/register)}"

MODEL="${ENRAI_MODEL:-Chatgpt}"
prompt="${*:-Hello! What is an OpenAI-compatible API?}"

# JSON escape: backslashes first, then double quotes.
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
    401) echo "Invalid API key." >&2 ;;
    429) echo "Rate limit reached (20 requests/minute, burst 5)." >&2 ;;
    502) echo "Upstream provider failed after failover - retry later." >&2 ;;
  esac
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  content="$(echo "$body" | jq -r '.choices[0].message.content // ""')"
  if [ -z "$content" ]; then
    echo "Empty answer from upstream - treat it as a failure." >&2
    exit 1
  fi
  echo "$content"
else
  echo "$body"
fi
