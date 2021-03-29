"""Raw representations of every data type in the AWS Cassandra service.

See Also:
    `AWS developer guide for Cassandra
    <https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Keyspace", "KeyspaceProperties", "Table", "TableProperties"]


@attrs(**ATTRSCONFIG)
class KeyspaceProperties(ResourceProperties):
    KeyspaceName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Keyspace(Resource):
    """A Keyspace for Cassandra.

    See Also:
        `AWS Cloud Formation documentation for Keyspace
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-keyspace.html>`_
    """

    RESOURCE_TYPE = "AWS::Cassandra::Keyspace"

    Properties: KeyspaceProperties = attrib(
        factory=KeyspaceProperties,
        converter=create_object_converter(KeyspaceProperties),
    )


@attrs(**ATTRSCONFIG)
class TableProperties(ResourceProperties):
    BillingMode = attrib(default=None)
    ClusteringKeyColumns = attrib(default=None)
    KeyspaceName = attrib(default=None)
    PartitionKeyColumns = attrib(default=None)
    RegularColumns = attrib(default=None)
    TableName = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Table(Resource):
    """A Table for Cassandra.

    See Also:
        `AWS Cloud Formation documentation for Table
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cassandra-table.html>`_
    """

    RESOURCE_TYPE = "AWS::Cassandra::Table"

    Properties: TableProperties = attrib(
        factory=TableProperties, converter=create_object_converter(TableProperties)
    )
