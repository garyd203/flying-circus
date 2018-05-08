"""Tests for the Stack base class."""
import re
from copy import copy

import hypothesis.strategies as st
import pytest
from hypothesis import given

from flyingcircus.core import AWSObject
from flyingcircus.core import AWS_Region
from flyingcircus.core import Output
from flyingcircus.core import Parameter
from flyingcircus.core import Resource
from flyingcircus.core import ResourceProperties
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.exceptions import StackMergeError
from .common import BaseTaggingTest
from .common import LOREM_IPSUM
from .common import SimpleResource
from .common import SingleAttributeObject
from .common import ZeroAttributeObject
from .common import aws_logical_name_strategy
from .common import parametrize_tagging_techniques


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

    def test_find_a_resource_when_only_searching_resources(self):
        # Setup
        name = "Foo"
        stack = Stack()
        data = ZeroAttributeObject()
        stack.Resources[name] = data

        # Exercise & Verify
        assert stack.get_logical_name(data, resources_only=True) == name

    @pytest.mark.parametrize('object_type', ["Metadata", "Mappings", "Conditions", "Transform", "Outputs"])
    def test_only_search_parameters_and_resources(self, object_type):
        # Setup
        stack = Stack()
        data = ZeroAttributeObject()
        setattr(stack, object_type, {"Foo": data})

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data)

        assert "not part of this stack" in str(excinfo.value)

    @pytest.mark.parametrize('object_type',
                             ["Parameters", "Metadata", "Mappings", "Conditions", "Transform", "Outputs"])
    def test_only_search_resources_when_requested(self, object_type):
        # Setup
        stack = Stack()
        data = ZeroAttributeObject()
        setattr(stack, object_type, {"Foo": data})

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data, resources_only=True)

        assert "not part of this stack" in str(excinfo.value)

    def test_fail_if_object_is_pseudo_parameter_when_only_searching_resources(self):
        # Setup
        data = AWS_Region
        stack = Stack()

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            stack.get_logical_name(data, resources_only=True)

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
        # TODO #87 Add Condition when we have a helper class
        # TODO #87 Add Mapping when we have a helper class
    ]

    # TODO #87 test_does_not_copy_metadata when we have a Metadata class

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

    def test_does_not_copy_description(self):
        # Setup
        source = Stack(Description="Source Description")
        original_description = "Target Description"
        target = Stack(Description=original_description)

        # Exercise
        target.merge_stack(source)

        # Verify
        assert target.Description == original_description

    def test_cannot_merge_if_template_version_is_different(self):
        source = Stack(AWSTemplateFormatVersion="123")
        target = Stack(AWSTemplateFormatVersion="456")

        # Exercise & Verify
        with pytest.raises(StackMergeError) as excinfo:
            target.merge_stack(source)

        assert "template version" in str(excinfo.value).lower()

    def test_cannot_merge_if_sam_transform_version_is_different(self):
        source = Stack(Transform="123")
        target = Stack(Transform="456")

        # Exercise & Verify
        with pytest.raises(StackMergeError) as excinfo:
            target.merge_stack(source)

        assert "transform version" in str(excinfo.value).lower()

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

    def test_return_value_is_a_new_stack(self):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise
        new_stack = stack.with_prefixed_names(self.STACK_PREFIX)

        # Verify
        assert isinstance(new_stack, Stack)
        assert new_stack is not stack

    @given(aws_logical_name_strategy())
    def test_prefix_is_an_underscored_alphanumeric_string(self, prefix):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise & Verify
        _ = stack.with_prefixed_names(prefix)  # Should not throw an error

    def test_prefix_cannot_be_empty(self):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            _ = stack.with_prefixed_names("")

        assert "empty" in str(excinfo.value).lower()

    def test_prefix_must_have_leading_capital(self):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            _ = stack.with_prefixed_names("lowercasedCamelsAreBactrianButInvalid")

        assert "uppercase" in str(excinfo.value).lower()

    @given(st.from_regex(re.compile(r"^[A-Z]\w*\W+\w*$", re.ASCII)))
    def test_prefix_cannot_contain_special_characters(self, prefix):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise & Verify
        with pytest.raises(ValueError) as excinfo:
            _ = stack.with_prefixed_names(prefix)

        assert "alphanumeric" in str(excinfo.value).lower()

    @pytest.mark.parametrize('prefix', [
        None,
        123,
        Stack(),
    ])
    def test_prefix_must_be_string(self, prefix):
        # Setup
        stack = Stack(Resources={"SomeName": SimpleResource()})

        # Exercise & Verify
        with pytest.raises(TypeError) as excinfo:
            _ = stack.with_prefixed_names(prefix)

        assert "string" in str(excinfo.value).lower()

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
        assert getattr(new_item, "Value", None) is getattr(item, "Value", None), \
            "This should be the same because it might be a Reference function or some such"

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


class TestTagStack(BaseTaggingTest):
    """Test recursive tagging for stack objects."""

    @parametrize_tagging_techniques()
    def test_resource_object_has_tags_applied(self, apply_tags):
        # Setup
        class TaggableResource(Resource):
            RESOURCE_TYPE = "NameSpace::Service::TaggableResource"
            RESOURCE_PROPERTIES = {"SomeProperty", "AnotherProperty", "Tags"}

        resource = TaggableResource()
        stack = Stack(Resources={"Foo": resource})

        key = "foo"
        value = "bar"

        # Exercise
        apply_tags(stack, key, value)

        # Verify
        self.verify_tag_exists(resource, key, value)

    @parametrize_tagging_techniques()
    def test_non_resource_object_is_silently_ignored(self, apply_tags):
        # Setup
        resource = {}
        stack = Stack(Resources={"Foo": resource})

        key = "foo"
        value = "bar"

        # Exercise
        apply_tags(stack, key, value)

        # Verify
        self.verify_tag_doesnt_exist(resource, key, value)

    @parametrize_tagging_techniques()
    def test_resource_like_object_has_tags_applied(self, apply_tags):
        # Setup Resource-like object.
        #
        # For simplicity of testing we use the same data structure as a
        # normal resource to store the tagging information
        class ResourceLikeThing(AWSObject):
            AWS_ATTRIBUTES = {"Properties"}

            def tag(self, tags=None, tag_derived_resources=True):
                # noinspection PyAttributeOutsideInit
                self.Properties = ResourceProperties(
                    property_names={"Tags"},
                    Tags=[{"Key": key, "Value": value} for key, value in tags.items()],
                )

        resource = ResourceLikeThing()

        # Setup
        stack = Stack(Resources={"Foo": resource})

        key = "foo"
        value = "bar"

        # Exercise
        apply_tags(stack, key, value)

        # Verify
        self.verify_tag_exists(resource, key, value)
