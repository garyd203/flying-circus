"""Raw representations of every data type in the AWS AutoScaling service.

See Also:
    `AWS developer guide for AutoScaling
    <http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html>`_

This file is automatically generated, and should not be directly edited.
"""

from ..core import Resource

__all__ = [
    "AutoScalingGroup",
    "LaunchConfiguration",
    "LifecycleHook",
    "ScalingPolicy",
    "ScheduledAction",
]


class AutoScalingGroup(Resource):
    """A Auto Scaling Group for AutoScaling.

    See Also:
        `AWS Cloud Formation documentation for AutoScalingGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html>`_
    """

    # NB: CreationPolicy and UpdatePolicy can be set for AutoScalingGroup
    # (unlike most Resource types)
    AWS_ATTRIBUTES = Resource.AWS_ATTRIBUTES.union({
        "CreationPolicy",
        "UpdatePolicy",
    })

    RESOURCE_TYPE = "AWS::AutoScaling::AutoScalingGroup"

    RESOURCE_PROPERTIES = {
        "AutoScalingGroupName",
        "AvailabilityZones",
        "Cooldown",
        "DesiredCapacity",
        "HealthCheckGracePeriod",
        "HealthCheckType",
        "InstanceId",
        "LaunchConfigurationName",
        "LaunchTemplate",
        "LifecycleHookSpecificationList",
        "LoadBalancerNames",
        "MaxSize",
        "MetricsCollection",
        "MinSize",
        "NotificationConfigurations",
        "PlacementGroup",
        "ServiceLinkedRoleARN",
        "Tags",
        "TargetGroupARNs",
        "TerminationPolicies",
        "VPCZoneIdentifier",
    }

    # noinspection PyPep8Naming
    def __init__(
            self, CreationPolicy=None, DeletionPolicy=None, DependsOn=None,
            Properties=None, UpdatePolicy=None
    ):
        Resource.__init__(self, DeletionPolicy=DeletionPolicy, DependsOn=DependsOn, Properties=Properties)
        self._set_constructor_attributes({
            "CreationPolicy": CreationPolicy,
            "UpdatePolicy": UpdatePolicy,
        })


class LaunchConfiguration(Resource):
    """A Launch Configuration for AutoScaling.

    See Also:
        `AWS Cloud Formation documentation for LaunchConfiguration
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html>`_
    """

    RESOURCE_TYPE = "AWS::AutoScaling::LaunchConfiguration"

    RESOURCE_PROPERTIES = {
        "AssociatePublicIpAddress",
        "BlockDeviceMappings",
        "ClassicLinkVPCId",
        "ClassicLinkVPCSecurityGroups",
        "EbsOptimized",
        "IamInstanceProfile",
        "ImageId",
        "InstanceId",
        "InstanceMonitoring",
        "InstanceType",
        "KernelId",
        "KeyName",
        "LaunchConfigurationName",
        "PlacementTenancy",
        "RamDiskId",
        "SecurityGroups",
        "SpotPrice",
        "UserData",
    }


class LifecycleHook(Resource):
    """A Lifecycle Hook for AutoScaling.

    See Also:
        `AWS Cloud Formation documentation for LifecycleHook
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html>`_
    """

    RESOURCE_TYPE = "AWS::AutoScaling::LifecycleHook"

    RESOURCE_PROPERTIES = {
        "AutoScalingGroupName",
        "DefaultResult",
        "HeartbeatTimeout",
        "LifecycleHookName",
        "LifecycleTransition",
        "NotificationMetadata",
        "NotificationTargetARN",
        "RoleARN",
    }


class ScalingPolicy(Resource):
    """A Scaling Policy for AutoScaling.

    See Also:
        `AWS Cloud Formation documentation for ScalingPolicy
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html>`_
    """

    RESOURCE_TYPE = "AWS::AutoScaling::ScalingPolicy"

    RESOURCE_PROPERTIES = {
        "AdjustmentType",
        "AutoScalingGroupName",
        "Cooldown",
        "EstimatedInstanceWarmup",
        "MetricAggregationType",
        "MinAdjustmentMagnitude",
        "PolicyType",
        "ScalingAdjustment",
        "StepAdjustments",
        "TargetTrackingConfiguration",
    }


class ScheduledAction(Resource):
    """A Scheduled Action for AutoScaling.

    See Also:
        `AWS Cloud Formation documentation for ScheduledAction
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html>`_
    """

    RESOURCE_TYPE = "AWS::AutoScaling::ScheduledAction"

    RESOURCE_PROPERTIES = {
        "AutoScalingGroupName",
        "DesiredCapacity",
        "EndTime",
        "MaxSize",
        "MinSize",
        "Recurrence",
        "StartTime",
    }
