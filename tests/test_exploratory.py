"""Pruebas para los resumenes reutilizables del EDA."""

import pandas as pd
import pytest

from spotify_popularity.analysis.exploratory import (
    expanded_genre_summary,
    popularity_summary,
    validate_processed_dataset,
)


def _data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "track_id": ["a", "b", "c"],
            "track_genres": ["pop|rock", "pop", "jazz"],
            "popularity": [0.0, 50.0, 80.0],
            "duration_ms": [100_000, 120_000, 140_000],
        }
    )


def test_validate_processed_dataset_reports_contract_controls() -> None:
    controls = validate_processed_dataset(_data())

    assert controls["shape"] == (3, 4)
    assert controls["missing_cells"] == 0
    assert controls["duplicate_track_ids"] == 0


def test_popularity_summary_calculates_operational_proportions() -> None:
    summary = popularity_summary(_data())

    assert summary["mediana"] == 50
    assert summary["proporcion_cero_pct"] == pytest.approx(100 / 3)
    assert summary["proporcion_70_o_mas_pct"] == pytest.approx(100 / 3)


def test_expanded_genre_summary_uses_unique_tracks_per_label() -> None:
    summary = expanded_genre_summary(_data(), minimum_count=1)

    pop = summary.set_index("genre").loc["pop"]
    assert pop["canciones"] == 2
    assert pop["popularidad_media"] == 25
