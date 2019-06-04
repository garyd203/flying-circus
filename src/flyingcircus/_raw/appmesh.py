"""Raw representations of every data type in the AWS AppMesh service.

See Also:
    `AWS developer guide for AppMesh
    <https://docs.aws.amazon.com/app-mesh/?id=docs_gateway>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Mesh",
    "MeshProperties",
    "Route",
    "RouteProperties",
    "VirtualNode",
    "VirtualNodeProperties",
    "VirtualRouter",
    "VirtualRouterProperties",
    "VirtualService",
    "VirtualServiceProperties",
]


@attrs(**ATTRSCONFIG)
class MeshProperties(ResourceProperties):
    MeshName = attrib(default=None)
    Spec = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Mesh(Resource):
    """A Mesh for AppMesh.

    See Also:
        `AWS Cloud Formation documentation for Mesh
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-mesh.html>`_
    """

    RESOURCE_TYPE = "AWS::AppMesh::Mesh"

    Properties: MeshProperties = attrib(
        factory=MeshProperties, converter=create_object_converter(MeshProperties)
    )


@attrs(**ATTRSCONFIG)
class RouteProperties(ResourceProperties):
    MeshName = attrib(default=None)
    RouteName = attrib(default=None)
    Spec = attrib(default=None)
    Tags = attrib(default=None)
    VirtualRouterName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Route(Resource):
    """A Route for AppMesh.

    See Also:
        `AWS Cloud Formation documentation for Route
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-route.html>`_
    """

    RESOURCE_TYPE = "AWS::AppMesh::Route"

    Properties: RouteProperties = attrib(
        factory=RouteProperties, converter=create_object_converter(RouteProperties)
    )


@attrs(**ATTRSCONFIG)
class VirtualNodeProperties(ResourceProperties):
    MeshName = attrib(default=None)
    Spec = attrib(default=None)
    Tags = attrib(default=None)
    VirtualNodeName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class VirtualNode(Resource):
    """A Virtual Node for AppMesh.

    See Also:
        `AWS Cloud Formation documentation for VirtualNode
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualnode.html>`_
    """

    RESOURCE_TYPE = "AWS::AppMesh::VirtualNode"

    Properties: VirtualNodeProperties = attrib(
        factory=VirtualNodeProperties,
        converter=create_object_converter(VirtualNodeProperties),
    )


@attrs(**ATTRSCONFIG)
class VirtualRouterProperties(ResourceProperties):
    MeshName = attrib(default=None)
    Spec = attrib(default=None)
    Tags = attrib(default=None)
    VirtualRouterName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class VirtualRouter(Resource):
    """A Virtual Router for AppMesh.

    See Also:
        `AWS Cloud Formation documentation for VirtualRouter
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualrouter.html>`_
    """

    RESOURCE_TYPE = "AWS::AppMesh::VirtualRouter"

    Properties: VirtualRouterProperties = attrib(
        factory=VirtualRouterProperties,
        converter=create_object_converter(VirtualRouterProperties),
    )


@attrs(**ATTRSCONFIG)
class VirtualServiceProperties(ResourceProperties):
    MeshName = attrib(default=None)
    Spec = attrib(default=None)
    Tags = attrib(default=None)
    VirtualServiceName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class VirtualService(Resource):
    """A Virtual Service for AppMesh.

    See Also:
        `AWS Cloud Formation documentation for VirtualService
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appmesh-virtualservice.html>`_
    """

    RESOURCE_TYPE = "AWS::AppMesh::VirtualService"

    Properties: VirtualServiceProperties = attrib(
        factory=VirtualServiceProperties,
        converter=create_object_converter(VirtualServiceProperties),
    )