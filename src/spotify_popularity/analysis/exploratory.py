"""Funciones reproducibles para el EDA posterior a la preparacion."""

from collections.abc import Sequence
from math import sqrt

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


def dataset_comparison(raw: pd.DataFrame, processed: pd.DataFrame) -> pd.DataFrame:
    """Compara indicadores clave antes y despues de consolidar canciones."""

    rows = []
    for stage, data in (("Original", raw), ("Procesado", processed)):
        popularity = data["popularity"]
        rows.append(
            {
                "dataset": stage,
                "filas": len(data),
                "canciones_unicas": data["track_id"].nunique(),
                "popularidad_media": popularity.mean(),
                "popularidad_mediana": popularity.median(),
                "popularidad_cero_pct": popularity.eq(0).mean() * 100,
                "popularidad_70_o_mas_pct": popularity.ge(70).mean() * 100,
            }
        )
    return pd.DataFrame(rows).set_index("dataset")


def explicit_effect_summary(data: pd.DataFrame) -> pd.Series:
    """Resume diferencias descriptivas y d de Cohen entre grupos de explicit."""

    required = {"explicit", "popularity"}
    if not required.issubset(data.columns):
        raise ValueError("Se requieren explicit y popularity.")

    non_explicit = data.loc[~data["explicit"].astype(bool), "popularity"]
    explicit = data.loc[data["explicit"].astype(bool), "popularity"]
    if len(non_explicit) < 2 or len(explicit) < 2:
        raise ValueError("Cada grupo debe contener al menos dos observaciones.")

    pooled_variance = (
        (len(explicit) - 1) * explicit.var() + (len(non_explicit) - 1) * non_explicit.var()
    ) / (len(explicit) + len(non_explicit) - 2)
    cohen_d = (explicit.mean() - non_explicit.mean()) / sqrt(pooled_variance)

    return pd.Series(
        {
            "n_no_explicita": len(non_explicit),
            "n_explicita": len(explicit),
            "diferencia_medias": explicit.mean() - non_explicit.mean(),
            "diferencia_medianas": explicit.median() - non_explicit.median(),
            "cohen_d": cohen_d,
        }
    )


def categorical_cardinality(data: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Cuenta valores unicos para orientar el tratamiento de categoricas."""

    missing = set(columns).difference(data.columns)
    if missing:
        raise ValueError(f"Faltan variables: {', '.join(sorted(missing))}")
    return pd.DataFrame(
        {
            "valores_unicos": data.loc[:, list(columns)].nunique(dropna=False),
            "porcentaje_sobre_filas": data.loc[:, list(columns)].nunique(dropna=False)
            / len(data)
            * 100,
        }
    ).rename_axis("variable")


def genre_support_sensitivity(
    data: pd.DataFrame, thresholds: Sequence[int] = (100, 200, 500)
) -> pd.DataFrame:
    """Evalua estabilidad del lider por mediana ante distintos soportes minimos."""

    rows = []
    for threshold in thresholds:
        summary = expanded_genre_summary(data, minimum_count=threshold)
        if summary.empty:
            rows.append(
                {
                    "soporte_minimo": threshold,
                    "generos_incluidos": 0,
                    "genero_lider": "No aplica",
                    "mediana_lider": float("nan"),
                }
            )
            continue
        leader = summary.iloc[0]
        rows.append(
            {
                "soporte_minimo": threshold,
                "generos_incluidos": len(summary),
                "genero_lider": leader["genre"],
                "mediana_lider": leader["popularidad_mediana"],
            }
        )
    return pd.DataFrame(rows).set_index("soporte_minimo")
