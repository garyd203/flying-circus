"""General-use classes to interact with the EC2 service through CloudFormation.

See Also:
    `AWS developer guide for EC2
    <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/>`_
"""

from flyingcircus.core import Stack
from flyingcircus.intrinsic_function import Ref
from .._raw import ec2 as _raw

# noinspection PyUnresolvedReferences
from .._raw.ec2 import *


class VPC(_raw.VPC):
    @property
    def internet_gateway(self) -> InternetGateway:
        """Get the Internet Gateway associated with this VPC.

        This will only work if the internet gateway was created using
        `ensure_internet_gateway_exists`.
        """
        assert hasattr(self, "_internet_gateway"), "`ensure_internet_gateway_exists` should be called first"
        return self._internet_gateway

    @property
    def internet_gateway_attachment(self) -> VPCGatewayAttachment:
        """Get the attachment object for the Internet Gateway associated with this VPC.

        This will only work if the internet gateway was created using
        `ensure_internet_gateway_exists`.
        """
        assert hasattr(self, "_internet_gateway_attachment"), "`ensure_internet_gateway_exists` should be called first"
        return self._internet_gateway_attachment

    def ensure_internet_gateway_exists(self, stack: Stack):
        """Ensure there is an internet gateway attached to this VPC as part of the stack."""
        # If we have already attached a gateway to this VPC, then there is
        # nothing more to do
        if hasattr(self, "_internet_gateway"):
            # Check that the internet gateway is in the desired stack
            if not [res for res in stack.Resources.values() if res is self._internet_gateway]:
                raise RuntimeError("Existing InternetGateway is not in this stack")
            if not [res for res in stack.Resources.values() if res is self._internet_gateway_attachment]:
                raise RuntimeError("Existing VPCGatewayAttachment for InternetGateway is not in this stack")

            return

        # Look for an existing gateway attached to this VPC
        for res in stack.Resources.values():
            if isinstance(res, VPCGatewayAttachment) \
                    and res.Properties.get("VpcId", None) == Ref(self) \
                    and res.Properties.get("InternetGatewayId", None):
                self._internet_gateway_attachment = res

                # Try to dodgily unwrap the internet gateway...
                gateway_ref = res.Properties["InternetGatewayId"]
                if not isinstance(gateway_ref, Ref):
                    raise RuntimeError("Can't deal with direct ID references!")
                if not isinstance(gateway_ref._data, InternetGateway):
                    raise RuntimeError("There's something weird attached to this VPC instead of an Internet Gateway")
                self._internet_gateway = gateway_ref._data

                return

        # Create an Internet Gateway
        self._internet_gateway = InternetGateway()
        if self.name:
            # Copy the Name of the VPC if one has already been set
            self._internet_gateway.name = self.name

        igw_stack_name = stack.get_logical_name(self, resources_only=True) + "IGW"
        if igw_stack_name in stack.Resources:
            raise RuntimeError(f"There's already a resource named {igw_stack_name}")
        stack.Resources[igw_stack_name] = self._internet_gateway

        # Attach the gateway to this VPC
        self._internet_gateway_attachment = VPCGatewayAttachment(Properties=dict(
            InternetGatewayId=Ref(self._internet_gateway),
            VpcId=Ref(self),
        ))

        attachment_stack_name = igw_stack_name + "Attachment"
        if attachment_stack_name in stack.Resources:
            raise RuntimeError(f"There's already a resource named {attachment_stack_name}")
        stack.Resources[attachment_stack_name] = self._internet_gateway_attachment
