"""Raw representations of every data type in the AWS Elasticsearch service.

See Also:
    `AWS developer guide for Elasticsearch
    <https://docs.aws.amazon.com/workspaces/latest/adminguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Domain", "DomainProperties"]


@attrs(**ATTRSCONFIG)
class DomainProperties(ResourceProperties):
    AccessPolicies = attrib(default=None)
    AdvancedOptions = attrib(default=None)
    AdvancedSecurityOptions = attrib(default=None)
    CognitoOptions = attrib(default=None)
    DomainEndpointOptions = attrib(default=None)
    DomainName = attrib(default=None)
    EBSOptions = attrib(default=None)
    ElasticsearchClusterConfig = attrib(default=None)
    ElasticsearchVersion = attrib(default=None)
    EncryptionAtRestOptions = attrib(default=None)
    LogPublishingOptions = attrib(default=None)
    NodeToNodeEncryptionOptions = attrib(default=None)
    SnapshotOptions = attrib(default=None)
    Tags = attrib(default=None)
    VPCOptions = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Domain(Resource):
    """A Domain for Elasticsearch.

    See Also:
        `AWS Cloud Formation documentation for Domain
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html>`_
    """

    RESOURCE_TYPE = "AWS::Elasticsearch::Domain"

    Properties: DomainProperties = attrib(
        factory=DomainProperties, converter=create_object_converter(DomainProperties)
    )
