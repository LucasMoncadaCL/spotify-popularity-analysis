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


### Definición, fórmula e interpretación de los indicadores

Para los indicadores predictivos, `yᵢ` es la popularidad observada y `ŷᵢ` la estimación. MAE y RMSE se expresan en puntos de popularidad (0–100); R² es adimensional. En un conjunto de evaluación fijo, menor MAE/RMSE es mejor y mayor R² es mejor, aunque R² puede ser negativo.

| Indicador | Fórmula / definición | Interpretación y sentido |
|---|---|---|
| MAE | `(1/n) × Σ |yᵢ − ŷᵢ|` | Error absoluto promedio; menor es mejor. Se interpreta directamente en puntos de popularidad. |
| RMSE | `sqrt((1/n) × Σ (yᵢ − ŷᵢ)²)` | Error cuadrático medio en la escala original; penaliza más las desviaciones grandes. Menor es mejor. |
| R² | `1 − Σ(yᵢ − ŷᵢ)² / Σ(yᵢ − ȳ)²` | Compara con predecir la media observada del conjunto evaluado. 1 es perfecto, 0 equivale a esa referencia y <0 indica peor ajuste que ella. No es accuracy. |
| Prevalencia ≥70 | `positivos / n`, donde positivo significa `popularity ≥ 70` | Proporción histórica de canciones del conjunto que alcanza el umbral. |
| Precisión del decil | `positivos entre las k seleccionadas / k`; `k = ceil(0,10 × n)` | Fracción popular dentro de las canciones con mayores predicciones; mayor describe mejor priorización retrospectiva. |
| Recall del decil | `positivos seleccionados / total de positivos` | Fracción de canciones históricamente populares recuperada por el decil; mayor es mejor para cobertura. |
| Lift del decil | `precisión / prevalencia` | Mejora relativa respecto de seleccionar canciones sin ranking; 1 equivale a la prevalencia base. |
| Brecha MAE | `MAE_validación − MAE_entrenamiento` | Diferencia de error entre datos no usados/usados en el ajuste; una brecha positiva grande alerta sobre sobreajuste. |
| Tiempo de ajuste | Segundos medidos durante `.fit()` | Costo de entrenamiento bajo el hardware y configuración registrados; menor facilita iteración, pero no compensa automáticamente menor calidad. |
| Completitud | `celdas no nulas / total de celdas` | Control de calidad de datos; más cercano a 100 % implica menos valores ausentes, sin garantizar validez semántica. |
| Duplicidad de ID | `track_id` duplicados después de preparar / filas preparadas | Debe ser 0 para que una canción no pese varias veces ni cruce entre entrenamiento y prueba. |

El top 10 % y el umbral 70 se usan como KPI retrospectivo porque la popularidad del dataset ya fue observada. Ninguna de esas cifras prueba rentabilidad, una acción promocional efectiva ni éxito de una canción futura. Tampoco corresponde interpretar el 80 % mencionado verbalmente como accuracy de este modelo de regresión sin una definición de objetivo y métrica.

## Metodología y estado

El equipo sigue CRISP-DM de forma iterativa. Los notebooks 01–03 documentan comprensión, preparación y EDA; los notebooks 04a–05 conservan las contribuciones del equipo y `06_ep3_final.ipynb` reproduce el análisis integrado EP3 desde el CSV original.

| Fase CRISP-DM | Aplicación en el proyecto | Estado |
|---|---|---|
| Business Understanding | Problema, usuarios, objetivos e indicadores. | Documentada en el notebook 01. |
| Data Understanding | Fuente, variables, estructura, calidad y distribuciones iniciales. | Documentada en 01 y ampliada en 03. |
| Data Preparation | Limpieza, deduplicación por `track_id`, consolidación de géneros y validaciones. | Reproducible en 02 y `src/`. |
| Modeling | Dummy mediana, Ridge, árbol, Random Forest optimizado, variantes y K-Means. | Reproducible en 04a–04c, 05 y 06. |
| Evaluation | Métricas, errores por segmentos, KPI retrospectivo, artistas y sensibilidad. | Integrada y ejecutada en 06. |
| Deployment | Comunicación reproducible en notebook, informe y presentación. | Informe y presentación EP3 preparados; no hay despliegue operativo. |


### Desarrollo de las seis fases CRISP-DM

1. **Comprensión del negocio.** Se acota la pregunta a estimar la popularidad observada en la fuente y explorar patrones útiles para priorizar análisis de catálogo. No se promete anticipar éxitos futuros ni atribuir causalidad.
2. **Comprensión de los datos.** Se revisan fuente, diccionario, esquema, distribuciones, popularidad objetivo, relaciones entre atributos, duplicados por canción y sesgos de la muestra. Los notebooks 01 y 03 documentan este levantamiento; el notebook 06 vuelve a producir EDA esencial.
3. **Preparación de los datos.** Se retira una fila sin identificación útil, se consolidan apariciones por `track_id`, se preservan los géneros multietiqueta y se valida el rango/completitud. Las codificaciones y escalados se ajustan dentro de cada pipeline y solo sobre el fold de entrenamiento correspondiente.
4. **Modelamiento.** Se usa `DummyRegressor` como referencia y se comparan Ridge, árbol y Random Forest para regresión; se estudian transformaciones de duración y escalado; K-Means identifica perfiles sin incluir `popularity`. PCA se usa como proyección de visualización.
5. **Evaluación.** Se mantienen protocolos separados: prueba aleatoria por canción, holdout por artista principal y GroupKFold. Selección de parámetros ocurre en entrenamiento/validación; la prueba no guía la selección. Se informan MAE/RMSE/R², KPI retrospectivo, segmentos, incertidumbre entre folds, tiempo y solapamientos secundarios.
6. **Despliegue/propuesta.** El proyecto entrega un análisis reproducible para apoyar una revisión humana del catálogo. No existe servicio productivo, integración con Spotify ni evaluación de lanzamientos posteriores. Antes de cualquier uso real se necesitarían datos actuales con fecha, exposición y resultados futuros, evaluación temporal, monitoreo y revisión de sesgo.

### Entregables y evidencia del proyecto

| Entregable | Contenido |
|---|---|
| [`01_data_understanding.ipynb`](notebooks/01_data_understanding.ipynb) | Problema, objetivos, KPIs, fuente y comprensión inicial. |
| [`02_data_preparation.ipynb`](notebooks/02_data_preparation.ipynb) | Preparación reproducible y validaciones de calidad. |
| [`03_exploratory_analysis.ipynb`](notebooks/03_exploratory_analysis.ipynb) | EDA, relaciones, sesgos, ética y privacidad. |
| [`04a_modeling_lucas.ipynb`](notebooks/04a_modeling_lucas.ipynb) | Núcleo común y comparación del aporte de géneros. |
| [`04b_modeling_ignacio.ipynb`](notebooks/04b_modeling_ignacio.ipynb) | Núcleo común y sensibilidad a duración/escalado. |
| [`04c_modeling_cesar.ipynb`](notebooks/04c_modeling_cesar.ipynb) | Núcleo común, errores por segmentos y partición por artista principal. |
| [`05_model_comparison.ipynb`](notebooks/05_model_comparison.ipynb) | Integra la comparación común EA2, K-Means/PCA, segmentos y validación por artista. |
| [`06_ep3_final.ipynb`](notebooks/06_ep3_final.ipynb) | Informe ejecutado desde kernel limpio: EDA, búsqueda RF, pruebas aleatoria/agrupada, segmentos, KPI, GroupKFold y K-Means/PCA. |
| [`docs/ep3/decision_cesar.md`](docs/ep3/decision_cesar.md) | Justifica la selección IE12, compara escenarios, métricas, complejidad y límites. |
| [`docs/ep3/auditoria_final.md`](docs/ep3/auditoria_final.md) | Matriz de cumplimiento IE9–IE12, evidencia y límites de la entrega. |
| [`docs/ep3/guion_defensa.md`](docs/ep3/guion_defensa.md) | Guion de 9 minutos 35 segundos y respuestas a preguntas técnicas. |
| [`output/presentations/spotify_popularity_ea2_final.pptx`](output/presentations/spotify_popularity_ea2_final.pptx) | Presentación base de EA2 conservada para trazabilidad. |
| [`output/presentations/spotify_popularity_ep3_final.pptx`](output/presentations/spotify_popularity_ep3_final.pptx) | Presentación integrada de EP3, 12 láminas y notas para exposición. |

El notebook [`06_ep3_final.ipynb`](notebooks/06_ep3_final.ipynb) es el punto de entrada integrado y vuelve a ejecutar los experimentos a partir del CSV original. Los notebooks 04a–05 conservan el detalle de las contribuciones y sus protocolos.

### Integración EP3: optimización, ensamble y selección IE12

Los notebooks 04a y 04b documentan las contribuciones originales de Lucas e Ignacio. La sección 10 de `06_ep3_final.ipynb` vuelve a preparar el CSV original, ejecuta desde cero la búsqueda de Random Forest y los tres folds GroupKFold, sin leer CSV antiguos para calcular métricas. El notebook completó 32 celdas (15 de código) desde un kernel limpio, sin errores; su manifiesto registra SHA-256, versiones y tiempos. Los CSV de `reports/figures/ea3/06_*` se regeneran con esa ejecución.

Para IE9, RandomizedSearchCV evaluó 12 de 144 configuraciones en 3 folds y seleccionó por MAE; el ganador de Random Forest coincide con los parámetros por defecto de scikit-learn 1.9.0, así que no se afirma una mejora frente al default. La ejecución limpia del notebook 06 tomó 4.310,6 s (71,8 min) en la búsqueda y refit, con cuatro procesos externos y `n_jobs=1` dentro de cada bosque. Notebook 05 valida Ridge y árbol en una partición interna separada del test y escribe `reports/figures/ea3/05_cesar_hyperparameter_validation.csv`: Ridge reduce MAE de validación de 11,7883 a 11,7855 (0,023 %) y el árbol no mejora respecto del default. No es una búsqueda anidada.

| Escenario | Modelo | MAE | RMSE | R² | Lectura |
|---|---|---:|---:|---:|---|
| Prueba aleatoria por canción (Lucas) | Ridge | 11,915 | 16,643 | 0,348 | Referencia lineal; la partición puede compartir artistas. |
| Prueba aleatoria por canción (Lucas) | Random Forest | **9,648** | **14,536** | **0,502** | Menor error observado en esta partición; brecha MAE train–CV de 6,133. |
| GroupKFold por artista principal, media de 3 folds (Ignacio) | Ridge | 12,061 ± 0,408 | **16,858 ± 0,650** | **0,328 ± 0,045** | Modelo recomendado para el escenario de principales no vistos: sencillo, rápido y con métricas comparables. |
| GroupKFold por artista principal, media de 3 folds (Ignacio) | Random Forest | **11,752 ± 0,458** | 16,969 ± 0,770 | 0,319 ± 0,055 | Gana 0,309 puntos de MAE; brecha train–validación de 8,060 y ajuste cercano a 1.086 s por fold. |
| Holdout agrupado independiente 04c | Ridge | 12,102 | 16,740 | 0,302 | Validación interna agrupada; 18.193 canciones reservadas. |
| Holdout agrupado independiente 04c | Árbol depth=15/leaf=100 | 14,455 | 18,247 | 0,171 | Validación interna agrupada. No incluye Random Forest. |

La selección depende del escenario: Random Forest es preferible si el único objetivo es minimizar MAE en la partición aleatoria de canciones. Para artistas principales no vistos, Ridge es una referencia prudente: en GroupKFold tiene RMSE menor, R² mayor y un costo de ajuste mucho menor; en el holdout independiente 04c supera al árbol, pero RF no fue evaluado en ese holdout. Solo hay tres folds y sus desviaciones estándar no demuestran significancia. Los protocolos agrupados separan artistas principales, pero conservan colaboradores secundarios compartidos. El bosque fue preseleccionado en CV aleatoria, así que el GroupKFold de candidatos fijos no equivale a una búsqueda anidada independiente.

La evaluación integrada de Notebook 05 completa el núcleo aleatorio supervisado. La tabla combina Dummy/Ridge/árbol seleccionados en esa validación con el Random Forest ya evaluado por Lucas. Los valores de Dummy y Ridge coinciden con Lucas y sirven para verificar el split común; el árbol de Notebook 05 (`max_depth=None`, `min_samples_leaf=1`) difiere del árbol de Lucas (`max_depth=15`, `min_samples_leaf=20`), por lo que se etiqueta su configuración y no se intercambian sus métricas.

| Modelo | Configuración evaluada | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Dummy mediana | Referencia | 17,250 | 20,612 | -0,000 |
| Ridge | α = 0,1 seleccionado en validación | 11,915 | 16,643 | 0,348 |
| Árbol | Default seleccionado en validación | 12,012 | 19,572 | 0,098 |
| Random Forest | 100 árboles; candidato de Lucas | **9,648** | **14,536** | **0,502** |

Estos resultados corresponden a la prueba de canciones con semilla 42. El árbol default de Notebook 05 (MAE 12,012) y el árbol depth=15/leaf=20 de Lucas (MAE 14,508, reproducido por Notebook 06) son configuraciones distintas; el bosque se compara con la segunda en la tabla EP3. El bosque reduce MAE 33,5 % frente al árbol congelado de Lucas y 19,7 % frente al árbol default de Notebook 05. Los resultados de artistas agrupados se mantienen aparte.

La prueba por canción y la CV por artista responden preguntas diferentes; no deben ordenarse como si fueran la misma partición. La popularidad es histórica, la muestra está balanceada artificialmente por género y no hay fechas, exposición o contexto comercial. El KPI retrospectivo tampoco demuestra éxito futuro ni utilidad comercial. «Accuracy 80 %» sigue pendiente de definición del docente: este trabajo resuelve regresión, y MAE/R² no son accuracy.

La presentación de 12 láminas y su guion se enlazan arriba. La rúbrica escrita asigna el nivel “Buen desempeño” a una banda de 80 %; eso no impone 80 % de accuracy al modelo. La frase oral sobre accuracy requiere aclarar objetivo, umbral y métrica con el docente.

### Resultados reproducidos por el notebook 06

Las siguientes tablas provienen de la ejecución completa desde un kernel limpio, con scikit-learn 1.9.0. La prueba aleatoria comparte los mismos ID de prueba usados en la integración previa (SHA-256 `7270ff57b6fb81215fba2f834942d194183e3854ccac935a65e5a03f7888b318`). Dummy, Ridge y árbol se mantienen como referencia; la comparación EP3 usa el árbol congelado de Lucas (`max_depth=15`, `min_samples_leaf=20`), por lo que su resultado difiere del árbol por defecto seleccionado por el notebook 05.

| Protocolo aleatorio | Modelo/configuración | MAE | RMSE | R² |
|---|---|---:|---:|---:|
| Prueba por canción | Dummy mediana | 17,250 | 20,612 | -0,000 |
| Prueba por canción | Ridge, α=0,1 | 11,915 | 16,643 | 0,348 |
| Prueba por canción | Árbol, depth=15/leaf=20 | 14,508 | 18,460 | 0,198 |
| Prueba por canción | Random Forest, 100 árboles/depth sin límite/leaf=1/max_features=1,0 | **9,648** | **14,536** | **0,502** |

La validación aleatoria de RF fue MAE `9,9005 ± 0,0176`, RMSE `14,7681 ± 0,0388` y R² `0,4845 ± 0,0031`; su MAE medio de entrenamiento fue 3,7674 y la brecha fue 6,1331 puntos. El tiempo medio de ajuste por fold de la configuración ganadora fue 1.554,0 s; la búsqueda completa y su refit tardaron 4.310,6 s.

| KPI retrospectivo del decil superior | Seleccionadas | Populares recuperadas / total ≥70 | Precisión | Recall | Lift |
|---|---:|---:|---:|---:|---:|
| Prevalencia de prueba | — | 653/17.948 | — | — | — |
| Ridge | 1.795 | 159/653 | 8,86 % | 24,35 % | 2,435 |
| Random Forest | 1.795 | 237/653 | 13,20 % | 36,29 % | 3,629 |

Los errores de RF varían con popularidad y contenido explícito; cada fila informa soporte. Son mediciones de la misma prueba aleatoria, no predicciones futuras.

| Segmento de la prueba | Canciones | MAE de RF |
|---|---:|---:|
| Popularidad = 0 | 1.863 | 14,192 |
| Popularidad (0,35) | 7.361 | 7,187 |
| Popularidad [35,70) | 8.071 | 9,081 |
| Popularidad [70,100] | 653 | 31,432 |
| No explícita | 16.431 | 9,546 |
| Explícita | 1.517 | 10,756 |

#### Generalización por artista principal

GroupKFold usa tres folds del entrenamiento aleatorio, con cero artistas principales compartidos entre ajuste y validación. En cada fold se observaron entre 3.032 y 3.093 canciones de validación con artistas secundarios presentes en el ajuste; por ello el aislamiento es por artista principal, no por toda colaboración.

| GroupKFold (media ± desviación estándar) | MAE | RMSE | R² | Brecha MAE | Ajuste medio/fold |
|---|---:|---:|---:|---:|---:|
| Ridge | 12,061 ± 0,408 | **16,858 ± 0,650** | **0,328 ± 0,045** | 0,324 | 0,370 s |
| Random Forest | **11,752 ± 0,458** | 16,969 ± 0,770 | 0,319 ± 0,055 | 8,060 | 1.086,1 s |

En esta evaluación el bosque gana 0,309 puntos de MAE, pero Ridge obtiene mejor RMSE y R², una brecha de entrenamiento mucho menor y un costo de ajuste muy inferior. La diferencia pequeña de MAE entre tres folds no demuestra significancia. La decisión IE12 sigue condicionada al uso: RF lidera para canciones retenidas similares a la muestra; Ridge es una referencia más prudente para artistas principales no vistos. Ninguno demuestra éxito comercial futuro.

La ejecución y artefactos se conservan en [`notebooks/06_ep3_final.ipynb`](notebooks/06_ep3_final.ipynb), [`reports/figures/ea3/06_ep3_manifest.json`](reports/figures/ea3/06_ep3_manifest.json) y las tablas `06_*` de `reports/figures/ea3/`.

## Resultados del núcleo de Notebook 05 (sin Random Forest)

Esta tabla corresponde al núcleo repetido en Notebook 05, con selección por validación interna y sin el Random Forest agregado de los artefactos de Lucas. La sección “Integración EP3” superior contiene la comparación completa. El árbol es una configuración distinta del árbol registrado por Lucas en 04a; véase la explicación de configuraciones antes de la tabla integrada.

El notebook 05 vuelve a preparar la fuente y ejecuta las comparaciones; las cifras siguientes se expresan en puntos de popularidad y corresponden a sus particiones reservadas.

### Prueba aleatoria por canción

| Variante | Modelo | MAE | RMSE | R² | Mejora de MAE vs. Dummy |
|---|---|---:|---:|---:|---:|
| Referencia | Dummy mediana | 17,250 | 20,612 | 0,000 | — |
| Completa | Ridge, α = 0,1 | 11,915 | 16,643 | 0,348 | 30,9 % |
| Completa | Árbol por defecto, profundidad sin límite, hoja mínima 1 | 12,012 | 19,572 | 0,098 | 30,4 % |
| Sin géneros | Ridge, α = 0,1 | 16,671 | 20,223 | 0,037 | 3,4 % |
| Sin géneros | Árbol, profundidad 15, hoja mínima 20 | 15,693 | 19,834 | 0,074 | 9,0 % |

Entre las variantes Ridge/árbol de esta tabla, Ridge con géneros presenta el menor MAE. En la comparación completa EP3, Random Forest obtiene menor MAE en la misma prueba. El resultado señala asociación predictiva dentro de la muestra; no implica que los géneros causen popularidad ni que el modelo anticipe éxito futuro. La popularidad sigue siendo histórica y el muestreo está balanceado artificialmente por género.

En el KPI retrospectivo del 10 % superior de la misma prueba, se seleccionan 1.795 de 17.948 canciones. Ridge recuperó 159 de 653 positivos (precisión 8,86 %, recall 24,35 %, lift 2,435); RF recuperó 237 (13,20 %, 36,29 %, 3,629). Es una medición sobre una variable objetivo ya observada, no evidencia de rentabilidad o utilidad comercial.

### Prueba agrupada por artista principal

| Variante | Modelo | MAE | RMSE | R² | Mejora de MAE vs. Dummy |
|---|---|---:|---:|---:|---:|
| Referencia | Dummy mediana | 16,707 | 20,075 | -0,003 | — |
| Completa | Ridge, α = 0,1 | 12,102 | 16,740 | 0,302 | 27,6 % |
| Completa | Árbol, profundidad 15, hoja mínima 100 | 14,455 | 18,247 | 0,171 | 13,5 % |

La partición reserva 3.528 artistas principales y no comparte artistas principales con entrenamiento. Aun así, 2.633 canciones de prueba tienen colaboradores secundarios que aparecen en entrenamiento. Por eso describe transferencia a principales no vistos con colaboración parcialmente compartida.

### Segmentos y agrupamiento

El Ridge completo tuvo MAE 8,040 para popularidad (0,35), 10,546 para [35,70), 24,448 para canciones con popularidad 0 y 36,759 para [70,100]. Por condición explícita, el soporte fue 16.431 canciones no explícitas (MAE 11,704) y 1.517 explícitas (MAE 14,198). Los errores dependen del grupo y deben leerse junto a sus tamaños.

K-Means eligió K=2 entre soluciones con al menos 1 % del entrenamiento en cada grupo: silueta 0,245; un perfil más energético y sonoro (54.011 canciones) y otro más acústico y tranquilo (17.781). PCA proyecta estos clústeres en dos dimensiones; conserva 44,1 % de la varianza y descarta el resto. K-Means se ajusta en las diez variables escaladas, no en esa proyección. La sensibilidad fue alta ante `log1p(duration_ms)` (ARI 0,968) y menor al retirar `loudness` (ARI 0,807). El notebook guarda la tabla integrada en [`05_model_comparison_results.csv`](reports/figures/ea2/05_model_comparison_results.csv) y la proyección en `reports/figures/ea2/05_clusters_pca.png`.

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

### Comparación antes y después de la preparación

| Dataset | Filas | Canciones únicas | Media | Mediana | Popularidad = 0 | Popularidad ≥ 70 |
|---|---:|---:|---:|---:|---:|---:|
| Original | 114.000 | 89.741 | 33,239 | 35 | 14,053% | 4,800% |
| Procesado | 89.740 | 89.740 | 33,198 | 33 | 10,468% | 3,480% |

La reducción de filas no equivale a perder 24.260 canciones: se consolidan apariciones del mismo
`track_id` asociadas a diferentes géneros y se retira una fila inválida. La media cambia poco,
pero la mediana y las proporciones extremas sí cambian. Esto demuestra que la repetición por género
alteraba la ponderación de la distribución original.

![Distribución de popularidad procesada](reports/figures/05_processed_popularity_distribution.png)

*Figura 5. Distribución de `popularity` sobre 89.740 canciones únicas. La concentración en valores
bajos y medios debe considerarse al definir líneas base y evaluar errores por segmentos.*

La popularidad procesada tiene media 33,20, mediana 33 y desviación estándar 20,58. Los percentiles
25, 75 y 95 son 19, 49 y 67. Los valores 0 y 100 pertenecen al rango documentado, por lo que no se
consideran errores únicamente por estar en los extremos.

### Relaciones numéricas con `popularity`

Pearson resume asociación lineal, mientras Spearman resume asociación monotónica a partir de
rangos. Ambas medidas describen asociación y no causalidad.

| Variable | Pearson | Spearman |
|---|---:|---:|
| `instrumentalness` | -0,127 | -0,124 |
| `loudness` | 0,072 | 0,067 |
| `speechiness` | -0,047 | -0,067 |
| `danceability` | 0,064 | 0,055 |
| `energy` | 0,014 | -0,016 |
| `duration_ms` | -0,023 | 0,013 |
| `liveness` | -0,014 | -0,012 |
| `valence` | -0,012 | -0,011 |
| `acousticness` | -0,039 | 0,010 |
| `tempo` | 0,007 | 0,008 |

Ninguna característica acústica individual presenta una asociación fuerte. `instrumentalness`
muestra la señal negativa de mayor magnitud; `loudness` y `danceability` tienen asociaciones
positivas pequeñas. Una correlación cercana a cero tampoco descarta relaciones no lineales,
interacciones o diferencias entre géneros.

![Matriz de correlación](reports/figures/06_numeric_correlation_heatmap.png)

*Figura 6. Matriz de Pearson. Las relaciones más intensas aparecen entre predictores de audio, no
entre un predictor individual y la variable objetivo.*

Las principales redundancias son `energy`–`loudness` (0,759), `energy`–`acousticness` (-0,733) y
`loudness`–`acousticness` (-0,583). En modelos lineales esto puede volver inestables los coeficientes;
se recomienda evaluar escalamiento, regularización y, si el objetivo es explicativo, diagnósticos
como VIF sobre la matriz de diseño definitiva.

### Relaciones bivariadas

Un scatterplot con casi 90 mil puntos produciría sobreposición. Por ello se dividieron variables
seleccionadas en cuantiles y se representó la mediana de popularidad por intervalo.

![Popularidad por cuantiles](reports/figures/07_binned_feature_popularity.png)

*Figura 7. Tendencias por cuantiles de cinco atributos. Permiten observar curvaturas que una
correlación global no representa.*

La caída asociada con `instrumentalness` es la tendencia más consistente. `loudness` y
`danceability` crecen en parte de su rango, mientras `energy` y `acousticness` presentan formas
curvas. Estos patrones justifican evaluar relaciones no lineales, pero no constituyen reglas para
modificar canciones ni demuestran efectos causales.

### Contenido explícito y relevancia práctica

| Grupo | Canciones | Media | Mediana | Desviación estándar |
|---|---:|---:|---:|---:|
| No explícita | 82.036 | 32,852 | 33 | 20,369 |
| Explícita | 7.704 | 36,884 | 37 | 22,352 |

La diferencia es 4,032 puntos en media y 4 puntos en mediana. Sin embargo, el tamaño de efecto
estandarizado es pequeño (`d` de Cohen = 0,196). Con una muestra grande una diferencia puede ser
estadísticamente detectable sin ser grande en términos prácticos.

![Popularidad según contenido explícito](reports/figures/08_explicit_popularity_boxplot.png)

*Figura 8. Los grupos presentan centros diferentes, pero también un solapamiento amplio. No se
puede concluir que el contenido explícito produzca mayor popularidad.*

### Géneros como variable multietiqueta

`track_genres` puede contener varias etiquetas separadas por `|`. Para resumir popularidad se
expande una canción por cada etiqueta, pero esas filas expandidas no representan canciones nuevas.
Los conteos se realizan sobre `track_id` únicos dentro de cada género.

![Popularidad por género](reports/figures/09_genre_popularity_summary.png)

*Figura 9. Géneros con mayor mediana entre aquellos con soporte suficiente. Los resultados describen
la muestra y no la prevalencia real del catálogo de Spotify.*

| Soporte mínimo | Géneros incluidos | Género con mayor mediana | Mediana |
|---:|---:|---|---:|
| 100 | 114 | `pop` | 66 |
| 200 | 114 | `pop` | 66 |
| 500 | 114 | `pop` | 66 |

La conclusión principal es estable ante esos tres umbrales porque todos los géneros poseen soporte
cercano a mil canciones. Esta estabilidad no elimina el sesgo de muestreo artificialmente
balanceado ni permite afirmar que un género cause popularidad.

### Valores extremos y anomalías

El criterio IQR se utiliza como señal de revisión, no como regla automática de eliminación.

| Variable | Mínimo | P1 | P99 | Máximo | Casos fuera de IQR |
|---|---:|---:|---:|---:|---:|
| `duration_ms` | 8.586 | 61.872 | 546.011 | 5.237.295 | 4.225 |
| `tempo` | 0 | 65,165 | 193,652 | 243,372 | 514 |
| `loudness` | -49,531 | -28,542 | -1,628 | 4,532 | 5.026 |
| `speechiness` | 0 | 0,025 | 0,619 | 0,965 | 10.644 |
| `instrumentalness` | 0 | 0 | 0,958 | 1 | 19.613 |
| `liveness` | 0 | 0,041 | 0,950 | 1 | 6.981 |

![Revisión de valores extremos](reports/figures/10_outlier_review.png)

*Figura 10. Las colas y concentraciones dependen de la naturaleza de cada atributo. Estar fuera del
IQR no demuestra un error de datos.*

La duración máxima equivale aproximadamente a 87,29 minutos y puede representar contenido largo
válido. `tempo=0` merece validación puntual, pero no se elimina sin evidencia adicional. Las
acumulaciones extremas en `speechiness`, `instrumentalness` y `liveness` son compatibles con
variables acotadas y asimétricas. Para modelamiento se sugiere comparar escalamiento robusto y una
transformación `log1p` de duración.

## Variables recomendadas para modelamiento

| Variable o grupo | Clasificación | Evidencia o riesgo | Recomendación |
|---|---|---|---|
| `popularity` | Target | Histórica, dinámica y con masa en cero | Regresión; evaluar errores en distintos rangos |
| Atributos acústicos | Candidatas | Señales individuales débiles y posibles interacciones | Evaluar conjuntamente y escalar según el modelo |
| `duration_ms`, `tempo`, `loudness` | Requieren tratamiento | Colas y extremos | Comparar transformación y escala robusta |
| `explicit` | Candidata binaria | Efecto descriptivo pequeño y posible confusión | Incluir con auditoría por grupos |
| `track_genres` | Requiere encoding | Multietiqueta y muestra balanceada | Aplicar multi-hot encoding |
| `key`, `mode`, `time_signature` | Requieren encoding | Categorías representadas numéricamente | No tratarlas automáticamente como distancias continuas |
| `artists` | Alta cardinalidad | 31.437 valores; riesgo de memorizar reputación | Excluir de línea base o validar por artista |
| `album_name` | Alta cardinalidad | 46.589 valores; riesgo de memorización | Excluir de línea base |
| `track_name` | Alta cardinalidad | 73.608 valores y texto libre | Excluir de línea base |
| `track_id` | Excluir | Identificador único y riesgo directo de leakage | Mantener solo para trazabilidad |

Las asociaciones individuales débiles no significan que un modelo multivariable sea necesariamente
inútil: una combinación de variables, interacciones o curvaturas podría aportar señal. Esa utilidad
debe demostrarse fuera de muestra frente a una línea base.

## Sesgos identificados

### Sesgo de muestreo

El dataset original contiene exactamente 1.000 filas por género. Esto no representa la frecuencia
natural de canciones ni de reproducciones en Spotify. Además, antes de consolidar, las canciones
con varias etiquetas tenían mayor peso en los agregados.

### Sesgo temporal

`popularity` depende de reproducciones y recencia, pero no existe fecha de extracción ni fecha de
lanzamiento. El dataset es una fotografía histórica y puede sufrir *concept drift*: las relaciones
aprendidas podrían cambiar con tendencias, audiencias o reglas de la plataforma.

### Variables omitidas

No se observan inversión de marketing, exposición en playlists, viralidad, popularidad previa del
artista, colaboraciones, región, fecha de lanzamiento, estacionalidad ni exposición externa. Estas
ausencias limitan tanto la predicción como cualquier interpretación causal.

### Sesgo por artista y género

Una partición aleatoria puede dejar canciones del mismo artista en entrenamiento y prueba, haciendo
que el modelo memorice reputación en vez de generalizar a artistas nuevos. Los géneros tampoco son
grupos excluyentes: una canción puede pertenecer a varias etiquetas y debe evaluarse como tal.

## Ética y uso responsable

Una predicción de popularidad podría reforzar artistas que ya reciben exposición, favorecer estilos
dominantes, reducir oportunidades para artistas emergentes o convertir correlaciones históricas en
reglas creativas. Tampoco debe confundirse popularidad estimada con mérito o calidad artística.

El uso responsable requiere:

- Tratar el modelo como apoyo a la decisión humana, no como criterio único.
- Informar incertidumbre, procedencia y límites de generalización.
- Revisar errores por género, contenido explícito y artistas vistos o no vistos.
- Monitorear cambios temporales y degradación del desempeño.
- Evitar asignaciones automáticas de presupuesto o promoción de alto impacto.
- Preservar diversidad y permitir revisión de las decisiones.

## Privacidad

El dataset contiene metadatos de canciones, nombres públicos de artistas y atributos musicales. No
incluye directamente identidad, ubicación, perfiles ni historial de escucha de oyentes, por lo que
el riesgo de privacidad individual es relativamente bajo frente a datasets de comportamiento.

Esto no elimina la obligación de conservar trazabilidad, respetar condiciones de uso y aplicar
minimización. Si en el futuro se integran playlists personales, ubicaciones o eventos de escucha,
serán necesarios controles de acceso, retención limitada, evaluación de reidentificación y una base
legal claramente definida.

## Matriz de riesgos técnicos

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| Leakage mediante `track_id` | Alto | Alta si se incluye | Excluir del conjunto predictor |
| Memorización por artista | Alto | Alta | Validación agrupada y control de encoding |
| Drift temporal | Alto | Alta | Obtener fechas y validar hacia adelante |
| Muestra no representativa | Alto | Alta | Limitar generalización y documentar cobertura |
| Variables contextuales omitidas | Alto | Alta | Incorporar contexto trazable sin afirmar causalidad |
| Multicolinealidad acústica | Medio | Alta | Escalamiento, regularización y diagnóstico |
| Géneros multietiqueta | Medio | Alta | Multi-hot encoding y métricas no excluyentes |
| Extremos válidos tratados como errores | Medio | Media | Validación puntual y análisis de sensibilidad |
| Desempeño desigual por segmentos | Alto | Media | Reportar métricas globales y por grupos |
| Sobreconfianza de negocio | Alto | Media | Supervisión humana y límites de uso |

Estas probabilidades e impactos son categorías cualitativas para priorizar controles, no frecuencias
estadísticas estimadas.

## Interpretación y uso recomendado

Ridge con géneros es el candidato con menor MAE en la prueba aleatoria y mejora la referencia mediana también cuando se reservan artistas principales completos. Puede servir como evidencia exploratoria para ordenar una revisión humana dentro de una muestra comparable. El árbol ofrece una alternativa no lineal más simple de comunicar por reglas, aunque sus errores son mayores aquí.

La señal de géneros es fuerte en esta muestra, pero su balance artificial impide extrapolar las diferencias a todo Spotify. El modelo subestima canciones de alta popularidad y su KPI retrospectivo no demuestra éxito futuro. Antes de un uso operativo harían falta datos temporales, contexto de exposición y una validación prospectiva; estas fuentes no están disponibles en el dataset actual.

La popularidad no es una medida de calidad artística. Una eventual herramienta debe servir para auditar y priorizar preguntas, con revisión humana y análisis de cobertura por género y por artistas nuevos.

## Conclusiones operativas

La comparación integrada identifica Ridge con géneros como el candidato de menor MAE en la prueba aleatoria compartida. La evaluación agrupada conserva una ventaja frente a Dummy al reservar artistas principales, con solapamiento parcial de colaboradores secundarios. Estos resultados respaldan un uso exploratorio para ordenar una revisión humana dentro de datos comparables.

La popularidad observada no se explica mediante una regla acústica simple. Géneros aportan señal predictiva en esta muestra, mientras que la transformación de duración y el escalado robusto apenas cambian los resultados. K-Means produce dos perfiles acústicos exploratorios; al retirar `loudness`, su asignación pierde estabilidad.

El muestreo artificialmente balanceado por género y la popularidad histórica limitan la generalización. La fuente no contiene fechas, exposición promocional, playlists, región ni reputación previa. Por tanto, el análisis no demuestra causalidad, éxito futuro ni utilidad comercial. La popularidad tampoco es una medida de calidad artística.

## Documentación técnica complementaria

El [informe LaTeX extendido](docs/latex/README.md) consolida el desarrollo, las decisiones,
la robustez estadística, los riesgos y una guía de defensa. Complementa este README y los
notebooks, que siguen siendo las fuentes oficiales de resumen y evidencia ejecutable. Su versión
compilada está disponible en [`output/pdf/main.pdf`](output/pdf/main.pdf).

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

La reproducción integrada de EP3 se realiza desde un kernel limpio y ejecutando todas las celdas, sin permitir errores:

```powershell
uv sync --all-groups
uv run python -m ipykernel install --user --name python3 --display-name "Python 3.12 (spotify-popularity-analysis)"
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/06_ep3_final.ipynb --ExecutePreprocessor.timeout=-1
```

La búsqueda de Random Forest y GroupKFold puede demorar considerablemente. La corrida registra versiones, SHA-256 de la fuente y de la partición de prueba, parámetros y tiempos en `reports/figures/ea3/06_ep3_manifest.json`; las tablas y figuras de esa carpeta se vuelven a generar al ejecutar el notebook.

```powershell
# Abrir los notebooks
uv run jupyter lab

# Generar la base intermedia sin modificar el archivo original
uv run python scripts/build_base_dataset.py

# Generar el dataset limpio de una canción por track_id
uv run python scripts/build_processed_dataset.py

# Regenerar las tablas estadísticas del informe extendido
uv run python scripts/build_latex_tables.py

# Verificar estilo y pruebas automatizadas
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Los notebooks se ejecutan en orden numérico. Notebook 05 reconstruye los análisis EA2 y consume los CSV EP3 versionados. Para regenerar también la evidencia EP3 desde el entrenamiento, ejecute primero `04a_modeling_lucas.ipynb` y `04b_modeling_ignacio.ipynb`, y luego `05_model_comparison.ipynb`; 04a y 04b pueden tardar bastante por la búsqueda y los folds de Random Forest. Para volver a ejecutar solo el consolidado con las tablas actuales:

```powershell
uv run python -m nbconvert --to notebook --execute notebooks/05_model_comparison.ipynb --inplace --ExecutePreprocessor.timeout=1800
```

El notebook registra los tamaños de las particiones, las huellas de los IDs de prueba, métricas y figuras. Requiere varios minutos de cómputo; mantiene las figuras EA2 en `reports/figures/ea2/` y escribe la comparación IE12 en `reports/figures/ea3/05_cesar_model_comparison.csv`.

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
│   ├── latex/                  # Informe técnico extendido y tablas reproducibles
│   └── data_dictionary.md      # Diccionario del dataset
├── models/                     # Modelos serializados generados
├── notebooks/                  # Análisis numerados en orden de ejecución
├── reports/figures/            # Figuras para informe y presentación
├── output/presentations/       # Presentación EA2
├── output/pdf/                 # Informe técnico compilado
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

Para la Evaluación Parcial 2, el [plan de trabajo de Lucas, Ignacio y César](docs/ea2/plan_trabajo.md)
define un núcleo técnico que los tres desarrollarán, sus comprobaciones individuales y la
integración de modelos supervisados, clustering y defensa cruzada.

## Evaluación Parcial 3

La evidencia final de modelamiento, selección por escenario, trazabilidad con la pauta y
limitaciones está en [auditoría EP3](docs/ep3/auditoria_final.md), [decisión de modelos](docs/ep3/decision_cesar.md)
y [guion de defensa](docs/ep3/guion_defensa.md). La presentación final tiene 12 láminas en
`output/presentations/spotify_popularity_ep3_final.pptx`. El informe técnico LaTeX se mantiene en
`docs/latex/` y su PDF compilado en `output/pdf/main.pdf`.

La validación agrupada tiene dos protocolos distintos: GroupKFold de tres folds por artista
principal en Notebook 04b y un holdout agrupado independiente con validación interna agrupada en
Notebook 04c. El holdout 04c evalúa Ridge y árbol, no Random Forest; sus resultados no deben
mezclarse con GroupKFold ni con la prueba aleatoria por canción.

## Limitaciones actuales

- El dataset es estático y no representa el estado actual de Spotify.
- `popularity` depende de factores temporales y comerciales que no están completamente
  representados en las variables disponibles.
- La fuente original repetía `track_id`; el dataset procesado ya representa una canción por fila,
  pero conserva la pertenencia multietiqueta en `track_genres`.
- La cobertura original perfectamente balanceada por género no representa la composición natural
  del catálogo ni la distribución de reproducciones.
- No existen fechas, regiones, exposición en playlists, inversión promocional ni comportamiento de
  oyentes para controlar esos factores.
- Los resultados descriptivos no permiten afirmar causalidad.
- No hay fecha de lanzamiento ni contexto de exposición para validar predicción temporal o utilidad
  comercial. La presentación requiere defensa oral individual y revisión final del equipo.
