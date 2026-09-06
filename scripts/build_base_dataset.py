"""Construye una copia base procesada conservando decisiones de EDA pendientes."""

from spotify_popularity.config import PROJECT_PATHS
from spotify_popularity.data.loader import load_raw_dataset, prepare_base_dataset


def main() -> None:
    """Carga, valida y guarda la versión base del dataset."""

    PROJECT_PATHS.create_generated_directories()
    raw_data = load_raw_dataset()
    prepared_data = prepare_base_dataset(raw_data)
    output_path = PROJECT_PATHS.data_processed / "spotify_tracks_base.csv"
    prepared_data.to_csv(output_path, index=False)
    print(f"Dataset base guardado en: {output_path}")
    print(f"Dimensiones: {prepared_data.shape[0]:,} filas × {prepared_data.shape[1]} columnas")


if __name__ == "__main__":
    main()
