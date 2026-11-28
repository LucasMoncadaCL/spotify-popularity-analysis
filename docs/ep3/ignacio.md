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

## Implementación IE11

**Estado técnico:** completado, revisado por el equipo e integrado en `dev` mediante el
merge PR #25. La rama de integración de César incorpora estas tablas en IE12.

La sección 9 del notebook conserva las 25 celdas históricas de EA2 y añade la comparación
de Dummy mediana, Ridge, árbol y el Random Forest fijado por Lucas. Usa tres folds aleatorios
con semilla 42 y tres folds deterministas de `GroupKFold`, exclusivamente sobre las 71.792
canciones del entrenamiento compartido. La escala y codificación se ajustan dentro de cada
fold. Se registran métricas de entrenamiento/validación, media/DE, costo, tamaños,
asignaciones por canción y solapamiento de artistas secundarios.

La evaluación de prueba de Lucas se reutiliza de su CSV publicado, con huellas registradas;
no se crea otra prueba ni se reevalúa el bosque sobre ella. El candidato ya había sido
seleccionado en este entrenamiento: el análisis es diagnóstico de candidatos congelados,
no validación anidada independiente de la selección anterior.

Las cifras, reproducción, límites y defensa están en el
[informe técnico de Ignacio](informe_ignacio.md). El
[mensaje para César](mensaje_cesar.md) entrega los pasos de revisión, merge e integración
IE12. Las salidas regenerables tienen prefijo `04b_ignacio_` en `reports/figures/ea3/`.
