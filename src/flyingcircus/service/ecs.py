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


class TaskDefinition(_raw.TaskDefinition):
    __slots__ = []

    # Implement Naming
    # ----------------
    @property
    def name(self):
        # TaskDefinitions are assigned randomised names. However, if you put
        # them in a family, then all TaskDefinitions in that family are
        # considered to be different versions of the same TaskDefinition,
        # which as a group are referenced by the Family name. Hence the
        # Family name is the TaskDefinition name.
        return self.Properties["Family"]  # Might be default of None

    @name.setter
    def name(self, value: str):
        self.Properties["Family"] = value
