"""Tests for the Stack base class."""

from flyingcircus.core import Stack


class TestBasicStackBehaviour:
    """Verify basic behaviour of the Stack class"""

    def test_template_version_defaults_to_2010(self):
        stack = Stack()

        assert stack.AWSTemplateFormatVersion == "2010-09-09"
