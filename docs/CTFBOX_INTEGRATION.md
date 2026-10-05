# CTFBox Integration

CTFBox is the competition platform; this repository is the service/checker pack.

CTFBox documents an A/D model with vulnboxes, checkers, flag expiry, service scores and configurable checker concurrency. citeturn2search0

## Service registration

Register one service named `jarmis` for every team vulnbox.

Recommended values:

- Service port: `8000/tcp`
- SLA health: `GET /health`
- SLA functional check: `GET /api/v1/search/id/mock-web`
- Flag placement: checker control endpoint `POST /_checker/flag`
- Flag retrieval: checker control endpoint `GET /_checker/flag/{round}`
- Attack target: `GET /api/v1/fetch?endpoint=...`

## Checker mapping

Map the platform lifecycle to:

- `CHECK_SLA` → `checker.py` with `ACTION=CHECK_SLA`
- `PUT_FLAG` → `checker.py` with `ACTION=PUT_FLAG`
- `GET_FLAG` → `checker.py` with `ACTION=GET_FLAG`

The public repository does not contain real competition tokens.

## Flag handling

Let CTFBox generate the flag and pass it to the checker for the current round. The service stores the flag by round. Configure CTFBox's own `flag_expire_ticks` for expiry. Do not duplicate global scoring or expiry logic inside the vulnbox. citeturn2search0

## Isolation

For the real event, prefer CTFBox's stronger VM isolation when feasible. CTFBox documents `incus-vm` as the safer choice for untrusted players and warns that privileged mode provides weak isolation. citeturn2search0

## Final compatibility test

Before the event, verify against the exact CTFBox checkout:

1. Deploy one team vulnbox.
2. Run `PUT_FLAG` for round 1.
3. Run `CHECK_SLA`.
4. Run `GET_FLAG`.
5. Confirm a player can reach the vulnbox but not the game server/control plane.
6. Exploit SSRF and submit the flag through the game server.
7. Patch SSRF.
8. Re-run SLA and confirm it remains healthy.
9. Repeat with all six teams.
