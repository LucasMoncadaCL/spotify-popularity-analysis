"""Metadatos documentales de las variables de entrada."""

import pandas as pd

VARIABLES = (
    ("Unnamed: 0", "Índice exportado", "entero", "0–113999", "Técnica; no predictiva"),
    (
        "track_id",
        "Identificador de la pista en Spotify",
        "texto",
        "ID alfanumérico",
        "Identificador",
    ),
    ("artists", "Nombre del artista o artistas", "texto", "categoría abierta", "Contextual"),
    ("album_name", "Nombre del álbum", "texto", "categoría abierta", "Contextual"),
    ("track_name", "Nombre de la canción", "texto", "categoría abierta", "Contextual"),
    ("popularity", "Puntaje de popularidad", "entero", "0–100", "Objetivo"),
    ("duration_ms", "Duración de la pista", "entero", "milisegundos", "Explicativa"),
    ("explicit", "Indica contenido explícito", "booleano", "False/True", "Explicativa"),
    ("danceability", "Aptitud percibida para bailar", "decimal", "0–1", "Explicativa"),
    ("energy", "Intensidad y actividad percibidas", "decimal", "0–1", "Explicativa"),
    ("key", "Tonalidad según notación de clases de altura", "entero", "0–11", "Explicativa"),
    ("loudness", "Sonoridad global", "decimal", "decibelios (dB)", "Explicativa"),
    ("mode", "Modalidad musical", "entero", "0 menor; 1 mayor", "Explicativa"),
    ("speechiness", "Presencia percibida de palabras habladas", "decimal", "0–1", "Explicativa"),
    ("acousticness", "Confianza de que la pista sea acústica", "decimal", "0–1", "Explicativa"),
    (
        "instrumentalness",
        "Probabilidad percibida de ausencia de voz",
        "decimal",
        "0–1",
        "Explicativa",
    ),
    ("liveness", "Presencia percibida de audiencia", "decimal", "0–1", "Explicativa"),
    ("valence", "Positividad musical percibida", "decimal", "0–1", "Explicativa"),
    ("tempo", "Tempo estimado", "decimal", "BPM", "Explicativa"),
    ("time_signature", "Compás estimado", "entero", "pulsos por compás", "Explicativa"),
    ("track_genre", "Género asignado a la pista", "texto", "114 categorías", "Contextual"),
)


def variable_dictionary() -> pd.DataFrame:
    """Devuelve el diccionario de variables como una tabla independiente."""

    return pd.DataFrame(
        VARIABLES,
        columns=["variable", "description", "conceptual_type", "unit_or_range", "role"],
    )
