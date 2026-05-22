"""
PokéSDK - Extractor Module
Handles all data extraction (E in ETL) from the PokéAPI.
"""
 
import requests
from typing import Dict, List, Optional
 
 
BASE_URL = "https://pokeapi.co/api/v2"
 
# Rangos de IDs por generación (inicio, fin inclusive)
GENERATIONS: Dict[int, tuple] = {
    1: (1,   151),
    2: (152, 251),
    3: (252, 386),
    4: (387, 493),
    5: (494, 649),
    6: (650, 721),
    7: (722, 809),
    8: (810, 905),
    9: (906, 1025),
}
 
 
class PokeAPIError(Exception):
    """Raised when the PokéAPI returns an unexpected response."""
    pass
 
 
class PokemonNotFoundError(PokeAPIError):
    """Raised when a Pokémon is not found (404)."""
    pass
 
 
def get_generation_names(generation: int = 1) -> List[str]:
    """
    Fetch the list of Pokémon names for a given generation.
 
    Args:
        generation: Generation number (1–9). Defaults to 1 (Kanto).
 
    Returns:
        List of Pokémon names in Pokédex order.
 
    Raises:
        ValueError: If the generation number is not between 1 and 9.
        PokeAPIError: If the API returns an unexpected response.
    """
    if generation not in GENERATIONS:
        raise ValueError(
            f"Invalid generation '{generation}'. Choose a number from 1 to 9."
        )
 
    start, end = GENERATIONS[generation]
    limit = end - start + 1
    offset = start - 1
 
    url = f"{BASE_URL}/pokemon?limit={limit}&offset={offset}"
    response = requests.get(url, timeout=10)
 
    if response.status_code != 200:
        raise PokeAPIError(
            f"Failed to fetch generation {generation} list "
            f"(status {response.status_code})."
        )
 
    data = response.json()
    return [pokemon["name"] for pokemon in data["results"]]
 
 
def get_pokemon(pokemon_name: str, session: Optional[requests.Session] = None) -> dict:
    """
    Fetch raw data for a single Pokémon from the PokéAPI.
 
    Args:
        pokemon_name: Name or ID of the Pokémon (case-insensitive).
        session: Optional requests.Session for connection reuse.
 
    Returns:
        dict: Full JSON response from the API.
 
    Raises:
        PokemonNotFoundError: If the Pokémon does not exist.
        PokeAPIError: For any other non-200 response.
        requests.RequestException: For network/connection errors.
    """
    url = f"{BASE_URL}/pokemon/{pokemon_name.strip().lower()}/"
    requester = session or requests
 
    response = requester.get(url, timeout=10)
 
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise PokemonNotFoundError(f"Pokémon '{pokemon_name}' not found.")
    else:
        raise PokeAPIError(
            f"Unexpected status {response.status_code} for '{pokemon_name}'."
        )
 
 
def get_pokemon_batch(
    pokemon_names: List[str],
    skip_errors: bool = True,
) -> List[dict]:
    """
    Fetch raw data for multiple Pokémon, reusing a single HTTP session.
 
    Args:
        pokemon_names: List of Pokémon names or IDs.
        skip_errors: If True, failed requests are skipped with a warning.
                     If False, the first error raises an exception.
 
    Returns:
        List of raw API response dicts (one per successful request).
    """
    results = []
 
    with requests.Session() as session:
        for name in pokemon_names:
            try:
                data = get_pokemon(name, session=session)
                results.append(data)
            except (PokeAPIError, requests.RequestException) as exc:
                if skip_errors:
                    print(f"[WARNING] Skipping '{name}': {exc}")
                else:
                    raise
 
    return results