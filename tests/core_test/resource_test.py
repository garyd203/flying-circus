"""Tests for the Resource base class."""

import importlib

import hypothesis.strategies as st
import pytest
from attr import attrib
from attr import attrs
from hypothesis import given

from flyingcircus.core import ATTRSCONFIG
from flyingcircus.core import LogicalName
from flyingcircus.core import Parameter
from flyingcircus.core import Resource
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from .common import BaseTaggingTest
from .common import FullResource
from .common import SimpleResource
from .common import SimpleResourceProperties
from .common import TaggableResource
from .common import parametrize_tagging_techniques
from ..pyyaml_helper import create_refsafe_dumper


class TestResourceSpecialAttributes:
    """Verify special behaviour for some attributes on a CloudFormation Resource"""

    # Sorting
    # -------
    def test_attributes_are_sorted_in_custom_order(self):
        # Setup
        data = FullResource()

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ["Type", "DependsOn", "Metadata", "CreationPolicy", "UpdatePolicy", "DeletionPolicy",
                                 "Properties"]

    # Type
    # ----

    def test_type_attribute_always_exists_and_is_from_class_constant(self):
        data = SimpleResource()

        assert data.Type == SimpleResource.RESOURCE_TYPE

    def test_type_cannot_be_set(self):
        data = SimpleResource()

        with pytest.raises(AttributeError):
            # noinspection PyPropertyAccess
            data.Type = "CantSetThis"

        assert data.Type == SimpleResource.RESOURCE_TYPE

    def test_type_must_be_specified_in_concrete_class(self):
        @attrs(**ATTRSCONFIG)
        class BrokenResourceClass(Resource):
            # RESOURCE_TYPE = "NameSpace::Service::Resource"
            Properties: SimpleResourceProperties = attrib(factory=SimpleResourceProperties)

        with pytest.raises(TypeError, match=r"BrokenResourceClass.*RESOURCE_TYPE"):
            _ = BrokenResourceClass()

    def test_type_is_included_in_iterator(self):
        data = SimpleResource()

        # Exercise
        attribs = iter(data)

        # Verify
        assert "Type" in set(attribs)
        assert len(data) == 5

    # Properties
    # ----------

    def test_properties_must_be_specified_in_concrete_class(self):
        @attrs(**ATTRSCONFIG)
        class BrokenResourceClass(Resource):
            RESOURCE_TYPE = "NameSpace::Service::Resource"
            # Properties: SimpleResourceProperties = attrib(factory=SimpleResourceProperties)

        with pytest.raises(TypeError, match=r"BrokenResourceClass.*Properties"):
            _ = BrokenResourceClass()

    # Metadata
    # --------

    def test_metadata_cannot_be_set_in_constructor(self):
        with pytest.raises(TypeError, match=r"Metadata"):
            # noinspection PyArgumentList
            _ = SimpleResource(Metadata={"CantSetThis": "Nope"})

    # Optional Attributes
    # -------------------

    @pytest.mark.parametrize("fieldname", [
        "CreationPolicy",
        "UpdatePolicy",
    ])
    def test_optional_attribute_does_not_exist_on_standard_resource(self, fieldname):
        # Setup
        data = SimpleResource()

        # Exercise & Verify
        with pytest.raises(AttributeError, match=fieldname):
            setattr(data, fieldname, "CantSetThis")

        with pytest.raises(AttributeError, match=fieldname):
            _ = getattr(data, fieldname)

        assert fieldname not in list(iter(data))

    def test_optional_attributes_are_included_in_iterator(self):
        # Setup
        data = FullResource()

        # Exercise
        attribs = set(iter(data))

        # Verify
        assert "CreationPolicy" in attribs
        assert "UpdatePolicy" in attribs
        assert len(data) == 7


class TestGetTag(BaseTaggingTest):
    """Test simplified tag retrieval with get_tag()."""

    def test_return_value_of_tag(self):
        # Setup
        key = "SomeTag"
        value = "To be or not to be"
        res = TaggableResource()
        res.tag({key: value, "SomethingElse": "42"})

        # Exercise & Verify
        assert res.get_tag(key) == value

    def test_return_none_when_tag_not_set(self):
        # Setup
        res = TaggableResource()
        res.tag({"SomethingElse": "42"})

        # Exercise & Verify
        assert res.get_tag("MissingKey") is None

    def test_return_none_when_no_tags_set(self):
        # Setup
        res = TaggableResource()

        # Exercise & Verify
        assert res.get_tag("MissingKey") is None

    def test_throws_error_when_untaggable(self):
        # Setup
        res = SimpleResource()

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

        res = TaggableResource()

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

        res = TaggableResource()
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

        res = TaggableResource()
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
        res = SimpleResource()

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
        res = TaggableResource()
        res.tag(Name=name)

        # Exercise & Verify
        assert res.name == name

    def test_sets_name_tag(self):
        # Setup
        name = "Some extraordinary name"
        res = TaggableResource()

        # Exercise
        res.name = name

        # Verify
        assert res.get_tag("Name") == name

    def test_set_throws_error_when_untaggable(self):
        # Setup
        res = SimpleResource()

        # Exercise & Verify
        with pytest.raises(AttributeError):
            res.name = "Can't touch this"

    @pytest.mark.parametrize(
        "name",
        [
            "cognito.UserPool",
            "ecs.TaskDefinition",
            # "kms.Key",
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


class TestLogicalName:
    """Test behaviour/output of the LogicalName function."""

    @given(st.text(min_size=1))
    def test_uses_logical_name_from_stack(self, name):
        # Setup
        data = SimpleResource(Properties={"props": 42})
        stack = Stack(Resources={name: data})
        ref = LogicalName(data)

        dumper = create_refsafe_dumper(stack)

        # Exercise
        node = ref.as_yaml_node(dumper)

        # Verify
        assert node.value == name

    def test_stack_yaml_output(self):
        """An integration test, yay!"""
        # Setup
        data = SimpleResource(Properties={"props": 42})
        stack = Stack(Resources=dict(Foo=data, Bar=LogicalName(data)))
        del stack.Metadata

        # Exercise
        output = stack.export("yaml")

        # Verify
        assert output == dedent("""
            ---
            AWSTemplateFormatVersion: '2010-09-09'
            Resources:
              Bar: Foo
              Foo:
                Type: NameSpace::Service::SimpleResource
                Properties:
                  props: 42
            """)

    def test_non_resource_cannot_be_found(self):
        # Setup
        name = "Foo"
        param = Parameter(Type="String", Default="Hello world")
        stack = Stack(Parameters={name: param})
        ref = LogicalName(param)

        dumper = create_refsafe_dumper(stack)

        # Exercise & Verify
        with pytest.raises(ValueError, match="Parameter"):
            _ = ref.as_yaml_node(dumper)
