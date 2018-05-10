"""General-use classes to interact with the ECS service through CloudFormation.

See Also:
    `AWS developer guide for ECS
    <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ecs as _raw

# noinspection PyUnresolvedReferences
from .._raw.ecs import *

# TODO specialised Service and TaskDefinition for use with fargate (which explicitly excludes some of the fields)
