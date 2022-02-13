import pytest

from summary import Summarizer

@pytest.mark.skip(reason="Not implimented.")
def test_extant():
    empty = Summarizer()
    assert empty is not None

