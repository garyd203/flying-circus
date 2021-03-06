"""Raw representations of every data type in the AWS CertificateManager service.

See Also:
    `AWS developer guide for CertificateManager
    <https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Certificate", "CertificateProperties"]


@attrs(**ATTRSCONFIG)
class CertificateProperties(ResourceProperties):
    DomainName = attrib(default=None)
    DomainValidationOptions = attrib(default=None)
    SubjectAlternativeNames = attrib(default=None)
    Tags = attrib(default=None)
    ValidationMethod = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Certificate(Resource):
    """A Certificate for CertificateManager.

    See Also:
        `AWS Cloud Formation documentation for Certificate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html>`_
    """

    RESOURCE_TYPE = "AWS::CertificateManager::Certificate"

    Properties: CertificateProperties = attrib(
        factory=CertificateProperties,
        converter=create_object_converter(CertificateProperties),
    )
