"""Raw representations of every data type in the AWS EMR service.

See Also:
    `AWS developer guide for EMR
    <https://docs.aws.amazon.com/dms/latest/userguide/index.html>`_

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
    "InstanceFleetConfig",
    "InstanceFleetConfigProperties",
    "InstanceGroupConfig",
    "InstanceGroupConfigProperties",
    "SecurityConfiguration",
    "SecurityConfigurationProperties",
    "Step",
    "StepProperties",
]


@attrs(**ATTRSCONFIG)
class ClusterProperties(ResourceProperties):
    AdditionalInfo = attrib(default=None)
    Applications = attrib(default=None)
    AutoScalingRole = attrib(default=None)
    BootstrapActions = attrib(default=None)
    Configurations = attrib(default=None)
    CustomAmiId = attrib(default=None)
    EbsRootVolumeSize = attrib(default=None)
    Instances = attrib(default=None)
    JobFlowRole = attrib(default=None)
    KerberosAttributes = attrib(default=None)
    LogEncryptionKmsKeyId = attrib(default=None)
    LogUri = attrib(default=None)
    ManagedScalingPolicy = attrib(default=None)
    Name = attrib(default=None)
    ReleaseLabel = attrib(default=None)
    ScaleDownBehavior = attrib(default=None)
    SecurityConfiguration = attrib(default=None)
    ServiceRole = attrib(default=None)
    StepConcurrencyLevel = attrib(default=None)
    Steps = attrib(default=None)
    Tags = attrib(default=None)
    VisibleToAllUsers = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Cluster(Resource):
    """A Cluster for EMR.

    See Also:
        `AWS Cloud Formation documentation for Cluster
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticmapreduce-cluster.html>`_
    """

    RESOURCE_TYPE = "AWS::EMR::Cluster"

    Properties: ClusterProperties = attrib(
        factory=ClusterProperties, converter=create_object_converter(ClusterProperties)
    )


@attrs(**ATTRSCONFIG)
class InstanceFleetConfigProperties(ResourceProperties):
    ClusterId = attrib(default=None)
    InstanceFleetType = attrib(default=None)
    InstanceTypeConfigs = attrib(default=None)
    LaunchSpecifications = attrib(default=None)
    Name = attrib(default=None)
    TargetOnDemandCapacity = attrib(default=None)
    TargetSpotCapacity = attrib(default=None)


@attrs(**ATTRSCONFIG)
class InstanceFleetConfig(Resource):
    """A Instance Fleet Config for EMR.

    See Also:
        `AWS Cloud Formation documentation for InstanceFleetConfig
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticmapreduce-instancefleetconfig.html>`_
    """

    RESOURCE_TYPE = "AWS::EMR::InstanceFleetConfig"

    Properties: InstanceFleetConfigProperties = attrib(
        factory=InstanceFleetConfigProperties,
        converter=create_object_converter(InstanceFleetConfigProperties),
    )


@attrs(**ATTRSCONFIG)
class InstanceGroupConfigProperties(ResourceProperties):
    AutoScalingPolicy = attrib(default=None)
    BidPrice = attrib(default=None)
    Configurations = attrib(default=None)
    EbsConfiguration = attrib(default=None)
    InstanceCount = attrib(default=None)
    InstanceRole = attrib(default=None)
    InstanceType = attrib(default=None)
    JobFlowId = attrib(default=None)
    Market = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class InstanceGroupConfig(Resource):
    """A Instance Group Config for EMR.

    See Also:
        `AWS Cloud Formation documentation for InstanceGroupConfig
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-instancegroupconfig.html>`_
    """

    RESOURCE_TYPE = "AWS::EMR::InstanceGroupConfig"

    Properties: InstanceGroupConfigProperties = attrib(
        factory=InstanceGroupConfigProperties,
        converter=create_object_converter(InstanceGroupConfigProperties),
    )


@attrs(**ATTRSCONFIG)
class SecurityConfigurationProperties(ResourceProperties):
    Name = attrib(default=None)
    SecurityConfiguration = attrib(default=None)


@attrs(**ATTRSCONFIG)
class SecurityConfiguration(Resource):
    """A Security Configuration for EMR.

    See Also:
        `AWS Cloud Formation documentation for SecurityConfiguration
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-securityconfiguration.html>`_
    """

    RESOURCE_TYPE = "AWS::EMR::SecurityConfiguration"

    Properties: SecurityConfigurationProperties = attrib(
        factory=SecurityConfigurationProperties,
        converter=create_object_converter(SecurityConfigurationProperties),
    )


@attrs(**ATTRSCONFIG)
class StepProperties(ResourceProperties):
    ActionOnFailure = attrib(default=None)
    HadoopJarStep = attrib(default=None)
    JobFlowId = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Step(Resource):
    """A Step for EMR.

    See Also:
        `AWS Cloud Formation documentation for Step
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-step.html>`_
    """

    RESOURCE_TYPE = "AWS::EMR::Step"

    Properties: StepProperties = attrib(
        factory=StepProperties, converter=create_object_converter(StepProperties)
    )
