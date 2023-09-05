from pathlib import Path
from typing import Any, NoReturn

import urwid as u  # type: ignore
from urwid import Divider, Filler, Frame, MainLoop, Pile, Text  # type: ignore

from podslicer.display import Row

HEADER_ROWS = [
    "<header>podslicer 🔪✨</header>",
    "",
    "<white>[a]</white> play (or stop) segment audio",
    "<white>[s]</white> show (or hide) segment transcript",
    "<white>[d]</white> next segment",
    "<white>[q]</white> quit",
]

TEXT_STYLES = [
    ("header", "bold,white", ""),
    ("white", "white", ""),
]


def input_handler(key_or_event: Any) -> NoReturn:
    raise u.ExitMainLoop()


def run(track_path: Path) -> None:
    if not track_path.is_dir():
        raise NotADirectoryError(f"Path to track cannot be found: {track_path}")

    header = Pile([Text(Row.parse(row)) for row in HEADER_ROWS])

    hint = Text("This is where a transcript would go.")
    progress = Text("0% complete (0 of 100)")
    body = Filler(Pile([Divider(), progress, Divider(), hint]), u.TOP)

    frame = Frame(body, header=header)

    loop = MainLoop(frame, TEXT_STYLES, unhandled_input=input_handler)
    loop.run()
