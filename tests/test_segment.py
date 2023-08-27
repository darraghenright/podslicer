from pathlib import Path

from podslicer.audio import AudioFile, Segment


def test_audio_file_is_required(valid_filepath: Path) -> None:
    audio_file = AudioFile(filepath=valid_filepath)
    segment = Segment(audio_file=audio_file)

    assert segment.audio_file == audio_file


def test_playback_can_be_toggled(valid_filepath: Path) -> None:
    segment = Segment(audio_file=AudioFile(filepath=valid_filepath))

    assert not segment.playing
    segment.playback()
    assert segment.playing
    segment.playback()
    assert not segment.playing
