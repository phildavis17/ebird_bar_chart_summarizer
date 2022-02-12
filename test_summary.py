import pytest

from summary import Summarizer

def test_extant():
    empty = Summarizer()
    assert empty is not None

