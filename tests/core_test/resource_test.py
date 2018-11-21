"""Tests for the Resource base class."""

import importlib

import pytest

from flyingcircus.core import Resource
from .common import BaseTaggingTest
from .common import SIMPLE_RESOURCE_NAME
from .common import SimpleResource
from .common import parametrize_tagging_techniques


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


class _UntaggableResource(Resource):
    RESOURCE_TYPE = "NameSpace::Service::UntaggableResource"
    RESOURCE_PROPERTIES = {"SomeProperty", "AnotherProperty"}


class _TaggableResource(Resource):
    RESOURCE_TYPE = "NameSpace::Service::TaggableResource"
    RESOURCE_PROPERTIES = {"SomeProperty", "AnotherProperty", "Tags"}


class TestGetTag(BaseTaggingTest):
    """Test simplified tag retrieval with get_tag()."""

    def test_return_value_of_tag(self):
        # Setup
        key = "SomeTag"
        value = "To be or not to be"
        res = _TaggableResource()
        res.tag({key: value, "SomethingElse": "42"})

        # Exercise & Verify
        assert res.get_tag(key) == value

    def test_return_none_when_tag_not_set(self):
        # Setup
        res = _TaggableResource()
        res.tag({"SomethingElse": "42"})

        # Exercise & Verify
        assert res.get_tag("MissingKey") is None

    def test_return_none_when_no_tags_set(self):
        # Setup
        res = _TaggableResource()

        # Exercise & Verify
        assert res.get_tag("MissingKey") is None

    def test_throws_error_when_untaggable(self):
        # Setup
        res = _UntaggableResource()

        # Exercise & Verify
        with pytest.raises(AttributeError) as excinfo:
            _ = res.name

        assert "not supported" in str(excinfo.value)


class TestTagging(BaseTaggingTest):
    """Test automatic tagging for Resource objects."""

    # TODO test cases:
    #   for tags and more_tags:
    #       - key is not a string
    #       - value is not a string
    #       - key is a crazy-but-acceptable string (use hypothesis)
    #       - value is a crazy-but-acceptable string (use hypothesis)
    #       - key has wrong length or invalid characters
    #       - value has wrong length or invalid characters
    #   same key and same value appears in both tags and more_tags
    #   same key and different value appears n both tags and more_tags
    #   tag_derived_resources behaviour. Need specific implementation
    #   Resource is a Stack Resource => we should tag it's children
    # TODO look up the weird resources that have unusual tag syntax (eg. ASG)
    # TODO look up the resources that have an unusual name for Tag property

    @parametrize_tagging_techniques()
    def test_tag_is_added_to_properties(self, apply_tags):
        # Setup
        key = "foo"
        value = "bar"

        res = _TaggableResource()

        # Exercise
        tagged = apply_tags(res, key, value)

        # Verify
        assert tagged
        self.verify_tag_exists(res, key, value)

    @parametrize_tagging_techniques()
    def test_tag_is_added_to_existing_tags(self, apply_tags):
        # Setup
        key1 = "existing"
        value1 = "frobnicate"
        key2 = "foo"
        value2 = "bar"

        res = _TaggableResource()
        res.Properties.Tags = [{"Key": key1, "Value": value1}]

        # Exercise
        tagged = apply_tags(res, key2, value2)

        # Verify
        assert tagged
        self.verify_tag_exists(res, key1, value1)
        self.verify_tag_exists(res, key2, value2)

    @parametrize_tagging_techniques()
    def test_tag_replaces_existing_tag_with_same_key(self, apply_tags):
        # Setup
        key1 = "existing"
        old_value = "frobnicate"
        key2 = "foo"
        value2 = "bar"
        new_value = "new"

        res = _TaggableResource()
        res.Properties.Tags = [
            {"Key": key1, "Value": old_value},
            {"Key": key2, "Value": value2},
        ]

        # Exercise
        tagged = apply_tags(res, key1, new_value)

        # Verify
        assert tagged
        self.verify_tag_doesnt_exist(res, key1, old_value)
        self.verify_tag_exists(res, key1, new_value)
        self.verify_tag_exists(res, key2, value2)

    def test_resource_doesnt_support_tagging(self):
        # Setup
        res = _UntaggableResource()

        # Exercise
        tagged = res.tag(foo="bar")

        # Verify
        assert not tagged

    @pytest.mark.parametrize(
        "name",
        [
            "cognito.UserPool",
        ],
    )
    @parametrize_tagging_techniques()
    def test_resource_with_nonstandard_tag_property_is_supported(self, name: str, apply_tags: callable):
        # Setup: Create a resource of this type
        modulename, classname = name.rsplit(".", 1)
        module = importlib.import_module("flyingcircus.service." + modulename)
        res = getattr(module, classname)()

        # Exercise
        tags_supported = apply_tags(res, "Foo", "1")
        apply_tags(res, "Bar", "2")
        apply_tags(res, "Bar", "3")

        # Verify
        assert tags_supported is True
        assert res.is_taggable is True, "This resource type should be taggable"
        assert res.get_tag("Foo") == "1", "Tags should be saved on the resource"
        assert res.get_tag("Bar") == "3", "Tags should be updated on the resource"
        assert not hasattr(res.Properties, "Tags"), "Tags should not be stored on the 'Tags' property"


class TestNameAccess:
    """Test automatic name access for Resource objects.

    The standard implementation simply calls `tag` and `set_tag`, so we take
    a light touch with the testing.
    """

    def test_fetches_name_tag(self):
        # Setup
        name = "Some extraordinary name"
        res = _TaggableResource()
        res.tag(Name=name)

        # Exercise & Verify
        assert res.name == name

    def test_sets_name_tag(self):
        # Setup
        name = "Some extraordinary name"
        res = _TaggableResource()

        # Exercise
        res.name = name

        # Verify
        assert res.get_tag("Name") == name

    def test_set_throws_error_when_untaggable(self):
        # Setup
        res = _UntaggableResource()

        # Exercise & Verify
        with pytest.raises(AttributeError):
            res.name = "Can't touch this"

    @pytest.mark.parametrize(
        "name",
        [
            "cognito.UserPool",
            "rds.DBInstance",
            "secretsmanager.Secret",
        ],
    )
    def test_resource_with_nonstandard_name_is_supported(self, name: str):
        # Setup: Create a resource of this type
        modulename, classname = name.rsplit(".", 1)
        module = importlib.import_module("flyingcircus.service." + modulename)
        res = getattr(module, classname)()

        name = "Some extraordinary name"

        # Exercise
        res.name = name

        # Verify
        assert res.name == name
