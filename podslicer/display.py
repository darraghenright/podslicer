from html.parser import HTMLParser
from typing import Optional, Self, Union

ParsedRow = Union[str, tuple[str, str]]


class Row(HTMLParser):
    """
    Parse `text` into a list of tokens
    that represent the row as a list of
    text or tuples of style and text.
    """

    @classmethod
    def parse(cls: type[Self], text: str) -> list[ParsedRow]:
        return cls(text).parsed_rows or [text]

    def __init__(self, text: str) -> None:
        super().__init__()

        self.open_tag: Optional[str] = None
        self.parsed_rows: list[ParsedRow] = []

        self.feed(text)

    def handle_data(self, data: str) -> None:
        self.parsed_rows.append((self.open_tag, data) if self.open_tag else data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.open_tag:
            raise ValueError("Nested tags are not allowed.")

        self.open_tag = tag

    def handle_endtag(self, tag: str) -> None:
        self.open_tag = None
