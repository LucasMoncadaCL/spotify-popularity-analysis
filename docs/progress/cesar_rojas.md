# Progreso - Cesar Rojas

**Responsabilidad principal:** EDA profundo posterior a la preparación, análisis de variables,
anomalías, sesgos, ética, privacidad y entrega a modelamiento.
**Estado:** completado inicialmente.
**Fecha de actualización:** 2026-09-11.

## Dataset recibido y validaciones

Se utilizó `data/processed/spotify_tracks_clean.csv`, regenerable mediante
`uv run python scripts/build_processed_dataset.py`. No se repitió la limpieza del CSV raw.

| Control | Resultado |
|---|---:|
| Filas y columnas | 89.740 x 20 |
| Celdas nulas | 0 |
| `track_id` únicos | 89.740 |
| `track_id` duplicados | 0 |
| Duraciones no positivas | 0 |
| Etiquetas de género vacías | 0 |

El resultado es consistente con la entrega de Ignacio: una fila por canción, sin `Unnamed: 0`,
con `track_genres` multietiqueta y `popularity` consolidada con mediana cuando correspondía.

## Análisis realizados y resultados principales

- Popularidad: media 33,20, mediana 33, desviación estándar 20,58; 10,47% de canciones en
  cero y 3,48% con 70 o más. Frente a las filas originales, las diferencias se explican por
  consolidar IDs repetidos y no ponderar una canción por cada género asignado.
- Correlaciones: no hay una asociación fuerte de un atributo acústico individual con
  `popularity`. `instrumentalness` presenta la asociación negativa más visible
  (Pearson -0,128; Spearman -0,124), mientras `loudness` y `danceability` son positivas y
  débiles.
- Redundancia: `energy` y `loudness` (0,759), y `energy` y `acousticness` (-0,733), requieren
  atención en modelos lineales mediante escala, regularización o diagnóstico de colinealidad.
- Contenido explícito: el grupo explícito tiene media 36,88 y mediana 37, frente a 32,85 y 33
  del grupo no explícito. Es una asociación descriptiva; género, audiencia, recencia y promoción
  pueden confundirla.
- Géneros: se expandieron etiquetas separadas por `|` y se usó soporte mínimo de 100 canciones.
  Cada fila expandida representa una asociación canción-género, no canciones nuevas. La cobertura
  balanceada del origen impide interpretar los conteos como prevalencia real.

## Extremos y decisiones

El IQR identifica colas en duración, tempo, loudness y variables acotadas. Se conserva todo:
duraciones largas pueden corresponder a piezas válidas; valores cercanos a los extremos en
`speechiness`, `instrumentalness` y `liveness` son coherentes con escalas 0-1. Para
modelamiento se recomienda revisar puntualmente tempo cero y duración, y evaluar escala robusta
o `log1p(duration_ms)`, sin eliminar observaciones automáticamente.

## Sesgos, ética y privacidad

**Sesgos y limitaciones observables:** la fuente original asigna 1.000 filas a cada género,
por lo que no representa el catálogo natural. `popularity` es una fotografía histórica ligada a
reproducciones y recencia, sin fecha de extracción. No se observan marketing, playlists,
viralidad, región, fecha de lanzamiento ni popularidad previa de artistas.

**Ética:** usar una predicción para promoción puede reforzar ventajas de artistas expuestos,
homogeneizar decisiones creativas y perjudicar indirectamente estilos con menor representación.
El modelo futuro debe apoyar decisiones humanas, no automatizar presupuesto o promoción; deben
revisarse métricas globales y por grupos.

**Privacidad:** hay metadatos musicales y de artistas, pero no datos personales directos ni
conducta de oyentes. El riesgo individual es menor, aunque se conserva trazabilidad de fuente,
transformaciones y condiciones de uso, y no se deben vincular estos datos con perfiles de usuarios
sin una base legal y controles adicionales.

## Entrega a modelamiento

Se recomiendan atributos acústicos y `explicit` como candidatas, con tratamiento de escala y
redundancia. `track_genres` requiere multi-hot encoding; `artists`, `track_name` y `album_name`
son de alta cardinalidad y presentan riesgo de memorización. `track_id` se conserva solo para
trazabilidad y control de particiones, no como predictor. La siguiente etapa debe evaluar MAE,
RMSE y R2, mantener particiones sin leakage y, si hay fechas disponibles, contrastar una
partición temporal.

## Evidencia entregada

- `notebooks/03_exploratory_analysis.ipynb`: narrativa, validación, tablas y gráficos ejecutables.
- `src/spotify_popularity/analysis/exploratory.py`: resúmenes reutilizables de validación,
  correlación, géneros y extremos.
- `reports/figures/05_*` a `10_*`: figuras nuevas del EDA profundo.
