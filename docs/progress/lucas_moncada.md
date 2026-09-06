# Progreso — Lucas Moncada

**Responsabilidad principal:** problema de negocio, objetivos, KPIs, fuente de datos,
herramientas colaborativas y metodología CRISP-DM.  
**Evidencia complementaria:** descripción del dataset, calidad preliminar y primeras
distribuciones.  
**Estado:** completado y documentado.  
**Fecha de actualización:** 2026-09-06.

## 1. Comprensión del problema de negocio

Se documentó el contexto de inteligencia musical, los stakeholders y las decisiones que el
análisis podría apoyar. La pregunta central estudia qué características musicales y
contextuales están asociadas con la popularidad observada en Spotify.

El alcance se declaró descriptivo y predictivo, no causal. No se afirma que modificar una
característica musical produzca por sí sola mayor popularidad.

**Evidencia:** secciones 1 del `README.md` y del notebook
`notebooks/01_data_understanding.ipynb`.

## 2. Objetivo general y objetivos específicos

Se definió como objetivo general analizar la relación entre atributos musicales y
contextuales y `popularity`, preparando evidencia reproducible para una futura regresión.
Los objetivos específicos cubren comprensión, calidad, variables relevantes y preparación
del flujo para las siguientes etapas.

**Evidencia:** sección 2 del README y del notebook.

## 3. Definición de KPIs

Los indicadores se separaron para evitar confundir resultados de negocio con métricas
técnicas:

- Negocio: popularidad promedio, mediana, proporción ≥ 70 y popularidad por género.
- Calidad: completitud y duplicidad de `track_id`.
- Modelo futuro: MAE, RMSE y R².

El umbral 70 se documentó como criterio operativo sujeto a análisis de sensibilidad, no como
clasificación oficial de Spotify.

**Evidencia:** sección 3 del README y del notebook.

## 4. Fuente de datos y herramientas colaborativas

La fuente operativa es el archivo entregado por la asignatura, preservado sin modificaciones
en `data/raw/`. Su estructura coincide con el dataset de Maharshi Pandya publicado en Kaggle
y sus definiciones se contrastaron con Spotify Web API.

Se justificaron las siguientes herramientas:

- Git para control de versiones, ramas y trazabilidad.
- GitHub como repositorio remoto privado para colaboración, respaldo e integración.
- Jupyter Notebook para vincular código, evidencia e interpretación.
- Markdown para el informe técnico versionable.
- uv para reproducir Python y las dependencias del equipo.

El repositorio privado `LucasMoncadaCL/spotify-popularity-analysis` está conectado como
`origin`. El flujo acordado emplea `main`, `dev` y ramas temporales `feature/*`, `fix/*` y
`hotfix/*`; los nombres técnicos de GitFlow permanecen en inglés y los mensajes de commit se
redactan en español. La integridad del CSV se comprobó con SHA-256.

**Evidencia:** sección 4 del README y del notebook; `docs/data_dictionary.md`.

## 5. Metodología CRISP-DM

Se explicó la aplicación de sus seis fases:

1. Business Understanding: problema, stakeholders, objetivos y KPIs.
2. Data Understanding: fuente, variables, calidad inicial y distribuciones.
3. Data Preparation: tratamiento posterior del índice, nulos, anomalías y repeticiones.
4. Modeling: futuros modelos de regresión y alternativas justificadas.
5. Evaluation: métricas predictivas, utilidad y limitaciones de negocio.
6. Deployment: entrega académica reproducible mediante README, notebooks, datos y
   presentación.

Se dejó explícito que CRISP-DM es iterativo y permite volver a fases anteriores según la
evidencia obtenida.

**Evidencia:** sección 5 del README y del notebook.

## 6. Descripción y diccionario de variables

Se documentaron las 21 columnas con descripción, tipo conceptual, unidad o rango y rol
analítico. Se distinguió `Unnamed: 0` como índice exportado y `popularity` como variable
objetivo.

**Evidencia:** `docs/data_dictionary.md` y sección 6 del notebook.

## 7. Inspección inicial y calidad preliminar

Se verificaron 114.000 filas, 21 columnas, tres celdas nulas y 89.741 `track_id` únicos. Se
detectaron 16.641 IDs repetidos, equivalentes a 24.259 apariciones adicionales. Los nulos
pertenecen a un mismo registro que también posee duración cero.

Estos elementos se diagnosticaron, pero no se eliminaron para no anticipar decisiones del
Integrante 2.

**Evidencia:** sección 7 del notebook y funciones en `src/spotify_popularity/analysis/`.

## 8. Primeras distribuciones

Se analizaron popularidad, duración, contenido explícito, características acústicas y
cobertura de géneros. Se exportaron cuatro figuras reproducibles a `reports/figures/`.

Estos resultados complementan Data Understanding, pero no reemplazan el EDA profundo de las
etapas siguientes.

**Evidencia:** sección 8 del notebook y `src/spotify_popularity/visualization/`.

## 9. Entrega documentada al Integrante 2

El Integrante 2 recibe las anomalías identificadas y deberá justificar:

- Retiro de `Unnamed: 0`.
- Tratamiento del registro con nulos y duración cero.
- Estrategia de consolidación o agrupación de `track_id` repetidos.
- Generación de una versión procesada sin modificar `data/raw/`.

La entrega se apoya en el notebook ejecutado, el README, el diccionario de variables, las
figuras y las funciones reutilizables de `src/`.

## Verificación técnica

- 8 pruebas automatizadas aprobadas.
- Código y formato aprobados por `ruff`.
- 16 celdas de código ejecutadas sin errores antes de esta actualización documental.
- Cuatro figuras generadas y revisadas visualmente.
- SHA-256 de la copia en `data/raw/` idéntico al archivo original.
