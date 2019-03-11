"""Raw representations of every data type in the AWS KinesisFirehose service.

See Also:
    `AWS developer guide for KinesisFirehose
    <https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "DeliveryStream",
    "DeliveryStreamProperties",
]


@attrs(**ATTRSCONFIG)
class DeliveryStreamProperties(ResourceProperties):
    DeliveryStreamName = attrib(default=None)
    DeliveryStreamType = attrib(default=None)
    ElasticsearchDestinationConfiguration = attrib(default=None)
    ExtendedS3DestinationConfiguration = attrib(default=None)
    KinesisStreamSourceConfiguration = attrib(default=None)
    RedshiftDestinationConfiguration = attrib(default=None)
    S3DestinationConfiguration = attrib(default=None)
    SplunkDestinationConfiguration = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DeliveryStream(Resource):
    """A Delivery Stream for KinesisFirehose.

    See Also:
        `AWS Cloud Formation documentation for DeliveryStream
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html>`_
    """

    RESOURCE_TYPE = "AWS::KinesisFirehose::DeliveryStream"

    Properties: DeliveryStreamProperties = attrib(
        factory=DeliveryStreamProperties,
        converter=create_object_converter(DeliveryStreamProperties),
    )