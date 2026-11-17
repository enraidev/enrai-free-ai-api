#!/usr/bin/env bash
# Cek model API yang aktif di Enrai (API AI gratis, kompatibel OpenAI).
# Pemakaian:
#   export ENRAI_API_KEY="YOUR_API_KEY"
#   ./models.sh
# Dokumentasi: https://enrai.web.id/docs

set -euo pipefail

: "${ENRAI_API_KEY:?Set dulu: export ENRAI_API_KEY='YOUR_API_KEY' (daftar gratis di https://enrai.web.id/register)}"

response="$(curl -sS -w '\n%{http_code}' https://enrai.web.id/v1/models \
  -H "Authorization: Bearer ${ENRAI_API_KEY}")"

status="${response##*$'\n'}"
body="${response%$'\n'*}"

if [ "$status" != "200" ]; then
  echo "HTTP ${status}: ${body}" >&2
  case "$status" in
    401) echo "API key tidak valid. Periksa ENRAI_API_KEY." >&2 ;;
    429) echo "Rate limit tercapai (60 request/menit untuk endpoint ini)." >&2 ;;
    *)   echo "Permintaan gagal." >&2 ;;
  esac
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  echo "$body" | jq -r '.data[]?.id // empty' | sed 's/^/model: /'
else
  echo "$body"
fi
