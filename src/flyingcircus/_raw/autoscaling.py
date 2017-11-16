"""Raw representations of every data type in the AWS AutoScaling service.

See http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html
"""

from ..core import Resource


class AutoScalingGroup(Resource):
    """An Auto Scaling Group.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
    and http://docs.aws.amazon.com/autoscaling/latest/userguide/AutoScalingGroup.html
    """

    # NB: CreationPolicy and UpdatePolicy are valid for an AutoScalingGroup
    # (unlike most Resource types)
    AWS_ATTRIBUTES = Resource.AWS_ATTRIBUTES.union({"CreationPolicy", "UpdatePolicy"})

    RESOURCE_TYPE = "AWS::AutoScaling::AutoScalingGroup"

    RESOURCE_PROPERTIES = {
        "AvailabilityZones",
        "Cooldown",
        "DesiredCapacity",
        "HealthCheckGracePeriod",
        "HealthCheckType",
        "InstanceId",
        "LaunchConfigurationName",
        "LoadBalancerNames",
        "MaxSize",
        "MetricsCollection",
        "MinSize",
        "NotificationConfigurations",
        "PlacementGroup",
        "Tags",
        "TargetGroupARNs",
        "TerminationPolicies",
        "VPCZoneIdentifier",
    }

    # noinspection PyPep8Naming
    def __init__(
            self, CreationPolicy=None, DeletionPolicy=None,
            DependsOn=None, Properties=None, UpdatePolicy=None
    ):
        current_attribs, other_params = self._split_current_attributes(locals())
        Resource.__init__(**other_params)
        self._set_constructor_attributes(current_attribs)


class LaunchConfiguration(Resource):
    """A Launch Configuration for an Auto Scaling Group

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
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
        "PlacementTenancy",
        "RamDiskId",
        "SecurityGroups",
        "SpotPrice",
        "UserData",
    }


class ScalingPolicy(Resource):
    """A Scaling Policy Configuration for an Auto Scaling Group

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
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
