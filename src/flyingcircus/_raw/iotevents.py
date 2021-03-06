"""Raw representations of every data type in the AWS IoTEvents service.

See Also:
    `AWS developer guide for IoTEvents
    <https://docs.aws.amazon.com/iotevents/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["DetectorModel", "DetectorModelProperties", "Input", "InputProperties"]


@attrs(**ATTRSCONFIG)
class DetectorModelProperties(ResourceProperties):
    DetectorModelDefinition = attrib(default=None)
    DetectorModelDescription = attrib(default=None)
    DetectorModelName = attrib(default=None)
    Key = attrib(default=None)
    RoleArn = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DetectorModel(Resource):
    """A Detector Model for IoTEvents.

    See Also:
        `AWS Cloud Formation documentation for DetectorModel
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTEvents::DetectorModel"

    Properties: DetectorModelProperties = attrib(
        factory=DetectorModelProperties,
        converter=create_object_converter(DetectorModelProperties),
    )


@attrs(**ATTRSCONFIG)
class InputProperties(ResourceProperties):
    InputDefinition = attrib(default=None)
    InputDescription = attrib(default=None)
    InputName = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Input(Resource):
    """A Input for IoTEvents.

    See Also:
        `AWS Cloud Formation documentation for Input
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html>`_
    """

    RESOURCE_TYPE = "AWS::IoTEvents::Input"

    Properties: InputProperties = attrib(
        factory=InputProperties, converter=create_object_converter(InputProperties)
    )
