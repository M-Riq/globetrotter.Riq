# GlobeTrotter – Travel Assistant

GlobeTrotter is a **monolithic Flask application** that serves as the starting point for a semester-long capstone project.  
Students build the monolith first, then refactor it into microservices, and finally deploy it to the cloud with resilience patterns using Docker, Kubernetes, and cloud-native tooling.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # Data models and JSON file I/O
│   ├── auth.py             # Registration, login, JWT handling
│   ├── destinations.py     # Destination search endpoint
│   ├── recommendations.py  # Personalised recommendations endpoint
│   ├── itineraries.py      # Create / list itineraries
│   └── main.py             # App entry point
├── data/
│   ├── destinations.json   # Static destination catalogue (seed data)
│   ├── users.json          # Created at runtime
│   └── itineraries.json    # Created at runtime
├── tests/                  # Placeholder for future tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## REST API

| Method | Endpoint            | Auth required | Description                              |
|--------|---------------------|---------------|------------------------------------------|
| POST   | `/register`         | No            | Register a new user                      |
| POST   | `/login`            | No            | Authenticate and receive a JWT token     |
| GET    | `/destinations`     | No            | Search the destination catalogue         |
| GET    | `/recommendations`  | Yes (JWT)     | Get personalised recommendations        |
| POST   | `/itineraries`      | Yes (JWT)     | Create a new itinerary                   |
| GET    | `/itineraries`      | Yes (JWT)     | List all itineraries for the logged-in user |

Protected routes expect the header:  
`Authorization: Bearer <your-token>`

### Example requests

```bash
# Register
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "s3cr3t", "preferences": ["beach", "food"]}'

# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "s3cr3t"}'
# Save the returned token: TOKEN=<value from .token field>

# Search destinations
curl "http://localhost:5000/destinations?tag=beach&max_cost=100"

# Personalised recommendations
curl http://localhost:5000/recommendations \
  -H "Authorization: Bearer $TOKEN"

# Create an itinerary
curl -X POST http://localhost:5000/itineraries \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Beach Escape", "destinations": ["Bali"], "start_date": "2025-07-01", "end_date": "2025-07-14"}'

# List itineraries
curl http://localhost:5000/itineraries \
  -H "Authorization: Bearer $TOKEN"
```

---

## Running Locally

### Prerequisites
- Python 3.9+
- pip

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app/main.py
```

The API will be available at `http://localhost:5000`.

---

## Running with Docker

```bash
# Build and start
docker-compose up --build

# Stop
docker-compose down
```

The `data/` directory is mounted into the container, so JSON files persist between runs.

---

## Data Storage

All data is persisted in plain JSON files inside the `data/` directory:

| File                    | Purpose                              |
|-------------------------|--------------------------------------|
| `data/destinations.json`| Static catalogue of travel destinations (seed data) |
| `data/users.json`       | Registered users (created at runtime) |
| `data/itineraries.json` | User itineraries (created at runtime) |

> **Note:** `data/*.json` (except `destinations.json`) are excluded from version control via `.gitignore`.

---

## Configuration

| Environment Variable | Default                              | Description           |
|----------------------|--------------------------------------|-----------------------|
| `SECRET_KEY`         | `globetrotter-secret-change-in-prod` | JWT signing key – **must be overridden in production** |
| `FLASK_DEBUG`        | `0`                                  | Set to `1` to enable Flask debug mode (development only) |
| `PORT`               | `5000`                               | Port the app listens on |

> **Important:** Always set `SECRET_KEY` to a long, random value in production (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).


------------------------------------------

# 📚 Additional Documentation (phase 1)

The backend has been progressively refactored from the original monolithic architecture into a layered architecture.

The project documentation is available in the **docs** directory.

| Document | Description |
|-----------|-------------|
| [Project Overview](docs/proj_overview.md) | Vision, objectives and roadmap |
| [Architecture](docs/architecture.md) | Layered backend architecture |
| [Refactoring History](docs/refactoringHistory.md) | Evolution from monolith to layered architecture |
| [API Documentation](docs/API.md) | REST API reference |

-------------------------------------------------------------------------------------------------------------
# 📚 microservices architecture Documentation (phase 2)

This backend is a refactor of the original Flask monolith into
independent microservices, reusing the monolith's layering
(Route -> Service -> Repository -> Validators, standardized JSON
responses, JWT auth) in every service rather than starting over.

## Architecture

```
                         ┌────────────────────┐
   Next.js Frontend ───► │    API Gateway      │  (port 5000, public)
   (unchanged)           │  thin reverse proxy  │
                         └──────────┬───────────┘
                                    │
        ┌──────────────┬───────────┼───────────┬──────────────┬──────────────┐
        ▼              ▼           ▼           ▼              ▼              ▼
  ┌───────────┐  ┌───────────┐ ┌────────────┐ ┌──────────────┐ ┌───────────┐ ┌───────────┐
  │   Auth    │  │   User    │ │Destination │ │Recommendation│ │ Itinerary │ │   Admin   │
  │  Service  │  │  Service  │ │  Service   │ │   Service    │ │  Service  │ │  Service  │
  │  :5001    │  │  :5002    │ │   :5003    │ │    :5004     │ │  :5005    │ │  :5006    │
  └─────┬─────┘  └─────┬─────┘ └──────┬─────┘ └──────┬───────┘ └─────┬─────┘ └─────┬─────┘
        │              │              │              │               │             │
     users.json  user_profiles.json destinations.json  (no data,   itineraries.json (no data,
                                                       calls other              aggregates
                                                        services)               via HTTP)

  Shared Infrastructure: common/ (responses, JWT+RBAC, storage abstraction,
  password hashing, exceptions) -- copied into every service's Docker build.
```

Every service is independently deployable, has its own
`routes/ services/ repositories/ validators/ config.py Dockerfile
requirements.txt README.md`, and owns its own slice of data. Services
talk to each other over plain HTTP (via small `clients/` HTTP
wrappers), never by reaching into another service's storage.

| Service | Port | Owns | Depends on |
|---|---|---|---|
| **API Gateway** | 5000 | routing table only | all services (proxies to them) |
| **Auth Service** | 5001 | `users.json` (credentials) | User Service (best-effort profile init) |
| **User Service** | 5002 | `user_profiles.json` (preferences, favorites) | -- |
| **Destination Service** | 5003 | `destinations.json` | -- |
| **Recommendation Service** | 5004 | nothing (stateless) | User Service, Destination Service |
| **Itinerary Service** | 5005 | `itineraries.json`, Google Maps integration | Destination Service |
| **Admin Service** | 5006 | nothing (stateless, dashboard aggregator) | User/Destination/Itinerary Services |

## Why this split

- **Admin vs. user APIs are fully separated** by URL prefix
  (`/api/admin/*` vs. the rest) and by JWT role (RBAC via
  `common.jwt_utils.require_role("admin")`), matching the frontend's
  two distinct interfaces.
- **The admin never creates itineraries** -- only destinations. The
  Itinerary Service always generates routes automatically from the
  visitor's position + a chosen destination.
- **No business logic is duplicated.** For example, "reached
  destination" tracking (impressions, ratings, dates, route used,
  WhatsApp sharing) lives only in the Itinerary Service, even though
  it's user-facing history -- because it's generated together with
  the route itself. The User Service owns only preferences and
  favorites.
- **JSON storage today, PostgreSQL-ready tomorrow.** Every repository
  talks to `common/storage/base_storage.py`'s `BaseStorage`
  interface, currently implemented by `JSONStorage`. A future
  `PostgresStorage` implementing the same interface can be swapped in
  via configuration alone -- no Service or Route code changes.
- **The Recommendation engine is pluggable.** Each scoring factor
  (preference match, rating, popularity, budget fit, proximity) is an
  independent function in `recommendation-service/services/engine/
  scorers.py`. Adding a future AI/ML-based scorer means registering
  one new function -- see that service's README.

## Running locally (Docker Compose)

```bash
cp .env.example .env   # edit JWT_SECRET_KEY, INTERNAL_SERVICE_KEY, admin creds
docker compose up --build
# or: ./scripts/dev-up.sh

curl http://localhost:5000/health   # aggregate health of every service
```

The frontend (already built, unmodified) should point at
`http://localhost:5000` (or wherever the gateway is deployed) as its
single API base URL.

## Running a single service without Docker

```bash
cd auth-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp -r ../common .            # only needed outside Docker, where the
                              # build-time COPY doesn't happen for you
JWT_SECRET_KEY=dev python app.py
```

## Documentation map

- **This file** -- overall architecture, run instructions.
- **`<service>/README.md`** -- endpoints, env vars, and responsibilities
  for that specific service.
- **`openapi/openapi.yaml`** -- OpenAPI 3.0 spec for the full public
  API surface as exposed by the API Gateway (import into Swagger UI /
  Postman / Insomnia).
- **`k8s/README.md`** -- how to deploy to Kubernetes, and what's still
  needed for a production cluster.
- **`docker-compose.yml`** -- local/single-host orchestration, with
  healthchecks, a shared Docker network, and named volumes for every
  service's JSON storage.

## Authentication & RBAC

- JWT access tokens (24h) + refresh tokens (30d), both HS256, signed
  with a `JWT_SECRET_KEY` shared by every service (`common/jwt_utils.py`).
  Token payload carries `role` (`user` or `admin`), so any service can
  enforce RBAC locally with `@require_auth` / `@require_role("admin")`
  without calling another service.
- Admin credentials are a single constant account for now
  (`ADMIN_EMAIL` / `ADMIN_PASSWORD`), per the current requirements --
  `auth-service/README.md` notes where to extend this to real admin
  onboarding later.
- Passwords are hashed with Werkzeug's `generate_password_hash`
  (unchanged from the monolith).

## Google Maps integration & fallback

The Itinerary Service wraps Directions, Distance Matrix, Geocoding and
Places Nearby (`itinerary-service/services/maps/google_maps_client.py`).
If `GOOGLE_MAPS_API_KEY` is unset, the `googlemaps` package isn't
installed, or any call fails, the service automatically falls back to
a generated textual itinerary (`.../maps/fallback_generator.py`) --
the "MODE SANS GOOGLE MAPS" behaviour from the spec. A walk/moto/taxi
comparison is always produced, using Google's road distance when
available and straight-line distance otherwise.

## What's intentionally out of scope for this pass

- Real PostgreSQL implementation (the abstraction is ready; the
  concrete `PostgresStorage` class is not written).
- A message broker / event bus for service-to-service notifications
  (the one place this matters today -- Auth Service notifying User
  Service on registration -- uses a simple best-effort synchronous
  HTTP call instead).
- Real WhatsApp Business API sending -- the share endpoint returns a
  `wa.me` deep link the visitor taps to share themselves, which needs
  no API key or approval process.
- Rate limiting, API keys for third-party consumers, and full
  observability (structured logs exist per-service via Flask/Gunicorn;
  distributed tracing does not).
