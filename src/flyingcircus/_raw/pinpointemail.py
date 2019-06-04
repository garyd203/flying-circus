"""Raw representations of every data type in the AWS PinpointEmail service.

See Also:
    `AWS developer guide for PinpointEmail
    <http://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "ConfigurationSet",
    "ConfigurationSetProperties",
    "ConfigurationSetEventDestination",
    "ConfigurationSetEventDestinationProperties",
    "DedicatedIpPool",
    "DedicatedIpPoolProperties",
    "Identity",
    "IdentityProperties",
]


@attrs(**ATTRSCONFIG)
class ConfigurationSetProperties(ResourceProperties):
    DeliveryOptions = attrib(default=None)
    Name = attrib(default=None)
    ReputationOptions = attrib(default=None)
    SendingOptions = attrib(default=None)
    Tags = attrib(default=None)
    TrackingOptions = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConfigurationSet(Resource):
    """A Configuration Set for PinpointEmail.

    See Also:
        `AWS Cloud Formation documentation for ConfigurationSet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationset.html>`_
    """

    RESOURCE_TYPE = "AWS::PinpointEmail::ConfigurationSet"

    Properties: ConfigurationSetProperties = attrib(
        factory=ConfigurationSetProperties,
        converter=create_object_converter(ConfigurationSetProperties),
    )


@attrs(**ATTRSCONFIG)
class ConfigurationSetEventDestinationProperties(ResourceProperties):
    ConfigurationSetName = attrib(default=None)
    EventDestination = attrib(default=None)
    EventDestinationName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConfigurationSetEventDestination(Resource):
    """A Configuration Set Event Destination for PinpointEmail.

    See Also:
        `AWS Cloud Formation documentation for ConfigurationSetEventDestination
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-configurationseteventdestination.html>`_
    """

    RESOURCE_TYPE = "AWS::PinpointEmail::ConfigurationSetEventDestination"

    Properties: ConfigurationSetEventDestinationProperties = attrib(
        factory=ConfigurationSetEventDestinationProperties,
        converter=create_object_converter(ConfigurationSetEventDestinationProperties),
    )


@attrs(**ATTRSCONFIG)
class DedicatedIpPoolProperties(ResourceProperties):
    PoolName = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DedicatedIpPool(Resource):
    """A Dedicated Ip Pool for PinpointEmail.

    See Also:
        `AWS Cloud Formation documentation for DedicatedIpPool
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-dedicatedippool.html>`_
    """

    RESOURCE_TYPE = "AWS::PinpointEmail::DedicatedIpPool"

    Properties: DedicatedIpPoolProperties = attrib(
        factory=DedicatedIpPoolProperties,
        converter=create_object_converter(DedicatedIpPoolProperties),
    )


@attrs(**ATTRSCONFIG)
class IdentityProperties(ResourceProperties):
    DkimSigningEnabled = attrib(default=None)
    FeedbackForwardingEnabled = attrib(default=None)
    MailFromAttributes = attrib(default=None)
    Name = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Identity(Resource):
    """A Identity for PinpointEmail.

    See Also:
        `AWS Cloud Formation documentation for Identity
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pinpointemail-identity.html>`_
    """

    RESOURCE_TYPE = "AWS::PinpointEmail::Identity"

    Properties: IdentityProperties = attrib(
        factory=IdentityProperties,
        converter=create_object_converter(IdentityProperties),
    )