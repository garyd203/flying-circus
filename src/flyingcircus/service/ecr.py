"""General-use classes to interact with the ECR service through CloudFormation.

See Also:
    `AWS developer guide for ECR
    <https://docs.aws.amazon.com/AmazonECR/latest/userguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ecr as _raw

# noinspection PyUnresolvedReferences
from .._raw.ecr import *
