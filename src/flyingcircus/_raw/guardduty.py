"""Raw representations of every data type in the AWS GuardDuty service.

See Also:
    `AWS developer guide for GuardDuty
    <https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Detector",
    "DetectorProperties",
    "Filter",
    "FilterProperties",
    "IPSet",
    "IPSetProperties",
    "Master",
    "MasterProperties",
    "Member",
    "MemberProperties",
    "ThreatIntelSet",
    "ThreatIntelSetProperties",
]


@attrs(**ATTRSCONFIG)
class DetectorProperties(ResourceProperties):
    DataSources = attrib(default=None)
    Enable = attrib(default=None)
    FindingPublishingFrequency = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Detector(Resource):
    """A Detector for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for Detector
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-detector.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::Detector"

    Properties: DetectorProperties = attrib(
        factory=DetectorProperties,
        converter=create_object_converter(DetectorProperties),
    )


@attrs(**ATTRSCONFIG)
class FilterProperties(ResourceProperties):
    Action = attrib(default=None)
    Description = attrib(default=None)
    DetectorId = attrib(default=None)
    FindingCriteria = attrib(default=None)
    Name = attrib(default=None)
    Rank = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Filter(Resource):
    """A Filter for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for Filter
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-filter.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::Filter"

    Properties: FilterProperties = attrib(
        factory=FilterProperties, converter=create_object_converter(FilterProperties)
    )


@attrs(**ATTRSCONFIG)
class IPSetProperties(ResourceProperties):
    Activate = attrib(default=None)
    DetectorId = attrib(default=None)
    Format = attrib(default=None)
    Location = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class IPSet(Resource):
    """A Ip Set for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for IPSet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-ipset.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::IPSet"

    Properties: IPSetProperties = attrib(
        factory=IPSetProperties, converter=create_object_converter(IPSetProperties)
    )


@attrs(**ATTRSCONFIG)
class MasterProperties(ResourceProperties):
    DetectorId = attrib(default=None)
    InvitationId = attrib(default=None)
    MasterId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Master(Resource):
    """A Master for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for Master
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-master.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::Master"

    Properties: MasterProperties = attrib(
        factory=MasterProperties, converter=create_object_converter(MasterProperties)
    )


@attrs(**ATTRSCONFIG)
class MemberProperties(ResourceProperties):
    DetectorId = attrib(default=None)
    DisableEmailNotification = attrib(default=None)
    Email = attrib(default=None)
    MemberId = attrib(default=None)
    Message = attrib(default=None)
    Status = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Member(Resource):
    """A Member for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for Member
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-member.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::Member"

    Properties: MemberProperties = attrib(
        factory=MemberProperties, converter=create_object_converter(MemberProperties)
    )


@attrs(**ATTRSCONFIG)
class ThreatIntelSetProperties(ResourceProperties):
    Activate = attrib(default=None)
    DetectorId = attrib(default=None)
    Format = attrib(default=None)
    Location = attrib(default=None)
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ThreatIntelSet(Resource):
    """A Threat Intel Set for GuardDuty.

    See Also:
        `AWS Cloud Formation documentation for ThreatIntelSet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-guardduty-threatintelset.html>`_
    """

    RESOURCE_TYPE = "AWS::GuardDuty::ThreatIntelSet"

    Properties: ThreatIntelSetProperties = attrib(
        factory=ThreatIntelSetProperties,
        converter=create_object_converter(ThreatIntelSetProperties),
    )
