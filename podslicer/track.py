import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from podslicer.audio import Audio

METADATA_FILE = "metadata.json"


@dataclass
class Metadata:
    current: int
    extension: str
    path: Path
    total: int

    @classmethod
    def from_path(cls: type[Self], path: Path) -> Self:
        """
        Build an instance of metadata from JSON
        encoded metadata state read from disc.
        """
        file = path / METADATA_FILE
        text = file.read_text()

        return cls(**json.loads(text) | dict(path=path))

    def audio(self) -> Path:
        """
        Return the path to the audio file.
        """
        return (self.path / str(self.current)).with_suffix(self.extension)

    def increment(self) -> None:
        """
        Increment the current index and save metadata.
        """
        if self.current < self.total:
            self.current += 1
            self.save()

    def decrement(self) -> None:
        """
        Decrement the current index and save metadata.
        """
        if self.current > 0:
            self.current -= 1
            self.save()

    def json(self) -> str:
        """
        JSON encode required subset of metadata state.
        """
        return json.dumps({k: v for (k, v) in vars(self).items() if k != "path"})

    def progress(self) -> float:
        """
        Return current progress as a percentage.
        """
        return round(self.current / self.total * 100, ndigits=1)

    def save(self) -> None:
        """
        Save JSON encoded metadata to the metadata file.
        """
        (self.path / METADATA_FILE).write_text(self.json())

    def transcript(self) -> Path:
        """
        Return the path to the transcript file.
        """
        return (self.path / str(self.current)).with_suffix(".txt")


class Track:
    def __init__(self, path: Path) -> None:
        """
        Create an instance of `Track`.
        """
        self.metadata = Metadata.from_path(path)
        self.load_segment()

    def load_segment(self) -> None:
        """
        Load the current segment.
        """
        self._audio = Audio(self.metadata.audio())
        self._transcript = self.metadata.transcript().read_text()

    def next_segment(self) -> None:
        """
        Attempt to load the next segment.
        An `IndexError` is raised if the
        current index exceeds the total.
        """
        self.metadata.increment()
        self.load_segment()

    def playback(self) -> None:
        self._audio.playback()

    def previous_segment(self) -> None:
        self.metadata.decrement()
        self.load_segment()

    def transcript(self) -> str:
        """
        Return the transcript text.
        """
        return self._transcript
