from json.decoder import JSONDecodeError
from pathlib import Path
from uuid import uuid4

import pytest

from podslicer.track import METADATA_FILE, Track


def test_track_requires_path() -> None:
    """
    Expect that an  instance of `Track`
    cannot be created without a path.
    """
    with pytest.raises(TypeError):
        Track()  # type: ignore


def test_track_requires_existing_path(tmp_path: Path) -> None:
    """
    Expect that an instance of `Track` cannot be
    created if the specified path does not exist.
    """
    path = tmp_path / uuid4().hex

    assert not path.exists()

    with pytest.raises(FileNotFoundError):
        Track(path=path)


def test_track_requires_metadata_file(track_path: Path) -> None:
    """
    Expect that an instance of `Track` cannot be created
    if no metadata file is found the specified path.
    """
    (track_path / METADATA_FILE).unlink()

    with pytest.raises(FileNotFoundError):
        Track(path=track_path)


def test_track_metadata_file_should_be_json(tmp_path: Path) -> None:
    """
    Expect that an instance of `Track` cannot be created
    if the metadata file does not contain valid JSON.
    """
    metadata_file = tmp_path / METADATA_FILE
    metadata_file.touch()

    assert metadata_file.is_file()

    with pytest.raises(JSONDecodeError):
        Track(path=tmp_path)


def test_track_metadata_can_be_read(track_path: Path) -> None:
    """
    Expect that an instance of `Track` can read a
    valid metadata JSON file and make its contents
    accessible as metadata properties.
    """
    track = Track(path=track_path)

    assert track.metadata.current == 0
    assert track.metadata.extension == ".m4a"
    assert track.metadata.total == 1


def test_track_requires_segment_audio_file(track_path: Path) -> None:
    """
    The value of `current` in a track's metadata is an index
    that represents progress throughout that track's segments.
    It's expected that both audio and transcript files numbered
    with this index are present at the specified path.

    Expect that the segment audio file exists and is readable.
    """
    (track_path / "0.m4a").unlink()

    with pytest.raises(FileNotFoundError) as e:
        Track(path=track_path)

    e.match(f"No such file or directory: '{track_path}/0.m4a'")


def test_track_requires_segment_transcript_file(track_path: Path) -> None:
    """
    The value of `current` in a track's metadata is an index
    that represents progress throughout that track's segments.
    It's expected that both audio and transcript files numbered
    with this index are present at the specified path.

    Expect that the segment transcript file exists and is readable.
    """
    (track_path / "0.txt").unlink()

    with pytest.raises(FileNotFoundError) as e:
        Track(path=track_path)

    e.match(f"No such file or directory: '{track_path}/0.txt'")


def test_track_should_load_and_iterate_through_segments(track_path: Path) -> None:
    """
    Expect that an instance of `Track` loads the segment
    at the current index, and expect that a track can
    iterate through segments up to and including the
    total, but not beyond it.
    """
    track = Track(path=track_path)

    assert track.metadata.current == 0
    assert track.metadata.current < track.metadata.total

    track.next_segment()

    assert track.metadata.current == 1
    assert track.metadata.current == track.metadata.total

    track.next_segment()

    assert track.metadata.current == 1
    assert track.metadata.current == track.metadata.total


def test_track_transcript_should_be_available(track_path: Path) -> None:
    track = Track(path=track_path)

    assert track.transcript() == "0"

    track.next_segment()

    assert track.transcript() == "1"
