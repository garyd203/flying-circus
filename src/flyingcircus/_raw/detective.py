"""Raw representations of every data type in the AWS Detective service.

See Also:
    `AWS developer guide for Detective
    <https://docs.aws.amazon.com/detective/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Graph", "GraphProperties", "MemberInvitation", "MemberInvitationProperties"]


@attrs(**ATTRSCONFIG)
class GraphProperties(ResourceProperties):
    # A Graph doesn't actually have any Properties.
    pass


@attrs(**ATTRSCONFIG)
class Graph(Resource):
    """A Graph for Detective.

    See Also:
        `AWS Cloud Formation documentation for Graph
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html>`_
    """

    RESOURCE_TYPE = "AWS::Detective::Graph"

    Properties: GraphProperties = attrib(
        factory=GraphProperties, converter=create_object_converter(GraphProperties)
    )


@attrs(**ATTRSCONFIG)
class MemberInvitationProperties(ResourceProperties):
    GraphArn = attrib(default=None)
    MemberEmailAddress = attrib(default=None)
    MemberId = attrib(default=None)
    Message = attrib(default=None)


@attrs(**ATTRSCONFIG)
class MemberInvitation(Resource):
    """A Member Invitation for Detective.

    See Also:
        `AWS Cloud Formation documentation for MemberInvitation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html>`_
    """

    RESOURCE_TYPE = "AWS::Detective::MemberInvitation"

    Properties: MemberInvitationProperties = attrib(
        factory=MemberInvitationProperties,
        converter=create_object_converter(MemberInvitationProperties),
    )
