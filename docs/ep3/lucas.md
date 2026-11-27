# Handoff EP3: Lucas Moncada

- **Indicadores principales:** IE9, optimización de hiperparámetros; IE10, técnicas de ensamble.
- **Rama propuesta:** `feature/ep3-lucas-ensemble`
- **Notebook de trabajo:** `notebooks/04a_modeling_lucas.ipynb`
- **PR destino:** `dev`

## Objetivo

Extender el modelo de regresión de popularidad de la EP2 con uno o más modelos de ensamble, ajustados de forma reproducible y comparados con Dummy, Ridge y árbol. La meta es demostrar si el ensamble mejora el desempeño y si esa mejora compensa su complejidad.

## Trabajo

- Mantener la misma fuente, canción única por `track_id`, predictores, semilla y protocolo común del equipo.
- Añadir al menos un regresor de ensamble, por ejemplo `RandomForestRegressor` o `ExtraTreesRegressor`.
- Definir una búsqueda acotada y razonada de hiperparámetros; registrar las combinaciones probadas y por qué son pertinentes.
- Seleccionar parámetros solo con el entrenamiento y la validación cruzada acordada con Ignacio. No ajustar mirando el test.
- Comparar contra Dummy mediana, Ridge y árbol mediante MAE, RMSE y R²; incluir promedio/dispersión de validación cruzada y una evaluación final reservada.
- Describir costo/tiempo si es relevante para la decisión y comunicar limitaciones sin prometer el umbral verbal de 80% antes de aclarar qué significa.

## Criterios de revisión

El notebook debe correr de inicio a fin, informar semilla, folds, parámetros, métricas y baseline, evitar fuga de datos y explicar si el ensamble aporta una mejora consistente. Ignacio revisa el notebook antes del PR de integración.

## Accuracy pendiente de definición

`popularity` es continuo; la métrica principal de este notebook sigue siendo de regresión. Si el docente confirma que requiere accuracy, coordinar antes de crear una variante de clasificación: clase objetivo, umbral, baseline y métricas complementarias. No usar como evidencia suficiente el accuracy de predecir siempre la clase mayoritaria.
