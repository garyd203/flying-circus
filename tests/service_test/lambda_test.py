"""Tests for Lambda functionality."""

import sys
from contextlib import contextmanager
from textwrap import dedent
from unittest.mock import patch

import pytest

from flyingcircus.service.lambda_ import Function
from flyingcircus.service.lambda_ import get_lambda_runtime_for_this_process


def fake_python_func(event, context):
    """Used for testing create_from_python_function()"""
    return "Hello world"


class TestCreateFromPythonFunction:
    """Tests for Function.create_from_python_function()"""

    def _clean_python_code(self, code: str) -> str:
        """Produce a slightly standardised version of some python code"""
        return dedent(code).strip()

    def test_should_create_resource_with_supplied_properties(self):
        # Setup
        def some_python_func():
            return "Hello world"

        func_name = "some_python_func"
        func_code = """
        def some_python_func():
            return "Hello world"
        """

        role = "arn::some:role"
        description = "some description"
        runtime_name = "python3.6"

        # Exercise
        func_resource = Function.create_from_python_function(
            some_python_func, role, description, runtime_name
        )

        # Verify
        assert isinstance(func_resource, Function)
        assert self._clean_python_code(
            func_resource.Properties.Code["ZipFile"]
        ) == self._clean_python_code(func_code)
        assert func_resource.Properties.Description == description
        assert func_resource.Properties.Handler.startswith("index.")
        assert func_resource.Properties.Handler[6:] == func_name
        assert func_resource.Properties.Role == role
        assert func_resource.Properties.Runtime == runtime_name

    def test_should_calculate_runtime_from_system_if_not_supplied(self):
        runtime_name = "python2.7"

        # Exercise
        with patch(
            "flyingcircus.service.lambda_.get_lambda_runtime_for_this_process",
            return_value=runtime_name,
        ):
            func_resource = Function.create_from_python_function(
                fake_python_func, "rolename"
            )

        # Verify
        assert func_resource.Properties.Runtime == runtime_name

    def test_should_generate_description_from_python_function_if_not_supplied(self):
        # Setup
        def some_python_func():
            """This is a docstring"""
            return "Hello world"

        # Exercise
        func_resource = Function.create_from_python_function(some_python_func, "role")

        # Verify
        assert func_resource.Properties.Description == "This is a docstring"

    def test_should_flatten_multi_line_docstring_in_description(self):
        # Setup
        def some_python_func():
            """This is a docstring that
            has a long introductory sentence.
            """
            return "Hello world"

        # Exercise
        func_resource = Function.create_from_python_function(some_python_func, "role")

        # Verify
        assert (
            func_resource.Properties.Description
            == "This is a docstring that has a long introductory sentence."
        )

    def test_should_ignore_secondary_paragraphs_from_docstring_in_description(self):
        def some_python_func():
            """
            This sentence describes the
            function.

            This later paragraph is not important at
            all...

            Neither is this one"""
            return "Hello world"

        # Exercise
        func_resource = Function.create_from_python_function(some_python_func, "role")

        # Verify
        assert (
            func_resource.Properties.Description
            == "This sentence describes the function."
        )

    def test_should_use_humanised_function_name_in_description_when_no_docstring(self):
        # Setup
        def some_python_func():
            return "Hello world"

        # Exercise
        func_resource = Function.create_from_python_function(some_python_func, "role")

        # Verify
        assert func_resource.Properties.Description == "Some python func."

    def test_handler_function_should_raise_error_for_too_many_parameters(self):
        # Setup function
        def some_python_func(event, context, unexpected_param):
            return "Hello world"

        # Exercise & Verify
        with pytest.raises(ValueError, match="too many parameters"):
            _ = Function.create_from_python_function(some_python_func, "role")

    def test_handler_function_should_show_warning_for_unusually_named_parameters(self):
        # Setup function
        def some_python_func(weird_parameter_one, weird_parameter_two):
            return "Hello world"

        # Exercise & Verify
        with pytest.warns(
            UserWarning, match="parameter.*name.*weird_parameter_(one|two)"
        ):
            _ = Function.create_from_python_function(some_python_func, "role")


class TestGetLambdaRuntime:
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

    @pytest.mark.parametrize(("major", "minor"), [(3, 9)])
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
