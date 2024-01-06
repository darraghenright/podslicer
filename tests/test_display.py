import pytest

from podslicer.display import Display, ParsedRow, Row

ROW_FIXTURES = [
    pytest.param(
        "",
        [""],
        id="blank",
    ),
    pytest.param(
        "untagged text",
        ["untagged text"],
        id="untagged",
    ),
    pytest.param(
        "<white>tagged text</white>",
        [("white", "tagged text")],
        id="tagged",
    ),
    pytest.param(
        "<WHITE>uppercase text</WHITE>",
        [("white", "uppercase text")],
        id="uppercase",
    ),
    pytest.param(
        "<bold>bold text</bold> untagged text",
        [("bold", "bold text"), " untagged text"],
        id="tagged_and_untagged",
    ),
    pytest.param(
        "<bold>bold text</bold> untagged text <white>white text</white>",
        [("bold", "bold text"), " untagged text ", ("white", "white text")],
        id="multiple_tags",
    ),
]


@pytest.mark.parametrize("row,expected", ROW_FIXTURES)
def test_row_should_be_parsed(row: str, expected: ParsedRow) -> None:
    assert Row.parse(row) == expected


def test_nested_tags_should_raise_an_exception() -> None:
    row = "<outer><inner>nested text</inner></inner>"

    with pytest.raises(ValueError) as e:
        Row.parse(row)

    e.match("Nested tags are not allowed.")


def test_display() -> None:
    Display()


def test_hide_hint() -> None:
    ...


# self.display.hide_hint()
# self.display.show_hint()
# self.display.update_progress(1, 100)
# self.display.toggle_hint(self.track.transcript())
