import json
from pathlib import Path
from typing import TypedDict

import pytest
from pytest import TempPathFactory

from podslicer.track import METADATA_FILE


class MetadataDict(TypedDict):
    current: int
    extension: str
    total: int


@pytest.fixture()
def metadata_dict() -> MetadataDict:
    return {
        "current": 0,
        "extension": ".m4a",
        "total": 1,
    }


@pytest.fixture()
def metadata_json(metadata_dict: MetadataDict) -> str:
    return json.dumps(metadata_dict)


@pytest.fixture()
def track_path(metadata_json: str, tmp_path_factory: TempPathFactory) -> Path:
    """
    Create a temporary path with minimum expected
    set of files for a happy path test. Files can
    be deleted as required for individual tests.

    Creates and populates the following files:

    * 0.m4a
    * 0.txt
    * 1.m4a
    * 1.txt
    * metadata.json

    This fixture has test scope so files can be
    modified or deleted during individual tests.
    """
    tmp_path = tmp_path_factory.mktemp("tmp-")
    audio_bytes = (Path(__file__).parent / "assets/test.m4a").read_bytes()

    for seq in ("0", "1"):
        (tmp_path / Path(seq).with_suffix(".txt")).write_text(seq)
        (tmp_path / Path(seq).with_suffix(".m4a")).write_bytes(audio_bytes)

    (tmp_path / METADATA_FILE).write_text(metadata_json)

    return tmp_path
