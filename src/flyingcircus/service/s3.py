from ..core import Resource


class Bucket(Resource):
    """An S3 bucket"""

    AWS_RESOURCE_TYPE = "AWS::S3::Bucket"
