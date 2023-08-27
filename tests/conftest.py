from pathlib import Path

import pytest


@pytest.fixture()
def valid_filepath() -> Path:
    return Path(__file__).parent / "test.m4a"
