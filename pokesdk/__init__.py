"""
PokéSDK
~~~~~~~
A lightweight ETL SDK for the PokeAPI.
 
Typical usage::
 
    import pokesdk
 
    # Todos los Pokemon de la primera generacion
    df = pokesdk.run_generation(1)
 
    # Lista personalizada
    df = pokesdk.run(['pikachu', 'charmander'])
 
    # Guardar Gen 2 en CSV
    pokesdk.run_generation(2, output_format='csv', output_path='gen2.csv')
"""
 
from .extractor import (
    get_pokemon,
    get_pokemon_batch,
    get_generation_names,
    PokeAPIError,
    PokemonNotFoundError,
    GENERATIONS,
)
from .transformer import (
    transform_pokemon,
    transform_batch,
    FIELD_MAP,
)
from .loader import (
    to_csv,
    to_json,
    to_parquet,
    to_records,
)
from .pipeline import run, run_generation
 
__all__ = [
    # Extractor
    "get_pokemon",
    "get_pokemon_batch",
    "get_generation_names",
    "PokeAPIError",
    "PokemonNotFoundError",
    "GENERATIONS",
    # Transformer
    "transform_pokemon",
    "transform_batch",
    "FIELD_MAP",
    # Loader
    "to_csv",
    "to_json",
    "to_parquet",
    "to_records",
    # Pipeline
    "run",
    "run_generation",
]
 
__version__ = "0.2.0"