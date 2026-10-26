"""Partición y preparación comunes para los tres notebooks de modelamiento."""

from dataclasses import dataclass
from hashlib import sha256

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted

NUMERIC_FEATURES = (
    "duration_ms",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
)
CATEGORICAL_FEATURES = ("key", "mode", "time_signature", "explicit")
TARGET = "popularity"
SEED = 42


@dataclass(frozen=True)
class TrackSplit:
    """IDs compartidos para ajuste, validación y prueba."""

    train_ids: tuple[str, ...]
    fit_ids: tuple[str, ...]
    validation_ids: tuple[str, ...]
    test_ids: tuple[str, ...]
    test_sha256: str


def split_track_ids(data: pd.DataFrame) -> TrackSplit:
    """Aplica el 80/20 y luego reserva el 20% del entrenamiento para validación."""

    if "track_id" not in data:
        raise ValueError("Falta track_id.")
    if data["track_id"].isna().any():
        raise ValueError("track_id debe ser único y no nulo.")
    identifiers = data["track_id"].astype(str)
    if identifiers.duplicated().any():
        raise ValueError("track_id debe ser único y no nulo.")
    ordered = sorted(identifiers.tolist())
    train_ids, test_ids = train_test_split(ordered, test_size=0.20, shuffle=True, random_state=SEED)
    fit_ids, validation_ids = train_test_split(
        sorted(train_ids), test_size=0.20, shuffle=True, random_state=SEED
    )
    fingerprint = sha256("\n".join(sorted(test_ids)).encode("utf-8")).hexdigest()
    return TrackSplit(
        train_ids=tuple(train_ids),
        fit_ids=tuple(fit_ids),
        validation_ids=tuple(validation_ids),
        test_ids=tuple(test_ids),
        test_sha256=fingerprint,
    )


def primary_artist(artists: str) -> str:
    """Normaliza el primer artista de la lista separada por punto y coma."""

    if pd.isna(artists):
        raise ValueError("artists contiene valores nulos.")
    name = str(artists).split(";", maxsplit=1)[0].strip().casefold()
    if not name:
        raise ValueError("artists contiene un artista principal vacío.")
    return name


def split_primary_artist_ids(data: pd.DataFrame) -> TrackSplit:
    """Crea prueba y validación disjuntas por artista principal."""

    if not {"track_id", "artists"}.issubset(data.columns):
        raise ValueError("Faltan track_id o artists.")
    if data["track_id"].isna().any() or data["track_id"].duplicated().any():
        raise ValueError("track_id debe ser único y no nulo.")
    ordered = data.sort_values("track_id", kind="stable").reset_index(drop=True)
    groups = ordered["artists"].map(primary_artist)
    outer = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=SEED)
    train_idx, test_idx = next(outer.split(ordered, groups=groups))
    inner = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=SEED)
    fit_local, validation_local = next(
        inner.split(ordered.iloc[train_idx], groups=groups.iloc[train_idx])
    )
    train_ids = tuple(ordered.iloc[train_idx]["track_id"].astype(str))
    test_ids = tuple(ordered.iloc[test_idx]["track_id"].astype(str))
    fit_ids = tuple(ordered.iloc[train_idx[fit_local]]["track_id"].astype(str))
    validation_ids = tuple(ordered.iloc[train_idx[validation_local]]["track_id"].astype(str))
    fingerprint = sha256("\n".join(sorted(test_ids)).encode("utf-8")).hexdigest()
    return TrackSplit(train_ids, fit_ids, validation_ids, test_ids, fingerprint)


class GenreBinarizer(TransformerMixin, BaseEstimator):
    """Codifica los géneros separados por | aprendidos solo en entrenamiento."""

    def fit(self, values: pd.DataFrame, y: object = None) -> "GenreBinarizer":
        labels = self._labels(values)
        self.classes_ = tuple(sorted({label for row in labels for label in row}))
        self.encoder_ = MultiLabelBinarizer(classes=self.classes_, sparse_output=True).fit(labels)
        return self

    def transform(self, values: pd.DataFrame):
        check_is_fitted(self, "classes_")
        labels = self._labels(values)
        known = set(self.classes_)
        return self.encoder_.transform(
            [tuple(label for label in row if label in known) for row in labels]
        )

    def get_feature_names_out(self, input_features=None) -> np.ndarray:
        check_is_fitted(self, "classes_")
        return np.asarray([f"genre_{name}" for name in self.classes_], dtype=object)

    @staticmethod
    def _labels(values: pd.DataFrame) -> list[tuple[str, ...]]:
        if isinstance(values, pd.DataFrame):
            source = values.iloc[:, 0]
        else:
            source = pd.Series(np.asarray(values).reshape(-1))
        if source.isna().any():
            raise ValueError("track_genres contiene valores nulos.")
        return [tuple(dict.fromkeys(str(value).split("|"))) for value in source]


def build_preprocessor(*, include_genres: bool = True) -> ColumnTransformer:
    """Escala números y codifica categorías/géneros dentro del pipeline."""

    transformers = [
        ("numeric", StandardScaler(), list(NUMERIC_FEATURES)),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            list(CATEGORICAL_FEATURES),
        ),
    ]
    if include_genres:
        transformers.append(("genres", GenreBinarizer(), ["track_genres"]))
    return ColumnTransformer(transformers, remainder="drop", sparse_threshold=1.0)


def model_pipeline(estimator, *, include_genres: bool = True) -> Pipeline:
    """Asegura que toda transformación se ajuste en la partición correspondiente."""

    return Pipeline(
        [("preprocessing", build_preprocessor(include_genres=include_genres)), ("model", estimator)]
    )


def genre_only_pipeline(estimator) -> Pipeline:
    """Usa exclusivamente las etiquetas de género como predictores."""

    preprocessor = ColumnTransformer(
        [("genres", GenreBinarizer(), ["track_genres"])],
        remainder="drop",
        sparse_threshold=1.0,
    )
    return Pipeline([("preprocessing", preprocessor), ("model", estimator)])


def audio_pipeline(estimator, *, include_genres: bool = False) -> Pipeline:
    """Usa solo los diez atributos numéricos de audio, opcionalmente con géneros."""

    transformers = [("numeric", StandardScaler(), list(NUMERIC_FEATURES))]
    if include_genres:
        transformers.append(("genres", GenreBinarizer(), ["track_genres"]))
    preprocessor = ColumnTransformer(transformers, remainder="drop", sparse_threshold=1.0)
    return Pipeline([("preprocessing", preprocessor), ("model", estimator)])


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    """Métricas en la escala original de popularidad."""

    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "R2": float(r2_score(y_true, y_pred)),
    }


def top_decile_kpi(track_ids, y_true, y_pred) -> dict[str, float | int]:
    """Precisión, recall y lift del 10% superior en esta muestra."""

    ranked = pd.DataFrame(
        {
            "track_id": np.asarray(track_ids),
            "actual": np.asarray(y_true),
            "predicted": np.asarray(y_pred),
        }
    ).sort_values(["predicted", "track_id"], ascending=[False, True])
    if ranked.empty:
        raise ValueError("No hay canciones para calcular el KPI.")
    capacity = int(np.ceil(len(ranked) * 0.10))
    positives = int(ranked["actual"].ge(70).sum())
    selected = int(ranked.iloc[:capacity]["actual"].ge(70).sum())
    prevalence = positives / len(ranked)
    precision = selected / capacity
    return {
        "seleccionadas": capacity,
        "populares_en_seleccion": selected,
        "populares_en_prueba": positives,
        "prevalencia": prevalence,
        "precision": precision,
        "recall": selected / positives if positives else float("nan"),
        "lift": precision / prevalence if prevalence else float("nan"),
    }
