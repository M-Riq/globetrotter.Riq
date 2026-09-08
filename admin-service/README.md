# Admin Service

Powers the admin dashboard with system-wide statistics, aggregated
live from the other services (it stores nothing itself). Entity
CRUD (destinations, users) and authentication stay in their owning
services -- this keeps each piece of business logic in exactly one
place, per the "aucune logique métier ne doit être dupliquée"
constraint.

## Endpoint

| Method | Path                         | Auth          | Description |
|--------|--------------------------------|---------------|--------------|
| GET    | `/api/admin/dashboard/stats`  | Bearer(admin) | Total users, total destinations (+ by category), total itineraries, total destinations reached |
| GET    | `/health`                     | none          | Liveness/readiness probe |

For destination CRUD see the **Destination Service**
(`/api/admin/destinations`), for user management see the
**User Service** (`/api/admin/users`), and for admin login see the
**Auth Service** (`/api/auth/admin/login`). The API Gateway exposes
all of these under a consistent `/api/admin/*` prefix regardless of
which service actually handles them.