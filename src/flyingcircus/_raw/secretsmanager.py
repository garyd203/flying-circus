"""Raw representations of every data type in the AWS SecretsManager service.

See Also:
    `AWS developer guide for SecretsManager
    <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_

This file is automatically generated, and should not be directly edited.
"""

from ..core import Resource

__all__ = [
    "ResourcePolicy",
    "RotationSchedule",
    "Secret",
    "SecretTargetAttachment",
]


class ResourcePolicy(Resource):
    """A Resource Policy for SecretsManager.

    See Also:
        `AWS Cloud Formation documentation for ResourcePolicy
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html>`_
    """

    RESOURCE_TYPE = "AWS::SecretsManager::ResourcePolicy"

    RESOURCE_PROPERTIES = {
        "ResourcePolicy",
        "SecretId",
    }


class RotationSchedule(Resource):
    """A Rotation Schedule for SecretsManager.

    See Also:
        `AWS Cloud Formation documentation for RotationSchedule
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html>`_
    """

    RESOURCE_TYPE = "AWS::SecretsManager::RotationSchedule"

    RESOURCE_PROPERTIES = {
        "RotationLambdaARN",
        "RotationRules",
        "SecretId",
    }


class Secret(Resource):
    """A Secret for SecretsManager.

    See Also:
        `AWS Cloud Formation documentation for Secret
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html>`_
    """

    RESOURCE_TYPE = "AWS::SecretsManager::Secret"

    RESOURCE_PROPERTIES = {
        "Description",
        "GenerateSecretString",
        "KmsKeyId",
        "Name",
        "SecretString",
        "Tags",
    }


class SecretTargetAttachment(Resource):
    """A Secret Target Attachment for SecretsManager.

    See Also:
        `AWS Cloud Formation documentation for SecretTargetAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::SecretsManager::SecretTargetAttachment"

    RESOURCE_PROPERTIES = {
        "SecretId",
        "TargetId",
        "TargetType",
    }
