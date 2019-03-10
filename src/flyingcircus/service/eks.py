"""General-use classes to interact with the EKS service through CloudFormation.

See Also:
    `AWS developer guide for EKS
    <https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import eks as _raw

# noinspection PyUnresolvedReferences
from .._raw.eks import *
