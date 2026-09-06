"""Carga y preparación base del dataset Spotify Tracks."""

from pathlib import Path

import pandas as pd

from spotify_popularity.config import PROJECT_PATHS
from spotify_popularity.data.schema import validate_schema


def load_raw_dataset(path: Path | None = None) -> pd.DataFrame:
    """Carga el CSV original y valida su contrato mínimo sin modificarlo."""

    dataset_path = path or PROJECT_PATHS.raw_dataset
    if not dataset_path.is_file():
        raise FileNotFoundError(f"No se encontró el dataset: {dataset_path}")

    data = pd.read_csv(dataset_path)
    validate_schema(data)
    return data


def prepare_base_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Aplica solo transformaciones inequívocas previas al EDA.

    La deduplicación y el tratamiento de anomalías se posponen hasta contar con
    evidencia y una justificación analítica.
    """

    validate_schema(data)
    prepared = data.copy()

    if "Unnamed: 0" in prepared.columns:
        prepared = prepared.drop(columns="Unnamed: 0")

    return prepared
