from typing import NoReturn

import urwid as u  # type: ignore
from urwid import Divider, Filler, Frame, MainLoop, Pile, Text  # type: ignore

from podslicer.display import Row


def exit_on_input(key: str) -> NoReturn:
    raise u.ExitMainLoop()


header_rows = [
    "<header>podslicer 🔪✨</header>",
    "",
    "<white>[a]</white> play (or stop) segment audio",
    "<white>[s]</white> show (or hide) segment transcript",
    "<white>[d]</white> next segment",
    "<white>[q]</white> quit",
]

styles = [
    ("header", "bold,white", ""),
    ("white", "white", ""),
]

header = Pile([Text(Row.parse(row)) for row in header_rows])

hint = Text("")
body = Filler(Pile([Divider(), hint]), u.TOP)

frame = Frame(body, header=header)

loop = MainLoop(frame, styles, unhandled_input=exit_on_input)
loop.run()
