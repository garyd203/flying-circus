"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""
import hypothesis.strategies as st
import inspect
import pytest
from hypothesis import given

from flyingcircus.core import AWSObject
from .common import SingleAttributeObject
from .common import ZeroAttributeObject


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
        data = ZeroAttributeObject()

        output = data.export(format)

        assert output is not None

    @given(st.text().filter(lambda x: x not in TestExport.VALID_EXPORT_FORMATS))
    def test_invalid_export_methods_cause_an_error(self, format):
        data = ZeroAttributeObject()

        with pytest.raises(ValueError) as excinfo:
            data.export(format)

        assert format in str(excinfo.value)


class TestAttributeAccess:
    """Verify behaviour of attributes on a Flying Circus AWS object"""

    class SimpleObject(AWSObject):
        """Simple AWS object for testing attribute access"""
        AWS_ATTRIBUTES = {"Foo", "bar"}

        def __init__(self, Foo=None, bar=None):
            AWSObject.__init__(self, Foo=Foo, bar=bar)

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

        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("bar", "hello")

        assert "bar" in str(excinfo.value)
        assert not hasattr(data, "bar")

    def test_internal_attributes_cannot_be_explicitly_set(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("_internal_value", "hello")

        assert "_internal_value" in str(excinfo.value)
        assert not hasattr(data, "_internal_value")

    # Set Special Cases
    # -----------------

    def test_attribute_can_be_set_to_none(self):
        """An attribute can be set to None, although
        it can't be initialised to None in the constructor.
        """
        # Setup
        data = self.SimpleObject()
        assert not hasattr(data, "Foo")

        # Exercise
        data.Foo = None

        # Verify
        assert hasattr(data, "Foo")
        assert data.Foo is None

    # Read Special Cases
    # ------------------

    def test_aws_attributes_cannot_be_read_before_they_are_set(self):
        data = self.SimpleObject()

        assert not hasattr(data, "Foo")

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

        data.WeirdValue = new_value

        assert data.WeirdValue == new_value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated_via_explicit_setter(self, old_value, new_value):
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

    @given(st.text())
    def test_internal_attributes_can_be_deleted(self, value):
        data = self.SimpleObject()
        data._internal_value = value

        del data._internal_value

        assert not hasattr(data, "_internal_value")

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

    def test_delete_nonexistent_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data.DoesNotExist

        assert "DoesNotExist" in str(excinfo.value)

    def test_delete_unset_aws_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data.Foo

        assert "Foo" in str(excinfo.value)

    def test_delete_nonexistent_internal_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data._internal_value

        assert "_internal_value" in str(excinfo.value)

    @given(st.text())
    def test_delete_already_deleted_unknown_aws_attribute_raises_error(self, value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", value)
        del data.WeirdValue

        with pytest.raises(AttributeError) as excinfo:
            del data.WeirdValue

        assert "WeirdValue" in str(excinfo.value)


class TestDictionaryAccess:
    """Verify behaviour of dictionary access to attributes on a Flying Circus AWS object"""

    # CRUD Access for AWS Attributes
    # ------------------------------

    @given(st.text())
    def test_aws_attributes_can_be_set(self, value):
        data = SingleAttributeObject()

        data["one"] = value

        assert hasattr(data, "one")
        assert data.one == value

    @given(st.text())
    def test_aws_attributes_can_be_read(self, value):
        data = SingleAttributeObject(one=value)

        assert data["one"] == value

    @given(st.text(), st.text())
    def test_aws_attributes_can_be_updated(self, old_value, new_value):
        data = SingleAttributeObject(one=old_value)

        data["one"] = new_value

        assert data["one"] == new_value
        assert data.one == new_value

    @given(st.text())
    def test_aws_attributes_can_be_deleted(self, value):
        data = SingleAttributeObject(one=value)

        del data["one"]

        assert not hasattr(data, "one")

    def test_unset_aws_attributes_cannot_be_read(self):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            _ = data["one"]

        assert "one" in str(excinfo.value)

    def test_unset_aws_attributes_cannot_be_deleted(self):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            del data["one"]

        assert "one" in str(excinfo.value)

    # CRUD Access For Internal Attributes
    # -----------------------------------

    @given(st.text())
    def test_internal_attributes_cannot_be_set(self, value):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            data["_internal_value"] = value

        assert "_internal_value" in str(excinfo.value)

    @given(st.text())
    def test_internal_attributes_cannot_be_read(self, value):
        data = SingleAttributeObject()
        data._internal_value = value

        with pytest.raises(KeyError) as excinfo:
            _ = data["_internal_value"]

        assert "_internal_value" in str(excinfo.value)

    @given(st.text(), st.text())
    def test_internal_attributes_cannot_be_updated(self, old_value, new_value):
        data = SingleAttributeObject()
        data._internal_value = old_value

        with pytest.raises(KeyError) as excinfo:
            data["_internal_value"] = new_value

        assert "_internal_value" in str(excinfo.value)
        assert data._internal_value == old_value

    @given(st.text())
    def test_internal_attributes_cannot_be_deleted(self, value):
        data = SingleAttributeObject()
        data._internal_value = value

        with pytest.raises(KeyError) as excinfo:
            _ = data["_internal_value"]

        assert "_internal_value" in str(excinfo.value)
        assert data._internal_value == value

    # CRUD Access For Unknown AWS Attributes
    # --------------------------------------

    @given(st.text())
    def test_unknown_aws_attributes_cannot_be_set(self, value):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            data["WeirdValue"] = value

        assert "WeirdValue" in str(excinfo.value)

    @given(st.text())
    def test_unknown_aws_attributes_can_be_read(self, value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        assert data["WeirdValue"] == value

    @given(st.text(), st.text())
    def test_unknown_aws_attributes_can_be_updated(self, old_value, new_value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data["WeirdValue"] = new_value

        assert data["WeirdValue"] == new_value
        assert data.WeirdValue == new_value

    @given(st.text())
    def test_unknown_aws_attributes_can_be_deleted(self, value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        del data["WeirdValue"]

        assert not hasattr(data, "WeirdValue")
