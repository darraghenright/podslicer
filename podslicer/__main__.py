from urwid import TOP, Divider, Filler, Frame, MainLoop, Pile, Text  # type: ignore

from podslicer.display import Row

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
body = Filler(Pile([Divider(), hint]), TOP)

frame = Frame(body, header=header)

loop = MainLoop(frame, styles)
loop.run()
