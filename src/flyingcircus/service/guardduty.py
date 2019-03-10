"""General-use classes to interact with the GuardDuty service through CloudFormation.

See Also:
    `AWS developer guide for GuardDuty
    <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import guardduty as _raw

# noinspection PyUnresolvedReferences
from .._raw.guardduty import *
