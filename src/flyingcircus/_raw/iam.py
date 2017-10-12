from ..core import BaseAWSObject
from ..core import Resource


class Role(Resource):
    """An IAM role"""

    AWS_RESOURCE_TYPE = "AWS::IAM::Role"
    AWS_ATTRIBUTES = [
        "Arn",
    ]


class PolicyDocument(BaseAWSObject):
    """An IAM PolicyDocument.

    See format specification at http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
    """

    @property
    def Statement(self):
        return self._data.setdefault('Statement', [])


class PolicyStatement(BaseAWSObject):
    """A single IAM Policy statement

    See http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Statement
    """
    #TODO fields: Sid, Effect, Action, NotAction, Resource, NotResource, Principal, NotPrincipal, Condition,
    pass


class Policy(BaseAWSObject):
    """An IAM Policy object"""

    # TODO roll together the policy document and the PolicyName attribute into one object (by inheriting this from PolicyDocument). the hierarchy adds no value.

    pass  # FIXME
