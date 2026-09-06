"""Visualizaciones consistentes para la exploración inicial."""

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from spotify_popularity.visualization.style import SPOTIFY_DARK, SPOTIFY_GREEN


def _require_columns(data: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = set(columns).difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas para construir la figura: {', '.join(sorted(missing))}")


def plot_popularity_distribution(data: pd.DataFrame) -> Figure:
    """Grafica la distribución de la variable objetivo y su mediana."""

    _require_columns(data, ["popularity"])
    figure, axis = plt.subplots(figsize=(9, 5))
    sns.histplot(data=data, x="popularity", bins=20, color=SPOTIFY_GREEN, ax=axis)
    median = data["popularity"].median()
    axis.axvline(median, color=SPOTIFY_DARK, linestyle="--", label=f"Mediana: {median:.0f}")
    axis.set(
        title="Distribución inicial de la popularidad",
        xlabel="Popularidad (0–100)",
        ylabel="Cantidad de registros",
    )
    axis.legend()
    figure.tight_layout()
    return figure


def plot_duration_distribution(data: pd.DataFrame, upper_quantile: float = 0.99) -> Figure:
    """Grafica duración en minutos limitando la vista al cuantil indicado."""

    _require_columns(data, ["duration_ms"])
    if not 0 < upper_quantile <= 1:
        raise ValueError("upper_quantile debe estar en el intervalo (0, 1].")

    duration_minutes = pd.Series(
        np.divide(data["duration_ms"].to_numpy(), 60_000),
        index=data.index,
        name="duration_minutes",
    )
    positive_duration = duration_minutes[duration_minutes > 0]
    upper_limit = positive_duration.quantile(upper_quantile)
    visible_duration = positive_duration[positive_duration <= upper_limit]

    figure, axis = plt.subplots(figsize=(9, 5))
    sns.histplot(visible_duration, bins=30, color=SPOTIFY_GREEN, ax=axis)
    axis.set(
        title=f"Duración de canciones (vista hasta percentil {upper_quantile:.0%})",
        xlabel="Duración (minutos)",
        ylabel="Cantidad de registros",
    )
    figure.tight_layout()
    return figure


def plot_explicit_distribution(data: pd.DataFrame) -> Figure:
    """Compara la cantidad de registros explícitos y no explícitos."""

    _require_columns(data, ["explicit"])
    labels = data["explicit"].map({False: "No explícita", True: "Explícita"})
    counts = labels.value_counts().reindex(["No explícita", "Explícita"], fill_value=0)

    figure, axis = plt.subplots(figsize=(7, 5))
    sns.barplot(x=counts.index, y=counts.values, color=SPOTIFY_GREEN, ax=axis)
    axis.set(
        title="Distribución de contenido explícito",
        xlabel="Clasificación",
        ylabel="Cantidad de registros",
    )
    figure.tight_layout()
    return figure


def plot_audio_feature_distributions(data: pd.DataFrame, features: tuple[str, ...]) -> Figure:
    """Compara distribuciones de características acústicas en escala 0–1."""

    _require_columns(data, features)
    figure, axes = plt.subplots(2, 4, figsize=(16, 8), sharex=True)
    for axis, feature in zip(axes.flat, features, strict=False):
        sns.histplot(data=data, x=feature, bins=20, color=SPOTIFY_GREEN, ax=axis)
        axis.set(title=feature, xlabel="Valor", ylabel="Frecuencia")

    for axis in axes.flat[len(features) :]:
        axis.set_visible(False)

    figure.suptitle("Distribuciones de características acústicas", fontsize=14)
    figure.tight_layout()
    return figure


def save_figure(figure: Figure, path: Path) -> None:
    """Guarda una figura creando previamente su directorio de destino."""

    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=150, bbox_inches="tight")
