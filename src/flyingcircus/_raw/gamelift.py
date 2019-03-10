"""Raw representations of every data type in the AWS GameLift service.

See Also:
    `AWS developer guide for GameLift
    <https://docs.aws.amazon.com/gamelift/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Alias",
    "AliasProperties",
    "Build",
    "BuildProperties",
    "Fleet",
    "FleetProperties",
]


@attrs(**ATTRSCONFIG)
class AliasProperties(ResourceProperties):
    Description = attrib(default=None)
    Name = attrib(default=None)
    RoutingStrategy = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Alias(Resource):
    """A Alias for GameLift.

    See Also:
        `AWS Cloud Formation documentation for Alias
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html>`_
    """

    RESOURCE_TYPE = "AWS::GameLift::Alias"

    Properties: AliasProperties = attrib(
        factory=AliasProperties,
        converter=create_object_converter(AliasProperties),
    )


@attrs(**ATTRSCONFIG)
class BuildProperties(ResourceProperties):
    Name = attrib(default=None)
    StorageLocation = attrib(default=None)
    Version = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Build(Resource):
    """A Build for GameLift.

    See Also:
        `AWS Cloud Formation documentation for Build
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html>`_
    """

    RESOURCE_TYPE = "AWS::GameLift::Build"

    Properties: BuildProperties = attrib(
        factory=BuildProperties,
        converter=create_object_converter(BuildProperties),
    )


@attrs(**ATTRSCONFIG)
class FleetProperties(ResourceProperties):
    BuildId = attrib(default=None)
    Description = attrib(default=None)
    DesiredEC2Instances = attrib(default=None)
    EC2InboundPermissions = attrib(default=None)
    EC2InstanceType = attrib(default=None)
    LogPaths = attrib(default=None)
    MaxSize = attrib(default=None)
    MinSize = attrib(default=None)
    Name = attrib(default=None)
    ServerLaunchParameters = attrib(default=None)
    ServerLaunchPath = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Fleet(Resource):
    """A Fleet for GameLift.

    See Also:
        `AWS Cloud Formation documentation for Fleet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html>`_
    """

    RESOURCE_TYPE = "AWS::GameLift::Fleet"

    Properties: FleetProperties = attrib(
        factory=FleetProperties,
        converter=create_object_converter(FleetProperties),
    )
