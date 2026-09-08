# Recommendation Service

Generates personalised recommendations from preferences, rating,
popularity, budget and distance. Calls the **User Service** (for the
caller's preferences) and the **Destination Service** (for the
candidate destinations) over HTTP -- it stores no data itself.

## Endpoint

| Method | Path                     | Auth   | Description |
|--------|---------------------------|--------|--------------|
| GET    | `/api/recommendations`    | Bearer | Query params: `limit` (default 5), `lat`, `lng` |
| GET    | `/health`                 | none   | Liveness/readiness probe |

## Scoring engine

`services/engine/engine.py` + `services/engine/scorers.py` implement a
small, pluggable weighted-scoring engine (`RecommendationEngine`).
Each factor (preference match, rating, popularity, budget fit,
proximity) is an independent function in `SCORER_REGISTRY`, combined
via weights in `config.WEIGHTS` (overridable by env vars). To plug in
a future ML/AI-based recommender, add a new scorer function and
register it -- the rest of the service is unchanged.
