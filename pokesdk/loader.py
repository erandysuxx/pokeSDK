"""
PokéSDK - Loader Module
Handles all data loading (L in ETL): exporting DataFrames to CSV, JSON,
Parquet, or an in-memory structure.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def to_csv(df: pd.DataFrame, path: str | Path, **kwargs) -> Path:
    """
    Save DataFrame to CSV.

    Args:
        df:     Transformed DataFrame.
        path:   Destination file path.
        **kwargs: Extra arguments forwarded to pd.DataFrame.to_csv().

    Returns:
        Resolved Path of the written file.
    """
    dest = Path(path).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    kwargs.setdefault("index", False)
    df.to_csv(dest, **kwargs)
    print(f"[LOADER] CSV saved → {dest}")
    return dest


def to_json(df: pd.DataFrame, path: str | Path, **kwargs) -> Path:
    """
    Save DataFrame to JSON (records orientation by default).

    Args:
        df:     Transformed DataFrame.
        path:   Destination file path.
        **kwargs: Extra arguments forwarded to pd.DataFrame.to_json().

    Returns:
        Resolved Path of the written file.
    """
    dest = Path(path).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    kwargs.setdefault("orient", "records")
    kwargs.setdefault("indent", 2)
    kwargs.setdefault("force_ascii", False)
    df.to_json(dest, **kwargs)
    print(f"[LOADER] JSON saved → {dest}")
    return dest


def to_parquet(df: pd.DataFrame, path: str | Path, **kwargs) -> Path:
    """
    Save DataFrame to Parquet.

    Args:
        df:     Transformed DataFrame.
        path:   Destination file path.
        **kwargs: Extra arguments forwarded to pd.DataFrame.to_parquet().

    Returns:
        Resolved Path of the written file.
    """
    dest = Path(path).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    kwargs.setdefault("index", False)
    df.to_parquet(dest, **kwargs)
    print(f"[LOADER] Parquet saved → {dest}")
    return dest


def to_records(df: pd.DataFrame) -> list[dict]:
    """
    Return the DataFrame as a list of plain Python dicts (no file I/O).

    Useful for in-memory pipelines or further processing.
    """
    return df.to_dict(orient="records")
