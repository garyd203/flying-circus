"""General-use classes to interact with the SSM service through CloudFormation.

See Also:
    `AWS developer guide for SSM
    <https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ssm as _raw

# noinspection PyUnresolvedReferences
from .._raw.ssm import *
