"""General-use classes to interact with the DynamoDB service through CloudFormation.

See Also:
    `AWS developer guide for DynamoDB
    <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import dynamodb as _raw

# noinspection PyUnresolvedReferences
from .._raw.dynamodb import *
