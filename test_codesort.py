# unit tests (via pytest)
from unittest.mock import MagicMock
import sys

# TODO only mock networkit (as it is a lengthy install)
sys.modules["git"] = MagicMock()
sys.modules["networkit"] = MagicMock()
import codesort

del sys.modules["git"]
del sys.modules["networkit"]


def test_noop():
    assert True
