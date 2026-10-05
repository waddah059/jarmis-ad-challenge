# Intended Attack Path — Instructor Only

1. `GET /` and `/health` reveal a web API.
2. Query `/api/v1/search/id/mock-web` and `/api/v1/search/signature/MOCK-JARM-7F4A-91B2`.
3. Notice `/api/v1/fetch?endpoint=...` accepts an arbitrary URL.
4. Target the private hostname `internal-service`.
5. Enumerate:
   - `/health`
   - `/api/info`
   - `/api/metadata`
   - `/api/run?cmd=status`
6. The `status` response contains the current flag.
7. Submit that flag to the competition flag server.

The challenge is intentionally designed so that the interesting pivot is **SSRF → internal service**, not real-world kernel exploitation.
