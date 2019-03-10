"""General-use classes to interact with the EMR service through CloudFormation.

See Also:
    `AWS developer guide for EMR
    <https://docs.aws.amazon.com/dms/latest/userguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import emr as _raw

# noinspection PyUnresolvedReferences
from .._raw.emr import *
