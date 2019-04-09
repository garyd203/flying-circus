"""Raw representations of every data type in the AWS StepFunctions service.

See Also:
    `AWS developer guide for StepFunctions
    <https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Activity", "ActivityProperties", "StateMachine", "StateMachineProperties"]


@attrs(**ATTRSCONFIG)
class ActivityProperties(ResourceProperties):
    Name = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Activity(Resource):
    """A Activity for StepFunctions.

    See Also:
        `AWS Cloud Formation documentation for Activity
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-activity.html>`_
    """

    RESOURCE_TYPE = "AWS::StepFunctions::Activity"

    Properties: ActivityProperties = attrib(
        factory=ActivityProperties,
        converter=create_object_converter(ActivityProperties),
    )


@attrs(**ATTRSCONFIG)
class StateMachineProperties(ResourceProperties):
    DefinitionString = attrib(default=None)
    RoleArn = attrib(default=None)
    StateMachineName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class StateMachine(Resource):
    """A State Machine for StepFunctions.

    See Also:
        `AWS Cloud Formation documentation for StateMachine
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-stepfunctions-statemachine.html>`_
    """

    RESOURCE_TYPE = "AWS::StepFunctions::StateMachine"

    Properties: StateMachineProperties = attrib(
        factory=StateMachineProperties,
        converter=create_object_converter(StateMachineProperties),
    )
