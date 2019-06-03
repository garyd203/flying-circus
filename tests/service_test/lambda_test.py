"""Tests for Lambda functionality."""

import sys
from contextlib import contextmanager
from unittest.mock import patch

import pytest

from flyingcircus.service.lambda_ import get_lambda_runtime_for_this_process


class TestGetLambdaRuntime(object):
    """Tests for get_lambda_runtime_for_this_process."""

    @contextmanager
    def _mock_python_version(self, major: int, minor: int):
        fake_version_info = (major, minor, 0, "fake-rc", 0)
        fake_version = "{}.{}.0-mocked".format(major, minor)
        with patch.multiple(sys, version=fake_version, version_info=fake_version_info):
            yield

    def test_current_system_should_be_supported(self):
        """Every Python version that flying-circus can run on should be supported."""
        version = get_lambda_runtime_for_this_process()
        assert len(version) > 0

    @pytest.mark.parametrize(
        ("major", "minor"), [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)]
    )
    def test_older_version3_systems_should_be_upgraded_to_36(self, major, minor):
        with self._mock_python_version(major, minor):
            version = get_lambda_runtime_for_this_process()
        assert version == "python3.6"

    @pytest.mark.parametrize(("major", "minor"), [(3, 8)])
    def test_newer_version3_systems_should_raise_error(self, major, minor):
        with self._mock_python_version(major, minor):
            with pytest.raises(ValueError, match="version '3"):
                _ = get_lambda_runtime_for_this_process()

    @pytest.mark.parametrize(
        ("major", "minor"), [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]
    )
    def test_older_version2_systems_should_be_upgraded_to_27(self, major, minor):
        with self._mock_python_version(major, minor):
            version = get_lambda_runtime_for_this_process()
        assert version == "python2.7"

    def test_unsupported_version_should_raise_error(self):
        with self._mock_python_version(4, 0):
            with pytest.raises(ValueError, match="version '4.0"):
                _ = get_lambda_runtime_for_this_process()
