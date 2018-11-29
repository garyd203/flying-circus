"""General-use classes to interact with the Lambda service through CloudFormation.

See Also:
    `AWS developer guide for Lambda
    <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import lambda_ as _raw

# noinspection PyUnresolvedReferences
from .._raw.lambda_ import *
