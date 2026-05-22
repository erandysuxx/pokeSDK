"""
PokéSDK - Transformer Module
Handles all data transformation (T in ETL): normalisation, column selection,
type casting, and DataFrame construction.
"""

from __future__ import annotations

import pandas as pd
from typing import Any, List, Optional


# ---------------------------------------------------------------------------
# Field extractors (one per logical concept)
# ---------------------------------------------------------------------------

def _extract_types(raw: dict) -> str:
    """Return type names as a comma-separated string (e.g. 'fire, flying')."""
    return ", ".join(sorted(
        slot["type"]["name"]
        for slot in raw.get("types", [])
    ))


def _extract_stats(raw: dict) -> dict[str, int]:
    """Return a flat dict of stat_name -> base_stat."""
    return {
        slot["stat"]["name"]: slot["base_stat"]
        for slot in raw.get("stats", [])
    }


def _extract_abilities(raw: dict) -> list[str]:
    """Return a list of ability names (hidden abilities flagged with *)."""
    abilities = []
    for slot in raw.get("abilities", []):
        name = slot["ability"]["name"]
        if slot.get("is_hidden"):
            name = f"{name}*"
        abilities.append(name)
    return abilities


def _extract_sprites(raw: dict) -> dict[str, str | None]:
    """Return front_default and official artwork URLs."""
    sprites = raw.get("sprites", {})
    official = (
        sprites.get("other", {})
        .get("official-artwork", {})
        .get("front_default")
    )
    return {
        "sprite_url": sprites.get("front_default"),
        "artwork_url": official,
    }


# ---------------------------------------------------------------------------
# Row builder
# ---------------------------------------------------------------------------

FIELD_MAP: dict[str, Any] = {
    "id":         lambda r: r.get("id"),
    "name":       lambda r: r.get("name"),
    "height_dm":  lambda r: r.get("height"),          # decimetres
    "weight_hg":  lambda r: r.get("weight"),          # hectograms
    "base_exp":   lambda r: r.get("base_experience"),
    "types":      _extract_types,
    "abilities":  _extract_abilities,
    **{f"stat_{k}": (lambda r, k=k: _extract_stats(r).get(k))
       for k in ["hp", "attack", "defense",
                 "special-attack", "special-defense", "speed"]},
    "sprite_url": lambda r: _extract_sprites(r)["sprite_url"],
    "artwork_url": lambda r: _extract_sprites(r)["artwork_url"],
}


def transform_pokemon(raw: dict, fields: list[str] | None = None) -> dict:
    """
    Flatten a single raw API response into a normalised dict.

    Args:
        raw:    Raw dict returned by the extractor.
        fields: Optional allowlist of field names. Defaults to all fields.

    Returns:
        Flat dict ready to be used as a DataFrame row.
    """
    selected = fields if fields else list(FIELD_MAP)
    return {
        field: FIELD_MAP[field](raw)
        for field in selected
        if field in FIELD_MAP
    }


def transform_batch(
    raw_list: list[dict],
    fields: list[str] | None = None,
) -> pd.DataFrame:
    """
    Transform a list of raw API responses into a pandas DataFrame.

    Args:
        raw_list: Output of extractor.get_pokemon_batch().
        fields:   Optional column allowlist.

    Returns:
        pd.DataFrame with one row per Pokémon.
    """
    rows = [transform_pokemon(raw, fields=fields) for raw in raw_list]
    df = pd.DataFrame(rows)

    # Friendly column ordering: id first, name second
    priority = ["id", "name"]
    cols = priority + [c for c in df.columns if c not in priority]
    return df[[c for c in cols if c in df.columns]]
