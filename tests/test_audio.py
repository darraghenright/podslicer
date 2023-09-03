from pathlib import Path
from uuid import uuid4

import pytest

from podslicer.audio import Audio, InvalidAudioFile


def test_path_is_required(track_path: Path) -> None:
    path = track_path / "0.m4a"

    with pytest.raises(TypeError) as e:
        Audio()  # type: ignore

    e.match("required positional argument: 'path'")

    assert Audio(path=path).path == path


def test_path_must_exist(tmp_path: Path) -> None:
    non_existent_file = tmp_path / uuid4().hex

    assert not non_existent_file.exists()

    with pytest.raises(FileNotFoundError) as e:
        Audio(path=non_existent_file)

    e.match(f"No such file or directory.")


def test_path_must_be_audio(tmp_path: Path) -> None:
    text_file = tmp_path / uuid4().hex
    text_file.write_text("123")

    assert text_file.is_file()

    with pytest.raises(InvalidAudioFile) as e:
        Audio(path=text_file)

    e.match(f"File {text_file} does not appear to be an audio file.")
