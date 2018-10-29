"""General-use classes to interact with the S3 service through CloudFormation.

See Also:
    `AWS developer guide for S3
    <https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import s3 as _raw

# noinspection PyUnresolvedReferences
from .._raw.s3 import *


class Bucket(_raw.Bucket):
    #: List of Status values for Bucket versioning, and whether they mean
    #: versioning is enabled
    _VERSIONING_STATUSES = {
        "Enabled": True,
        "Suspended": False,  # Default
    }

    @property
    def versioning(self) -> bool:
        """Whether versioning is enabled for this bucket.

        This sets the nested CloudFormation property "VersioningConfiguration.Status".

        Raises:
            ValueError: If the existing property does not have a valid value.

        See Also:
            `VersioningConfiguration documentation
            <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html>`
        """
        try:
            status = self.Properties["VersioningConfiguration"]["Status"]
        except KeyError:
            return False

        try:
            return self._VERSIONING_STATUSES[status]
        except KeyError:
            raise ValueError(f"Unknown VersioningConfiguration status: {status}")

    @versioning.setter
    def versioning(self, value: bool):
        try:
            config = self.Properties["VersioningConfiguration"]
        except KeyError:
            config = self.Properties["VersioningConfiguration"] = {}
        config["Status"] = "Enabled" if value else "Suspended"
