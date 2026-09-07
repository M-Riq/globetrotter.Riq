# Itinerary Service

The main microservice. The admin never creates itineraries manually
-- only destinations. Itineraries are always generated automatically
from the visitor's current position + a chosen destination.

## Endpoints

| Method | Path                                | Auth   | Description |
|--------|---------------------------------------|--------|--------------|
| POST   | `/api/itineraries/generate`           | Bearer | Preview a route (not saved): `{origin_lat, origin_lng, destination_id, mode}` |
| POST   | `/api/itineraries`                    | Bearer | Save an itinerary (e.g. mark reached): adds `{status, impression, rating, reached_at}` |
| GET    | `/api/itineraries`                    | Bearer | List my itineraries + count reached |
| GET    | `/api/itineraries/<id>`               | Bearer | Get one of my itineraries |
| POST   | `/api/itineraries/<id>/share`         | Bearer | Generate a `wa.me` WhatsApp share link |
| GET    | `/health`                             | none   | Liveness/readiness; also reports `google_maps_configured` |

`mode` is one of `walking`, `moto`, `taxi` (default `walking`).

## Google Maps integration

`services/maps/google_maps_client.py` wraps Directions, Distance
Matrix, Geocoding and Places Nearby. Every call degrades to `None` on
any failure. When Google Maps is unavailable (`GOOGLE_MAPS_API_KEY`
unset, package missing, or the call fails), `services/itinerary_service.py`
automatically falls back to `services/maps/fallback_generator.py`,
which produces a step-by-step textual itinerary from straight-line
distance, exactly per the "MODE SANS GOOGLE MAPS" requirement.

`services/maps/transport_estimator.py` always returns a walk / moto /
taxi comparison (distance, duration, estimated price in FCFA), using
Google's road distance when available and haversine distance
otherwise. Price/speed assumptions live in `config.TRANSPORT_PROFILES`
and should be recalibrated against real Yaoundé fares.

## Environment variables

| Var                    | Default   | Notes |
|--------------------------|-----------|-------|
| `GOOGLE_MAPS_API_KEY`    | *(empty)* | Leave unset to always use the textual fallback |
| `DESTINATION_SERVICE_URL`| `http://destination-service:5003` | |
| `JWT_SECRET_KEY`         | shared    | Must match every other service |
