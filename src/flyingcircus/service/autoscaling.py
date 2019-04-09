"""General-use classes to interact with the AutoScaling service through CloudFormation.

See Also:
    `AWS developer guide for AutoScaling
     <http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html>`_
"""

from flyingcircus import Fn
from flyingcircus.core import AWS_Region
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from . import cloudwatch

# noinspection PyUnresolvedReferences
from .._raw import autoscaling as _raw

# noinspection PyUnresolvedReferences
from .._raw.autoscaling import *


def autoscaling_group_by_cpu(low=20, high=80):
    """Create an auto-scaling group that scales based on it's CPU load."""
    # TODO this is more like a recipe than a basic service
    stack = Stack(
        # TODO generate description by auto-breaking the line with the (not-yet-existent) reflow function instead
        Description=dedent(
            """
            Deploy an auto-scaling group that scales based on lower and upper CPU usage
            thresholds.
            """
        )
    )

    launch_config = stack.Resources["LaunchConfiguration"] = LaunchConfiguration(
        Properties=LaunchConfigurationProperties(
            ImageId="ami-1a668878",  # Amazon Linux 2017.09.01 in ap-southeast-2
            InstanceType="t2.micro",  # TODO consider making this a lookup value
            # TODO KeyName would probably be helpful
        )
    )

    asg = stack.Resources["AutoScalingGroup"] = AutoScalingGroup(
        Properties=AutoScalingGroupProperties(
            AvailabilityZones=Fn.GetAZs(Fn.Ref(AWS_Region)),
            LaunchConfigurationName=Fn.Ref(launch_config),
            MinSize=1,
            MaxSize=3,
        )
    )

    stack.merge_stack(
        simple_scaling_policy(
            cloudwatch.Alarms.high_cpu(threshold=high), Fn.Ref(asg), downscale=False
        ).with_prefixed_names("ScaleUp")
    ).merge_stack(
        simple_scaling_policy(
            cloudwatch.Alarms.low_cpu(threshold=low), Fn.Ref(asg), downscale=True
        ).with_prefixed_names("ScaleDown")
    )

    return stack


def simple_scaling_policy(alarm, asg_name, downscale=False):
    """Create a simple scaling policy using the supplied alarm."""
    stack = Stack(Description="Resources for a single scaling policy.")

    scaling_policy = ScalingPolicy(
        Properties=ScalingPolicyProperties(
            AdjustmentType="ChangeInCapacity",  # TODO consider making this a lookup value
            AutoScalingGroupName=asg_name,
            Cooldown=1,
            ScalingAdjustment=-1 if downscale else 1,
        )
    )
    stack.Resources["ScalingPolicy"] = scaling_policy

    # TODO need properties to auto-create empty lists.
    if alarm.Properties.AlarmActions is None:
        alarm.Properties.AlarmActions = []
    if alarm.Properties.Dimensions is None:
        alarm.Properties.Dimensions = []

    alarm.Properties.AlarmActions.append(Fn.Ref(scaling_policy))
    alarm.Properties.Dimensions.append(
        # TODO logical class that wraps this up instead, and allows you to express in a mroe convenient way
        dict(Name="AutoScalingGroupName", Value=asg_name)
    )
    stack.Resources["ScalingAlarm"] = alarm

    return stack
