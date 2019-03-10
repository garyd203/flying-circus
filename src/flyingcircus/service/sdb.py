"""General-use classes to interact with the SDB service through CloudFormation.

See Also:
    `AWS developer guide for SDB
    <https://docs.aws.amazon.com/AmazonSimpleDB/latest/DeveloperGuide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import sdb as _raw

# noinspection PyUnresolvedReferences
from .._raw.sdb import *
