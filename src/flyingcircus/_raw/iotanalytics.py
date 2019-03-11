"""Raw representations of every data type in the AWS IoTAnalytics service.

See Also:
    `AWS developer guide for IoTAnalytics
    <https://docs.aws.amazon.com/appsync/latest/devguide/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Channel",
    "ChannelProperties",
    "Dataset",
    "DatasetProperties",
    "Datastore",
    "DatastoreProperties",
    "Pipeline",
    "PipelineProperties",
]


@attrs(**ATTRSCONFIG)
class ChannelProperties(ResourceProperties):
    ChannelName = attrib(default=None)
    RetentionPeriod = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Channel(Resource):
    """A Channel for IoTAnalytics.

    See Also:
        `AWS Cloud Formation documentation for Channel
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTAnalytics::Channel"

    Properties: ChannelProperties = attrib(
        factory=ChannelProperties,
        converter=create_object_converter(ChannelProperties),
    )


@attrs(**ATTRSCONFIG)
class DatasetProperties(ResourceProperties):
    Actions = attrib(default=None)
    DatasetName = attrib(default=None)
    RetentionPeriod = attrib(default=None)
    Tags = attrib(default=None)
    Triggers = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Dataset(Resource):
    """A Dataset for IoTAnalytics.

    See Also:
        `AWS Cloud Formation documentation for Dataset
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTAnalytics::Dataset"

    Properties: DatasetProperties = attrib(
        factory=DatasetProperties,
        converter=create_object_converter(DatasetProperties),
    )


@attrs(**ATTRSCONFIG)
class DatastoreProperties(ResourceProperties):
    DatastoreName = attrib(default=None)
    RetentionPeriod = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Datastore(Resource):
    """A Datastore for IoTAnalytics.

    See Also:
        `AWS Cloud Formation documentation for Datastore
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTAnalytics::Datastore"

    Properties: DatastoreProperties = attrib(
        factory=DatastoreProperties,
        converter=create_object_converter(DatastoreProperties),
    )


@attrs(**ATTRSCONFIG)
class PipelineProperties(ResourceProperties):
    PipelineActivities = attrib(default=None)
    PipelineName = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Pipeline(Resource):
    """A Pipeline for IoTAnalytics.

    See Also:
        `AWS Cloud Formation documentation for Pipeline
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTAnalytics::Pipeline"

    Properties: PipelineProperties = attrib(
        factory=PipelineProperties,
        converter=create_object_converter(PipelineProperties),
    )