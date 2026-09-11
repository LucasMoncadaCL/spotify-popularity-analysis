"""Funciones reproducibles para el EDA posterior a la preparacion."""

from collections.abc import Sequence

import pandas as pd

NUMERIC_FEATURES = (
    "popularity",
    "duration_ms",
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


def validate_processed_dataset(data: pd.DataFrame) -> dict[str, object]:
    """Resume los controles de contrato del dataset preparado."""

    required = {"track_id", "track_genres", "popularity", "duration_ms"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(missing))}")

    return {
        "shape": data.shape,
        "missing_cells": int(data.isna().sum().sum()),
        "unique_track_ids": int(data["track_id"].nunique()),
        "duplicate_track_ids": int(data["track_id"].duplicated().sum()),
        "non_positive_durations": int(data["duration_ms"].le(0).sum()),
        "empty_genres": int(data["track_genres"].astype("string").str.strip().eq("").sum()),
    }


def popularity_summary(data: pd.DataFrame) -> pd.Series:
    """Calcula estadisticos y proporciones operativas de popularidad."""

    popularity = data["popularity"]
    return pd.Series(
        {
            "media": popularity.mean(),
            "mediana": popularity.median(),
            "desviacion_estandar": popularity.std(),
            "minimo": popularity.min(),
            "p25": popularity.quantile(0.25),
            "p75": popularity.quantile(0.75),
            "p95": popularity.quantile(0.95),
            "maximo": popularity.max(),
            "proporcion_cero_pct": popularity.eq(0).mean() * 100,
            "proporcion_70_o_mas_pct": popularity.ge(70).mean() * 100,
        }
    )


def target_correlations(data: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    """Compara correlaciones Pearson y Spearman de predictores con el objetivo."""

    missing = set(features).difference(data.columns)
    if missing:
        raise ValueError(f"Faltan variables: {', '.join(sorted(missing))}")

    return (
        pd.DataFrame(
            {
                "pearson": data.loc[:, list(features)].corrwith(
                    data["popularity"], method="pearson"
                ),
                "spearman": data.loc[:, list(features)].corrwith(
                    data["popularity"], method="spearman"
                ),
            }
        )
        .rename_axis("variable")
        .sort_values("spearman", key=lambda values: values.abs(), ascending=False)
    )


def expanded_genre_summary(data: pd.DataFrame, minimum_count: int = 100) -> pd.DataFrame:
    """Expande etiquetas de genero y filtra resultados con soporte suficiente."""

    if minimum_count < 1:
        raise ValueError("minimum_count debe ser al menos 1.")
    if not {"track_id", "track_genres", "popularity"}.issubset(data.columns):
        raise ValueError("Se requieren track_id, track_genres y popularity.")

    expanded = data.loc[:, ["track_id", "track_genres", "popularity"]].copy()
    expanded["genre"] = expanded.pop("track_genres").str.split("|")
    expanded = expanded.explode("genre")
    summary = expanded.groupby("genre", as_index=False).agg(
        canciones=("track_id", "nunique"),
        popularidad_media=("popularity", "mean"),
        popularidad_mediana=("popularity", "median"),
        desviacion_estandar=("popularity", "std"),
    )
    return summary.loc[summary["canciones"].ge(minimum_count)].sort_values(
        ["popularidad_mediana", "canciones"], ascending=[False, False]
    )


def iqr_outlier_summary(data: pd.DataFrame, features: Sequence[str]) -> pd.DataFrame:
    """Resume limites IQR y recuentos; no etiqueta observaciones como errores."""

    rows: list[dict[str, float | int | str]] = []
    for feature in features:
        values = data[feature]
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        rows.append(
            {
                "variable": feature,
                "minimo": values.min(),
                "p1": values.quantile(0.01),
                "p99": values.quantile(0.99),
                "maximo": values.max(),
                "limite_inferior_iqr": lower,
                "limite_superior_iqr": upper,
                "casos_fuera_iqr": int(((values < lower) | (values > upper)).sum()),
            }
        )
    return pd.DataFrame(rows).set_index("variable")
