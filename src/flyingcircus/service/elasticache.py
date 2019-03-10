"""General-use classes to interact with the ElastiCache service through CloudFormation.

See Also:
    `AWS developer guide for ElastiCache
    <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import elasticache as _raw

# noinspection PyUnresolvedReferences
from .._raw.elasticache import *
