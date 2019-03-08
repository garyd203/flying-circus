"""Raw representations of every data type in the AWS SSM service.

See Also:
    `AWS developer guide for SSM
    <https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Association",
    "AssociationProperties",
    "Document",
    "DocumentProperties",
    "MaintenanceWindow",
    "MaintenanceWindowProperties",
    "MaintenanceWindowTask",
    "MaintenanceWindowTaskProperties",
    "Parameter",
    "ParameterProperties",
    "PatchBaseline",
    "PatchBaselineProperties",
    "ResourceDataSync",
    "ResourceDataSyncProperties",
]


@attrs(**ATTRSCONFIG)
class AssociationProperties(ResourceProperties):
    AssociationName = attrib(default=None)
    DocumentVersion = attrib(default=None)
    InstanceId = attrib(default=None)
    Name = attrib(default=None)
    OutputLocation = attrib(default=None)
    Parameters = attrib(default=None)
    ScheduleExpression = attrib(default=None)
    Targets = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Association(Resource):
    """A Association for SSM.

    See Also:
        `AWS Cloud Formation documentation for Association
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::Association"

    Properties: AssociationProperties = attrib(
        factory=AssociationProperties,
        converter=create_object_converter(AssociationProperties),
    )


@attrs(**ATTRSCONFIG)
class DocumentProperties(ResourceProperties):
    Content = attrib(default=None)
    DocumentType = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Document(Resource):
    """A Document for SSM.

    See Also:
        `AWS Cloud Formation documentation for Document
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::Document"

    Properties: DocumentProperties = attrib(
        factory=DocumentProperties,
        converter=create_object_converter(DocumentProperties),
    )


@attrs(**ATTRSCONFIG)
class MaintenanceWindowProperties(ResourceProperties):
    AllowUnassociatedTargets = attrib(default=None)
    Cutoff = attrib(default=None)
    Description = attrib(default=None)
    Duration = attrib(default=None)
    EndDate = attrib(default=None)
    Name = attrib(default=None)
    Schedule = attrib(default=None)
    ScheduleTimezone = attrib(default=None)
    StartDate = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class MaintenanceWindow(Resource):
    """A Maintenance Window for SSM.

    See Also:
        `AWS Cloud Formation documentation for MaintenanceWindow
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::MaintenanceWindow"

    Properties: MaintenanceWindowProperties = attrib(
        factory=MaintenanceWindowProperties,
        converter=create_object_converter(MaintenanceWindowProperties),
    )


@attrs(**ATTRSCONFIG)
class MaintenanceWindowTaskProperties(ResourceProperties):
    Description = attrib(default=None)
    LoggingInfo = attrib(default=None)
    MaxConcurrency = attrib(default=None)
    MaxErrors = attrib(default=None)
    Name = attrib(default=None)
    Priority = attrib(default=None)
    ServiceRoleArn = attrib(default=None)
    Targets = attrib(default=None)
    TaskArn = attrib(default=None)
    TaskInvocationParameters = attrib(default=None)
    TaskParameters = attrib(default=None)
    TaskType = attrib(default=None)
    WindowId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class MaintenanceWindowTask(Resource):
    """A Maintenance Window Task for SSM.

    See Also:
        `AWS Cloud Formation documentation for MaintenanceWindowTask
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::MaintenanceWindowTask"

    Properties: MaintenanceWindowTaskProperties = attrib(
        factory=MaintenanceWindowTaskProperties,
        converter=create_object_converter(MaintenanceWindowTaskProperties),
    )


@attrs(**ATTRSCONFIG)
class ParameterProperties(ResourceProperties):
    AllowedPattern = attrib(default=None)
    Description = attrib(default=None)
    Name = attrib(default=None)
    Type = attrib(default=None)
    Value = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Parameter(Resource):
    """A Parameter for SSM.

    See Also:
        `AWS Cloud Formation documentation for Parameter
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::Parameter"

    Properties: ParameterProperties = attrib(
        factory=ParameterProperties,
        converter=create_object_converter(ParameterProperties),
    )


@attrs(**ATTRSCONFIG)
class PatchBaselineProperties(ResourceProperties):
    ApprovalRules = attrib(default=None)
    ApprovedPatches = attrib(default=None)
    ApprovedPatchesComplianceLevel = attrib(default=None)
    ApprovedPatchesEnableNonSecurity = attrib(default=None)
    Description = attrib(default=None)
    GlobalFilters = attrib(default=None)
    Name = attrib(default=None)
    OperatingSystem = attrib(default=None)
    PatchGroups = attrib(default=None)
    RejectedPatches = attrib(default=None)
    RejectedPatchesAction = attrib(default=None)
    Sources = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PatchBaseline(Resource):
    """A Patch Baseline for SSM.

    See Also:
        `AWS Cloud Formation documentation for PatchBaseline
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::PatchBaseline"

    Properties: PatchBaselineProperties = attrib(
        factory=PatchBaselineProperties,
        converter=create_object_converter(PatchBaselineProperties),
    )


@attrs(**ATTRSCONFIG)
class ResourceDataSyncProperties(ResourceProperties):
    BucketName = attrib(default=None)
    BucketPrefix = attrib(default=None)
    BucketRegion = attrib(default=None)
    KMSKeyArn = attrib(default=None)
    SyncFormat = attrib(default=None)
    SyncName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ResourceDataSync(Resource):
    """A Resource Data Sync for SSM.

    See Also:
        `AWS Cloud Formation documentation for ResourceDataSync
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html>`_
    """

    RESOURCE_TYPE = "AWS::SSM::ResourceDataSync"

    Properties: ResourceDataSyncProperties = attrib(
        factory=ResourceDataSyncProperties,
        converter=create_object_converter(ResourceDataSyncProperties),
    )
