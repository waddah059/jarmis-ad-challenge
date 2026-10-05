# Defender Guide — Competition Version

## What defenders are expected to do

Patch the SSRF while keeping the service alive.

A reasonable fix is to replace arbitrary URL fetching with an allow-list of known public resources, or remove the feature entirely if the event rules allow it.

## SLA-critical endpoints

Keep these working:

- `GET /health`
- `GET /api/v1/search/id/mock-web`
- `GET /api/v1/search/signature/MOCK-JARM-7F4A-91B2`

Breaking these should reduce SLA.

## What is intentionally not required

The following is challenge control-plane functionality and should not be targeted by players:

- `/_checker/*`

Those endpoints require a secret token and return 404 without it.

## Organizer rule

Defenders should be told that patching the SSRF is valid and encouraged. They should not need to delete the entire application or firewall off their own service to score well.
