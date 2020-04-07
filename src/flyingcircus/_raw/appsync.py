"""Raw representations of every data type in the AWS AppSync service.

See Also:
    `AWS developer guide for AppSync
    <https://docs.aws.amazon.com/appsync/latest/devguide/welcome.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "ApiCache",
    "ApiCacheProperties",
    "ApiKey",
    "ApiKeyProperties",
    "DataSource",
    "DataSourceProperties",
    "FunctionConfiguration",
    "FunctionConfigurationProperties",
    "GraphQLApi",
    "GraphQLApiProperties",
    "GraphQLSchema",
    "GraphQLSchemaProperties",
    "Resolver",
    "ResolverProperties",
]


@attrs(**ATTRSCONFIG)
class ApiCacheProperties(ResourceProperties):
    ApiCachingBehavior = attrib(default=None)
    ApiId = attrib(default=None)
    AtRestEncryptionEnabled = attrib(default=None)
    TransitEncryptionEnabled = attrib(default=None)
    Ttl = attrib(default=None)
    Type = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ApiCache(Resource):
    """A Api Cache for AppSync.

    See Also:
        `AWS Cloud Formation documentation for ApiCache
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::ApiCache"

    Properties: ApiCacheProperties = attrib(
        factory=ApiCacheProperties,
        converter=create_object_converter(ApiCacheProperties),
    )


@attrs(**ATTRSCONFIG)
class ApiKeyProperties(ResourceProperties):
    ApiId = attrib(default=None)
    Description = attrib(default=None)
    Expires = attrib(default=None)


@attrs(**ATTRSCONFIG)
class ApiKey(Resource):
    """A Api Key for AppSync.

    See Also:
        `AWS Cloud Formation documentation for ApiKey
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::ApiKey"

    Properties: ApiKeyProperties = attrib(
        factory=ApiKeyProperties, converter=create_object_converter(ApiKeyProperties)
    )


@attrs(**ATTRSCONFIG)
class DataSourceProperties(ResourceProperties):
    ApiId = attrib(default=None)
    Description = attrib(default=None)
    DynamoDBConfig = attrib(default=None)
    ElasticsearchConfig = attrib(default=None)
    HttpConfig = attrib(default=None)
    LambdaConfig = attrib(default=None)
    Name = attrib(default=None)
    RelationalDatabaseConfig = attrib(default=None)
    ServiceRoleArn = attrib(default=None)
    Type = attrib(default=None)


@attrs(**ATTRSCONFIG)
class DataSource(Resource):
    """A Data Source for AppSync.

    See Also:
        `AWS Cloud Formation documentation for DataSource
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::DataSource"

    Properties: DataSourceProperties = attrib(
        factory=DataSourceProperties,
        converter=create_object_converter(DataSourceProperties),
    )


@attrs(**ATTRSCONFIG)
class FunctionConfigurationProperties(ResourceProperties):
    ApiId = attrib(default=None)
    DataSourceName = attrib(default=None)
    Description = attrib(default=None)
    FunctionVersion = attrib(default=None)
    Name = attrib(default=None)
    RequestMappingTemplate = attrib(default=None)
    RequestMappingTemplateS3Location = attrib(default=None)
    ResponseMappingTemplate = attrib(default=None)
    ResponseMappingTemplateS3Location = attrib(default=None)


@attrs(**ATTRSCONFIG)
class FunctionConfiguration(Resource):
    """A Function Configuration for AppSync.

    See Also:
        `AWS Cloud Formation documentation for FunctionConfiguration
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::FunctionConfiguration"

    Properties: FunctionConfigurationProperties = attrib(
        factory=FunctionConfigurationProperties,
        converter=create_object_converter(FunctionConfigurationProperties),
    )


@attrs(**ATTRSCONFIG)
class GraphQLApiProperties(ResourceProperties):
    AdditionalAuthenticationProviders = attrib(default=None)
    AuthenticationType = attrib(default=None)
    LogConfig = attrib(default=None)
    Name = attrib(default=None)
    OpenIDConnectConfig = attrib(default=None)
    Tags = attrib(default=None)
    UserPoolConfig = attrib(default=None)


@attrs(**ATTRSCONFIG)
class GraphQLApi(Resource):
    """A Graph Ql Api for AppSync.

    See Also:
        `AWS Cloud Formation documentation for GraphQLApi
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::GraphQLApi"

    Properties: GraphQLApiProperties = attrib(
        factory=GraphQLApiProperties,
        converter=create_object_converter(GraphQLApiProperties),
    )


@attrs(**ATTRSCONFIG)
class GraphQLSchemaProperties(ResourceProperties):
    ApiId = attrib(default=None)
    Definition = attrib(default=None)
    DefinitionS3Location = attrib(default=None)


@attrs(**ATTRSCONFIG)
class GraphQLSchema(Resource):
    """A Graph Ql Schema for AppSync.

    See Also:
        `AWS Cloud Formation documentation for GraphQLSchema
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::GraphQLSchema"

    Properties: GraphQLSchemaProperties = attrib(
        factory=GraphQLSchemaProperties,
        converter=create_object_converter(GraphQLSchemaProperties),
    )


@attrs(**ATTRSCONFIG)
class ResolverProperties(ResourceProperties):
    ApiId = attrib(default=None)
    CachingConfig = attrib(default=None)
    DataSourceName = attrib(default=None)
    FieldName = attrib(default=None)
    Kind = attrib(default=None)
    PipelineConfig = attrib(default=None)
    RequestMappingTemplate = attrib(default=None)
    RequestMappingTemplateS3Location = attrib(default=None)
    ResponseMappingTemplate = attrib(default=None)
    ResponseMappingTemplateS3Location = attrib(default=None)
    SyncConfig = attrib(default=None)
    TypeName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Resolver(Resource):
    """A Resolver for AppSync.

    See Also:
        `AWS Cloud Formation documentation for Resolver
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html>`_
    """

    RESOURCE_TYPE = "AWS::AppSync::Resolver"

    Properties: ResolverProperties = attrib(
        factory=ResolverProperties,
        converter=create_object_converter(ResolverProperties),
    )
