"""General-use classes to interact with the EC2 service through CloudFormation.

See Also:
    `AWS developer guide for EC2
    <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import ec2 as _raw

# noinspection PyUnresolvedReferences
from .._raw.ec2 import *
