# Diccionario de datos

La descripción se basa en el archivo entregado por la asignatura, la ficha del dataset de
Kaggle y la documentación de Spotify Web API. Los rangos indicados son conceptuales; los
rangos observados se verifican por separado en el notebook.

| Variable | Descripción | Tipo conceptual | Unidad/rango | Rol |
|---|---|---|---|---|
| `Unnamed: 0` | Índice de fila exportado junto con el CSV | Entero | 0–113999 | Técnica; no predictiva |
| `track_id` | Identificador de la pista en Spotify | Texto | ID alfanumérico | Identificador |
| `artists` | Nombre del artista o artistas | Texto | Categoría abierta | Contextual |
| `album_name` | Nombre del álbum | Texto | Categoría abierta | Contextual |
| `track_name` | Nombre de la canción | Texto | Categoría abierta | Contextual |
| `popularity` | Puntaje de popularidad de la pista | Entero | 0–100 | Variable objetivo |
| `duration_ms` | Duración de la pista | Entero | Milisegundos | Explicativa |
| `explicit` | Indica si posee contenido explícito | Booleano | `False`/`True` | Explicativa |
| `danceability` | Aptitud percibida para bailar | Decimal | 0–1 | Explicativa |
| `energy` | Intensidad y actividad percibidas | Decimal | 0–1 | Explicativa |
| `key` | Tonalidad según clases de altura | Entero | 0–11 | Explicativa |
| `loudness` | Sonoridad global | Decimal | Decibelios (dB) | Explicativa |
| `mode` | Modalidad musical | Entero | 0 menor; 1 mayor | Explicativa |
| `speechiness` | Presencia percibida de palabras habladas | Decimal | 0–1 | Explicativa |
| `acousticness` | Confianza de que la pista sea acústica | Decimal | 0–1 | Explicativa |
| `instrumentalness` | Probabilidad percibida de ausencia de voz | Decimal | 0–1 | Explicativa |
| `liveness` | Presencia percibida de audiencia | Decimal | 0–1 | Explicativa |
| `valence` | Positividad musical percibida | Decimal | 0–1 | Explicativa |
| `tempo` | Tempo estimado | Decimal | BPM | Explicativa |
| `time_signature` | Compás estimado | Entero | Pulsos por compás | Explicativa |
| `track_genre` | Género asignado a la pista | Texto | 114 categorías | Contextual |

## Consideraciones de interpretación

- `popularity` es una medición dinámica dependiente de reproducciones y recencia; la copia
  disponible es una fotografía histórica sin fecha de extracción documentada.
- `track_id` identifica contenido musical, no a una persona. Se conserva para estudiar
  repeticiones y evitar fugas de información en etapas posteriores.
- Una misma pista puede aparecer en más de un género; por ello, cada fila no equivale
  necesariamente a una canción única.
- `explicit=False` puede significar contenido no explícito o clasificación desconocida,
  según la definición de Spotify.
- `Unnamed: 0` reproduce exactamente la secuencia de filas y no representa una propiedad
  musical.

## Dataset procesado

El archivo regenerable `data/processed/spotify_tracks_clean.csv` no contiene `Unnamed: 0`.
También reemplaza `track_genre` por `track_genres`: una lista de etiquetas únicas, ordenadas y
separadas por `|` para conservar que una misma canción puede pertenecer a más de un género.
La columna `popularity` puede ser decimal porque se calcula su mediana al consolidar filas del
mismo `track_id` con valores diferentes.

## Referencias

- Dataset entregado por la asignatura: `data/raw/Spotify_Tracks_Dataset.csv`.
- [Spotify Tracks Dataset de Maharshi Pandya en Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset).
- [Spotify Web API — Track](https://developer.spotify.com/documentation/web-api/reference/get-track).
