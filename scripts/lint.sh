#!/usr/bin/env sh
set -eu
python3 -m py_compile service/*.py checker/checker.py
python3 - <<'PY'
import yaml
for p in ['deploy/docker-compose.yml','deploy/local-six-teams.yml']:
    yaml.safe_load(open(p)); print('YAML OK:', p)
PY
echo 'Static checks passed.'
