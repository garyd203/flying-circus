"""Raw representations of every data type in the AWS MediaConvert service.

See Also:
    `AWS developer guide for MediaConvert
    <http://docs.aws.amazon.com/mediaconvert/latest/ug/what-is.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "JobTemplate",
    "JobTemplateProperties",
    "Preset",
    "PresetProperties",
    "Queue",
    "QueueProperties",
]


@attrs(**ATTRSCONFIG)
class JobTemplateProperties(ResourceProperties):
    AccelerationSettings = attrib(default=None)
    Category = attrib(default=None)
    Description = attrib(default=None)
    Name = attrib(default=None)
    Priority = attrib(default=None)
    Queue = attrib(default=None)
    SettingsJson = attrib(default=None)
    StatusUpdateInterval = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class JobTemplate(Resource):
    """A Job Template for MediaConvert.

    See Also:
        `AWS Cloud Formation documentation for JobTemplate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconvert-jobtemplate.html>`_
    """

    RESOURCE_TYPE = "AWS::MediaConvert::JobTemplate"

    Properties: JobTemplateProperties = attrib(
        factory=JobTemplateProperties,
        converter=create_object_converter(JobTemplateProperties),
    )


@attrs(**ATTRSCONFIG)
class PresetProperties(ResourceProperties):
    Category = attrib(default=None)
    Description = attrib(default=None)
    Name = attrib(default=None)
    SettingsJson = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Preset(Resource):
    """A Preset for MediaConvert.

    See Also:
        `AWS Cloud Formation documentation for Preset
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconvert-preset.html>`_
    """

    RESOURCE_TYPE = "AWS::MediaConvert::Preset"

    Properties: PresetProperties = attrib(
        factory=PresetProperties, converter=create_object_converter(PresetProperties)
    )


@attrs(**ATTRSCONFIG)
class QueueProperties(ResourceProperties):
    Description = attrib(default=None)
    Name = attrib(default=None)
    PricingPlan = attrib(default=None)
    Status = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Queue(Resource):
    """A Queue for MediaConvert.

    See Also:
        `AWS Cloud Formation documentation for Queue
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconvert-queue.html>`_
    """

    RESOURCE_TYPE = "AWS::MediaConvert::Queue"

    Properties: QueueProperties = attrib(
        factory=QueueProperties, converter=create_object_converter(QueueProperties)
    )
