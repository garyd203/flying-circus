"""General-use classes to interact with the AutoScaling service through CloudFormation."""

from flyingcircus.core import Stack, dedent
from . import cloudwatch
from .._raw import autoscaling as raw

# TODO rethink this approach. maybe an __all__, or an from _raw import * ?
AutoScalingGroup = raw.AutoScalingGroup
LaunchConfiguration = raw.LaunchConfiguration
Resource = raw.Resource
ScalingPolicy = raw.ScalingPolicy


# TODO note on how convenience functions will work.
#   We should expect that they will create more than one object, which will not necessarily
#   be a resource. Hence the best interface is for them to return a stack.
#
#   This implies that we will need functionality to combine stacks, eg if we want a stack composed
#   out of 2 convenience functions. Stack combining should:
#       - merge all stack components together and erro on namespace clash
#       - create a new stack, rather than merge into an existing
#           eg. new_stack = stack1 + stack2
#       - have option to add namespace prefix to all (some???) objects in each stack, in order to improve disambiguation
#           eg. new_stack = combine_stacks(stack1, stack2, MagicVariableNameThatBecomesNamespacePrefixForThisStack=stack3)
#           or. new_stack = stack1 + stack2 + stack3.add_namespace_prefix("Prefix")


def autoscaling_group_with_cpu(low=20, high=90):
    # FIXME docstring
    # FIXME rename
    # FIXME tweak default values for cpu thresholds. eg. to match some AWS doco
    stack = Stack(
        # TODO generate description by auto-breaking the line with the (not-yet-existent) reflow function instead
        Description=dedent("""
            Deploy an auto-scaling group that scales based on lower and upper CPU usage
            thresholds.
            """),
        Resources={},  # TODO shouldn't need to initialise this explicitly to an empty dict
    )

    launch_config = LaunchConfiguration(
        Properties=dict(
            ImageId="ami-1a668878",  # Amazon Linux 2017.09.01 in ap-southeast-2
            InstanceType="t2.micro",  # FIXME make this a lookup value
            InstanceMonitoring=False,  # Disable the costly version of monitoring
        ),
    )
    stack.Resources["LaunchConfiguration"] = launch_config  # FIXME set+lookup intrinsic resource name

    asg = AutoScalingGroup(
        Properties=dict(
            AvailabilityZones="Fn::GetAZs: !Ref AWS::Region",  # FIXME need real functions
            LaunchConfigurationName="!Ref LaunchConfiguration",  # FIXME need real !Ref
            MinSize=1,
            MaxSize=3,
        ),
    )
    stack.Resources["AutoScalingGroup"] = asg

    high_alarm = cloudwatch.Alarm(
        Properties=dict(
            EvaluationPeriods=1,
            Statistic="Average",  # FIXME lookup constant
            Threshold=75,
            AlarmDescription="Alarm if CPU too high or metric disappears indicating instance is down",
            Period=60,
            AlarmActions=["!Ref ScaleUpPolicy"],  # FIXME need real !Ref
            Namespace="AWS/EC2",  # FIXME lookup constant?
            Dimensions=[
                # TODO logical class that wraps this up instead, and allows you to express in a mroe convenient way
                dict(
                    Name="AutoScalingGroupName",
                    Value="!Ref AutoScalingGroup",  # FIXME need real !Ref

                ),
            ],
            ComparisonOperator="GreaterThanThreshold",  # FIXME lookup constant
            MetricName="CPUUtilization"  # TODO Lookup a very long list?
        ),
    )
    stack.Resources["CPUAlarmHigh"] = high_alarm

    scale_up_policy = ScalingPolicy(
        Properties=dict(
            AdjustmentType="ChangeInCapacity",  # FIXME lookup constant
            AutoScalingGroupName="!Ref AutoScalingGroup",  # FIXME need real !Ref
            Cooldown=1,
            ScalingAdjustment=1,
        ),
    )
    stack.Resources["ScaleUpPolicy"] = scale_up_policy

    return stack
