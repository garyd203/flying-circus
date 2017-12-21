"""Tests for the yaml helper module."""

import pytest

from flyingcircus.core import Stack
from flyingcircus.yaml import AmazonCFNDumper
from .core_test.common import ZeroAttributeObject


class TestCloudFormationStackProperty:
    """Verify that the current stack reference works correctly."""

    def test_stack_is_initialised_to_none(self):
        dumper = AmazonCFNDumper(None)

        assert dumper.cfn_stack is None

    def test_stack_returns_the_supplied_value(self):
        # Setup
        dumper = AmazonCFNDumper(None)
        stack = Stack()

        dumper.cfn_stack = stack

        # Exercise & Verify
        assert dumper.cfn_stack is stack

    def test_stack_can_be_set_to_none(self):
        # Setup
        dumper = AmazonCFNDumper(None)
        stack = Stack()

        # Exercise
        dumper.cfn_stack = None

        dumper.cfn_stack = stack
        dumper.cfn_stack = None

        # Verify
        assert dumper.cfn_stack is None

    def test_stack_must_be_a_stack_object(self):
        # Setup
        dumper = AmazonCFNDumper(None)
        not_a_stack = ZeroAttributeObject()

        # Exercise
        with pytest.raises(TypeError) as excinfo:
            dumper.cfn_stack = not_a_stack

        # Verify
        assert "must be a Stack" in str(excinfo.value)

    def test_stack_cannot_be_set_when_it_is_already_set(self):
        # Setup
        dumper = AmazonCFNDumper(None)
        stack1 = Stack()
        stack2 = Stack()

        dumper.cfn_stack = stack1

        # Exercise & Verify
        with pytest.raises(RuntimeError) as excinfo:
            dumper.cfn_stack = stack2

        assert "already set" in str(excinfo.value)

    def test_stack_can_be_set_after_it_has_been_reset(self):
        # Setup
        dumper = AmazonCFNDumper(None)
        stack1 = Stack()
        stack2 = Stack()

        dumper.cfn_stack = stack1
        dumper.cfn_stack = None

        # Exercise
        dumper.cfn_stack = stack2

        # Verify
        assert dumper.cfn_stack is stack2
