"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""
import pytest
from bdb import foo
from hypothesis import given
import hypothesis.strategies as st

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

    @given(st.text(), st.text())
    def test_valid_aws_attributes_can_be_set_and_read(self, foo_value, bar_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.Foo = foo_value
        data.bar = bar_value

        assert hasattr(data, "Foo")
        assert data.Foo == foo_value
        assert hasattr(data, "bar")
        assert data.bar == bar_value

    @given(st.text())
    def test_internal_attributes_can_be_set_and_read(self, value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data._internal_value = value

        assert hasattr(data, "_internal_value")
        assert data._internal_value == value

    def test_unknown_attributes_cannot_be_set_directly(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        with pytest.raises(AttributeError) as excinfo:
            data.WeirdValue = "hello"
        assert "WeirdValue" in str(excinfo.value)
        assert not hasattr(data, "WeirdValue")

    @given(st.text())
    def test_unknown_aws_attributes_can_be_explicitly_set_and_read_normally(self, value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.set_unknown_aws_attribute("WeirdValue", value)

        assert hasattr(data, "WeirdValue")
        assert data.WeirdValue == value

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

    @given(st.text(), st.text(), st.text())
    def test_aws_attributes_can_be_updated(self, foo_value_old, foo_value_new, bar_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        # Setup: set initial values
        data.Foo = foo_value_old
        data.bar = bar_value

        # Exercise
        data.Foo = foo_value_new

        # Verify
        assert data.Foo == foo_value_new
        assert data.bar == bar_value

    @given(st.text())
    def test_aws_attributes_with_a_default_value_can_be_updated(self, new_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        data.ValueWithDefault = new_value

        assert data.ValueWithDefault == new_value

    @given(st.text(), st.text())
    def test_internal_attributes_can_be_updated(self, old_value, new_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()
        data._internal_value = old_value

        data._internal_value = new_value

        assert data._internal_value == new_value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated_directly(self, old_value, new_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        # FIXME breaks because attrib is not known. we could either just look up pre-existing attributs on the object, or keep a dynamic list of valid AWS attributes for this object that gets updated by set_unknown_aws_attribute
        data.WeirdValue = new_value

        assert data.WeirdValue == new_value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated_via_explict_setter(self, old_value, new_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data.set_unknown_aws_attribute("WeirdValue", new_value)

        assert data.WeirdValue == new_value

    # Delete
    # ------

    @given(st.text(), st.text())
    def test_aws_attributes_can_be_deleted(self, foo_value, bar_value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        # Setup: set initial values
        data.Foo = foo_value
        data.bar = bar_value

        # Exercise
        del data.Foo
        del data.bar

        # Verify
        assert not hasattr(data, "Foo")
        assert not hasattr(data, "bar")

    def test_aws_attributes_with_a_default_value_can_be_deleted(self):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()

        del data.ValueWithDefault

        assert not hasattr(data, "ValueWithDefault")

    @given(st.text())
    def test_unknown_aws_attributes_can_be_deleted(self, value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()
        data.set_unknown_aws_attribute("WeirdValue", value)

        del data.WeirdValue

        assert not hasattr(data, "WeirdValue")

    @given(st.text())
    def test_internal_attributes_can_be_deleted(self, value):
        SimpleClass = self._create_simple_class()
        data = SimpleClass()
        data._internal_value = value

        del data._internal_value

        assert not hasattr(data, "_internal_value")
