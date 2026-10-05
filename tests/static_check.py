from pathlib import Path
import re, ast

root=Path(__file__).parents[1]
for p in [*root.glob('service/*.py'), root/'checker/checker.py']:
    ast.parse(p.read_text()); print('PY OK',p)

compose=(root/'deploy/docker-compose.yml').read_text()
assert 'privileged:' not in compose
assert 'docker.sock' not in compose
assert 'network_mode: host' not in compose
assert 'internal: true' in compose
print('SECURITY STATIC CHECKS OK')

for p in [root/'service/app.py', root/'service/internal.py']:
    assert 'JARM{' not in p.read_text(), f'possible hard-coded flag in {p}'
print('NO HARDCODED FLAGS CHECK OK')
