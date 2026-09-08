# Destination Service

Owns every destination in Yaoundé (restaurants, shopping, vie
nocturne, tourisme, hôtels, services administratifs, santé, culture,
loisirs, sports, transport).

## Endpoints

| Method | Path                              | Auth          | Description |
|--------|------------------------------------|---------------|--------------|
| GET    | `/api/destinations`                | none          | Search/filter: `q, category, tag, max_budget, min_rating, lat, lng` |
| GET    | `/api/destinations/<id>`           | none          | Get one destination |
| GET    | `/api/admin/destinations`          | Bearer(admin) | List all (admin view) |
| POST   | `/api/admin/destinations`          | Bearer(admin) | Create |
| PUT    | `/api/admin/destinations/<id>`     | Bearer(admin) | Update |
| DELETE | `/api/admin/destinations/<id>`     | Bearer(admin) | Delete |
| GET    | `/health`                          | none          | Liveness/readiness probe |

When `lat`/`lng` are supplied, results include `distance_km` and are
sorted nearest-first (haversine distance) -- used by the
Recommendation and Itinerary services.
