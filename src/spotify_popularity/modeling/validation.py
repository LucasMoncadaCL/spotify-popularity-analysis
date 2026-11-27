"""Validación IE11 sobre entrenamiento, con auditoría de separación por artista."""

from dataclasses import dataclass
from hashlib import sha256
from time import perf_counter

import numpy as np
import pandas as pd
from joblib import Parallel, delayed, parallel_config
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold
from sklearn.tree import DecisionTreeRegressor

from spotify_popularity.modeling.protocol import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    SEED,
    model_pipeline,
    primary_artist,
    regression_metrics,
)


@dataclass(frozen=True)
class ValidationFold:
    """Posiciones sobre el entrenamiento, nunca sobre el dataset completo."""

    strategy: str
    number: int
    fit: np.ndarray
    validation: np.ndarray


def id_fingerprint(identifiers) -> str:
    """Huella compatible con la partición compartida."""
    return sha256("\n".join(sorted(map(str, identifiers))).encode("utf-8")).hexdigest()


def ep3_candidates() -> dict:
    """Candidatos congelados del handoff de Lucas; no realiza otra búsqueda."""
    return {
        "Dummy mediana": DummyRegressor(strategy="median"),
        "Ridge": model_pipeline(Ridge(alpha=0.1)),
        "Árbol": model_pipeline(
            DecisionTreeRegressor(max_depth=15, min_samples_leaf=20, random_state=SEED)
        ),
        "Random Forest": model_pipeline(
            RandomForestRegressor(
                n_estimators=100,
                max_depth=None,
                min_samples_leaf=1,
                max_features=1.0,
                random_state=SEED,
                n_jobs=1,
            )
        ),
    }


def validation_plan(training: pd.DataFrame, reserved_ids, *, n_splits: int = 3):
    """Construye folds comunes y falla si recibe una canción de la prueba final."""
    identifiers = training["track_id"]
    if identifiers.isna().any() or identifiers.duplicated().any():
        raise ValueError("track_id debe ser único y no nulo.")
    reserved = set(map(str, reserved_ids))
    if set(identifiers.astype(str)) & reserved:
        raise ValueError("El entrenamiento contiene IDs de la prueba reservada.")
    groups = training["artists"].map(primary_artist)
    artists = training["artists"].map(
        lambda value: tuple(
            name.strip().casefold() for name in str(value).split(";") if name.strip()
        )
    )
    splitters = {
        "KFold": KFold(n_splits=n_splits, shuffle=True, random_state=SEED),
        "GroupKFold": GroupKFold(n_splits=n_splits, shuffle=False),
    }
    folds, audit = [], []
    assignments = training[["track_id"]].reset_index(drop=True).copy()
    for strategy, splitter in splitters.items():
        assignment = np.zeros(len(training), dtype=int)
        splits = (
            splitter.split(training, groups=groups)
            if strategy == "GroupKFold"
            else splitter.split(training)
        )
        for number, (fit, validation) in enumerate(splits, start=1):
            fit_ids = set(identifiers.iloc[fit])
            validation_ids = set(identifiers.iloc[validation])
            overlap = set(groups.iloc[fit]) & set(groups.iloc[validation])
            if fit_ids & validation_ids or (strategy == "GroupKFold" and overlap):
                raise ValueError("Hay fuga de IDs o artistas principales entre folds.")
            all_fit_artists = {name for row in artists.iloc[fit] for name in row}
            secondary_shared = artists.iloc[validation].map(
                lambda names, known=all_fit_artists: bool(set(names[1:]) & known)
            )
            audit.append(
                {
                    "estrategia": strategy,
                    "fold": number,
                    "fit_canciones": len(fit),
                    "validacion_canciones": len(validation),
                    "fit_artistas_principales": groups.iloc[fit].nunique(),
                    "validacion_artistas_principales": groups.iloc[validation].nunique(),
                    "principales_compartidos": len(overlap),
                    "validacion_con_secundario_en_fit": int(secondary_shared.sum()),
                    "fit_sha256": id_fingerprint(fit_ids),
                    "validacion_sha256": id_fingerprint(validation_ids),
                    "prueba_ids_en_fold": len((fit_ids | validation_ids) & reserved),
                }
            )
            folds.append(ValidationFold(strategy, number, fit, validation))
            assignment[validation] += number
        if (assignment == 0).any():
            raise ValueError("Cada canción debe pertenecer a un fold de validación.")
        assignments[strategy] = assignment
    return folds, pd.DataFrame(audit), assignments


def _score_fold(estimator, name, training, fold):
    features = list(NUMERIC_FEATURES) + list(CATEGORICAL_FEATURES) + ["track_genres"]
    fit = training.iloc[fold.fit]
    validation = training.iloc[fold.validation]
    fitted = clone(estimator)
    started = perf_counter()
    fitted.fit(fit[features], fit["popularity"])
    fit_seconds = perf_counter() - started
    predicted = fitted.predict(validation[features])
    scores = regression_metrics(validation["popularity"], predicted)
    train_scores = regression_metrics(fit["popularity"], fitted.predict(fit[features]))
    return {
        "estrategia": fold.strategy,
        "fold": fold.number,
        "modelo": name,
        **scores,
        **{f"{metric}_train": value for metric, value in train_scores.items()},
        "brecha_MAE": scores["MAE"] - train_scores["MAE"],
        "fit_seconds": fit_seconds,
    }


def evaluate_validation(training, folds, candidates=None, *, n_jobs: int = 3):
    """Clona y ajusta cada pipeline desde cero; no recibe datos de prueba."""
    if candidates is None:
        candidates = ep3_candidates()
    with parallel_config(backend="loky", inner_max_num_threads=1):
        rows = Parallel(n_jobs=n_jobs, pre_dispatch=n_jobs)(
            delayed(_score_fold)(estimator, name, training, fold)
            for name, estimator in candidates.items()
            for fold in folds
        )
    return pd.DataFrame(rows)


def summarize_validation(scores: pd.DataFrame) -> pd.DataFrame:
    """Media y DE poblacional (ddof=0), como en la evidencia de Lucas."""
    rows = []
    for (strategy, name), group in scores.groupby(["estrategia", "modelo"], sort=False):
        row = {"estrategia": strategy, "modelo": name, "folds": len(group)}
        for metric in ("MAE", "RMSE", "R2", "MAE_train", "brecha_MAE", "fit_seconds"):
            row[f"{metric}_media"] = float(group[metric].mean())
            row[f"{metric}_sd"] = float(group[metric].std(ddof=0))
        rows.append(row)
    return pd.DataFrame(rows)
