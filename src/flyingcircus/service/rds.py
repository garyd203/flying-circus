"""General-use classes to interact with the RDS service through CloudFormation.

See Also:
    `AWS developer guide for RDS
    <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/index.html>`_
"""

from .._raw import rds as _raw

# noinspection PyUnresolvedReferences
from .._raw.rds import *


class DBInstance(_raw.DBInstance):
    __slots__ = []

    # Implement Naming
    # ----------------
    @property
    def name(self):
        return self.Properties["DBInstanceIdentifier"]  # Might be default of None

    @name.setter
    def name(self, value: str):
        self.Properties["DBInstanceIdentifier"] = value
