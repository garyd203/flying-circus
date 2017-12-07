"""Tests for the Stack base class."""

import pytest

from core_test.common import SingleAttributeObject
from core_test.common import ZeroAttributeObject
from flyingcircus.core import AWS_Region
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

    def test_find_a_pseudo_parameter(self):
        # Setup
        data = AWS_Region
        stack = Stack()

        # Exercise & Verify
        assert stack.get_logical_name(data) == "AWS::Region"

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


class _ObjectThatReferencesStack(SingleAttributeObject):
    """Test object that verifies it has the correct stack when exported"""

    def __init__(self, containing_stack):
        SingleAttributeObject.__init__(self, one="foo")
        self._expected_stack = containing_stack

    def as_yaml_node(self, dumper):
        assert dumper.cfn_stack is self._expected_stack
        return super().as_yaml_node(dumper)


class TestCurrentStack:
    """Verify that the current stack object is set correctly when exporting."""

    def _create_stack_that_checks_reference(self):
        stack = Stack()
        data = _ObjectThatReferencesStack(stack)
        stack.Resources["Data"] = data
        return stack

    def test_current_stack_is_available_to_attributes(self):
        # Setup
        stack = self._create_stack_that_checks_reference()

        # Exercise
        stack.export("yaml")  # Should not throw error

    def test_correct_stack_is_available_when_multiple_stacks_have_been_exported(self):
        # Setup
        stack1 = self._create_stack_that_checks_reference()
        stack2 = self._create_stack_that_checks_reference()

        stack1.export("yaml")

        # Exercise
        stack2.export("yaml")  # Should not throw error
