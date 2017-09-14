"""Core classes for compsinig AWS Cloud Formation Stacks."""


class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""
    pass


class Resource(BaseAWSObject):
    """Base class to represent a single resource in AWS Cloud Formation."""
    pass


class Stack(BaseAWSObject):
    """Base class to represent a single stack in AWS Cloud Formation."""
    pass
