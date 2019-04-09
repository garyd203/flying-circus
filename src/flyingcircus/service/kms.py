"""General-use classes to interact with the KMS service through CloudFormation.

See Also:
    `AWS developer guide for KMS
    <https://docs.aws.amazon.com/kms/latest/developerguide/overview.html>`_
"""

from .._raw import kms as _raw

# noinspection PyUnresolvedReferences
from .._raw.kms import *


class Key(_raw.Key):
    __slots__ = []

    @property
    def name(self):
        # TODO #113 create an Alias instead
        raise NotImplementedError(
            "Key.name cannot be set as a tag. We need to use an Alias."
        )
