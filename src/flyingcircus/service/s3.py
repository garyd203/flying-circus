"""General-use classes to interact with the S3 service through CloudFormation.

See Also:
    `AWS developer guide for S3
    <https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_
"""

from .._raw import s3 as _raw

# noinspection PyUnresolvedReferences
from .._raw.s3 import *


class Bucket(_raw.Bucket):
    __slots__ = []

    #: Key ID for the AWS-supplied KMS Master Key used for server-side
    #: encryption if a customer-managed key is not explicitly specified.
    SSE_KMS_DEFAULT_MASTER_KEY = "aws/s3"

    def set_encryption(
        self, kms_keyid=SSE_KMS_DEFAULT_MASTER_KEY, s3_managed: bool = False
    ):
        """Set the default server-side encryption approach for this bucket.

        This convenience function can be used to set any one of the mutually
        exclusive `AWS server-side encryption schemes
        <https://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html>`_
        With default parameters, it will set KMS-managed encryption with the
        default AWS S3 KMS key.

        Parameters:
            kms_keyid: Use KMS-managed encryption with this custom KMS key.
            s3_managed: Use S3-managed encryption.
        """
        # TODO also implement is_s3_encrypted, is_kms_encrypted, get_kms_key

        # Checks
        if s3_managed and kms_keyid != self.SSE_KMS_DEFAULT_MASTER_KEY:
            raise ValueError(
                "Unable to set both S3-managed and KMS-managed bucket encryption"
            )

        # Get the top-level encryption config object
        config = self.Properties["BucketEncryption"]
        if not config:
            self.Properties["BucketEncryption"] = {}
            config = self.Properties["BucketEncryption"] = {}

        # Create a fresh single-value list of server-side encryption rules
        if s3_managed:
            rule = {"SSEAlgorithm": "AES256"}
        else:
            rule = {"KMSMasterKeyID": kms_keyid, "SSEAlgorithm": "aws:kms"}
        config["ServerSideEncryptionConfiguration"] = [
            {"ServerSideEncryptionByDefault": rule}
        ]

    #: List of Status values for Bucket versioning, and whether they mean
    #: versioning is enabled
    _VERSIONING_STATUSES = {"Enabled": True, "Suspended": False}  # Default

    @property
    def versioning(self) -> bool:
        """Whether versioning is enabled for this bucket.

        This sets the nested CloudFormation property "VersioningConfiguration.Status".

        Raises:
            ValueError: If the existing property does not have a valid value.

        See Also:
            `VersioningConfiguration documentation
            <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html>`_
        """
        config = self.Properties["VersioningConfiguration"]
        if not config:
            return False
        status = config["Status"]

        try:
            return self._VERSIONING_STATUSES[status]
        except KeyError:
            raise ValueError(f"Unknown VersioningConfiguration status: {status}")

    @versioning.setter
    def versioning(self, value: bool):
        config = self.Properties["VersioningConfiguration"]
        if not config:
            self.Properties["VersioningConfiguration"] = {}
            config = self.Properties["VersioningConfiguration"]
        config["Status"] = "Enabled" if value else "Suspended"
