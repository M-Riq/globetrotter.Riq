"""
Recommendation Engine.

Combines pluggable scorers with configurable weights into a single
ranked list. Deliberately storage- and transport-agnostic: it only
needs destinations + context dicts, so it doesn't care whether the
destinations came from JSON files today or PostgreSQL / a search
index tomorrow.
"""
from services.engine.scorers import SCORER_REGISTRY


class RecommendationEngine:
    def __init__(self, weights: dict, scorer_registry: dict = None):
        self.weights = weights
        self.scorers = scorer_registry or SCORER_REGISTRY

    def rank(self, destinations: list, context: dict, limit: int = 5) -> list:
        scored = []
        for destination in destinations:
            total = 0.0
            breakdown = {}
            for name, weight in self.weights.items():
                scorer = self.scorers.get(name)
                if not scorer:
                    continue
                component = scorer(destination, context)
                breakdown[name] = round(component, 3)
                total += component * weight

            item = dict(destination)
            item["match_score"] = round(total, 3)
            item["score_breakdown"] = breakdown
            scored.append(item)

        scored.sort(key=lambda d: (-d["match_score"], d.get("name", "")))
        return scored[:limit]
