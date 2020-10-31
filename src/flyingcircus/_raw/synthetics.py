"""Raw representations of every data type in the AWS Synthetics service.

See Also:
    `AWS developer guide for Synthetics
    <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Canary", "CanaryProperties"]


@attrs(**ATTRSCONFIG)
class CanaryProperties(ResourceProperties):
    ArtifactS3Location = attrib(default=None)
    Code = attrib(default=None)
    ExecutionRoleArn = attrib(default=None)
    FailureRetentionPeriod = attrib(default=None)
    Name = attrib(default=None)
    RunConfig = attrib(default=None)
    RuntimeVersion = attrib(default=None)
    Schedule = attrib(default=None)
    StartCanaryAfterCreation = attrib(default=None)
    SuccessRetentionPeriod = attrib(default=None)
    Tags = attrib(default=None)
    VPCConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Canary(Resource):
    """A Canary for Synthetics.

    See Also:
        `AWS Cloud Formation documentation for Canary
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html>`_
    """

    RESOURCE_TYPE = "AWS::Synthetics::Canary"

    Properties: CanaryProperties = attrib(
        factory=CanaryProperties, converter=create_object_converter(CanaryProperties)
    )
