"""Raw representations of every data type in the AWS DMS service.

See Also:
    `AWS developer guide for DMS
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
    "Certificate",
    "CertificateProperties",
    "Endpoint",
    "EndpointProperties",
    "EventSubscription",
    "EventSubscriptionProperties",
    "ReplicationInstance",
    "ReplicationInstanceProperties",
    "ReplicationSubnetGroup",
    "ReplicationSubnetGroupProperties",
    "ReplicationTask",
    "ReplicationTaskProperties",
]


@attrs(**ATTRSCONFIG)
class CertificateProperties(ResourceProperties):
    CertificateIdentifier = attrib(default=None)
    CertificatePem = attrib(default=None)
    CertificateWallet = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Certificate(Resource):
    """A Certificate for DMS.

    See Also:
        `AWS Cloud Formation documentation for Certificate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::Certificate"

    Properties: CertificateProperties = attrib(
        factory=CertificateProperties,
        converter=create_object_converter(CertificateProperties),
    )


@attrs(**ATTRSCONFIG)
class EndpointProperties(ResourceProperties):
    CertificateArn = attrib(default=None)
    DatabaseName = attrib(default=None)
    DynamoDbSettings = attrib(default=None)
    ElasticsearchSettings = attrib(default=None)
    EndpointIdentifier = attrib(default=None)
    EndpointType = attrib(default=None)
    EngineName = attrib(default=None)
    ExtraConnectionAttributes = attrib(default=None)
    KinesisSettings = attrib(default=None)
    KmsKeyId = attrib(default=None)
    MongoDbSettings = attrib(default=None)
    Password = attrib(default=None)
    Port = attrib(default=None)
    S3Settings = attrib(default=None)
    ServerName = attrib(default=None)
    SslMode = attrib(default=None)
    Tags = attrib(default=None)
    Username = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Endpoint(Resource):
    """A Endpoint for DMS.

    See Also:
        `AWS Cloud Formation documentation for Endpoint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::Endpoint"

    Properties: EndpointProperties = attrib(
        factory=EndpointProperties,
        converter=create_object_converter(EndpointProperties),
    )


@attrs(**ATTRSCONFIG)
class EventSubscriptionProperties(ResourceProperties):
    Enabled = attrib(default=None)
    EventCategories = attrib(default=None)
    SnsTopicArn = attrib(default=None)
    SourceIds = attrib(default=None)
    SourceType = attrib(default=None)
    SubscriptionName = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class EventSubscription(Resource):
    """A Event Subscription for DMS.

    See Also:
        `AWS Cloud Formation documentation for EventSubscription
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::EventSubscription"

    Properties: EventSubscriptionProperties = attrib(
        factory=EventSubscriptionProperties,
        converter=create_object_converter(EventSubscriptionProperties),
    )


@attrs(**ATTRSCONFIG)
class ReplicationInstanceProperties(ResourceProperties):
    AllocatedStorage = attrib(default=None)
    AllowMajorVersionUpgrade = attrib(default=None)
    AutoMinorVersionUpgrade = attrib(default=None)
    AvailabilityZone = attrib(default=None)
    EngineVersion = attrib(default=None)
    KmsKeyId = attrib(default=None)
    MultiAZ = attrib(default=None)
    PreferredMaintenanceWindow = attrib(default=None)
    PubliclyAccessible = attrib(default=None)
    ReplicationInstanceClass = attrib(default=None)
    ReplicationInstanceIdentifier = attrib(default=None)
    ReplicationSubnetGroupIdentifier = attrib(default=None)
    Tags = attrib(default=None)
    VpcSecurityGroupIds = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ReplicationInstance(Resource):
    """A Replication Instance for DMS.

    See Also:
        `AWS Cloud Formation documentation for ReplicationInstance
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::ReplicationInstance"

    Properties: ReplicationInstanceProperties = attrib(
        factory=ReplicationInstanceProperties,
        converter=create_object_converter(ReplicationInstanceProperties),
    )


@attrs(**ATTRSCONFIG)
class ReplicationSubnetGroupProperties(ResourceProperties):
    ReplicationSubnetGroupDescription = attrib(default=None)
    ReplicationSubnetGroupIdentifier = attrib(default=None)
    SubnetIds = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ReplicationSubnetGroup(Resource):
    """A Replication Subnet Group for DMS.

    See Also:
        `AWS Cloud Formation documentation for ReplicationSubnetGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::ReplicationSubnetGroup"

    Properties: ReplicationSubnetGroupProperties = attrib(
        factory=ReplicationSubnetGroupProperties,
        converter=create_object_converter(ReplicationSubnetGroupProperties),
    )


@attrs(**ATTRSCONFIG)
class ReplicationTaskProperties(ResourceProperties):
    CdcStartTime = attrib(default=None)
    MigrationType = attrib(default=None)
    ReplicationInstanceArn = attrib(default=None)
    ReplicationTaskIdentifier = attrib(default=None)
    ReplicationTaskSettings = attrib(default=None)
    SourceEndpointArn = attrib(default=None)
    TableMappings = attrib(default=None)
    Tags = attrib(default=None)
    TargetEndpointArn = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ReplicationTask(Resource):
    """A Replication Task for DMS.

    See Also:
        `AWS Cloud Formation documentation for ReplicationTask
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html>`_
    """

    RESOURCE_TYPE = "AWS::DMS::ReplicationTask"

    Properties: ReplicationTaskProperties = attrib(
        factory=ReplicationTaskProperties,
        converter=create_object_converter(ReplicationTaskProperties),
    )