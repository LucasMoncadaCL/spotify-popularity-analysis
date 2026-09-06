"""Contrato estructural mínimo del dataset Spotify Tracks."""

import pandas as pd

REQUIRED_COLUMNS = frozenset(
    {
        "track_id",
        "artists",
        "album_name",
        "track_name",
        "popularity",
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
        "track_genre",
    }
)


def validate_schema(data: pd.DataFrame) -> None:
    """Comprueba que estén presentes las variables mínimas esperadas."""

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"El dataset no contiene las columnas requeridas: {missing}")
