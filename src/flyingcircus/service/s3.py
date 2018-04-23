"""General-use classes to interact with the S3 service through CloudFormation.

See Also:
    `AWS developer guide for S3
    <https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import s3 as _raw

# noinspection PyUnresolvedReferences
from .._raw.s3 import *
