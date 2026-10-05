# Competition Deployment Checklist

## Before the event

- [ ] Freeze the exact service image/repository commit.
- [ ] Generate six unique checker tokens.
- [ ] Configure six unique team IDs.
- [ ] Configure the CTFBox service and checker.
- [ ] Set flag expiry and service score in CTFBox.
- [ ] Use isolated event networking.
- [ ] Prefer VM isolation for participant boxes.
- [ ] Confirm the scoreboard/control plane is not reachable from player subnets.
- [ ] Test a clean team box and a patched team box.

## During a dry run

- [ ] Six teams start with identical services.
- [ ] Checker places a fresh flag for every team.
- [ ] Checker confirms SLA.
- [ ] Team A steals Team B's flag.
- [ ] Team A submits it to the game server.
- [ ] Team B patches SSRF.
- [ ] Team B still receives SLA.
- [ ] Team A can no longer steal a fresh flag from Team B.
- [ ] Resetting a team restores the original vulnerable image.

## Do not do this

- Do not expose the vulnboxes to the Internet.
- Do not use privileged containers for untrusted players when stronger isolation is available.
- Do not place checker tokens in the player image.
- Do not give players access to Docker socket, host filesystem, or organizer APIs.
