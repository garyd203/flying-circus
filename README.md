[![PyPI release](https://img.shields.io/pypi/v/flying-circus.svg)](https://pypi.python.org/pypi/flying-circus)
[![Python versions](https://img.shields.io/pypi/pyversions/flying-circus.svg)](https://pypi.python.org/pypi/flying-circus)
[![Build Status](https://dev.azure.com/garyd203/flying-circus/_apis/build/status/garyd203.flying-circus?branchName=master)](https://dev.azure.com/garyd203/flying-circus/_build/latest?definitionId=1&branchName=master)
[![Documentation Status](https://readthedocs.org/projects/flying-circus/badge/?version=latest)](http://flying-circus.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://img.shields.io/pypi/dm/flying-circus.svg)](https://pypi.python.org/pypi/flying-circus)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# flying-circus

Flying Circus is a tool for describing AWS infrastructure as code (using
Python). It uses the same data structures as the AWS Cloud Formation service,
except described as Python objects instead of the usual YAML. The Python
program generates a YAML template, which is passed across to Cloud Formation
in the usual manner.

It is a bit unusual to use a full programming language to describe
infrastructure, instead of a static configuration file like many of us are
used to (whether or not we also utilise a templating tool).
We hope that the Flying Circus library can empower DevOps folk by unlocking
some of the techniques that are available for software code, like named
variables and techniques to structure code independently of the output format,
libraries to allow code re-use with versioning, automated refactoring tools
and so on.

You can learn how to use Flying Circus yourself by reading the
[documentation](https://flying-circus.readthedocs.io/)

# Installation

Install Flying Circus through the Python packaging system:

```bash
pip install flying-circus
```

Many people also use the Amazon Web Services command line tools to deploy
their CloudFormation stacks. If you want this, a good way to install an
up-to-date version is also with `pip`:

```bash
# Optional
pip install awscli
```

# Example

Here is a simple example of how you can use Flying Circus to describe some EC2
instances and deploy them using the AWS CloudFormation service.

First, create a python script (called `my_ec2_stack.py` in this case) to
describe your infrastructure. Any valid Python can be used to create the
Flying Circus objects, along with any valid CloudFormation properties and
attributes.

This example is intentionally simplistic - it just creates two EC2 instances
with varying configuration, and outputs the internal IP for one. However, it
does hint at some of the more complex and powerful usage patterns.

```python
import os

from flyingcircus.core import Stack, Output
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


if __name__ == "__main__":
    stack = Stack()

    stack.Resources["WebServer"] = create_ec2_instance("webserver")
    stack.Resources["DatabaseServer"] = dbserver = create_ec2_instance("dbserver", "t2.medium")
    dbserver.DeletionPolicy = "Retain"

    stack.Outputs["DatabaseServerIp"] = Output(
        Description=f"Internal IP address for the database server",
        Value=GetAtt(dbserver, "PrivateIp"),
    )

    stack.tag(application="api-service", environment="test", owner=os.environ.get("USER"))

    print(stack.export("yaml"))
```

Now generate CloudFormation YAML from your Python script. Note that the result
will *always* be valid well-formatted YAML, and internal checks mean that it
is also difficult to generate invalid CloudFormation.

Finally, use the AWS command line tools to create/update a stack and it's
associated resources.

```bash
python my_ec2_stack.py > my_ec2_stack.yaml
aws cloudformation deploy --stack-name demo-flying-circus-ec2 --template-file my_ec2_stack.yaml
```

You could do these steps in your Continuous Integration server ;-)

# Is/Is Not

There's a lot of tools for managing Infrastructure as Code, often with subtle
differences and passionate advocates. A quick discussion of our scope may
help you understand where Flying Circus fits into this ecosystem, and whether it can
help you. This is presented in the simple "Is/Is Not" format.

## Flying Circus Is...

* ...a Pythonic DSL for writing fully featured Python code
* ...for Amazon Web Services infrastructure
* ...built on top of AWS [Cloud Formation templates](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-guide.html)
* ...a generator that always produces valid, consistent, human-readable, good-practice YAML

## Flying Circus Is Not...

* ...YAML or JSON. It's Python.
* ...a tool to make it easier to write YAML or JSON. You write Python, and YAML is an output format.
* ...a DSL with a completely new syntax. You use normal Python syntax with all
  of it's features and nothing changed.
* ...a templating language, like Jinja2.
* ...a template management tool, like Ansible.
* ...an independent implementation of infrastructure management, like AWS
  Cloud Formation stacks, or Terraform.
* ...a cloud-agnostic abstraction layer.
* ...multi-cloud - although it could become this in the future.
  The current implementation is focused on representing AWS infrastructure
  using the CloudFormation data model. Other cloud providers have similar
  native data models, so it is feasible that we could re-use the concepts and
  tooling to support Google Cloud Platform, etc.
* ...a tool for interacting with the Cloud Formation service. There
  are other tools that can do this for you (such as boto3 or the AWS CLI,
  for starters)
* ...a validation tool - although it could become this in the future, and
  already has elements of validation as a by-product of presenting a helpful
  interface to users.

# Sounds Great, Can I Use It?

Sure, of course you can. The [documentation will get you started](https://flying-circus.readthedocs.io/en/latest/getting_started.html).

Flying Circus is currently in **Beta**. This means it is expected
to work for the supported AWS services, and is in use by real customers.
However, the details of the interface and implementation are still being
validated and may change drastically.

# How Do I Help?

Just use it!
