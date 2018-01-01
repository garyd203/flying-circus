"""Common base test classes and helper methods."""

import hypothesis.strategies as st

from flyingcircus.core import AWSObject


class CommonAWSObjectTests:
    """Shared tests to be applied to all AWSObject implementations."""

    def test_init_should_only_have_named_parameters_in_spec(self):
        # TODO we don't want to simply do **kwargs plucking. we want named params for the benefit of autocomplete
        assert False

    def test_get_logical_name_is_not_implemented_or_string(self):
        assert False


class ZeroAttributeObject(AWSObject):
    """Test object with no attributes.

    This is the same as using AWSObject directly, but naming it explicitly
    makes the test's intention clearer.
    """
    pass


class SingleAttributeObject(AWSObject):
    """Test object with 1 attribute"""
    AWS_ATTRIBUTES = {"one"}

    def __init__(self, one=None):
        AWSObject.__init__(self, one=one)


class DualAttributeObject(AWSObject):
    """Test object with 2 attributes"""
    AWS_ATTRIBUTES = {"one", "two"}

    def __init__(self, one=None, two=None):
        AWSObject.__init__(self, one=one, two=two)


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
    attributes = draw(st.sets(st.text()))

    class HypothesisedAWSObject(AWSObject):
        AWS_ATTRIBUTES = attributes

    return draw(st.builds(HypothesisedAWSObject, **{name: aws_attribute_strategy() for name in attributes}))
