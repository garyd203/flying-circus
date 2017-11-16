from flyingcircus.core import dedent
from flyingcircus.service.autoscaling import autoscaling_group_with_cpu


class TestCpuAutoScalingGroup:
    """Test the behaviour of a CPU_based auto-scaling group."""

    ASG_WITH_CPU_YAML = dedent("""
        ---
        AWSTemplateFormatVersion: '2010-09-09'
        Description: |
          Deploy an auto-scaling group that scales based on lower and upper CPU usage
          thresholds.
        Resources:
          AutoScalingGroup:
            Type: AWS::AutoScaling::AutoScalingGroup
            Properties:
              AvailabilityZones:
                Fn::GetAZs: !Ref AWS::Region
              LaunchConfigurationName: !Ref LaunchConfiguration
              MinSize: 1
              MaxSize: 3
          LaunchConfiguration:
            Type: AWS::AutoScaling::LaunchConfiguration
            Properties:
              ImageId: ami-1a668878
              InstanceType: t2.micro
              InstanceMonitoring: false
          CPUAlarmHigh:
            Type: AWS::CloudWatch::Alarm
            Properties:
              EvaluationPeriods: 1
              Statistic: Average
              Threshold: 75
              AlarmDescription: Alarm if CPU too high or metric disappears indicating instance is down
              Period: 60
              AlarmActions:
                - !Ref ScaleUpPolicy
              Namespace: AWS/EC2
              Dimensions:
              - Name: AutoScalingGroupName
                Value: !Ref AutoScalingGroup
              ComparisonOperator: GreaterThanThreshold
              MetricName: CPUUtilization
          ScaleUpPolicy:
            Type: AWS::AutoScaling::ScalingPolicy
            Properties:
              AdjustmentType: ChangeInCapacity
              AutoScalingGroupName: !Ref AutoScalingGroup
              Cooldown: 1
              ScalingAdjustment: 1
    """)
    ASG_WITH_CPU_YAML_MUNGED_DELETEME = dedent("""
        ---
        AWSTemplateFormatVersion: '2010-09-09'
        Description: |
          Deploy an auto-scaling group that scales based on lower and upper CPU usage
          thresholds.
        Resources:
          AutoScalingGroup:
            Type: AWS::AutoScaling::AutoScalingGroup
            Properties:
              AvailabilityZones: 'Fn::GetAZs: !Ref AWS::Region'
              LaunchConfigurationName: '!Ref LaunchConfiguration'
              MaxSize: 3
              MinSize: 1
          CPUAlarmHigh:
            Type: AWS::CloudWatch::Alarm
            Properties:
              AlarmActions:
              - '!Ref ScaleUpPolicy'
              AlarmDescription: |-
                Alarm if CPU too high or metric disappears indicating instance is down
              ComparisonOperator: GreaterThanThreshold
              Dimensions:
              - Name: AutoScalingGroupName
                Value: '!Ref AutoScalingGroup'
              EvaluationPeriods: 1
              MetricName: CPUUtilization
              Namespace: AWS/EC2
              Period: 60
              Statistic: Average
              Threshold: 75
          LaunchConfiguration:
            Type: AWS::AutoScaling::LaunchConfiguration
            Properties:
              ImageId: ami-1a668878
              InstanceMonitoring: false
              InstanceType: t2.micro
          ScaleUpPolicy:
            Type: AWS::AutoScaling::ScalingPolicy
            Properties:
              AdjustmentType: ChangeInCapacity
              AutoScalingGroupName: '!Ref AutoScalingGroup'
              Cooldown: 1
              ScalingAdjustment: 1
    """)

    def test_yaml(self):
        stack = autoscaling_group_with_cpu(low=50, high=75)

        template = stack.export("yaml")

        assert template == self.ASG_WITH_CPU_YAML_MUNGED_DELETEME  # FIXME use the real version instead whne we get basic intrinsic functions working
