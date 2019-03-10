"""General-use classes to interact with the DAX service through CloudFormation.

See Also:
    `AWS developer guide for DAX
    <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import dax as _raw

# noinspection PyUnresolvedReferences
from .._raw.dax import *
