from pathlib import Path
from uuid import uuid4

import pytest

from audio import AudioFile, InvalidAudioFile, Segment

FILEPATH = Path("test.m4a")


def test_audio_file_requires_filepath() -> None:
    """
    A newly created `AudioFile` requires a `filepath` property.
    """
    audio_file = AudioFile(filepath=FILEPATH)

    assert audio_file.filepath == FILEPATH


def test_audio_file_requires_filepath_to_exist(tmp_path: Path) -> None:
    """
    Raise an exception if a newly created `AudioFile`
    receives a `filepath` that does not exist.
    """
    filepath = tmp_path / uuid4().hex

    assert not filepath.exists()

    with pytest.raises(InvalidAudioFile) as e:
        AudioFile(filepath=filepath)

    e.match(f"File {filepath} does not appear to be an audio file.")


def test_audio_file_requires_filepath_to_be_audio(tmp_path: Path) -> None:
    """
    Raise an exception if a newly created `AudioFile`
    does not recognise the `filepath` as audio.
    """
    filepath = tmp_path / uuid4().hex
    filepath.write_text("123")

    assert filepath.is_file()

    with pytest.raises(InvalidAudioFile) as e:
        AudioFile(filepath=filepath)

    e.match(f"File {filepath} does not appear to be an audio file.")


def test_segment_requires_audio_file() -> None:
    """
    A newly created `Segment` requires an `audio_file` property.
    """
    audio_file = AudioFile(filepath=FILEPATH)
    segment = Segment(audio_file=audio_file)

    assert segment.audio_file == audio_file


def test_segment_should_toggle_playback() -> None:
    """
    A `Segment` should be able to toggle playback repeatedly.
    """
    audio_file = AudioFile(filepath=FILEPATH)
    segment = Segment(audio_file=audio_file)

    assert not segment.playing
    segment.playback()
    assert segment.playing
    segment.playback()
    assert not segment.playing
