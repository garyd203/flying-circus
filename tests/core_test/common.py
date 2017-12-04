"""Common base test classes and helper methods."""

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
