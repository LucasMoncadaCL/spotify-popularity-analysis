# Datos

- `raw/`: archivos originales de solo lectura.
- `interim/`: resultados intermedios que pueden regenerarse.
- `processed/`: datasets preparados para EDA o modelamiento.

`processed/spotify_tracks_clean.csv` se genera con
`scripts/build_processed_dataset.py`. Contiene una fila por `track_id`; la columna
`track_genres` conserva todas las etiquetas de género de cada pista, separadas por `|`.

El archivo original no debe editarse manualmente. Toda transformación debe realizarse desde
el código de `src/` o mediante un script reproducible.
