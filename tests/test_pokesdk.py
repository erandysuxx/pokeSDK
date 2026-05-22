"""
Unit tests for PokéSDK using mock HTTP responses.
Run with: pytest tests/
"""
 
import pytest
import responses as resp_mock
import requests
 
from pokesdk.extractor import get_pokemon, get_pokemon_batch, PokemonNotFoundError, PokeAPIError
from pokesdk.transformer import transform_pokemon, transform_batch
from pokesdk.loader import to_records
 
 
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
 
PIKACHU_RAW = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "base_experience": 112,
    "types": [{"slot": 1, "type": {"name": "electric", "url": ""}}],
    "abilities": [
        {"ability": {"name": "static", "url": ""}, "is_hidden": False},
        {"ability": {"name": "lightning-rod", "url": ""}, "is_hidden": True},
    ],
    "stats": [
        {"base_stat": 35, "stat": {"name": "hp"}},
        {"base_stat": 55, "stat": {"name": "attack"}},
        {"base_stat": 40, "stat": {"name": "defense"}},
        {"base_stat": 50, "stat": {"name": "special-attack"}},
        {"base_stat": 50, "stat": {"name": "special-defense"}},
        {"base_stat": 90, "stat": {"name": "speed"}},
    ],
    "sprites": {
        "front_default": "https://sprites/pikachu.png",
        "other": {"official-artwork": {"front_default": "https://art/pikachu.png"}},
    },
}
 
 
# ---------------------------------------------------------------------------
# Extractor tests
# ---------------------------------------------------------------------------
 
@resp_mock.activate
def test_get_pokemon_success():
    resp_mock.add(
        resp_mock.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu/",
        json=PIKACHU_RAW,
        status=200,
    )
    data = get_pokemon("pikachu")
    assert data["id"] == 25
 
 
@resp_mock.activate
def test_get_pokemon_not_found():
    resp_mock.add(
        resp_mock.GET,
        "https://pokeapi.co/api/v2/pokemon/fakemon/",
        status=404,
    )
    with pytest.raises(PokemonNotFoundError):
        get_pokemon("fakemon")
 
 
@resp_mock.activate
def test_get_pokemon_server_error():
    resp_mock.add(
        resp_mock.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu/",
        status=500,
    )
    with pytest.raises(PokeAPIError):
        get_pokemon("pikachu")
 
 
@resp_mock.activate
def test_get_pokemon_batch_skip_errors():
    resp_mock.add(
        resp_mock.GET,
        "https://pokeapi.co/api/v2/pokemon/pikachu/",
        json=PIKACHU_RAW,
        status=200,
    )
    resp_mock.add(
        resp_mock.GET,
        "https://pokeapi.co/api/v2/pokemon/fakemon/",
        status=404,
    )
    results = get_pokemon_batch(["pikachu", "fakemon"], skip_errors=True)
    assert len(results) == 1
    assert results[0]["name"] == "pikachu"
 
 
# ---------------------------------------------------------------------------
# Transformer tests
# ---------------------------------------------------------------------------
 
def test_transform_pokemon_fields():
    row = transform_pokemon(PIKACHU_RAW)
    assert row["id"] == 25
    assert row["name"] == "pikachu"
    assert row["types"] == "electric"
    assert "lightning-rod*" in row["abilities"]
    assert row["stat_hp"] == 35
    assert row["stat_speed"] == 90
 
 
def test_transform_pokemon_field_filter():
    row = transform_pokemon(PIKACHU_RAW, fields=["id", "name"])
    assert set(row.keys()) == {"id", "name"}
 
 
def test_transform_batch_returns_dataframe():
    import pandas as pd
    df = transform_batch([PIKACHU_RAW])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "id" in df.columns
    assert df.iloc[0]["name"] == "pikachu"
 
 
# ---------------------------------------------------------------------------
# Loader tests
# ---------------------------------------------------------------------------
 
def test_to_records():
    import pandas as pd
    df = transform_batch([PIKACHU_RAW])
    records = to_records(df)
    assert isinstance(records, list)
    assert records[0]["name"] == "pikachu"