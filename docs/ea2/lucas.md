# Lucas Moncada: trabajo de EA2 en Spotify

**Objetivo personal:** completar y explicar el ciclo técnico de modelamiento supervisado, no supervisado y evaluación sobre Spotify, usando el mismo protocolo que Ignacio y César. Mi comprobación adicional medirá el aporte de `track_genres` a la estimación de popularidad.

## Informe individual para revisión cruzada

El [informe de Lucas en PDF](informe_lucas/informe_lucas.pdf) consolida datos, método,
resultados, figuras, límites y conclusiones del notebook 04a. Incluye un apartado de traspaso
para que Ignacio y César puedan comprobar las cifras y llevarlas al notebook integrador. La
[fuente LaTeX](informe_lucas/main.tex) y las [instrucciones de compilación](informe_lucas/README.md)
quedan junto al PDF. El notebook ejecutado sigue siendo la evidencia de cálculo.

## Reproducción del notebook 04a

Desde la raíz del repositorio, con Python y dependencias gestionados por `uv`:

```powershell
uv sync --locked
uv run python scripts/build_base_dataset.py
uv run python scripts/build_processed_dataset.py
uv run jupyter nbconvert --to notebook --execute notebooks/04a_modeling_lucas.ipynb --output 04a_modeling_lucas_reproduced.ipynb --output-dir notebooks --ExecutePreprocessor.timeout=1800
```

El último comando guarda una copia ejecutada en `notebooks/` y genera las figuras de EA2 en
`reports/figures/ea2/`. También se puede abrir el notebook con `uv run jupyter lab` y ejecutar
todas sus celdas en orden. La fuente debe tener SHA-256
`b202fa49909b2d5cef71a04b1d21243cfeb36414535f2ca9272aa646721177bd` y el procesado
89.740 canciones únicas; el notebook muestra la huella de la fuente, comprueba los controles del
procesado y registra las huellas de las particiones.

**Comprobación local del 24-10-2026:** en una copia aislada sin `.venv`, dataset procesado ni
figuras previas, `uv 0.11.8` instaló el entorno desde `uv.lock` con Python 3.12.13. Se ejecutaron
las 13 celdas de código sin errores; sus salidas textuales y los hashes SHA-256 de las tres
figuras guardadas coincidieron con la ejecución original. `ruff check .` y
`ruff format --check .` pasaron, y `pytest` terminó con 18 pruebas aprobadas. Esta comprobación
incluyó los archivos de esta rama. Una clonación podrá repetirla tras publicar la rama en el remoto.

## 1. Protocolo común antes de modelar

Lucas prepara la propuesta inicial de protocolo y la somete a revisión de Ignacio y César. El acuerdo debe fijar dataset, unidad de análisis, columnas, partición por `track_id`, semilla, métricas y formato de resultados. Los tres verifican la preparación y pueden reproducir la misma partición. Este trabajo de coordinación no reemplaza el notebook técnico personal de Lucas.

**Entrega:** un PR acotado desde `feature/ea2-shared-protocol` hacia `dev`, con el acuerdo documentado y solo el código reutilizable que haga falta. Se integra antes de los tres notebooks 04.

## 2. Notebook técnico propio

**Archivo:** `notebooks/04a_modeling_lucas.ipynb`, en `feature/ea2-modeling-lucas` creada desde `dev` actualizado.

El notebook debe ejecutarse en orden desde el inicio y cubrir:

1. **Contexto y datos:** pregunta de negocio, objetivo `popularity`, fuente, KPIs y relación con CRISP-DM. Regenerar o cargar el dataset procesado y comprobar canción única por `track_id`, faltantes, rangos y variables pertinentes. Resumir los hallazgos de EDA de EP1 que explican las decisiones de modelamiento.
2. **Partición y preparación:** usar el conjunto de prueba común (20%, semilla 42). Mantener `track_id` para control, fuera de los predictores. Ajustar escala, codificación de `key`, `mode`, `time_signature` y géneros multietiqueta solo con entrenamiento dentro del flujo de modelamiento. Excluir nombres de pista, álbum y artista de la matriz principal.
3. **Aprendizaje supervisado:** entrenar `DummyRegressor(strategy="median")`, `Ridge` y `DecisionTreeRegressor`. Explicar por qué regresión corresponde a un objetivo continuo, qué supuestos/ventajas ofrece cada algoritmo y cómo se eligen sus parámetros sin consultar la prueba.
4. **Evaluación:** informar MAE, RMSE y R² de los tres modelos en la misma prueba; interpretar MAE/RMSE en puntos de popularidad, R² frente a la referencia y errores por rangos o segmentos. Calcular el KPI de priorización acordado: proporción con `popularity >= 70` entre el 10% mejor puntuado, frente a la prevalencia de la prueba. Concluir cuándo el resultado serviría como apoyo a una revisión humana del catálogo.
5. **Aprendizaje no supervisado:** escalar los atributos musicales numéricos del entrenamiento, aplicar K-Means sin `popularity`, justificar K con inercia/codo y silueta, visualizar con PCA e informar varianza explicada. Describir tamaños, perfiles originales y popularidad posterior de los clústeres; proponer una lectura útil para el catálogo sin atribuir causalidad.
6. **Límites y ética:** discutir muestreo balanceado por género, falta de fechas y exposición promocional, posibles diferencias de error entre segmentos y riesgo de favorecer estilos ya populares.

## 3. Comprobación propia: aporte de los géneros

Comparar dos versiones de la misma regresión usando idénticas canciones y protocolo: atributos musicales y estructura **sin** `track_genres`, y los mismos predictores **con** `track_genres` codificado como multietiqueta. Realizar la comparación para Ridge y árbol. Seleccionar configuraciones con entrenamiento/validación y reservar la prueba para la evaluación final; informar tamaño del cambio en MAE, RMSE, R² y KPI operativo. Si la ganancia es pequeña o inestable, decirlo explícitamente. Explicar que el muestreo de la fuente impide generalizar una mejora por género a todo Spotify.

## 4. Integración y defensa

- Abrir el PR del notebook hacia `dev` con una tabla de resultados, parámetros, decisiones, verificaciones y limitaciones. Ignacio y César revisan el resultado; Lucas revisa el notebook de Ignacio según la rotación acordada.
- Entregar las cifras y conclusiones reproducibles para `notebooks/05_model_comparison.ipynb` y el `README.md` oficial. Evitar editar esos archivos compartidos a la vez que otra persona.
- Practicar una explicación breve de cada indicador IE5–IE8 y responder preguntas cruzadas sobre los modelos, K-Means, métricas, datos y ética, además del experimento de géneros.

## Cierre verificable

- [ ] Ignacio y César revisaron el protocolo común; los tres obtienen la misma partición.
- [ ] El notebook de Lucas se ejecuta completo desde una instalación nueva, sin rutas personales ni celdas con errores.
- [ ] Hay referencia, dos regresores, métricas comparables, KPI, K-Means, PCA y perfiles interpretados con cifras reales.
- [ ] La comparación con y sin géneros usa la misma prueba y explica tanto la magnitud de la diferencia como sus límites.
- [ ] Lucas puede explicar todas las etapas de la evaluación, no solo la sección que redactó.
