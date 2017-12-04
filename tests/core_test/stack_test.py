"""Tests for the Stack base class."""
import pytest

from core_test.common import ZeroAttributeObject
from flyingcircus.core import Stack


class TestBasicStackBehaviour:
    """Verify basic behaviour of the Stack class"""

    def test_template_version_defaults_to_2010(self):
        stack = Stack()

        assert stack.AWSTemplateFormatVersion == "2010-09-09"


class TestGetLogicalName:
    """Verify reverse lookup of a resource's logical name"""

    def test_find_a_parameter(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = ZeroAttributeObject()
        stack.Parameters[name] = data

        # Exercise & Verify
        assert stack.get_logical_name(data) == name

    def test_find_a_resource(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = ZeroAttributeObject()
        stack.Resources[name] = data

        # Exercise & Verify
        assert stack.get_logical_name(data) == name

    def test_find_a_resource_which_is_a_plain_dict(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = dict()
        stack.Resources[name] = data

        # Exercise & Verify
        assert stack.get_logical_name(data) == name

    def test_only_search_parameters_and_resources(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = ZeroAttributeObject()
        for attribute_name in ["Mappings", "Conditions", "Transform", "Outputs"]:
            stack[attribute_name][name] = data

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data)

        assert "not part of this stack" in str(excinfo.value)

    def test_fail_if_object_doesnt_exist(self):
        # Setup
        stack = Stack()
        data = ZeroAttributeObject()

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data)

        assert "not part of this stack" in str(excinfo.value)

    def test_fail_if_object_doesnt_exist_except_in_another_stack(self):
        # Setup
        name = "Foo"
        stack = Stack()
        stack2 = Stack()
        data = ZeroAttributeObject()
        stack2.Resources[name] = data

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data)

        assert "not part of this stack" in str(excinfo.value)

    def test_fail_if_object_is_duplicated(self):
        # Setup
        name1 = "Foo"
        name2 = "Bar"
        stack = Stack()
        data = ZeroAttributeObject()

        stack.Parameters[name1] = data
        stack.Parameters[name2] = data

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data)

        assert "multiple names" in str(excinfo.value)
