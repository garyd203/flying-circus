"""General-use classes to interact with the Greengrass service through CloudFormation.

See Also:
    `AWS developer guide for Greengrass
    <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import greengrass as _raw

# noinspection PyUnresolvedReferences
from .._raw.greengrass import *
