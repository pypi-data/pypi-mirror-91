"""A Hypothesis extension for ASN.1 records.

The only public API is `from_asn1`; check the docstring for details.
"""

import pyasn1
from hypothesis import strategies as st

__version__ = "0.0.1"
__all__ = ["from_template"]


def from_asn1(record: object) -> st.SearchStrategy[object]:
    """Parse the given ASN.1 record into a strategy."""
    assert pyasn1 is not None
    raise NotImplementedError
