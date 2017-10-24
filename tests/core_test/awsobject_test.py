"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""
import hypothesis.strategies as st
import inspect
import pytest
from hypothesis import given

from flyingcircus.core import AWSObject


class TestInitMethod:
    """Verify behaviour of the base AWSObject's constructor"""

    def test_init_should_not_accept_positional_parameters(self):
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                # NB: Make sure we exercise the __init__ in the base class!
                AWSObject.__init__(self, Foo)

        with pytest.raises(TypeError) as excinfo:
            _ = InitTestObject()

        assert "positional" in str(excinfo.value)

    def test_init_should_only_accept_kwargs(self):
        sig = inspect.signature(AWSObject.__init__)
        for param in sig.parameters.values():
            if param.name == 'self':
                continue
            assert param.kind == param.VAR_KEYWORD

    @given(st.text(), st.text(), st.text())
    def test_init_should_map_keyword_args_to_attributes(self, foo_value, default_value, bar_value):
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo", "ValueWithDefault", "Bar"}

            def __init__(self, Foo=None, ValueWithDefault=default_value, Bar=None):
                AWSObject.__init__(self, Foo=Foo, ValueWithDefault=ValueWithDefault, Bar=Bar)

        data = InitTestObject(foo_value, Bar=bar_value)

        assert data.Foo == foo_value
        assert data.ValueWithDefault == default_value
        assert data.Bar == bar_value

    @given(st.text())
    def test_init_should_only_accept_keyword_args_that_are_known_aws_attributes(self, value):
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                # NB: Make sure we exercise the __init__ in the base class!
                AWSObject.__init__(self, Foo=Foo, SomeUnknownAttribute=value)

        with pytest.raises(TypeError) as excinfo:
            _ = InitTestObject()

        assert "SomeUnknownAttribute" in str(excinfo.value)

    def test_init_should_ignore_keyword_parameters_that_are_none(self):
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                AWSObject.__init__(self, Foo=Foo)

        data = InitTestObject()

        assert not hasattr(data, "Foo")


class TestExport:
    """Verify behaviour of the export method"""

    VALID_EXPORT_FORMATS = {"yaml"}

    @pytest.mark.parametrize('format', VALID_EXPORT_FORMATS)
    def test_valid_export_methods_produce_a_result(self, format):
        data = AWSObject()

        output = data.export(format)

        assert output is not None

    @given(st.text().filter(lambda x: x not in TestExport.VALID_EXPORT_FORMATS))
    def test_invalid_export_methods_cause_an_error(self, format):
        data = AWSObject()

        with pytest.raises(ValueError) as excinfo:
            data.export(format)

        assert format in str(excinfo.value)


class TestAttributeAccess:
    """Verify behaviour of attributes on a Flying Circus AWS object"""

    # TODO dict access for aws attributes only
    # TODO test deleting nonexistent attributes of various sorts
    # TODO verify behaviour of set_unknown_aws_attribute with known/internal attribute
    # TODO consider why we have default values set in the concrete classes? What is the value of passing these through, rather than setting no value and having it fall through to AWS? Documentation is nice, and consistency is nice (if aws defaults change), and explicit is better than implicit, but it just feels that we are doing something that shouldn't be our business.

    class SimpleObject(AWSObject):
        """Simple AWS object for testing attribute access"""
        AWS_ATTRIBUTES = {"Foo", "bar", "ValueWithDefault"}

        def __init__(self, Foo=None, bar=None, ValueWithDefault=42):
            AWSObject.__init__(self, Foo=Foo, bar=bar, ValueWithDefault=ValueWithDefault)

    # Set and Read
    # ------------

    @given(st.text(), st.text())
    def test_valid_aws_attributes_can_be_set_and_read(self, foo_value, bar_value):
        data = self.SimpleObject()

        data.Foo = foo_value
        data.bar = bar_value

        assert hasattr(data, "Foo")
        assert data.Foo == foo_value
        assert hasattr(data, "bar")
        assert data.bar == bar_value

    @given(st.text())
    def test_internal_attributes_can_be_set_and_read(self, value):
        data = self.SimpleObject()

        data._internal_value = value

        assert hasattr(data, "_internal_value")
        assert data._internal_value == value

    def test_unknown_attributes_cannot_be_set_directly(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            data.WeirdValue = "hello"
        assert "WeirdValue" in str(excinfo.value)
        assert not hasattr(data, "WeirdValue")

    @given(st.text())
    def test_unknown_aws_attributes_can_be_explicitly_set_and_read_normally(self, value):
        data = self.SimpleObject()

        data.set_unknown_aws_attribute("WeirdValue", value)

        assert hasattr(data, "WeirdValue")
        assert data.WeirdValue == value

    def test_valid_aws_attributes_cannot_be_explicitly_set(self):
        data = self.SimpleObject()

        data.set_unknown_aws_attribute("WeirdValue", "hello")
        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("bar", "hello")
        assert "bar" in str(excinfo.value)
        assert not hasattr(data, "bar")

    # Read Special Cases
    # ------------------

    def test_aws_attributes_cannot_be_read_before_they_are_set(self):
        data = self.SimpleObject()

        assert not hasattr(data, "Foo")

    def test_aws_attributes_with_a_default_value_can_be_read_before_they_are_set(self):
        data = self.SimpleObject()

        assert hasattr(data, "ValueWithDefault")
        assert data.ValueWithDefault == 42

    # Update
    # ------

    @given(st.text(), st.text(), st.text())
    def test_aws_attributes_can_be_updated(self, foo_value_old, foo_value_new, bar_value):
        data = self.SimpleObject()

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
        data = self.SimpleObject()

        data.ValueWithDefault = new_value

        assert data.ValueWithDefault == new_value

    @given(st.text(), st.text())
    def test_internal_attributes_can_be_updated(self, old_value, new_value):
        data = self.SimpleObject()
        data._internal_value = old_value

        data._internal_value = new_value

        assert data._internal_value == new_value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated_directly(self, old_value, new_value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        # FIXME breaks because attrib is not known. we could either just look up pre-existing attributs on the object, or keep a dynamic list of valid AWS attributes for this object that gets updated by set_unknown_aws_attribute
        data.WeirdValue = new_value

        assert data.WeirdValue == new_value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated_via_explict_setter(self, old_value, new_value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data.set_unknown_aws_attribute("WeirdValue", new_value)

        assert data.WeirdValue == new_value

    # Delete
    # ------

    @given(st.text(), st.text())
    def test_aws_attributes_can_be_deleted(self, foo_value, bar_value):
        data = self.SimpleObject()

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
        data = self.SimpleObject()

        del data.ValueWithDefault

        assert not hasattr(data, "ValueWithDefault")

    @given(st.text())
    def test_unknown_aws_attributes_can_be_deleted(self, value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        del data.WeirdValue

        assert not hasattr(data, "WeirdValue")

    @given(st.text())
    def test_internal_attributes_can_be_deleted(self, value):
        data = self.SimpleObject()
        data._internal_value = value

        del data._internal_value

        assert not hasattr(data, "_internal_value")
