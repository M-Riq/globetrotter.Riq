# Postman Validation Checklist

Use this before reconnecting the Next.js frontend. It walks through
three phases:

1. **Validate each microservice individually**, bypassing the gateway,
   so a failure points straight at one service.
2. **Validate the complete workflow through the API Gateway only** --
   the exact path the frontend will take.
3. **Point the frontend at the gateway** once phase 2 is green.

A ready-to-import Postman collection and environment live in
[`postman/`](./postman/):

- `postman/GlobeTrotter.postman_collection.json` -- 56 requests across
  9 folders (health checks, one folder per service, a full gateway
  workflow, and an optional cleanup folder).
- `postman/GlobeTrotter.postman_environment.json` -- every URL,
  credential, and chained variable (tokens/IDs) the collection needs.

Every request that returns something another request needs (a token,
a user id, a destination id) sets it automatically via a Postman
**Tests** script (`pm.environment.set(...)`) -- run folders top to
bottom and you never have to copy/paste a value by hand.

---

## 0. Setup (5 minutes)

1. **Import both files** into Postman: *Import* → drag in both JSON
   files from `postman/`.
2. **Select the "GlobeTrotter Local" environment** in the top-right
   environment picker. Its defaults already match `.env.example`
   (`admin@globetrotter.cm` / `ChangeMe123!`) -- update
   `admin_email` / `admin_password` in the environment if you changed
   them in your own `.env`.
3. **Start the stack with all ports exposed for testing:**

   ```bash
   cp .env.example .env    # if you haven't already
   docker compose up --build
   ```

   `docker-compose.override.yml` is picked up automatically and maps
   every service's port to `localhost` (5001-5006) in addition to the
   gateway's `5000`, so the collection can hit each service directly.
   **This override is for local validation only** -- it's not present
   in a production deployment, where only the gateway (5000) should
   be reachable. You can delete the file, or run
   `docker compose -f docker-compose.yml up` to ignore it, once
   you're done validating.

4. Confirm everything is reachable before opening Postman:

   ```bash
   ./scripts/health-check.sh
   ```

---

## Phase 1 -- Each microservice individually

Run these folders **in order**; later ones depend on tokens/IDs set
by earlier ones. Each request has its own test assertions (visible in
Postman's *Test Results* tab) -- a folder is "passing" when every
request in it is green.

### ☐ `00 - Health Checks`
All 7 requests return 200 with `status: "ok"` (gateway may say
`"degraded"` if you run this before the other services are up --
re-run it last if so).

### ☐ `01 - Auth Service (direct :5001)`
- Register succeeds (201); registering the *same* username again
  correctly fails (409).
- Login returns an access token + refresh token; wrong password
  correctly fails (401).
- Admin login succeeds with the constant credentials.
- `Verify Token` confirms the access token's `sub` matches the
  registered user.
- `Refresh Access Token` returns a new access token from the refresh
  token.

**What this proves in isolation:** JWT issuance/validation, password
hashing, and the admin login path all work without any other service
running.

### ☐ `02 - User Service (direct :5002)`
- `Get My Profile` succeeds *without you ever calling User Service
  directly to create it* -- this is the proof that Auth Service's
  internal call to User Service on registration worked. If this
  request 404s or returns empty preferences, check
  `auth-service`'s logs for `"Could not reach user-service to init
  profile"` and confirm `INTERNAL_SERVICE_KEY` matches between the
  two services' environments.
- Preference update, add/list/remove favorite all succeed.
- The RBAC check (`[RBAC] Non-admin cannot list all users`) confirms
  a normal user's token is correctly rejected with 403 before the
  admin-token version of the same call succeeds with 200.

### ☐ `03 - Destination Service (direct :5003)`
- Public search and get-by-id work with no `Authorization` header at
  all.
- The near-point search returns results sorted by ascending
  `distance_km`.
- The RBAC check confirms a non-admin gets 403 on destination
  creation.
- Admin create/update/list succeed. **Note:** the create step
  overwrites the environment's `destination_id` with the new
  destination's real id -- everything downstream (favorites,
  recommendations, itineraries) now exercises a destination you just
  created, not just the seed data.

### ☐ `04 - Recommendation Service (direct :5004)`
- Both requests succeed and every result carries a `match_score`.
- **This is the first request that depends on two other services
  being reachable** (User Service for preferences, Destination
  Service for candidates) even though you're hitting Recommendation
  Service directly. If it fails but `02` and `03` passed on their
  own, the problem is Recommendation Service's `USER_SERVICE_URL` /
  `DESTINATION_SERVICE_URL` env vars, not those services themselves --
  check they point at Docker network names (`http://user-service:5002`),
  not `localhost`.

### ☐ `05 - Itinerary Service (direct :5005)`
- `Generate Route Preview` succeeds; with no `GOOGLE_MAPS_API_KEY`
  configured, `route.source` should read `fallback_textual`. If you
  *have* set a real key, expect `google_maps` instead -- either is
  correct, just confirm it matches what you configured.
- Generating for an unknown destination correctly 404s.
- `Save Itinerary` persists a "reached" record and sets `itinerary_id`.
- The ownership check confirms a *different* user's token (here, the
  admin token, which has a different `sub`) cannot read your
  itinerary -- 404, not 403, since the service doesn't leak whether
  the resource exists to non-owners.
- `Share via WhatsApp` returns a `https://wa.me/?text=...` link.

### ☐ `06 - Admin Service (direct :5006)`
- `Dashboard Stats` returns non-zero counts *if* you ran folders
  `02`, `03`, and `05` first (it aggregates live from them). Zero
  counts here don't necessarily mean a bug -- check you didn't skip
  ahead.

**Checkpoint:** if every box above is checked, all six services are
individually correct. Any failure from here on is either the Gateway
itself or how two services are wired to reach each other -- not a bug
inside one service's own business logic.

---

## Phase 2 -- Full workflow through the API Gateway only

### ☐ `07 - API Gateway - Full E2E Workflow`

Run this folder top to bottom **using only `{{gateway_url}}`
(port 5000)** -- no direct service ports are used anywhere in this
folder. This is deliberately a fresh, independent run (its own
`gw_*` variables) so it doesn't matter whether you ran Phase 1 first.

It repeats the same shape of workflow as Phase 1, but every request
proves something specific about the **gateway's routing table**
(`api-gateway/config.py`), not about the underlying service:

| Request | What it proves about the Gateway |
|---|---|
| Register / Login / Admin Login | `/api/auth/*` is routed to Auth Service |
| My Profile | `/api/users/*` is routed to User Service |
| Admin - Create Destination | `/api/admin/destinations` is routed to **Destination Service**, not swallowed by the more general `/api/admin` prefix -- this is the longest-prefix-wins rule |
| Search Destinations | `/api/destinations` (no `/admin`) is routed to Destination Service too, and the destination just created through the gateway is actually visible |
| Get Recommendations | The gateway can carry a single request three services deep (Gateway → Recommendation Service → User + Destination Services) without anything breaking |
| Generate / Save / List / Share Itinerary | `/api/itineraries/*` is routed to Itinerary Service, including the `/generate` and `/{id}/share` sub-paths |
| Admin Dashboard Stats | `/api/admin/dashboard/stats` correctly falls through to the general `/api/admin` prefix → Admin Service (since no more specific prefix matches) |
| Unmapped path → 404 | The gateway doesn't silently swallow a typo'd path -- it fails loudly instead of forwarding somewhere wrong |

**Checkpoint:** every request in this folder passing means the
gateway's routing table is correct end-to-end -- this is the closest
thing to "the frontend already works," short of running the frontend
itself.

### ☐ `08 - Cleanup (run manually)`
Optional. Deletes the test destinations and the test user profile
created above. Not part of the automated pass/fail -- run it if you'd
rather not leave test data sitting in your local `data/*.json` files.
(It only removes the User Service *profile*; the Auth Service
credential record has no delete endpoint yet, so the login will still
technically work afterward -- see the root README's "out of scope"
notes.)

---

## Phase 3 -- Reconnect the frontend

Once Phase 2 is fully green:

1. Point the frontend's API base URL at the gateway
   (`http://localhost:5000` locally, or your deployed gateway/Ingress
   URL in production) -- **not** at any individual service.
2. Optionally remove `docker-compose.override.yml` (or stop using it)
   so only the gateway is exposed, matching how it'll run in
   production/Kubernetes.
3. Do one manual smoke pass in the actual UI: register, log in,
   browse destinations, get a recommendation, generate + save an
   itinerary, share it, and (as admin) check the dashboard. If
   Phase 2 passed, this should just work -- if something differs, the
   gap is specifically in how the frontend calls the API (headers,
   payload shape, base URL), not in the backend itself.

## Troubleshooting quick reference

| Symptom | Likely cause |
|---|---|
| A direct-service request works but the same one through the gateway 404s | Check `api-gateway/config.py`'s `SERVICE_ROUTES` / `ORDERED_PREFIXES` -- a new path prefix may need adding, or an existing one is shadowing it |
| `502` from the gateway | The target service is down, or its `*_SERVICE_URL` env var on the **gateway** doesn't match the Docker network name |
| User profile missing right after registration | Auth → User Service internal call failed (check `INTERNAL_SERVICE_KEY` matches on both, and `USER_SERVICE_URL` on Auth Service) -- the profile will still lazily create itself on first `GET /api/users/me`, just without the preferences you registered with |
| Recommendations / dashboard stats always empty | The calling service's `Authorization` header isn't being forwarded, or its `USER_SERVICE_URL` / `DESTINATION_SERVICE_URL` / `ITINERARY_SERVICE_URL` env vars point at `localhost` instead of the Docker network name |
| `route.source` is never `google_maps` | Expected with no `GOOGLE_MAPS_API_KEY` set -- this is the designed fallback, not a bug |
| 403 where you expected 200 | JWT `role` claim doesn't match what the route requires -- confirm you're using `admin_token` (from `/api/auth/admin/login`), not `access_token`, for admin-only requests |
