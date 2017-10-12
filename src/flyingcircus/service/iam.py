from .._raw import iam as raw
from .._raw.iam import *

__all__ = [
    "Policy",
    "PolicyDocument",
    "PolicyStatement",
    "PrincipalSet",
    "Role",
    "simple_assume_role_policy",
]

class PolicyDocument(raw.PolicyDocument):
    def _override_function_that_updates_parameters_with_default_values(self):
        pass


class Defaults:
    """Standard implementation of all raw classes with sensible defaults"""

    @staticmethod
    def PolicyDocument(Version="2012-10-17",
                       **kwargs):  # TODO want all arguments to be present here for autocomplete and typing
        # kwargs.setdefault("Version", "2012-10-17")
        return raw.PolicyDocument(**kwargs)


class BestPractice:
    """Best-practice implementations for basic scenarios, cookbook-style"""
    # TODO advanced scenarios should be in another package, maybe?
    pass


def simple_assume_role_policy(principals):
    """Create a simple trust policy document to describe who can assume a role."""
    return PolicyDocument(
        Version='2012-10-17',
        Statement=[
            PolicyStatement(
                Action=['sts:AssumeRole'],
                Effect="Allow",
                Principal=principals,
            ),
        ],
    )


class Principal:
    """Factory methods to create strings for different sorts of principal.

    These do not comprise a standalone PrincipalSet, but are used to build one.
    """

    @staticmethod
    def aws_account(accountid):
        return 'arn:aws:iam::{}:root'.format(accountid)

    @staticmethod
    def iam_user(accountid, username):
        return 'arn:aws:iam::{}:user/{}'.format(accountid, username)

