"""Raw representations of every data type in the AWS Cognito service.

See Also:
    `AWS developer guide for Cognito
    <https://docs.aws.amazon.com/cognito/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "IdentityPool",
    "IdentityPoolProperties",
    "IdentityPoolRoleAttachment",
    "IdentityPoolRoleAttachmentProperties",
    "UserPool",
    "UserPoolProperties",
    "UserPoolClient",
    "UserPoolClientProperties",
    "UserPoolDomain",
    "UserPoolDomainProperties",
    "UserPoolGroup",
    "UserPoolGroupProperties",
    "UserPoolIdentityProvider",
    "UserPoolIdentityProviderProperties",
    "UserPoolResourceServer",
    "UserPoolResourceServerProperties",
    "UserPoolRiskConfigurationAttachment",
    "UserPoolRiskConfigurationAttachmentProperties",
    "UserPoolUICustomizationAttachment",
    "UserPoolUICustomizationAttachmentProperties",
    "UserPoolUser",
    "UserPoolUserProperties",
    "UserPoolUserToGroupAttachment",
    "UserPoolUserToGroupAttachmentProperties",
]


@attrs(**ATTRSCONFIG)
class IdentityPoolProperties(ResourceProperties):
    AllowClassicFlow = attrib(default=None)
    AllowUnauthenticatedIdentities = attrib(default=None)
    CognitoEvents = attrib(default=None)
    CognitoIdentityProviders = attrib(default=None)
    CognitoStreams = attrib(default=None)
    DeveloperProviderName = attrib(default=None)
    IdentityPoolName = attrib(default=None)
    OpenIdConnectProviderARNs = attrib(default=None)
    PushSync = attrib(default=None)
    SamlProviderARNs = attrib(default=None)
    SupportedLoginProviders = attrib(default=None)


@attrs(**ATTRSCONFIG)
class IdentityPool(Resource):
    """A Identity Pool for Cognito.

    See Also:
        `AWS Cloud Formation documentation for IdentityPool
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypool.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::IdentityPool"

    Properties: IdentityPoolProperties = attrib(
        factory=IdentityPoolProperties,
        converter=create_object_converter(IdentityPoolProperties),
    )


@attrs(**ATTRSCONFIG)
class IdentityPoolRoleAttachmentProperties(ResourceProperties):
    IdentityPoolId = attrib(default=None)
    RoleMappings = attrib(default=None)
    Roles = attrib(default=None)


@attrs(**ATTRSCONFIG)
class IdentityPoolRoleAttachment(Resource):
    """A Identity Pool Role Attachment for Cognito.

    See Also:
        `AWS Cloud Formation documentation for IdentityPoolRoleAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-identitypoolroleattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::IdentityPoolRoleAttachment"

    Properties: IdentityPoolRoleAttachmentProperties = attrib(
        factory=IdentityPoolRoleAttachmentProperties,
        converter=create_object_converter(IdentityPoolRoleAttachmentProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolProperties(ResourceProperties):
    AdminCreateUserConfig = attrib(default=None)
    AliasAttributes = attrib(default=None)
    AutoVerifiedAttributes = attrib(default=None)
    DeviceConfiguration = attrib(default=None)
    EmailConfiguration = attrib(default=None)
    EmailVerificationMessage = attrib(default=None)
    EmailVerificationSubject = attrib(default=None)
    EnabledMfas = attrib(default=None)
    LambdaConfig = attrib(default=None)
    MfaConfiguration = attrib(default=None)
    Policies = attrib(default=None)
    Schema = attrib(default=None)
    SmsAuthenticationMessage = attrib(default=None)
    SmsConfiguration = attrib(default=None)
    SmsVerificationMessage = attrib(default=None)
    UsernameAttributes = attrib(default=None)
    UserPoolAddOns = attrib(default=None)
    UserPoolName = attrib(default=None)
    UserPoolTags = attrib(default=None)
    VerificationMessageTemplate = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPool(Resource):
    """A User Pool for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPool
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPool"

    Properties: UserPoolProperties = attrib(
        factory=UserPoolProperties,
        converter=create_object_converter(UserPoolProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolClientProperties(ResourceProperties):
    AllowedOAuthFlows = attrib(default=None)
    AllowedOAuthFlowsUserPoolClient = attrib(default=None)
    AllowedOAuthScopes = attrib(default=None)
    AnalyticsConfiguration = attrib(default=None)
    CallbackURLs = attrib(default=None)
    ClientName = attrib(default=None)
    DefaultRedirectURI = attrib(default=None)
    ExplicitAuthFlows = attrib(default=None)
    GenerateSecret = attrib(default=None)
    LogoutURLs = attrib(default=None)
    PreventUserExistenceErrors = attrib(default=None)
    ReadAttributes = attrib(default=None)
    RefreshTokenValidity = attrib(default=None)
    SupportedIdentityProviders = attrib(default=None)
    UserPoolId = attrib(default=None)
    WriteAttributes = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolClient(Resource):
    """A User Pool Client for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolClient
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolClient"

    Properties: UserPoolClientProperties = attrib(
        factory=UserPoolClientProperties,
        converter=create_object_converter(UserPoolClientProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolDomainProperties(ResourceProperties):
    CustomDomainConfig = attrib(default=None)
    Domain = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolDomain(Resource):
    """A User Pool Domain for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolDomain
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolDomain"

    Properties: UserPoolDomainProperties = attrib(
        factory=UserPoolDomainProperties,
        converter=create_object_converter(UserPoolDomainProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolGroupProperties(ResourceProperties):
    Description = attrib(default=None)
    GroupName = attrib(default=None)
    Precedence = attrib(default=None)
    RoleArn = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolGroup(Resource):
    """A User Pool Group for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolgroup.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolGroup"

    Properties: UserPoolGroupProperties = attrib(
        factory=UserPoolGroupProperties,
        converter=create_object_converter(UserPoolGroupProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolIdentityProviderProperties(ResourceProperties):
    AttributeMapping = attrib(default=None)
    IdpIdentifiers = attrib(default=None)
    ProviderDetails = attrib(default=None)
    ProviderName = attrib(default=None)
    ProviderType = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolIdentityProvider(Resource):
    """A User Pool Identity Provider for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolIdentityProvider
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolidentityprovider.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolIdentityProvider"

    Properties: UserPoolIdentityProviderProperties = attrib(
        factory=UserPoolIdentityProviderProperties,
        converter=create_object_converter(UserPoolIdentityProviderProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolResourceServerProperties(ResourceProperties):
    Identifier = attrib(default=None)
    Name = attrib(default=None)
    Scopes = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolResourceServer(Resource):
    """A User Pool Resource Server for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolResourceServer
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolresourceserver.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolResourceServer"

    Properties: UserPoolResourceServerProperties = attrib(
        factory=UserPoolResourceServerProperties,
        converter=create_object_converter(UserPoolResourceServerProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolRiskConfigurationAttachmentProperties(ResourceProperties):
    AccountTakeoverRiskConfiguration = attrib(default=None)
    ClientId = attrib(default=None)
    CompromisedCredentialsRiskConfiguration = attrib(default=None)
    RiskExceptionConfiguration = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolRiskConfigurationAttachment(Resource):
    """A User Pool Risk Configuration Attachment for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolRiskConfigurationAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolriskconfigurationattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolRiskConfigurationAttachment"

    Properties: UserPoolRiskConfigurationAttachmentProperties = attrib(
        factory=UserPoolRiskConfigurationAttachmentProperties,
        converter=create_object_converter(
            UserPoolRiskConfigurationAttachmentProperties
        ),
    )


@attrs(**ATTRSCONFIG)
class UserPoolUICustomizationAttachmentProperties(ResourceProperties):
    ClientId = attrib(default=None)
    CSS = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolUICustomizationAttachment(Resource):
    """A User Pool Ui Customization Attachment for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolUICustomizationAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluicustomizationattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolUICustomizationAttachment"

    Properties: UserPoolUICustomizationAttachmentProperties = attrib(
        factory=UserPoolUICustomizationAttachmentProperties,
        converter=create_object_converter(UserPoolUICustomizationAttachmentProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolUserProperties(ResourceProperties):
    ClientMetadata = attrib(default=None)
    DesiredDeliveryMediums = attrib(default=None)
    ForceAliasCreation = attrib(default=None)
    MessageAction = attrib(default=None)
    UserAttributes = attrib(default=None)
    Username = attrib(default=None)
    UserPoolId = attrib(default=None)
    ValidationData = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolUser(Resource):
    """A User Pool User for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolUser
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooluser.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolUser"

    Properties: UserPoolUserProperties = attrib(
        factory=UserPoolUserProperties,
        converter=create_object_converter(UserPoolUserProperties),
    )


@attrs(**ATTRSCONFIG)
class UserPoolUserToGroupAttachmentProperties(ResourceProperties):
    GroupName = attrib(default=None)
    Username = attrib(default=None)
    UserPoolId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class UserPoolUserToGroupAttachment(Resource):
    """A User Pool User To Group Attachment for Cognito.

    See Also:
        `AWS Cloud Formation documentation for UserPoolUserToGroupAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolusertogroupattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::Cognito::UserPoolUserToGroupAttachment"

    Properties: UserPoolUserToGroupAttachmentProperties = attrib(
        factory=UserPoolUserToGroupAttachmentProperties,
        converter=create_object_converter(UserPoolUserToGroupAttachmentProperties),
    )
