"""Construye el dataset limpio y consolidado para EDA y modelamiento."""

from spotify_popularity.config import PROJECT_PATHS
from spotify_popularity.data.loader import load_raw_dataset
from spotify_popularity.data.preparation import prepare_modeling_dataset


def main() -> None:
    """Genera el CSV procesado sin modificar la fuente original."""

    PROJECT_PATHS.create_generated_directories()
    prepared, summary = prepare_modeling_dataset(load_raw_dataset())
    output_path = PROJECT_PATHS.data_processed / "spotify_tracks_clean.csv"
    prepared.to_csv(output_path, index=False)
    print(f"Dataset procesado guardado en: {output_path}")
    print(
        "Filas: "
        f"{summary.input_rows:,} -> {summary.output_rows:,}; "
        f"inválidas retiradas: {summary.invalid_rows_removed:,}; "
        f"repeticiones consolidadas: {summary.repeated_track_ids_consolidated:,}."
    )


if __name__ == "__main__":
    main()
