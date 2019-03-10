"""General-use classes to interact with the Redshift service through CloudFormation.

See Also:
    `AWS developer guide for Redshift
    <https://docs.aws.amazon.com/redshift/latest/gsg/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import redshift as _raw

# noinspection PyUnresolvedReferences
from .._raw.redshift import *
