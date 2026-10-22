# Propuesta de protocolo común: EA2 Spotify

**Estado:** propuesta de Lucas para revisión de Ignacio y César. Tras el acuerdo, este documento será la referencia de los notebooks 04a–04c y del notebook final 05. Toda excepción debe quedar escrita junto con su motivo; los resultados principales usarán exactamente el mismo protocolo.

## 1. Pregunta, unidad de análisis y fuente

- **Tarea supervisada:** estimar el valor histórico de `popularity` (0–100) de una canción; es regresión porque el objetivo es numérico. No se interpretará como pronóstico de éxito de un lanzamiento futuro.
- **Tarea no supervisada:** descubrir perfiles de canciones según sus atributos musicales, sin incluir `popularity` en la formación de grupos.
- **Fuente única:** `data/raw/Spotify_Tracks_Dataset.csv`, conservado intacto. Regenerar `data/processed/spotify_tracks_clean.csv` con `uv run python scripts/build_processed_dataset.py` antes de trabajar.
- **Unidad:** una canción por `track_id` en el procesado. Con la fuente actual se esperan 89.740 filas, 20 columnas, cero nulos, `track_id` único, duración positiva y `popularity` dentro de 0–100. Si algún control falla, detener el experimento e investigar; no cambiar el filtro de datos por cuenta propia.
- **Géneros:** `track_genres` contiene etiquetas múltiples separadas por `|`. Una canción conserva una fila durante la partición y evaluación, aunque pertenezca a varios géneros.

## 2. Partición idéntica y uso de los datos

1. Ordenar los `track_id` únicos como texto. Aplicar `train_test_split` de scikit-learn con `test_size=0.20`, `shuffle=True` y `random_state=42` sobre esa lista ordenada. Usar los IDs resultantes para seleccionar las filas; nunca partir el CSV bruto con pistas repetidas. Con 89.740 canciones se esperan 71.792 de entrenamiento y 17.948 de prueba.
2. Dentro de los IDs de entrenamiento, crear una validación de 20% usando el mismo procedimiento y semilla 42. La selección de transformaciones, géneros e hiperparámetros se hace con entrenamiento/validación; después se reajusta el modelo elegido con las 71.792 canciones de entrenamiento.
3. Usar la prueba una vez para informar el resultado final de los modelos y las variantes declaradas de antemano. No elegir un modelo, umbral, conjunto de variables o parámetro mirando sus métricas de prueba. Guardar en los resultados la semilla, tamaños y una huella de los IDs de prueba para comprobar que los tres usaron la misma partición.
4. Mantener `track_id` solo para verificar la partición y unir resultados. `artists` puede usarse en un análisis adicional de generalización por artista, pero queda fuera de los predictores principales.

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
- **Métricas de prueba:** MAE y RMSE en puntos de popularidad, R² respecto de una predicción constante, más cantidad de filas evaluadas. Mostrar la diferencia de MAE frente a la referencia sin afirmar causalidad.
- **Diagnóstico de errores:** informar MAE y número de canciones para `popularity = 0`, `(0,35)`, `[35,70)` y `[70,100]`, además de al menos un desglose por `explicit` o género con soporte visible. Los segmentos se construyen con valores reales solo después de predecir, nunca para entrenar.
- **KPI operativo:** ordenar la prueba por popularidad predicha descendente, con `track_id` ascendente para desempatar. Medir la proporción con `popularity >= 70` en el 10% superior (redondeando la cantidad hacia arriba), comparada con la prevalencia de ese grupo en toda la prueba. Es una medida de priorización de revisión del catálogo, no de ventas ni de desempeño futuro.

Lucas informará, como análisis adicional previamente definido, el desempeño de Ridge y árbol con y sin géneros en la misma partición. La elección del modelo recomendado se justifica por validación, no por la comparación posterior en prueba.

## 5. Clustering y evaluación no supervisada

- Usar solo las diez columnas numéricas de la tabla anterior, tomadas del entrenamiento. Ajustar `StandardScaler` en entrenamiento; no incluir `popularity`, nombres, IDs ni géneros en la distancia de K-Means.
- Ejecutar K-Means para K entre 2 y 8, con `random_state=42` y `n_init=10`. Mostrar inercia/codo. Calcular silueta sobre una muestra reproducible de hasta 2.000 canciones para controlar el costo. Elegir K considerando ambas señales, tamaño de grupos e interpretabilidad; registrar la decisión aunque no haya un codo claro.
- Ajustar el K elegido en el entrenamiento escalado. Mostrar tamaños y perfiles con medianas de atributos originales. Solo después de asignar grupos, resumir `popularity` por clúster para explorar su relación con el objetivo; no usar ese resumen para cambiar retrospectivamente K.
- Ajustar PCA de dos componentes sobre el entrenamiento escalado, informar varianza explicada y usarlo para visualizar una muestra reproducible de los grupos. PCA es una proyección visual; los clústeres se calculan en el espacio de atributos definido arriba.
- Traducir perfiles en una hipótesis concreta de análisis de catálogo y señalar límites del muestreo por género, falta de fechas y posible refuerzo de exposición de artistas ya conocidos.

## 6. Formato común de evidencia y revisión

Cada notebook registra: versión/datos usados, tamaños y huella de partición, columnas, transformaciones, semilla, parámetros candidatos y elegidos, métricas de validación y prueba, tabla de errores/KPI, justificación de K, perfiles de clústeres y conclusiones. Las cifras finales del `README.md` y de la presentación deben provenir del notebook final reproducible, no de copiar manualmente una salida de un notebook personal.

Antes de comenzar a entrenar, Ignacio y César revisan especialmente: (1) si la partición por IDs y el conjunto de prueba son inequívocos; (2) si columnas y transformaciones son comunes; (3) si el KPI responde a una decisión de negocio defendible; y (4) si el clustering usa atributos y criterios adecuados. Tras resolver sus comentarios, los tres toman la misma versión aprobada de `dev`.

## Condiciones para aceptar el protocolo

- [ ] Ignacio y César revisaron el documento y quedaron registradas las decisiones corregidas.
- [ ] Los tres pueden producir los mismos IDs y tamaños de entrenamiento, validación y prueba desde el CSV original.
- [ ] El objetivo y `track_id` no entran a ningún predictor; escala y codificación se ajustan sin ver la prueba.
- [ ] Los dos regresores, la referencia, las métricas y K-Means tienen configuraciones comparables y criterios de interpretación definidos antes de conocer resultados.
- [ ] El protocolo está integrado en `dev` antes de abrir los PR de notebooks 04.
