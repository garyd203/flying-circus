"""Tests for the implementation of intrinsic functions"""

import re
from unittest.mock import Mock

import hypothesis.strategies as st
import pytest
from hypothesis import given
from yaml import ScalarNode
from yaml import SequenceNode

from flyingcircus.core import AWS_Region
from flyingcircus.core import AWS_StackName
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.intrinsic_function import Base64
from flyingcircus.intrinsic_function import GetAZs
from flyingcircus.intrinsic_function import GetAtt
from flyingcircus.intrinsic_function import ImportValue
from flyingcircus.intrinsic_function import Join
from flyingcircus.intrinsic_function import Ref
from flyingcircus.intrinsic_function import Sub
from .core_test.common import SingleAttributeObject
from .core_test.common import ZeroAttributeObject
from .pyyaml_helper import create_refsafe_dumper
from .pyyaml_helper import get_mapping_node_key


# TODO these tests are in dire need of hypothesis and some smart strategies


class TestBase64:
    """Test behaviour of the Base64 function."""

    def test_uses_abbreviated_tag_for_yaml_scalar(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Base64("Something something")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!Base64"

    def test_yaml_output(self):
        # Setup
        func = Base64("Something")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Base64 Something
            """
        )

    def test_yaml_output_doesnt_modify_string(self):
        # Setup
        func = Base64("Some 6HSsort of text_?:%#")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Base64 Some 6HSsort of text_?:%#
            """
        )

    def test_nested_function_forces_longform_name(self):
        # TODO #37 do this with a Sub to be more realistic
        # Setup
        dumper = create_refsafe_dumper(Stack())
        func = Base64(Ref(AWS_StackName))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == dumper.DEFAULT_MAPPING_TAG
        assert len(node.value) == 1

        function_name = get_mapping_node_key(node, 0)
        assert function_name == "Fn::Base64"

    def test_yaml_output_with_nested_function(self):
        """Nested YAML functions can't both use the ! short form."""
        # TODO #37 do this with a Sub to be more realistic

        # Setup
        func = Base64(Ref(AWS_StackName))
        data = SingleAttributeObject(one=func)
        stack = Stack(Resources=dict(SomeResource=data))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              SomeResource:
                one:
                  Fn::Base64: !Ref AWS::StackName
            """
        )


class TestGetAtt:
    """Test behaviour/output of the GetAtt function."""

    # Helper Methods
    # --------------
    @staticmethod
    def _create_getatt_function(resource_name, *attrib_name):
        """Create a GetAtt function object that refers to a valid resource.

        Returns:
            A tuple of (dumper, function_object)
        """
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources={resource_name: data})
        func = GetAtt(data, *attrib_name)

        dumper = create_refsafe_dumper(stack)

        return dumper, func

    # YAML Output
    # -----------
    def test_uses_abbreviated_tag_for_yaml_scalar(self):
        # Setup
        dumper, func = self._create_getatt_function("SomeResource", "Attrib")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!GetAtt"

    def test_stack_yaml_output(self):
        """An integration test, yay!"""
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources=dict(Foo=data, Bar=GetAtt(data, "ResourceAttrib1")))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              Bar: !GetAtt Foo.ResourceAttrib1
              Foo:
                one: 42
            """
        )

    def test_nested_function_forces_longform_name(self):
        # Setup
        dumper, func = self._create_getatt_function(
            "SomeResource", "Foo", Ref(AWS_Region)
        )

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == dumper.DEFAULT_MAPPING_TAG
        assert len(node.value) == 1

        function_name = get_mapping_node_key(node, 0)
        assert function_name == "Fn::GetAtt"

    def test_yaml_output_with_nested_function(self):
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(
            Resources=dict(
                Foo=data, Bar=GetAtt(data, "ResourceAttrib1", Ref(AWS_Region))
            )
        )
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              Bar:
                Fn::GetAtt:
                - Foo
                - ResourceAttrib1
                - !Ref AWS::Region
              Foo:
                one: 42
            """
        )

    # Stack Reference Lookup
    # ----------------------

    def test_uses_logical_name_from_stack(self):
        # Setup
        dumper, func = self._create_getatt_function("SomeResource", "Attrib")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == "SomeResource.Attrib"

    def test_referred_object_can_be_a_plain_dict(self):
        # Setup
        data = {"one": 42}
        stack = Stack(Resources={"SomeResource": data})
        func = GetAtt(data, "Attrib")

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == "SomeResource.Attrib"

    def test_referred_object_that_is_a_string_is_rejected_immediately(self):
        # Setup
        name = "SomeResource"
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources={name: data})

        # Exercise
        with pytest.raises(TypeError) as excinfo:
            _ = GetAtt(name, "AttribName")

        assert "directly create a GetAtt on a logical name" in str(excinfo.value)

    @pytest.mark.parametrize(
        "object_type",
        ["Parameters", "Metadata", "Mappings", "Conditions", "Transform", "Outputs"],
    )
    def test_non_resource_stack_objects_cannot_be_referenced(self, object_type):
        # Setup
        data = {"one": 42}
        stack = Stack()
        setattr(stack, object_type, {"SomeResource": data})

        func = GetAtt(data, "Attrib")

        dumper = create_refsafe_dumper(stack)

        # Exercise
        with pytest.raises(Exception):
            func.as_yaml_node(dumper)

    # Attribute Name
    # --------------
    def test_attribute_name_list_cannot_be_empty(self):
        # Exercise
        with pytest.raises(ValueError) as excinfo:
            _ = GetAtt({"one": 42})

        assert "AWS attribute name is required" in str(excinfo.value)

    def test_attribute_name_is_a_single_string(self):
        # Setup
        dumper, func = self._create_getatt_function("SomeResource", "Attrib")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == "SomeResource.Attrib"

    def test_attribute_name_is_a_single_dotted_string(self):
        # Setup
        dumper, func = self._create_getatt_function("SomeResource", "Attrib.SubAttrib")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == "SomeResource.Attrib.SubAttrib"

    def test_attribute_name_is_a_list_of_strings(self):
        # Setup
        dumper, func = self._create_getatt_function(
            "SomeResource", "Attrib", "SubAttrib", "SomethingElse"
        )

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == "SomeResource.Attrib.SubAttrib.SomethingElse"

    test_attribute_name_contains_a_ref = test_nested_function_forces_longform_name

    def test_attribute_name_contains_an_unsupported_function(self):
        # Exercise
        with pytest.raises(ValueError) as excinfo:
            _ = GetAtt({"one": 42}, "Attrib", GetAZs())

        assert "GetAZs" in str(excinfo.value)

    # Equality
    # --------
    def test_getatt_on_same_resource_is_equal(self):
        # Setup
        data = SingleAttributeObject(one=42)
        func1 = GetAtt(data, "Attrib")
        func2 = GetAtt(data, "Attrib")

        # Verify
        assert func1 == func2
        assert not (func1 != func2)
        assert hash(func1) == hash(func2)

    def test_getatt_with_same_ref_as_attribute_is_equal(self):
        # Setup
        data = SingleAttributeObject(one=42)
        referent = ZeroAttributeObject()

        func1 = GetAtt(data, Ref(referent))
        func2 = GetAtt(data, Ref(referent))

        # Verify
        assert func1 == func2
        assert not (func1 != func2)
        assert hash(func1) == hash(func2)

    def test_getatt_on_different_resources_is_not_equal(self):
        # Setup
        func1 = GetAtt(SingleAttributeObject(one=42), "Attrib")
        func2 = GetAtt(ZeroAttributeObject(), "Attrib")

        # Verify
        assert func1 != func2
        assert not (func1 == func2)
        assert hash(func1) != hash(func2)

    def test_getatt_on_different_attributes_is_not_equal(self):
        # Setup
        data = SingleAttributeObject(one=42)
        func1 = GetAtt(data, "Attrib1", "Attrib2")
        func2 = GetAtt(data, "Attrib2", "Attrib1")

        # Verify
        assert func1 != func2
        assert not (func1 == func2)
        assert hash(func1) != hash(func2)

    def test_getatt_on_similar_resources_is_not_equal(self):
        # Setup
        func1 = GetAtt(SingleAttributeObject(one=42), "Attrib")
        func2 = GetAtt(SingleAttributeObject(one=42), "Attrib")

        # Verify
        assert func1 != func2
        assert not (func1 == func2)
        assert hash(func1) != hash(func2)

    @pytest.mark.parametrize(
        "constructor",
        [
            # An unrelated data type
            lambda a, b: tuple((a, b))
        ],
    )
    def test_getatt_is_not_equal_to_arbitrary_object(self, constructor):
        # Setup
        data = SingleAttributeObject(one=42)

        func = GetAtt(data, "Attrib")
        other = constructor(data, "Attrib")

        # Verify
        assert func != other
        assert other != func
        assert not (func == other)
        assert not (other == func)
        assert hash(func) != hash(other)

    def test_hash_is_different_from_hash_of_resource(self):
        # Setup
        data = SingleAttributeObject(one=42)
        func = GetAtt(data, "Attrib")

        # Verify
        assert hash(data) != hash(func)


class TestGetAZs:
    """Test behaviour/output of the GetAZs function."""

    def _get_mapping_node_value(self, node, i=0):
        return node.value[i][1].value

    def test_uses_abbreviated_tag_for_yaml_scalar(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = GetAZs("ap-southeast-2")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!GetAZs"

    @pytest.mark.parametrize("region", ["us-east-1", "ap-southeast-2"])
    def test_supplied_region_is_used_in_output(self, region):
        # Setup. We test with a couple of regions only
        dumper = create_refsafe_dumper(None)
        func = GetAZs(region)

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == region

    def test_yaml_output(self):
        # Setup
        func = GetAZs("ap-southeast-2")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !GetAZs ap-southeast-2
            """
        )

    def test_nested_function_forces_longform_name(self):
        # Setup
        dumper = create_refsafe_dumper(Stack())
        func = GetAZs(Ref(AWS_Region))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == dumper.DEFAULT_MAPPING_TAG
        assert len(node.value) == 1

        function_name = get_mapping_node_key(node, 0)
        assert function_name == "Fn::GetAZs"

    def test_yaml_output_with_nested_function(self):
        """Nested YAML functions can't both use the ! short form."""
        # Setup
        func = GetAZs(Ref(AWS_Region))
        data = SingleAttributeObject(one=func)
        stack = Stack(Resources=dict(SomeResource=data))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              SomeResource:
                one:
                  Fn::GetAZs: !Ref AWS::Region
            """
        )

    def test_region_can_be_a_ref_function(self):
        # Setup
        dumper = create_refsafe_dumper(Stack())
        region = AWS_Region
        func = GetAZs(Ref(region))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        function_param = self._get_mapping_node_value(node, 0)
        assert function_param == str(region)

    def test_empty_region_becomes_explicit_aws_region_reference(self):
        # Setup
        dumper = create_refsafe_dumper(Stack())
        func = GetAZs("")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        function_param = self._get_mapping_node_value(node, 0)
        assert function_param == str(AWS_Region)

    def test_unspecified_region_becomes_explicit_aws_region_reference(self):
        # Setup
        dumper = create_refsafe_dumper(Stack())
        func = GetAZs()

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        function_param = self._get_mapping_node_value(node, 0)
        assert function_param == str(AWS_Region)

    @pytest.mark.skip("#60: Fail early if we supply an invalid region")
    def test_region_string_must_be_a_valid_region(self):
        with pytest.raises(ValueError) as excinfo:
            _ = GetAZs("some-fakeregion-2")

        assert "unknown region" in str(excinfo.value)


class TestImportValue:
    """Test behaviour/output of the ImportValue function."""

    def test_uses_abbreviated_tag_for_yaml_scalar(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = ImportValue("some_export_name")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!ImportValue"

    def test_supplied_export_name_is_used_in_output(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        export_name = "some_export_name"
        func = ImportValue(export_name)

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value == export_name

    def test_yaml_output(self):
        # Setup
        func = ImportValue("SomeStack-export_name")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !ImportValue SomeStack-export_name
            """
        )

    def test_nested_function_forces_longform_name(self):
        # Setup
        dumper = create_refsafe_dumper(Stack())
        func = ImportValue(Sub("${AWS::Region}-SharedLogBucket"))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == dumper.DEFAULT_MAPPING_TAG
        assert len(node.value) == 1

        function_name = get_mapping_node_key(node, 0)
        assert function_name == "Fn::ImportValue"

    def test_yaml_output_with_nested_function(self):
        """Nested YAML functions can't both use the ! short form."""
        # Setup
        func = ImportValue(Sub("${AWS::Region}-SharedLogBucket"))
        data = SingleAttributeObject(one=func)
        stack = Stack(Resources=dict(SomeResource=data))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              SomeResource:
                one:
                  Fn::ImportValue: !Sub '${AWS::Region}-SharedLogBucket'
            """
        )

    # Equality
    # --------
    def test_imports_of_same_name_are_equal(self):
        # Setup
        name = "some-exported-name"
        import1 = ImportValue(name)
        import2 = ImportValue(name)

        # Verify
        assert import1 == import2
        assert not (import1 != import2)
        assert hash(import1) == hash(import2)

    def test_imports_of_different_names_are_not_equal(self):
        # Setup
        import1 = ImportValue("exported-name-1")
        import2 = ImportValue("exported-name-2")

        # Verify
        assert import1 != import2
        assert not (import1 == import2)
        assert hash(import1) != hash(import2)

    @pytest.mark.parametrize(
        "constructor",
        [
            # An ImportValue-like object
            Base64,
            # An unrelated data type
            str,
        ],
    )
    def test_import_is_not_equal_to_arbitrary_object(self, constructor):
        # Setup
        name = "some-exported-name"
        func = ImportValue(name)
        other = constructor(name)

        # Verify
        assert func != other
        assert other != func
        assert not (func == other)
        assert not (other == func)
        assert hash(func) != hash(other)

    def test_hash_is_different_from_hash_of_export_name(self):
        # Setup
        name = "some-exported-name"
        func = ImportValue(name)

        # Verify
        assert hash(name) != hash(func)


class TestJoin:
    """Test behaviour/output of the Join function."""

    # Test Helpers
    # ------------

    def _verify_delimiter(self, node, delimiter):
        assert node.value[0].value == delimiter

    def _verify_values(self, node, values: list):
        actual_values = [n.value for n in node.value[1].value]
        assert actual_values == values

    # YAML Output
    # -----------

    def test_uses_abbreviated_tag(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Join(".", "foo", "bar")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == "!Join"

    def test_supplied_values_are_used_in_output(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        expected_delimiter = "."
        expected_values = ["foo", "bar", "baz"]
        func = Join(expected_delimiter, *expected_values)

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, SequenceNode)
        assert len(node.value) == 2
        self._verify_delimiter(node, expected_delimiter)
        self._verify_values(node, expected_values)

    def test_yaml_output_as_args(self):
        # Setup
        func = Join(".", "foo", "bar")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Join
            - .
            - - foo
              - bar
            """
        )

    def test_yaml_output_as_list_parameter(self):
        # Setup
        func = Join(".", ["foo", "bar"])
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Join
            - .
            - - foo
              - bar
            """
        )

    # Delimiter
    # ---------

    @pytest.mark.parametrize("value", [None, Ref(AWS_StackName)])
    def test_delimiter_must_be_a_string(self, value):
        with pytest.raises(TypeError, match=re.compile(r"delimiter.*string", re.I)):
            _ = Join(value, "foo", "bar")

    def test_delimiter_can_be_empty_string(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Join("", "foo", "bar")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        self._verify_delimiter(node, "")

    def test_yaml_output_when_delimiter_is_empty(self):
        # Setup
        func = Join("", ["foo", "bar"])
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Join
            - ''
            - - foo
              - bar
            """
        )

    def test_delimiter_can_have_more_than_one_character(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Join("::", "foo", "bar")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        self._verify_delimiter(node, "::")

    def test_delimiter_should_not_be_huge(self):
        delimiter = "syzygy" * 10

        with pytest.raises(
            ValueError, match=re.compile(r"delimiter.*(large|long)", re.I)
        ):
            _ = Join(delimiter, "foo", "bar")

    # Input Values
    # ------------

    def test_input_values_can_be_a_single_list_parameter(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        expected_delimiter = "."
        expected_values = ["foo", "bar", "baz"]
        func = Join(expected_delimiter, expected_values)

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, SequenceNode)
        assert len(node.value) == 2
        self._verify_delimiter(node, expected_delimiter)
        self._verify_values(node, expected_values)

    def test_input_values_can_include_functions(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Join(".", [Base64("Something"), "foo", "bar"])

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.value[1].value[0].tag == "!Base64"
        self._verify_values(node, ["Something", "foo", "bar"])

    def test_input_values_must_contain_multiple_values(self):
        with pytest.raises(ValueError, match=r"values.*at least 2"):
            _ = Join(".", "foo")

    def test_input_values_as_list_must_contain_multiple_values(self):
        with pytest.raises(ValueError, match=r"values.*at least 2"):
            _ = Join(".", ["foo"])


class TestRef:
    """Test behaviour/output of the Ref function."""

    # TODO output should be single-quote encapsulated if it contains a special character. eg. AWS::Region. Will need to tweak our yaml output (again)

    def test_uses_bang_ref_tag_for_yaml_scalar(self):
        # Setup
        dumper = create_refsafe_dumper(Mock(Stack))
        ref = Ref(ZeroAttributeObject())

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!Ref"

    @given(st.text(min_size=1))
    def test_uses_logical_name_from_stack(self, name):
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources={name: data})
        ref = Ref(data)

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_stack_yaml_output(self):
        """An integration test, yay!"""
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources=dict(Foo=data, Bar=Ref(data)))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              Bar: !Ref Foo
              Foo:
                one: 42
            """
        )

    def test_referred_object_can_be_a_plain_dict(self):
        # Setup
        data = dict(bar="hello")
        name = "Foo"
        stack = Stack(Resources={name: data})
        ref = Ref(data)

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_referred_object_can_be_a_pseudo_parameter(self):
        # Setup
        name = "SomeRegion"
        ref = Ref(AWS_Region)
        stack = Stack(Resources={name: ref})

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == "AWS::Region"

    def test_referred_object_that_is_a_string_is_rejected_immediately(self):
        # Setup
        data = SingleAttributeObject(one=42)
        name = "Foo"
        stack = Stack(Resources={name: data})

        # Exercise & Verify
        with pytest.raises(TypeError) as excinfo:
            _ = Ref(name)

        assert "directly create a Ref to a name" in str(excinfo.value)

    @pytest.mark.parametrize("object_type", ["Parameters", "Resources"])
    def test_all_valid_stack_object_types_can_be_found(self, object_type):
        # Setup
        data = SingleAttributeObject(one=42)
        name = "Foo"
        stack = Stack()
        stack[object_type][name] = data
        ref = Ref(data)

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    @pytest.mark.parametrize(
        "object_type", ["Metadata", "Mappings", "Conditions", "Transform", "Outputs"]
    )
    def test_invalid_stack_object_types_cannot_be_found(self, object_type):
        # Setup
        data = SingleAttributeObject(one=42)
        name = "Foo"
        stack = Stack()
        setattr(stack, object_type, {name: data})
        ref = Ref(data)

        dumper = create_refsafe_dumper(stack)

        # Exercise & Verify
        with pytest.raises(Exception):
            ref.as_yaml_node(dumper)

    def test_refs_to_same_object_are_equal(self):
        # Setup
        data = SingleAttributeObject(one=42)
        ref1 = Ref(data)
        ref2 = Ref(data)

        # Verify
        assert ref1 == ref2
        assert not (ref1 != ref2)
        assert hash(ref1) == hash(ref2)

    def test_refs_to_different_objects_are_not_equal(self):
        # Setup
        ref1 = Ref(SingleAttributeObject(one=42))
        ref2 = Ref(ZeroAttributeObject())

        # Verify
        assert ref1 != ref2
        assert not (ref1 == ref2)
        assert hash(ref1) != hash(ref2)

    def test_refs_to_similar_objects_are_not_equal(self):
        # Setup
        ref1 = Ref(SingleAttributeObject(one=42))
        ref2 = Ref(SingleAttributeObject(one=42))

        # Verify
        assert ref1 != ref2
        assert not (ref1 == ref2)
        assert hash(ref1) != hash(ref2)

    @pytest.mark.parametrize(
        "func",
        [
            # A Ref-like object
            Base64,
            # An unrelated data type
            str,
        ],
    )
    def test_ref_is_not_equal_to_arbitrary_object(self, func):
        # Setup
        data = SingleAttributeObject(one=42)

        ref = Ref(data)
        other = func(data)

        # Verify
        assert ref != other
        assert other != ref
        assert not (ref == other)
        assert not (other == ref)
        assert hash(ref) != hash(other)

    def test_hash_is_different_from_hash_of_referent(self):
        # Setup
        data = SingleAttributeObject(one=42)
        ref = Ref(data)

        # Verify
        assert hash(data) != hash(ref)


class TestSubWithoutExplicitVariables:
    """Test behaviour/output of the Sub function, when a variable mapping is not used."""

    # YAML Output
    # -----------
    def test_uses_abbreviated_tag_for_yaml_scalar(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Sub("Something something")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.tag == "!Sub"

    def test_always_uses_string_quoting_for_input(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Sub("Something something")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, ScalarNode)
        assert node.style != ""

    def test_yaml_output(self):
        # Setup
        func = Sub("Something")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub 'Something'
            """
        )

    def test_yaml_output_doesnt_modify_complex_string(self):
        # Setup. Use example from AWS documentation
        func = Sub("arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:vpc/${vpc}")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub 'arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:vpc/${vpc}'
            """
        )

    def test_yaml_output_doesnt_modify_multiline_string(self):
        # Setup. Use example from AWS documentation
        func = Sub(
            dedent(
                """
            #!/bin/bash -xe
            yum update -y aws-cfn-bootstrap
            /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfig --configsets wordpress_install --region ${AWS::Region}
            /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerGroup --region ${AWS::Region}
            """
            )
        )

        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub |
              #!/bin/bash -xe
              yum update -y aws-cfn-bootstrap
              /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfig --configsets wordpress_install --region ${AWS::Region}
              /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerGroup --region ${AWS::Region}
            """
        )

    # Parameters
    # ----------
    @pytest.mark.parametrize(
        "input",
        [
            AWS_Region,  # string-like PseudoParameter
            Base64("Some string with ${AWS::Region} embedded"),  # String-like function
        ],
    )
    def test_nonstring_input_is_rejected_immediately(self, input):
        with pytest.raises(TypeError):
            _ = Sub(input)


class TestSubWithVariableMapping:
    """Test behaviour/output of the Sub function, when a variable mapping is used."""

    # YAML Output
    # -----------
    def test_uses_abbreviated_tag_for_yaml_sequence(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Sub("Something-${foo}", foo="bar")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert isinstance(node, SequenceNode)
        assert node.tag == "!Sub"

    def test_yaml_output(self):
        # Setup
        func = Sub("Something-${foo}", foo="bar")
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub
            - Something-${foo}
            - foo: bar
            """
        )

    def test_yaml_output_doesnt_modify_complex_string(self):
        # Setup. Use (modified) example from AWS documentation
        func = Sub(
            "arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:vpc/${vpc}", vpc="someid"
        )
        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub
            - arn:aws:ec2:${AWS::Region}:${AWS::AccountId}:vpc/${vpc}
            - vpc: someid
            """
        )

    def test_yaml_output_doesnt_modify_multiline_string(self):
        # Setup. Use (modified) example from AWS documentation
        func = Sub(
            dedent(
                """
            #!/bin/bash -xe
            yum update -y aws-cfn-bootstrap
            /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfig --configsets wordpress_install --region ${AWS::Region}
            /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerGroup --region ${AWS::Region}
            echo hello from ${user}
            """
            ),
            user="bobbytables",
        )

        data = SingleAttributeObject(one=func)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent(
            """
            ---
            one: !Sub
            - |
              #!/bin/bash -xe
              yum update -y aws-cfn-bootstrap
              /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfig --configsets wordpress_install --region ${AWS::Region}
              /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource WebServerGroup --region ${AWS::Region}
              echo hello from ${user}
            - user: bobbytables
            """
        )

    # Variable Map
    # ------------
    def test_variable_map_can_include_functions(self):
        # Setup
        dumper = create_refsafe_dumper(None)
        func = Sub(
            "arn:aws:ec2:${AWS::Region}:${account}:vpc/${vpc}",
            account="123456789012",
            vpc=ImportValue("my-vpc-id"),
        )

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        varmap_node = node.value[1]
        vpc_var_node = varmap_node.value[1]
        assert (
            vpc_var_node[1].tag == "!ImportValue"
        )  # The dict value is the second element in a tuple

    # Parameters
    # ----------
    @pytest.mark.parametrize(
        "input",
        [
            AWS_Region,  # string-like PseudoParameter
            Base64("Some string with ${AWS::Region} embedded"),  # String-like function
        ],
    )
    def test_nonstring_input_is_rejected_immediately(self, input):
        with pytest.raises(TypeError):
            _ = Sub(input, foo="bar")

    @pytest.mark.parametrize("input", [123])  # number
    def test_nonstring_variable_name_is_rejected_immediately(self, input):
        with pytest.raises(TypeError):
            _ = Sub("Something something", **{input: "bar"})
