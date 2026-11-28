# Handoff EP3: César Rojas

- **Indicador principal:** IE12, selección y justificación de la solución analítica óptima.
- **Rama propuesta:** `feature/ep3-cesar-integration`
- **Entregables de integración:** `notebooks/05_model_comparison.ipynb`, `README.md` y presentación EP3.
- **PR destino:** `dev`

## Objetivo

Integrar la evidencia revisada de Lucas e Ignacio, decidir qué solución conviene recomendar para el problema y dejar cifras consistentes entre notebook, informe y presentación.

## Trabajo

- Los PR #24 (Lucas) y #25 (Ignacio) ya están integrados en `dev`; la sección IE12 consume sus resultados versionados.
- Comparar Dummy, Ridge, árbol y ensambles con criterios acordados previamente: métrica de selección, rendimiento en test, estabilidad entre folds, complejidad, errores por segmentos e interpretación de negocio.
- Mantener la prueba final como evaluación única; no cambiar modelo, umbral o relato después de ver sus resultados.
- Explicar qué solución se recomienda, bajo qué condiciones y por qué una alternativa más compleja no necesariamente es mejor.
- Actualizar notebook 05, README e informe/presentación para que compartan los mismos números, parámetros, caveats y referencias a la evidencia.
- La decisión quedó documentada en [`decision_cesar.md`](decision_cesar.md), el notebook 05 y la presentación EP3; revisar en conjunto antes de abrir el PR de esta rama.
- Conservar sesgos, ética, privacidad, límites de popularidad histórica y recomendaciones de revisión humana.
- Organizar la presentación para un máximo de 10 minutos y participar en la defensa cruzada de todo el pipeline.

## Accuracy: decisión con el docente

No llamar accuracy a MAE, R² ni a la precisión del KPI del 10% superior. El objetivo actual es regresión. Si se confirma que la calificación exige accuracy, definir con Lucas e Ignacio si se agrega clasificación y cuál es la etiqueta.

Para `popularity >= 70`, la prevalencia en la prueba actual es 3,64%; predecir siempre la clase negativa alcanza 96,36% de accuracy. Ese baseline hace que “accuracy ≥80%” sea insuficiente como criterio de calidad. Informar baseline y métricas sensibles al desbalance; no presentar el resultado trivial como éxito del modelo.

## Criterios de revisión

Las cifras del resumen deben rastrearse al notebook 05 y su salida; el argumento de selección debe incluir comparación con baseline y describir trade-offs. Ignacio revisa la integración antes del PR final.
