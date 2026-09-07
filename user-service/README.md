# User Service

Owns visitor profiles: preferences and favorites (bookmarked
destinations). Credentials stay in the **Auth Service**; the history
of *reached* destinations (impressions, ratings, dates, route used)
lives in the **Itinerary Service**, since it's generated alongside
the route itself -- keeping that logic in one place only. Profiles
are linked to Auth records only by `user_id`.

## Endpoints

| Method | Path                            | Auth          | Description |
|--------|----------------------------------|---------------|--------------|
| GET    | `/api/users/me`                  | Bearer        | Get my profile (preferences/favorites) |
| PUT    | `/api/users/me`                  | Bearer        | Update my preferences |
| GET    | `/api/users/me/favorites`        | Bearer        | List favorite destination ids |
| POST   | `/api/users/me/favorites`        | Bearer        | Add a favorite `{destination_id}` |
| DELETE | `/api/users/me/favorites/<id>`   | Bearer        | Remove a favorite |
| GET    | `/api/admin/users`               | Bearer(admin) | List all profiles |
| GET    | `/api/admin/users/<user_id>`     | Bearer(admin) | Get one profile |
| DELETE | `/api/admin/users/<user_id>`     | Bearer(admin) | Delete a profile |
| POST   | `/internal/users/profiles`       | Internal key  | Called by Auth Service on registration |
| GET    | `/health`                        | none          | Liveness/readiness probe |

## Environment variables

See `config.py`. `JWT_SECRET_KEY` and `INTERNAL_SERVICE_KEY` must
match the values used by the Auth Service.
