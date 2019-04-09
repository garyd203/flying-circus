"""General-use classes to interact with the CloudWatch service through CloudFormation.

See Also:
    `AWS developer guide for CloudWatch
     <http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import cloudwatch as _raw

# noinspection PyUnresolvedReferences
from .._raw.cloudwatch import *


class Alarms:
    """Factory methods to create common types of alarm."""

    # TODO: note: We are providing factory functions, not abstractions. This is because one of our core principles is to use native CFN, so managing an abstraction layer on top of that ourselves is unwise.
    # TODO i don't like shipping in the Java idea of using a class as a namespace. prefer a sub-module, but that conflates with the AWS service namespace we are mimicking?

    @staticmethod
    def high_cpu(threshold):
        """An alarm that triggers when CPU is too high
        (or the underlying metric disappears, indicating the instance is down).
        """
        # TODO I think dimension should be a compulsory attribute
        # TODO share code with the cpu_low_alarm implementation
        return Alarm(
            Properties=dict(
                # TODO sort these in some sensible order, perhaps
                EvaluationPeriods=1,
                Statistic="Average",  # FIXME lookup constant
                Threshold=threshold,
                AlarmDescription="Alarm if CPU too high or metric disappears indicating instance is down",  # TODO tweak
                Period=60,
                Namespace="AWS/EC2",  # FIXME lookup constant?
                ComparisonOperator="GreaterThanThreshold",  # FIXME lookup constant
                MetricName="CPUUtilization",  # TODO Lookup a very long list?
            )
        )

    @staticmethod
    def low_cpu(threshold):
        """An alarm that triggers when CPU is too low
        (or the underlying metric disappears, indicating the instance is down).
        """
        # TODO I think dimension should be a compulsory attribute
        # TODO share code with the cpu_high_alarm implementation
        return Alarm(
            Properties=dict(
                # TODO sort these in some sensible order, perhaps
                EvaluationPeriods=1,
                Statistic="Average",  # FIXME lookup constant
                Threshold=threshold,
                AlarmDescription="Alarm if CPU too low or metric disappears indicating instance is down",  # TODO tweak
                Period=60,
                Namespace="AWS/EC2",  # FIXME lookup constant?
                ComparisonOperator="LessThanThreshold",  # FIXME lookup constant
                # FIXME check LessThanThreshold is correct, and it;s not LowerThanThreshold or some similar synonym
                MetricName="CPUUtilization",  # TODO Lookup a very long list?
            )
        )
