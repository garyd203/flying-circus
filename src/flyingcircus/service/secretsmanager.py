"""General-use classes to interact with the SecretsManager service through CloudFormation.

See Also:
    `AWS developer guide for SecretsManager
    <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import secretsmanager as _raw

# noinspection PyUnresolvedReferences
from .._raw.secretsmanager import *
