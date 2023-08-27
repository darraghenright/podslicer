from pathlib import Path
from uuid import uuid4

import pytest

from podslicer.audio import AudioFile, InvalidAudioFile


def test_filepath_is_required(valid_filepath: Path) -> None:
    with pytest.raises(TypeError):
        AudioFile()  # type: ignore

    assert AudioFile(filepath=valid_filepath).filepath == valid_filepath


def test_filepath_must_exist(tmp_path: Path) -> None:
    non_existent_file = tmp_path / uuid4().hex

    assert not non_existent_file.exists()

    with pytest.raises(InvalidAudioFile) as e:
        AudioFile(filepath=non_existent_file)

    e.match(f"File {non_existent_file} does not appear to be an audio file.")


def test_filepath_must_be_audio(tmp_path: Path) -> None:
    text_file = tmp_path / uuid4().hex
    text_file.write_text("123")

    assert text_file.is_file()

    with pytest.raises(InvalidAudioFile) as e:
        AudioFile(filepath=text_file)

    e.match(f"File {text_file} does not appear to be an audio file.")
