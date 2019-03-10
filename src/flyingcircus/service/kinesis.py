"""General-use classes to interact with the Kinesis service through CloudFormation.

See Also:
    `AWS developer guide for Kinesis
    <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import kinesis as _raw

# noinspection PyUnresolvedReferences
from .._raw.kinesis import *
