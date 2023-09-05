import json
from pathlib import Path

import pytest

from podslicer.track import METADATA_FILE, Metadata


@pytest.fixture()
def metadata(track_path: Path) -> Metadata:
    return Metadata(current=0, extension=".m4a", path=track_path, total=1)


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
    current: int, total: int, expected: int, track_path: Path
) -> None:
    metadata = Metadata(current=current, extension=".m4a", path=track_path, total=total)

    assert metadata.progress() == expected


def test_metadata_should_return_path_to_audio_file(
    metadata: Metadata, track_path: Path
) -> None:
    assert metadata.audio() == track_path / "0.m4a"


def test_metadata_should_return_path_to_transcript_file(
    metadata: Metadata, track_path: Path
) -> None:
    assert metadata.transcript() == track_path / "0.txt"


def test_increment_should_increase_current_index(metadata: Metadata) -> None:
    assert metadata.current == 0

    metadata.increment()

    assert metadata.current == 1

    metadata.increment()

    assert metadata.current == 1


def test_increment_should_encode_and_save_progress(metadata: Metadata) -> None:
    path_to_json = metadata.path / METADATA_FILE

    assert path_to_json.is_file()

    first = path_to_json.read_text()
    metadata.increment()
    saved = path_to_json.read_text()

    assert json.loads(first)["current"] == 0
    assert json.loads(saved)["current"] == 1
