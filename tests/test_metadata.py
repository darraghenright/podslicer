from pathlib import Path

import pytest

from podslicer.track import Metadata

from .conftest import MetadataDict


def test_metadata_can_be_json_encoded(
    metadata_dict: MetadataDict, metadata_json: str
) -> None:
    metadata = Metadata(**metadata_dict)

    assert metadata.json() == metadata_json


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
def test_metadata_can_report_progress(current: int, total: int, expected: int) -> None:
    metadata = Metadata(current=current, extension=".m4a", total=total)

    assert metadata.progress() == expected


def test_metadata_can_return_audio_filename() -> None:
    metadata = Metadata(current=0, extension=".m4a", total=1)

    assert metadata.audio() == Path("0.m4a")


def test_metadata_can_return_transcript_filename() -> None:
    metadata = Metadata(current=0, extension=".m4a", total=1)

    assert metadata.transcript() == Path("0.txt")


def test_increment_should_increase_current_index() -> None:
    metadata = Metadata(current=0, extension=".m4a", total=1)

    assert metadata.current == 0

    metadata.increment()

    assert metadata.current == 1

    with pytest.raises(IndexError):
        metadata.increment()

    assert metadata.current == 1
