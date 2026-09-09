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

for overlay in staging production; do
  kubectl kustomize "k8s/overlays/$overlay" >/tmp/factory-api-"$overlay".yaml
  test -s /tmp/factory-api-"$overlay".yaml
done

sed -n '/factory-api.json: |-/,${p}' monitoring/grafana-dashboard.yaml \
  | tail -n +2 \
  | sed 's/^    //' \
  | python3 -m json.tool >/dev/null

echo "Validation locale réussie"
