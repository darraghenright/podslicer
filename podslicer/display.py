from html.parser import HTMLParser
from typing import Optional, Self, Union

from urwid import TOP, Divider, Filler, Frame, Pile, Text  # type: ignore

ParsedRow = Union[str, tuple[str, str]]


HEADER_ROWS = [
    "<header>podslicer 🔪✨</header>",
    "",
    "<white>[a]</white> play (or stop) segment audio",
    "<white>[s]</white> toggle segment transcript",
    "<white>[←]</white> previous segment",
    "<white>[→]</white> next segment",
    "<white>[q]</white> quit",
]

TEXT_STYLES = [
    ("header", "bold,white", ""),
    ("white", "white", ""),
]


class Display:
    def __init__(self, header_rows: Optional[list[str]] = None) -> None:
        self.header_rows = header_rows if header_rows else []
        self.hint = Text("")
        self.progress = Text("")
        self._show_hint = False

        # TODO update progress here

    def layout(self) -> Frame:
        div = Divider()
        body = Filler(Pile([div, self.progress, div, self.hint]), TOP)
        header = Pile([Text(Row.parse(row)) for row in self.header_rows])

        return Frame(body, header=header)

    def hide_hint(self) -> None:
        self._show_hint = False
        self.hint.set_text("")  # type: ignore

    def toggle_hint(self, text: str) -> None:
        self._show_hint = not self._show_hint
        self.hint.set_text(text if self._show_hint else "")  # type: ignore

    def update_progress(self, percent: float, current: int, total: int) -> None:
        progress = Row.parse(
            f"<white>{percent}%</white> complete ({current} of {total})"
        )
        self.progress.set_text(progress)  # type: ignore


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
