# Auditoría final de presentación EP3

## Dictamen

Se contrastó la presentación y las evidencias locales con la pauta oficial EP3. La evaluación es orientativa: IE9 queda parcialmente demostrado porque las búsquedas se ejecutaron, pero no produjeron una mejora relevante frente a los valores predeterminados; IE10–IE12 tienen evidencia coherente con sus criterios, con límites explícitos. No se asigna un 100 % artificial ni se repitió el entrenamiento de Random Forest, cuyo costo registrado fue alto.

## Matriz de rúbrica

| Indicador | Peso | Nivel demostrado estimado | Evidencia y límite |
|---|---:|---:|---|
| IE9 · Optimización de hiperparámetros | 20 % | 80 % | RandomizedSearchCV documenta 12/144 configuraciones y MAE, pero el ganador coincide con defaults; Ridge mejora 0,023 % y el árbol 0 %. La rúbrica pide optimizar para mejorar el rendimiento, por lo que este indicador no se declara completo. |
| IE10 · Técnicas de ensamble | 30 % | 100 % | RF se compara en la misma prueba aleatoria: mejora MAE 19,03 % frente a Ridge y 19,68 % frente al árbol principal; se informan agregación, bootstrap, brecha de ajuste y costo. |
| IE11 · Generalización | 20 % | 100 % | 04b aporta GroupKFold de 3 folds por artista; 04c aporta holdout independiente por artista principal con selección interna agrupada. No hay artistas principales compartidos; secundarios pueden solaparse. El holdout 04c no evalúa RF. No es validación temporal ni nested CV. |
| IE12 · Selección de solución | 30 % | 100 % | Decisión condicional al escenario, con MAE/RMSE/R², costo y generalización. Ridge se recomienda como referencia para principales no vistos; RF para menor MAE en canciones retenidas al azar. |
| **Total ponderado estimado** | **100 %** | **96 %** | Cálculo orientativo: 0,2×80 + 0,3×100 + 0,2×100 + 0,3×100. La evaluación docente puede diferir. |

Los porcentajes son una estimación interpretativa de niveles de desempeño de la pauta, no una nota garantizada. La mención oral de “accuracy 80 %” no se resuelve con la pauta escrita ni con las métricas de regresión actuales; requiere que se defina tarea, clase, umbral y protocolo.

## Trazabilidad de evidencia

| Afirmación | Evidencia primaria |
|---|---|
| 89.740 filas únicas; media 33,20; mediana 33; 10,47 % en cero; 3,48 % ≥70 | `notebooks/03_exploratory_analysis.ipynb`; `reports/figures/05_processed_popularity_distribution.png`; `reports/figures/06_numeric_correlation_heatmap.png` |
| Prueba aleatoria 71.792/17.948, semilla 42; Dummy/Ridge/árbol/RF | `notebooks/04a_modeling_lucas.ipynb`; `notebooks/05_model_comparison.ipynb`; `reports/figures/ea3/05_cesar_model_comparison.csv`; resultados RF en `reports/figures/ea3/04a_lucas_test_comparison.csv` |
| RF: 12/144, KFold(3), MAE; 100 árboles, depth=None, leaf=1, max_features=1,0 | `notebooks/04a_modeling_lucas.ipynb`, búsqueda y CSV `reports/figures/ea3/04a_lucas_search.csv` |
| Ridge/árbol: validación interna y parámetros seleccionados | Notebook 05, celdas de validación; `reports/figures/ea3/05_cesar_hyperparameter_validation.csv` |
| GroupKFold 3 folds, medias, desviaciones y ajuste | `notebooks/04b_modeling_ignacio.ipynb`; `reports/figures/ea3/04b_ignacio_cv_summary.csv` y manifiesto/folds asociados |
| Holdout agrupado independiente: split y evaluación Ridge/árbol | `notebooks/04c_modeling_cesar.ipynb`, celdas 18–19 y salidas ejecutadas. 71.547 train/18.193 test; validación interna agrupada 57.176/14.371; cero principales compartidos; 2.633 canciones de prueba comparten secundarios. No incluye RF. |
| KPI top 10 % y MAE por popularidad | `reports/figures/ea3/04a_lucas_top_decile_kpi.csv`; `notebooks/05_model_comparison.ipynb`; se comparan 1.795 seleccionadas de 17.948 y positivos observados ≥70. |
| K-Means/PCA y sensibilidad | `notebooks/05_model_comparison.ipynb`; `reports/figures/ea2/05_clusters_pca.png`; métricas/tabla de sensibilidad incorporadas en notebook. |

## Correcciones aplicadas a la presentación

| Lámina | Corrección |
|---:|---|
| 1 | Identificación como Evaluación Parcial 3. |
| 2 | Necesidad, usuario, objetivo general, decisión de apoyo y frontera entre estimación histórica y futuro. |
| 3 | EDA y cifras verificadas; conecta cola ≥70 con análisis por segmentos y correlación débil con exploración no lineal. |
| 4 | Separa holdout aleatorio, validación interna, GroupKFold y holdout agrupado independiente 04c; explica solapamiento secundario y pipeline. |
| 5 | Nombra hiperparámetros y espacios reales, método de búsqueda, presupuesto, valores ganadores y mejoras pequeñas o nulas. |
| 6 | Comparación homogénea Dummy/Ridge/árbol principal/RF; árbol principal es Notebook 05 default, y no el árbol alternativo de Lucas. |
| 7 | Corrige reducciones MAE a 19,03 % vs Ridge y 19,68 % vs árbol principal; explica bootstrap, `max_features=1.0`, brecha exacta y costo. |
| 8 | Corrige “menor RMSE, mayor R²”; distingue GroupKFold de 04b y holdout 04c; informa costo, brecha y límites. |
| 9 | Compara KPI Ridge/RF con el mismo test y selección top 10 %; conserva MAE por segmentos y carácter retrospectivo. |
| 10 | Aclara que K-Means usa 71.792 canciones de entrenamiento y diez variables escaladas; PCA solo visualiza y conserva 44,1 %. |
| 11 | Selección condicionada por escenario y costo. |
| 12 | Limitaciones de muestra, temporalidad y uso responsable; propone evaluación prospectiva como paso futuro. |

## Decisión técnica

En la prueba aleatoria común RF obtiene MAE 9,648, RMSE 14,536 y R² 0,502; Ridge obtiene 11,915, 16,643 y 0,348. RF reduce MAE 19,03 % frente a Ridge. En GroupKFold de 04b RF baja MAE medio 0,309, mientras Ridge tiene RMSE menor, R² mayor, brecha menor y ajuste medio mucho más rápido. En el holdout independiente 04c, con selección interna agrupada, Ridge logra MAE/RMSE/R² 12,102/16,740/0,302 y el árbol 14,455/18,247/0,171. Como ese holdout no mide RF, la recomendación para artistas nuevos se presenta como referencia prudente, no como comparación completa de todos los modelos en prueba externa.

La brecha RF aleatoria se calcula con cifras no redondeadas: 9,900504163 − 3,767441017 = 6,133063146. La reducción vs árbol principal es (12,011595105 − 9,647897824) / 12,011595105 = 19,678 %; vs Ridge es 19,028 %.

## Experimentos y limitaciones

No se añadieron experimentos. El repositorio ya contiene selección interna, GroupKFold y un holdout independiente agrupado; repetir la búsqueda RF sería costoso (aprox. 61 minutos reportados para las 12 configuraciones) y no hay evidencia previa de que un nuevo presupuesto razonable vaya a mejorar el criterio. Esta decisión conserva intactos los tests y evita prometer una mejora. IE9 queda como limitación real. El holdout agrupado 04c no incluye RF; el GroupKFold sí compara un candidato RF previamente seleccionado por CV aleatoria, por lo que no sustituye una búsqueda anidada. Tampoco hay validación temporal.

La presentación tiene 12 láminas, notas de expositor y duración objetivo de 9:35. Se inspeccionaron visualmente las 12 imágenes exportadas, se verificaron 12 diapositivas y 2 gráficos nativos y pasaron los chequeos estructurales y geométricos. La apertura en PowerPoint nativo no pudo verificarse automáticamente.
