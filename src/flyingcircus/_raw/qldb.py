"""Raw representations of every data type in the AWS QLDB service.

See Also:
    `AWS developer guide for QLDB
    <https://docs.aws.amazon.com/qldb/latest/developerguide/index.html>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = ["Ledger", "LedgerProperties"]


@attrs(**ATTRSCONFIG)
class LedgerProperties(ResourceProperties):
    DeletionProtection = attrib(default=None)
    Name = attrib(default=None)
    PermissionsMode = attrib(default=None)
    Tags = attrib(default=None)


@attrs(**ATTRSCONFIG)
class Ledger(Resource):
    """A Ledger for QLDB.

    See Also:
        `AWS Cloud Formation documentation for Ledger
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html>`_
    """

    RESOURCE_TYPE = "AWS::QLDB::Ledger"

    Properties: LedgerProperties = attrib(
        factory=LedgerProperties, converter=create_object_converter(LedgerProperties)
    )
