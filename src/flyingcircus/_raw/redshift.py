"""Raw representations of every data type in the AWS Redshift service.

See Also:
    `AWS developer guide for Redshift
    <https://docs.aws.amazon.com/redshift/latest/gsg/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Cluster",
    "ClusterProperties",
    "ClusterParameterGroup",
    "ClusterParameterGroupProperties",
    "ClusterSecurityGroup",
    "ClusterSecurityGroupProperties",
    "ClusterSecurityGroupIngress",
    "ClusterSecurityGroupIngressProperties",
    "ClusterSubnetGroup",
    "ClusterSubnetGroupProperties",
]


@attrs(**ATTRSCONFIG)
class ClusterProperties(ResourceProperties):
    AllowVersionUpgrade = attrib(default=None)
    AutomatedSnapshotRetentionPeriod = attrib(default=None)
    AvailabilityZone = attrib(default=None)
    ClusterIdentifier = attrib(default=None)
    ClusterParameterGroupName = attrib(default=None)
    ClusterSecurityGroups = attrib(default=None)
    ClusterSubnetGroupName = attrib(default=None)
    ClusterType = attrib(default=None)
    ClusterVersion = attrib(default=None)
    DBName = attrib(default=None)
    ElasticIp = attrib(default=None)
    Encrypted = attrib(default=None)
    HsmClientCertificateIdentifier = attrib(default=None)
    HsmConfigurationIdentifier = attrib(default=None)
    IamRoles = attrib(default=None)
    KmsKeyId = attrib(default=None)
    LoggingProperties = attrib(default=None)
    MasterUsername = attrib(default=None)
    MasterUserPassword = attrib(default=None)
    NodeType = attrib(default=None)
    NumberOfNodes = attrib(default=None)
    OwnerAccount = attrib(default=None)
    Port = attrib(default=None)
    PreferredMaintenanceWindow = attrib(default=None)
    PubliclyAccessible = attrib(default=None)
    SnapshotClusterIdentifier = attrib(default=None)
    SnapshotIdentifier = attrib(default=None)
    Tags = attrib(default=None)
    VpcSecurityGroupIds = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Cluster(Resource):
    """A Cluster for Redshift.

    See Also:
        `AWS Cloud Formation documentation for Cluster
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_
    """

    RESOURCE_TYPE = "AWS::Redshift::Cluster"

    Properties: ClusterProperties = attrib(
        factory=ClusterProperties,
        converter=create_object_converter(ClusterProperties),
    )


@attrs(**ATTRSCONFIG)
class ClusterParameterGroupProperties(ResourceProperties):
    Description = attrib(default=None)
    ParameterGroupFamily = attrib(default=None)
    Parameters = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ClusterParameterGroup(Resource):
    """A Cluster Parameter Group for Redshift.

    See Also:
        `AWS Cloud Formation documentation for ClusterParameterGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html>`_
    """

    RESOURCE_TYPE = "AWS::Redshift::ClusterParameterGroup"

    Properties: ClusterParameterGroupProperties = attrib(
        factory=ClusterParameterGroupProperties,
        converter=create_object_converter(ClusterParameterGroupProperties),
    )


@attrs(**ATTRSCONFIG)
class ClusterSecurityGroupProperties(ResourceProperties):
    Description = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ClusterSecurityGroup(Resource):
    """A Cluster Security Group for Redshift.

    See Also:
        `AWS Cloud Formation documentation for ClusterSecurityGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html>`_
    """

    RESOURCE_TYPE = "AWS::Redshift::ClusterSecurityGroup"

    Properties: ClusterSecurityGroupProperties = attrib(
        factory=ClusterSecurityGroupProperties,
        converter=create_object_converter(ClusterSecurityGroupProperties),
    )


@attrs(**ATTRSCONFIG)
class ClusterSecurityGroupIngressProperties(ResourceProperties):
    CIDRIP = attrib(default=None)
    ClusterSecurityGroupName = attrib(default=None)
    EC2SecurityGroupName = attrib(default=None)
    EC2SecurityGroupOwnerId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ClusterSecurityGroupIngress(Resource):
    """A Cluster Security Group Ingress for Redshift.

    See Also:
        `AWS Cloud Formation documentation for ClusterSecurityGroupIngress
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html>`_
    """

    RESOURCE_TYPE = "AWS::Redshift::ClusterSecurityGroupIngress"

    Properties: ClusterSecurityGroupIngressProperties = attrib(
        factory=ClusterSecurityGroupIngressProperties,
        converter=create_object_converter(ClusterSecurityGroupIngressProperties),
    )


@attrs(**ATTRSCONFIG)
class ClusterSubnetGroupProperties(ResourceProperties):
    Description = attrib(default=None)
    SubnetIds = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ClusterSubnetGroup(Resource):
    """A Cluster Subnet Group for Redshift.

    See Also:
        `AWS Cloud Formation documentation for ClusterSubnetGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html>`_
    """

    RESOURCE_TYPE = "AWS::Redshift::ClusterSubnetGroup"

    Properties: ClusterSubnetGroupProperties = attrib(
        factory=ClusterSubnetGroupProperties,
        converter=create_object_converter(ClusterSubnetGroupProperties),
    )
