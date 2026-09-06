"""Pruebas del contrato documental de variables."""

from spotify_popularity.data.metadata import variable_dictionary
from spotify_popularity.data.schema import REQUIRED_COLUMNS


def test_variable_dictionary_covers_all_raw_columns_once() -> None:
    dictionary = variable_dictionary()
    documented_variables = set(dictionary["variable"])

    assert dictionary["variable"].is_unique
    assert documented_variables == REQUIRED_COLUMNS | {"Unnamed: 0"}
