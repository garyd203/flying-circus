[![Documentation Status](https://readthedocs.org/projects/flying-circus/badge/?version=latest)](http://flying-circus.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/flying-circus.svg)](https://badge.fury.io/py/flying-circus)

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
[documentation](http://flying-circus.readthedocs.io/)

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
* ...a tool to make it easier to write YAML or JSON. You write Python, and YAML is an output.
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

Sure, of course you can.

Flying Circus is currently in **Beta**. This means it is expected
to work for the supported AWS services, and is in use by real customers.
However, the details of the interface and implementation are still being
validated and may change drastically.

# How Do I Help?

Just use it!
