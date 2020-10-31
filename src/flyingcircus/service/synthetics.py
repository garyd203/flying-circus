"""General-use classes to interact with the Synthetics service through CloudFormation.

See Also:
    `AWS developer guide for Synthetics
    <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import synthetics as _raw

# noinspection PyUnresolvedReferences
from .._raw.synthetics import *
