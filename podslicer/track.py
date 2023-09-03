import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

METADATA_FILE = "metadata.json"


@dataclass
class Metadata:
    current: int
    extension: str
    path: Path
    total: int

    @classmethod
    def from_path(cls: type[Self], path: Path) -> Self:
        file = path / METADATA_FILE
        text = file.read_text()

        return cls(**json.loads(text) | dict(path=path))

    def audio(self) -> Path:
        return Path(str(self.current)).with_suffix(self.extension)

    def increment(self) -> None:
        if self.current < self.total:
            self.current += 1
        else:
            raise IndexError("Reached the last segment.")

    def json(self) -> str:
        return json.dumps({k: v for (k, v) in vars(self).items() if k != "path"})

    def progress(self) -> float:
        return round(self.current / self.total * 100, ndigits=1)

    def transcript(self) -> Path:
        return Path(str(self.current)).with_suffix(".txt")


class Track:
    def __init__(self, path: Path) -> None:
        self.metadata = Metadata.from_path(path)
        self.path = path
        self.load_segment()

    def load_segment(self) -> None:
        self._audio = self.path / self.metadata.audio()
        self._transcript = self.path / self.metadata.transcript()
        self._audio.stat()
        self._transcript.stat()

    def next_segment(self) -> None:
        self.metadata.increment()
        self.load_segment()

    def transcript(self) -> str:
        return self._transcript.read_text()
