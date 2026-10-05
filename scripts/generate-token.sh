#!/usr/bin/env sh
set -eu
python3 - <<'PY'
import secrets
for i in range(1,7): print(f'team{i}: {secrets.token_urlsafe(32)}')
PY
