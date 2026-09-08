"""
Individual scoring functions ("scorers").

Each scorer takes a destination dict + a context dict and returns a
float in roughly [0, 1]. The engine (engine.py) combines them with
configurable weights. This is the extension point for a future
AI/ML-based recommender: add a new scorer function here (e.g. one
backed by a trained model or an LLM call), register it in
`SCORER_REGISTRY`, and give it a weight in config.WEIGHTS -- nothing
else in the service has to change.
"""


def preference_match_scorer(destination: dict, context: dict) -> float:
    preferences = context.get("preferences") or []
    if not preferences:
        return 0.5  # neutral when we don't know the user's tastes yet
    tags = [t.lower() for t in destination.get("tags", [])]
    preferences = [p.lower() for p in preferences]
    if not tags:
        return 0.0
    matches = sum(1 for p in preferences if p in tags or p == destination.get("category", "").lower())
    return min(1.0, matches / max(1, len(preferences)))


def rating_scorer(destination: dict, context: dict) -> float:
    rating = destination.get("rating") or 0
    return max(0.0, min(1.0, rating / 5.0))


def popularity_scorer(destination: dict, context: dict) -> float:
    popularity = destination.get("popularity") or 0
    return max(0.0, min(1.0, popularity / 100.0))


def budget_fit_scorer(destination: dict, context: dict) -> float:
    max_budget = context.get("max_budget")
    if max_budget is None:
        return 0.5
    cost = destination.get("budget_estimate")
    if cost is None:
        return 0.5
    if cost <= max_budget:
        return 1.0
    overage_ratio = (cost - max_budget) / max_budget if max_budget else 1
    return max(0.0, 1.0 - overage_ratio)


def proximity_scorer(destination: dict, context: dict) -> float:
    distance_km = destination.get("distance_km")
    if distance_km is None:
        return 0.5
    # Full score within 1km, fading out to 0 by 15km.
    return max(0.0, min(1.0, 1.0 - (distance_km / 15.0)))


SCORER_REGISTRY = {
    "preference_match": preference_match_scorer,
    "rating": rating_scorer,
    "popularity": popularity_scorer,
    "budget_fit": budget_fit_scorer,
    "proximity": proximity_scorer,
}
