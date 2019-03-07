Getting Started
===============

Installation
------------

Install Flying Circus through the Python packaging system:

.. code-block:: bash

   pip install flying-circus

Many people also use the Amazon Web Services command line tools to deploy
their CloudFormation stacks. The Python packaging system is a good way to
install an up-to-date version of these too:

.. code-block:: bash

   # Optional
   pip install awscli


Example
-------

Here is a simple example of how you can use Flying Circus to describe some EC2
instances and deploy them using the AWS CloudFormation service.

First, create a python script (called `ec2_example.py` in this case) to
describe your infrastructure. Any valid Python can be used to create the
Flying Circus objects, along with any valid CloudFormation properties and
attributes.

This example is intentionally simplistic - it just creates two EC2 instances
with varying configuration, and outputs the internal IP address for one.
However, it does hint at some of the more complex and powerful usage patterns.

.. literalinclude:: ec2_example.py
   :language: python

Now generate CloudFormation YAML from your Python script. Note that the result
will *always* be valid well-formatted YAML, and internal checks mean that it
is also difficult to generate invalid CloudFormation.

Finally, use the AWS command line tools to create/update a stack and it's
associated resources (assuming you have configured your AWS credentials...).

.. code-block:: bash

   python ec2_example.py > ec2_example.yaml
   aws cloudformation deploy --stack-name flying-circus-ec2-example --template-file ec2_example.yaml

These last steps are an obvious candidate to go in your Continuous Integration server ;-)