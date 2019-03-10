"""General-use classes to interact with the SQS service through CloudFormation.

See Also:
    `AWS developer guide for SQS
    <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import sqs as _raw

# noinspection PyUnresolvedReferences
from .._raw.sqs import *
