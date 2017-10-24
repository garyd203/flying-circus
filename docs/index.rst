Principles:

* complete one-for-one mapping for classes in the raw package - just a straight python representation, same names, same everything. consider enhancing "standard" behaviour for top-level superclasses (like collapsing Properties for Resource)
* Updated classes in the service package, with minor behaviour tweaked for good result
* factory functions for concrete scenarios, with pythonic naming (snake-cased function names and parameter names). SHould this be in another package again? It's more helpful to be in the service package, but it's logically different from the base classes?

General

* use a factory function for modifying class behaviour - reserve classes for the raw data types.

Initial text...

reuse code

test code


Tag line: "Putting the Code back into Infrastructure as Code"

Name ideas
• NB: All the good names are already taken on pypi.
• A high level type of cloud, like cirrus
• Some dramatic powerful cloud-related idea, like thunder storm.
• Thor. He controls clouds.
• Zeus. God of the clouds, etc
• Some God or cloud allusion from Monty python
• (flying circus). Allusion to Monty python. Allusion to ww1 German fighter "formation".  Mis spelling of cirrus

What it is :
• A representation of an AWS cloud formation stack using python (rather than, say, JSON or YAML)
• Enables easy use of coding constructs for code reuse, looping, conditionals, etc.
• Produces good practice, human readable YAML

What it isn't:
• Interface to non-AWS cloud providers
• An abstraction layer
• A new implementation of AWS stacks
• Direct interface to AWS stacks (not yet anyway)
• YAML

Classes we need
1. Base class to represent an AWS CFN resource, plus other low level primitives
2. Base classes to represent all AWS services as resources, with well-defined fields. A bug-for-bug pass-through implementation of existing functionality, complete with quirky names
3. Library of best practice default implementations of all services
4. Library of good practice implementations of common multi-service patterns
5. Multiple (internal) libraries of localised services
6. Concrete stacks built on top of the library classes

Other cross cutting programmatic constructs
• Export to YAML
• Interact with CFN directly
• Extra naming layer that is consistent across services and pythonic
• CFN linter at instance creation time

Programming Standards
• Well tested
• Based off boto3, perhaps
• Clear doco
• Python 2 & 3
• Allow full access to underlying CFN
• Easy exit strategy to go back to YAML
