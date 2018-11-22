"""General-use classes to interact with the Cognito service through CloudFormation.

See Also:
    `AWS developer guide for Cognito
    <https://docs.aws.amazon.com/cognito/latest/developerguide/index.html>`_
"""

from .._raw import cognito as _raw

# noinspection PyUnresolvedReferences
from .._raw.cognito import *


class UserPool(_raw.UserPool):
    __slots__ = []

    # Implement Tagging
    # -----------------
    #
    # User Pools store tags as a dictionary (somebody had to), and use a
    # different Property name for the tag data
    TAG_PROPERTY = "UserPoolTags"

    def tag(self, tags=None, tag_derived_resources=True, **more_tags):
        tagdata = self.Properties[self.TAG_PROPERTY]

        if tagdata is None:
            # No tags set yet
            self.Properties[self.TAG_PROPERTY] = {}
            tagdata = self.Properties[self.TAG_PROPERTY]

        tagdata.update(tags or {})
        tagdata.update(more_tags)

        return True

    def get_tag(self, key: str):
        tagdata = self.Properties[self.TAG_PROPERTY]

        if tagdata is None:
            # No tags set yet
            return None

        return tagdata.get(key, None)

    # Implement Naming
    # ----------------
    @property
    def name(self):
        return self.Properties["UserPoolName"]  # Might be default of None

    @name.setter
    def name(self, value: str):
        self.Properties["UserPoolName"] = value
