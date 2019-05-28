"""General-use classes to interact with the SSM service through CloudFormation.

See Also:
    `AWS developer guide for SSM
    <https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html>`_
"""

from .._raw import ssm as _raw

# noinspection PyUnresolvedReferences
from .._raw.ssm import *

# Also provide an alias for the SSM Parameter resource, to reduce conflicts
# with the top-level template Parameter object
# FIXME do these as imports instead, so that pycharm type chekcing picks them up more reliably
SSMParameter = _raw.Parameter
SSMParameterProperties = _raw.ParameterProperties
