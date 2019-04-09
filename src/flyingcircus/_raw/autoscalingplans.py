"""Raw representations of every data type in the AWS AutoScalingPlans service.

See Also:
    `AWS developer guide for AutoScalingPlans
    <https://docs.aws.amazon.com/autoscaling/plans/userguide/>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["ScalingPlan", "ScalingPlanProperties"]


@attrs(**ATTRSCONFIG)
class ScalingPlanProperties(ResourceProperties):
    ApplicationSource = attrib(default=None)
    ScalingInstructions = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ScalingPlan(Resource):
    """A Scaling Plan for AutoScalingPlans.

    See Also:
        `AWS Cloud Formation documentation for ScalingPlan
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-autoscalingplans-scalingplan.html>`_
    """

    RESOURCE_TYPE = "AWS::AutoScalingPlans::ScalingPlan"

    Properties: ScalingPlanProperties = attrib(
        factory=ScalingPlanProperties,
        converter=create_object_converter(ScalingPlanProperties),
    )
