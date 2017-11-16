"""Raw representations of every data type in the AWS CloudWatch service.

See http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
"""

from ..core import Resource


class Alarm(Resource):
    """A CloudWatch alarm

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
    """

    RESOURCE_TYPE = "AWS::CloudWatch::Alarm"

    RESOURCE_PROPERTIES = {
        "ActionsEnabled",
        "AlarmActions",
        "AlarmDescription",
        "AlarmName",
        "ComparisonOperator",
        "Dimensions",
        "EvaluateLowSampleCountPercentile",
        "EvaluationPeriods",
        "ExtendedStatistic",
        "InsufficientDataActions",
        "MetricName",
        "Namespace",
        "OKActions",
        "Period",
        "Statistic",
        "Threshold",
        "TreatMissingData",
        "Unit",
    }
