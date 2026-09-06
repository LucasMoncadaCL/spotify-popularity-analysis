"""Carga, contrato, metadatos e integridad de datos."""

from spotify_popularity.data.loader import load_raw_dataset, prepare_base_dataset
from spotify_popularity.data.preparation import PreparationSummary, prepare_modeling_dataset
from spotify_popularity.data.schema import REQUIRED_COLUMNS, validate_schema

__all__ = [
    "REQUIRED_COLUMNS",
    "PreparationSummary",
    "load_raw_dataset",
    "prepare_base_dataset",
    "prepare_modeling_dataset",
    "validate_schema",
]
