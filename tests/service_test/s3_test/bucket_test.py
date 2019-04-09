"""Test enhanced S3 Bucket functionality."""

import pytest

from flyingcircus.service.s3 import Bucket


class TestEncryption(object):
    """Verify the behaviour of the `set_encryption` helper function."""

    def _verify_has_kms_encryption(self, bucket: Bucket, keyid):
        """Verify that this bucket has KMS-managed encryption with the specified key."""
        encryption_rules = bucket.Properties["BucketEncryption"][
            "ServerSideEncryptionConfiguration"
        ]
        assert (
            len(encryption_rules) == 1
        ), "There should only be one ServerSideEncryptionRule"

        sse_config = encryption_rules[0]["ServerSideEncryptionByDefault"]
        assert sse_config["SSEAlgorithm"] == "aws:kms"
        assert sse_config["KMSMasterKeyID"] == keyid

    def _verify_has_s3_encryption(self, bucket: Bucket):
        """Verify that this bucket has S3-managed encryption"""
        encryption_rules = bucket.Properties["BucketEncryption"][
            "ServerSideEncryptionConfiguration"
        ]
        assert (
            len(encryption_rules) == 1
        ), "There should only be one ServerSideEncryptionRule"

        sse_config = encryption_rules[0]["ServerSideEncryptionByDefault"]
        assert sse_config["SSEAlgorithm"] == "AES256"
        assert "KMSMasterKeyID" not in sse_config

    def test_sets_kms_encryption_with_default_key_when_no_parameters_set(self):
        bucket = Bucket()

        bucket.set_encryption()

        self._verify_has_kms_encryption(bucket, "aws/s3")

    def test_sets_kms_encryption_with_specified_key(self):
        bucket = Bucket()
        keyid = "arn:aws:kms:us-east-1:123456789012:key/52a6b44c-8840-41e3-86cd-78cbb022af5e"

        bucket.set_encryption(kms_keyid=keyid)

        self._verify_has_kms_encryption(bucket, keyid)

    def test_set_allows_default_kms_key_to_be_explicitly_specified(self):
        bucket = Bucket()
        keyid = "aws/s3"

        bucket.set_encryption(kms_keyid=keyid)

        self._verify_has_kms_encryption(bucket, keyid)

    def test_sets_s3_encryption_when_specified(self):
        bucket = Bucket()

        bucket.set_encryption(s3_managed=True)

        self._verify_has_s3_encryption(bucket)

    def test_raises_error_when_setting_kms_key_and_s3_encryption(self):
        bucket = Bucket()
        keyid = "arn:aws:kms:us-east-1:123456789012:key/52a6b44c-8840-41e3-86cd-78cbb022af5e"

        with pytest.raises(ValueError, match=r"S3.*KMS.*managed"):
            bucket.set_encryption(kms_keyid=keyid, s3_managed=True)

    def test_replaces_existing_s3_configuration(self):
        # Setup
        bucket = Bucket()
        bucket.set_encryption(s3_managed=True)

        # Exercise
        bucket.set_encryption()

        # Verify
        self._verify_has_kms_encryption(bucket, "aws/s3")

    def test_replaces_existing_kms_configuration(self):
        # Setup
        bucket = Bucket()
        bucket.set_encryption()

        # Exercise
        bucket.set_encryption(s3_managed=True)

        # Verify
        self._verify_has_s3_encryption(bucket)

    def test_replaces_existing_kms_configuration_with_another_key(self):
        # Setup
        bucket = Bucket()
        old_keyid = "arn:aws:kms:us-east-1:123456789012:key/52a6b44c-8840-41e3-86cd-78cbb022af5e"
        new_keyid = "arn:aws:kms:us-east-1:123456789012:key/e624caf8-2e45-447d-b3a7-5b1faef96dce"
        bucket.set_encryption(kms_keyid=old_keyid)

        # Exercise
        bucket.set_encryption(kms_keyid=new_keyid)

        # Verify
        self._verify_has_kms_encryption(bucket, new_keyid)

    def test_replaces_existing_multiple_rule_configuration(self):
        # Setup
        bucket = Bucket(
            Properties={
                "BucketEncryption": {
                    "ServerSideEncryptionConfiguration": [
                        {
                            "ServerSideEncryptionByDefault": {
                                "KMSMasterKeyID": "aws/s3",
                                "SSEAlgorithm": "aws:kms",
                            }
                        },
                        # Note that this is invalid, but hey!
                        {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}},
                    ]
                }
            }
        )

        keyid = "arn:aws:kms:us-east-1:123456789012:key/52a6b44c-8840-41e3-86cd-78cbb022af5e"

        # Exercise
        bucket.set_encryption(kms_keyid=keyid)

        # Verify
        self._verify_has_kms_encryption(bucket, keyid)


class TestVersioning(object):
    """Verify the behaviour of the `Bucket.versioning` property"""

    #: Valid values for the CloudFormation property "VersioningConfiguration.Status"
    STATUS_VALUES = [("Enabled", True), ("Suspended", False)]

    def test_should_be_false_when_no_property_is_set(self):
        bucket = Bucket()
        assert bucket.versioning is False

    @pytest.mark.parametrize(("status", "is_enabled"), STATUS_VALUES)
    def test_should_get_value_from_underlying_property(self, status, is_enabled):
        bucket = Bucket(Properties=dict(VersioningConfiguration=dict(Status=status)))

        assert bucket.versioning is is_enabled

    def test_get_should_raise_error_when_existing_property_is_invalid(self):
        bucket = Bucket(
            Properties=dict(VersioningConfiguration=dict(Status="ItsComplicated"))
        )

        with pytest.raises(ValueError, match=r"ItsComplicated"):
            _ = bucket.versioning

    @pytest.mark.parametrize(("status", "is_enabled"), STATUS_VALUES)
    def test_should_set_underlying_property(self, status, is_enabled):
        bucket = Bucket()
        bucket.versioning = is_enabled

        assert bucket["Properties"]["VersioningConfiguration"]["Status"] == status

    def test_set_should_override_existing_property(self):
        # Setup
        bucket = Bucket(
            Properties=dict(VersioningConfiguration=dict(Status="Suspended"))
        )

        # Exercise
        bucket.versioning = True

        # Verify
        assert bucket["Properties"]["VersioningConfiguration"]["Status"] == "Enabled"
