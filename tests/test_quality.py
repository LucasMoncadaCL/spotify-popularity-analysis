"""Pruebas del reporte de calidad."""

import pandas as pd

from spotify_popularity.analysis.quality import column_quality_report, dataset_overview


def test_column_quality_report_counts_missing_and_unique_values() -> None:
    data = pd.DataFrame({"genre": ["pop", "pop", None], "score": [1, 2, 2]})

    report = column_quality_report(data)

    assert report.loc["genre", "missing_count"] == 1
    assert report.loc["genre", "unique_count"] == 2
    assert report.loc["score", "duplicate_count"] == 1


def test_dataset_overview_distinguishes_repeated_identifiers_from_exact_duplicates() -> None:
    data = pd.DataFrame(
        {
            "track_id": ["a", "a", "b", "c", "c"],
            "track_genre": ["pop", "rock", "jazz", "pop", "pop"],
            "value": [1, 1, 2, 3, 3],
        }
    )

    overview = dataset_overview(data)

    assert overview["row_count"] == 5
    assert overview["column_count"] == 3
    assert overview["unique_track_ids"] == 3
    assert overview["repeated_track_ids"] == 2
    assert overview["rows_with_repeated_track_id"] == 4
    assert overview["extra_track_id_rows"] == 2
    assert overview["exact_duplicate_rows"] == 1
