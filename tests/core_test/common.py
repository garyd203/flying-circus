"""Common base test classes and helper methods."""

import hypothesis.strategies as st
import pytest
from attr import attrib
from attr import attrs

from flyingcircus.core import AWSObject
from flyingcircus.core import Resource


class CommonAWSObjectTests:
    """Shared tests to be applied to all AWSObject implementations."""

    def test_init_should_only_have_named_parameters_in_spec(self):
        # TODO we don't want to simply do **kwargs plucking. we want named params for the benefit of autocomplete
        assert False

    def test_get_logical_name_is_not_implemented_or_string(self):
        assert False


@attrs(**AWSObject.ATTR_ARGS)
class ZeroAttributeObject(AWSObject):
    """Test object with no attributes.

    This is the same as using AWSObject directly, but naming it explicitly
    makes the test's intention clearer.
    """
    pass


@attrs(**AWSObject.ATTR_ARGS)
class SingleAttributeObject(AWSObject):
    """Test object with 1 attribute"""
    one = attrib(default=None)


@attrs(**AWSObject.ATTR_ARGS)
class DualAttributeObject(AWSObject):
    """Test object with 2 attributes"""
    one = attrib(default=None)
    two = attrib(default=None)


@attrs(**AWSObject.ATTR_ARGS)
class MixedAttributeObject(AWSObject):
    """Test object with AWS attributes and internal attributes"""
    one = attrib(default=None)
    two = attrib(default=None)
    _a = attrib(default=None)
    _b = attrib(default=None)


@st.composite
def aws_attribute_strategy(draw):
    """A strategy that produces an attribute for an AWS CFN object."""
    return draw(st.one_of(
        st.text(),
        st.integers(),
        st.floats(),
        st.booleans(),
        st.dictionaries(st.text(), st.text()),
        aws_object_strategy(),
    ))


@st.composite
def aws_object_strategy(draw):
    """A strategy that produces an AWS CFN object."""
    attributes = draw(st.sets(aws_logical_name_strategy()))

    @attrs(
        these={name: attrib(default=None) for name in attributes},
        **AWSObject.ATTR_ARGS
    )
    class HypothesisedAWSObject(AWSObject):
        pass

    return draw(st.builds(HypothesisedAWSObject, **{name: aws_attribute_strategy() for name in attributes}))


@st.composite
def aws_logical_name_strategy(draw):
    """A strategy that produces a valid logical name for an AWS Stack object"""
    return draw(st.builds(
        lambda a, b: a + b,
        st.text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=1),
        st.text("abcdefghijklmnnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"),
    ))


SIMPLE_RESOURCE_NAME = "NameSpace::Service::Resource"
SIMPLE_RESOURCE_PROPERTIES = {"props", "kudos"}


class SimpleResource(Resource):
    RESOURCE_TYPE = SIMPLE_RESOURCE_NAME
    RESOURCE_PROPERTIES = SIMPLE_RESOURCE_PROPERTIES


LOREM_IPSUM = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum."""


class BaseTaggingTest:
    """Base class for testing tagging on AWS Objects"""

    # Helper Methods
    # --------------

    def verify_tag_doesnt_exist(self, res, key, value):
        if not hasattr(res, "Properties") \
                or not hasattr(res.Properties, "Tags"):
            return
        for tag in getattr(res.Properties, "Tags", []):
            assert not (tag["Key"] == key and tag["Value"] == value)

    def verify_tag_exists(self, res, key, value):
        for tag in res.Properties.Tags:
            if tag["Key"] == key and tag["Value"] == value:
                return

        assert False, "Tag not found in resource"


def parametrize_tagging_techniques():
    """Decorator that parametrizes tests across the two techniques of applying tags."""

    return pytest.mark.parametrize(
        argnames='apply_tags',
        argvalues=[
            lambda res, key, value: res.tag({key: value}),
            lambda res, key, value: res.tag(**{key: value}),
        ],
        ids=[
            "dict",
            "keywords"
        ],
    )
