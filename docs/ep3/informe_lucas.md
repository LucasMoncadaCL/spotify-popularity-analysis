# Informe técnico individual EP3 — Lucas Moncada

## 1. Alcance y conclusión

Este informe documenta la implementación de **IE9 (optimización de hiperparámetros)** e **IE10 (ensamble)** para predecir la `popularity` histórica de canciones de Spotify. La implementación ejecutable está en [`04a_modeling_lucas.ipynb`](../../notebooks/04a_modeling_lucas.ipynb); las tablas y la figura generadas están en [`reports/figures/ea3`](../../reports/figures/ea3/). El [plan del equipo](plan_trabajo.md) asigna la validación de generalización por artista a Ignacio (IE11) y la selección final e integración a César (IE12).

El candidato elegido **antes de consultar las predicciones de prueba de EP3** fue un `RandomForestRegressor` de 100 árboles, sin límite de profundidad, con una observación mínima por hoja y todas las variables disponibles por división. En validación cruzada obtuvo MAE **9,901 ± 0,018**; en la prueba compartida, **9,648**, frente a **11,915** de Ridge. La mejora observada debe sopesarse con un ajuste mucho más lento, una brecha de MAE de **6,133** puntos entre entrenamiento y validación, y un MAE de **31,432** en canciones con popularidad de 70 o más. Este es un **candidato para IE11/IE12**, no la solución final elegida por el equipo.

| Requisito de Lucas | Evidencia |
| --- | --- |
| IE9: espacio, búsqueda y selección reproducible | Sección 10.1 del notebook; [`04a_lucas_search.csv`](../../reports/figures/ea3/04a_lucas_search.csv), 12 configuraciones y 3 folds. |
| IE10: al menos un ensamble y comparación justa | Secciones 10.2–10.3; [`04a_lucas_cv_comparison.csv`](../../reports/figures/ea3/04a_lucas_cv_comparison.csv) y [`04a_lucas_test_comparison.csv`](../../reports/figures/ea3/04a_lucas_test_comparison.csv). |
| Diagnósticos y criterio de negocio | [`04a_lucas_segments.csv`](../../reports/figures/ea3/04a_lucas_segments.csv), [`04a_lucas_top_decile_kpi.csv`](../../reports/figures/ea3/04a_lucas_top_decile_kpi.csv) y secciones 7–9 de este informe. |
| Reproducción y handoff | Secciones 10–12 de este informe y [`lucas.md`](lucas.md). |

## 2. Problema y decisión sobre la métrica

`popularity` es una variable numérica continua de 0 a 100. Por ello se resolvió como **regresión**. La métrica de selección fue el **MAE** o error absoluto medio, expresado en puntos de popularidad: facilita comparar cuánto se equivoca el modelo en la escala original. También se registraron **RMSE**, que da más peso a los errores grandes, y **R²**, que compara el error cuadrático del modelo con el de predecir la media. Un R² alto no prueba causalidad ni utilidad comercial.

No se convirtió el objetivo a una clase binaria para perseguir el “accuracy 80 %” mencionado verbalmente. La pauta no define esa etiqueta ni un umbral de accuracy para el modelo. En esta prueba solo **653 de 17.948 canciones (3,64 %)** tienen `popularity >= 70`; un clasificador que predijera siempre “no popular” alcanzaría **96,36 % de accuracy** y no encontraría ninguna canción popular. El corte de 70 se usa únicamente para analizar errores y el ranking retrospectivo. La precisión del ranking se refiere a las canciones seleccionadas, no al accuracy global de una clasificación.

## 3. Datos, preparación y separación

La fuente es [`data/raw/Spotify_Tracks_Dataset.csv`](../../data/raw/Spotify_Tracks_Dataset.csv), con SHA-256 `b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd`. El notebook la carga con `load_raw_dataset()` y aplica `prepare_modeling_dataset()` del código compartido. De **114.000 filas** originales se excluyó **una** inválida y se consolidaron **24.259** filas repetidas por `track_id`, hasta obtener **89.740 canciones únicas**. Los atributos invariantes deben concordar entre filas del mismo ID; la popularidad se agrega por mediana y los géneros se unen como etiquetas. Se comprueba ausencia de IDs duplicados, datos faltantes, duraciones no positivas y géneros vacíos. Estas reglas vienen de la preparación común, no se modificaron para obtener mejores resultados EP3.

Se mantuvo el protocolo de EA2 (`split_track_ids`, semilla **42**): **71.792** canciones para entrenamiento y **17.948** para prueba. La huella SHA-256 de los IDs de prueba ordenados es `7270ff57b6fb81215fba2f834942d194183e3854ccac935a65e5a03f7888b318`. Todos los modelos se compararon sobre esos mismos IDs. El conjunto de prueba **ya había sido observado en EA2**; por eso constituye una comparación compartida útil, pero no una prueba inédita para el proyecto. La elección de hiperparámetros de este experimento se hizo dentro de entrenamiento, antes de evaluar al nuevo bosque en esa prueba.

Los predictores son los diez atributos numéricos `duration_ms`, `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence` y `tempo`; las cuatro variables categóricas `key`, `mode`, `time_signature` y `explicit`; y `track_genres` como etiquetas múltiples. `track_id`, nombres, artistas y `popularity` **no son predictores**. El `model_pipeline` común estandariza numéricos, aplica one-hot a las categorías y binariza los géneros. El transformador de géneros aprende sus etiquetas solo en las filas de ajuste y omite etiquetas desconocidas al transformar. El pipeline completo se ajusta por separado en cada fold, lo que evita que las transformaciones aprendan de la validación o de la prueba.

La separación aleatoria por canción puede dejar canciones del mismo artista a ambos lados. Eso no es una fuga de preprocesamiento, pero sí limita lo que puede afirmarse sobre artistas nuevos. Ignacio evaluará esa transferencia con particiones agrupadas en IE11.

## 4. Referencias y elección del ensamble

Se compararon cuatro candidatos sobre los mismos predictores y particiones:

| Modelo | Configuración | Función en la comparación |
| --- | --- | --- |
| Dummy mediana | `DummyRegressor(strategy="median")` | Referencia sin aprendizaje de relaciones entre atributos y popularidad. |
| Ridge | `alpha=0.1`, con pipeline común | Referencia lineal regularizada ya fijada en EA2; ajuste rápido. |
| Árbol | `max_depth=15`, `min_samples_leaf=20`, `random_state=42`, con pipeline común | Referencia no lineal de EA2, interpretable por reglas pero propensa a inestabilidad. |
| Random Forest | `random_state=42`, `n_jobs=1`, con pipeline común | Promedia múltiples árboles para explorar relaciones no lineales e interacciones entre atributos. |

Ridge y árbol conservaron parámetros históricos de EA2; no se reajustaron a partir de la prueba. El Dummy no necesita transformación de atributos porque predice la mediana del objetivo de entrenamiento. Se eligió **un** ensamble para el alcance obligatorio: la búsqueda completa consumió **3.682 s** de pared, incluido el reajuste del mejor bosque. Un segundo ensamble era opcional y requeriría otra comparación costosa antes de aportar una conclusión clara.

## 5. Búsqueda de hiperparámetros IE9

`RandomizedSearchCV` exploró **12 de 144 combinaciones** posibles, con `random_state=42`, `KFold(n_splits=3, shuffle=True, random_state=42)`, selección y reajuste por **menor MAE medio de validación** (`refit="MAE"`). Son **36 ajustes de búsqueda** más un reajuste del ganador con las 71.792 canciones de entrenamiento. `n_jobs=4` en la búsqueda y `n_jobs=1` dentro de cada bosque evitan paralelismo anidado. Se registraron MAE, RMSE, R², sus desviaciones entre folds, MAE de entrenamiento y tiempo medio de ajuste. Las métricas secundarias no cambiaron el criterio de elección.

| Parámetro | Valores explorados | Razón de incluirlo |
| --- | --- | --- |
| `n_estimators` | 100, 200, 300 | Más árboles pueden estabilizar el promedio, con mayor tiempo y memoria. |
| `max_depth` | 10, 15, 25, `None` | Contrasta árboles limitados con árboles capaces de ajustar patrones más específicos. |
| `min_samples_leaf` | 1, 2, 5, 10 | Hojas mayores suavizan predicciones y pueden reducir sobreajuste. |
| `max_features` | `"sqrt"`, 0.5, 1.0 | Controla cuántos predictores compiten por división y la diversidad entre árboles. |

La búsqueda aleatoria fue una forma reproducible de limitar el costo frente a una cuadrícula completa de **432 ajustes de CV** (144 × 3), sin afirmar que haya encontrado el óptimo global. La tabla completa de las 12 configuraciones está en [`04a_lucas_search.csv`](../../reports/figures/ea3/04a_lucas_search.csv). La mejor combinación fue `n_estimators=100`, `max_depth=None`, `min_samples_leaf=1`, `max_features=1.0`; su MAE de CV fue **9,901**, frente a **11,671** de la segunda configuración probada. La combinación ganadora permite árboles muy flexibles y explica por qué se revisó explícitamente la brecha entre entrenamiento y validación; la diferencia entre configuraciones no demuestra por sí sola qué hiperparámetro causó la mejora, pues cambiaron varios a la vez.

## 6. Resultados y costo

**Validación cruzada dentro de entrenamiento.** Cada valor “±” es la desviación estándar entre los **tres** folds, no un intervalo de confianza. Las referencias pasaron por los mismos folds que el bosque. Los tiempos por fold son de esta ejecución y dependen del equipo; el paralelismo hace que su suma no sea tiempo de pared.

| Modelo | MAE CV ± DE | RMSE CV ± DE | R² CV ± DE | MAE entrenamiento CV | Ajuste medio/fold |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dummy mediana | 17,224 ± 0,026 | 20,570 ± 0,027 | −0,000 ± 0,000 | 17,224 | 0,22 s |
| Ridge | 11,819 ± 0,045 | 16,521 ± 0,069 | 0,355 ± 0,005 | 11,782 | 0,33 s |
| Árbol | 14,382 ± 0,017 | 18,319 ± 0,029 | 0,207 ± 0,001 | 14,235 | 1,19 s |
| Random Forest | **9,901 ± 0,018** | **14,768 ± 0,039** | **0,485 ± 0,003** | **3,767** | **1.204 s** |

El bosque muestra una brecha de **9,901 − 3,767 = 6,133 puntos de MAE** entre validación y entrenamiento. Es una señal de ajuste fuerte a las canciones vistas; su MAE de validación y de prueba sigue siendo mejor que las referencias en esta partición. La desviación pequeña de solo tres folds aleatorios no resuelve el riesgo de transferencia a otros artistas o épocas.

**Prueba compartida tras fijar el candidato.** Las predicciones finales se obtuvieron ajustando cada referencia con todo el entrenamiento y usando el `best_estimator_` reajustado del bosque.

| Modelo | MAE prueba | RMSE prueba | R² prueba | Mejora MAE frente a Dummy |
| --- | ---: | ---: | ---: | ---: |
| Dummy mediana | 17,250 | 20,612 | −0,000 | 0,0 % |
| Ridge | 11,915 | 16,643 | 0,348 | 30,9 % |
| Árbol | 14,508 | 18,460 | 0,198 | 15,9 % |
| Random Forest | **9,648** | **14,536** | **0,502** | **44,1 %** |

El bosque redujo el MAE de prueba en **2,267 puntos** (**19,0 %**) respecto de Ridge y en **7,602 puntos** respecto de Dummy. También tuvo el menor RMSE y el mayor R² entre los cuatro modelos de esta comparación. La figura [`04a_lucas_cv_test_mae.png`](../../reports/figures/ea3/04a_lucas_cv_test_mae.png) permite cotejar MAE de CV y prueba. Esta evidencia favorece al bosque para este conjunto histórico; César decidirá si el beneficio compensa el costo y si se sostiene tras IE11.

## 7. Diagnósticos de errores

Los segmentos se definieron **después de entrenar y predecir**, sin usarlos para elegir parámetros. El sesgo es `predicho − observado`: positivo significa sobreestimación y negativo, subestimación. El MAE y RMSE se calculan sobre las canciones de cada segmento; la columna `canciones` indica su soporte.

| Popularidad observada | Canciones | MAE Ridge | MAE bosque | Sesgo bosque |
| --- | ---: | ---: | ---: | ---: |
| 0 | 1.863 | 24,448 | **14,192** | +14,192 |
| (0,35) | 7.361 | 8,040 | **7,187** | +5,528 |
| [35,70) | 8.071 | 10,546 | **9,081** | −6,904 |
| [70,100] | 653 | 36,759 | **31,432** | −31,418 |

El ensamble mejora el MAE en los cuatro rangos frente a Ridge, incluido el más popular. Sin embargo, sigue sobreestimando canciones de popularidad cero y **subestimando marcadamente** las de 70 o más. Una mejora en el promedio global no elimina ese límite de uso.

En canciones no explícitas (16.431), el MAE del bosque fue **9,546** frente a **11,704** de Ridge; en explícitas (1.517), **10,756** frente a **14,198**. La diferencia entre grupos es descriptiva y no permite atribuirla al contenido explícito: también pueden cambiar géneros y otros atributos. La tabla completa contiene los errores por **114 etiquetas de género** para cada modelo. Una canción puede pertenecer a varios géneros; por ello, los soportes de género no suman 17.948 y no deben interpretarse como grupos independientes. Algunas etiquetas tienen pocos casos y sus MAE son inestables. No se usó ninguna de estas cifras para reajustar el bosque.

## 8. KPI retrospectivo del 10 % superior

La función común `top_decile_kpi` ordena las **17.948** canciones de prueba por popularidad predicha (desempata por `track_id`) y selecciona `ceil(0,10 × 17.948) = 1.795`. Una canción cuenta como “popular” para este diagnóstico si su popularidad observada es **≥ 70**. Hay **653** populares en la prueba, prevalencia **3,638 %**. La precisión es populares dentro de 1.795 seleccionadas; el recall es populares seleccionadas entre las 653 disponibles; el lift divide esa precisión por la prevalencia.

| Modelo | Populares seleccionadas | Precisión | Recall | Lift |
| --- | ---: | ---: | ---: | ---: |
| Dummy mediana | 63 | 3,51 % | 9,65 % | 0,965 |
| Ridge | 159 | 8,86 % | 24,35 % | 2,435 |
| Árbol | 119 | 6,63 % | 18,22 % | 1,822 |
| Random Forest | **237** | **13,20 %** | **36,29 %** | **3,629** |

El bosque encuentra **78** canciones populares más que Ridge en la misma capacidad de selección. Aun así, **1.558 de sus 1.795 seleccionadas** no alcanzan 70 y **416 de las 653 populares** quedan fuera. El KPI describe priorización retrospectiva en esta muestra, no accuracy, causalidad, éxito futuro ni una recomendación automática de promoción.

## 9. Interpretación y límites

- **Beneficio observado:** el bosque mejora MAE, RMSE, R² y el KPI del decil superior frente a Dummy, Ridge y árbol en esta prueba compartida. También reduce el error de las canciones de popularidad alta, aunque ese sigue siendo el segmento con mayor MAE.
- **Costo y complejidad:** el ganador requirió aproximadamente **1.204 s de ajuste medio por fold** y **3.682 s** de búsqueda más reajuste, frente a menos de dos segundos por fold para las referencias. El tiempo depende de hardware, memoria y paralelismo. Ridge puede seguir siendo preferible si la mejora no justifica ese costo operativo.
- **Sobreajuste y generalización:** el MAE de entrenamiento del bosque (3,767) es mucho menor que su MAE de CV (9,901). Los folds aleatorios separan canciones, no artistas. IE11 debe comprobar artistas principales no vistos; incluso esa separación puede conservar artistas secundarios compartidos. Tampoco hay validación temporal.
- **Datos y uso:** la fuente histórica fue balanceada artificialmente por género; no representa necesariamente la distribución de nuevos lanzamientos ni incluye exposición, inversión promocional o fechas que expliquen popularidad. Los errores por género y `explicit` no establecen causas ni justifican tratar de forma distinta a personas o artistas. Cualquier uso de priorización requiere revisión humana y evaluación en datos representativos del contexto real.
- **Prueba conocida:** EA2 ya había expuesto la partición de prueba al equipo. Las cifras EP3 deben presentarse con esa reserva; seleccionar otro candidato tras verlas invalidaría el criterio de elección anunciado.

Los clústeres K-Means y la proyección PCA del proyecto provienen de EA2. Son análisis exploratorios y no forman parte del ajuste de hiperparámetros IE9/IE10. César puede integrarlos en el relato global sin presentarlos como evidencia de que el bosque causa popularidad.

## 10. Reproducción y trazabilidad

El repositorio fija Python **3.12** y dependencias mediante `uv.lock`. La ejecución registrada usó Python **3.12.10**, scikit-learn **1.9.0** y pandas **2.3.3**. Desde la raíz del repositorio en PowerShell:

```powershell
uv run --locked python -m nbconvert --to notebook --execute notebooks/04a_modeling_lucas.ipynb --output lucas_ep3_executed.ipynb --output-dir "$env:TEMP" --ExecutePreprocessor.timeout=7200
```

El comando lee el CSV en `data/raw/Spotify_Tracks_Dataset.csv`, ejecuta el notebook de inicio a fin y escribe una copia ejecutada temporal. Las tablas y la figura nuevas se regeneran en `reports/figures/ea3/`; el notebook fuente conserva las salidas de la ejecución verificada. La ejecución completa finalizó con código de salida **0**. Durante el cierre aparecieron mensajes de limpieza de archivos temporales de joblib; no se produjo una excepción de celda ni faltó ningún archivo de resultados. No se requieren rutas personales dentro del código.

| Archivo | Contenido y uso |
| --- | --- |
| [`04a_lucas_search.csv`](../../reports/figures/ea3/04a_lucas_search.csv) | Las 12 configuraciones, ranking, medias/DE de CV y tiempos de ajuste. |
| [`04a_lucas_cv_comparison.csv`](../../reports/figures/ea3/04a_lucas_cv_comparison.csv) | Cuatro modelos en los mismos folds, métricas de entrenamiento y brecha de MAE. |
| [`04a_lucas_test_comparison.csv`](../../reports/figures/ea3/04a_lucas_test_comparison.csv) | Métricas de los cuatro modelos sobre los mismos IDs de prueba. |
| [`04a_lucas_segments.csv`](../../reports/figures/ea3/04a_lucas_segments.csv) | Cantidad de canciones, MAE, RMSE y sesgo por popularidad, contenido explícito y género. |
| [`04a_lucas_top_decile_kpi.csv`](../../reports/figures/ea3/04a_lucas_top_decile_kpi.csv) | Capacidad, populares recuperadas, prevalencia, precisión, recall y lift. |
| [`04a_lucas_cv_test_mae.png`](../../reports/figures/ea3/04a_lucas_cv_test_mae.png) | Comparación visual de MAE de CV y prueba. |

Las cifras de este informe están redondeadas para lectura; los CSV conservan los valores calculados. La semilla, las huellas y los parámetros seleccionados también aparecen en las salidas del notebook.

## 11. Handoff concreto

**Para Ignacio (IE11):** usar el mismo `model_pipeline`, los mismos predictores y `SEED=42`. El candidato es `RandomForestRegressor(n_estimators=100, max_depth=None, min_samples_leaf=1, max_features=1.0, random_state=42, n_jobs=1)`. La selección IE9 usó 3 folds aleatorios con `shuffle=True` y semilla 42; los resultados de CV/prueba y el costo están en las tablas anteriores. Comparar este candidato con Ridge y árbol mediante particiones por artista principal, sin ajustar según el test ya conocido. Declarar el posible solapamiento de artistas secundarios. La validación agrupada puede requerir presupuesto de cómputo separado por el tiempo de ajuste del bosque.

**Para César (IE12):** contrastar el bosque con la evidencia de generalización de Ignacio, su costo, brecha entrenamiento/CV, errores por segmento y KPI. Si se recomienda, explicar las condiciones de uso y la revisión humana; si no se recomienda, documentar qué criterio pesa más que la mejora de MAE en esta prueba. La integración de notebook 05, README, informe y presentación corresponde a César. El “accuracy 80 %” sigue sin definición formal y no se declara alcanzado.

## 12. Guion breve para defensa individual

1. **Problema:** predecimos popularidad histórica en escala 0–100; por eso MAE, RMSE y R², no accuracy de clasificación.
2. **Comparación justa:** conservamos fuente, canciones únicas, predictores, semilla y prueba de EA2; toda elección nueva se hizo con CV dentro del entrenamiento y el preprocesamiento se ajustó dentro de cada fold.
3. **IE9:** exploramos 12 combinaciones de cantidad de árboles, profundidad, hojas y variables por división; elegimos menor MAE medio de 3 folds, registrando dispersión y costo.
4. **IE10:** Random Forest llegó a MAE 9,648 en prueba frente a 11,915 de Ridge; también recuperó 237 canciones populares en el decil superior frente a 159 de Ridge.
5. **Límites:** cuesta mucho más, muestra brecha de entrenamiento/CV, subestima las canciones más populares y aún falta la prueba por artista nuevo. El dataset y el KPI son históricos; K-Means/PCA son exploratorios. La recomendación final requiere IE11 e IE12.
