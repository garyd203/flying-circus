"""Tests for the implementation of intrinsic functions"""

import hypothesis.strategies as st
import pytest
from hypothesis import given
from unittest.mock import Mock

from core_test.common import SingleAttributeObject
from core_test.common import ZeroAttributeObject
from flyingcircus.core import AWS_Region
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from flyingcircus.intrinsic_function import Ref
from flyingcircus.yaml import AmazonCFNDumper


class TestRef:
    """Test behaviour/output of the Ref function."""

    # TODO output should be single-quote encapsulated if it contains a special character. eg. AWS::Region. Will need to tweak our yaml output (again)

    def _create_dumper(self, stack):
        dumper = AmazonCFNDumper(None)
        dumper.cfn_stack = stack
        return dumper

    def test_uses_bang_ref_tag_for_yaml_scalar(self):
        # Setup
        dumper = self._create_dumper(Mock(Stack))
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

        dumper = self._create_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    @pytest.mark.skip("#45: We currently explicitly set all top-level Stack attributes, which pollutes the output")
    def test_stack_yaml_output(self):
        """An integration test, yay!"""
        # Setup
        data = SingleAttributeObject(one=42)
        stack = Stack(Resources=dict(Foo=data, Bar=Ref(data)))

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent("""
            ---
            AWSTemplateFormatVersion: '2010-09-09'
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

        dumper = self._create_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_referred_object_can_be_a_pseudo_parameter(self):
        # Setup
        name = "SomeRegion"
        ref = Ref(AWS_Region)
        stack = Stack(Resources={name: ref})

        dumper = self._create_dumper(stack)

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

        dumper = self._create_dumper(stack)

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
        stack[object_type][name] = data
        ref = Ref(data)

        dumper = self._create_dumper(stack)

        # Exercise & Verify
        with pytest.raises(Exception):
            ref.as_yaml_node(dumper)
