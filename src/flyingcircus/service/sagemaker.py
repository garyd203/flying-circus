"""General-use classes to interact with the SageMaker service through CloudFormation.

See Also:
    `AWS developer guide for SageMaker
    <https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import sagemaker as _raw

# noinspection PyUnresolvedReferences
from .._raw.sagemaker import *
