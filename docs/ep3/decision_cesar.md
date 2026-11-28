# Selección de solución EP3 — IE12

## Decisión

La elección depende del escenario. Para canciones retenidas al azar, Random Forest ofrece el menor MAE observado. Para el escenario de artistas principales no vistos, Ridge queda como referencia prudente por su menor RMSE, mayor R², menor brecha y costo; sin embargo, el holdout agrupado independiente 04c no incluye Random Forest, por lo que no demuestra que Ridge sea superior a RF en ese test externo.

## Resultados por protocolo

| Protocolo | Modelo | MAE | RMSE | R² | Lectura |
|---|---|---:|---:|---:|---|
| Prueba aleatoria por canción | Ridge | 11,915 | 16,643 | 0,348 | Referencia lineal. |
| Prueba aleatoria por canción | Random Forest | 9,648 | 14,536 | 0,502 | Mejor MAE; mismos casos que Ridge. |
| Prueba aleatoria por canción | Árbol default Notebook 05 | 12,012 | 19,572 | 0,098 | Árbol de referencia principal. |
| GroupKFold por artista principal, media ± DE (3 folds) | Ridge | 12,061 ± 0,408 | 16,858 ± 0,650 | 0,328 ± 0,045 | Ajuste medio 0,370 s/fold; gap MAE 0,324. |
| GroupKFold por artista principal, media ± DE (3 folds) | Random Forest | 11,752 ± 0,458 | 16,969 ± 0,770 | 0,319 ± 0,055 | MAE 0,309 menor; ajuste 1.086,074 s/fold; gap 8,060. |
| Holdout agrupado independiente 04c | Ridge | 12,102 | 16,740 | 0,302 | Seleccionado en validación agrupada; 18.193 canciones de test. |
| Holdout agrupado independiente 04c | Árbol depth=15/leaf=100 | 14,455 | 18,247 | 0,171 | Seleccionado en validación agrupada. No se evaluó RF en este holdout. |

En GroupKFold, Ridge tiene menor RMSE y mayor R²; las desviaciones estándar de tres folds no son pruebas de significancia. La prueba agrupada 04c es diferente: retiene artistas principales completos, selecciona internamente con grupos y evalúa una sola vez el grupo externo. No se deben presentar ambas como el mismo resultado.

## Límites de selección

- RF se eligió con CV aleatoria dentro del conjunto de entrenamiento; el GroupKFold de Ignacio evalúa candidatos ya fijados, no es búsqueda anidada.
- El holdout independiente de 04c compara Ridge y árbol, no RF. Por tanto, la decisión agrupada es una referencia operativa razonada, no una comparación externa completa.
- No hay solapamiento de artistas principales en las particiones agrupadas, pero 2.633 canciones del holdout 04c comparten colaboradores secundarios con entrenamiento.
- No hay evaluación temporal ni datos de exposición. Popularidad es histórica y la muestra está balanceada artificialmente por género.

## KPI y significado de negocio

Sobre las mismas 17.948 canciones de prueba se selecciona el 10 % superior por puntuación (1.795 casos), con popularidad observada ≥70 como positivo. Ridge recupera 159/653 positivos (precisión 8,86 %, recall 24,35 %, lift 2,435); RF recupera 237/653 (13,20 %, 36,29 %, lift 3,629). Es una medición retrospectiva de ranking, no ROI ni evidencia de aumento de ingresos o popularidad futura. Su uso hipotético es priorizar revisión humana.

La regresión no tiene accuracy. La frase oral “accuracy mínimo 80 %” necesita precisar tarea, umbral, clase y partición. Con prevalencia de positivos 3,64 %, el clasificador mayoritario tiene 96,36 % accuracy y recall cero, lo que ilustra por qué accuracy aislada sería engañosa.

## Reproducción

Evidencia en `notebooks/04a_modeling_lucas.ipynb`, `notebooks/04b_modeling_ignacio.ipynb`, `notebooks/04c_modeling_cesar.ipynb` y `notebooks/05_model_comparison.ipynb`; comparación aleatoria consolidada en `reports/figures/ea3/05_cesar_model_comparison.csv`.
