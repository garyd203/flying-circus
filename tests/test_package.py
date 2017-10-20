"""Tests for the package itself"""

import semver

import flyingcircus


def test_has_version_attribute():
    assert hasattr(flyingcircus, "__version__")
    assert isinstance(flyingcircus.__version__, str)
    _ = semver.parse(flyingcircus.__version__)  # Should not raise ValueError
