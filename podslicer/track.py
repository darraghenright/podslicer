import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

METADATA_FILE = "metadata.json"


@dataclass
class Metadata:
    current: int
    extension: str
    total: int

    @classmethod
    def from_path(cls: type[Self], path: Path) -> Self:
        file = path / METADATA_FILE
        text = file.read_text()

        return cls(**json.loads(text))

    def json(self) -> str:
        return json.dumps(vars(self))

    def progress(self) -> float:
        percentage = self.current / self.total * 100

        return round(percentage, 1)


class Segment:
    def __init__(self, audio: Path, transcript: Path) -> None:
        audio.stat()
        transcript.stat()

        self.audio = audio
        self.transcript = transcript.read_text()


class Track:
    def __init__(self, path: Path) -> None:
        self.metadata = Metadata.from_path(path)
        self.path = path
        self._load_segment()

    def _audio_file(self) -> Path:
        current = str(self.metadata.current)
        extension = self.metadata.extension

        return self.path / Path(current).with_suffix(extension)

    def _transcript_file(self) -> Path:
        current = str(self.metadata.current)
        extension = ".txt"

        return self.path / Path(current).with_suffix(extension)

    def _load_segment(self) -> None:
        self.segment = Segment(self._audio_file(), self._transcript_file())

    def next_segment(self) -> None:
        # this could go into metadata. internal state integrity/
        if (self.metadata.current + 1) > self.metadata.total:
            raise IndexError()
        self.metadata.current += 1

        self._load_segment()
