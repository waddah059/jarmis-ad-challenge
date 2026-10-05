# Prompt — Generate a Competition-Ready A/D Web Challenge From Scratch

You are a senior Attack/Defense CTF challenge architect, web-security engineer, Docker engineer, and competition-infrastructure developer.

Build a complete, production-quality Attack/Defense CTF service from scratch for a university cybersecurity competition.

## Competition context

- Platform: CTFBox (or an equivalent Oasis/CTFBox-style A/D platform).
- Teams: 6 teams.
- Team size: 4 players.
- Each team owns one isolated vulnbox/service instance.
- Players can attack other teams' service instances during the active game period.
- Defenders must patch their own instance without losing service-availability/SLA points.
- Flags are generated and expired by the competition platform.
- The game server/scoreboard/checker infrastructure is separate from player services.
- The challenge must run safely on an isolated event network.
- The target must be suitable for Raspberry-Pi-class or small VM deployment where practical.

## Challenge concept

Create a Jarmis-inspired web challenge with this learning chain:

recon → JARM/TLS-style API enumeration → SSRF → internal service discovery → flag theft

Do NOT copy proprietary content, source code, flags, or exact implementation from any existing machine. Make an original implementation inspired only by the general learning progression.

Do NOT deploy a real OMIGOD/OMI exploit, arbitrary shell execution, Docker socket access, privileged containers, host filesystem mounts, or a real container escape.

## Required player-facing application

Implement a small Python FastAPI web application with:

- `/`
- `/health`
- `/api/v1/search/id/{id}`
- `/api/v1/search/signature/{signature}`
- `/api/v1/fetch?endpoint=...`

The `/api/v1/fetch` endpoint must contain an intentional SSRF vulnerability suitable for the competition.

The API should expose enough information through normal recon to make the intended path discoverable without giving away the flag directly.

## Required internal service

Create a second service named `internal-service` that:

- is reachable from the web application container;
- is NOT published to the host or player network directly;
- exposes `/health`, `/api/info`, `/api/metadata`, and `/api/run?cmd=status`;
- returns the current competition flag from the `status` endpoint;
- contains no real command execution;
- accepts only predefined harmless responses.

The intended exploit must be:

1. discover SSRF;
2. discover the internal hostname/port;
3. enumerate the internal service;
4. retrieve the current flag;
5. submit the flag through the A/D game server.

## A/D requirements

The service must be designed for attack/defense scoring, not just a standalone CTF.

Implement:

1. Per-team identity via `TEAM_ID`.
2. Per-round flag storage.
3. Token-protected checker control endpoints for placing and retrieving flags.
4. A standalone checker with these actions:
   - `CHECK_SLA`
   - `PUT_FLAG`
   - `GET_FLAG`
5. Checker timeouts and clear failure messages.
6. Health checks that do NOT require the vulnerable SSRF to remain present.
7. A design where defenders can patch the SSRF and keep SLA points.
8. No player access to checker secrets.
9. No duplicate global scoring system inside the vulnbox; the A/D platform owns scoring and flag expiry.

Use an interface compatible with common Oasis/CTFBox-style checker execution, for example:

```text
ACTION=CHECK_SLA TARGET_URL=http://TEAM_IP:8000
ACTION=PUT_FLAG TARGET_URL=http://TEAM_IP:8000 ROUND=12 FLAG='JARMIS{...}' CHECKER_TOKEN='...'
ACTION=GET_FLAG TARGET_URL=http://TEAM_IP:8000 ROUND=12 CHECKER_TOKEN='...'
```

Also document exactly how to map these actions to the selected CTFBox version.

## Docker security requirements

Use multi-service Docker Compose.

The web service must:

- run as a non-root user;
- use a read-only filesystem where practical;
- use a writable volume only for required application state;
- use `tmpfs` for `/tmp` if needed;
- drop Linux capabilities;
- set `no-new-privileges`;
- never use `privileged: true`;
- never mount `/var/run/docker.sock`;
- never use host networking;
- never mount the host filesystem;
- never require host-level shell access.

The internal network must be isolated from the player-facing network.

## Repository requirements

Generate the COMPLETE repository, not a sketch.

Use this structure or a better equivalent:

```text
challenge-name/
├── README.md
├── LICENSE
├── .gitignore
├── PROMPT_FROM_SCRATCH.md
├── service/
│   ├── Dockerfile
│   ├── Dockerfile.internal
│   ├── requirements.txt
│   ├── app.py
│   ├── internal.py
│   └── .dockerignore
├── checker/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── checker.py
├── deploy/
│   ├── docker-compose.yml
│   ├── local-six-teams.yml
│   └── .env.example
├── docs/
│   ├── CHALLENGE_SPEC.md
│   ├── ATTACK_PATH.md
│   ├── DEFENDER_GUIDE.md
│   ├── CTFBOX_INTEGRATION.md
│   ├── DEPLOYMENT.md
│   └── TEST_PLAN.md
├── scripts/
│   ├── generate-token.sh
│   └── lint.sh
└── tests/
```

## Documentation requirements

README must contain:

- challenge overview;
- architecture diagram in ASCII;
- intended attack path;
- intended defensive patch;
- local deployment instructions;
- six-team simulation instructions;
- checker usage;
- CTFBox integration instructions;
- scoring recommendations;
- security/isolation requirements;
- troubleshooting;
- exact list of exposed ports;
- reset procedure.

Create an instructor-only attack guide and a defender guide.

## Testing requirements

Create automated or semi-automated tests for:

- health;
- JARM lookup;
- SSRF reachability;
- internal service isolation;
- flag placement;
- flag retrieval;
- invalid checker token rejection;
- per-team state separation;
- checker SLA after SSRF is patched;
- absence of privileged Docker settings.

If Docker is available, actually run:

```bash
docker compose config

docker compose build

docker compose up -d
```

Then test the full chain and tear it down.

If Docker is NOT available, do not pretend that runtime testing was performed. Run every possible static test, compile all Python files, parse all YAML, and explicitly report what could not be tested.

## A/D fairness requirements

The challenge must satisfy all of these:

- The exploit is reproducible across all six team instances.
- Each team gets a unique current flag.
- Flags are not visible in source code.
- A stolen flag is useless after the platform expires it.
- A defender can patch SSRF without destroying SLA-critical functionality.
- Stopping the whole service should lose SLA points.
- Merely touching the vulnerable endpoint must not award attack points.
- Attack points require valid flag submission through the game server.
- The checker must never reveal the expected flag to players.
- Team A must never receive Team B's flag from its own instance.

## Difficulty

Target difficulty: medium-hard for engineering students with basic web-security knowledge.

Make the intended path solvable without guessing obscure endpoints, but do not expose the flag directly through the public API.

## Deliverables

Return:

1. the complete repository tree;
2. every file's complete contents;
3. exact commands to deploy it;
4. exact commands to run the checker;
5. exact CTFBox integration steps;
6. the intended attacker solve path for instructors;
7. the defender patch strategy;
8. a pre-event six-team acceptance-test procedure;
9. a list of assumptions and anything that depends on the exact CTFBox version;
10. a final verification report stating exactly what was tested and what was not tested.

Never claim that something was executed if you could only inspect the source.
