"""Test enhanced S3 Bucket functionality."""
import pytest

from flyingcircus.service.s3 import Bucket


class TestVersioning(object):
    """Verify the behaviour of the `Bucket.versioning` property"""

    #: Valid values for the CloudFormation property "VersioningConfiguration.Status"
    STATUS_VALUES = [
        ("Enabled", True),
        ("Suspended", False),
    ]

    def test_should_be_false_when_no_property_is_set(self):
        bucket = Bucket()
        assert bucket.versioning is False

    @pytest.mark.parametrize(("status", "is_enabled"), STATUS_VALUES)
    def test_should_get_value_from_underlying_property(self, status, is_enabled):
        bucket = Bucket(Properties=dict(
            VersioningConfiguration=dict(
                Status=status,
            ),
        ))

        assert bucket.versioning is is_enabled

    def test_get_should_raise_error_when_existing_property_is_invalid(self):
        bucket = Bucket(Properties=dict(
            VersioningConfiguration=dict(
                Status="ItsComplicated",
            ),
        ))

        with pytest.raises(ValueError, match=r"ItsComplicated"):
            _ = bucket.versioning

    @pytest.mark.parametrize(("status", "is_enabled"), STATUS_VALUES)
    def test_should_set_underlying_property(self, status, is_enabled):
        bucket = Bucket()
        bucket.versioning = is_enabled

        assert bucket["Properties"]["VersioningConfiguration"]["Status"] == status

    def test_set_should_override_existing_property(self):
        # Setup
        bucket = Bucket(Properties=dict(
            VersioningConfiguration=dict(
                Status="Suspended",
            ),
        ))

        # Exercise
        bucket.versioning = True

        # Verify
        assert bucket["Properties"]["VersioningConfiguration"]["Status"] == "Enabled"
