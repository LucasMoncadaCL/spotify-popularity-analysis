# Handoff EP3: Ignacio Silva

- **Indicador principal:** IE11, evaluación de la capacidad de generalización.
- **Rama propuesta:** `feature/ep3-ignacio-validation`
- **Notebook de trabajo:** `notebooks/04b_modeling_ignacio.ipynb`
- **PR destino:** `dev`

## Objetivo

Evaluar cuánto varía el desempeño de los modelos entre particiones y cómo se comportan ante artistas principales no vistos, sin usar el conjunto de prueba para elegir parámetros.

## Trabajo

- Mantener la preparación y predictores comunes, y dejar el test final intacto.
- Implementar validación cruzada reproducible en el conjunto de entrenamiento para regresión; reportar promedio y desviación de MAE, RMSE y R² por fold.
- Evaluar folds agrupados por artista principal con separación estricta por grupo. Comparar Ridge, árbol y el/los ensambles acordados con Lucas.
- Registrar cantidad de folds, tamaños por fold, semillas cuando correspondan y diferencias entre validación cruzada y prueba reservada.
- Declarar que los artistas secundarios aún pueden aparecer en ambos lados si la agrupación solo usa artista principal.
- No afirmar generalización temporal: la fuente no contiene fechas.

## Criterios de revisión

La validación se ejecuta solo en entrenamiento; los pipelines ajustan codificación y escala dentro de cada fold; los modelos se comparan con iguales datos y métricas. Lucas revisa el notebook antes del PR de integración.

## Accuracy pendiente de definición

La validación y métricas primarias actuales son de regresión. Si el docente confirma clasificación, acordar clase/umbrales antes de entrenar y usar accuracy junto con balanced accuracy, matriz de confusión, precisión, recall, macro-F1 y PR-AUC. Para una clase `popularity >= 70`, el clasificador mayoritario ya supera 80% de accuracy, por lo que ese porcentaje solo no demuestra capacidad de detectar canciones populares.
