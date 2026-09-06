# Spotify Popularity Analysis

**Responsable de comprensión del negocio, objetivos, KPIs, fuentes, colaboración y CRISP-DM:** Lucas Moncada.

Proyecto reproducible de Machine Learning para estudiar qué características musicales y
contextuales están asociadas con la popularidad de canciones. El trabajo sigue CRISP-DM y
prioriza preparación, calidad de datos, EDA y análisis ético según la rúbrica de la EP1.

## 1. Comprensión del problema de negocio

La industria musical debe decidir qué canciones priorizar en campañas, playlists y acciones
de promoción antes de conocer completamente su desempeño. Este proyecto estudia qué
características musicales y contextuales están asociadas con la popularidad registrada en
Spotify y hasta qué punto pueden aportar evidencia a esas decisiones.

La pregunta central es:

> ¿Qué características musicales y contextuales están asociadas con la popularidad de una
> canción y cómo puede esta información apoyar decisiones de artistas, sellos y equipos de
> marketing musical?

El análisis es descriptivo y predictivo, no causal. Una asociación no demuestra que modificar
una característica produzca mayor popularidad.

### Stakeholders y decisiones

- Artistas y sellos: priorización de lanzamientos y recursos promocionales.
- Equipos de marketing: caracterización de segmentos y evaluación de campañas.
- Curadores de contenido: comprensión de perfiles musicales y diversidad del catálogo.
- Equipo analítico: preparación de una base reproducible para un futuro modelo de regresión.

## 2. Objetivos

**Objetivo general:** analizar la relación entre los atributos de las canciones y su
popularidad, preparando evidencia reproducible para una futura estimación de `popularity`.

**Objetivos específicos:**

1. Describir la estructura, procedencia y calidad inicial del dataset.
2. Identificar distribuciones, anomalías y posibles sesgos de cobertura.
3. Explorar variables acústicas y contextuales potencialmente relevantes.
4. Preparar un flujo verificable para las etapas posteriores de limpieza y modelamiento.

## 3. KPIs e indicadores

| Tipo | Indicador | Propósito |
|---|---|---|
| Negocio | Popularidad promedio y mediana | Establecer el desempeño central del catálogo observado. |
| Negocio | Proporción con popularidad ≥ 70 | Segmentar operativamente canciones de alta popularidad; el umbral se someterá a sensibilidad. |
| Negocio | Popularidad por género | Comparar segmentos sin interpretar diferencias como efectos causales. |
| Calidad | Completitud | Medir la proporción de celdas disponibles. |
| Calidad | Duplicidad de `track_id` | Evitar conteos sesgados y futura fuga entre entrenamiento y prueba. |
| Modelo futuro | MAE, RMSE y R² | Evaluar error y capacidad explicativa de una regresión posterior. |

## 4. Fuente de datos y herramientas colaborativas

### Fuente y alcance de los datos

El archivo analizado fue proporcionado por la asignatura y se conserva sin modificaciones en
`data/raw/Spotify_Tracks_Dataset.csv`. Su estructura coincide con el
[Spotify Tracks Dataset publicado en Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset),
atribuido a Maharshi Pandya y construido con metadatos y características de Spotify.

La definición actual de `popularity` en la
[documentación de Spotify](https://developer.spotify.com/documentation/web-api/reference/get-track)
la sitúa entre 0 y 100 y señala que depende principalmente de reproducciones y recencia. El
campo aparece actualmente como obsoleto en esa API, por lo que el dataset debe interpretarse
como una fotografía histórica y no como una medición en tiempo real.

La integridad del archivo se controla con SHA-256 mediante la biblioteca estándar `hashlib`:

```text
b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd
```

El diccionario completo está disponible en [`docs/data_dictionary.md`](docs/data_dictionary.md).

### Herramientas colaborativas y reproducibilidad

| Herramienta | Uso y justificación | Estado actual |
|---|---|---|
| Git | Control de versiones, ramas y trazabilidad de cambios por integrante. | En uso y conectado con `origin`. |
| GitHub | Repositorio remoto privado, revisión, respaldo e integración grupal. | En uso: [`LucasMoncadaCL/spotify-popularity-analysis`](https://github.com/LucasMoncadaCL/spotify-popularity-analysis). |
| Jupyter Notebook | Une código, evidencia e interpretación en documentos ejecutables. | En uso. |
| Markdown | Informe técnico legible, portable y versionable. | En uso. |
| uv | Reproduce Python y dependencias mediante `pyproject.toml` y `uv.lock`. | En uso. |

El flujo acordado mantiene `main` para entregas estables, `dev` para integración y ramas
temporales `feature/*`, `fix/*` y, solo cuando corresponda, `hotfix/*`. Los nombres técnicos
de GitFlow se mantienen en inglés y los títulos y descripciones de los commits se escriben en
español.

## 5. Metodología CRISP-DM

| Fase | Aplicación al proyecto | Estado |
|---|---|---|
| Business Understanding | Problema, stakeholders, objetivos y KPIs. | Desarrollado por Lucas Moncada. |
| Data Understanding | Fuente, variables, calidad preliminar y distribuciones. | Iniciado por Lucas Moncada. |
| Data Preparation | Tratamiento del índice, nulos, anomalías y duplicidad por `track_id`. | Entrega al Integrante 2. |
| Modeling | Entrenamiento de regresiones y alternativas justificadas. | Etapa posterior. |
| Evaluation | MAE, RMSE y R², junto con utilidad y limitaciones de negocio. | Etapa posterior. |
| Deployment | README, notebooks, datos y presentación reproducibles. | Entrega académica final. |

CRISP-DM se aplicará de forma iterativa: los resultados de preparación, modelamiento o
evaluación pueden exigir revisar objetivos, variables y decisiones anteriores.

## 6. Descripción e inspección inicial del dataset

| Evidencia | Resultado |
|---|---:|
| Dimensiones | 114.000 filas × 21 columnas |
| Tipos | 9 `float64`, 6 `int64`, 5 `object`, 1 `bool` |
| Celdas nulas | 3 |
| Filas exactamente duplicadas | 0 |
| `track_id` únicos | 89.741 |
| IDs que aparecen más de una vez | 16.641 |
| Filas asociadas a IDs repetidos | 40.900 |
| Géneros | 114, exactamente 1.000 filas por género |

La popularidad media es 33,24 y la mediana 35. El 14,05% de los registros tiene popularidad
cero y el 4,8% alcanza al menos 70 puntos. Estos resultados describen las filas observadas;
antes de realizar inferencia por canción deberá resolverse la repetición de `track_id`.

## Requisitos

- [uv](https://docs.astral.sh/uv/)
- Python 3.12 (uv lo instala automáticamente si no está disponible)

## Preparación del entorno

```powershell
uv sync
```

No es necesario activar manualmente `.venv`: anteponga `uv run` a cada comando.

## Comandos principales

```powershell
# Verificar calidad del código y pruebas
uv run ruff check .
uv run ruff format --check .
uv run pytest

# Crear la versión base procesada sin alterar el archivo original
uv run python scripts/build_base_dataset.py

# Abrir los notebooks
uv run jupyter lab
```

Al abrir Jupyter mediante `uv run`, el notebook utiliza directamente el kernel `python3` del
entorno del proyecto; no requiere instalar un kernel global en el equipo.

## Estructura

```text
.
├── data/
│   ├── raw/             # Datos originales, inmutables
│   ├── interim/         # Resultados intermedios regenerables
│   └── processed/       # Datos preparados para análisis/modelamiento
├── docs/reference/      # Rúbrica y documentación de origen
├── models/              # Modelos serializados (generados)
├── notebooks/           # Experimentos y narrativa analítica numerada
├── reports/figures/     # Gráficos exportados para informe/presentación
├── scripts/             # Puntos de entrada ejecutables
├── src/spotify_popularity/ # Paquete principal
│   ├── config.py          # Configuración transversal
│   ├── data/              # Carga, esquema, metadatos e integridad
│   ├── analysis/          # Calidad y análisis descriptivo
│   └── visualization/     # Distribuciones y estilo visual
├── tests/               # Pruebas automatizadas
├── pyproject.toml       # Dependencias y configuración de herramientas
└── uv.lock              # Versiones exactas para reproducibilidad
```

## Convenciones

- `data/raw/` nunca se modifica; toda salida se escribe en `data/interim/` o
  `data/processed/`.
- La lógica reutilizable pertenece a `src/`, no a los notebooks.
- Los notebooks se numeran según su orden de ejecución.
- Las rutas se resuelven desde la raíz del proyecto, evitando rutas absolutas personales.
- Toda decisión de limpieza debe quedar justificada en el informe y en el notebook.
