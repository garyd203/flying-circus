"""Represent the application of YAML functions.

These will probably return a special object that resolves into a YAML string scalar containing the function reference. Some functions may be able to be resolved internally (hah!).
"""
from .core import *


class GetAtt(Function):
    """Models the behaviour of Fn:GetAtt for Python objects.

    From http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html
        The Fn::GetAtt intrinsic function returns the value of an attribute from a resource in the template
    """

    def __init__(self, logicalNameOfResource, attributeName):
        self._resource_name = logicalNameOfResource
        self._attribute_name = attributeName

    def as_yaml_node(self, dumper):
        return dumper.represent_scalar("!GetAtt", "{}.{}".format(self._resource_name, self._attribute_name), style='')


class Join(Function):
    """Models the behaviour of Fn:Join for Python objects.

    From http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-join.html
        The intrinsic function Fn::Join appends a set of values into a single value, separated by the specified delimiter. If a delimiter is the empty string, the set of values are concatenated with no delimiter.
    """

    def __init__(self, delimiter, *values):
        self._delimiter = delimiter
        self._values = list(values)

    def as_yaml_node(self, dumper):
        args = [self._delimiter, self._values]
        return dumper.represent_sequence("!Join", args, flow_style='[')
