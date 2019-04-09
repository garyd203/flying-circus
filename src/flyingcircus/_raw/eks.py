"""Raw representations of every data type in the AWS EKS service.

See Also:
    `AWS developer guide for EKS
    <https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html>`_

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
    Name = attrib(default=None)
    ResourcesVpcConfig = attrib(default=None)
    RoleArn = attrib(default=None)
    Version = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Cluster(Resource):
    """A Cluster for EKS.

    See Also:
        `AWS Cloud Formation documentation for Cluster
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html>`_
    """

    RESOURCE_TYPE = "AWS::EKS::Cluster"

    Properties: ClusterProperties = attrib(
        factory=ClusterProperties, converter=create_object_converter(ClusterProperties)
    )
