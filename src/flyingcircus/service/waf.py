"""General-use classes to interact with the WAF service through CloudFormation.

See Also:
    `AWS developer guide for WAF
    <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import waf as _raw

# noinspection PyUnresolvedReferences
from .._raw.waf import *
