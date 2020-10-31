"""Raw representations of every data type in the AWS Config service.

See Also:
    `AWS developer guide for Config
    <https://docs.aws.amazon.com/config/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "AggregationAuthorization",
    "AggregationAuthorizationProperties",
    "ConfigRule",
    "ConfigRuleProperties",
    "ConfigurationAggregator",
    "ConfigurationAggregatorProperties",
    "ConfigurationRecorder",
    "ConfigurationRecorderProperties",
    "ConformancePack",
    "ConformancePackProperties",
    "DeliveryChannel",
    "DeliveryChannelProperties",
    "OrganizationConfigRule",
    "OrganizationConfigRuleProperties",
    "OrganizationConformancePack",
    "OrganizationConformancePackProperties",
    "RemediationConfiguration",
    "RemediationConfigurationProperties",
]


@attrs(**ATTRSCONFIG)
class AggregationAuthorizationProperties(ResourceProperties):
    AuthorizedAccountId = attrib(default=None)
    AuthorizedAwsRegion = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class AggregationAuthorization(Resource):
    """A Aggregation Authorization for Config.

    See Also:
        `AWS Cloud Formation documentation for AggregationAuthorization
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::AggregationAuthorization"

    Properties: AggregationAuthorizationProperties = attrib(
        factory=AggregationAuthorizationProperties,
        converter=create_object_converter(AggregationAuthorizationProperties),
    )


@attrs(**ATTRSCONFIG)
class ConfigRuleProperties(ResourceProperties):
    ConfigRuleName = attrib(default=None)
    Description = attrib(default=None)
    InputParameters = attrib(default=None)
    MaximumExecutionFrequency = attrib(default=None)
    Scope = attrib(default=None)
    Source = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConfigRule(Resource):
    """A Config Rule for Config.

    See Also:
        `AWS Cloud Formation documentation for ConfigRule
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::ConfigRule"

    Properties: ConfigRuleProperties = attrib(
        factory=ConfigRuleProperties,
        converter=create_object_converter(ConfigRuleProperties),
    )


@attrs(**ATTRSCONFIG)
class ConfigurationAggregatorProperties(ResourceProperties):
    AccountAggregationSources = attrib(default=None)
    ConfigurationAggregatorName = attrib(default=None)
    OrganizationAggregationSource = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConfigurationAggregator(Resource):
    """A Configuration Aggregator for Config.

    See Also:
        `AWS Cloud Formation documentation for ConfigurationAggregator
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::ConfigurationAggregator"

    Properties: ConfigurationAggregatorProperties = attrib(
        factory=ConfigurationAggregatorProperties,
        converter=create_object_converter(ConfigurationAggregatorProperties),
    )


@attrs(**ATTRSCONFIG)
class ConfigurationRecorderProperties(ResourceProperties):
    Name = attrib(default=None)
    RecordingGroup = attrib(default=None)
    RoleARN = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConfigurationRecorder(Resource):
    """A Configuration Recorder for Config.

    See Also:
        `AWS Cloud Formation documentation for ConfigurationRecorder
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::ConfigurationRecorder"

    Properties: ConfigurationRecorderProperties = attrib(
        factory=ConfigurationRecorderProperties,
        converter=create_object_converter(ConfigurationRecorderProperties),
    )


@attrs(**ATTRSCONFIG)
class ConformancePackProperties(ResourceProperties):
    ConformancePackInputParameters = attrib(default=None)
    ConformancePackName = attrib(default=None)
    DeliveryS3Bucket = attrib(default=None)
    DeliveryS3KeyPrefix = attrib(default=None)
    TemplateBody = attrib(default=None)
    TemplateS3Uri = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ConformancePack(Resource):
    """A Conformance Pack for Config.

    See Also:
        `AWS Cloud Formation documentation for ConformancePack
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-conformancepack.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::ConformancePack"

    Properties: ConformancePackProperties = attrib(
        factory=ConformancePackProperties,
        converter=create_object_converter(ConformancePackProperties),
    )


@attrs(**ATTRSCONFIG)
class DeliveryChannelProperties(ResourceProperties):
    ConfigSnapshotDeliveryProperties = attrib(default=None)
    Name = attrib(default=None)
    S3BucketName = attrib(default=None)
    S3KeyPrefix = attrib(default=None)
    SnsTopicARN = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DeliveryChannel(Resource):
    """A Delivery Channel for Config.

    See Also:
        `AWS Cloud Formation documentation for DeliveryChannel
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::DeliveryChannel"

    Properties: DeliveryChannelProperties = attrib(
        factory=DeliveryChannelProperties,
        converter=create_object_converter(DeliveryChannelProperties),
    )


@attrs(**ATTRSCONFIG)
class OrganizationConfigRuleProperties(ResourceProperties):
    ExcludedAccounts = attrib(default=None)
    OrganizationConfigRuleName = attrib(default=None)
    OrganizationCustomRuleMetadata = attrib(default=None)
    OrganizationManagedRuleMetadata = attrib(default=None)


@attrs(**ATTRSCONFIG)
class OrganizationConfigRule(Resource):
    """A Organization Config Rule for Config.

    See Also:
        `AWS Cloud Formation documentation for OrganizationConfigRule
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconfigrule.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::OrganizationConfigRule"

    Properties: OrganizationConfigRuleProperties = attrib(
        factory=OrganizationConfigRuleProperties,
        converter=create_object_converter(OrganizationConfigRuleProperties),
    )


@attrs(**ATTRSCONFIG)
class OrganizationConformancePackProperties(ResourceProperties):
    ConformancePackInputParameters = attrib(default=None)
    DeliveryS3Bucket = attrib(default=None)
    DeliveryS3KeyPrefix = attrib(default=None)
    ExcludedAccounts = attrib(default=None)
    OrganizationConformancePackName = attrib(default=None)
    TemplateBody = attrib(default=None)
    TemplateS3Uri = attrib(default=None)


@attrs(**ATTRSCONFIG)
class OrganizationConformancePack(Resource):
    """A Organization Conformance Pack for Config.

    See Also:
        `AWS Cloud Formation documentation for OrganizationConformancePack
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-organizationconformancepack.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::OrganizationConformancePack"

    Properties: OrganizationConformancePackProperties = attrib(
        factory=OrganizationConformancePackProperties,
        converter=create_object_converter(OrganizationConformancePackProperties),
    )


@attrs(**ATTRSCONFIG)
class RemediationConfigurationProperties(ResourceProperties):
    Automatic = attrib(default=None)
    ConfigRuleName = attrib(default=None)
    ExecutionControls = attrib(default=None)
    MaximumAutomaticAttempts = attrib(default=None)
    Parameters = attrib(default=None)
    ResourceType = attrib(default=None)
    RetryAttemptSeconds = attrib(default=None)
    TargetId = attrib(default=None)
    TargetType = attrib(default=None)
    TargetVersion = attrib(default=None)


@attrs(**ATTRSCONFIG)
class RemediationConfiguration(Resource):
    """A Remediation Configuration for Config.

    See Also:
        `AWS Cloud Formation documentation for RemediationConfiguration
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-remediationconfiguration.html>`_
    """

    RESOURCE_TYPE = "AWS::Config::RemediationConfiguration"

    Properties: RemediationConfigurationProperties = attrib(
        factory=RemediationConfigurationProperties,
        converter=create_object_converter(RemediationConfigurationProperties),
    )
