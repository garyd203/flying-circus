"""General-use classes to interact with the Elasticsearch service through CloudFormation.

See Also:
    `AWS developer guide for Elasticsearch
    <https://docs.aws.amazon.com/workspaces/latest/adminguide/index.html>`_
"""

# noinspection PyUnresolvedReferences
from .._raw import elasticsearch as _raw

# noinspection PyUnresolvedReferences
from .._raw.elasticsearch import *
