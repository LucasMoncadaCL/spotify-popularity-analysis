"""Controles de fuga, cobertura de folds y ajuste independiente para IE11."""

import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor

from spotify_popularity.modeling.protocol import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from spotify_popularity.modeling.validation import (
    evaluate_validation,
    summarize_validation,
    validation_plan,
)


def _training():
    rows = []
    for group in range(6):
        for song in range(3):
            rows.append(
                {
                    **dict.fromkeys(NUMERIC_FEATURES, 0.5),
                    **dict.fromkeys(CATEGORICAL_FEATURES, 1),
                    "track_id": f"{group}-{song}",
                    "artists": f" Artist {group} ; Shared guest",
                    "track_genres": "pop",
                    "popularity": float(group * 10 + song),
                }
            )
    return pd.DataFrame(rows)


def test_group_folds_isolate_principals_cover_training_and_count_secondary_overlap():
    data = _training()
    folds, audit, assignments = validation_plan(data, ["reserved"])
    repeated = validation_plan(data, ["reserved"])[2]
    pd.testing.assert_frame_equal(assignments, repeated)
    for strategy in ("KFold", "GroupKFold"):
        positions = np.concatenate([f.validation for f in folds if f.strategy == strategy])
        assert sorted(positions.tolist()) == list(range(len(data)))
    grouped = audit.loc[audit.estrategia.eq("GroupKFold")]
    assert grouped.principales_compartidos.eq(0).all()
    assert grouped.validacion_con_secundario_en_fit.eq(grouped.validacion_canciones).all()
    assert audit.prueba_ids_en_fold.eq(0).all()


def test_plan_rejects_reserved_test_ids_and_duplicate_tracks():
    data = _training()
    with pytest.raises(ValueError, match="prueba reservada"):
        validation_plan(data, [data.track_id.iloc[0]])
    with pytest.raises(ValueError, match="único"):
        validation_plan(pd.concat([data, data.iloc[:1]]), [])


def test_each_fold_fits_its_own_model_without_mutating_candidate():
    data = _training()
    folds, _, _ = validation_plan(data, ["reserved"])
    estimator = DummyRegressor(strategy="median")
    scores = evaluate_validation(data, folds, {"Dummy": estimator}, n_jobs=1)
    assert not hasattr(estimator, "constant_")
    for fold, row in zip(folds, scores.itertuples(), strict=True):
        expected = np.abs(
            data.popularity.iloc[fold.validation] - data.popularity.iloc[fold.fit].median()
        ).mean()
        assert pytest.approx(expected) == row.MAE
    summary = summarize_validation(scores)
    assert summary.folds.eq(3).all()
    assert summary.iloc[0].MAE_sd == pytest.approx(scores.iloc[:3].MAE.std(ddof=0))
