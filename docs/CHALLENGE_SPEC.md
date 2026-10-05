# Challenge Specification

**Name:** Jarmis A/D

**Category:** Web / SSRF / Internal Network Discovery

**Difficulty:** Medium–Hard for a mixed university A/D event

**Core vulnerability:** Server-Side Request Forgery

**Secondary skill:** HTTP enumeration and internal service discovery

**Player objective:** steal flags from other teams while keeping the team's own service operational.

**Defender objective:** patch the SSRF without destroying the SLA-critical API.

**Flag location:** internal management service, exposed through a status endpoint reachable only from the internal network.

**Expected solve:** roughly 10–30 minutes for a competent web player after recon, depending on event hints.

**Intended lesson:** SSRF is not just “read localhost”; it becomes dangerous when the application can reach services that the attacker cannot directly reach.
