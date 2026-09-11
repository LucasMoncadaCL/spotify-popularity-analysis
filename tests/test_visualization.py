"""Pruebas basicas de las visualizaciones publicas."""

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from spotify_popularity.visualization.distributions import (  # noqa: E402
    plot_binned_popularity,
    plot_explicit_distribution,
    plot_popularity_distribution,
)


def test_plot_popularity_distribution_labels_the_target() -> None:
    figure = plot_popularity_distribution(pd.DataFrame({"popularity": [0, 25, 50, 75, 100]}))

    assert "popularidad" in figure.axes[0].get_title().lower()


def test_plot_explicit_distribution_shows_both_categories() -> None:
    figure = plot_explicit_distribution(pd.DataFrame({"explicit": [True, False, False]}))

    assert len(figure.axes[0].get_xticklabels()) == 2


def test_plot_binned_popularity_labels_the_association() -> None:
    data = pd.DataFrame({"energy": [0.1, 0.2, 0.7, 0.9], "popularity": [10, 20, 60, 80]})

    figure = plot_binned_popularity(data, "energy", bins=2)

    assert figure.axes[0].get_ylabel() == "Popularidad mediana"
