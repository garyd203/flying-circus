#!/usr/bin/env python3

import os

from flyingcircus.core import Output
from flyingcircus.intrinsic_function import GetAtt
from flyingcircus.service.ec2 import *


def create_ec2_instance(name, instance_type="t2.micro"):
    instance = Instance(Properties=InstanceProperties(
        ImageId="ami-942dd1f6",
        InstanceType=instance_type,
        Monitoring=False,
    ))
    instance.name = name
    return instance


def generate_stack_template():
    stack = Stack()

    stack.Resources["WebServer"] = create_ec2_instance("webserver")

    stack.Resources["DatabaseServer"] = dbserver = create_ec2_instance("dbserver", "t2.medium")
    dbserver.DeletionPolicy = "Retain"

    stack.Outputs["DatabaseServerIp"] = Output(
        Description=f"Internal IP address for the database server",
        Value=GetAtt(dbserver, "PrivateIp"),
    )

    stack.tag(application="api-service", environment="test", owner=os.environ.get("USER"))

    return stack.export("yaml")


if __name__ == "__main__":
    print(generate_stack_template())
