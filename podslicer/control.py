from typing import Any


class InputController:
    def back(self):
        ...

    def forward(self):
        ...

    def playback(self):
        ...

    def transcript(self):
        ...


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
            case "s" | "S":
                self.controller.transcript()
            case _:
                pass
