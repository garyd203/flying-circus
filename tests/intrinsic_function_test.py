"""Tests for the implementation of intrinsic functions"""

from unittest.mock import Mock

import hypothesis.strategies as st
import pytest
from hypothesis import given

from flyingcircus.core import AWS_Region
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.intrinsic_function import GetAZs
from flyingcircus.intrinsic_function import Ref
from flyingcircus.yaml import AmazonCFNDumper
from .core_test.common import SingleAttributeObject
from .core_test.common import ZeroAttributeObject


def _create_refsafe_dumper(stack):
    dumper = AmazonCFNDumper(None)
    dumper.cfn_stack = stack
    return dumper


class TestGetAZs:
    """Test behaviour/output of the GetAZs function."""

    def _get_mapping_node_key(self, node, i=0):
        return node.value[i][0].value

    def _get_mapping_node_value(self, node, i=0):
        return node.value[i][1].value

    def test_uses_bang_ref_tag_for_yaml_scalar(self):
        # Setup
        dumper = _create_refsafe_dumper(None)
        func = GetAZs("ap-southeast-2")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == "!GetAZs"

    @pytest.mark.parametrize("region", ["us-east-1", "ap-southeast-2"])
    def test_supplied_region_is_used_in_output(self, region):
        # Setup. We test with a couple of regions only
        dumper = _create_refsafe_dumper(None)
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
        assert output == dedent("""
            ---
            one: !GetAZs ap-southeast-2
            """)

    def test_nested_function_forces_longform_name(self):
        # Setup
        dumper = _create_refsafe_dumper(Stack())
        func = GetAZs(Ref(AWS_Region))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        assert node.tag == dumper.DEFAULT_MAPPING_TAG
        assert len(node.value) == 1

        function_name = self._get_mapping_node_key(node, 0)
        assert function_name == "Fn::GetAZs"

    def test_region_can_be_a_ref_function(self):
        # Setup
        dumper = _create_refsafe_dumper(Stack())
        region = AWS_Region
        func = GetAZs(Ref(region))

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        function_param = self._get_mapping_node_value(node, 0)
        assert function_param == str(region)

    def test_yaml_output_with_nested_function(self):
        """Nested YAML functions can't both use the ! short form."""
        # Setup
        func = GetAZs(Ref(AWS_Region))
        data = SingleAttributeObject(one=func)
        stack = Stack(Resources=dict(SomeResource=data))

        # Exercise
        output = stack.export("yaml")

        # Verify
        # TODO "#45: clean up the unnecessary empty top-level stack attributes
        assert output == dedent("""
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Parameters: {}
            Resources:
              SomeResource:
                one:
                  Fn::GetAZs: !Ref AWS::Region
            """)

    def test_empty_region_becomes_explicit_aws_region_reference(self):
        # Setup
        dumper = _create_refsafe_dumper(Stack())
        func = GetAZs("")

        # Exercise
        node = func.as_yaml_node(dumper)

        # Verify
        function_param = self._get_mapping_node_value(node, 0)
        assert function_param == str(AWS_Region)

    def test_unspecified_region_becomes_explicit_aws_region_reference(self):
        # Setup
        dumper = _create_refsafe_dumper(Stack())
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


class TestRef:
    """Test behaviour/output of the Ref function."""

    # TODO output should be single-quote encapsulated if it contains a special character. eg. AWS::Region. Will need to tweak our yaml output (again)

    def test_uses_bang_ref_tag_for_yaml_scalar(self):
        # Setup
        dumper = _create_refsafe_dumper(Mock(Stack))
        ref = Ref(ZeroAttributeObject())

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.tag == "!Ref"

    @given(st.text())
    def test_uses_logical_name_from_stack(self, name):
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources={name: data})
        ref = Ref(data)

        dumper = _create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_stack_yaml_output(self):
        """An integration test, yay!"""
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources=dict(Foo=data, Bar=Ref(data)))

        # Exercise
        output = stack.export("yaml")

        # Verify
        # TODO "#45: clean up the unnecessary empty top-level stack attributes
        assert output == dedent("""
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Parameters: {}
            Resources:
              Bar: !Ref Foo
              Foo:
                one: 42
            """)

    def test_referred_object_can_be_a_plain_dict(self):
        # Setup
        data = dict(bar='hello')
        name = "Foo"
        stack = Stack(Resources={name: data})
        ref = Ref(data)

        dumper = _create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_referred_object_can_be_a_pseudo_parameter(self):
        # Setup
        name = "SomeRegion"
        ref = Ref(AWS_Region)
        stack = Stack(Resources={name: ref})

        dumper = _create_refsafe_dumper(stack)

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

    @pytest.mark.parametrize('object_type', ["Parameters", "Resources"])
    def test_all_valid_stack_object_types_can_be_found(self, object_type):
        # Setup
        data = SingleAttributeObject(one=42)
        name = "Foo"
        stack = Stack()
        stack[object_type][name] = data
        ref = Ref(data)

        dumper = _create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    @pytest.mark.parametrize('object_type', ["Metadata", "Mappings", "Conditions", "Transform", "Outputs"])
    def test_invalid_stack_object_types_cannot_be_found(self, object_type):
        # Setup
        data = SingleAttributeObject(one=42)
        name = "Foo"
        stack = Stack()
        setattr(stack, object_type, {name: data})
        ref = Ref(data)

        dumper = _create_refsafe_dumper(stack)

        # Exercise & Verify
        with pytest.raises(Exception):
            ref.as_yaml_node(dumper)
