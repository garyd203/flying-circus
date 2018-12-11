"""General-use classes to interact with the Route53 service through CloudFormation.

See Also:
    `AWS developer guide for Route53
    <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import route53 as _raw

# noinspection PyUnresolvedReferences
from .._raw.route53 import *
