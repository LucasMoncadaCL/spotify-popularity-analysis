"""Pruebas unitarias para carga y preparación de datos."""

import pandas as pd
import pytest

from spotify_popularity.data.loader import prepare_base_dataset
from spotify_popularity.data.schema import validate_schema


def _valid_row() -> dict[str, object]:
    return {
        "track_id": "track-1",
        "artists": "Artist",
        "album_name": "Album",
        "track_name": "Song",
        "popularity": 50,
        "duration_ms": 180_000,
        "explicit": False,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 0,
        "loudness": -8.0,
        "mode": 1,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 120.0,
        "time_signature": 4,
        "track_genre": "pop",
    }


def test_validate_schema_rejects_missing_required_column() -> None:
    data = pd.DataFrame([_valid_row()]).drop(columns="popularity")

    with pytest.raises(ValueError, match="popularity"):
        validate_schema(data)


def test_prepare_base_dataset_removes_exported_index_without_mutating_input() -> None:
    data = pd.DataFrame([{**_valid_row(), "Unnamed: 0": 0}])

    prepared = prepare_base_dataset(data)

    assert "Unnamed: 0" not in prepared.columns
    assert "Unnamed: 0" in data.columns
    assert prepared.loc[0, "track_id"] == "track-1"
