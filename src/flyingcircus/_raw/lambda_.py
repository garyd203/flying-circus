"""Raw representations of every data type in the AWS Lambda service.

See Also:
    `AWS developer guide for Lambda
    <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from typing import Any
from typing import Dict

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Alias",
    "AliasProperties",
    "EventSourceMapping",
    "EventSourceMappingProperties",
    "Function",
    "FunctionProperties",
    "LayerVersion",
    "LayerVersionProperties",
    "LayerVersionPermission",
    "LayerVersionPermissionProperties",
    "Permission",
    "PermissionProperties",
    "Version",
    "VersionProperties",
]


@attrs(**ATTRSCONFIG)
class AliasProperties(ResourceProperties):
    Description = attrib(default=None)
    FunctionName = attrib(default=None)
    FunctionVersion = attrib(default=None)
    Name = attrib(default=None)
    RoutingConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Alias(Resource):
    """A Alias for Lambda.

    See Also:
        `AWS Cloud Formation documentation for Alias
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::Alias"

    Properties: AliasProperties = attrib(
        factory=AliasProperties, converter=create_object_converter(AliasProperties)
    )

    # NB: UpdatePolicy may be set for Alias
    # (unlike most Resource types)
    UpdatePolicy: Dict[str, Any] = attrib(factory=dict)


@attrs(**ATTRSCONFIG)
class EventSourceMappingProperties(ResourceProperties):
    BatchSize = attrib(default=None)
    Enabled = attrib(default=None)
    EventSourceArn = attrib(default=None)
    FunctionName = attrib(default=None)
    StartingPosition = attrib(default=None)


@attrs(**ATTRSCONFIG)
class EventSourceMapping(Resource):
    """A Event Source Mapping for Lambda.

    See Also:
        `AWS Cloud Formation documentation for EventSourceMapping
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::EventSourceMapping"

    Properties: EventSourceMappingProperties = attrib(
        factory=EventSourceMappingProperties,
        converter=create_object_converter(EventSourceMappingProperties),
    )


@attrs(**ATTRSCONFIG)
class FunctionProperties(ResourceProperties):
    Code = attrib(default=None)
    DeadLetterConfig = attrib(default=None)
    Description = attrib(default=None)
    Environment = attrib(default=None)
    FunctionName = attrib(default=None)
    Handler = attrib(default=None)
    KmsKeyArn = attrib(default=None)
    Layers = attrib(default=None)
    MemorySize = attrib(default=None)
    ReservedConcurrentExecutions = attrib(default=None)
    Role = attrib(default=None)
    Runtime = attrib(default=None)
    Tags = attrib(default=None)
    Timeout = attrib(default=None)
    TracingConfig = attrib(default=None)
    VpcConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Function(Resource):
    """A Function for Lambda.

    See Also:
        `AWS Cloud Formation documentation for Function
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::Function"

    Properties: FunctionProperties = attrib(
        factory=FunctionProperties,
        converter=create_object_converter(FunctionProperties),
    )


@attrs(**ATTRSCONFIG)
class LayerVersionProperties(ResourceProperties):
    CompatibleRuntimes = attrib(default=None)
    Content = attrib(default=None)
    Description = attrib(default=None)
    LayerName = attrib(default=None)
    LicenseInfo = attrib(default=None)


@attrs(**ATTRSCONFIG)
class LayerVersion(Resource):
    """A Layer Version for Lambda.

    See Also:
        `AWS Cloud Formation documentation for LayerVersion
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::LayerVersion"

    Properties: LayerVersionProperties = attrib(
        factory=LayerVersionProperties,
        converter=create_object_converter(LayerVersionProperties),
    )


@attrs(**ATTRSCONFIG)
class LayerVersionPermissionProperties(ResourceProperties):
    Action = attrib(default=None)
    LayerVersionArn = attrib(default=None)
    OrganizationId = attrib(default=None)
    Principal = attrib(default=None)


@attrs(**ATTRSCONFIG)
class LayerVersionPermission(Resource):
    """A Layer Version Permission for Lambda.

    See Also:
        `AWS Cloud Formation documentation for LayerVersionPermission
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::LayerVersionPermission"

    Properties: LayerVersionPermissionProperties = attrib(
        factory=LayerVersionPermissionProperties,
        converter=create_object_converter(LayerVersionPermissionProperties),
    )


@attrs(**ATTRSCONFIG)
class PermissionProperties(ResourceProperties):
    Action = attrib(default=None)
    EventSourceToken = attrib(default=None)
    FunctionName = attrib(default=None)
    Principal = attrib(default=None)
    SourceAccount = attrib(default=None)
    SourceArn = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Permission(Resource):
    """A Permission for Lambda.

    See Also:
        `AWS Cloud Formation documentation for Permission
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::Permission"

    Properties: PermissionProperties = attrib(
        factory=PermissionProperties,
        converter=create_object_converter(PermissionProperties),
    )


@attrs(**ATTRSCONFIG)
class VersionProperties(ResourceProperties):
    CodeSha256 = attrib(default=None)
    Description = attrib(default=None)
    FunctionName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Version(Resource):
    """A Version for Lambda.

    See Also:
        `AWS Cloud Formation documentation for Version
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html>`_
    """

    RESOURCE_TYPE = "AWS::Lambda::Version"

    Properties: VersionProperties = attrib(
        factory=VersionProperties, converter=create_object_converter(VersionProperties)
    )
