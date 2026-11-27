# Handoff EP3: Lucas Moncada

El [informe técnico individual](informe_lucas.md) documenta las decisiones, justificaciones, resultados, límites, reproducción y material para la defensa de IE9/IE10. Este archivo conserva el plan y el handoff operativo.

- **Indicadores principales:** IE9, optimización de hiperparámetros; IE10, técnicas de ensamble.
- **Rama propuesta:** `feature/ep3-lucas-ensemble`
- **Notebook de trabajo:** `notebooks/04a_modeling_lucas.ipynb`
- **PR destino:** `dev`

## Objetivo

Extender el modelo de regresión de popularidad de la EP2 con uno o más modelos de ensamble, ajustados de forma reproducible y comparados con Dummy, Ridge y árbol. La meta es demostrar si el ensamble mejora el desempeño y si esa mejora compensa su complejidad.

## Trabajo

- Mantener la misma fuente, canción única por `track_id`, predictores, semilla 42 y protocolo común ya definido por el equipo. Avanzar de forma independiente, sin esperar coordinación o aprobación previa de Ignacio.
- Añadir al menos un regresor de ensamble, por ejemplo `RandomForestRegressor` o `ExtraTreesRegressor`.
- Definir una búsqueda acotada y razonada de hiperparámetros; registrar las combinaciones probadas y por qué son pertinentes.
- Definir y documentar una validación cruzada reproducible dentro del entrenamiento. Registrar semilla, número de folds y métrica de selección para que Ignacio pueda reutilizar esa evidencia en su trabajo de generalización. No ajustar mirando el test.
- Comparar contra Dummy mediana, Ridge y árbol mediante MAE, RMSE y R²; incluir promedio/dispersión de validación cruzada y una evaluación final reservada.
- Describir costo/tiempo si es relevante para la decisión y comunicar limitaciones sin prometer el umbral verbal de 80% antes de aclarar qué significa.

## Plan técnico implementado

Plan aprobado por Lucas e implementado para IE9 e IE10 en esta rama.

### 1. Datos y separación

- Regenerar los datos desde la fuente sin modificar mediante `prepare_modeling_dataset(load_raw_dataset())`; verificar una fila por `track_id`, valores válidos y la huella SHA-256 de la fuente.
- Conservar `popularity` como objetivo continuo y los mismos predictores de la EA2. Reutilizar `split_track_ids`, la semilla 42 y la huella de los IDs de prueba. Usar todo el entrenamiento para CV y reservar la misma prueba para la comparación final.
- La prueba ya se utilizó en la EA2: no elegir configuraciones ni cambiar el relato a partir de los resultados históricos conocidos, y dejar explícito ese antecedente al informar la evaluación EP3.
- Mantener `popularity >= 70` solo como segmento y KPI retrospectivo. La regresión no requiere una etiqueta binaria ni un umbral de accuracy.

### 2. Modelo y búsqueda

- Implementar primero `RandomForestRegressor` dentro de `model_pipeline`, conservando las transformaciones comunes y ajustándolas dentro de cada fold.
- Usar `RandomizedSearchCV` con `random_state=42`, una búsqueda acotada de 12 configuraciones y 3 folds `KFold` reproducibles (`shuffle=True`, `random_state=42`). Esto da un presupuesto inicial de 36 ajustes de búsqueda, además del reajuste final y las referencias; medir y registrar el tiempo real.
- Explorar `n_estimators` en `{100, 200, 300}`, `max_depth` en `{10, 15, 25, None}`, `min_samples_leaf` en `{1, 2, 5, 10}` y `max_features` en `{"sqrt", 0.5, 1.0}`. Fijar `random_state=42` en el bosque y evitar paralelismo anidado.
- Seleccionar por MAE promedio de CV. Registrar para cada configuración MAE, RMSE y R² promedio y desviación entre folds, junto con tiempos de ajuste. Las métricas secundarias ayudan a interpretar el resultado, pero no cambian el criterio de selección.
- Si el costo de cómputo obliga a reducir las 12 configuraciones, fijar y documentar el nuevo presupuesto usando solo tiempos del entrenamiento, antes de consultar la prueba. Un segundo ensamble queda como extensión opcional si el primero y el presupuesto justifican la comparación.

### 3. Comparación y prueba final

- Calcular métricas de CV para Dummy mediana, Ridge (`alpha=0.1` del baseline EA2), árbol (profundidad 15 y hoja mínima 20) y el ensamble elegido, usando los mismos folds, predictores y transformaciones aplicables. Las configuraciones de Ridge y árbol son referencias históricas fijas, no nuevas selecciones sobre la prueba.
- Fijar el candidato y sus parámetros antes de evaluarlo en la prueba. Ajustar cada modelo con todo el entrenamiento y comparar MAE, RMSE y R² sobre los mismos `track_id` de prueba; mostrar la mejora en MAE frente a Dummy y a Ridge.
- Informar por separado el promedio/desviación de CV y las cifras de prueba. Registrar también las métricas de entrenamiento de los folds para analizar su brecha con validación y detectar sobreajuste. La CV aleatoria no prueba transferencia a artistas principales nuevos; ese análisis corresponde a Ignacio.

### 4. Diagnósticos que César dejó como referencia

- Comparar errores de los cuatro modelos por rangos de popularidad (`0`, `(0,35)`, `[35,70)` y `[70,100]`), contenido explícito y género, mostrando MAE y cantidad de canciones de cada segmento. Expandir los géneros después de predecir y advertir que una canción puede pertenecer a varios grupos.
- Calcular para cada modelo el KPI retrospectivo del 10% superior con la función común `top_decile_kpi`: canciones `popularity >= 70` recuperadas, precisión, recall y lift, junto con la prevalencia de referencia. No llamar accuracy a este KPI.
- Mostrar si el ensamble mejora los segmentos difíciles, especialmente las canciones de popularidad alta, o si solo reduce el error promedio. Interpretar esas diferencias dentro de una muestra histórica balanceada artificialmente por género, sin prometer éxito futuro ni una decisión automática de promoción.
- Conservar K-Means/PCA como evidencia previa del proyecto completo; Lucas no volverá a ajustarlos para IE9/IE10. César los incluirá en la integración de la presentación e informe EP3.

### 5. Selección y entrega de Lucas

- Describir el beneficio y costo del ensamble frente a las referencias, incluyendo CV, prueba, segmentos y KPI. Registrar fortalezas y límites de cada candidato para que César haga la selección final de IE12 con criterios previamente fijados; no cambiar hiperparámetros ni el candidato preseleccionado tras ver la prueba.
- Actualizar `notebooks/04a_modeling_lucas.ipynb` con controles, protocolo, búsqueda, tabla completa CV, comparación final, diagnósticos por segmento/KPI, costo, interpretación y límites. Guardar tablas y figuras necesarias en `reports/figures/ea3/` sin sobrescribir la evidencia EA2.
- Ejecutar el notebook de inicio a fin desde el entorno definido por `uv.lock`, sin rutas personales. Registrar versiones, semillas, huellas de la fuente y de la prueba, parámetros elegidos y comandos de reproducción.
- Entregar a Ignacio el modelo candidato, parámetros, configuración exacta de folds, resultados CV y de prueba, tiempos, tablas diagnósticas y límites para que pueda iniciar IE11 sin coordinación previa.
- Mantener la integración de resultados del equipo en notebook 05, README e informe/presentación bajo la responsabilidad de César.
- Preparar una explicación breve para la defensa individual: por qué `popularity` es regresión, cómo se evitó la fuga, qué se optimizó, qué aporta el ensamble, cómo se leen MAE/RMSE/R² y el KPI, y qué límites tienen los datos, la CV aleatoria y los clústeres previos.

## Resultado ejecutado y handoff a Ignacio

El notebook `04a_modeling_lucas.ipynb` corrió de inicio a fin con `uv run --locked python -m nbconvert --to notebook --execute notebooks/04a_modeling_lucas.ipynb --output lucas_ep3_executed.ipynb --output-dir "$env:TEMP" --ExecutePreprocessor.timeout=7200`. La ejecución completa fue reproducible con la fuente original, aunque tomó alrededor de una hora. Los avisos de limpieza temporal de joblib al cerrar no alteraron los resultados ni el código de salida (0).

- **Datos y partición:** SHA-256 de la fuente `b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd`; SHA-256 de los IDs de prueba `7270ff57b6fb81215fba2f834942d194183e3854ccac935a65e5a03f7888b318`; 71.792 canciones en entrenamiento y 17.948 en prueba. Son los mismos IDs y predictores de EA2. La prueba ya era conocida por EA2, por lo que la estimación final se interpreta con esa limitación.
- **Búsqueda IE9:** 12 configuraciones aleatorias reproducibles del espacio documentado arriba, 3 folds `KFold(shuffle=True, random_state=42)`, selección por menor MAE promedio. Se ajustó el preprocesamiento dentro de cada fold. Bosque `random_state=42`, `n_jobs=1`; la búsqueda empleó `n_jobs=4`, sin paralelismo anidado. Búsqueda más reajuste: 3.682 s. La tabla completa, incluidos parámetros, métricas por fold resumidas y tiempo promedio de ajuste, está en `reports/figures/ea3/04a_lucas_search.csv`.
- **Candidato IE10 fijado antes de prueba:** `RandomForestRegressor(n_estimators=100, min_samples_leaf=1, max_features=1.0, max_depth=None, random_state=42, n_jobs=1)`. MAE de CV **9,901 ± 0,018**; RMSE **14,768 ± 0,039**; R² **0,485 ± 0,003**. Ajuste promedio por fold de este candidato: **1.204 s**. Su MAE de entrenamiento en CV fue **3,767**, brecha de **6,133 puntos**: posible sobreajuste que requiere validar con artistas no vistos.

| Modelo | MAE CV ± DE | MAE prueba | RMSE prueba | R² prueba |
| --- | ---: | ---: | ---: | ---: |
| Dummy mediana | 17,224 ± 0,026 | 17,250 | 20,612 | −0,000 |
| Ridge | 11,819 ± 0,045 | 11,915 | 16,643 | 0,348 |
| Árbol | 14,382 ± 0,017 | 14,508 | 18,460 | 0,198 |
| Random Forest | **9,901 ± 0,018** | **9,648** | **14,536** | **0,502** |

El bosque redujo el MAE de prueba en **2,267 puntos** frente a Ridge y **44,1 %** frente a Dummy. En canciones `popularity >= 70`, su MAE fue **31,432** frente a **36,759** de Ridge; el sesgo siguió siendo negativo (**−31,418**), de modo que continúa subestimando las canciones más populares. En el 10 % superior predicho recuperó **237 de 653** canciones populares: precisión **13,20 %**, recall **36,29 %** y lift **3,629** ante una prevalencia de **3,64 %**. Ridge recuperó 159, con precisión 8,86 %, recall 24,35 % y lift 2,435. Estas cifras son un KPI retrospectivo, no accuracy ni garantía comercial.

Para IE11, Ignacio puede usar el notebook ejecutable y `reports/figures/ea3/04a_lucas_cv_comparison.csv`, `04a_lucas_test_comparison.csv`, `04a_lucas_segments.csv` y `04a_lucas_top_decile_kpi.csv`, además de la tabla de búsqueda. Las tablas de segmento incluyen cantidad de canciones, MAE, RMSE y sesgo para popularidad, contenido explícito y género; una canción puede figurar en varios géneros. La CV aleatoria no comprueba transferencia a artistas nuevos: esa es la validación pendiente de Ignacio. El bosque consume mucho más tiempo y muestra brecha de entrenamiento/validación, factores que César debe considerar al seleccionar la solución final para IE12. La muestra histórica fue balanceada artificialmente por género y no contiene exposición o fechas de lanzamientos futuros.

Para la defensa individual: `popularity` es continuo, por eso se optimizó MAE de regresión y se reportaron RMSE y R². El pipeline evitó fuga al ajustar transformaciones en cada fold. Random Forest disminuyó el error de validación, prueba y segmentos difíciles frente a Ridge, pero conserva subestimación de popularidad alta y tiene costo alto. El KPI del decil superior mide priorización retrospectiva; no es accuracy. Los clústeres K-Means y la proyección PCA siguen siendo evidencia exploratoria de EA2, no parte del ajuste IE9/IE10.

## Criterios de revisión

El notebook debe correr de inicio a fin, informar semilla, folds, parámetros, métricas y baseline, evitar fuga de datos y explicar si el ensamble aporta una mejora consistente. Al cerrarlo, Lucas entrega el handoff de IE11 a Ignacio. Según la rotación del plan del equipo, César revisa el PR de Lucas antes de integrarlo.

## Accuracy pendiente de definición

`popularity` es continuo; la métrica principal de este notebook sigue siendo de regresión. Si el docente confirma que requiere accuracy, coordinar antes de crear una variante de clasificación: clase objetivo, umbral, baseline y métricas complementarias. No usar como evidencia suficiente el accuracy de predecir siempre la clase mayoritaria.
