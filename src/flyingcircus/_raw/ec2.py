"""Raw representations of every data type in the AWS EC2 service.

See Also:
    `AWS developer guide for EC2
    <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/>`_

This file is automatically generated, and should not be directly edited.
"""

from attr import attrib
from attr import attrs

from ..core import ATTRSCONFIG
from ..core import Resource
from ..core import ResourceProperties
from ..core import create_object_converter

__all__ = [
    "CustomerGateway",
    "DHCPOptions",
    "EgressOnlyInternetGateway",
    "EIP",
    "EIPAssociation",
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
    "Volume",
    "VolumeAttachment",
    "VPC",
    "VPCCidrBlock",
    "VPCDHCPOptionsAssociation",
    "VPCEndpoint",
    "VPCEndpointServicePermissions",
    "VPCGatewayAttachment",
    "VPCPeeringConnection",
    "VPNConnection",
    "VPNConnectionRoute",
    "VPNGateway",
    "VPNGatewayRoutePropagation",
]


@attrs(**ATTRSCONFIG)
class CustomerGateway(Resource):
    """A Customer Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for CustomerGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::CustomerGateway"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        BgpAsn = attrib(default=None)
        IpAddress = attrib(default=None)
        Tags = attrib(default=None)
        Type = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class DHCPOptions(Resource):
    """A Dhcp Options for EC2.

    See Also:
        `AWS Cloud Formation documentation for DHCPOptions
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::DHCPOptions"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DomainName = attrib(default=None)
        DomainNameServers = attrib(default=None)
        NetbiosNameServers = attrib(default=None)
        NetbiosNodeType = attrib(default=None)
        NtpServers = attrib(default=None)
        Tags = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class EIP(Resource):
    """A Eip for EC2.

    See Also:
        `AWS Cloud Formation documentation for EIP
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EIP"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Domain = attrib(default=None)
        InstanceId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class EIPAssociation(Resource):
    """A Eip Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for EIPAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EIPAssociation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AllocationId = attrib(default=None)
        EIP = attrib(default=None)
        InstanceId = attrib(default=None)
        NetworkInterfaceId = attrib(default=None)
        PrivateIpAddress = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class EgressOnlyInternetGateway(Resource):
    """A Egress Only Internet Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for EgressOnlyInternetGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-egressonlyinternetgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::EgressOnlyInternetGateway"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class FlowLog(Resource):
    """A Flow Log for EC2.

    See Also:
        `AWS Cloud Formation documentation for FlowLog
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::FlowLog"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DeliverLogsPermissionArn = attrib(default=None)
        LogDestination = attrib(default=None)
        LogDestinationType = attrib(default=None)
        LogGroupName = attrib(default=None)
        ResourceId = attrib(default=None)
        ResourceType = attrib(default=None)
        TrafficType = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class Host(Resource):
    """A Host for EC2.

    See Also:
        `AWS Cloud Formation documentation for Host
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Host"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AutoPlacement = attrib(default=None)
        AvailabilityZone = attrib(default=None)
        InstanceType = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class Instance(Resource):
    """A Instance for EC2.

    See Also:
        `AWS Cloud Formation documentation for Instance
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Instance"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AdditionalInfo = attrib(default=None)
        Affinity = attrib(default=None)
        AvailabilityZone = attrib(default=None)
        BlockDeviceMappings = attrib(default=None)
        CreditSpecification = attrib(default=None)
        DisableApiTermination = attrib(default=None)
        EbsOptimized = attrib(default=None)
        ElasticGpuSpecifications = attrib(default=None)
        HostId = attrib(default=None)
        IamInstanceProfile = attrib(default=None)
        ImageId = attrib(default=None)
        InstanceInitiatedShutdownBehavior = attrib(default=None)
        InstanceType = attrib(default=None)
        Ipv6AddressCount = attrib(default=None)
        Ipv6Addresses = attrib(default=None)
        KernelId = attrib(default=None)
        KeyName = attrib(default=None)
        LaunchTemplate = attrib(default=None)
        Monitoring = attrib(default=None)
        NetworkInterfaces = attrib(default=None)
        PlacementGroupName = attrib(default=None)
        PrivateIpAddress = attrib(default=None)
        RamdiskId = attrib(default=None)
        SecurityGroupIds = attrib(default=None)
        SecurityGroups = attrib(default=None)
        SourceDestCheck = attrib(default=None)
        SsmAssociations = attrib(default=None)
        SubnetId = attrib(default=None)
        Tags = attrib(default=None)
        Tenancy = attrib(default=None)
        UserData = attrib(default=None)
        Volumes = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class InternetGateway(Resource):
    """A Internet Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for InternetGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::InternetGateway"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Tags = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class LaunchTemplate(Resource):
    """A Launch Template for EC2.

    See Also:
        `AWS Cloud Formation documentation for LaunchTemplate
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::LaunchTemplate"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        LaunchTemplateData = attrib(default=None)
        LaunchTemplateName = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NatGateway(Resource):
    """A Nat Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for NatGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NatGateway"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AllocationId = attrib(default=None)
        SubnetId = attrib(default=None)
        Tags = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NetworkAcl(Resource):
    """A Network Acl for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkAcl
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkAcl"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Tags = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NetworkAclEntry(Resource):
    """A Network Acl Entry for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkAclEntry
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkAclEntry"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        CidrBlock = attrib(default=None)
        Egress = attrib(default=None)
        Icmp = attrib(default=None)
        Ipv6CidrBlock = attrib(default=None)
        NetworkAclId = attrib(default=None)
        PortRange = attrib(default=None)
        Protocol = attrib(default=None)
        RuleAction = attrib(default=None)
        RuleNumber = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NetworkInterface(Resource):
    """A Network Interface for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterface
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterface"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Description = attrib(default=None)
        GroupSet = attrib(default=None)
        InterfaceType = attrib(default=None)
        Ipv6AddressCount = attrib(default=None)
        Ipv6Addresses = attrib(default=None)
        PrivateIpAddress = attrib(default=None)
        PrivateIpAddresses = attrib(default=None)
        SecondaryPrivateIpAddressCount = attrib(default=None)
        SourceDestCheck = attrib(default=None)
        SubnetId = attrib(default=None)
        Tags = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NetworkInterfaceAttachment(Resource):
    """A Network Interface Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterfaceAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterfaceAttachment"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DeleteOnTermination = attrib(default=None)
        DeviceIndex = attrib(default=None)
        InstanceId = attrib(default=None)
        NetworkInterfaceId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class NetworkInterfacePermission(Resource):
    """A Network Interface Permission for EC2.

    See Also:
        `AWS Cloud Formation documentation for NetworkInterfacePermission
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::NetworkInterfacePermission"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AwsAccountId = attrib(default=None)
        NetworkInterfaceId = attrib(default=None)
        Permission = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class PlacementGroup(Resource):
    """A Placement Group for EC2.

    See Also:
        `AWS Cloud Formation documentation for PlacementGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-placementgroup.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::PlacementGroup"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Strategy = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class Route(Resource):
    """A Route for EC2.

    See Also:
        `AWS Cloud Formation documentation for Route
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Route"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DestinationCidrBlock = attrib(default=None)
        DestinationIpv6CidrBlock = attrib(default=None)
        EgressOnlyInternetGatewayId = attrib(default=None)
        GatewayId = attrib(default=None)
        InstanceId = attrib(default=None)
        NatGatewayId = attrib(default=None)
        NetworkInterfaceId = attrib(default=None)
        RouteTableId = attrib(default=None)
        VpcPeeringConnectionId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class RouteTable(Resource):
    """A Route Table for EC2.

    See Also:
        `AWS Cloud Formation documentation for RouteTable
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::RouteTable"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Tags = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SecurityGroup(Resource):
    """A Security Group for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroup
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroup"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        GroupDescription = attrib(default=None)
        GroupName = attrib(default=None)
        SecurityGroupEgress = attrib(default=None)
        SecurityGroupIngress = attrib(default=None)
        Tags = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SecurityGroupEgress(Resource):
    """A Security Group Egress for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroupEgress
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroupEgress"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        CidrIp = attrib(default=None)
        CidrIpv6 = attrib(default=None)
        Description = attrib(default=None)
        DestinationPrefixListId = attrib(default=None)
        DestinationSecurityGroupId = attrib(default=None)
        FromPort = attrib(default=None)
        GroupId = attrib(default=None)
        IpProtocol = attrib(default=None)
        ToPort = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SecurityGroupIngress(Resource):
    """A Security Group Ingress for EC2.

    See Also:
        `AWS Cloud Formation documentation for SecurityGroupIngress
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SecurityGroupIngress"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        CidrIp = attrib(default=None)
        CidrIpv6 = attrib(default=None)
        Description = attrib(default=None)
        FromPort = attrib(default=None)
        GroupId = attrib(default=None)
        GroupName = attrib(default=None)
        IpProtocol = attrib(default=None)
        SourcePrefixListId = attrib(default=None)
        SourceSecurityGroupId = attrib(default=None)
        SourceSecurityGroupName = attrib(default=None)
        SourceSecurityGroupOwnerId = attrib(default=None)
        ToPort = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SpotFleet(Resource):
    """A Spot Fleet for EC2.

    See Also:
        `AWS Cloud Formation documentation for SpotFleet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-spotfleet.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SpotFleet"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        SpotFleetRequestConfigData = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class Subnet(Resource):
    """A Subnet for EC2.

    See Also:
        `AWS Cloud Formation documentation for Subnet
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Subnet"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AssignIpv6AddressOnCreation = attrib(default=None)
        AvailabilityZone = attrib(default=None)
        CidrBlock = attrib(default=None)
        Ipv6CidrBlock = attrib(default=None)
        MapPublicIpOnLaunch = attrib(default=None)
        Tags = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SubnetCidrBlock(Resource):
    """A Subnet Cidr Block for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetCidrBlock
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetCidrBlock"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Ipv6CidrBlock = attrib(default=None)
        SubnetId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SubnetNetworkAclAssociation(Resource):
    """A Subnet Network Acl Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetNetworkAclAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetNetworkAclAssociation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        NetworkAclId = attrib(default=None)
        SubnetId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class SubnetRouteTableAssociation(Resource):
    """A Subnet Route Table Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for SubnetRouteTableAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::SubnetRouteTableAssociation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        RouteTableId = attrib(default=None)
        SubnetId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class TrunkInterfaceAssociation(Resource):
    """A Trunk Interface Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for TrunkInterfaceAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-trunkinterfaceassociation.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::TrunkInterfaceAssociation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        BranchInterfaceId = attrib(default=None)
        GREKey = attrib(default=None)
        TrunkInterfaceId = attrib(default=None)
        VLANId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPC(Resource):
    """A Vpc for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPC
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPC"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        CidrBlock = attrib(default=None)
        EnableDnsHostnames = attrib(default=None)
        EnableDnsSupport = attrib(default=None)
        InstanceTenancy = attrib(default=None)
        Tags = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCCidrBlock(Resource):
    """A Vpc Cidr Block for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCCidrBlock
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCCidrBlock"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AmazonProvidedIpv6CidrBlock = attrib(default=None)
        CidrBlock = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCDHCPOptionsAssociation(Resource):
    """A Vpcdhcp Options Association for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCDHCPOptionsAssociation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCDHCPOptionsAssociation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DhcpOptionsId = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCEndpoint(Resource):
    """A Vpc Endpoint for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCEndpoint
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCEndpoint"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        PolicyDocument = attrib(default=None)
        PrivateDnsEnabled = attrib(default=None)
        RouteTableIds = attrib(default=None)
        SecurityGroupIds = attrib(default=None)
        ServiceName = attrib(default=None)
        SubnetIds = attrib(default=None)
        VPCEndpointType = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCEndpointServicePermissions(Resource):
    """A Vpc Endpoint Service Permissions for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCEndpointServicePermissions
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservicepermissions.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCEndpointServicePermissions"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AllowedPrincipals = attrib(default=None)
        ServiceId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCGatewayAttachment(Resource):
    """A Vpc Gateway Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCGatewayAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCGatewayAttachment"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        InternetGatewayId = attrib(default=None)
        VpcId = attrib(default=None)
        VpnGatewayId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPCPeeringConnection(Resource):
    """A Vpc Peering Connection for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPCPeeringConnection
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPCPeeringConnection"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        PeerOwnerId = attrib(default=None)
        PeerRegion = attrib(default=None)
        PeerRoleArn = attrib(default=None)
        PeerVpcId = attrib(default=None)
        Tags = attrib(default=None)
        VpcId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPNConnection(Resource):
    """A Vpn Connection for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNConnection
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNConnection"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        CustomerGatewayId = attrib(default=None)
        StaticRoutesOnly = attrib(default=None)
        Tags = attrib(default=None)
        Type = attrib(default=None)
        VpnGatewayId = attrib(default=None)
        VpnTunnelOptionsSpecifications = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPNConnectionRoute(Resource):
    """A Vpn Connection Route for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNConnectionRoute
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNConnectionRoute"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        DestinationCidrBlock = attrib(default=None)
        VpnConnectionId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPNGateway(Resource):
    """A Vpn Gateway for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNGateway
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNGateway"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AmazonSideAsn = attrib(default=None)
        Tags = attrib(default=None)
        Type = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VPNGatewayRoutePropagation(Resource):
    """A Vpn Gateway Route Propagation for EC2.

    See Also:
        `AWS Cloud Formation documentation for VPNGatewayRoutePropagation
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VPNGatewayRoutePropagation"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        RouteTableIds = attrib(default=None)
        VpnGatewayId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class Volume(Resource):
    """A Volume for EC2.

    See Also:
        `AWS Cloud Formation documentation for Volume
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::Volume"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        AutoEnableIO = attrib(default=None)
        AvailabilityZone = attrib(default=None)
        Encrypted = attrib(default=None)
        Iops = attrib(default=None)
        KmsKeyId = attrib(default=None)
        Size = attrib(default=None)
        SnapshotId = attrib(default=None)
        Tags = attrib(default=None)
        VolumeType = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))


@attrs(**ATTRSCONFIG)
class VolumeAttachment(Resource):
    """A Volume Attachment for EC2.

    See Also:
        `AWS Cloud Formation documentation for VolumeAttachment
        <http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html>`_
    """

    RESOURCE_TYPE = "AWS::EC2::VolumeAttachment"

    @attrs(**ATTRSCONFIG)
    class PropertiesType(ResourceProperties):
        Device = attrib(default=None)
        InstanceId = attrib(default=None)
        VolumeId = attrib(default=None)

    Properties: PropertiesType = attrib(factory=PropertiesType, converter=create_object_converter(PropertiesType))
