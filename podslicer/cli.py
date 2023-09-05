from pathlib import Path

import urwid as u  # type: ignore

from podslicer.control import InputController, InputHandler
from podslicer.display import HEADER_ROWS, TEXT_STYLES, Display
from podslicer.track import Track


def run(track_path: Path) -> None:
    if not track_path.is_dir():
        raise NotADirectoryError(f"Path to track cannot be found: {track_path}")

    display = Display(HEADER_ROWS)
    track = Track(track_path)
    input_handler = InputHandler(InputController(display, track))
    loop = u.MainLoop(display.layout(), TEXT_STYLES, unhandled_input=input_handler)

    loop.run()
