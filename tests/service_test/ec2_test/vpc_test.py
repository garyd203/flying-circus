"""Test VPC service components."""

import pytest

from flyingcircus.core import Stack
from flyingcircus.intrinsic_function import Ref
from flyingcircus.service.ec2 import InternetGateway
from flyingcircus.service.ec2 import VPC
from flyingcircus.service.ec2 import VPCGatewayAttachment
from flyingcircus.service.ec2 import VPNGateway


class TestVpcEnsureInternetGatewayExists:
    """Verify behaviour of VPC.ensure_internet_gateway_exists()
    and associated access functions.
    """

    def _verify_resource_is_in_stack(self, resource, stack, unique=False):
        """Verify that the supplied resource exists in this stack.

        Params:
            unique (bool): Whether this should be the only resource of it's
                type in the stack.
        """
        all_resources = [
            res
            for res in stack.Resources.values()
            if isinstance(res, resource.__class__)
        ]
        if unique:
            assert (
                len(all_resources) == 1
            ), "Stack contains several {} resources".format(resource.Type)

        identical_resources = [res for res in all_resources if res is resource]
        assert len(identical_resources) == 1, "Resource should be in stack exactly once"

    def _verify_vpc_has_valid_internet_gateway(self, vpc):
        assert vpc.internet_gateway is not None
        assert isinstance(vpc.internet_gateway, InternetGateway)

        assert vpc.internet_gateway_attachment is not None
        assert isinstance(vpc.internet_gateway_attachment, VPCGatewayAttachment)
        assert vpc.internet_gateway_attachment.Properties["InternetGatewayId"] == Ref(
            vpc.internet_gateway
        )
        assert vpc.internet_gateway_attachment.Properties["VpcId"] == Ref(vpc)

    def test_should_create_resources_in_stack(self):
        # Setup
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()

        # Exercise
        vpc.ensure_internet_gateway_exists(stack)

        # Verify
        self._verify_vpc_has_valid_internet_gateway(vpc)
        self._verify_resource_is_in_stack(vpc.internet_gateway, stack, unique=True)
        self._verify_resource_is_in_stack(
            vpc.internet_gateway_attachment, stack, unique=True
        )

    def test_should_do_nothing_when_called_a_second_time(self):
        # Setup: Create stack
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()

        # Setup: Call once
        vpc.ensure_internet_gateway_exists(stack)
        original_igw = vpc.internet_gateway
        original_attachment = vpc.internet_gateway_attachment

        # Exercise
        vpc.ensure_internet_gateway_exists(stack)

        # Verify
        self._verify_vpc_has_valid_internet_gateway(vpc)
        self._verify_resource_is_in_stack(vpc.internet_gateway, stack, unique=True)
        self._verify_resource_is_in_stack(
            vpc.internet_gateway_attachment, stack, unique=True
        )

        # Verify Internet Gateway hasn't changed
        assert vpc.internet_gateway is original_igw
        assert vpc.internet_gateway_attachment is original_attachment

    def test_should_throw_error_when_called_a_second_time_with_wrong_stack(self):
        # Setup: Create stack with gateway
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()
        vpc.ensure_internet_gateway_exists(stack)

        # Setup: Create second stack
        unrelated_stack = Stack()

        # Exercise & Verify
        with pytest.raises(RuntimeError) as excinfo:
            vpc.ensure_internet_gateway_exists(unrelated_stack)

        assert "not in this stack" in str(excinfo.value)

    def test_should_use_existing_igw_attached_to_vpc_in_stack(self):
        # Setup
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()
        stack.Resources["MyGateway"] = igw = InternetGateway()
        stack.Resources["MyGatewayAttachment"] = attachment = VPCGatewayAttachment(
            Properties=dict(InternetGatewayId=Ref(igw), VpcId=Ref(vpc))
        )

        # Exercise
        vpc.ensure_internet_gateway_exists(stack)

        # Verify
        self._verify_vpc_has_valid_internet_gateway(vpc)
        self._verify_resource_is_in_stack(vpc.internet_gateway, stack, unique=True)
        self._verify_resource_is_in_stack(
            vpc.internet_gateway_attachment, stack, unique=True
        )

        # Verify existing Internet Gateway is used
        assert vpc.internet_gateway is igw
        assert vpc.internet_gateway_attachment is attachment

    def test_should_not_use_existing_igw_attached_to_different_vpc_in_stack(self):
        # Setup
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()
        stack.Resources["OtherVPC"] = other_vpc = VPC()
        stack.Resources["MyGateway"] = igw = InternetGateway()
        stack.Resources["MyGatewayAttachment"] = attachment = VPCGatewayAttachment(
            Properties=dict(InternetGatewayId=Ref(igw), VpcId=Ref(other_vpc))
        )

        # Exercise
        vpc.ensure_internet_gateway_exists(stack)

        # Verify
        self._verify_vpc_has_valid_internet_gateway(vpc)
        self._verify_resource_is_in_stack(vpc.internet_gateway, stack)
        self._verify_resource_is_in_stack(vpc.internet_gateway_attachment, stack)

        # Verify existing Internet Gateway attachment is not used
        assert igw is not vpc.internet_gateway
        self._verify_resource_is_in_stack(igw, stack)

        assert attachment is not vpc.internet_gateway_attachment
        self._verify_resource_is_in_stack(attachment, stack)

    def test_should_not_use_existing_non_igw_attached_to_vpc_in_stack(self):
        # Setup
        stack = Stack()
        stack.Resources["MyVPC"] = vpc = VPC()
        stack.Resources["MyGateway"] = vpn_gateway = VPNGateway(
            Properties=dict(Type="ipsec.1")
        )
        stack.Resources["MyGatewayAttachment"] = attachment = VPCGatewayAttachment(
            Properties=dict(VpcId=Ref(vpc), VpnGatewayId=Ref(vpn_gateway))
        )

        # Exercise
        vpc.ensure_internet_gateway_exists(stack)

        # Verify
        self._verify_vpc_has_valid_internet_gateway(vpc)
        self._verify_resource_is_in_stack(vpc.internet_gateway, stack, unique=True)
        self._verify_resource_is_in_stack(vpc.internet_gateway_attachment, stack)

        # Verify existing Internet Gateway is not used
        assert attachment is not vpc.internet_gateway_attachment
        self._verify_resource_is_in_stack(attachment, stack)
