"""Common base test classes and helper methods."""


class CommonAWSOBjectTests:
    """Shared tests to be applied to all AWSObject implementations."""

    def test_get_logical_name_is_not_implemented_or_string(self):
        assert False
