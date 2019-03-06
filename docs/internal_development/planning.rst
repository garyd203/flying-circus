Classes we need
1. Base class to represent an AWS CFN resource, plus other low level primitives
2. Base classes to represent all AWS services as resources, with well-defined fields. A bug-for-bug pass-through implementation of existing functionality, complete with quirky names
3. Library of best practice default implementations of all services
4. Library of good practice implementations of common multi-resource patterns
5. Multiple (internal) libraries of localised services
6. Concrete stacks built on top of the library classes

Other cross cutting programmatic constructs
• Export to YAML
• Interact with CFN directly
• Extra naming layer that is consistent across services and pythonic
• CFN linter at instance creation time
