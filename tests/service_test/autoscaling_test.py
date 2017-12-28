"""Tests for AutoScalingGroup functionality."""

from flyingcircus.core import dedent
from flyingcircus.service.autoscaling import autoscaling_group_by_cpu
from ..validation_helper import AwsTemplateValidation


class TestCpuAutoScalingGroup:
    """Test the behaviour of a CPU-based auto-scaling group."""

    ASG_WITH_CPU_YAML = dedent("""
        ---
        AWSTemplateFormatVersion: '2010-09-09'
        Description: |
          Deploy an auto-scaling group that scales based on lower and upper CPU usage
          thresholds.
        Parameters: {}
        Resources:
          AutoScalingGroup:
            Type: AWS::AutoScaling::AutoScalingGroup
            Properties:
              AvailabilityZones:
                Fn::GetAZs: !Ref AWS::Region
              LaunchConfigurationName: !Ref LaunchConfiguration
              MaxSize: 3
              MinSize: 1
          CPUAlarmHigh:
            Type: AWS::CloudWatch::Alarm
            Properties:
              AlarmActions:
              - !Ref ScaleUpPolicy
              AlarmDescription: |-
                Alarm if CPU too high or metric disappears indicating instance is down
              ComparisonOperator: GreaterThanThreshold
              Dimensions:
              - Name: AutoScalingGroupName
                Value: !Ref AutoScalingGroup
              EvaluationPeriods: 1
              MetricName: CPUUtilization
              Namespace: AWS/EC2
              Period: 60
              Statistic: Average
              Threshold: 74
          CPUAlarmLow:
            Type: AWS::CloudWatch::Alarm
            Properties:
              AlarmActions:
              - !Ref ScaleDownPolicy
              AlarmDescription: |-
                Alarm if CPU too low or metric disappears indicating instance is down
              ComparisonOperator: LessThanThreshold
              Dimensions:
              - Name: AutoScalingGroupName
                Value: !Ref AutoScalingGroup
              EvaluationPeriods: 1
              MetricName: CPUUtilization
              Namespace: AWS/EC2
              Period: 60
              Statistic: Average
              Threshold: 49
          LaunchConfiguration:
            Type: AWS::AutoScaling::LaunchConfiguration
            Properties:
              ImageId: ami-1a668878
              InstanceType: t2.micro
          ScaleDownPolicy:
            Type: AWS::AutoScaling::ScalingPolicy
            Properties:
              AdjustmentType: ChangeInCapacity
              AutoScalingGroupName: !Ref AutoScalingGroup
              Cooldown: 1
              ScalingAdjustment: -1
          ScaleUpPolicy:
            Type: AWS::AutoScaling::ScalingPolicy
            Properties:
              AdjustmentType: ChangeInCapacity
              AutoScalingGroupName: !Ref AutoScalingGroup
              Cooldown: 1
              ScalingAdjustment: 1
    """)

    def test_yaml(self):
        stack = autoscaling_group_by_cpu(low=49, high=74)

        template = stack.export("yaml")

        assert template == self.ASG_WITH_CPU_YAML


class TestValidateAutoScalingService(AwsTemplateValidation):
    """Verify that all convenience functions Autoscaling service module
    produce stacks that are valid.
    """

    def get_stacks_under_test(self):
        return [
            autoscaling_group_by_cpu(),
            # TODO simple_scaling_policy
        ]
