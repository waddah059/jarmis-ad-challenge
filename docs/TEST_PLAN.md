# Acceptance Test Plan

## Static checks

- Python files compile with `python3 -m py_compile`.
- Compose YAML parses.
- No checker token is committed to the source tree.
- No host Docker socket is mounted.
- No `privileged: true` is present.
- No host network mode is used.

## Functional checks

1. `/health` returns 200.
2. JARM lookup returns the expected mock record.
3. SSRF accepts HTTP URLs.
4. `internal-service` is not published to the host.
5. SSRF reaches `internal-service` from the application network.
6. `/_checker/flag` returns 404 without the token.
7. Correct checker token places a flag.
8. Internal status exposes the current flag through the intended challenge path.
9. Checker SLA still passes after SSRF is patched.
10. Six isolated team instances do not share their SQLite state.

## Competition test

Run at least two complete attack/defense rounds before using six teams. Then run a full six-team dry run with the actual CTFBox configuration.
