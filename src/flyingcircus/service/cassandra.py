"""General-use classes to interact with the Cassandra service through CloudFormation.

See Also:
    `AWS developer guide for Cassandra
    <https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import cassandra as _raw

# noinspection PyUnresolvedReferences
from .._raw.cassandra import *
