from dataclasses import dataclass

import pandas as pd

from spotify_popularity.data.schema import validate_schema

TEXT_COLUMNS = ("track_id", "artists", "album_name", "track_name", "track_genre")
INVARIANT_COLUMNS = (
    "artists",
    "album_name",
    "track_name",
    "duration_ms",
    "explicit",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
)


@dataclass(frozen=True)
class PreparationSummary:
    input_rows: int
    invalid_rows_removed: int
    output_rows: int
    repeated_track_ids_consolidated: int


def _invalid_rows(data: pd.DataFrame) -> pd.Series:
    missing_text = data.loc[:, TEXT_COLUMNS].isna().any(axis=1)
    blank_text = (
        data.loc[:, TEXT_COLUMNS]
        .apply(lambda column: column.astype("string").str.strip().eq(""))
        .any(axis=1)
    )
    missing_measurement = data[["popularity", "duration_ms"]].isna().any(axis=1)
    return missing_text | blank_text | missing_measurement | data["duration_ms"].le(0)


def _validate_invariant_attributes(data: pd.DataFrame) -> None:
    counts = data.groupby("track_id", sort=False)[list(INVARIANT_COLUMNS)].nunique(dropna=False)
    conflicts = counts.gt(1).any(axis=1)
    if conflicts.any():
        identifiers = ", ".join(conflicts[conflicts].index[:5])
        raise ValueError(
            "No se pueden consolidar track_id con atributos invariantes conflictivos: "
            f"{identifiers}"
        )


def prepare_modeling_dataset(data: pd.DataFrame) -> tuple[pd.DataFrame, PreparationSummary]:
    validate_schema(data)
    input_rows = len(data)
    cleaned = data.drop(columns="Unnamed: 0", errors="ignore").copy()
    invalid_rows = _invalid_rows(cleaned)
    cleaned = cleaned.loc[~invalid_rows].copy()
    _validate_invariant_attributes(cleaned)

    aggregations = {column: "first" for column in INVARIANT_COLUMNS}
    aggregations["popularity"] = "median"
    aggregations["track_genre"] = lambda values: "|".join(sorted(values.unique()))
    prepared = (
        cleaned.groupby("track_id", as_index=False, sort=True)
        .agg(aggregations)
        .rename(columns={"track_genre": "track_genres"})
    )
    prepared["popularity"] = prepared["popularity"].astype(float)

    summary = PreparationSummary(
        input_rows=input_rows,
        invalid_rows_removed=int(invalid_rows.sum()),
        output_rows=len(prepared),
        repeated_track_ids_consolidated=len(cleaned) - len(prepared),
    )
    return prepared, summary
