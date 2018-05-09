"""General-use classes to interact with the ECS service through CloudFormation.

See Also:
    `AWS developer guide for ECS
    <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ecs as _raw

# noinspection PyUnresolvedReferences
from .._raw.ecs import *
