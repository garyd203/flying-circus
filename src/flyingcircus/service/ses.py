"""General-use classes to interact with the SES service through CloudFormation.

See Also:
    `AWS developer guide for SES
    <https://docs.aws.amazon.com/servicecatalog/latest/dg/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ses as _raw

# noinspection PyUnresolvedReferences
from .._raw.ses import *
