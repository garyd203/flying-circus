"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""
import pytest

from flyingcircus.core import AWSObject


class TestYAMLOutput:
    """Verify YAML output."""
    pass


class TestBaseClass:
    """Verify behaviour of the base AWSObject class specifically"""

    @pytest.mark.skip
    def test_init_should_not_accept_positional_parameters(self):
        assert False

    @pytest.mark.skip
    def test_init_should_only_accept_kwargs(self):
        assert False

    @pytest.mark.skip
    def test_init_should_map_keyword_args_to_attributes(self):
        assert False


class TestAttributeAccess:
    """Verify behaviour of attributes on a Flying Circus AWS object"""

    # TODO dict access for aws attributes only
    # TODO default values. Do this with constructor default args
    # TODO use hypothesis for value injection
    # TODO delete nonexistent attributes of various sorts
    # TODO verify behaviour of set_unknown_aws_attribute with know attribute

    def _create_simple_class(self):
        class SimpleClass(AWSObject):
            AWS_ATTRIBUTES = {"Foo", "bar", "ValueWithDefault"}

            def __init__(self, Foo=None, bar=None, ValueWithDefault=42):
                AWSObject.__init__(self, Foo=Foo, bar=bar, ValueWithDefault=ValueWithDefault)

        return SimpleClass

    # Set and Read
    # ------------

    def test_valid_aws_attributes_can_be_set_and_read(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.Foo = "123"
        data.bar = "321"

        assert hasattr(data, "Foo")
        assert data.Foo == "123"
        assert hasattr(data, "bar")
        assert data.bar == "321"

    def test_internal_attributes_can_be_set_and_read(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data._internal_value = "123"

        assert hasattr(data, "_internal_value")
        assert data._internal_value == "123"

    def test_unknown_attributes_cannot_be_set_directly(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        with pytest.raises(AttributeError) as excinfo:
            data.WeirdValue = "hello"
        assert "WeirdValue" in str(excinfo.value)
        assert not hasattr(data, "WeirdValue")

    def test_unknown_aws_attributes_can_be_explicitly_set_and_read_normally(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.set_unknown_aws_attribute("WeirdValue", "hello")

        assert hasattr(data, "WeirdValue")
        assert data.WeirdValue == "hello"

    def test_valid_aws_attributes_cannot_be_explicitly_set(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.set_unknown_aws_attribute("WeirdValue", "hello")
        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("bar", "hello")
        assert "bar" in str(excinfo.value)
        assert not hasattr(data, "bar")

    # Read Special Cases
    # ------------------

    def test_aws_attributes_cannot_be_read_before_they_are_set(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        assert not hasattr(data, "Foo")

    def test_aws_attributes_with_a_default_value_can_be_read_before_they_are_set(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        assert hasattr(data, "ValueWithDefault")
        assert data.ValueWithDefault == 42

    # Update
    # ------

    @pytest.mark.skip
    def test_aws_attributes_can_be_updated(self):
        assert False

    @pytest.mark.skip
    def test_internal_attributes_can_be_updated(self):
        assert False

    @pytest.mark.skip
    def test_unknown_aws_attributes_can_be_updated(self):
        # TODO By the same special access function and/or normal setattr
        assert False

    # Delete
    # ------

    @pytest.mark.skip
    def test_aws_attributes_can_be_deleted(self):
        assert False

    @pytest.mark.skip
    def test_unknown_aws_attributes_can_be_deleted(self):
        assert False

    @pytest.mark.skip
    def test_internal_attributes_can_be_deleted(self):
        assert False
