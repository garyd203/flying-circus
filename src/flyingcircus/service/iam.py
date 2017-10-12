from .._raw.iam import *

__all__ = [
    "AssumeRolePolicy",
    "Policy",
    "PolicyDocument",
    "PolicyStatement",
    "PrincipalSet",
    "Role",
]


class AssumeRolePolicy(PolicyDocument):
    """A simple trust policy to describe can assume a role."""

    def __init__(self, principals):
        PolicyDocument.__init__(
            self,
            Version='2012-10-17',
            Statement=[
                PolicyStatement(
                    Action=['sts:AssumeRole'],
                    Effect="Allow",
                    Principal=principals,
                ),
            ],
        )
