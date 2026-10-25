# Alcance individual de César para la EA2

**Rama:** `feature/ea2-modeling-cesar`  
**Notebook:** `notebooks/04c_modeling_cesar.ipynb`  
**Destino del PR:** `dev`

## Trabajo individual

El notebook reproduce el protocolo común del equipo: partición aleatoria de canciones, referencia mediana, Ridge, árbol, métricas fuera de muestra, KPI retrospectivo, errores por rangos, K-Means, perfiles y visualización PCA.

La contribución específica de César audita MAE, RMSE, sesgo y recuperación de canciones con popularidad ≥ 70 por contenido explícito y por género. El análisis de géneros expande las etiquetas múltiples después de predecir, muestra el soporte por canción única y advierte que cada canción puede aparecer en varios grupos. El notebook también reproduce la evaluación con separación por artista principal, selección de parámetros en validación agrupada y conteo de colaboradores secundarios compartidos.

Los resultados son de una muestra histórica equilibrada artificialmente por género. Se presentan como evidencia descriptiva; no implican causalidad, éxito futuro ni una regla automática de promoción.

## Reproducción

Desde la raíz del proyecto:

```powershell
uv sync --locked
uv run python scripts/build_base_dataset.py
uv run python scripts/build_processed_dataset.py
uv run python -m nbconvert --to notebook --execute notebooks/04c_modeling_cesar.ipynb --inplace --ExecutePreprocessor.timeout=1800
```

El notebook registra las huellas de la fuente y de ambas particiones. Genera figuras en `reports/figures/ea2/` con prefijo `04c_cesar_`. Para la integración, el notebook 05 debe volver a calcular las cifras y mantener las limitaciones asociadas a cada partición y segmento.
