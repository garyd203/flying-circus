"""General-use classes to interact with the RDS service through CloudFormation.

See Also:
    `AWS developer guide for RDS
    <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/index.html>`_
"""

from .._raw import rds as _raw

# noinspection PyUnresolvedReferences
from .._raw.rds import *


class DBInstance(_raw.DBInstance):
    # Implement Naming
    # ----------------
    @property
    def name(self):
        try:
            return self.Properties["DBInstanceIdentifier"]
        except KeyError:
            # No name set yet
            return None

    @name.setter
    def name(self, value: str):
        self.Properties["DBInstanceIdentifier"] = value
