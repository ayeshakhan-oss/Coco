"""What a screening run costs, in dollars.

Coco had token counts before this module (`AnthropicDrafter._record` captures
input, output and both cache figures per call) but no price table anywhere, so
nothing could answer "what will this run cost" before spending it.

🔴 THESE RATES ARE NOT REMEMBERED. They come from the `claude-api` skill's
model table (cached 2026-06-24), which is the same source the screenshots'
"$1/$5 per million tokens" line for Haiku 4.5 agrees with. CLAUDE.md Rule 1:
no guessing. When a rate here is stale the fix is to re-read that table, not
to adjust a number until a total looks plausible.

An estimate is an estimate. `estimate_run_cost` works from character counts
because counting real tokens would mean an API round trip per candidate before
the run has been approved, which is the thing the estimate exists to avoid. The
run's `cost_cap_usd` and its recorded `actual_cost_usd` are the real controls,
and the wizard says so on the page rather than implying the estimate is a
quote.
"""

from __future__ import annotations

from typing import Optional

# USD per million tokens. Input and output are published rates; the two cache
# multipliers are the documented ratios against the input rate (a cache read is
# about a tenth of an input token, a cache write about 1.25x).
_PER_MTOK = {
    "claude-opus-5": (5.00, 25.00),
    "claude-opus-4-8": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
}

CACHE_READ_MULTIPLIER = 0.1
CACHE_WRITE_MULTIPLIER = 1.25

# The Batch API runs asynchronously at half price.
BATCH_DISCOUNT = 0.5

_MILLION = 1_000_000


class UnknownModelPrice(KeyError):
    """No published rate for this model id."""


def _rates(model: str) -> tuple[float, float]:
    """Resolve a model id to (input, output) per-MTok rates.

    Production runs `claude-haiku-4-5-20251001`, a dated variant of a table
    entry, so an exact-match-only lookup would fail on the one model the app
    actually uses. Longest prefix wins, so a future dated id resolves without
    an edit here, and an id that matches nothing raises rather than silently
    costing $0.00 -- a run that reports zero spend is exactly how three earlier
    runs hid the fact that they had failed (actual_cost_usd 0.000000 on 369
    failed items).
    """
    if not model:
        raise UnknownModelPrice("no model id given")
    candidates = [k for k in _PER_MTOK if model.startswith(k)]
    if not candidates:
        raise UnknownModelPrice(
            f"no published price for model {model!r}. Add it from the claude-api "
            "skill's model table rather than guessing a rate."
        )
    return _PER_MTOK[max(candidates, key=len)]


def cost_usd(
    *,
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_creation_tokens: int = 0,
    batch: bool = False,
) -> float:
    """Actual cost of one call from its recorded token usage.

    `input_tokens` from the API already EXCLUDES cached tokens, which are
    reported separately, so these four are added rather than netted off.
    """
    rate_in, rate_out = _rates(model)
    total = (
        (input_tokens or 0) * rate_in
        + (output_tokens or 0) * rate_out
        + (cache_read_tokens or 0) * rate_in * CACHE_READ_MULTIPLIER
        + (cache_creation_tokens or 0) * rate_in * CACHE_WRITE_MULTIPLIER
    ) / _MILLION
    if batch:
        total *= BATCH_DISCOUNT
    return round(total, 6)


def cost_of_call(row: dict, *, batch: bool = False) -> float:
    """One row from `AnthropicDrafter.calls` to dollars.

    That dict uses `cache_read`/`cache_write`; the API uses
    `cache_read_input_tokens`/`cache_creation_input_tokens`. Accept either so
    a caller holding raw usage does not have to rename fields first.
    """
    return cost_usd(
        model=row.get("model") or "",
        input_tokens=row.get("input_tokens") or 0,
        output_tokens=row.get("output_tokens") or 0,
        cache_read_tokens=row.get("cache_read")
        or row.get("cache_read_input_tokens")
        or 0,
        cache_creation_tokens=row.get("cache_write")
        or row.get("cache_creation_input_tokens")
        or 0,
        batch=batch,
    )


# Rough characters per token for English prose. Used ONLY for the pre-run
# estimate; every recorded cost comes from real usage.
CHARS_PER_TOKEN = 4

# What one screened candidate is expected to emit. The output schema is a fixed
# shape (5 dimension scores with evidence, strengths, gaps, filter flags,
# verdict), so this varies far less than the input does.
EST_OUTPUT_TOKENS_PER_CANDIDATE = 900


def estimate_run_cost(
    *,
    model: str,
    candidates: int,
    system_prompt_chars: int,
    avg_cv_chars: int,
    batch: bool = False,
) -> dict:
    """Estimate a whole run before it is launched.

    The rubric's system prompt is identical for every candidate in the run and
    is sent under `cache_control`, so after the first call it bills at the
    cache-read rate. That is most of the saving the wizard reports, and it is
    the reason the estimate is not simply candidates x full prompt.
    """
    if candidates <= 0:
        return {
            "candidates": 0,
            "est_input_tokens": 0,
            "est_cached_tokens": 0,
            "est_output_tokens": 0,
            "est_cost_usd": 0.0,
            "uncached_cost_usd": 0.0,
            "cache_saving_usd": 0.0,
            "batch_saving_usd": 0.0,
        }

    system_tokens = max(1, system_prompt_chars // CHARS_PER_TOKEN)
    cv_tokens = max(1, avg_cv_chars // CHARS_PER_TOKEN)
    output_tokens = EST_OUTPUT_TOKENS_PER_CANDIDATE * candidates

    # First call writes the cache, the rest read it.
    cache_write = system_tokens
    cache_read = system_tokens * (candidates - 1)
    fresh_input = cv_tokens * candidates

    est = cost_usd(
        model=model,
        input_tokens=fresh_input,
        output_tokens=output_tokens,
        cache_read_tokens=cache_read,
        cache_creation_tokens=cache_write,
        batch=batch,
    )
    # What the same run would cost sending the full prompt every time.
    uncached = cost_usd(
        model=model,
        input_tokens=fresh_input + system_tokens * candidates,
        output_tokens=output_tokens,
        batch=batch,
    )
    unbatched = est if not batch else est / BATCH_DISCOUNT
    return {
        "candidates": candidates,
        "est_input_tokens": fresh_input,
        "est_cached_tokens": cache_read + cache_write,
        "est_output_tokens": output_tokens,
        "est_cost_usd": est,
        "uncached_cost_usd": uncached,
        "cache_saving_usd": round(max(0.0, uncached - est), 6),
        "batch_saving_usd": round(max(0.0, unbatched - est), 6) if batch
        else round(unbatched * (1 - BATCH_DISCOUNT), 6),
    }


def price_table() -> list[dict]:
    """What the wizard's model picker shows. Ordered cheapest first, which is
    also least to most capable, so the default sits at the top."""
    order = [
        ("claude-haiku-4-5", "Claude Haiku 4.5"),
        ("claude-sonnet-5", "Claude Sonnet 5"),
        ("claude-opus-5", "Claude Opus 5"),
    ]
    out = []
    for model_id, label in order:
        rate_in, rate_out = _PER_MTOK[model_id]
        out.append(
            {
                "model": model_id,
                "label": label,
                "input_per_mtok": rate_in,
                "output_per_mtok": rate_out,
            }
        )
    return out


def known_models() -> list[str]:
    return sorted(_PER_MTOK)


def price_for(model: str) -> Optional[tuple[float, float]]:
    try:
        return _rates(model)
    except UnknownModelPrice:
        return None
