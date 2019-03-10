"""Raw representations of every data type in the AWS ServiceCatalog service.

See Also:
    `AWS developer guide for ServiceCatalog
    <https://docs.aws.amazon.com/servicecatalog/latest/dg/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "AcceptedPortfolioShare",
    "AcceptedPortfolioShareProperties",
    "CloudFormationProduct",
    "CloudFormationProductProperties",
    "CloudFormationProvisionedProduct",
    "CloudFormationProvisionedProductProperties",
    "LaunchNotificationConstraint",
    "LaunchNotificationConstraintProperties",
    "LaunchRoleConstraint",
    "LaunchRoleConstraintProperties",
    "LaunchTemplateConstraint",
    "LaunchTemplateConstraintProperties",
    "Portfolio",
    "PortfolioProperties",
    "PortfolioPrincipalAssociation",
    "PortfolioPrincipalAssociationProperties",
    "PortfolioProductAssociation",
    "PortfolioProductAssociationProperties",
    "PortfolioShare",
    "PortfolioShareProperties",
    "TagOption",
    "TagOptionProperties",
    "TagOptionAssociation",
    "TagOptionAssociationProperties",
]


@attrs(**ATTRSCONFIG)
class AcceptedPortfolioShareProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    PortfolioId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class AcceptedPortfolioShare(Resource):
    """A Accepted Portfolio Share for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for AcceptedPortfolioShare
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::AcceptedPortfolioShare"

    Properties: AcceptedPortfolioShareProperties = attrib(
        factory=AcceptedPortfolioShareProperties,
        converter=create_object_converter(AcceptedPortfolioShareProperties),
    )


@attrs(**ATTRSCONFIG)
class CloudFormationProductProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    Description = attrib(default=None)
    Distributor = attrib(default=None)
    Name = attrib(default=None)
    Owner = attrib(default=None)
    ProvisioningArtifactParameters = attrib(default=None)
    SupportDescription = attrib(default=None)
    SupportEmail = attrib(default=None)
    SupportUrl = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class CloudFormationProduct(Resource):
    """A Cloud Formation Product for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for CloudFormationProduct
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::CloudFormationProduct"

    Properties: CloudFormationProductProperties = attrib(
        factory=CloudFormationProductProperties,
        converter=create_object_converter(CloudFormationProductProperties),
    )


@attrs(**ATTRSCONFIG)
class CloudFormationProvisionedProductProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    NotificationArns = attrib(default=None)
    PathId = attrib(default=None)
    ProductId = attrib(default=None)
    ProductName = attrib(default=None)
    ProvisionedProductName = attrib(default=None)
    ProvisioningArtifactId = attrib(default=None)
    ProvisioningArtifactName = attrib(default=None)
    ProvisioningParameters = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class CloudFormationProvisionedProduct(Resource):
    """A Cloud Formation Provisioned Product for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for CloudFormationProvisionedProduct
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::CloudFormationProvisionedProduct"

    Properties: CloudFormationProvisionedProductProperties = attrib(
        factory=CloudFormationProvisionedProductProperties,
        converter=create_object_converter(CloudFormationProvisionedProductProperties),
    )


@attrs(**ATTRSCONFIG)
class LaunchNotificationConstraintProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    Description = attrib(default=None)
    NotificationArns = attrib(default=None)
    PortfolioId = attrib(default=None)
    ProductId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class LaunchNotificationConstraint(Resource):
    """A Launch Notification Constraint for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for LaunchNotificationConstraint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::LaunchNotificationConstraint"

    Properties: LaunchNotificationConstraintProperties = attrib(
        factory=LaunchNotificationConstraintProperties,
        converter=create_object_converter(LaunchNotificationConstraintProperties),
    )


@attrs(**ATTRSCONFIG)
class LaunchRoleConstraintProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    Description = attrib(default=None)
    PortfolioId = attrib(default=None)
    ProductId = attrib(default=None)
    RoleArn = attrib(default=None)


@attrs(**ATTRSCONFIG)
class LaunchRoleConstraint(Resource):
    """A Launch Role Constraint for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for LaunchRoleConstraint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::LaunchRoleConstraint"

    Properties: LaunchRoleConstraintProperties = attrib(
        factory=LaunchRoleConstraintProperties,
        converter=create_object_converter(LaunchRoleConstraintProperties),
    )


@attrs(**ATTRSCONFIG)
class LaunchTemplateConstraintProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    Description = attrib(default=None)
    PortfolioId = attrib(default=None)
    ProductId = attrib(default=None)
    Rules = attrib(default=None)


@attrs(**ATTRSCONFIG)
class LaunchTemplateConstraint(Resource):
    """A Launch Template Constraint for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for LaunchTemplateConstraint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::LaunchTemplateConstraint"

    Properties: LaunchTemplateConstraintProperties = attrib(
        factory=LaunchTemplateConstraintProperties,
        converter=create_object_converter(LaunchTemplateConstraintProperties),
    )


@attrs(**ATTRSCONFIG)
class PortfolioProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    Description = attrib(default=None)
    DisplayName = attrib(default=None)
    ProviderName = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Portfolio(Resource):
    """A Portfolio for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for Portfolio
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::Portfolio"

    Properties: PortfolioProperties = attrib(
        factory=PortfolioProperties,
        converter=create_object_converter(PortfolioProperties),
    )


@attrs(**ATTRSCONFIG)
class PortfolioPrincipalAssociationProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    PortfolioId = attrib(default=None)
    PrincipalARN = attrib(default=None)
    PrincipalType = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PortfolioPrincipalAssociation(Resource):
    """A Portfolio Principal Association for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for PortfolioPrincipalAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::PortfolioPrincipalAssociation"

    Properties: PortfolioPrincipalAssociationProperties = attrib(
        factory=PortfolioPrincipalAssociationProperties,
        converter=create_object_converter(PortfolioPrincipalAssociationProperties),
    )


@attrs(**ATTRSCONFIG)
class PortfolioProductAssociationProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    PortfolioId = attrib(default=None)
    ProductId = attrib(default=None)
    SourcePortfolioId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PortfolioProductAssociation(Resource):
    """A Portfolio Product Association for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for PortfolioProductAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::PortfolioProductAssociation"

    Properties: PortfolioProductAssociationProperties = attrib(
        factory=PortfolioProductAssociationProperties,
        converter=create_object_converter(PortfolioProductAssociationProperties),
    )


@attrs(**ATTRSCONFIG)
class PortfolioShareProperties(ResourceProperties):
    AcceptLanguage = attrib(default=None)
    AccountId = attrib(default=None)
    PortfolioId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class PortfolioShare(Resource):
    """A Portfolio Share for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for PortfolioShare
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::PortfolioShare"

    Properties: PortfolioShareProperties = attrib(
        factory=PortfolioShareProperties,
        converter=create_object_converter(PortfolioShareProperties),
    )


@attrs(**ATTRSCONFIG)
class TagOptionProperties(ResourceProperties):
    Active = attrib(default=None)
    Key = attrib(default=None)
    Value = attrib(default=None)


@attrs(**ATTRSCONFIG)
class TagOption(Resource):
    """A Tag Option for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for TagOption
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::TagOption"

    Properties: TagOptionProperties = attrib(
        factory=TagOptionProperties,
        converter=create_object_converter(TagOptionProperties),
    )


@attrs(**ATTRSCONFIG)
class TagOptionAssociationProperties(ResourceProperties):
    ResourceId = attrib(default=None)
    TagOptionId = attrib(default=None)


@attrs(**ATTRSCONFIG)
class TagOptionAssociation(Resource):
    """A Tag Option Association for ServiceCatalog.

    See Also:
        `AWS Cloud Formation documentation for TagOptionAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::ServiceCatalog::TagOptionAssociation"

    Properties: TagOptionAssociationProperties = attrib(
        factory=TagOptionAssociationProperties,
        converter=create_object_converter(TagOptionAssociationProperties),
    )
