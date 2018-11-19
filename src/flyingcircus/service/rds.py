"""General-use classes to interact with the RDS service through CloudFormation.

See Also:
    `AWS developer guide for RDS
    <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import rds as _raw

# noinspection PyUnresolvedReferences
from .._raw.rds import *
