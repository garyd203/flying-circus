"""Tests for the Stack base class."""
from copy import copy

import pytest

from flyingcircus.core import AWS_Region
from flyingcircus.core import Output
from flyingcircus.core import Parameter
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.exceptions import StackMergeError
from .common import SimpleResource
from .common import SingleAttributeObject
from .common import ZeroAttributeObject


class TestBasicStackBehaviour:
    """Verify basic behaviour of the Stack class"""

    def test_export_basic_stack(self):
        """Should be able to create and export a simple stack example."""
        stack = Stack()
        stack.Resources["SomeName"] = SimpleResource()
        output = stack.export("yaml")

        assert output == dedent("""
        ---
        AWSTemplateFormatVersion: '2010-09-09'
        Resources:
          SomeName:
            Type: NameSpace::Service::Resource
        """)

    def test_template_version_defaults_to_2010(self):
        stack = Stack()

        assert stack.AWSTemplateFormatVersion == "2010-09-09"


class TestGetLogicalName:
    """Verify reverse lookup of a resource's logical name"""

    def test_find_a_parameter(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = Parameter(Type="String")
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
            setattr(stack, attribute_name, {name: data})

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
        data = Parameter(Type="String")

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


class TestMergeStack:
    """Verify the stack merge functionality."""
    PARAMETRIZE_NAMES = 'stack_attribute,item'
    MERGED_ATTRIBUTE_EXAMPLES = [
        ("Outputs", Output(Value="HelloWorld")),
        ("Parameters", Parameter(Type="String")),
        ("Resources", SimpleResource()),
    ]

    def test_merge_returns_target_stack(self):
        # Setup
        source = Stack(Resources={"SomeResource": SimpleResource()})
        target = Stack()

        # Exercise
        result = target.merge_stack(source)

        # Verify
        assert target is result

    @pytest.mark.parametrize(PARAMETRIZE_NAMES, MERGED_ATTRIBUTE_EXAMPLES)
    def test_item_is_added_to_the_target_stack(self, stack_attribute, item):
        # Setup
        item_name = "SomeChildProperty"
        source = Stack()
        source[stack_attribute] = {item_name: item}
        target = Stack()

        # Exercise
        target.merge_stack(source)

        # Verify
        assert len(target[stack_attribute]) == 1
        assert target[stack_attribute][item_name] is item

    @pytest.mark.parametrize(PARAMETRIZE_NAMES, MERGED_ATTRIBUTE_EXAMPLES)
    def test_item_is_not_removed_from_source_stack(self, stack_attribute, item):
        # Setup
        item_name = "SomeChildProperty"
        source = Stack()
        source[stack_attribute] = {item_name: item}
        target = Stack()

        # Exercise
        target.merge_stack(source)

        # Verify
        assert len(source[stack_attribute]) == 1
        assert source[stack_attribute][item_name] is item

    @pytest.mark.parametrize(PARAMETRIZE_NAMES, MERGED_ATTRIBUTE_EXAMPLES)
    def test_does_not_clobber_existing_items_in_target_stack(self, stack_attribute, item):
        # Setup
        item_name = "SomeChildProperty"
        source = Stack()
        source[stack_attribute] = {item_name: item}

        existing_item = copy(item)
        existing_item_name = "SomeOldItem"
        target = Stack()
        target[stack_attribute] = {existing_item_name: existing_item}

        # Exercise
        target.merge_stack(source)

        # Verify
        assert len(target[stack_attribute]) == 2
        assert target[stack_attribute][item_name] is item
        assert target[stack_attribute][existing_item_name] is existing_item

    @pytest.mark.parametrize(PARAMETRIZE_NAMES, MERGED_ATTRIBUTE_EXAMPLES)
    def test_cannot_merge_if_logical_name_is_already_used_for_that_item_type(self, stack_attribute, item):
        # Setup
        item_name = "SomeChildProperty"
        source = Stack()
        source[stack_attribute] = {item_name: item}

        existing_item = copy(item)
        target = Stack()
        target[stack_attribute] = {item_name: existing_item}

        # Exercise & Verify
        with pytest.raises(StackMergeError) as excinfo:
            target.merge_stack(source)

        assert "in this stack already has an item with the logical name" in str(excinfo.value)

    def test_cannot_merge_if_two_outputs_have_the_same_export_name(self):
        # Setup
        export_name = "SpecialExportedValue"

        source_output = Output(Value=123, Export={"Name": export_name})
        source = Stack(Outputs={"SourceOutput": source_output})

        target_output = Output(Value=987, Export={"Name": export_name})
        target = Stack(Outputs={"TargetOutput": target_output})

        # Exercise & Verify
        with pytest.raises(StackMergeError) as excinfo:
            target.merge_stack(source)

        assert "the target stack already has exports" in str(excinfo.value).lower()
