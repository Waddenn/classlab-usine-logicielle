#!/usr/bin/env sh
set -eu

base_url="${1:-http://127.0.0.1:8000}"

curl --fail --silent --show-error "$base_url/health/live" | grep -q '"status":"ok"'
curl --fail --silent --show-error "$base_url/health/ready" | grep -q '"status":"ready"'
curl --fail --silent --show-error "$base_url/api/v1/info" | grep -q '"version"'
curl --fail --silent --show-error "$base_url/metrics" | grep -q 'factory_http_requests_total'
printf 'Smoke test réussi sur %s\n' "$base_url"
