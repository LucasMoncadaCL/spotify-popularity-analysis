# Spotify Popularity Analysis

Proyecto académico de análisis de datos y Machine Learning orientado a estudiar qué
características musicales y contextuales están asociadas con la popularidad de canciones en
Spotify. El trabajo sigue la metodología CRISP-DM y prioriza la trazabilidad, la calidad de
datos, el análisis exploratorio y la reproducibilidad exigidos en la Evaluación Parcial 1.

## Problema y propósito del proyecto

Artistas, sellos, equipos de marketing y curadores de contenido deben decidir qué canciones
priorizar sin conocer completamente su desempeño futuro. El proyecto busca aportar evidencia
para esas decisiones mediante la siguiente pregunta de negocio:

> ¿Qué características musicales y contextuales están asociadas con la popularidad de una
> canción y cómo puede esta información apoyar decisiones de promoción y gestión de catálogo?

El objetivo general es analizar la relación entre los atributos disponibles y `popularity`,
además de preparar una base confiable para evaluar posteriormente modelos de regresión. El
análisis identifica asociaciones y patrones; no pretende demostrar relaciones causales.

Los objetivos específicos del equipo son:

1. Comprender el contexto de negocio, los usuarios del análisis y sus necesidades.
2. Examinar la estructura, procedencia y calidad del dataset.
3. Preparar los datos con decisiones justificadas y reproducibles.
4. Explorar patrones, relaciones, anomalías y posibles sesgos.
5. Evaluar variables y modelos pertinentes para estimar popularidad.
6. Comunicar resultados, limitaciones y consideraciones éticas de forma defendible.

## Dataset

El archivo de trabajo fue proporcionado por la asignatura y se conserva sin modificaciones
en `data/raw/Spotify_Tracks_Dataset.csv`. Su estructura coincide con el
[Spotify Tracks Dataset publicado en Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset),
atribuido a Maharshi Pandya y construido con metadatos y características de Spotify.

La variable de interés es `popularity`, medida en una escala de 0 a 100. La
[documentación de Spotify](https://developer.spotify.com/documentation/web-api/reference/get-track)
indica que esta medida depende principalmente de reproducciones y recencia; actualmente el
campo aparece como obsoleto en la API. Por ello, el dataset se interpreta como una fotografía
histórica y no como información en tiempo real.

El archivo contiene 114.000 filas y 21 columnas antes de cualquier transformación. Su
integridad se controla con SHA-256:

```text
b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd
```

El significado, tipo y rol esperado de cada campo se encuentra en el
[diccionario de variables](docs/data_dictionary.md).

## Indicadores de evaluación

El proyecto separa los indicadores descriptivos, de calidad y de desempeño predictivo para
evitar confundir éxito de negocio con precisión técnica.

| Categoría | Indicador | Uso previsto |
|---|---|---|
| Negocio | Popularidad promedio y mediana | Caracterizar el desempeño central del catálogo observado. |
| Negocio | Proporción con popularidad ≥ 70 | Explorar un segmento operativo de alta popularidad; el umbral requiere análisis de sensibilidad. |
| Negocio | Popularidad por género | Comparar segmentos sin interpretar diferencias como efectos causales. |
| Calidad | Completitud | Cuantificar la disponibilidad de los datos. |
| Calidad | Duplicidad de `track_id` | Prevenir conteos sesgados y futura fuga entre entrenamiento y prueba. |
| Modelo | MAE, RMSE y R² | Evaluar el error y la capacidad explicativa de modelos de regresión. |

## Metodología y estado

CRISP-DM se aplica de manera iterativa: un hallazgo de preparación, modelamiento o evaluación
puede exigir revisar decisiones anteriores.

| Fase CRISP-DM | Aplicación en el proyecto | Estado |
|---|---|---|
| Business Understanding | Problema, stakeholders, objetivos e indicadores. | Completada inicialmente. |
| Data Understanding | Fuente, variables, estructura, calidad preliminar y primeras distribuciones. | Completada inicialmente. |
| Data Preparation | Tratamiento del índice exportado, nulos, anomalías y repetición de `track_id`. | Completada inicialmente. |
| Modeling | Comparación de regresiones y alternativas justificadas. | Pendiente. |
| Evaluation | Métricas técnicas, utilidad de negocio, sesgos y limitaciones. | Pendiente. |
| Deployment | Informe, notebooks, datos y presentación reproducibles. | En construcción. |

### Entregables y responsables

| Entregable | Alcance | Responsable | Estado |
|---|---|---|---|
| [`01_data_understanding.ipynb`](notebooks/01_data_understanding.ipynb) | Problema, objetivos, KPIs, fuente, CRISP-DM, descripción de variables, inspección inicial y primeras distribuciones. | Lucas Moncada | Completado. |
| [Registro de avance de Lucas Moncada](docs/progress/lucas_moncada.md) | Decisiones, resultados verificados y entrega de hallazgos para la preparación de datos. | Lucas Moncada | Completado. |
| [`02_data_preparation.ipynb`](notebooks/02_data_preparation.ipynb) | Limpieza reproducible, tratamiento de anomalías, nulos y `track_id`, validación, transformaciones y construcción documentada del dataset procesado. | Ignacio Silva | Completado. |
| [Registro de avance de Ignacio Silva](docs/progress/ignacio_silva.md) | Checkpoints, decisiones, validaciones y entrega documentada de la etapa de calidad. | Ignacio Silva | Completado. |
| [`03_exploratory_analysis.ipynb`](notebooks/03_exploratory_analysis.ipynb) | EDA profundo de popularidad, relaciones, anomalías, sesgos, ética, privacidad y recomendaciones para modelamiento. | César Rojas | Completado inicialmente. |
| [Registro de avance de César Rojas](docs/progress/cesar_rojas.md) | Validaciones, hallazgos, decisiones de EDA y entrega documentada a modelamiento. | César Rojas | Completado inicialmente. |
| Modelamiento y evaluación | Línea base, modelos y métricas predictivas. | Equipo | Pendiente. |

Esta tabla se actualizará cuando el equipo incorpore nuevas etapas; no se crean enlaces a
archivos que todavía no existen.

## Resultados disponibles

La comprensión inicial confirmó:

- 114.000 registros y 21 variables.
- 3 celdas nulas, concentradas en una misma fila anómala.
- 0 filas exactamente duplicadas.
- 89.741 valores únicos de `track_id`.
- 16.641 IDs repetidos, asociados a 40.900 filas.
- 114 géneros con 1.000 registros cada uno.
- Popularidad media de 33,24 y mediana de 35.
- 14,05% de los registros con popularidad 0 y 4,8% con popularidad igual o superior a 70.

Estos resultados describen las filas observadas. Antes de formular conclusiones por canción o
dividir datos para modelamiento, debe resolverse la repetición de `track_id`.

## Preparación de datos disponible

La etapa 2 genera `data/processed/spotify_tracks_clean.csv` de forma reproducible con:

- Eliminación de `Unnamed: 0`, que solo reproduce el índice exportado.
- Exclusión de 1 registro sin artista, álbum ni nombre de pista, y con duración cero.
- Consolidación de 24.259 apariciones adicionales de `track_id`; cada canción queda una vez.
- Conservación de las etiquetas múltiples de género en `track_genres`, ordenadas y separadas
  por `|`.
- Uso de la mediana de `popularity` cuando un mismo ID tiene valores distintos, evitando
  elegir arbitrariamente una de sus asignaciones de género.

El resultado contiene 89.740 canciones, 20 columnas, ningún valor nulo y duración positiva.
Las decisiones, sus controles y las limitaciones se registran en el
[checkpoint de preparación](docs/progress/ignacio_silva.md). Para regenerarlo:

```powershell
uv run python scripts/build_processed_dataset.py
```

## EDA profundo disponible

El [notebook de EDA](notebooks/03_exploratory_analysis.ipynb) usa exclusivamente el dataset
procesado y valida su contrato antes de analizarlo. Sus principales hallazgos son:

- Popularidad media 33,20 y mediana 33; 10,47% de canciones con valor cero y 3,48% con 70 o más.
- Ningún atributo acústico aislado tiene asociación fuerte con popularidad; `instrumentalness`
  presenta la asociación negativa más visible.
- `energy`, `loudness` y `acousticness` muestran redundancia relevante para modelos lineales.
- El análisis documenta los sesgos de género y temporalidad, riesgos éticos y de privacidad, y la
  recomendación de usar modelos como apoyo a decisiones humanas.

El detalle de decisiones, limitaciones y traspaso se encuentra en el
[registro de César Rojas](docs/progress/cesar_rojas.md).

## Instalación reproducible

### Requisitos

- [uv](https://docs.astral.sh/uv/)
- Git

El proyecto fija Python 3.12 y las versiones exactas de sus dependencias en `uv.lock`. Desde
la raíz del repositorio:

```powershell
uv sync
```

No es necesario activar `.venv` manualmente: `uv run` ejecuta cada comando dentro del entorno
del proyecto.

## Ejecución y verificación

```powershell
# Abrir los notebooks
uv run jupyter lab

# Generar la base intermedia sin modificar el archivo original
uv run python scripts/build_base_dataset.py

# Verificar estilo y pruebas automatizadas
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Los notebooks se ejecutan en orden numérico. La lógica reutilizable se mantiene en `src/` y
las celdas se concentran en la narrativa, las llamadas al paquete y la interpretación de
resultados.

## Flujo de datos

```text
data/raw/
    │  datos originales e inmutables
    ▼
data/interim/
    │  resultados intermedios regenerables
    ▼
data/processed/
    │  datos preparados para análisis y modelamiento
    ├──────────────► reports/figures/
    └──────────────► models/
```

Las transformaciones deben implementarse en `src/spotify_popularity/`, exponerse mediante
scripts o notebooks y acompañarse de pruebas cuando contengan reglas reutilizables.

## Estructura del repositorio

```text
.
├── data/
│   ├── raw/                    # Datos originales, inmutables
│   ├── interim/                # Resultados intermedios regenerables
│   └── processed/              # Datos preparados para análisis/modelamiento
├── docs/
│   ├── progress/               # Registro de avances y traspasos
│   ├── reference/              # Rúbrica y documentación de origen
│   └── data_dictionary.md      # Diccionario del dataset
├── models/                     # Modelos serializados generados
├── notebooks/                  # Análisis numerados en orden de ejecución
├── reports/figures/            # Figuras para informe y presentación
├── scripts/                    # Puntos de entrada ejecutables
├── src/spotify_popularity/
│   ├── config.py               # Configuración transversal
│   ├── data/                   # Carga, esquema, metadatos e integridad
│   ├── analysis/               # Calidad y análisis descriptivo
│   └── visualization/          # Distribuciones y estilo visual
├── tests/                      # Pruebas automatizadas
├── COLLABORATORS.md            # Flujo de colaboración y GitFlow
├── pyproject.toml              # Dependencias y herramientas
└── uv.lock                     # Resolución exacta de dependencias
```

## Colaboración

El repositorio utiliza un GitFlow simplificado:

- `main` contiene hitos estables.
- `dev` integra cambios revisados.
- `feature/*`, `fix/*` y `hotfix/*` contienen tareas acotadas.

Los commits, Pull Requests y documentación se redactan en español; los nombres técnicos de
GitFlow permanecen en inglés. Las reglas completas de ramas, notebooks, datos, validación e
integración están en la [guía de colaboración](COLLABORATORS.md).

## Limitaciones actuales

- El dataset es estático y no representa el estado actual de Spotify.
- `popularity` depende de factores temporales y comerciales que no están completamente
  representados en las variables disponibles.
- Un mismo `track_id` puede aparecer en más de una fila o género.
- Los resultados descriptivos no permiten afirmar causalidad.
- La preparación, el modelamiento y el análisis ético aún deben completarse antes de formular
  conclusiones finales.
