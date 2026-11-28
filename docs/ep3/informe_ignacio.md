# Informe técnico individual EP3 — Ignacio Silva

## Alcance de IE11

Este informe acompaña la sección 9 de
[`04b_modeling_ignacio.ipynb`](../../notebooks/04b_modeling_ignacio.ipynb).
Evalúa la variación entre particiones y la transferencia a artistas principales
ausentes del ajuste para los candidatos entregados por Lucas en el
[PR #24](https://github.com/LucasMoncadaCL/spotify-popularity-analysis/pull/24).
La selección final IE12 y la integración en notebook 05, README y presentación
corresponden a César. La evidencia histórica de EA2 se conserva.

## Datos y prueba preservada

Se regenera la preparación común desde `data/raw/Spotify_Tracks_Dataset.csv`:
114.000 filas originales, una fila inválida excluida y consolidación por `track_id`
hasta 89.740 canciones, sin nulos ni IDs repetidos. Los géneros se conservan como
multietiquetas y la popularidad por ID se resume con mediana. No se modifica la fuente.

- SHA-256 de la fuente: `b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd`.
- Entrenamiento compartido: **71.792 canciones**; solo estas ingresan en IE11.
- Prueba compartida: **17.948 canciones**, excluidas de todos los folds nuevos.
- SHA-256 de los IDs de prueba ordenados:
  `7270ff57b6fb81215fba2f834942d194183e3854ccac935a65e5a03f7888b318`.

No se genera otro conjunto de prueba ni se vuelve a evaluar el bosque sobre la prueba
compartida. Para contrastar CV y prueba se leen las métricas publicadas por Lucas en
`04a_lucas_test_comparison.csv`; el notebook registra su huella y la del CSV de CV.
La prueba ya era conocida en EA2 y en el trabajo de Lucas. Las evaluaciones de las
celdas históricas EA2 permanecen documentadas como tales.

Los predictores son los diez atributos numéricos y cuatro categóricos del protocolo,
más `track_genres`. Artistas, nombres, IDs y objetivo no entran como predictores.
El `model_pipeline` común ajusta escala, one-hot y vocabulario de géneros exclusivamente
con el ajuste de cada fold; cada ejecución usa un clon nuevo del modelo.

## Diseño fijado antes de evaluar

Se mantienen exactamente los cuatro candidatos del handoff:

| Modelo | Parámetros congelados |
| --- | --- |
| Dummy mediana | `strategy="median"`; no requiere preprocesamiento. |
| Ridge | `alpha=0.1`, pipeline común. |
| Árbol | `max_depth=15`, `min_samples_leaf=20`, `random_state=42`, pipeline común. |
| Random Forest | `n_estimators=100`, `max_depth=None`, `min_samples_leaf=1`, `max_features=1.0`, `random_state=42`, `n_jobs=1`, pipeline común. |

No se realiza una segunda búsqueda ni se cambian parámetros según los resultados.
Las dos estrategias contienen las mismas canciones de entrenamiento y usan los mismos
folds para todos los modelos:

1. **KFold:** 3 folds, `shuffle=True`, `random_state=42`, con el mismo orden de
   `split.train_ids` usado por Lucas. Se comprueba que MAE, RMSE y R² medios reproducen
   sus CSV con tolerancia numérica de `1e-5` absoluta y relativa.
2. **GroupKFold:** 3 folds, `shuffle=False`. El grupo es el primer nombre de `artists`
   antes de `;`, sin espacios laterales y normalizado con `casefold`, como en EA2.
   Es determinista y no usa semilla de mezcla; equilibra aproximadamente las canciones
   sin dividir un artista principal entre ajuste y validación.

Cada canción se valida una vez por estrategia. La asignación por ID, los tamaños,
cantidades de artistas y huellas de cada lado quedan en CSV. La auditoría debe mostrar
cero IDs de prueba en todos los folds y cero principales compartidos en GroupKFold.
Se cuentan además canciones de validación cuyo artista secundario aparece en ajuste
en cualquier rol. Los colaboradores pueden seguir compartidos.
Este uso de grupos sigue la
[documentación oficial de GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html).

Las métricas son MAE, RMSE y R² en validación y entrenamiento, brecha
`MAE_validación − MAE_entrenamiento` y tiempo de ajuste. Se presentan medias y
desviaciones poblacionales (`ddof=0`) de tres folds, igual que Lucas; no son intervalos
de confianza. El resumen es promedio simple entre folds; los tamaños quedan disponibles
para interpretar diferencias. Se emplean seis procesos externos, un hilo por bosque
y un máximo de un hilo interno por proceso para evitar paralelismo anidado.

<!-- RESULTADOS_IE11_INICIO -->
## Resultados ejecutados

| CV | Modelo | MAE ± DE | RMSE ± DE | R² ± DE | MAE entrenamiento | Brecha MAE | Ajuste/fold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KFold | Dummy mediana | 17,224 ± 0,026 | 20,570 ± 0,027 | -0,000 ± 0,000 | 17,224 | -0,000 | 0.1 s |
| KFold | Ridge | 11,819 ± 0,045 | 16,521 ± 0,069 | 0,355 ± 0,005 | 11,782 | 0,037 | 0.4 s |
| KFold | Árbol | 14,382 ± 0,017 | 18,319 ± 0,029 | 0,207 ± 0,001 | 14,235 | 0,146 | 1.4 s |
| KFold | Random Forest | 9,901 ± 0,018 | 14,768 ± 0,039 | 0,485 ± 0,003 | 3,767 | 6,133 | 991.9 s |
| GroupKFold | Dummy mediana | 17,224 ± 0,145 | 20,570 ± 0,110 | -0,000 ± 0,000 | 17,224 | 0,000 | 0.1 s |
| GroupKFold | Ridge | 12,061 ± 0,408 | 16,858 ± 0,650 | 0,328 ± 0,045 | 11,736 | 0,324 | 0.4 s |
| GroupKFold | Árbol | 14,751 ± 0,195 | 18,696 ± 0,269 | 0,174 ± 0,015 | 14,211 | 0,541 | 1.4 s |
| GroupKFold | Random Forest | 11,752 ± 0,458 | 16,969 ± 0,770 | 0,319 ± 0,055 | 3,692 | 8,060 | 1,086.1 s |

La CV aleatoria reproduce las métricas publicadas por Lucas dentro de la tolerancia
declarada. Al agrupar por principal, el MAE del bosque pasa de
**9,901 a 11,752**
(diferencia **1,852 puntos**). La diferencia agrupada `MAE_Ridge − MAE_bosque`
es **0,309 puntos**, con Ridge en 12,061:
un valor positivo favorece al bosque y uno negativo a Ridge. La brecha agrupada
entre entrenamiento y validación del bosque es **8,060 puntos**;
esta brecha indica un ajuste fuerte a las canciones vistas.

| Modelo | MAE aleatorio | MAE agrupado | Agrupado − aleatorio | MAE prueba Lucas |
| --- | --- | --- | --- | --- |
| Dummy mediana | 17,224 | 17,224 | 0,000 | 17,250 |
| Ridge | 11,819 | 12,061 | 0,242 | 11,915 |
| Árbol | 14,382 | 14,751 | 0,370 | 14,508 |
| Random Forest | 9,901 | 11,752 | 1,852 | 9,648 |

La prueba proviene exclusivamente de la evaluación publicada por Lucas. Las diferencias
entre CV agrupada y prueba aleatoria no deben presentarse como una prueba independiente
de transferencia a artistas nuevos.

| CV | Fold | Ajuste | Validación | Principales compartidos | Validación con secundario en ajuste |
| --- | --- | --- | --- | --- | --- |
| KFold | 1 | 47861 | 23931 | 6791 | 4291 |
| KFold | 2 | 47861 | 23931 | 6831 | 4260 |
| KFold | 3 | 47862 | 23930 | 6752 | 4226 |
| GroupKFold | 1 | 47861 | 23931 | 0 | 3032 |
| GroupKFold | 2 | 47861 | 23931 | 0 | 3087 |
| GroupKFold | 3 | 47862 | 23930 | 0 | 3093 |

Los seis folds contienen cero IDs de prueba. GroupKFold comparte cero principales,
pero registra entre **3032 y
3093 canciones por fold** con
un colaborador secundario presente en ajuste. Hay **16.068 artistas principales** en el
entrenamiento y **5.356** en cada validación agrupada; los folds contienen
23.931, 23.931 y 23.930 canciones, respectivamente.

La sección IE11 tardó **1021.6 s** de pared en esta ejecución,
con seis ajustes externos concurrentes del bosque. No incluye el tiempo de la evidencia
EA2 previa.
Versiones: Python **3.12.14**, scikit-learn **1.9.0**,
pandas **2.3.3** y NumPy **2.5.3**.
Estos resultados entregan a César evidencia de rendimiento, dispersión y costo para IE12;
no sustituyen su decisión documentada ni la revisión cruzada humana.
<!-- RESULTADOS_IE11_FIN -->

## Qué permite concluir la comparación

El bosque conserva el menor MAE medio agrupado, pero su ventaja sobre Ridge se reduce
de **1,918 puntos** en CV aleatoria a **0,309 puntos** al separar principales. Además,
Ridge obtiene mejor RMSE agrupado (**16,858** frente a **16,969**) y R² (**0,328** frente
a **0,319**). La desviación del MAE del bosque pasa de **0,018** a **0,458** al agrupar;
la de Ridge agrupado es **0,408**. Con tres folds y ajustes correlacionados, estas cifras
no demuestran una diferencia estadísticamente significativa ni una superioridad general.

El bosque tarda aproximadamente **1.086 s por fold agrupado**, frente a **0,370 s** de
Ridge en este equipo, y su brecha de MAE agrupada es **8,060 puntos**, frente a **0,324**
de Ridge. Por tanto, la mejora de MAE por sí sola no resuelve IE12: César debe ponderar
el error absoluto frente a errores grandes, estabilidad, costo y las condiciones de uso.
Estas observaciones diagnostican los candidatos congelados y no se usan aquí para
reajustarlos ni escoger una nueva solución tras consultar la prueba.

La comparación aleatoria mide predicción de canciones retenidas en esta muestra y puede
compartir artistas principales. La agrupada pregunta por canciones de principales que
no aparecen en el ajuste del fold, bajo el solapamiento secundario declarado. El cambio
de MAE entre estrategias describe sensibilidad del candidato a la partición: no es el
efecto causal de excluir artistas. El test por canción de Lucas tampoco es un test de
principales nuevos y no debe presentarse como tal.

**Sesgo de selección previo:** el bosque se eligió con CV aleatoria sobre estas mismas
71.792 canciones. Repetir sus folds reproduce esa evidencia; agrupar después no hace
independiente toda la selección anterior. Este ejercicio diagnostica candidatos fijos
y no equivale a CV anidada. Para una estimación sin ese sesgo habría que repetir la
búsqueda completa solo dentro del ajuste de cada fold externo agrupado, o evaluar en
nuevos datos no consultados. No se proclama esa validación adicional como realizada.

Tres folds no garantizan estabilidad entre semillas o épocas. La agrupación usa nombres
de artista, sin resolver homónimos o identidades alternativas. La fuente histórica fue
balanceada artificialmente por género y no contiene fechas ni exposición promocional:
no se demuestra generalización temporal, causalidad o utilidad comercial. Las brechas,
errores de popularidad alta y costo de Lucas siguen siendo relevantes para IE12.

`popularity` sigue siendo una regresión. Ni R² ni precisión del ranking son accuracy.
El requisito verbal de 80% sigue pendiente de definición por el docente. Si confirma
clasificación, el equipo deberá acordar clases y umbrales y usar métricas por clase y
sensibles al desbalance. El baseline de predecir siempre «no popular» ya tiene 96,36%
en la prueba compartida y no identifica ninguna canción popular.

## Artefactos para reproducir e integrar

La lógica reutilizable está en
[`validation.py`](../../src/spotify_popularity/modeling/validation.py), con pruebas de
exclusión del test, separación de principales, cobertura, colaboradores compartidos y
ajuste independiente en [`test_modeling_validation.py`](../../tests/test_modeling_validation.py).
Las salidas están en [`reports/figures/ea3/`](../../reports/figures/ea3/):

| Prefijo `04b_ignacio_` | Contenido |
| --- | --- |
| `fold_assignments.csv` | Un registro por canción de entrenamiento, fold aleatorio y agrupado. |
| `fold_audit.csv` | Tamaños, principales compartidos, colaboradores secundarios y huellas por fold. |
| `random_folds.csv`, `grouped_folds.csv`, `cv_folds.csv` | Métricas individuales y tiempo de cada ajuste. |
| `cv_summary.csv` | Medias/DE de métricas, brecha y costo por estrategia/modelo. |
| `cv_vs_test.csv` | Contraste explícito con la prueba ya publicada por Lucas. |
| `artist_shift.csv` | Diferencia de MAE agrupado menos aleatorio. |
| `generalization_mae.png` | Comparación visual de CV y prueba publicada. |
| `manifest.json` | Versiones, parámetros, semillas, paralelismo, huellas y duración. |

Desde la raíz del repositorio, en PowerShell:

```powershell
uv sync --locked
uv run --locked python -X utf8 -m nbconvert --to notebook --execute notebooks/04b_modeling_ignacio.ipynb --output 04b_ignacio_ep3_executed.ipynb --output-dir tmp --ExecutePreprocessor.timeout=14400
uv run --locked pytest -q
uv run --locked ruff check src scripts tests
uv run --locked ruff format --check src scripts tests
```

La ejecución completa reproduce tanto EA2 como la sección nueva EP3; las tablas y figuras
nuevas se generan automáticamente. Los tiempos dependen del equipo. Las celdas y salidas
históricas de EA2 versionadas se conservan; el notebook incluye las salidas ejecutadas EP3.

## Verificaciones de calidad

- Notebook completo: **14 celdas de código ejecutadas sin errores**, salida 0 y 24 ajustes de CV.
- `uv run --locked pytest -q`: **21 pruebas aprobadas**.
- `uv run --locked ruff check src scripts tests`: aprobado.
- `uv run --locked ruff format --check src scripts tests`: 27 archivos con formato correcto.
- `uv lock --check`: bloqueo vigente.
- Las 25 celdas históricas de Ignacio conservan fuente, salidas y metadatos; las nuevas
  celdas EP3 no agregan diagnósticos de lint.
- `ruff check .` conserva **35 diagnósticos previos** de notebooks (imports y longitud
  de línea), cotejados con los mismos archivos de `origin/dev`; `ruff format --check .`
  señala los cuatro notebooks históricos 04a–04c/05. No se declara aprobado el lint
  global ni se reformatea trabajo de otros integrantes en este PR de IE11.

## Handoff y defensa individual

El [mensaje para César](mensaje_cesar.md) indica qué integrar después del merge a `dev`.
César debe contrastar beneficio del bosque, variación por artista, brecha, costo y
segmentos de Lucas; justificar la solución de IE12 y mantener cifras consistentes entre
notebook 05, README e informe/presentación. No se añade aquí la conclusión final del equipo.
Lucas debe revisar IE11 según la rotación acordada; César realiza el merge tras esa revisión.

Para defender IE11: explicar qué problema resuelve separar grupos, por qué el pipeline se
reajusta en cada fold, cómo se interpretan MAE/RMSE/R² y media/DE, qué significa la brecha,
por qué se reutiliza la evaluación de prueba ya publicada y qué limitaciones conserva
un candidato seleccionado previamente en este mismo entrenamiento.
