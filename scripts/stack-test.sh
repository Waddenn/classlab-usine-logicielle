#!/usr/bin/env sh
set -eu

app_url="${APP_URL:-http://127.0.0.1:8000}"
prometheus_url="${PROMETHEUS_URL:-http://127.0.0.1:9090}"
grafana_url="${GRAFANA_URL:-http://127.0.0.1:3000}"
grafana_user="${GRAFANA_ADMIN_USER:-admin}"
grafana_password="${GRAFANA_ADMIN_PASSWORD:-classlab}"

"$(dirname "$0")/smoke-test.sh" "$app_url"
curl --fail --silent --show-error "$prometheus_url/-/ready" >/dev/null

target_value=$(curl --fail --silent --show-error --get \
  --data-urlencode 'query=up{job="factory-api"}' \
  "$prometheus_url/api/v1/query" \
  | python3 -c 'import json,sys; data=json.load(sys.stdin)["data"]["result"]; print(data[0]["value"][1] if data else "0")')
test "$target_value" = "1"

curl --fail --silent --show-error "$grafana_url/api/health" | grep -q '"database": "ok"'
curl --fail --silent --show-error \
  --user "$grafana_user:$grafana_password" \
  "$grafana_url/api/dashboards/uid/factory-api" \
  | grep -q '"title":"Factory API"'

printf 'Pile complète validée : application, Prometheus et Grafana\n'
