"""Tests for the hypothesis-asn1 library."""

import pytest

from hypothesis_asn1 import from_asn1


def test_not_implemented_yet():
    with pytest.raises(NotImplementedError):
        from_asn1(None)
