"""Raw representations of every data type in the AWS AppStream service.

See Also:
    `AWS developer guide for AppStream
    <https://docs.aws.amazon.com/appstream2/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "DirectoryConfig",
    "DirectoryConfigProperties",
    "Fleet",
    "FleetProperties",
    "ImageBuilder",
    "ImageBuilderProperties",
    "Stack",
    "StackProperties",
    "StackFleetAssociation",
    "StackFleetAssociationProperties",
    "StackUserAssociation",
    "StackUserAssociationProperties",
    "User",
    "UserProperties",
]


@attrs(**ATTRSCONFIG)
class DirectoryConfigProperties(ResourceProperties):
    DirectoryName = attrib(default=None)
    OrganizationalUnitDistinguishedNames = attrib(default=None)
    ServiceAccountCredentials = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DirectoryConfig(Resource):
    """A Directory Config for AppStream.

    See Also:
        `AWS Cloud Formation documentation for DirectoryConfig
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::DirectoryConfig"

    Properties: DirectoryConfigProperties = attrib(
        factory=DirectoryConfigProperties,
        converter=create_object_converter(DirectoryConfigProperties),
    )


@attrs(**ATTRSCONFIG)
class FleetProperties(ResourceProperties):
    ComputeCapacity = attrib(default=None)
    Description = attrib(default=None)
    DisconnectTimeoutInSeconds = attrib(default=None)
    DisplayName = attrib(default=None)
    DomainJoinInfo = attrib(default=None)
    EnableDefaultInternetAccess = attrib(default=None)
    FleetType = attrib(default=None)
    IamRoleArn = attrib(default=None)
    IdleDisconnectTimeoutInSeconds = attrib(default=None)
    ImageArn = attrib(default=None)
    ImageName = attrib(default=None)
    InstanceType = attrib(default=None)
    MaxUserDurationInSeconds = attrib(default=None)
    Name = attrib(default=None)
    StreamView = attrib(default=None)
    Tags = attrib(default=None)
    VpcConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Fleet(Resource):
    """A Fleet for AppStream.

    See Also:
        `AWS Cloud Formation documentation for Fleet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::Fleet"

    Properties: FleetProperties = attrib(
        factory=FleetProperties, converter=create_object_converter(FleetProperties)
    )


@attrs(**ATTRSCONFIG)
class ImageBuilderProperties(ResourceProperties):
    AccessEndpoints = attrib(default=None)
    AppstreamAgentVersion = attrib(default=None)
    Description = attrib(default=None)
    DisplayName = attrib(default=None)
    DomainJoinInfo = attrib(default=None)
    EnableDefaultInternetAccess = attrib(default=None)
    IamRoleArn = attrib(default=None)
    ImageArn = attrib(default=None)
    ImageName = attrib(default=None)
    InstanceType = attrib(default=None)
    Name = attrib(default=None)
    Tags = attrib(default=None)
    VpcConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ImageBuilder(Resource):
    """A Image Builder for AppStream.

    See Also:
        `AWS Cloud Formation documentation for ImageBuilder
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::ImageBuilder"

    Properties: ImageBuilderProperties = attrib(
        factory=ImageBuilderProperties,
        converter=create_object_converter(ImageBuilderProperties),
    )


@attrs(**ATTRSCONFIG)
class StackProperties(ResourceProperties):
    AccessEndpoints = attrib(default=None)
    ApplicationSettings = attrib(default=None)
    AttributesToDelete = attrib(default=None)
    DeleteStorageConnectors = attrib(default=None)
    Description = attrib(default=None)
    DisplayName = attrib(default=None)
    EmbedHostDomains = attrib(default=None)
    FeedbackURL = attrib(default=None)
    Name = attrib(default=None)
    RedirectURL = attrib(default=None)
    StorageConnectors = attrib(default=None)
    Tags = attrib(default=None)
    UserSettings = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Stack(Resource):
    """A Stack for AppStream.

    See Also:
        `AWS Cloud Formation documentation for Stack
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::Stack"

    Properties: StackProperties = attrib(
        factory=StackProperties, converter=create_object_converter(StackProperties)
    )


@attrs(**ATTRSCONFIG)
class StackFleetAssociationProperties(ResourceProperties):
    FleetName = attrib(default=None)
    StackName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class StackFleetAssociation(Resource):
    """A Stack Fleet Association for AppStream.

    See Also:
        `AWS Cloud Formation documentation for StackFleetAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::StackFleetAssociation"

    Properties: StackFleetAssociationProperties = attrib(
        factory=StackFleetAssociationProperties,
        converter=create_object_converter(StackFleetAssociationProperties),
    )


@attrs(**ATTRSCONFIG)
class StackUserAssociationProperties(ResourceProperties):
    AuthenticationType = attrib(default=None)
    SendEmailNotification = attrib(default=None)
    StackName = attrib(default=None)
    UserName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class StackUserAssociation(Resource):
    """A Stack User Association for AppStream.

    See Also:
        `AWS Cloud Formation documentation for StackUserAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::StackUserAssociation"

    Properties: StackUserAssociationProperties = attrib(
        factory=StackUserAssociationProperties,
        converter=create_object_converter(StackUserAssociationProperties),
    )


@attrs(**ATTRSCONFIG)
class UserProperties(ResourceProperties):
    AuthenticationType = attrib(default=None)
    FirstName = attrib(default=None)
    LastName = attrib(default=None)
    MessageAction = attrib(default=None)
    UserName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class User(Resource):
    """A User for AppStream.

    See Also:
        `AWS Cloud Formation documentation for User
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html>`_
    """

    RESOURCE_TYPE = "AWS::AppStream::User"

    Properties: UserProperties = attrib(
        factory=UserProperties, converter=create_object_converter(UserProperties)
    )
