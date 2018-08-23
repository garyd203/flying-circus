"""General-use classes to interact with the KMS service through CloudFormation.

See Also:
    `AWS developer guide for KMS
    <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import kms as _raw

# noinspection PyUnresolvedReferences
from .._raw.kms import *
