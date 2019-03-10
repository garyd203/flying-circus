"""General-use classes to interact with the Athena service through CloudFormation.

See Also:
    `AWS developer guide for Athena
    <https://docs.aws.amazon.com/athena/latest/ug/what-is.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import athena as _raw

# noinspection PyUnresolvedReferences
from .._raw.athena import *
