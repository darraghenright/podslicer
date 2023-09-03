import pytest

from podslicer.track import Metadata

from .conftest import MetadataDict


def test_track_metadata_can_be_json_encoded(
    metadata_dict: MetadataDict, metadata_json: str
) -> None:
    assert Metadata(**metadata_dict).json() == metadata_json


@pytest.mark.parametrize(
    "current,total,expected",
    [
        (0, 100, 0),
        (1, 30, 3.3),
        (10, 200, 5),
        (50, 100, 50),
        (100, 100, 100),
    ],
)
def test_track_progress(current: int, total: int, expected: int) -> None:
    metadata = Metadata(
        current=current,
        extension=".m4a",
        total=total,
    )

    assert metadata.progress() == expected

