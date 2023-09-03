from pathlib import Path
from subprocess import DEVNULL, CalledProcessError, Popen, run
from threading import Thread
from time import sleep


class InvalidAudioFile(RuntimeError):
    """
    Raised when a file is not recognised
    as an audio file or does not exist.
    """


class Audio:
    def __init__(self, path: Path) -> None:
        self.playing = False
        self._validate(path)
        self.path = path

    def _validate(self, path: Path) -> None:
        """
        Check that the `path` exists, is readable and
        is recognised as an audio file. Any non-zero
        return code raises a `CalledProcessError` which
        means the file is probably not audio.
        """
        path.stat()

        try:
            run(["afinfo", path], check=True, stdout=DEVNULL)
        except CalledProcessError:
            raise InvalidAudioFile(f"File {path} does not appear to be an audio file.")

    def playback(self) -> None:
        """
        Play audio file or flag it as stopped.
        """
        if self.playing:
            self.playing = False
        else:
            Thread(target=self._play_audio_file, daemon=True).start()

    def _play_audio_file(self) -> None:
        """
        Play audio file, poll for status and stop if required.
        """
        self.playing = True

        with Popen(["afplay", self.path]) as process:
            while process.poll() is None:
                if not self.playing:
                    process.kill()
                sleep(0.2)

        self.playing = False
