# Lucas Moncada: trabajo de EA2 en Spotify

**Objetivo personal:** completar y explicar el ciclo técnico de modelamiento supervisado, no supervisado y evaluación sobre Spotify, usando el mismo protocolo que Ignacio y César. Mi comprobación adicional medirá el aporte de `track_genres` a la estimación de popularidad.

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
