from ..core import Resource


class Role(Resource):
    """An IAM role"""

    AWS_RESOURCE_TYPE = "AWS::IAM::Role"
    AWS_ATTRIBUTES = [
        "Arn",
    ]

