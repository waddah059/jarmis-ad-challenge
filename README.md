# Jarmis A/D — Competition-Ready Service Pack

A self-contained Attack/Defense vulnbox inspired by the learning chain of the retired HTB Jarmis machine:

**recon → JARM-style lookup → SSRF → internal-service discovery → flag theft**

This is a deliberately vulnerable educational service. It does **not** deploy real OMIGOD/OMI exploitation or arbitrary command execution.

## What is included

- Hardened Docker service container.
- Private internal service reachable only from the service container's internal Docker network.
- Intentional SSRF in `/api/v1/fetch`.
- Mock JARM lookup API.
- Per-team identity via `TEAM_ID`.
- Per-round flag storage.
- Token-protected checker control plane for flag placement/retrieval.
- Standalone checker with `CHECK_SLA`, `PUT_FLAG`, and `GET_FLAG` actions.
- Single-team deployment for development.
- Six-team local simulation template.
- Attack path, defender notes, deployment guide, scoring guidance, and test checklist.

## Competition chain

1. Players discover the API.
2. They enumerate the mock JARM database.
3. They identify the SSRF endpoint.
4. They use SSRF against `http://internal-service:9000`.
5. They enumerate `/api/info`, `/api/metadata`, and `/api/run?cmd=status`.
6. The status response contains the current team flag.
7. They submit the stolen flag to the CTF platform.
8. Defenders patch the SSRF while keeping `/health` and JARM lookup functional.

The checker deliberately does **not** depend on the vulnerable SSRF endpoint for ordinary SLA checks. A team can therefore patch the SSRF without automatically losing service-availability points.

## Quick local deployment

Requires Docker Engine + Compose v2.

```bash
cd deploy
cp .env.example .env
# edit .env and replace CHECKER_TOKEN
# keep this service on an isolated test network

docker compose up -d --build
docker compose ps
curl http://127.0.0.1:8000/health
```

The supplied compose file intentionally publishes no host port. For a quick demo, temporarily add a loopback-only mapping such as `127.0.0.1:18001:8000`.

## Local six-team simulation

```bash
docker compose -f deploy/local-six-teams.yml up -d --build
```

The six public ports are 18001–18006. Each team has a separate internal network and state volume.

## Checker interface

The checker follows the common Oasis/CTFBox-style action model:

```bash
ACTION=CHECK_SLA TARGET_URL=http://TEAM_IP:8000 ./checker/checker.py
ACTION=PUT_FLAG  TARGET_URL=http://TEAM_IP:8000 ROUND=12 FLAG='JARMIS{...}' CHECKER_TOKEN='...' ./checker/checker.py
ACTION=GET_FLAG  TARGET_URL=http://TEAM_IP:8000 ROUND=12 CHECKER_TOKEN='...' ./checker/checker.py
```

For CTFBox, wire these actions into the platform's checker lifecycle rather than exposing the checker token to players. CTFBox currently documents a checker-based A/D architecture with configurable flag expiry, service score, checker timeout/concurrency, and team vulnboxes. citeturn2search0

## CTFBox deployment model

Recommended competition topology:

- CTFBox control/game server: scoreboard, flag submissions, checkers.
- One vulnbox per team.
- Six identical Jarmis service instances, each with a unique `TEAM_ID`, checker token and state volume.
- Player traffic only reaches the team vulnbox through the game network.
- Checker traffic is controlled by the CTFBox checker network.
- No organizer/control-plane port is exposed to player networks.

CTFBox supports `incus-vm` for stronger isolation when players are not trusted; its documentation specifically warns against privileged team boxes for untrusted participants. citeturn2search0

## Suggested scoring

Let the platform handle the exact global scoring formula. For this service use:

- **SLA:** 100% when `/health` and JARM lookup work.
- **Flag:** one accepted flag submission for each valid attacker/victim/round pair.
- **Patch:** defenders receive full SLA after removing SSRF while preserving normal functionality.
- **Service failure:** zero SLA for the affected check interval.
- **Flag expiry:** use the CTFBox `flag_expire_ticks` setting rather than implementing a second expiry system inside the service.

Do not award attack points merely because a player hits `/api/v1/fetch`; require a valid flag submission through the game server.

## Security boundary

The challenge is intentionally vulnerable, but the competition infrastructure must not be.

- Isolate the competition LAN/VPN.
- Do not publish the vulnboxes to the public Internet.
- Keep checker tokens outside the repository and player images.
- Do not run the service container privileged.
- Do not mount `/var/run/docker.sock`.
- Do not grant `NET_ADMIN`, host networking, or host filesystem mounts.
- Prefer VM-level isolation for untrusted participants.

## Instructor material

- `docs/ATTACK_PATH.md` — intended solve path.
- `docs/DEFENDER_GUIDE.md` — what teams can patch and what must remain functional.
- `docs/CTFBOX_INTEGRATION.md` — integration checklist and checker mapping.
- `docs/DEPLOYMENT.md` — competition deployment checklist.
- `docs/TEST_PLAN.md` — pre-event acceptance tests.
- `docs/CHALLENGE_SPEC.md` — final challenge specification.

## Important status

The repository is **deployment-ready as a service pack**, but the final CTFBox wiring must be tested against the exact CTFBox commit/version used by your organizers. The checker intentionally exposes a small, platform-neutral interface instead of pretending that a version-specific internal CTFBox API is stable.
