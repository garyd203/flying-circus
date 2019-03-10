"""General-use classes to interact with the EFS service through CloudFormation.

See Also:
    `AWS developer guide for EFS
    <https://docs.aws.amazon.com/efs/latest/ug/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import efs as _raw

# noinspection PyUnresolvedReferences
from .._raw.efs import *
