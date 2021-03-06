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

__all__ = ["Cluster", "ClusterProperties", "Nodegroup", "NodegroupProperties"]


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


@attrs(**ATTRSCONFIG)
class NodegroupProperties(ResourceProperties):
    AmiType = attrib(default=None)
    ClusterName = attrib(default=None)
    DiskSize = attrib(default=None)
    ForceUpdateEnabled = attrib(default=None)
    InstanceTypes = attrib(default=None)
    Labels = attrib(default=None)
    NodegroupName = attrib(default=None)
    NodeRole = attrib(default=None)
    ReleaseVersion = attrib(default=None)
    RemoteAccess = attrib(default=None)
    ScalingConfig = attrib(default=None)
    Subnets = attrib(default=None)
    Tags = attrib(default=None)
    Version = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Nodegroup(Resource):
    """A Nodegroup for EKS.

    See Also:
        `AWS Cloud Formation documentation for Nodegroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html>`_
    """

    RESOURCE_TYPE = "AWS::EKS::Nodegroup"

    Properties: NodegroupProperties = attrib(
        factory=NodegroupProperties,
        converter=create_object_converter(NodegroupProperties),
    )
