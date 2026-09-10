#!/usr/bin/env sh
set -eu

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

if [ ! -x .venv/bin/python ]; then
  echo "Environnement absent. Exécuter: make install" >&2
  exit 1
fi

.venv/bin/ruff check app tests
.venv/bin/ruff format --check app tests
.venv/bin/python -m pytest
docker compose config --quiet

for overlay in staging production; do
  kubectl kustomize "k8s/overlays/$overlay" >/tmp/factory-api-"$overlay".yaml
  test -s /tmp/factory-api-"$overlay".yaml
done

grep -q '^  name: factory-staging$' /tmp/factory-api-staging.yaml
grep -q '^  namespace: factory-staging$' /tmp/factory-api-staging.yaml
grep -q '^  name: factory-api-staging$' /tmp/factory-api-staging.yaml
grep -q '^  namespace: factory$' /tmp/factory-api-production.yaml

sed -n '/factory-api.json: |-/,${p}' monitoring/grafana-dashboard.yaml \
  | tail -n +2 \
  | sed 's/^    //' \
  | python3 -m json.tool >/dev/null
python3 -m json.tool monitoring/grafana/dashboards/factory-api.json >/dev/null

echo "Validation locale réussie"
