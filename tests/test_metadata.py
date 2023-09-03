from pathlib import Path

import pytest

from podslicer.track import Metadata


@pytest.fixture()
def metadata(tmp_path: Path) -> Metadata:
    return Metadata(current=0, extension=".m4a", path=tmp_path, total=1)


def test_metadata_can_be_json_encoded(metadata: Metadata, metadata_json: str) -> None:
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
def test_metadata_can_report_progress(
    current: int, total: int, expected: int, tmp_path: Path
) -> None:
    metadata = Metadata(current=current, extension=".m4a", path=tmp_path, total=total)

    assert metadata.progress() == expected


def test_metadata_should_return_audio_filepath(
    metadata: Metadata, tmp_path: Path
) -> None:
    assert metadata.audio() == tmp_path / "0.m4a"


def test_metadata_should_return_transcript_filepath(
    metadata: Metadata, tmp_path: Path
) -> None:
    assert metadata.transcript() == tmp_path / "0.txt"


def test_increment_should_increase_current_index(metadata: Metadata) -> None:
    assert metadata.current == 0

    metadata.increment()

    assert metadata.current == 1

    with pytest.raises(IndexError):
        metadata.increment()

    assert metadata.current == 1
