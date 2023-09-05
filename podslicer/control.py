from typing import Any

from urwid import ExitMainLoop  # type: ignore

from podslicer.display import Display
from podslicer.track import Track


class InputController:
    def __init__(self, display: Display, track: Track) -> None:
        self.display = display
        self.track = track

    def back(self) -> None:
        self.track.previous_segment()
    def forward(self) -> None:
        self.track.next_segment()

    def playback(self) -> None:
        self.track.playback()

    def transcript(self) -> None:
        pass


class InputHandler:
    def __init__(self, controller: InputController) -> None:
        self.controller = controller

    def __call__(self, key_or_event: Any) -> None:
        match key_or_event:
            case "a" | "A":
                self.controller.playback()
            case "left":
                self.controller.back()
            case "right":
                self.controller.forward()
            case "q" | "Q":
                raise ExitMainLoop()
            case "s" | "S":
                self.controller.transcript()
            case _:
                pass
