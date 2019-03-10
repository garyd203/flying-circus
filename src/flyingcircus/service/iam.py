"""General-use classes to interact with the IAM service through CloudFormation.

See Also:
    `AWS developer guide for IAM
    <https://docs.aws.amazon.com/IAM/latest/UserGuide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import iam as _raw

# noinspection PyUnresolvedReferences
from .._raw.iam import *
