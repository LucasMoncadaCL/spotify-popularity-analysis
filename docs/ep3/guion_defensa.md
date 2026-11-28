# Guion de presentación y defensa EP3

## Distribución para 9 minutos 35 segundos

| Lámina | Tiempo | Idea principal |
|---:|---:|---|
| 1. Portada | 0:15 | Caso Spotify y propósito de la evaluación. |
| 2. Problema y objetivo | 0:40 | Usuario, necesidad, decisión de apoyo y alcance histórico. |
| 3. EDA | 0:40 | Distribución, segmentos raros y límites de correlaciones simples. |
| 4. Preparación y protocolos | 0:45 | Separar holdout aleatorio, validación interna, GroupKFold y holdout independiente 04c. |
| 5. IE9: optimización | 1:15 | Espacios reales, RandomizedSearchCV, presupuesto y mejoras pequeñas o nulas. |
| 6. Comparación supervisada | 0:40 | Cuatro modelos sobre la misma prueba aleatoria. |
| 7. IE10: ensamble | 1:10 | Mejora MAE correcta, mecanismo, brecha y costo RF. |
| 8. IE11: generalización | 1:10 | GroupKFold frente al holdout independiente; límites y solapamientos. |
| 9. Errores y KPI | 0:45 | Error por popularidad y top 10 % retrospectivo. |
| 10. K-Means/PCA | 0:40 | Perfiles exploratorios y PCA como visualización. |
| 11. Decisión IE12 | 1:05 | RF/Ridge según escenario y costo. |
| 12. Cierre | 0:30 | Limitaciones y paso prospectivo. |
| **Total** | **9:35** | Las respuestas extendidas quedan para preguntas. |

## Respuestas para preguntas

1. **¿Qué significa 80 %?** La pauta escrita usa bandas de desempeño; no define un umbral de accuracy. La indicación oral requiere confirmar qué objetivo, clase, umbral y validación quiso decir el docente.
2. **¿El modelo tiene 80 % de accuracy?** No medimos accuracy: la tarea implementada es regresión. Para popularidad ≥70, un clasificador que siempre responde negativo tendría 96,36 % accuracy por la baja prevalencia, pero recall cero.
3. **¿Qué se optimizó?** RF: RandomizedSearchCV, 12 de 144 configuraciones, tres folds y selección por MAE; ganó 100/None/1/1,0, igual a defaults de sklearn 1.7. Ridge mejoró su MAE de validación 0,00276 puntos (0,023 %); el árbol no mejoró frente a default. La búsqueda está documentada, pero su mejora práctica es limitada.
4. **¿Por qué no buscar las 144 configuraciones?** Las 12 configuraciones reportaron unas 4.311 s (~71,8 min) en total. Expandir el presupuesto es costoso y no hay evidencia de que el ganador default vaya a mejorar; no se repitió una búsqueda sin hipótesis clara.
5. **¿Cuál es el mejor modelo?** En test aleatorio, RF logra MAE 9,648 frente a Ridge 11,915. En GroupKFold, RF gana 0,309 MAE, pero Ridge consigue RMSE menor y R² mayor, con menor brecha y costo. No hay ganador universal.
6. **¿Qué diferencia hay entre los protocolos agrupados?** 04b aplica GroupKFold de tres folds en el entrenamiento y promedia resultados; 04c reserva un grupo externo de artistas principales completos, selecciona Ridge/árbol en una validación agrupada interna y evalúa el holdout una vez. El 04c no mide RF.
7. **¿Se comparten artistas en la evaluación agrupada?** No los principales. En el holdout 04c, 2.633 canciones comparten colaboradores secundarios; tampoco hay validación temporal.
8. **¿Por qué decir menor RMSE y mayor R² para Ridge?** En GroupKFold obtiene RMSE 16,858 frente a 16,969 y R² 0,328 frente a 0,319. “Menor R²” sería incorrecto. Las diferencias de tres folds no implican significancia estadística.
9. **¿Qué significa la brecha RF?** En CV aleatoria MAE de entrenamiento 3,767 y validación 9,901; usando cifras completas, la diferencia es 6,133. Indica ajuste bastante mejor al entrenamiento que a folds retenidos.
10. **¿Por qué Random Forest es un ensamble?** Ajusta árboles sobre muestras bootstrap y promedia sus predicciones. La configuración ganadora usa `max_features=1.0`, es decir, todos los predictores disponibles en cada split; no afirmar que el ganador toma subconjuntos aleatorios de variables.
11. **¿El 33,5 % frente al árbol es correcto?** Solo para el árbol alternativo de Lucas con MAE 14,508. El árbol principal de Notebook 05 tiene MAE 12,012; respecto a ese, la mejora RF es 19,68 %. Frente a Ridge es 19,03 %.
12. **¿Qué dice el KPI top 10 %?** Se ordenan las 17.948 canciones del test y se seleccionan 1.795. Con positivo observado ≥70, Ridge recupera 159/653 y RF 237/653. La precisión y lift describen ranking retrospectivo; no ROI ni impacto futuro.
13. **¿Por qué revisar segmentos?** RF tiene MAE 31,432 para canciones con popularidad ≥70 (n=653), mucho más alto que los demás intervalos; se informa soporte porque el grupo es menor.
14. **¿Qué aporta K-Means?** Una segmentación exploratoria de 71.792 canciones de entrenamiento y diez variables escaladas. K=2 obtiene silueta 0,245; dos perfiles son descriptivos, no categorías naturales ni causalidad.
15. **¿Qué conserva PCA?** Las dos componentes visibles contienen 44,1 % de la varianza; el 55,9 % restante no aparece. PCA solo proyecta el gráfico; K-Means se ajusta en las variables escaladas originales.
16. **¿Qué limitaciones impiden una conclusión comercial?** Popularidad histórica, muestra balanceada por género, ausencia de fechas, región, exposición y promoción. No se prueba éxito futuro, causalidad ni calidad artística.

## Recordatorio para el equipo

Al citar métricas, nombre siempre el protocolo. No mezcle el holdout aleatorio con GroupKFold o el holdout independiente 04c. No llame “accuracy” a MAE, R², precisión del top 10 % ni lift. Presente a Ridge como referencia prudente para principales no vistos, señalando que el holdout independiente no incluye RF.
