# Informe técnico extendido en LaTeX

Esta carpeta contiene documentación complementaria del proyecto. El `README.md` de la raíz
sigue siendo el informe Markdown oficial exigido por la pauta; los notebooks conservan la
evidencia ejecutable. El documento LaTeX consolida esa evidencia y añade material para la defensa.

## Estructura

- `main.tex`: portada, configuración e inclusión ordenada de secciones.
- `sections/`: capítulos temáticos del informe.
- `bibliography.bib`: fuentes realmente citadas.
- `tables/`: tablas generadas reproduciblemente mediante Python.
- `../../reports/figures/`: fuente única de las figuras; no se copian aquí.

## Reproducción de tablas y compilación

Desde la raíz del repositorio:

```powershell
uv run python scripts/build_processed_dataset.py
uv run python scripts/build_latex_tables.py
New-Item -ItemType Directory -Force output/pdf | Out-Null
Set-Location docs/latex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../../output/pdf main.tex
```

La salida final queda en `output/pdf/main.pdf`. La instalación de LaTeX debe proporcionar
`latexmk`, `pdflatex`, BibTeX y los paquetes declarados en `main.tex`.

Si MiKTeX dispone de `pdflatex` y BibTeX, pero `latexmk` no puede ejecutarse por falta de Perl,
puede usarse la secuencia equivalente desde `docs/latex/`:

```powershell
pdflatex '--output-directory=..\..\output\pdf' -interaction=nonstopmode -halt-on-error main.tex
bibtex ..\..\output\pdf\main
pdflatex '--output-directory=..\..\output\pdf' -interaction=nonstopmode -halt-on-error main.tex
pdflatex '--output-directory=..\..\output\pdf' -interaction=nonstopmode -halt-on-error main.tex
```

## Mantenimiento

Las cifras nuevas deben calcularse en Python y regenerarse con el script; no deben calcularse
dentro de LaTeX. Al actualizar el EDA, primero se ejecutan los notebooks y luego el generador de
tablas. Las figuras se referencian por rutas relativas desde `reports/figures/` para mantener una
sola fuente de verdad. No se deben copiar párrafos extensos entre este informe, el README y los
registros de progreso: cada artefacto conserva su propósito y se actualizan en conjunto cuando
cambia una decisión o un resultado.
