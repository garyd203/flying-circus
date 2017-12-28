"""General-use classes to interact with the AutoScaling service through CloudFormation."""

from flyingcircus import fn
from flyingcircus.core import AWS_Region
from flyingcircus.core import Stack
from flyingcircus.core import dedent
from . import cloudwatch
from .._raw import autoscaling as raw

# TODO rethink this approach. maybe an __all__, or a from _raw import * ?
AutoScalingGroup = raw.AutoScalingGroup
LaunchConfiguration = raw.LaunchConfiguration
ScalingPolicy = raw.ScalingPolicy


def autoscaling_group_by_cpu(low=20, high=80):
    """Create an auto-scaling group that scales based on it's CPU load."""
    stack = Stack(
        # TODO generate description by auto-breaking the line with the (not-yet-existent) reflow function instead
        Description=dedent("""
            Deploy an auto-scaling group that scales based on lower and upper CPU usage
            thresholds.
            """),
    )

    launch_config = LaunchConfiguration(
        Properties=dict(
            ImageId="ami-1a668878",  # Amazon Linux 2017.09.01 in ap-southeast-2
            InstanceType="t2.micro",  # TODO consider making this a lookup value
            #TODO KeyName would probably be helpful
        ),
    )
    stack.Resources["LaunchConfiguration"] = launch_config

    asg = AutoScalingGroup(
        Properties=dict(
            AvailabilityZones=fn.GetAZs(fn.Ref(AWS_Region)),
            LaunchConfigurationName=fn.Ref(launch_config),
            MinSize=1,
            MaxSize=3,
        ),
    )
    stack.Resources["AutoScalingGroup"] = asg

    scale_up_policy = ScalingPolicy(
        Properties=dict(
            AdjustmentType="ChangeInCapacity",  # TODO consider making this a lookup value
            AutoScalingGroupName=fn.Ref(asg),
            Cooldown=1,
            ScalingAdjustment=1,
        ),
    )
    stack.Resources["ScaleUpPolicy"] = scale_up_policy

    high_alarm = cloudwatch.Alarms.high_cpu(threshold=high)
    # FIXME need properties to be a real object (not a dict), and to auto-create empty lists. Then we can do an append here, rather than setting the list
    high_alarm.Properties['AlarmActions'] = [fn.Ref(scale_up_policy)]
    high_alarm.Properties['Dimensions'] = [
        # TODO logical class that wraps this up instead, and allows you to express in a mroe convenient way
        dict(
            Name="AutoScalingGroupName",
            Value=fn.Ref(asg),
        )
    ]
    stack.Resources["CPUAlarmHigh"] = high_alarm

    scale_down_policy = ScalingPolicy(
        Properties=dict(
            AdjustmentType="ChangeInCapacity",  # TODO consider making this a lookup value
            AutoScalingGroupName=fn.Ref(asg),
            Cooldown=1,
            ScalingAdjustment=-1,
        ),
    )
    stack.Resources["ScaleDownPolicy"] = scale_down_policy

    low_alarm = cloudwatch.Alarms.low_cpu(threshold=low)
    # FIXME need properties to be a real object (not a dict), and to auto-create empty lists. Then we can do an append here, rather than setting the list
    low_alarm.Properties['AlarmActions'] = [fn.Ref(scale_down_policy)]
    low_alarm.Properties['Dimensions'] = [
        # TODO logical class that wraps this up instead, and allows you to express in a mroe convenient way
        dict(
            Name="AutoScalingGroupName",
            Value=fn.Ref(asg),
        )
    ]
    stack.Resources["CPUAlarmLow"] = low_alarm

    return stack


def simple_scaling_policy(alarm, asg_name, downscale=False):
    """Create a simple scaling policy using the supplied alarm."""
    # TODO #61: need stack merge to work before this is usable
    stack = Stack(Description="Resources for a single scaling policy.")

    scaling_policy = ScalingPolicy(
        Properties=dict(
            AdjustmentType="ChangeInCapacity",  # TODO consider making this a lookup value
            AutoScalingGroupName=asg_name,
            Cooldown=1,
            ScalingAdjustment=-1 if downscale else 1,
        ),
    )
    stack.Resources["ScalingPolicy"] = scaling_policy

    # TODO need properties to be a real object (not a dict), and to auto-create empty lists.
    alarm.Properties.setdefault("AlarmActions", []).append(fn.Ref(scaling_policy))
    stack.Resources["ScalingAlarm"] = alarm

    return stack
