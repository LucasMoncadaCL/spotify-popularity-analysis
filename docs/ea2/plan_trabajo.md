# EA2 Spotify: plan de trabajo de Lucas, Ignacio y César

**Objetivo:** completar y defender la Evaluación Parcial 2 con el caso C (Spotify Tracks), haciendo que los tres integrantes practiquen el flujo técnico completo y comprendan todas sus decisiones.

**Por qué se requiere este plan:** tres personas trabajarán en paralelo sobre el mismo proyecto y necesitan resultados comparables, integración sin conflictos y una defensa individual de cualquier parte.

**Criterio de aceptación:** el repositorio contiene dos modelos supervisados de regresión comparados contra una línea base, un análisis no supervisado interpretable, métricas fuera de muestra, conclusiones de negocio, un informe Markdown completo y una entrega reproducible. Lucas, Ignacio y César pueden ejecutar y explicar todas las etapas y responder preguntas cruzadas.

## Matriz de cumplimiento de la rúbrica EA2

La pauta oficial evalúa IE5 (20%), IE6 (30%), IE7 (30%) e IE8 (20%). Las evidencias de EP1 sirven de base, pero deben conectarse explícitamente con los resultados nuevos de EA2. Una casilla se marca solo después de revisar el archivo y su ejecución; este plan no declara resultados aún inexistentes.

| Exigencia | Evidencia prevista | Condición para darla por cumplida |
|---|---|---|
| **IE5, metodología CRISP-DM (20%)** | `README.md`, notebooks 01–05, trazabilidad del dataset y decisiones de modelamiento. | Explicar las seis fases y mostrar la secuencia real: problema y KPI → comprensión/EDA → preparación → modelamiento → evaluación → entrega académica. Registrar iteraciones o cambios motivados por hallazgos. |
| **IE6, supervisado (30%)** | Notebooks 04a–04c y comparación en 05. | Entrenar y comparar al menos Ridge y árbol de regresión adecuados al objetivo continuo, justificar selección y configuración, incluir referencia mediana y documentar partición, pipeline y control de fuga. |
| **IE7, no supervisado (30%)** | Notebooks 04a–04c, perfiles y figuras en 05/`reports/figures/`. | Ajustar K-Means sin el objetivo, justificar K con codo y silueta, describir tamaños y perfiles de clústeres con variables originales y explicar una utilidad concreta para análisis de catálogo o promoción exploratoria. Evitar presentar grupos como categorías objetivas o causas de popularidad. |
| **IE8, desempeño y negocio (20%)** | Tabla de MAE, RMSE, R², análisis por segmentos, KPI operativo y recomendaciones en 05 y `README.md`. | Interpretar las unidades y diferencias frente a la referencia, identificar errores relevantes y traducirlos a una decisión prudente, con condiciones para usar o descartar el modelo. |
| **Contenido obligatorio de la presentación** | Presentación e informe ejecutivo. | Incluir problema, objetivos y KPIs; fuente, EDA, patrones, calidad y variables; preparación; modelos supervisados y no supervisados; métricas, comparación y conclusiones. |
| **Entrega formal** | `README.md` como informe técnico Markdown; notebooks documentados; `data/`, `models/` si hay artefactos, `reports/figures/`, `pyproject.toml` y `uv.lock`. | Otra persona puede obtener el proyecto, regenerar datos, ejecutar todos los notebooks sin modificar rutas ni archivos y relacionar cada cifra del informe con una salida reproducible. |
| **Ética y defensa individual** | Secciones de sesgos, límites y uso responsable; ensayo de preguntas cruzadas. | Mostrar cómo el muestreo por género, la falta de fechas y la desigualdad de exposición limitan el uso. Cada integrante explica cualquiera de los indicadores IE5–IE8 en una presentación de hasta 10 minutos. |

**KPI de negocio para EA2:** evaluar la utilidad de una lista de revisión de catálogo con la proporción de canciones de `popularity >= 70` entre el 10% mejor puntuado por el modelo, comparada con la prevalencia de ese segmento en la prueba. Es una medida de priorización dentro de esta muestra, no una estimación de ingresos ni de éxito de lanzamientos futuros. Conservar además los indicadores descriptivos y de calidad de EP1; MAE, RMSE y R² son métricas técnicas, no KPIs de negocio.

## Organización del mismo repositorio para EA2

Conservar el repositorio `spotify-popularity-analysis`: la rúbrica admite Spotify como caso C y EP1 ya aporta fuente, preparación, EDA y análisis ético. Mantener esos archivos y sus rutas para preservar la ejecución y los enlaces existentes. El commit publicado de EP1 puede recibir una etiqueta de versión sin reescribir su historial.

| Ubicación | Uso en EA2 |
|---|---|
| `README.md` | Informe técnico Markdown oficial y puerta de entrada del proyecto. Ampliar las secciones de EP1 con modelamiento, clustering, resultados, interpretación y reproducción de EA2, indicando qué hallazgos pertenecen a cada evaluación. |
| `notebooks/01_*.ipynb` a `03_*.ipynb` | Evidencia existente de comprensión, preparación y EDA; conservarlos. |
| `notebooks/04a_*`, `04b_*`, `04c_*` | Práctica completa e independiente de Lucas, Ignacio y César con el protocolo común. |
| `notebooks/05_model_comparison.ipynb` | Notebook oficial de EA2: ejecutar desde la fuente o regenerar el procesado, mostrar controles/EDA esenciales, entrenar los dos regresores, aplicar clustering y producir todas las cifras citadas en el README. No depender de salidas guardadas en los notebooks 04. |
| `src/spotify_popularity/modeling/` | Incorporar únicamente las transformaciones y funciones de modelamiento reutilizadas por el notebook oficial; evitar tres implementaciones compartidas incompatibles. |
| `data/raw/`, `data/processed/`, `models/` | Preservar el CSV original; regenerar el procesado y cualquier modelo guardado. El notebook y las instrucciones deben funcionar aunque los artefactos ignorados no estén versionados. |
| `reports/figures/ea2/` | Figuras finales de modelos, errores y clústeres; separar visualmente las de EP1 sin moverlas. |
| `docs/reference/` | La rúbrica EA2 está copiada junto a la pauta EP1 para que los tres trabajen con la misma versión oficial. |
| `docs/latex/`, `output/pdf/` | Mantener el informe PDF de EP1 como complemento histórico; la entrega evaluada en EA2 se centra en Markdown y notebooks. |

### Transición GitFlow entre evaluaciones

1. `origin/dev` fue sincronizada con `origin/main` en el commit `a4fd36a` antes de iniciar EA2. La rama local `feature/ea2-project-structure` parte del mismo commit. Abrir su PR hacia `dev` para integrar el plan y la rúbrica sin modificar la publicación de EP1 en `main`.
2. Tras integrar ese PR, cada integrante actualiza `dev` y crea su rama acotada desde allí: `feature/ea2-modeling-lucas`, `feature/ea2-modeling-ignacio` y `feature/ea2-modeling-cesar`. El protocolo/código compartido y el notebook final se integran en PR separados para poder revisarlos.
3. Cada PR apunta a `dev`, muestra el notebook ejecutado o evidencia equivalente, decisiones, métricas verificadas y limitaciones. La revisión cruzada Lucas → Ignacio → César → Lucas evita que una sola persona sea dueña del conocimiento.
4. Cuando la matriz de cumplimiento y la lista de entrega estén completas, abrir un PR `dev` → `main`. Crear una etiqueta de cierre de EA2 sobre el commit integrado. No mezclar resultados de EA2 en la publicación EP1 ni forzar ramas.

## Decisiones comunes antes de empezar

- **Caso y pregunta:** estimar la `popularity` observada de una canción a partir de atributos disponibles y explorar segmentos musicales. La puntuación histórica no equivale a éxito futuro ni mérito artístico.
- **Base de datos:** reutilizar `data/raw/Spotify_Tracks_Dataset.csv` y la preparación existente. La unidad de análisis es un `track_id` único; `data/processed/spotify_tracks_clean.csv` se regenera, no se edita a mano.
- **Protocolo principal:** fijar una única partición entrenamiento/prueba (80/20, semilla 42) y compartir los mismos identificadores de filas. Mantener la prueba reservada hasta escoger transformaciones e hiperparámetros con entrenamiento. Ningún pipeline usa `track_id`, `popularity`, nombres de pista, álbum o artista como predictores principales.
- **Predictores comunes:** los tres parten de atributos acústicos, duración, `explicit`, estructura musical (`key`, `mode`, `time_signature`) y `track_genres`. Codificar las categorías y los géneros multietiqueta dentro del pipeline; las comprobaciones adicionales cambian una decisión a la vez respecto de esta versión compartida.
- **Modelos comunes:** `DummyRegressor(strategy="median")` como referencia, `Ridge` como regresor lineal regularizado y `DecisionTreeRegressor` con profundidad/tamaño de hoja controlados como alternativa no lineal. Los tres construyen y evalúan los tres; pueden ajustar configuraciones usando solo entrenamiento.
- **Métricas comunes:** MAE, RMSE y R² en la misma prueba, con interpretación en puntos de popularidad y comparación contra la referencia. Incluir errores por rangos de popularidad y al menos un segmento musical, además del KPI de priorización definido arriba. Los resultados se presentan como evidencia de la muestra, sin prometer capacidad causal o temporal.
- **Clustering común:** K-Means sobre el mismo conjunto de atributos musicales numéricos escalados para los tres, sin `popularity` entre las entradas. Comparar varios valores de K con codo/inercia y silueta sobre una muestra reproducible; perfilar los clústeres con las variables originales y `popularity` solo después de asignarlos. Usar PCA para mostrar los grupos en dos dimensiones e informar la varianza explicada.
- **Prevención de fuga:** ajustar imputación, escala, codificación y selección de variables dentro del entrenamiento o de pipelines. Ajustar el clustering con datos de entrenamiento para no incorporar información del conjunto reservado en la evaluación supervisada. Documentar que las canciones están deduplicadas y que una partición aleatoria puede compartir artistas entre ambos conjuntos.

### Resultado 1: protocolo compartido y trabajo independiente

- **Trabajo:** acordar columnas, partición y formato de tabla de resultados antes de entrenar; registrar esa decisión en el notebook integrador o en código reutilizable. Cada persona crea su propio notebook, sin editar simultáneamente el de otra: `notebooks/04a_modeling_lucas.ipynb`, `04b_modeling_ignacio.ipynb` y `04c_modeling_cesar.ipynb`. Los tres siguen la secuencia: carga y control de datos → partición → pipeline → referencia y dos modelos → métricas → K-Means/PCA → interpretación y límites.
- **Verificar:** regenerar los datos con `uv run python scripts/build_processed_dataset.py`; comprobar en cada notebook que las tres evaluaciones usan los mismos `track_id` de prueba y que las celdas se ejecutan en orden.

### Resultado 2: práctica completa de cada integrante

| Integrante | Núcleo obligatorio idéntico para los tres | Comprobación adicional para aportar evidencia distinta |
|---|---|---|
| Lucas | Referencia, Ridge, árbol, K-Means, PCA, métricas e interpretación. | Medir cuánto cambia la predicción al incorporar géneros multietiqueta frente a usar solo atributos musicales. |
| Ignacio | Referencia, Ridge, árbol, K-Means, PCA, métricas e interpretación. | Comparar un tratamiento estándar con una transformación justificada de duración y escalado robusto. |
| César | Referencia, Ridge, árbol, K-Means, PCA, métricas e interpretación. | Auditar errores por género/contenido explícito y contrastar la evaluación aleatoria con una partición agrupada por artista si las etiquetas lo permiten. |

- **Trabajo:** cada notebook explica por qué se eligieron los algoritmos, muestra el tamaño de entrenamiento/prueba, registra parámetros y semilla, interpreta una tabla de métricas y describe los clústeres en términos musicales útiles. Cada integrante deja al menos una limitación y una recomendación de uso responsable. Las comprobaciones adicionales son extensiones: no sustituyen el núcleo común.
- **Verificar:** ejecutar los tres notebooks completos en un entorno limpio después de `uv sync`; revisar que cada uno contiene resultados de los dos regresores, referencia y clustering, y que no usa la prueba durante el ajuste.

### Resultado 3: integración y defensa común

- **Trabajo:** consolidar en `notebooks/05_model_comparison.ipynb` una tabla comparable de los experimentos y escoger la solución final por error, estabilidad, complejidad e interpretación de negocio. Completar `README.md` como informe técnico con problema, objetivos, KPIs, fuentes, EDA, calidad, preparación, seis fases CRISP-DM, modelos, resultados, ética, recomendaciones y pasos de reproducción. Incorporar figuras necesarias y una presentación de hasta 10 minutos. Cada persona explica en el ensayo: CRISP-DM, preparación, ambos modelos, métricas, clustering, ética y limitaciones; las preguntas se rotan para practicar la defensa cruzada.
- **Responsabilidades de coordinación:** Lucas reúne el relato del problema y el protocolo; Ignacio revisa reproducibilidad y consistencia de datos; César revisa interpretación, sesgos y claridad de gráficos. Cada uno revisa el notebook de otra persona (Lucas → Ignacio → César → Lucas). Estas tareas de coordinación no reemplazan el trabajo técnico idéntico de la tabla anterior.
- **Verificar:** seguir desde cero las instrucciones del `README.md`, ejecutar los notebooks en orden y comprobar que todas las cifras del informe y la presentación coinciden con las salidas. Ejecutar `uv run ruff check .` y `uv run pytest` si se modifica código Python reutilizable.

## Control de entrega: no cerrar EA2 con casillas pendientes

- [ ] `README.md` contiene las secciones formales exigidas y vincula cada afirmación de resultados con notebooks o figuras; fuentes y limitaciones quedan identificadas.
- [ ] El CSV original sigue intacto; el procesado se regenera y los archivos necesarios están disponibles en la entrega o tienen instrucciones automáticas suficientes para obtenerlos.
- [ ] Los notebooks 01–05 se ejecutan de inicio a fin desde una instalación nueva, en el orden documentado y sin rutas locales de los autores.
- [ ] Hay al menos dos regresores funcionales comparados en la misma prueba contra la referencia, con algoritmo y parámetros justificados.
- [ ] K-Means produce una selección argumentada de K, perfiles interpretables y una aplicación al problema de negocio; PCA se usa e interpreta correctamente como visualización.
- [ ] MAE, RMSE, R², errores por segmento y KPI operativo tienen cifras reales, interpretación y una recomendación proporcional a la calidad observada.
- [ ] Se documentan sesgos, privacidad, ausencia de temporalidad y límites de generalización; ninguna conclusión afirma causalidad sin evidencia.
- [ ] Informe, figuras, notebooks y presentación usan los mismos números y el equipo puede reproducirlos.
- [ ] Lucas, Ignacio y César completaron su notebook, revisaron el de otra persona y resolvieron preguntas cruzadas sobre IE5, IE6, IE7 e IE8.
- [ ] La presentación cubre todos los apartados obligatorios dentro de 10 minutos y reserva tiempo para la defensa individual.

## Flujo de colaboración y puntos de decisión

1. Integrar el plan EA2 en `dev` como se describe arriba y hacer que los tres partan del mismo commit actualizado.
2. Abrir una rama `feature/*` por notebook o cambio acotado; no compartir un `.ipynb` editable entre personas. La lógica verdaderamente común se integra en `src/spotify_popularity/` tras acordar su interfaz.
3. Integrar primero protocolo y código compartido; luego los tres notebooks; por último comparación, README y presentación. La revisión cruzada ocurre antes de cada integración en `dev`.
4. Si el tiempo de cómputo obliga a reducir alcance, conservar el núcleo obligatorio de cada persona y reducir las comprobaciones adicionales antes de eliminar un modelo o el clustering.

## Lista de dominio individual

Cada integrante debe poder explicar sin leer el notebook: por qué `popularity` es regresión; qué aprende la referencia; diferencias entre Ridge y árbol; qué significan MAE, RMSE y R²; cómo se evitó la fuga; por qué se escala K-Means; cómo se eligió K; qué aporta PCA; qué caracteriza cada clúster; y qué límites impiden extrapolar el resultado a lanzamientos futuros.
