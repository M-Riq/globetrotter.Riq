# API Gateway

Single entry point for the Next.js frontend. A thin, stateless
reverse proxy -- it forwards each request to the owning microservice
and streams the response back unchanged (status, body, headers). It
does **not** duplicate authentication or RBAC: every downstream
service validates its own JWT, exactly as if the frontend called it
directly.

## Routing table

| Path prefix                  | Forwarded to             |
|-------------------------------|---------------------------|
| `/api/auth/*`                 | Auth Service (5001)       |
| `/api/admin/users/*`          | User Service (5002)       |
| `/api/admin/destinations/*`   | Destination Service (5003)|
| `/api/admin/itineraries/*`    | Itinerary Service (5005)  |
| `/api/admin/*` (everything else, e.g. `dashboard/stats`) | Admin Service (5006) |
| `/api/users/*`                | User Service (5002)       |
| `/api/destinations/*`         | Destination Service (5003)|
| `/api/recommendations/*`      | Recommendation Service (5004) |
| `/api/itineraries/*`          | Itinerary Service (5005)  |

Longest prefix wins, so `/api/admin/destinations` is matched before
the more general `/api/admin`. See `config.SERVICE_ROUTES` /
`ORDERED_PREFIXES`.

## Health

`GET /health` pings every downstream service's own `/health` and
returns an aggregate status -- handy for a single "is GlobeTrotter up"
check without hitting six separate URLs.

## Environment variables

Each `*_SERVICE_URL` var overrides where that prefix is forwarded
(defaults point at the Docker Compose service names). `CORS_ORIGINS`
should be the frontend's origin(s) in production.
