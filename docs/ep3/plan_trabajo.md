# EP3 Spotify: plan de trabajo de Lucas, Ignacio y César

## Objetivo

Adaptar el proyecto Spotify Tracks de la EP2 a la pauta de la EP3 sin borrar ni reescribir la evidencia histórica de la EP2. La entrega debe mostrar optimización de hiperparámetros, al menos un método de ensamble, validación de generalización y una selección final justificada; además, cada integrante debe poder defender el trabajo completo.

La pauta asigna IE9 (optimización) 20%, IE10 (ensamble) 30%, IE11 (generalización) 20% e IE12 (selección de solución) 30%. Los insumos formales son un informe Markdown, notebooks ejecutables, datos/archivos complementarios reproducibles y una presentación de hasta 10 minutos con defensa individual.

## Punto pendiente: significado de “accuracy 80%”

El docente mencionó “accuracy mínimo 80%”, sin precisar objetivo ni métrica. El objetivo actual `popularity` es continuo y se evalúa como regresión con MAE, RMSE y R²; accuracy no es una métrica directa de regresión. La pauta no fija un umbral de accuracy del modelo: sus niveles 100/80/60/30/0% califican el logro de cada indicador.

Si se convierte el objetivo a “popular” (`popularity >= 70`), solo 653 de 17.948 canciones de la prueba son positivas (3,64%). Predecir siempre “no popular” daría 96,36% de accuracy, por lo que superar 80% no demostraría que el modelo identifique canciones populares. El KPI actual de precisión en el 10% superior tampoco es accuracy.

**Decisión de trabajo:** mientras no se aclare el requisito, se mantiene la regresión Spotify como análisis principal y se completa IE9–IE12 con métricas apropiadas. No se declarará cumplido el objetivo de 80% por el baseline trivial ni se llamará accuracy a una métrica distinta. Si el docente confirma que requiere clasificación, el equipo acordará antes de modelar la definición de clases y evaluará accuracy junto con balanced accuracy, matriz de confusión, precisión, recall, macro-F1 y PR-AUC.

## Protocolo compartido

- Fuente, preparación, unidad `track_id`, predictores y semillas se mantienen coherentes con la EP2.
- Todo ajuste de transformación, hiperparámetros o umbral se realiza solo con datos de entrenamiento mediante validación cruzada. La prueba final permanece intacta hasta seleccionar candidatos.
- Comparar cada modelo contra Dummy, Ridge y árbol ya existentes; informar MAE, RMSE y R² (regresión), además de métricas por segmento y KPI pertinente.
- Para generalización agrupada, separar artistas principales completos. Declarar solapamiento de artistas secundarios y mantenerlo fuera de cualquier afirmación de artistas totalmente desconocidos.
- Si se confirma clasificación, fijar clases y umbral antes de consultar la prueba; comparar contra un clasificador ingenuo y explicar desbalance.

## Distribución del trabajo

| Integrante | Indicadores | Responsabilidad | Evidencia prevista |
|---|---|---|---|
| Lucas | IE9, IE10 | Definir una búsqueda acotada de hiperparámetros e implementar modelos de ensamble para popularidad continua. Compararlos con Ridge, árbol y Dummy con el protocolo común. | `notebooks/04a_modeling_lucas.ipynb` actualizado; tabla de búsqueda y métricas; figuras/salidas reproducibles. |
| Ignacio | IE11 | Medir generalización con validación cruzada dentro del entrenamiento y una partición agrupada por artista principal. Aplicar el mismo protocolo a los candidatos acordados, incluido el ensamble. | `notebooks/04b_modeling_ignacio.ipynb` actualizado; resultados media/desviación por fold y resultados agrupados. |
| César | IE12 e integración | Comparar resultados y seleccionar la solución con criterios técnicos, estabilidad, complejidad e interpretación de negocio. Actualizar el notebook oficial, informe y presentación. Resolver con el equipo la interpretación del 80%. | `notebooks/05_model_comparison.ipynb`, `README.md`, presentación EP3 y resumen de decisión. |

## Entregables por integrante

### Lucas: ensambles y optimización

- Añadir al notebook propio al menos un regresor de ensamble (por ejemplo, Random Forest o Extra Trees); probar un segundo solo si el costo de cómputo permite una comparación informativa.
- Definir y justificar el espacio de búsqueda (por ejemplo, cantidad de árboles, profundidad, mínimo de observaciones por hoja y variables consideradas por división).
- Seleccionar hiperparámetros con entrenamiento/validación cruzada; registrar configuración, semilla, métrica de selección y costo de ejecución.
- Comparar contra Dummy, Ridge y árbol, mostrando si el ensamble aporta una mejora suficiente para justificar su complejidad.
- No modificar el test ni seleccionar parámetros a partir de sus resultados.

### Ignacio: generalización y validación

- Establecer una validación cruzada aleatoria reproducible dentro del conjunto de entrenamiento y reportar promedio y dispersión de las métricas.
- Evaluar transferencia a artistas principales no vistos mediante particiones agrupadas (p. ej., GroupKFold), manteniendo artistas principales fuera de los folds de validación.
- Reutilizar los mismos predictores y candidatos de Lucas, y comparar con Ridge/árbol. No duplicar ni alterar el conjunto de prueba final.
- Explicar que la agrupación por artista principal no evita por completo el solapamiento de artistas secundarios.
- Si el docente confirma clasificación, añadir la validación estratificada o agrupada adecuada y métricas por clase; no usar accuracy sola.

### César: decisión e integración

- Esperar los resultados revisados de Lucas e Ignacio antes de consolidar cambios al notebook 05, README o presentación.
- Aplicar criterios acordados antes de revisar la prueba: métrica principal, métricas de apoyo, estabilidad entre folds, complejidad, errores por grupo y utilidad de negocio.
- Documentar cuándo el ensamble justifica su costo o cuándo Ridge/árbol sigue siendo preferible.
- Mantener las limitaciones del dataset histórico, el muestreo artificialmente balanceado por género, la ausencia de fechas/exposición y el carácter retrospectivo del KPI.
- Si se confirma el requisito de accuracy, precisar la definición con el equipo y reportar su baseline para evitar una conclusión inflada por desbalance.
- Actualizar presentación a EP3 y reservar tiempo dentro de 10 minutos para objetivos, método, comparación, límites y preguntas.

## Flujo de ramas y revisión

Crear cada rama desde `dev` actualizado y enviar PR a `dev`:

- `feature/ep3-lucas-ensemble`
- `feature/ep3-ignacio-validation`
- `feature/ep3-cesar-integration`

Lucas e Ignacio pueden avanzar en notebooks distintos. César integra cuando los dos PR técnicos estén revisados; evitar ediciones simultáneas de `notebooks/05_model_comparison.ipynb`, `README.md` y la presentación. Mantener la rotación de revisión: Lucas revisa a Ignacio, Ignacio a César y César a Lucas.

## Criterios para cerrar la preparación EP3

- Los hiperparámetros se eligen sin mirar el test y se justifica la estrategia de búsqueda.
- El aporte de al menos un ensamble se compara contra baseline y modelos actuales con métricas apropiadas.
- La generalización se reporta mediante validación cruzada y prueba independiente; los folds agrupados respetan la separación acordada.
- La solución final se selecciona con criterios explícitos y cifras idénticas en notebook, README e informe/presentación.
- La fuente puede regenerar las salidas; notebooks y comandos corren desde el entorno definido por `uv.lock` sin rutas personales.
- El equipo completa revisión cruzada, ensayo cronometrado y preguntas individuales sobre todo el flujo.
- El requisito verbal de accuracy queda confirmado y definido antes de presentarlo como criterio logrado.
