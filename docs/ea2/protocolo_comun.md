# Propuesta de protocolo común: EA2 Spotify

**Estado:** propuesta de Lucas para revisión de Ignacio y César. Tras el acuerdo, este documento será la referencia de los notebooks 04a–04c y del notebook final 05. Toda excepción debe quedar escrita junto con su motivo; los resultados principales usarán exactamente el mismo protocolo.

## 1. Pregunta, unidad de análisis y fuente

- **Tarea supervisada:** estimar el valor histórico de `popularity` (0–100) de una canción; es regresión porque el objetivo es numérico. No se interpretará como pronóstico de éxito de un lanzamiento futuro.
- **Tarea no supervisada:** descubrir perfiles de canciones según sus atributos musicales, sin incluir `popularity` en la formación de grupos.
- **Alcance de negocio:** comprobar retrospectivamente si audio y géneros contienen señal para estimar popularidad y describir segmentos musicales. El valor real de `popularity` ya existe en esta fuente: la lista de revisión definida más abajo es una simulación de evaluación, no una herramienta lista para decidir promociones.
- **Fuente única:** `data/raw/Spotify_Tracks_Dataset.csv`, conservado intacto. Regenerar `data/processed/spotify_tracks_clean.csv` con `uv run python scripts/build_processed_dataset.py` antes de trabajar.
- **Unidad:** una canción por `track_id` en el procesado. Con la fuente actual se esperan 89.740 filas, 20 columnas, cero nulos, `track_id` único, duración positiva y `popularity` dentro de 0–100. Si algún control falla, detener el experimento e investigar; no cambiar el filtro de datos por cuenta propia.
- **Géneros:** `track_genres` contiene etiquetas múltiples separadas por `|`. Una canción conserva una fila durante la partición y evaluación, aunque pertenezca a varios géneros.

El [informe de EP1](../../README.md) y su [EDA](../../notebooks/03_exploratory_analysis.ipynb) encontraron una mediana de popularidad de 33, un 10,47% de canciones con popularidad cero y solo un 3,48% con 70 o más en el procesado. Ningún atributo acústico aislado mostró una asociación fuerte con la popularidad. Esos hallazgos justifican la referencia, el análisis de errores por rangos y la comparación de modelos lineales y no lineales; **no anticipan que alguno vaya a superar la referencia**. El origen aportó exactamente 1.000 filas por género; durante la preparación se consolidaron con la mediana las discrepancias de `popularity` de algunos IDs repetidos. La prevalencia y el objetivo describen esta muestra histórica, no el catálogo actual de Spotify.

## 2. Partición idéntica y uso de los datos

1. Ordenar los `track_id` únicos como texto. Aplicar `train_test_split` de scikit-learn con `test_size=0.20`, `shuffle=True` y `random_state=42` sobre esa lista ordenada. Usar los IDs resultantes para seleccionar las filas; nunca partir el CSV bruto con pistas repetidas. Con 89.740 canciones se esperan 71.792 de entrenamiento y 17.948 de prueba.
2. Dentro de los IDs de entrenamiento, crear una validación de 20% usando el mismo procedimiento y semilla 42. La selección de transformaciones, géneros e hiperparámetros se hace con entrenamiento/validación; después se reajusta el modelo elegido con las 71.792 canciones de entrenamiento.
3. Usar la prueba una vez para informar el resultado final de los modelos y las variantes declaradas de antemano. No elegir un modelo, umbral, conjunto de variables o parámetro mirando sus métricas de prueba. Guardar en los resultados la semilla, tamaños y una huella de los IDs de prueba para comprobar que los tres usaron la misma partición.
4. Mantener `track_id` solo para verificar la partición y unir resultados. `artists` queda fuera de los predictores principales y se usa obligatoriamente para el diagnóstico de generalización del punto siguiente.
5. **Diagnóstico obligatorio por artista principal:** definir el grupo como el primer nombre de `artists` antes de `;`, sin espacios laterales y con comparación insensible a mayúsculas. Aplicar `GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)` sobre el procesado; su 20% se refiere a grupos y no garantiza un 20% exacto de canciones. Registrar tamaños y comprobar que ningún artista principal esté en ambos conjuntos. Dentro del entrenamiento agrupado, generar otra validación agrupada con la misma regla; elegir entre los parámetros candidatos ya declarados usando solo ese entrenamiento y validación, reajustar el pipeline desde cero con todo el entrenamiento agrupado y evaluar una vez en su prueba. La validación de la partición aleatoria no sirve para elegir parámetros aquí porque puede contener canciones de la prueba agrupada. Informar MAE, RMSE, R² y diferencia respecto de la referencia agrupada para contrastar con la partición principal. Este análisis mide transferencia a artistas **principales** no vistos; las colaboraciones pueden compartir artistas secundarios y esa superposición debe contarse y declararse. César coordina su implementación y el notebook 05 lo reproduce para que los tres puedan explicarlo.

## 3. Predictores y preparación supervisada

| Grupo | Columnas | Tratamiento común |
|---|---|---|
| Numéricas | `duration_ms`, `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo` | Escala estándar ajustada solo con entrenamiento. Conservar valores extremos válidos; cualquier transformación adicional es un experimento separado. |
| Categóricas | `key`, `mode`, `time_signature`, `explicit` | Codificación one-hot ajustada solo con entrenamiento y tolerante a categorías nuevas. No interpretar los códigos de tonalidad o compás como distancias. |
| Multietiqueta | `track_genres` | Separar por `|` y producir indicadores 0/1 para las etiquetas aprendidas solo en entrenamiento. Una canción puede activar varias columnas. |
| Excluidas | `popularity`, `track_id`, `artists`, `album_name`, `track_name` | `popularity` es el objetivo; los otros campos no entran al modelo principal por identidad, cardinalidad o riesgo de memorización. |

Las transformaciones se ajustan dentro de un pipeline con los datos de entrenamiento. Los tres usan la misma versión completa de predictores para la comparación principal; la variante de Lucas elimina únicamente `track_genres`. Los experimentos adicionales de Ignacio y César indican con precisión qué decisión cambian.

## 4. Modelos, selección y métricas

- **Referencia:** `DummyRegressor(strategy="median")`, ajustado con entrenamiento.
- **Modelo lineal:** `Ridge`, con candidatos de `alpha` 0,1; 1; 10; 100.
- **Modelo no lineal:** `DecisionTreeRegressor`, con `max_depth` 5, 10 o 15 y `min_samples_leaf` 20 o 100. Fijar `random_state=42`.
- **Selección:** elegir parámetros por menor MAE de validación; usar RMSE y complejidad para desempatar. Reajustar cada configuración seleccionada con todo el entrenamiento y comparar referencia, Ridge y árbol en la misma prueba. Explicar por qué los algoritmos son adecuados y qué limitaciones tienen.
- **Métricas de prueba:** MAE y RMSE en puntos de popularidad, R² respecto de la referencia constante igual a la media de la prueba, más cantidad de filas evaluadas. Mostrar la mejora absoluta y relativa de MAE frente al `DummyRegressor` de mediana sin afirmar causalidad. Si no mejora la referencia, concluir que esa configuración no aporta evidencia predictiva suficiente.
- **Diagnóstico de errores:** informar MAE y número de canciones para `popularity = 0`, `(0,35)`, `[35,70)` y `[70,100]`, además de al menos un desglose por `explicit` o género con soporte visible. Los segmentos se construyen con valores reales solo después de predecir, nunca para entrenar.
- **KPI retrospectivo de priorización:** ordenar la prueba por popularidad predicha descendente, con `track_id` ascendente para desempatar. El umbral `popularity >= 70` y la capacidad de revisar el 10% se fijan antes del modelamiento; el 70 proviene del segmento descriptivo de EP1, no de optimizar la prueba. Para ese 10% (cantidad redondeada hacia arriba), informar cuántas canciones cumplen el umbral, precisión, exhaustividad (*recall*) y *lift* = precisión / prevalencia de `popularity >= 70` en toda la prueba. La prevalencia se calcula por canción única y es el rendimiento esperado de una selección aleatoria de igual tamaño en **esta muestra**; no estima la prevalencia del catálogo real. Si el *lift* no supera 1, no afirmar que el ranking mejore la selección aleatoria. Incluso si lo supera, el resultado no demuestra utilidad comercial ni predice lanzamientos futuros, porque la fuente ya contiene la popularidad histórica y carece de fechas y contexto de exposición.

Lucas informará, como análisis adicional previamente definido, el desempeño de Ridge y árbol con y sin géneros en la misma partición. La elección del modelo recomendado se justifica por validación, no por la comparación posterior en prueba.

## 5. Clustering y evaluación no supervisada

- Usar solo las diez columnas numéricas de la tabla anterior, tomadas del entrenamiento. Ajustar `StandardScaler` en entrenamiento; no incluir `popularity`, nombres, IDs ni géneros en la distancia de K-Means.
- Ejecutar K-Means para K entre 2 y 8, con `random_state=42` y `n_init=10`. Mostrar inercia/codo. Calcular silueta sobre una muestra reproducible de hasta 2.000 canciones para controlar el costo. Elegir K considerando ambas señales, tamaño de grupos e interpretabilidad; registrar la decisión aunque no haya un codo claro.
- Ajustar el K elegido en el entrenamiento escalado. Mostrar tamaños y perfiles con medianas de atributos originales. Solo después de asignar grupos, resumir `popularity` por clúster para explorar su relación con el objetivo; no usar ese resumen para cambiar retrospectivamente K.
- **Sensibilidad motivada por EP1:** `duration_ms` tiene una cola larga y `energy`–`loudness` están correlacionadas (r ≈ 0,759). Sin volver a elegir K, repetir por separado el K elegido (a) con `log1p(duration_ms)` antes de escalar y (b) sin `loudness`; ajustar cada transformación solo con entrenamiento. Comparar tamaños, perfiles y concordancia de asignaciones mediante ARI, reconociendo que los números de clúster son arbitrarios. Si los perfiles cambian sustancialmente, describir los segmentos como dependientes de las variables y la escala, sin convertirlos en categorías estables del catálogo.
- Ajustar PCA de dos componentes sobre el entrenamiento escalado, informar varianza explicada y usarlo para visualizar una muestra reproducible de los grupos. PCA es una proyección visual; los clústeres se calculan en el espacio de atributos definido arriba.
- Traducir perfiles en una hipótesis concreta de análisis de catálogo y señalar límites del muestreo por género, falta de fechas y posible refuerzo de exposición de artistas ya conocidos.

## 6. Formato común de evidencia y revisión

Cada notebook registra: versión/datos usados, tamaños y huella de partición, columnas, transformaciones, semilla, parámetros candidatos y elegidos, métricas de validación y prueba, tabla de errores/KPI, justificación de K, perfiles de clústeres y conclusiones. El notebook 05 añade obligatoriamente la prueba por artista principal y la sensibilidad de K-Means. Las cifras finales del `README.md` y de la presentación deben provenir del notebook final reproducible, no de copiar manualmente una salida de un notebook personal.

Antes de comenzar a entrenar, Ignacio y César revisan especialmente: (1) si la partición por IDs y la prueba por artista principal son inequívocas; (2) si columnas y transformaciones son comunes; (3) si el KPI se entiende como simulación retrospectiva y su prevalencia pertenece solo a la muestra; y (4) si el clustering y su sensibilidad usan atributos y criterios adecuados. Tras resolver sus comentarios, los tres toman la misma versión aprobada de `dev`.

## Condiciones para aceptar el protocolo

- [ ] Ignacio y César revisaron el documento y quedaron registradas las decisiones corregidas.
- [ ] Los tres pueden producir los mismos IDs y tamaños de entrenamiento, validación y prueba desde el CSV original.
- [ ] La evaluación complementaria separa artistas principales, informa sus tamaños reales y la superposición de colaboradores secundarios, y puede reproducirse en el notebook 05.
- [ ] El objetivo y `track_id` no entran a ningún predictor; escala y codificación se ajustan sin ver la prueba.
- [ ] Los dos regresores, la referencia, las métricas y K-Means tienen configuraciones comparables y criterios de interpretación definidos antes de conocer resultados; el KPI y la sensibilidad de clústeres distinguen evidencia de esta muestra y utilidad comercial real.
- [ ] El protocolo está integrado en `dev` antes de abrir los PR de notebooks 04.
