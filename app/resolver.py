from __future__ import annotations

from difflib import SequenceMatcher

from app import models


KEYWORD_CAPABILITIES = {
    "function": "tool_use",
    "tool": "tool_use",
    "calling": "tool_use",
    "agent": "software_engineering",
    "coding": "software_engineering",
    "code": "coding",
    "math": "math",
    "reasoning": "reasoning",
    "science": "expert_reasoning",
    "multimodal": "multimodal_reasoning",
    "vision": "multimodal_reasoning",
    "long context": "long_context",
    "retrieval": "long_context",
    "preference": "preference",
    "safety": "safety",
}


def normalize_text(value: str) -> str:
    return value.lower().replace("-", " ").replace("_", " ").strip()


def resolve_benchmarks(
    query: str, benchmarks: list[models.Benchmark], limit: int = 5
) -> list[dict[str, object]]:
    normalized_query = normalize_text(query)
    matches: list[dict[str, object]] = []

    for benchmark in benchmarks:
        names = [benchmark.benchmark_id, benchmark.name, *benchmark.aliases]
        normalized_names = [normalize_text(name) for name in names if name]

        exact = normalized_query in normalized_names
        if exact:
            matches.append(
                {
                    "benchmark_id": benchmark.benchmark_id,
                    "name": benchmark.name,
                    "confidence": 1.0,
                    "reason": "Exact benchmark ID, name, or alias match.",
                }
            )
            continue

        fuzzy = max(SequenceMatcher(None, normalized_query, name).ratio() for name in normalized_names)
        keyword_score = 0.0
        reason = "Fuzzy string match."
        for keyword, capability in KEYWORD_CAPABILITIES.items():
            if keyword in normalized_query and capability == benchmark.capability:
                keyword_score = max(keyword_score, 0.82)
                reason = f"Matches {benchmark.capability} capability."

        confidence = max(fuzzy * 0.8, keyword_score)
        if confidence >= 0.45:
            matches.append(
                {
                    "benchmark_id": benchmark.benchmark_id,
                    "name": benchmark.name,
                    "confidence": round(confidence, 2),
                    "reason": reason,
                }
            )

    return sorted(matches, key=lambda item: item["confidence"], reverse=True)[:limit]

