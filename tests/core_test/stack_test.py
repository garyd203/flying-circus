"""Tests for the Stack base class."""
from copy import copy

import pytest

from flyingcircus.core import AWS_Region
from flyingcircus.core import Output
from flyingcircus.core import Parameter
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.exceptions import StackMergeError
from .common import SimpleResource, LOREM_IPSUM
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

    # TODO #61 don't copy metadata/Description/etc.

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


class TestPrefixedNames:
    """Verify the object name prefixing functionality."""
    ATTRIBUTE_PARAMETRIZE_NAMES = 'stack_attribute,item'
    PREFIXABLE_ATTRIBUTE_EXAMPLES = [
        ("Parameters", Parameter(Type="String")),
        ("Resources", SimpleResource()),
        # TODO #87 Add Condition when we have a helper class
        # TODO #87 Add Mapping when we have a helper class
        # TODO #87 Add Metadata when we have a helper class. Consider whether we should retain the Metadata or just throw it away
    ]
    OUTPUT_EXAMPLES = [
        ("Outputs", Output(Value="HelloWorld")),
        ("Outputs", Output(Value="HelloWorld", Export={"Name": "SomeGloballyScopedValue"})),
    ]

    STACK_PREFIX = "NewScope"

    # Basic Prefixing Behaviour
    # -------------------------

    # FIXME empty prefix, non-string prefix, stupidly long prefix, prefix that is non-alpha-numeric, prefix that is not leading capital
    # fixme new stack is different from old stack, old stack is not modified

    # Prefixable Dictionaries
    # -----------------------

    @pytest.mark.parametrize(ATTRIBUTE_PARAMETRIZE_NAMES, PREFIXABLE_ATTRIBUTE_EXAMPLES)
    def test_item_is_prefixed_in_the_new_stack(self, stack_attribute, item):
        # Setup
        item_name = "SomeItemName"
        stack = Stack()
        stack[stack_attribute] = {item_name: item}

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        new_name = self.STACK_PREFIX + item_name

        assert len(new_stack[stack_attribute]) == 1
        assert item_name not in new_stack[stack_attribute]
        assert new_stack[stack_attribute][new_name] is item

    @pytest.mark.parametrize(ATTRIBUTE_PARAMETRIZE_NAMES, OUTPUT_EXAMPLES)
    def test_output_is_prefixed_in_the_new_stack_but_not_same_object(self, stack_attribute, item):
        # Setup
        item_name = "SomeItemName"
        stack = Stack()
        stack[stack_attribute] = {item_name: item}

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        new_name = self.STACK_PREFIX + item_name

        assert len(new_stack[stack_attribute]) == 1
        assert item_name not in new_stack[stack_attribute]

        new_item = new_stack[stack_attribute][new_name]
        assert new_item is not item
        assert getattr(new_item, "Description", None) == getattr(item, "Description", None)
        assert getattr(new_item, "Value", None) is getattr(item, "Value",
                                                           None), "This should be the same because it might be a Reference function or some such"

    @pytest.mark.parametrize(ATTRIBUTE_PARAMETRIZE_NAMES, PREFIXABLE_ATTRIBUTE_EXAMPLES + OUTPUT_EXAMPLES)
    def test_item_is_not_removed_from_original_stack(self, stack_attribute, item):
        # Setup
        item_name = "SomeItemName"
        stack = Stack()
        stack[stack_attribute] = {item_name: item}

        # Exercise
        _ = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert len(stack[stack_attribute]) == 1
        assert stack[stack_attribute][item_name] is item
        assert stack[stack_attribute][item_name] == item

    # Special Cases
    # -------------

    def test_copy_cfn_template_version(self):
        """AWSTemplateFormatVersion should be a string which we copy across unchanged"""
        # Setup
        version_string = "WhatIfThisWaSemanticallyVersioned.1.0"
        stack = Stack(AWSTemplateFormatVersion=version_string)

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert new_stack.AWSTemplateFormatVersion == version_string
        assert stack.AWSTemplateFormatVersion == version_string, "Old stack should not be modified"

    def test_copy_sam_version_in_transform(self):
        """If set, Transform should be the version of the Serverless Application Model
        being used, which we copy across unchanged.
        """
        # Setup
        version_string = "AWS::Serverless-1999-12-31"
        stack = Stack(Transform=version_string)

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert new_stack.Transform == version_string
        assert stack.Transform == version_string, "Old stack should not be modified"

    def test_modify_content_of_description(self):
        # Setup
        stack = Stack(Description=LOREM_IPSUM)

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert self.STACK_PREFIX in new_stack.Description
        assert LOREM_IPSUM in new_stack.Description
        assert stack.Description == LOREM_IPSUM, "Old stack should not be modified"

    def test_create_description_when_it_is_not_set(self):
        # Setup
        stack = Stack()

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert self.STACK_PREFIX == new_stack.Description
        assert not hasattr(stack, "Description") or stack.Description is None, "Old stack should not be modified"

    def test_prefix_export_name_for_output(self):
        # Setup
        name = "SomeItemName"
        export_name = "SomeGloballyScopedValue"
        output = Output(Value="HelloWorld", Export={"Name": export_name})
        stack = Stack(Outputs={name: output})

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert new_stack.Outputs[self.STACK_PREFIX + name]["Export"]["Name"] == self.STACK_PREFIX + export_name

    def test_dont_create_export_name_for_output_when_it_is_not_set(self):
        # Setup
        name = "SomeItemName"
        stack = Stack(Outputs={name: (Output(Value="HelloWorld"))})

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        new_output = new_stack.Outputs[self.STACK_PREFIX + name]
        assert getattr(new_output, "Export", None) is None
