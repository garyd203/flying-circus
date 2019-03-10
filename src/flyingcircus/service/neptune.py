"""General-use classes to interact with the Neptune service through CloudFormation.

See Also:
    `AWS developer guide for Neptune
    <https://docs.aws.amazon.com/neptune/latest/userguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import neptune as _raw

# noinspection PyUnresolvedReferences
from .._raw.neptune import *
