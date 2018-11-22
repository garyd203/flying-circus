"""General-use classes to interact with the SecretsManager service through CloudFormation.

See Also:
    `AWS developer guide for SecretsManager
    <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_
"""

from .._raw import secretsmanager as _raw

# noinspection PyUnresolvedReferences
from .._raw.secretsmanager import *


class Secret(_raw.Secret):
    __slots__ = []

    # Implement Naming
    # ----------------
    @property
    def name(self):
        return self.Properties["Name"]  # Might be default of None

    @name.setter
    def name(self, value: str):
        self.Properties["Name"] = value
