"""Raw representations of every data type in the AWS IoT service.

See Also:
    `AWS developer guide for IoT
    <https://docs.aws.amazon.com/iot/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "Authorizer",
    "AuthorizerProperties",
    "Certificate",
    "CertificateProperties",
    "Policy",
    "PolicyProperties",
    "PolicyPrincipalAttachment",
    "PolicyPrincipalAttachmentProperties",
    "ProvisioningTemplate",
    "ProvisioningTemplateProperties",
    "Thing",
    "ThingProperties",
    "ThingPrincipalAttachment",
    "ThingPrincipalAttachmentProperties",
    "TopicRule",
    "TopicRuleProperties",
]


@attrs(**ATTRSCONFIG)
class AuthorizerProperties(ResourceProperties):
    AuthorizerFunctionArn = attrib(default=None)
    AuthorizerName = attrib(default=None)
    SigningDisabled = attrib(default=None)
    Status = attrib(default=None)
    Tags = attrib(default=None)
    TokenKeyName = attrib(default=None)
    TokenSigningPublicKeys = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Authorizer(Resource):
    """A Authorizer for IoT.

    See Also:
        `AWS Cloud Formation documentation for Authorizer
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-authorizer.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::Authorizer"

    Properties: AuthorizerProperties = attrib(
        factory=AuthorizerProperties,
        converter=create_object_converter(AuthorizerProperties),
    )


@attrs(**ATTRSCONFIG)
class CertificateProperties(ResourceProperties):
    CACertificatePem = attrib(default=None)
    CertificateMode = attrib(default=None)
    CertificatePem = attrib(default=None)
    CertificateSigningRequest = attrib(default=None)
    Status = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Certificate(Resource):
    """A Certificate for IoT.

    See Also:
        `AWS Cloud Formation documentation for Certificate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::Certificate"

    Properties: CertificateProperties = attrib(
        factory=CertificateProperties,
        converter=create_object_converter(CertificateProperties),
    )


@attrs(**ATTRSCONFIG)
class PolicyProperties(ResourceProperties):
    PolicyDocument = attrib(default=None)
    PolicyName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Policy(Resource):
    """A Policy for IoT.

    See Also:
        `AWS Cloud Formation documentation for Policy
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::Policy"

    Properties: PolicyProperties = attrib(
        factory=PolicyProperties, converter=create_object_converter(PolicyProperties)
    )


@attrs(**ATTRSCONFIG)
class PolicyPrincipalAttachmentProperties(ResourceProperties):
    PolicyName = attrib(default=None)
    Principal = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PolicyPrincipalAttachment(Resource):
    """A Policy Principal Attachment for IoT.

    See Also:
        `AWS Cloud Formation documentation for PolicyPrincipalAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::PolicyPrincipalAttachment"

    Properties: PolicyPrincipalAttachmentProperties = attrib(
        factory=PolicyPrincipalAttachmentProperties,
        converter=create_object_converter(PolicyPrincipalAttachmentProperties),
    )


@attrs(**ATTRSCONFIG)
class ProvisioningTemplateProperties(ResourceProperties):
    Description = attrib(default=None)
    Enabled = attrib(default=None)
    PreProvisioningHook = attrib(default=None)
    ProvisioningRoleArn = attrib(default=None)
    Tags = attrib(default=None)
    TemplateBody = attrib(default=None)
    TemplateName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ProvisioningTemplate(Resource):
    """A Provisioning Template for IoT.

    See Also:
        `AWS Cloud Formation documentation for ProvisioningTemplate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-provisioningtemplate.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::ProvisioningTemplate"

    Properties: ProvisioningTemplateProperties = attrib(
        factory=ProvisioningTemplateProperties,
        converter=create_object_converter(ProvisioningTemplateProperties),
    )


@attrs(**ATTRSCONFIG)
class ThingProperties(ResourceProperties):
    AttributePayload = attrib(default=None)
    ThingName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Thing(Resource):
    """A Thing for IoT.

    See Also:
        `AWS Cloud Formation documentation for Thing
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::Thing"

    Properties: ThingProperties = attrib(
        factory=ThingProperties, converter=create_object_converter(ThingProperties)
    )


@attrs(**ATTRSCONFIG)
class ThingPrincipalAttachmentProperties(ResourceProperties):
    Principal = attrib(default=None)
    ThingName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ThingPrincipalAttachment(Resource):
    """A Thing Principal Attachment for IoT.

    See Also:
        `AWS Cloud Formation documentation for ThingPrincipalAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::ThingPrincipalAttachment"

    Properties: ThingPrincipalAttachmentProperties = attrib(
        factory=ThingPrincipalAttachmentProperties,
        converter=create_object_converter(ThingPrincipalAttachmentProperties),
    )


@attrs(**ATTRSCONFIG)
class TopicRuleProperties(ResourceProperties):
    RuleName = attrib(default=None)
    TopicRulePayload = attrib(default=None)


@attrs(**ATTRSCONFIG)
class TopicRule(Resource):
    """A Topic Rule for IoT.

    See Also:
        `AWS Cloud Formation documentation for TopicRule
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html>`_
    """

    RESOURCE_TYPE = "AWS::IoT::TopicRule"

    Properties: TopicRuleProperties = attrib(
        factory=TopicRuleProperties,
        converter=create_object_converter(TopicRuleProperties),
    )
