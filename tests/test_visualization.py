"""Pruebas básicas de las visualizaciones públicas."""

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from spotify_popularity.visualization.distributions import (  # noqa: E402
    plot_explicit_distribution,
    plot_popularity_distribution,
)


def test_plot_popularity_distribution_labels_the_target() -> None:
    data = pd.DataFrame({"popularity": [0, 25, 50, 75, 100]})

    figure = plot_popularity_distribution(data)

    assert figure.axes[0].get_xlabel() == "Popularidad (0–100)"
    assert "popularidad" in figure.axes[0].get_title().lower()


def test_plot_explicit_distribution_shows_both_categories() -> None:
    data = pd.DataFrame({"explicit": [True, False, False]})

    figure = plot_explicit_distribution(data)

    labels = {tick.get_text() for tick in figure.axes[0].get_xticklabels()}
    assert labels == {"No explícita", "Explícita"}
