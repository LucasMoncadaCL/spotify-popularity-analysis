# Informe de Lucas para EA2

Este directorio contiene el informe individual de Lucas para revisar con Ignacio y César:

- `main.tex` y `sections/`: fuente editable.
- `images/`: seis figuras incluidas en el informe. Cuatro provienen del notebook `04a_modeling_lucas.ipynb` (la selección de K se extrajo de su salida ejecutada) y dos del EDA de EP1.
- `informe_lucas.pdf`: compilación revisada del informe.

El notebook es la evidencia ejecutable de los resultados. El informe resume el método,
las cifras y sus límites, e identifica las preguntas que quedan para la integración.

## Compilar

Desde este directorio, con MiKTeX y `pdflatex` disponibles:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

El PDF resultante será `main.pdf`; se puede renombrar a `informe_lucas.pdf`. La segunda
pasada resuelve referencias y tabla de contenido. Si se usa `latexmk`, MiKTeX requiere
una instalación de Perl. Los archivos auxiliares (`.aux`, `.log`, `.toc`, `.out`) no son
parte del informe.

## Para la revisión del equipo

1. Seguir la reproducción desde instalación limpia descrita en `docs/ea2/lucas.md`.
2. Comparar las huellas de fuente y particiones antes de trasladar cifras al notebook 05.
3. Revisar especialmente la dependencia de los géneros, los errores de canciones populares,
   el alcance del corte por artista principal y la estabilidad moderada de K-Means.
4. Distinguir los resultados medidos de las hipótesis propuestas para la integración.
