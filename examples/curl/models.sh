#!/usr/bin/env bash
# List the live Enrai models (free AI API, OpenAI-compatible).
# Usage:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./models.sh
# Documentation: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set it first: export ENRAI_API_KEY='YOUR_API_KEY' (sign up free at https://enrai.web.id/register)}"

response="$(curl -sS -w '\n%{http_code}' https://enrai.web.id/v1/models \
  -H "Authorization: Bearer ${ENRAI_API_KEY}")"

status="${response##*$'\n'}"
body="${response%$'\n'*}"

if [ "$status" != "200" ]; then
  echo "HTTP ${status}: ${body}" >&2
  case "$status" in
    401) echo "Invalid API key. Check ENRAI_API_KEY." >&2 ;;
    429) echo "Rate limit reached (60 requests/minute for this endpoint)." >&2 ;;
    *)   echo "Request failed." >&2 ;;
  esac
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  echo "$body" | jq -r '.data[]?.id // empty' | sed 's/^/model: /'
else
  echo "$body"
fi
