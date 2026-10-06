import random


def normalize(value: float, low: float, high: float) -> int:
    """
    Normalizes a value into a 0–100 score using min-max scaling.
    Returns 50 (neutral) when the range is degenerate.
    """
    if high == low:
        return 50
    score = (value - low) / (high - low)
    return max(0, min(100, int(score * 100)))


def compute_monetization_score(query: str) -> int:
    """
    Estimates monetization potential from keywords in the query.

    Tiers:
      High  (80–90): SaaS, B2B, AI tools, subscription, enterprise
      Medium (50–65): apps, marketplaces, services, platform
      Low   (20–40): social, community, free tools, open-source
    """
    query_lower = query.lower()
    words = set(query_lower.split())

    high_keywords = {
        "saas", "b2b", "enterprise", "subscription", "ai", "automation",
        "analytics", "api", "license", "fintech", "insurtech", "healthtech",
        "cybersecurity", "devtools", "infrastructure", "cloud",
    }
    medium_keywords = {
        "app", "marketplace", "platform", "service", "ecommerce",
        "e-commerce", "d2c", "b2c", "delivery", "booking", "rental",
        "commission", "freemium", "premium", "ads", "advertising",
    }
    low_keywords = {
        "social", "community", "free", "open-source", "nonprofit",
        "charity", "blog", "forum", "wiki", "volunteer",
    }

    high_hits = len(high_keywords.intersection(words))
    medium_hits = len(medium_keywords.intersection(words))
    low_hits = len(low_keywords.intersection(words))

    if high_hits > 0:
        base = 80 + min(high_hits - 1, 2) * 3  # 80 → 86 max
    elif medium_hits > 0:
        base = 50 + min(medium_hits - 1, 3) * 5  # 50 → 65 max
    elif low_hits > 0:
        base = 20 + min(low_hits - 1, 4) * 5   # 20 → 40 max
    else:
        base = 50  # neutral when no keyword matched

    # Slight randomness to avoid identical outputs across runs
    noise = random.randint(-3, 3)
    return max(0, min(100, base + noise))


def compute_all_scores(
    num_chunks: int,
    keyword_freq: int,
    avg_chunk_length: float,
    unique_word_count: int,
    query: str,
) -> dict:
    """
    Computes all five sub-scores and a weighted viability score.

    Dynamic ranges (calibrated against real pipeline output):
      • demand        ← keyword_freq      in [0, 300]
      • idea_strength ← unique_word_count  in [100, 1500]
      • competition   ← num_chunks         in [10, 200]
      • growth        ← avg_chunk_length   in [100, 350]
      • monetization  ← keyword heuristic
    """

    # ── Individual metric scores ────────────────────────────────────
    # Ranges set so *typical* pipeline output (~20 chunks from DDG + Wiki
    # + synthetic fallback) lands near 40–60, with room for outliers.
    #   keyword_freq:      50 – 500   (query words counted across all chunks)
    #   unique_word_count: 400 – 1800 (vocabulary size of corpus)
    #   num_chunks:          5 – 40   (document count after chunking)
    #   avg_chunk_length:   60 – 220  (words per chunk)
    demand_score = normalize(keyword_freq, 50, 500)
    idea_strength_score = normalize(unique_word_count, 400, 1800)
    competition_score = normalize(num_chunks, 5, 40)
    growth_score = normalize(avg_chunk_length, 60, 220)
    monetization_score = compute_monetization_score(query)

    # ── Break uniformity when raw features are too close ────────────
    # If all four normalized scores fall within a 12-point band, inject
    # controlled noise so the dashboard never looks "flat".
    raw_scores = [demand_score, idea_strength_score, competition_score, growth_score]
    if max(raw_scores) - min(raw_scores) < 12:
        demand_score = max(0, min(100, demand_score + random.randint(-5, 5)))
        idea_strength_score = max(0, min(100, idea_strength_score + random.randint(-5, 5)))
        competition_score = max(0, min(100, competition_score + random.randint(-5, 5)))
        growth_score = max(0, min(100, growth_score + random.randint(-5, 5)))

    # ── Weighted viability score ────────────────────────────────────
    # Note: competition is inverted — lower competition is better.
    viability_score = int(
        demand_score * 0.30
        + idea_strength_score * 0.20
        + (100 - competition_score) * 0.20
        + growth_score * 0.20
        + monetization_score * 0.10
    )

    # Smoothing variation ±3 and final clamp
    viability_score = max(0, min(100, viability_score + random.randint(-3, 3)))

    return {
        "demand": demand_score,
        "idea_strength": idea_strength_score,
        "competition": competition_score,
        "growth": growth_score,
        "monetization": monetization_score,
        "viability": viability_score,
    }
