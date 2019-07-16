"""Raw representations of every data type in the AWS MSK service.

See Also:
    `AWS developer guide for MSK
    <https://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Cluster", "ClusterProperties"]


@attrs(**ATTRSCONFIG)
class ClusterProperties(ResourceProperties):
    BrokerNodeGroupInfo = attrib(default=None)
    ClientAuthentication = attrib(default=None)
    ClusterName = attrib(default=None)
    ConfigurationInfo = attrib(default=None)
    EncryptionInfo = attrib(default=None)
    EnhancedMonitoring = attrib(default=None)
    KafkaVersion = attrib(default=None)
    NumberOfBrokerNodes = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Cluster(Resource):
    """A Cluster for MSK.

    See Also:
        `AWS Cloud Formation documentation for Cluster
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html>`_
    """

    RESOURCE_TYPE = "AWS::MSK::Cluster"

    Properties: ClusterProperties = attrib(
        factory=ClusterProperties, converter=create_object_converter(ClusterProperties)
    )