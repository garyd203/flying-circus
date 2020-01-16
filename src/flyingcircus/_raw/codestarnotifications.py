"""Raw representations of every data type in the AWS CodeStarNotifications service.

See Also:
    `AWS developer guide for CodeStarNotifications
    <https://docs.aws.amazon.com/codestar-notifications/latest/userguide/>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["NotificationRule", "NotificationRuleProperties"]


@attrs(**ATTRSCONFIG)
class NotificationRuleProperties(ResourceProperties):
    DetailType = attrib(default=None)
    EventTypeIds = attrib(default=None)
    Name = attrib(default=None)
    Resource = attrib(default=None)
    Status = attrib(default=None)
    Tags = attrib(default=None)
    Targets = attrib(default=None)


@attrs(**ATTRSCONFIG)
class NotificationRule(Resource):
    """A Notification Rule for CodeStarNotifications.

    See Also:
        `AWS Cloud Formation documentation for NotificationRule
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html>`_
    """

    RESOURCE_TYPE = "AWS::CodeStarNotifications::NotificationRule"

    Properties: NotificationRuleProperties = attrib(
        factory=NotificationRuleProperties,
        converter=create_object_converter(NotificationRuleProperties),
    )