"""Common base test classes and helper methods."""


class CommonAWSOBjectTests:
    """Shared tests to be applied to all AWSObject implementations."""
    def test_init_should_only_have_named_parameters_in_spec(self):
        # TODO we don't want to simply do **kwargs plucking. we want named params for the benefit of autocomplete
        assert False

    def test_get_logical_name_is_not_implemented_or_string(self):
        assert False
