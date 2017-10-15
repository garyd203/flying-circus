"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""


class TestYAMLOutput:
    """Verify YAML output."""
    pass


class TestAttributeAccess:
    """Verify behaviour of attributes on a Flying Circus AWS object"""

    def test_init_should_not_accept_positional_parameters(self):
        assert False

    def test_init_should_accept_named_parameters(self):
        assert False

    def test_init_should_have_named_parameters_in_spec(self):
        # TODO we don't want to simply do **kwargs plucking. we want named params for the benefit of autocomplete
        assert False

    def test_valid_aws_attributes_can_be_set(self):
        assert False

    def test_unknown_attributes_cannot_be_set_directly(self):
        assert False

    def test_unknown_attributes_can_be_set_by_special_function(self):
        # MOtivation nis to allow use of (older versions of ) flying circus when AWS bumps their interface spec and we havent caught up yet
        assert False

    def test_valid_aws_attributes_can_be_read(self):
        assert False

    def test_aws_attributes_cannot_be_read_if_they_are_not_set(self):
        assert False

    def test_aws_attributes_with_a_default_value_can_be_read_if_they_are_not_set(self):
        assert False

    def test_unknown_attributes_that_have_been_forcibly_set_can_be_read(self):
        assert False

    def test_aws_attributes_can_be_updated(self):
        assert False

    def test_unknown_attributes_that_have_been_forcibly_set_can_be_updated(self):
        # BY the same special access function and/or normal setattr
        assert False

    def test_aws_attributes_can_be_deleted(self):
        assert False

    def test_unknown_attributes_that_have_been_forcibly_set_can_be_deleted(self):
        assert False
