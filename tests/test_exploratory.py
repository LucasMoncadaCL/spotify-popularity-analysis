"""Pruebas para los resumenes reutilizables del EDA."""

import pandas as pd
import pytest

from spotify_popularity.analysis.exploratory import (
    categorical_cardinality,
    dataset_comparison,
    expanded_genre_summary,
    explicit_effect_summary,
    genre_support_sensitivity,
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


def test_dataset_comparison_preserves_both_stages() -> None:
    comparison = dataset_comparison(_data(), _data().iloc[:2])

    assert comparison.loc["Original", "filas"] == 3
    assert comparison.loc["Procesado", "canciones_unicas"] == 2


def test_explicit_effect_summary_calculates_standardized_difference() -> None:
    data = pd.DataFrame(
        {
            "explicit": [False, False, True, True],
            "popularity": [10.0, 20.0, 20.0, 30.0],
        }
    )

    effect = explicit_effect_summary(data)

    assert effect["diferencia_medias"] == 10
    assert effect["diferencia_medianas"] == 10
    assert effect["cohen_d"] == pytest.approx(2**0.5)


def test_categorical_cardinality_counts_values() -> None:
    cardinality = categorical_cardinality(_data(), ["track_genres"])

    assert cardinality.loc["track_genres", "valores_unicos"] == 3


def test_genre_support_sensitivity_reports_empty_threshold() -> None:
    sensitivity = genre_support_sensitivity(_data(), thresholds=(1, 3))

    assert sensitivity.loc[1, "generos_incluidos"] == 3
    assert sensitivity.loc[3, "generos_incluidos"] == 0
