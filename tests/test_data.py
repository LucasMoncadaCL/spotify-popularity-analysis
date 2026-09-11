"""Pruebas unitarias para carga y preparación de datos."""

import pandas as pd
import pytest

from spotify_popularity.data.loader import prepare_base_dataset
from spotify_popularity.data.preparation import prepare_modeling_dataset
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


def test_prepare_modeling_dataset_removes_invalid_row_and_consolidates_track_ids() -> None:
    valid = _valid_row()
    repeated = {**valid, "Unnamed: 0": 1, "track_genre": "rock", "popularity": 60}
    invalid = {
        **valid,
        "Unnamed: 0": 2,
        "track_id": "invalid",
        "artists": None,
        "duration_ms": 0,
    }

    prepared, summary = prepare_modeling_dataset(
        pd.DataFrame([{**valid, "Unnamed: 0": 0}, repeated, invalid])
    )

    assert prepared.shape == (1, 20)
    assert prepared.loc[0, "track_genres"] == "pop|rock"
    assert prepared.loc[0, "popularity"] == 55.0
    assert "Unnamed: 0" not in prepared.columns
    assert summary.invalid_rows_removed == 1
    assert summary.repeated_track_ids_consolidated == 1


def test_prepare_modeling_dataset_rejects_conflicting_track_attributes() -> None:
    first = {**_valid_row(), "Unnamed: 0": 0}
    conflicting = {**first, "Unnamed: 0": 1, "energy": 0.8}

    with pytest.raises(ValueError, match="conflictivos"):
        prepare_modeling_dataset(pd.DataFrame([first, conflicting]))
