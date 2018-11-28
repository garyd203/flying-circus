"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""

import hypothesis.strategies as st
import pytest
from attr import attrib
from attr import attrs
from hypothesis import given

from flyingcircus.core import ATTRSCONFIG
from flyingcircus.core import AWSObject
from .common import DualAttributeObject
from .common import MixedAttributeObject
from .common import NestedAttributeObject
from .common import SingleAttributeObject
from .common import ZeroAttributeObject
from .common import aws_attribute_strategy


class TestInitMethod:
    """Verify behaviour of the base AWSObject's constructor"""

    def test_init_should_not_accept_positional_parameters(self):
        with pytest.raises(TypeError, match="positional"):
            _ = SingleAttributeObject(42)

    def test_init_should_not_accept_parameters_that_are_internal_attributes(self):
        @attrs(**ATTRSCONFIG)
        class InitTestObject(AWSObject):
            aws_attribute: int = attrib(default=None)
            _internal_attribute: int = attrib(default=None, init=False)

        with pytest.raises(TypeError, match="internal_attribute"):
            _ = InitTestObject(internal_attribute=42)

    def test_init_should_convert_dict_values_to_object_attributes(self):
        # Exercise
        data = NestedAttributeObject(top=dict(one=42))

        # Verify
        assert isinstance(data.top, SingleAttributeObject)
        assert data.top.one == 42


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
    """Verify behaviour of attributes on a Flying Circus AWS object.

    Most behaviour is implemented with `attrs`, so we just need to validate
    some corner-cases and configuration.
    """

    def test_unknown_attributes_cannot_be_set(self):
        data = ZeroAttributeObject()

        with pytest.raises(AttributeError, match="WeirdValue"):
            data.WeirdValue = "hello"
        assert not hasattr(data, "WeirdValue")

    def test_dict_values_should_be_converted_to_objects(self):
        data = NestedAttributeObject()

        # Exercise
        data.top = {"one": 42}

        # Verify
        assert isinstance(data.top, SingleAttributeObject)
        assert data.top.one == 42


class TestDictionaryAccess:
    """Verify behaviour of dictionary access to attributes on a Flying Circus AWS object"""

    # CRUD Access for AWS Attributes
    # ------------------------------

    @given(aws_attribute_strategy())
    def test_aws_attributes_can_be_set(self, value):
        data = SingleAttributeObject()

        data["one"] = value

        assert hasattr(data, "one")
        assert data.one is value

    @given(aws_attribute_strategy())
    def test_aws_attributes_can_be_read(self, value):
        data = SingleAttributeObject(one=value)

        assert data["one"] is value

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_aws_attributes_can_be_updated(self, old_value, new_value):
        data = SingleAttributeObject(one=old_value)

        data["one"] = new_value

        assert data["one"] is new_value
        assert data.one is new_value

    # CRUD Access For Internal Attributes
    # -----------------------------------

    @given(st.text())
    def test_internal_attributes_cannot_be_set(self, value):
        data = MixedAttributeObject()

        with pytest.raises(KeyError, match="_a") as excinfo:
            data["_a"] = value

    @given(st.text())
    def test_internal_attributes_cannot_be_read(self, value):
        data = MixedAttributeObject(a=value)

        with pytest.raises(KeyError, match="_a") as excinfo:
            _ = data["_a"]


class TestIteratorAccess:
    """Verify behaviour of attribute iteration on a Flying Circus AWS object.

    Note that attribute length is highly coupled functionality, so we verify
    the behaviour of both `__iter__` and `__len__` together.
    """

    def test_object_iteration_returns_attribute_names(self):
        # Setup
        data = DualAttributeObject(one=42, two='hello world')

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_includes_attributes_set_to_none(self):
        # Setup
        data = DualAttributeObject(one=42)
        data.two = None

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_includes_attributes_set_to_an_empty_object(self):
        # Setup
        data = DualAttributeObject(one=42, two={})

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_excludes_internal_attributes(self):
        # Setup
        data = MixedAttributeObject(one=42, two='hello world', a="nope")

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_sorts_in_order_of_declaration(self):
        @attrs(**ATTRSCONFIG)
        class OrderedObject(AWSObject):
            b = attrib()
            a = attrib()

        # Setup
        data = OrderedObject(a=42, b='hello world')

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b', 'a']
        assert len(data) == 2
