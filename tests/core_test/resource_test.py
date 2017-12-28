"""Tests for the Resource base class."""

import pytest

from flyingcircus.core import Resource

SIMPLE_RESOURCE_NAME = "NameSpace::Service::Resource"
SIMPLE_RESOURCE_PROPERTIES = {"props", "kudos"}


class SimpleResource(Resource):
    RESOURCE_TYPE = SIMPLE_RESOURCE_NAME
    RESOURCE_PROPERTIES = SIMPLE_RESOURCE_PROPERTIES


class TestResourceUnusualAttributes:
    """Verify special behaviour for some attributes on a CloudFormation Resource"""

    # Type
    # ----

    def test_type_attribute_always_exists_and_is_from_class_constant(self):
        data = SimpleResource()

        assert data.Type == SIMPLE_RESOURCE_NAME

    def test_type_cannot_be_set_in_constructor(self):
        with pytest.raises(TypeError) as excinfo:
            # noinspection PyArgumentList
            _ = SimpleResource(Type="CantSetThis")

        assert "Type" in str(excinfo.value)

    def test_type_cannot_be_set_as_attribute(self):
        data = SimpleResource()

        with pytest.raises(AttributeError):
            # noinspection PyPropertyAccess
            data.Type = "CantSetThis"

        assert data.Type == SIMPLE_RESOURCE_NAME

    def test_type_must_be_specified_in_concrete_class(self):
        class InvalidResource(Resource):
            # RESOURCE_TYPE = "SomethingSomething
            pass

        with pytest.raises(TypeError) as excinfo:
            _ = InvalidResource()

        error_message = str(excinfo.value)
        assert "RESOURCE_TYPE" in error_message \
               and "InvalidResource" in error_message

    # Metadata
    # --------

    def test_metadata_attribute_can_be_set_and_read(self):
        data = SimpleResource()

        foo_value = 'bar'
        data.Metadata = {'foo': foo_value}

        assert data.Metadata['foo'] is foo_value

    def test_metadata_cannot_be_set_in_constructor(self):
        with pytest.raises(TypeError) as excinfo:
            # noinspection PyArgumentList
            _ = SimpleResource(Metadata={"CantSetThis": "Nope"})

        assert "Metadata" in str(excinfo.value)

    # Resource-Specific Attributes
    # ----------------------------

    def test_creationpolicy_cannot_be_set_on_normal_resource(self):
        data = SimpleResource()

        with pytest.raises(AttributeError) as excinfo:
            data.CreationPolicy = "CantSetThis"

        assert "CreationPolicy" in str(excinfo.value)

    def test_updatepolicy_cannot_be_set_on_normal_resource(self):
        data = SimpleResource()

        with pytest.raises(AttributeError) as excinfo:
            data.UpdatePolicy = "CantSetThis"

        assert "UpdatePolicy" in str(excinfo.value)


class TestProperties:
    """Test the Properties attribute on a Resource."""

    def test_properties_attribute_always_exists(self):
        data = SimpleResource()

        assert hasattr(data, "Properties")
        assert data.Properties is not None

    def test_properties_has_attributes_from_resource_definition(self):
        data = SimpleResource()

        data.Properties.kudos = 1
        data.Properties.props = 'hello'
