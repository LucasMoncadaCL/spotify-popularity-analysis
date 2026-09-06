"""Diagnósticos reutilizables de calidad de datos."""

import pandas as pd


def dataset_overview(data: pd.DataFrame, id_column: str = "track_id") -> dict[str, int]:
    """Resume dimensiones, ausencia y duplicidad sin transformar los datos."""

    if id_column not in data.columns:
        raise ValueError(f"No existe la columna identificadora: {id_column}")

    identifier_counts = data[id_column].value_counts(dropna=False)
    repeated_counts = identifier_counts[identifier_counts > 1]

    return {
        "row_count": len(data),
        "column_count": data.shape[1],
        "missing_cells": int(data.isna().sum().sum()),
        "exact_duplicate_rows": int(data.duplicated().sum()),
        "unique_track_ids": int(data[id_column].nunique(dropna=True)),
        "repeated_track_ids": len(repeated_counts),
        "rows_with_repeated_track_id": int(repeated_counts.sum()),
        "extra_track_id_rows": int((repeated_counts - 1).sum()),
    }


def column_quality_report(data: pd.DataFrame) -> pd.DataFrame:
    """Devuelve métricas básicas de calidad para cada columna."""

    row_count = len(data)
    report = pd.DataFrame(
        {
            "dtype": data.dtypes.astype(str),
            "missing_count": data.isna().sum(),
            "missing_pct": data.isna().mean().mul(100),
            "unique_count": data.nunique(dropna=False),
        }
    )
    report["duplicate_count"] = row_count - report["unique_count"]
    return report.sort_values(["missing_pct", "unique_count"], ascending=[False, True])
