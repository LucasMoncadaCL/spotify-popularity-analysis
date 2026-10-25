# Alcance individual de Ignacio Silva para la EA2

**Rama:** `feature/ea2-modeling-ignacio`
**Notebook:** `notebooks/04b_modeling_ignacio.ipynb`
**Destino de integración:** `dev`

## Trabajo

El notebook reproduce el protocolo común de la EA2 con la fuente y preparación existentes, la partición aleatoria compartida por canción, `DummyRegressor(strategy="median")`, Ridge y árbol de decisión. Selecciona parámetros con entrenamiento y validación, informa MAE, RMSE y R² en prueba, calcula el KPI retrospectivo y analiza errores por rangos de popularidad. Incluye K-Means, perfiles en atributos originales y una visualización PCA.

La extensión personal es un diseño factorial 2×2: tratamiento estándar, `log1p(duration_ms)` con escalado estándar, `RobustScaler` y la combinación de transformación y escalado robusto. Los cuatro tratamientos conservan predictores, filas y candidatos. La selección de hiperparámetros y del tratamiento se hace en validación; la prueba se usa una vez para evaluación. Las transformaciones se ajustan dentro de los pipelines para evitar fuga.

## Interpretación

`log1p` comprime la cola larga de la duración. `RobustScaler` centra por la mediana y escala por el rango intercuartílico, reduciendo la influencia de valores extremos sobre la escala sin eliminar observaciones. Las diferencias de desempeño se limitan a esta muestra histórica, artificialmente balanceada por género; no demuestran causalidad, utilidad comercial ni éxito futuro. La integración final del equipo debe reproducir las cifras en el notebook 05.

## Reproducción

Desde la raíz del proyecto:

```powershell
uv sync --locked
uv run python scripts/build_base_dataset.py
uv run python scripts/build_processed_dataset.py
uv run python -m nbconvert --to notebook --execute notebooks/04b_modeling_ignacio.ipynb --inplace --ExecutePreprocessor.timeout=1800
```

Las figuras de esta contribución usan el prefijo `04b_ignacio_` en `reports/figures/ea2/`.
