"""Raw representations of every data type in the AWS EC2 service.

See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/
"""

from ..core import Resource


class Instance(Resource):
    """An EC2 instance.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html
    """

    RESOURCE_TYPE = "AWS::EC2::Instance"

    RESOURCE_PROPERTIES = {
        "Affinity",
        "AvailabilityZone",
        "BlockDeviceMappings",
        "CreditSpecification",
        "DisableApiTermination",
        "EbsOptimized",
        "ElasticGpuSpecifications",
        "HostId",
        "IamInstanceProfile",
        "ImageId",
        "InstanceInitiatedShutdownBehavior",
        "InstanceType",
        "Ipv6AddressCount",
        "Ipv6Addresses",
        "KernelId",
        "KeyName",
        "Monitoring",
        "NetworkInterfaces",
        "PlacementGroupName",
        "PrivateIpAddress",
        "RamdiskId",
        "SecurityGroupIds",
        "SecurityGroups",
        "SourceDestCheck",
        "SsmAssociations",
        "SubnetId",
        "Tags",
        "Tenancy",
        "UserData",
        "Volumes",
    }
