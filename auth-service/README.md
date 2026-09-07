# Auth Service

Handles registration, login (user + admin), token issuance, and
token refresh for all of GlobeTrotter. Owns `users.json`
(credentials only -- profile data lives in the **User Service**).

## Endpoints

| Method | Path                     | Auth  | Description                        |
|--------|--------------------------|-------|-------------------------------------|
| POST   | `/api/auth/register`     | none  | Register a new visitor account      |
| POST   | `/api/auth/login`        | none  | Log in, returns access+refresh JWT  |
| POST   | `/api/auth/admin/login`  | none  | Admin login (constant credentials)  |
| POST   | `/api/auth/refresh`      | none  | Exchange a refresh token for a new access token |
| GET    | `/api/auth/verify`       | Bearer| Validate a token, returns its payload |
| GET    | `/health`                | none  | Liveness/readiness probe            |

## Environment variables

| Var               | Default                    | Notes                              |
|--------------------|----------------------------|-------------------------------------|
| `PORT`             | `5001`                     |                                      |
| `JWT_SECRET_KEY`   | `dev-secret-change-me`     | **Must be identical across every service** |
| `DATA_DIR`         | `./data`                   | JSON storage directory              |
| `ADMIN_EMAIL`      | `admin@globetrotter.cm`    | Single constant admin account       |
| `ADMIN_PASSWORD`   | `ChangeMe123!`              | Change in production via secrets    |
| `CORS_ORIGINS`     | `*`                        |                                      |

## Run locally

```bash
pip install -r requirements.txt
cp -r ../common .   # only needed if running outside Docker
PORT=5001 python app.py
```

## Run via Docker (from repo root)
```bash
docker compose up --build auth-service
```
