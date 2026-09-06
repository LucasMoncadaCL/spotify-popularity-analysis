# Guía de colaboración

Este documento define cómo trabajar de forma consistente en **Spotify Popularity Analysis**.
Todas las contribuciones deben seguir estas reglas para conservar trazabilidad,
reproducibilidad y un historial fácil de revisar.

## Equipo y acceso

| Cuenta de GitHub | Estado/función |
|---|---|
| [`LucasMoncadaCL`](https://github.com/LucasMoncadaCL) | Propietario del repositorio; responsable inicial de comprensión del negocio y CRISP-DM |
| [`yvvvl`](https://github.com/yvvvl) | Colaborador invitado con permiso de escritura |
| [`Cesitar16`](https://github.com/Cesitar16) | Colaborador invitado con permiso de escritura |

Los colaboradores invitados deben aceptar la invitación antes de clonar o publicar ramas.
El repositorio es privado y no debe hacerse público sin aprobación del equipo.

## Preparación inicial

```powershell
git clone https://github.com/LucasMoncadaCL/spotify-popularity-analysis.git
cd spotify-popularity-analysis
git switch dev
uv sync
```

No es necesario activar `.venv` manualmente. Los comandos Python deben ejecutarse con
`uv run` para usar el entorno bloqueado en `uv.lock`.

Cada integrante debe comprobar su identidad antes de crear commits:

```powershell
git config user.name
git config user.email
gh auth status
```

## GitFlow simplificado

### Ramas permanentes

- `main`: entregas estables y versiones finales de la evaluación.
- `dev`: integración del trabajo terminado y revisado.

No se realizan commits directos en `main` ni `dev`. Toda modificación se desarrolla en una
rama temporal y se integra mediante Pull Request.

### Ramas temporales permitidas

- `feature/<descripcion>`: nueva funcionalidad, análisis o documentación.
- `fix/<descripcion>`: corrección de un defecto en desarrollo.
- `hotfix/<descripcion>`: corrección urgente de una versión ya publicada en `main`.

Los nombres técnicos se escriben en inglés, con minúsculas y guiones:

```text
feature/data-preparation
feature/exploratory-analysis
feature/ethics-and-privacy
fix/notebook-paths
```

No deben crearse ramas `codex/*`, ramas permanentes por persona ni nombres como `rama-final`
o `prueba-2`.

## Inicio de una tarea

Actualizar `dev` y crear la rama desde ella:

```powershell
git switch dev
git pull --ff-only origin dev
git switch -c feature/nombre-de-la-tarea
```

Una rama debe contener una tarea concreta. No se deben mezclar limpieza, EDA, modelamiento y
presentación en el mismo cambio.

## Convención de commits

El tipo técnico se conserva en inglés y el título descriptivo se escribe en español:

```text
feat: agrega preparación reproducible del dataset
fix: corrige rutas relativas del notebook
docs: documenta decisiones de limpieza
test: valida el tratamiento de duplicados
refactor: separa transformaciones por responsabilidad
chore: actualiza dependencias del entorno
```

Reglas:

- Usar verbos en presente: `agrega`, `corrige`, `documenta`, `separa`.
- Mantener cada commit pequeño y coherente.
- No usar mensajes como `cambios`, `avance`, `final` o `arreglos varios`.
- No incluir archivos ajenos a la tarea.
- No reescribir commits que otra persona ya esté utilizando sin coordinación previa.

## Validación antes de publicar

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Si se modifica un notebook, también debe ejecutarse completamente desde el entorno del
proyecto y quedar sin celdas con errores. Las afirmaciones del README deben coincidir con sus
resultados reales.

## Publicación y Pull Request

```powershell
git push -u origin feature/nombre-de-la-tarea
gh pr create --base dev --head feature/nombre-de-la-tarea
```

El título y la descripción del Pull Request se redactan en español. Debe incluir:

- Resumen de lo desarrollado.
- Decisiones relevantes.
- Archivos o etapas afectadas.
- Verificaciones ejecutadas.
- Limitaciones o trabajo pendiente.

Después de la revisión se integra con merge commit para conservar los commits individuales.
La rama temporal se elimina una vez confirmada la integración.

## Trabajo con notebooks

- Solo una persona debe editar un notebook específico a la vez.
- Los notebooks se numeran según el orden del flujo analítico.
- La explicación y las conclusiones se escriben en celdas Markdown.
- La lógica reutilizable pertenece a `src/`, no debe copiarse entre notebooks.
- Las celdas deben poder ejecutarse en orden desde el inicio.
- No se deben escribir rutas personales como `C:\\Users\\nombre\\...`.

Antes de editar un notebook compartido, avisar al equipo qué archivo y sección se trabajará.
Esto reduce conflictos difíciles de resolver en archivos `.ipynb`.

## Datos y resultados

- `data/raw/` contiene los datos originales y nunca debe modificarse.
- `data/interim/` y `data/processed/` contienen resultados regenerables.
- No deben versionarse secretos, tokens, credenciales ni archivos `.env`.
- Las figuras seleccionadas para el informe se guardan en `reports/figures/`.
- Toda limpieza debe quedar justificada en el notebook y, cuando corresponda, en el README.
- Las particiones de entrenamiento y prueba deberán impedir que un mismo `track_id` quede en
  ambos conjuntos.

## Integración en `main`

Cuando el equipo complete y revise un hito:

1. Verificar `dev` desde un entorno limpio.
2. Abrir un Pull Request de `dev` hacia `main`.
3. Revisar notebook, README, datos, figuras y pruebas.
4. Integrar con merge commit.
5. Crear una etiqueta de versión, por ejemplo `ep1-v1.0.0`.

`main` no se actualiza por cada tarea individual; representa hitos completos y defendibles.

## Comunicación y resolución de conflictos

- Avisar antes de modificar archivos compartidos como `README.md` o un notebook existente.
- Resolver los conflictos en la rama temporal, nunca directamente en `dev` o `main`.
- No eliminar ni sobrescribir trabajo de otro integrante sin revisarlo con su autor.
- Si una decisión cambia el significado de los datos, registrarla explícitamente.
- Cuando una prueba falle, corregir la causa antes de solicitar integración.

