from pathlib import Path
from subprocess import DEVNULL, CalledProcessError, Popen, run
from threading import Thread
from time import sleep


class InvalidAudioFile(RuntimeError):
    """
    Raised when a file is not recognised
    as an audio file or does not exist.
    """


class AudioFile:
    """
    A validated filepath to an audio file.
    """

    def __init__(self, filepath: Path) -> None:
        self._validate(filepath)
        self.filepath = filepath

    def _validate(self, filepath: Path) -> None:
        """
        Check that the filepath is recognised as
        an audio file. Any non-zero return code
        raises a `CalledProcessError` which means
        the file is probably not audio.
        """
        try:
            run(["afinfo", filepath], check=True, stdout=DEVNULL)
        except CalledProcessError:
            raise InvalidAudioFile(
                f"File {filepath} does not appear to be an audio file."
            )


class Segment:
    def __init__(self, audio_file: AudioFile) -> None:
        """
        Create a new `Segment` instance.
        """
        self.audio_file = audio_file
        self.playing = False

    def playback(self) -> None:
        """
        Play an audio segment or flag it as stopped.
        """
        if self.playing:
            self.playing = False
        else:
            Thread(target=self._play_audio_file, daemon=True).start()

    def _play_audio_file(self) -> None:
        """
        Play segment, poll for status and stop if required.
        """
        self.playing = True

        with Popen(["afplay", self.audio_file.filepath]) as process:
            while process.poll() is None:
                if not self.playing:
                    process.kill()
                sleep(0.2)

        self.playing = False
