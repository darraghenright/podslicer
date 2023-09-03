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
    """
    tmp_path = tmp_path_factory.mktemp("tmp-")

    for seq in ("0", "1"):
        for ext in (".m4a", ".txt"):
            (tmp_path / Path(seq).with_suffix(ext)).write_text(seq)

    (tmp_path / METADATA_FILE).write_text(metadata_json)

    return tmp_path
