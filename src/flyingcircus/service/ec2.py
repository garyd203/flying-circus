"""General-use classes to interact with the EC2 service through CloudFormation.

See Also:
    `AWS developer guide for EC2
    <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/>`_
"""

from attr import attrib
from attr import attrs

from flyingcircus.core import ATTRSCONFIG
from flyingcircus.core import Stack
from flyingcircus.intrinsic_function import Ref
from .._raw import ec2 as _raw
from .._raw.ec2 import *


class SecurityGroup(_raw.SecurityGroup):
    __slots__ = []

    #: Empty SecurityGroupEgressRule that can be used to replace the default.
    #:
    #: When Cloud Formation creates a security group, if there are no egress
    #: rules specified then it always creates a default egress rule that
    #: allows all-traffic. Sometimes this is undesirable, so the approved
    #: workaround is to create an egress rule that has no effect (eg. allows
    #: traffic to localhost).
    #:
    #:  See Also:
    #:      `Example of replacing the default rule in the SecurityGroup documentation
    #:      <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html>`_
    EMPTY_EGRESS_RULE = dict(
        CidrIp="127.0.0.1/32",
        Description="NOOP rule to prevent CloudFormation from adding a rule that allows all traffic",
        IpProtocol="-1",
    )


@attrs(**ATTRSCONFIG)
class VPC(_raw.VPC):
    _internet_gateway: InternetGateway = attrib(default=None)
    _internet_gateway_attachment: VPCGatewayAttachment = attrib(default=None)

    @property
    def internet_gateway(self) -> InternetGateway:
        """Get the Internet Gateway associated with this VPC.

        This will only work if the internet gateway was created using
        `ensure_internet_gateway_exists`.
        """
        assert (
            self._internet_gateway is not None
        ), "`ensure_internet_gateway_exists` should be called first"
        return self._internet_gateway

    @property
    def internet_gateway_attachment(self) -> VPCGatewayAttachment:
        """Get the attachment object for the Internet Gateway associated with this VPC.

        This will only work if the internet gateway was created using
        `ensure_internet_gateway_exists`.
        """
        assert (
            self._internet_gateway_attachment is not None
        ), "`ensure_internet_gateway_exists` should be called first"
        return self._internet_gateway_attachment

    def ensure_internet_gateway_exists(self, stack: Stack):
        """Ensure there is an internet gateway attached to this VPC as part of the stack."""
        # If we have already attached a gateway to this VPC, then there is
        # nothing more to do
        if self._internet_gateway is not None:
            # Check that the internet gateway is in the desired stack
            if not [
                res for res in stack.Resources.values() if res is self._internet_gateway
            ]:
                raise RuntimeError("Existing InternetGateway is not in this stack")
            if not [
                res
                for res in stack.Resources.values()
                if res is self._internet_gateway_attachment
            ]:
                raise RuntimeError(
                    "Existing VPCGatewayAttachment for InternetGateway is not in this stack"
                )

            return

        # Look for an existing gateway attached to this VPC
        for res in stack.Resources.values():
            if (
                isinstance(res, VPCGatewayAttachment)
                and res.Properties.VpcId == Ref(self)
                and res.Properties.InternetGatewayId
            ):
                self._internet_gateway_attachment = res

                # Try to dodgily unwrap the internet gateway...
                gateway_ref = res.Properties.InternetGatewayId
                if not isinstance(gateway_ref, Ref):
                    raise RuntimeError("Can't deal with direct ID references!")
                if not isinstance(gateway_ref._data, InternetGateway):
                    raise RuntimeError(
                        "There's something weird attached to this VPC instead of an Internet Gateway"
                    )
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
        self._internet_gateway_attachment = VPCGatewayAttachment(
            Properties=VPCGatewayAttachmentProperties(
                InternetGatewayId=Ref(self._internet_gateway), VpcId=Ref(self)
            )
        )

        attachment_stack_name = igw_stack_name + "Attachment"
        if attachment_stack_name in stack.Resources:
            raise RuntimeError(
                f"There's already a resource named {attachment_stack_name}"
            )
        stack.Resources[attachment_stack_name] = self._internet_gateway_attachment
