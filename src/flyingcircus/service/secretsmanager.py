"""General-use classes to interact with the SecretsManager service through CloudFormation.

See Also:
    `AWS developer guide for SecretsManager
    <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_
"""

from .._raw import secretsmanager as _raw

# noinspection PyUnresolvedReferences
from .._raw.secretsmanager import *


class Secret(_raw.Secret):
    # Implement Naming
    # ----------------
    @property
    def name(self):
        try:
            return self.Properties["Name"]
        except KeyError:
            # No name set yet
            return None

    @name.setter
    def name(self, value: str):
        self.Properties["Name"] = value
