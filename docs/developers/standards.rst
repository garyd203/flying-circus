Programming Standards
=====================

Principles:

* complete one-for-one mapping for classes in the raw package - just a straight python representation, same names, same everything. consider enhancing "standard" behaviour for top-level superclasses (like collapsing Properties for Resource)
* Updated classes in the service package, with minor behaviour tweaked for good result
* factory functions for concrete scenarios, with pythonic naming (snake-cased function names and parameter names). SHould this be in another package again? It's more helpful to be in the service package, but it's logically different from the base classes?

General

* Well tested
* Based off boto3, perhaps
* Clear documentation
* Support Python 2 & 3
* Allow full access to underlying CFN
* Easy exit strategy to go back to YAML

Random points
* use a factory function for modifying class behaviour - reserve classes for the raw data types.
