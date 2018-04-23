"""Raw representations of every data type in the AWS EC2 service.

See Also:
    `AWS developer guide for EC2
    <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/>`_

This file is automatically generated, and should not be directly edited.
"""

from ..core import Resource

__all__ = [
    "CustomerGateway",
    "DHCPOptions",
    "EIP",
    "EIPAssociation",
    "EgressOnlyInternetGateway",
    "FlowLog",
    "Host",
    "Instance",
    "InternetGateway",
    "LaunchTemplate",
    "NatGateway",
    "NetworkAcl",
    "NetworkAclEntry",
    "NetworkInterface",
    "NetworkInterfaceAttachment",
    "NetworkInterfacePermission",
    "PlacementGroup",
    "Route",
    "RouteTable",
    "SecurityGroup",
    "SecurityGroupEgress",
    "SecurityGroupIngress",
    "SpotFleet",
    "Subnet",
    "SubnetCidrBlock",
    "SubnetNetworkAclAssociation",
    "SubnetRouteTableAssociation",
    "TrunkInterfaceAssociation",
    "VPC",
    "VPCCidrBlock",
    "VPCDHCPOptionsAssociation",
    "VPCEndpoint",
    "VPCGatewayAttachment",
    "VPCPeeringConnection",
    "VPNConnection",
    "VPNConnectionRoute",
    "VPNGateway",
    "VPNGatewayRoutePropagation",
    "Volume",
    "VolumeAttachment",
]


class CustomerGateway(Resource):
    """A Customer Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for CustomerGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::CustomerGateway"

    RESOURCE_PROPERTIES = {
        "BgpAsn",
        "IpAddress",
        "Tags",
        "Type",
    }


class DHCPOptions(Resource):
    """A Dhcp Options for EC2.

    See Also:
        `AWS Cloud Formation documentation for DHCPOptions
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::DHCPOptions"

    RESOURCE_PROPERTIES = {
        "DomainName",
        "DomainNameServers",
        "NetbiosNameServers",
        "NetbiosNodeType",
        "NtpServers",
        "Tags",
    }


class EIP(Resource):
    """A Eip for EC2.

    See Also:
        `AWS Cloud Formation documentation for EIP
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EIP"

    RESOURCE_PROPERTIES = {
        "Domain",
        "InstanceId",
    }


class EIPAssociation(Resource):
    """A Eip Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for EIPAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EIPAssociation"

    RESOURCE_PROPERTIES = {
        "AllocationId",
        "EIP",
        "InstanceId",
        "NetworkInterfaceId",
        "PrivateIpAddress",
    }


class EgressOnlyInternetGateway(Resource):
    """A Egress Only Internet Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for EgressOnlyInternetGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-egressonlyinternetgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EgressOnlyInternetGateway"

    RESOURCE_PROPERTIES = {
        "VpcId",
    }


class FlowLog(Resource):
    """A Flow Log for EC2.

    See Also:
        `AWS Cloud Formation documentation for FlowLog
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::FlowLog"

    RESOURCE_PROPERTIES = {
        "DeliverLogsPermissionArn",
        "LogGroupName",
        "ResourceId",
        "ResourceType",
        "TrafficType",
    }


class Host(Resource):
    """A Host for EC2.

    See Also:
        `AWS Cloud Formation documentation for Host
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Host"

    RESOURCE_PROPERTIES = {
        "AutoPlacement",
        "AvailabilityZone",
        "InstanceType",
    }


class Instance(Resource):
    """A Instance for EC2.

    See Also:
        `AWS Cloud Formation documentation for Instance
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html>`_
    """

    # NB: CreationPolicy can be set for Instance
    # (unlike most Resource types)
    AWS_ATTRIBUTES = Resource.AWS_ATTRIBUTES.union({
        "CreationPolicy",
    })

    RESOURCE_TYPE = "AWS::EC2::Instance"

    RESOURCE_PROPERTIES = {
        "AdditionalInfo",
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

    # noinspection PyPep8Naming
    def __init__(
            self, CreationPolicy=None, DeletionPolicy=None, DependsOn=None,
            Properties=None
    ):
        Resource.__init__(self, DeletionPolicy=DeletionPolicy, DependsOn=DependsOn, Properties=Properties)
        self._set_constructor_attributes({
            "CreationPolicy": CreationPolicy,
        })


class InternetGateway(Resource):
    """A Internet Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for InternetGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::InternetGateway"

    RESOURCE_PROPERTIES = {
        "Tags",
    }


class LaunchTemplate(Resource):
    """A Launch Template for EC2.

    See Also:
        `AWS Cloud Formation documentation for LaunchTemplate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::LaunchTemplate"

    RESOURCE_PROPERTIES = {
        "LaunchTemplateData",
        "LaunchTemplateName",
    }


class NatGateway(Resource):
    """A Nat Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for NatGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NatGateway"

    RESOURCE_PROPERTIES = {
        "AllocationId",
        "SubnetId",
        "Tags",
    }


class NetworkAcl(Resource):
    """A Network Acl for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkAcl
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkAcl"

    RESOURCE_PROPERTIES = {
        "Tags",
        "VpcId",
    }


class NetworkAclEntry(Resource):
    """A Network Acl Entry for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkAclEntry
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkAclEntry"

    RESOURCE_PROPERTIES = {
        "CidrBlock",
        "Egress",
        "Icmp",
        "Ipv6CidrBlock",
        "NetworkAclId",
        "PortRange",
        "Protocol",
        "RuleAction",
        "RuleNumber",
    }


class NetworkInterface(Resource):
    """A Network Interface for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterface
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterface"

    RESOURCE_PROPERTIES = {
        "Description",
        "GroupSet",
        "InterfaceType",
        "Ipv6AddressCount",
        "Ipv6Addresses",
        "PrivateIpAddress",
        "PrivateIpAddresses",
        "SecondaryPrivateIpAddressCount",
        "SourceDestCheck",
        "SubnetId",
        "Tags",
    }


class NetworkInterfaceAttachment(Resource):
    """A Network Interface Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterfaceAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterfaceAttachment"

    RESOURCE_PROPERTIES = {
        "DeleteOnTermination",
        "DeviceIndex",
        "InstanceId",
        "NetworkInterfaceId",
    }


class NetworkInterfacePermission(Resource):
    """A Network Interface Permission for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterfacePermission
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterfacePermission"

    RESOURCE_PROPERTIES = {
        "AwsAccountId",
        "NetworkInterfaceId",
        "Permission",
    }


class PlacementGroup(Resource):
    """A Placement Group for EC2.

    See Also:
        `AWS Cloud Formation documentation for PlacementGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-placementgroup.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::PlacementGroup"

    RESOURCE_PROPERTIES = {
        "Strategy",
    }


class Route(Resource):
    """A Route for EC2.

    See Also:
        `AWS Cloud Formation documentation for Route
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Route"

    RESOURCE_PROPERTIES = {
        "DestinationCidrBlock",
        "DestinationIpv6CidrBlock",
        "EgressOnlyInternetGatewayId",
        "GatewayId",
        "InstanceId",
        "NatGatewayId",
        "NetworkInterfaceId",
        "RouteTableId",
        "VpcPeeringConnectionId",
    }


class RouteTable(Resource):
    """A Route Table for EC2.

    See Also:
        `AWS Cloud Formation documentation for RouteTable
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::RouteTable"

    RESOURCE_PROPERTIES = {
        "Tags",
        "VpcId",
    }


class SecurityGroup(Resource):
    """A Security Group for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroup"

    RESOURCE_PROPERTIES = {
        "GroupDescription",
        "GroupName",
        "SecurityGroupEgress",
        "SecurityGroupIngress",
        "Tags",
        "VpcId",
    }


class SecurityGroupEgress(Resource):
    """A Security Group Egress for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroupEgress
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroupEgress"

    RESOURCE_PROPERTIES = {
        "CidrIp",
        "CidrIpv6",
        "Description",
        "DestinationPrefixListId",
        "DestinationSecurityGroupId",
        "FromPort",
        "GroupId",
        "IpProtocol",
        "ToPort",
    }


class SecurityGroupIngress(Resource):
    """A Security Group Ingress for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroupIngress
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroupIngress"

    RESOURCE_PROPERTIES = {
        "CidrIp",
        "CidrIpv6",
        "Description",
        "FromPort",
        "GroupId",
        "GroupName",
        "IpProtocol",
        "SourceSecurityGroupId",
        "SourceSecurityGroupName",
        "SourceSecurityGroupOwnerId",
        "ToPort",
    }


class SpotFleet(Resource):
    """A Spot Fleet for EC2.

    See Also:
        `AWS Cloud Formation documentation for SpotFleet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-spotfleet.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SpotFleet"

    RESOURCE_PROPERTIES = {
        "SpotFleetRequestConfigData",
    }


class Subnet(Resource):
    """A Subnet for EC2.

    See Also:
        `AWS Cloud Formation documentation for Subnet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Subnet"

    RESOURCE_PROPERTIES = {
        "AssignIpv6AddressOnCreation",
        "AvailabilityZone",
        "CidrBlock",
        "Ipv6CidrBlock",
        "MapPublicIpOnLaunch",
        "Tags",
        "VpcId",
    }


class SubnetCidrBlock(Resource):
    """A Subnet Cidr Block for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetCidrBlock
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetCidrBlock"

    RESOURCE_PROPERTIES = {
        "Ipv6CidrBlock",
        "SubnetId",
    }


class SubnetNetworkAclAssociation(Resource):
    """A Subnet Network Acl Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetNetworkAclAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetNetworkAclAssociation"

    RESOURCE_PROPERTIES = {
        "NetworkAclId",
        "SubnetId",
    }


class SubnetRouteTableAssociation(Resource):
    """A Subnet Route Table Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetRouteTableAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetRouteTableAssociation"

    RESOURCE_PROPERTIES = {
        "RouteTableId",
        "SubnetId",
    }


class TrunkInterfaceAssociation(Resource):
    """A Trunk Interface Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for TrunkInterfaceAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-trunkinterfaceassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::TrunkInterfaceAssociation"

    RESOURCE_PROPERTIES = {
        "BranchInterfaceId",
        "GREKey",
        "TrunkInterfaceId",
        "VLANId",
    }


class VPC(Resource):
    """A Vpc for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPC
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPC"

    RESOURCE_PROPERTIES = {
        "CidrBlock",
        "EnableDnsHostnames",
        "EnableDnsSupport",
        "InstanceTenancy",
        "Tags",
    }


class VPCCidrBlock(Resource):
    """A Vpc Cidr Block for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCCidrBlock
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCCidrBlock"

    RESOURCE_PROPERTIES = {
        "AmazonProvidedIpv6CidrBlock",
        "CidrBlock",
        "VpcId",
    }


class VPCDHCPOptionsAssociation(Resource):
    """A Vpcdhcp Options Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCDHCPOptionsAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCDHCPOptionsAssociation"

    RESOURCE_PROPERTIES = {
        "DhcpOptionsId",
        "VpcId",
    }


class VPCEndpoint(Resource):
    """A Vpc Endpoint for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCEndpoint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCEndpoint"

    RESOURCE_PROPERTIES = {
        "PolicyDocument",
        "RouteTableIds",
        "ServiceName",
        "VpcId",
    }


class VPCGatewayAttachment(Resource):
    """A Vpc Gateway Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCGatewayAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCGatewayAttachment"

    RESOURCE_PROPERTIES = {
        "InternetGatewayId",
        "VpcId",
        "VpnGatewayId",
    }


class VPCPeeringConnection(Resource):
    """A Vpc Peering Connection for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCPeeringConnection
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCPeeringConnection"

    RESOURCE_PROPERTIES = {
        "PeerOwnerId",
        "PeerRoleArn",
        "PeerVpcId",
        "Tags",
        "VpcId",
    }


class VPNConnection(Resource):
    """A Vpn Connection for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNConnection
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNConnection"

    RESOURCE_PROPERTIES = {
        "CustomerGatewayId",
        "StaticRoutesOnly",
        "Tags",
        "Type",
        "VpnGatewayId",
        "VpnTunnelOptionsSpecifications",
    }


class VPNConnectionRoute(Resource):
    """A Vpn Connection Route for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNConnectionRoute
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNConnectionRoute"

    RESOURCE_PROPERTIES = {
        "DestinationCidrBlock",
        "VpnConnectionId",
    }


class VPNGateway(Resource):
    """A Vpn Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNGateway"

    RESOURCE_PROPERTIES = {
        "AmazonSideAsn",
        "Tags",
        "Type",
    }


class VPNGatewayRoutePropagation(Resource):
    """A Vpn Gateway Route Propagation for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNGatewayRoutePropagation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNGatewayRoutePropagation"

    RESOURCE_PROPERTIES = {
        "RouteTableIds",
        "VpnGatewayId",
    }


class Volume(Resource):
    """A Volume for EC2.

    See Also:
        `AWS Cloud Formation documentation for Volume
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Volume"

    RESOURCE_PROPERTIES = {
        "AutoEnableIO",
        "AvailabilityZone",
        "Encrypted",
        "Iops",
        "KmsKeyId",
        "Size",
        "SnapshotId",
        "Tags",
        "VolumeType",
    }


class VolumeAttachment(Resource):
    """A Volume Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for VolumeAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VolumeAttachment"

    RESOURCE_PROPERTIES = {
        "Device",
        "InstanceId",
        "VolumeId",
    }
