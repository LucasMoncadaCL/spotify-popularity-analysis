# Traspaso a César — EP3 / IE11 de Ignacio

César, dejé el trabajo de IE11 en **`feature/ep3-ignacio-validation`**, con destino
**`dev`**. El notebook `04b_modeling_ignacio.ipynb` conserva EA2 y añade la validación
aleatoria y por artista principal de Dummy, Ridge, árbol y el bosque de Lucas.
El [informe de Ignacio](informe_ignacio.md) contiene cifras, decisiones, límites y reproducción.

<!-- RESUMEN_CESAR_INICIO -->
La ejecución completa terminó sin errores: **14 celdas de código**,
**24 ajustes de validación** y tablas de media/DE por modelo. La CV aleatoria reproduce
la de Lucas. El bosque obtiene MAE **9,901 ± 0,018**
en KFold y **11,752 ± 0,458** en GroupKFold;
Ridge agrupado obtiene **12,061 ± 0,408**.
La brecha entrenamiento/validación agrupada del bosque es **8,060**.
La prueba compartida se conserva: su MAE de bosque **9,648**
se cita del CSV publicado por Lucas y no de una nueva evaluación en IE11.
Hay cero principales compartidos en los folds agrupados, pero siguen existiendo
colaboradores secundarios compartidos; no se afirma transferencia temporal.
<!-- RESUMEN_CESAR_FIN -->

Para IE12, la ventaja agrupada del bosque sobre Ridge en MAE es de solo **0,309 puntos**.
Ridge queda ligeramente mejor en RMSE (**16,858** frente a **16,969**) y R²
(**0,328** frente a **0,319**), con un ajuste mucho más rápido. No presentar al bosque
como ganador de todas las métricas ni interpretar tres folds como prueba de significancia.

Para continuar:

1. Revisar el notebook ejecutado, informe y CSV `04b_ignacio_*` en
   `reports/figures/ea3/`. Lucas revisa IE11 según la rotación acordada; esa revisión
   humana queda pendiente y no se presenta como aprobada automáticamente.
2. Cuando la revisión esté resuelta, integrar este PR en `dev` con **merge commit**.
   La rama está publicada para que tú hagas el merge; no se integra automáticamente.
3. Crear `feature/ep3-cesar-integration` desde `dev` actualizado e implementar IE12
   usando los resultados de Lucas (PR #24) e Ignacio. Comparar error, dispersión,
   brecha de entrenamiento, costo, segmentos y utilidad antes de justificar la solución.
4. Actualizar `notebooks/05_model_comparison.ipynb`, `README.md` e informe/presentación
   EP3 con las mismas cifras y parámetros. La presentación debe durar como máximo
   diez minutos y conservar los límites del muestreo histórico, géneros y revisión humana.
5. Mantener la prueba compartida y sus métricas publicadas; no repetir búsqueda ni
   ajustar umbrales a partir del test. Citar que IE11 reutiliza la prueba de Lucas,
   mientras que la validación por artista se hace dentro de entrenamiento.
6. Confirmar con el docente qué significa «accuracy 80%». El trabajo actual es regresión;
   MAE/R² y precisión del ranking no son accuracy. No presentar el baseline mayoritario
   de 96,36% como éxito de detección de canciones populares. Si se exige clasificación,
   acordar primero clases, umbral y métricas sensibles al desbalance.

La evaluación por artista principal conserva colaboradores secundarios compartidos.
Además, el bosque fue preseleccionado con este entrenamiento: la CV nueva es un diagnóstico
de candidatos fijos, no CV anidada independiente de esa selección. Tampoco demuestra
transferencia temporal o éxito de canciones futuras. Estas reservas deben acompañar IE12.

Para reproducir, seguir el comando completo del informe. Las pruebas automatizadas y
la ejecución del notebook son evidencia técnica; revisión cruzada y ensayo de defensa
siguen siendo tareas humanas del equipo.
