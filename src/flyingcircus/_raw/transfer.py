"""Raw representations of every data type in the AWS Transfer service.

See Also:
    `AWS developer guide for Transfer
    <https://docs.aws.amazon.com/transfer/latest/userguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Server", "ServerProperties", "User", "UserProperties"]


@attrs(**ATTRSCONFIG)
class ServerProperties(ResourceProperties):
    EndpointDetails = attrib(default=None)
    EndpointType = attrib(default=None)
    IdentityProviderDetails = attrib(default=None)
    IdentityProviderType = attrib(default=None)
    LoggingRole = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Server(Resource):
    """A Server for Transfer.

    See Also:
        `AWS Cloud Formation documentation for Server
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html>`_
    """

    RESOURCE_TYPE = "AWS::Transfer::Server"

    Properties: ServerProperties = attrib(
        factory=ServerProperties, converter=create_object_converter(ServerProperties)
    )


@attrs(**ATTRSCONFIG)
class UserProperties(ResourceProperties):
    HomeDirectory = attrib(default=None)
    Policy = attrib(default=None)
    Role = attrib(default=None)
    ServerId = attrib(default=None)
    SshPublicKeys = attrib(default=None)
    Tags = attrib(default=None)
    UserName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class User(Resource):
    """A User for Transfer.

    See Also:
        `AWS Cloud Formation documentation for User
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html>`_
    """

    RESOURCE_TYPE = "AWS::Transfer::User"

    Properties: UserProperties = attrib(
        factory=UserProperties, converter=create_object_converter(UserProperties)
    )
