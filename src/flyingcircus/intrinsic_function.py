"""Represent the application of intrinsic CloudFormation functions.

These will probably return a special object that exports as a YAML scalar
("string") containing the function reference. Some functions may be able to
be resolved internally.

See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
"""

from .yaml import CustomYamlObject


class _Function(CustomYamlObject):
    """Base class for all intrinsic CloudFormation functions"""
    pass


class Ref(_Function):
    """Models the behaviour of Ref for Python objects.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html
    """

    # TODO should we provide a version where you just give the logical name (perhaps check it at export time if we are keen)?

    def __init__(self, data):
        """
        :param data: The Python object that is being referenced.
        """
        _Function.__init__(self)
        self._data = data

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(self._data)  # Pass error through
        return dumper.represent_scalar("!Ref", name, style="")
