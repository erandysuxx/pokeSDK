"""
PokéSDK - Pipeline
High-level orchestrator that wires Extract -> Transform -> Load together.
"""
 
from __future__ import annotations
 
from pathlib import Path
from typing import List, Literal, Optional, Union
 
import pandas as pd
 
from .extractor import get_pokemon_batch, get_generation_names
from .transformer import transform_batch
from . import loader as _loader
 
 
OutputFormat = Literal["csv", "json", "parquet", "records", "dataframe"]
 
 
def run_generation(
    generation: int = 1,
    fields: Optional[List[str]] = None,
    output_format: OutputFormat = "dataframe",
    output_path: Optional[Union[str, Path]] = None,
    skip_errors: bool = True,
) -> Union[pd.DataFrame, List[dict], Path]:
    """
    Run the full ETL pipeline for an entire Pokemon generation.
 
    Args:
        generation:     Generation number (1-9). Defaults to 1 (Kanto, 151 Pokemon).
        fields:         Columns to keep (None = all).
        output_format:  One of 'csv', 'json', 'parquet', 'records', 'dataframe'.
        output_path:    Required when output_format is a file format.
        skip_errors:    Skip Pokemon that fail to fetch (True) or raise (False).
 
    Example::
 
        df = pokesdk.run_generation(1)
        pokesdk.run_generation(2, output_format='csv', output_path='gen2.csv')
    """
    names = get_generation_names(generation)
    print(f"[INFO] Fetching {len(names)} Pokemon from generation {generation}...")
    return run(
        names,
        fields=fields,
        output_format=output_format,
        output_path=output_path,
        skip_errors=skip_errors,
    )
 
 
def run(
    pokemon_names: List[str],
    fields: Optional[List[str]] = None,
    output_format: OutputFormat = "dataframe",
    output_path: Optional[Union[str, Path]] = None,
    skip_errors: bool = True,
) -> Union[pd.DataFrame, List[dict], Path]:
    """
    Run the full ETL pipeline for a custom list of Pokemon.
 
    Args:
        pokemon_names:  Names or IDs to fetch.
        fields:         Columns to keep (None = all).
        output_format:  One of 'csv', 'json', 'parquet', 'records', 'dataframe'.
        output_path:    Required when output_format is a file format.
        skip_errors:    Skip Pokemon that fail to fetch (True) or raise (False).
    """
    # --- Extract ---
    raw_list = get_pokemon_batch(pokemon_names, skip_errors=skip_errors)
 
    # --- Transform ---
    df = transform_batch(raw_list, fields=fields)
 
    # --- Load ---
    if output_format == "dataframe":
        return df
 
    if output_format == "records":
        return _loader.to_records(df)
 
    if output_path is None:
        raise ValueError(
            f"output_path is required when output_format='{output_format}'."
        )
 
    dispatch = {
        "csv":     _loader.to_csv,
        "json":    _loader.to_json,
        "parquet": _loader.to_parquet,
    }
 
    if output_format not in dispatch:
        raise ValueError(
            f"Unknown output_format '{output_format}'. "
            f"Choose from: {list(dispatch) + ['records', 'dataframe']}"
        )
 
    return dispatch[output_format](df, output_path)