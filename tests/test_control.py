from unittest.mock import MagicMock

import pytest
from urwid import ExitMainLoop  # type: ignore

from podslicer.control import InputController, InputHandler


def test_input_handler_requires_controller() -> None:
    with pytest.raises(TypeError) as e:
        InputHandler()  # type: ignore

    e.match("missing 1 required positional argument: 'controller'")


def test_input_handler_should_handle_playback_input() -> None:
    controller_mock = MagicMock()
    input_handler = InputHandler(controller_mock)

    for key in ("a", "A"):
        input_handler(key)
        controller_mock.playback.assert_called_once()  # type: ignore
        controller_mock.reset_mock()


def test_input_handler_should_handle_transcript_input() -> None:
    controller_mock = MagicMock()
    input_handler = InputHandler(controller_mock)

    for key in ("s", "S"):
        input_handler(key)
        controller_mock.transcript.assert_called_once()  # type: ignore
        controller_mock.reset_mock()


def test_input_handler_should_handle_back_input() -> None:
    controller_mock = MagicMock()
    input_handler = InputHandler(controller_mock)

    input_handler("left")
    controller_mock.back.assert_called_once()  # type: ignore


def test_input_handler_should_handle_forward_input() -> None:
    controller_mock = MagicMock()
    input_handler = InputHandler(controller_mock)

    input_handler("right")
    controller_mock.forward.assert_called_once()  # type: ignore


def test_input_handler_should_handle_quit() -> None:
    input_handler = InputHandler(MagicMock())

    for key in ("q", "Q"):
        with pytest.raises(ExitMainLoop):
            input_handler(key)


def test_input_handler_should_silently_ignore_other_inputs() -> None:
    input_handler = InputHandler(MagicMock())
    input_handler("XYZ")
    input_handler([])
    input_handler(None)


def test_input_controller_requires_display_and_track() -> None:
    with pytest.raises(TypeError) as e:
        InputController()  # type: ignore

    e.match("missing 2 required positional arguments: 'display' and 'track'")


def test_input_controller_should_back() -> None:
    ...


def test_input_controller_should_forward() -> None:
    ...


def test_input_controller_should_playback() -> None:
    ...


def test_input_controller_should_transcript() -> None:
    ...
