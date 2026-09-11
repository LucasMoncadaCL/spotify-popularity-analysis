"""Genera tablas de evidencia reproducible para el informe LaTeX."""

import pandas as pd

from spotify_popularity.analysis.exploratory import (
    categorical_cardinality,
    dataset_comparison,
    explicit_effect_summary,
    genre_support_sensitivity,
    iqr_outlier_summary,
    target_correlations,
)
from spotify_popularity.config import PROJECT_PATHS
from spotify_popularity.data.loader import load_raw_dataset

OUTPUT_DIRECTORY = PROJECT_PATHS.root / "docs" / "latex" / "tables"


def _write_table(data: pd.DataFrame, filename: str, *, index: bool = True) -> None:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    table = data.to_latex(index=index, escape=True, float_format=lambda value: f"{value:.3f}")
    (OUTPUT_DIRECTORY / filename).write_text(table, encoding="utf-8")


def main() -> None:
    processed_path = PROJECT_PATHS.data_processed / "spotify_tracks_clean.csv"
    if not processed_path.exists():
        raise FileNotFoundError(
            "Falta el dataset procesado. Ejecute primero scripts/build_processed_dataset.py."
        )

    raw = load_raw_dataset()
    processed = pd.read_csv(processed_path)

    comparison = dataset_comparison(raw, processed).rename(
        columns={
            "filas": "Filas",
            "canciones_unicas": "Canciones unicas",
            "popularidad_media": "Media",
            "popularidad_mediana": "Mediana",
            "popularidad_cero_pct": "Porcentaje igual a 0",
            "popularidad_70_o_mas_pct": "Porcentaje mayor o igual a 70",
        }
    )
    _write_table(comparison, "dataset_comparison.tex")

    features = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
    ]
    correlations = target_correlations(processed, features).rename(
        columns={"pearson": "Pearson", "spearman": "Spearman"}
    )
    _write_table(correlations, "target_correlations.tex")

    effect = explicit_effect_summary(processed).rename(
        {
            "n_no_explicita": "Canciones no explicitas",
            "n_explicita": "Canciones explicitas",
            "diferencia_medias": "Diferencia de medias",
            "diferencia_medianas": "Diferencia de medianas",
            "cohen_d": "d de Cohen",
        }
    )
    _write_table(effect.rename("Valor").to_frame(), "explicit_effect.tex")

    sensitivity = genre_support_sensitivity(processed).rename(
        columns={
            "generos_incluidos": "Generos incluidos",
            "genero_lider": "Genero lider",
            "mediana_lider": "Mediana lider",
        }
    )
    sensitivity.index.name = "Soporte minimo"
    _write_table(sensitivity, "genre_sensitivity.tex")

    categorical_columns = [
        "artists",
        "album_name",
        "track_name",
        "track_genres",
        "explicit",
        "key",
        "mode",
        "time_signature",
    ]
    cardinality = categorical_cardinality(processed, categorical_columns)
    risks = {
        "artists": "Alta cardinalidad y memorizacion",
        "album_name": "Alta cardinalidad y memorizacion",
        "track_name": "Alta cardinalidad y texto libre",
        "track_genres": "Multietiqueta; combinaciones de etiquetas",
        "explicit": "Desbalance y posibles variables de confusion",
        "key": "Categoria nominal codificada como numero",
        "mode": "Baja cardinalidad",
        "time_signature": "Categoria discreta con clases poco frecuentes",
    }
    cardinality["Riesgo"] = cardinality.index.map(risks)
    cardinality = cardinality.rename(
        columns={
            "valores_unicos": "Valores unicos",
            "porcentaje_sobre_filas": "Porcentaje sobre filas",
        }
    )
    _write_table(cardinality, "categorical_cardinality.tex")

    outliers = iqr_outlier_summary(
        processed,
        ["duration_ms", "tempo", "loudness", "speechiness", "instrumentalness", "liveness"],
    )[["minimo", "p1", "p99", "maximo", "casos_fuera_iqr"]].rename(
        columns={
            "minimo": "Minimo",
            "p1": "P1",
            "p99": "P99",
            "maximo": "Maximo",
            "casos_fuera_iqr": "Fuera de IQR",
        }
    )
    _write_table(outliers, "outlier_summary.tex")

    print("Tablas LaTeX generadas en:", OUTPUT_DIRECTORY)
    print("\nComparacion original/procesado:\n", comparison.round(3))
    print("\nEfecto de explicit:\n", effect.round(3))
    print("\nSensibilidad por soporte:\n", sensitivity)
    print("\nCardinalidad:\n", cardinality)


if __name__ == "__main__":
    main()
