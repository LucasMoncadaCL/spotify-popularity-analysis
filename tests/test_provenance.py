"""Pruebas de trazabilidad e integridad del dataset."""

import hashlib

from spotify_popularity.data.provenance import sha256_file


def test_sha256_file_matches_standard_library(tmp_path) -> None:
    dataset = tmp_path / "sample.csv"
    content = b"track_id,popularity\nabc,50\n"
    dataset.write_bytes(content)

    assert sha256_file(dataset) == hashlib.sha256(content).hexdigest()
