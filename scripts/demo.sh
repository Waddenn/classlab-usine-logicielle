#!/usr/bin/env bash
set -euo pipefail

namespace=factory
base_url="${1:-http://factory.192.168.56.12.nip.io}"

echo "1/4 État du déploiement"
kubectl -n "$namespace" get deployment,pods,service,ingress,hpa

echo "2/4 Version servie"
curl --fail --silent --show-error "$base_url/api/v1/info"
echo

echo "3/4 Génération de trafic"
for _ in $(seq 1 30); do curl --silent "$base_url/api/v1/info" >/dev/null; done

echo "4/4 Métriques applicatives"
curl --fail --silent --show-error "$base_url/metrics" \
  | grep '^factory_http_requests_total' \
  | head
