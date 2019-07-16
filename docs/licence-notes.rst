Licencing - LGPL
================

What?
-----

Flying Circus and its code is made available under the LGPL (GNU Lesser
General Public Licence), version 3.
This is a copy-left open source licence intended for libraries that are used
by other projects, regardless of the licencing that project uses.

The expectation is that if you modify Flying Circus itself (eg. fix a bug in
the core components, or update the mappings to Amazon Web Services) then you
will make those improvements available to the broader community, ideally via
a Pull Request on GitHub. When you use Flying Circus to define your AWS
infrastructure as a separate project or Python module, then that Python code
and any generated artefacts (like Cloud Formation YAML) remains your own,
which you can do with as you please.

Why?
----

The open source community nowadays is a fantastic example of something that is
greater than the sum of it's parts. So much modern software is built on the
shoulders of giants - our predecessors and peers who have created powerful
software for us to use. But there will always be selfish people who take
advantage of everyone else, and don't want to give back to the community.

A GPL-style licence provides a degree of legal protection to force bad
actors to do the right thing, whilst not inconveniencing the rest of us. The
LGPL variant, in particular, allows users to retain IP ownership and
confidentiality for their internal infrastructure, whilst still gaining the
power of Flying Circus.

Thanks for reading. We sincerely hope that Flying Circus helps you, and look
forward to hearing from you in our community.

Third Party
-----------

Flying Circus functionality is implemented using 3rd party libraries that have
their own licences. It is your responsibility to check that these licences
are acceptable to you.

Flying Circus is used in conjunction with Amazon Web Services, as a tool for
using the AWS CloudFormation API. As such, Flying Circus is partially
dependent on the `AWS CloudFormation Template Resource specification
<https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification.html>`_
. The current version of the specification referenced by Flying Circus can be
found in the ``contrib/`` directory in the project's source code.