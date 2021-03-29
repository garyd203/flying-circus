"""General-use classes to interact with the SSO service through CloudFormation.

See Also:
    `AWS developer guide for SSO
    <https://docs.aws.amazon.com/singlesignon/latest/userguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import sso as _raw

# noinspection PyUnresolvedReferences
from .._raw.sso import *
