"""Raw representations of every data type in the AWS ServiceDiscovery service.

See Also:
    `AWS developer guide for ServiceDiscovery
    <https://docs.aws.amazon.com/cloud-map/latest/dg/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "HttpNamespace",
    "HttpNamespaceProperties",
    "Instance",
    "InstanceProperties",
    "PrivateDnsNamespace",
    "PrivateDnsNamespaceProperties",
    "PublicDnsNamespace",
    "PublicDnsNamespaceProperties",
    "Service",
    "ServiceProperties",
]


@attrs(**ATTRSCONFIG)
class HttpNamespaceProperties(ResourceProperties):
    Description = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class HttpNamespace(Resource):
    """A Http Namespace for ServiceDiscovery.

    See Also:
        `AWS Cloud Formation documentation for HttpNamespace
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceDiscovery::HttpNamespace"

    Properties: HttpNamespaceProperties = attrib(
        factory=HttpNamespaceProperties,
        converter=create_object_converter(HttpNamespaceProperties),
    )


@attrs(**ATTRSCONFIG)
class InstanceProperties(ResourceProperties):
    InstanceAttributes = attrib(default=None)
    InstanceId = attrib(default=None)
    ServiceId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Instance(Resource):
    """A Instance for ServiceDiscovery.

    See Also:
        `AWS Cloud Formation documentation for Instance
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceDiscovery::Instance"

    Properties: InstanceProperties = attrib(
        factory=InstanceProperties,
        converter=create_object_converter(InstanceProperties),
    )


@attrs(**ATTRSCONFIG)
class PrivateDnsNamespaceProperties(ResourceProperties):
    Description = attrib(default=None)
    Name = attrib(default=None)
    Vpc = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PrivateDnsNamespace(Resource):
    """A Private Dns Namespace for ServiceDiscovery.

    See Also:
        `AWS Cloud Formation documentation for PrivateDnsNamespace
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceDiscovery::PrivateDnsNamespace"

    Properties: PrivateDnsNamespaceProperties = attrib(
        factory=PrivateDnsNamespaceProperties,
        converter=create_object_converter(PrivateDnsNamespaceProperties),
    )


@attrs(**ATTRSCONFIG)
class PublicDnsNamespaceProperties(ResourceProperties):
    Description = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PublicDnsNamespace(Resource):
    """A Public Dns Namespace for ServiceDiscovery.

    See Also:
        `AWS Cloud Formation documentation for PublicDnsNamespace
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceDiscovery::PublicDnsNamespace"

    Properties: PublicDnsNamespaceProperties = attrib(
        factory=PublicDnsNamespaceProperties,
        converter=create_object_converter(PublicDnsNamespaceProperties),
    )


@attrs(**ATTRSCONFIG)
class ServiceProperties(ResourceProperties):
    Description = attrib(default=None)
    DnsConfig = attrib(default=None)
    HealthCheckConfig = attrib(default=None)
    HealthCheckCustomConfig = attrib(default=None)
    Name = attrib(default=None)
    NamespaceId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Service(Resource):
    """A Service for ServiceDiscovery.

    See Also:
        `AWS Cloud Formation documentation for Service
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceDiscovery::Service"

    Properties: ServiceProperties = attrib(
        factory=ServiceProperties,
        converter=create_object_converter(ServiceProperties),
    )
