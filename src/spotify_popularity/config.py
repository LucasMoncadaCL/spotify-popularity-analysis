"""Configuración central de rutas del proyecto."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Rutas absolutas derivadas de la ubicación del paquete."""

    root: Path

    @property
    def data_raw(self) -> Path:
        return self.root / "data" / "raw"

    @property
    def data_interim(self) -> Path:
        return self.root / "data" / "interim"

    @property
    def data_processed(self) -> Path:
        return self.root / "data" / "processed"

    @property
    def figures(self) -> Path:
        return self.root / "reports" / "figures"

    @property
    def raw_dataset(self) -> Path:
        return self.data_raw / "Spotify_Tracks_Dataset.csv"

    def create_generated_directories(self) -> None:
        """Crea únicamente directorios destinados a resultados regenerables."""

        for directory in (self.data_interim, self.data_processed, self.figures):
            directory.mkdir(parents=True, exist_ok=True)


PROJECT_PATHS = ProjectPaths(root=Path(__file__).resolve().parents[2])
