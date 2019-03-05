Introduction
============

.. pull-quote::
   Putting more *Code* into your *Infrastructure as Code*

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
