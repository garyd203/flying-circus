"""Raw representations of every data type in the AWS OpsWorksCM service.

See Also:
    `AWS developer guide for OpsWorksCM
    <https://docs.aws.amazon.com/opsworks/latest/userguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Server", "ServerProperties"]


@attrs(**ATTRSCONFIG)
class ServerProperties(ResourceProperties):
    AssociatePublicIpAddress = attrib(default=None)
    BackupId = attrib(default=None)
    BackupRetentionCount = attrib(default=None)
    CustomCertificate = attrib(default=None)
    CustomDomain = attrib(default=None)
    CustomPrivateKey = attrib(default=None)
    DisableAutomatedBackup = attrib(default=None)
    Engine = attrib(default=None)
    EngineAttributes = attrib(default=None)
    EngineModel = attrib(default=None)
    EngineVersion = attrib(default=None)
    InstanceProfileArn = attrib(default=None)
    InstanceType = attrib(default=None)
    KeyPair = attrib(default=None)
    PreferredBackupWindow = attrib(default=None)
    PreferredMaintenanceWindow = attrib(default=None)
    SecurityGroupIds = attrib(default=None)
    ServerName = attrib(default=None)
    ServiceRoleArn = attrib(default=None)
    SubnetIds = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Server(Resource):
    """A Server for OpsWorksCM.

    See Also:
        `AWS Cloud Formation documentation for Server
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworkscm-server.html>`_
    """

    RESOURCE_TYPE = "AWS::OpsWorksCM::Server"

    Properties: ServerProperties = attrib(
        factory=ServerProperties, converter=create_object_converter(ServerProperties)
    )
