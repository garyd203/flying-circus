"""General-use classes to interact with the SNS service through CloudFormation.

See Also:
    `AWS developer guide for SNS
    <https://docs.aws.amazon.com/sns/latest/dg/welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import sns as _raw

# noinspection PyUnresolvedReferences
from .._raw.sns import *
