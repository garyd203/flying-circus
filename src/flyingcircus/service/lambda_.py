"""General-use classes to interact with the Lambda service through CloudFormation.

See Also:
    `AWS developer guide for Lambda
    <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_
"""

import sys

# noinspection PyUnresolvedReferences
from .._raw import lambda_ as _raw

# noinspection PyUnresolvedReferences
from .._raw.lambda_ import *

#: Lambda Runtimes for Python that we know about.
#: See `the definitive list in the AWS documentation
#: <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html>`_
_KNOWN_LAMBDA_RUNTIMES = {(2, 7): "python2.7", (3, 6): "python3.6", (3, 7): "python3.7"}


def get_lambda_runtime_for_this_process() -> str:
    """Determine the best Lambda runtime for the current Python process."""
    # The basic premise is to use exact matching if possible, upgrade if
    # necessary, and don't downgrade

    (major, minor, _, _, _) = sys.version_info

    try:
        return _KNOWN_LAMBDA_RUNTIMES[(major, minor)]
    except KeyError:
        pass

    # Maybe this is an old Python v3
    if major == 3 and minor < 6:
        return _KNOWN_LAMBDA_RUNTIMES[(3, 6)]

    # Maybe this is an old Python v2
    if major == 2 and minor < 7:
        return _KNOWN_LAMBDA_RUNTIMES[(2, 7)]

    raise ValueError(
        "Python version '{}' cannot be supported by AWS Lambda".format(sys.version)
    )
