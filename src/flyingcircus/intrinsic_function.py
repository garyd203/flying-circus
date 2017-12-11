"""Represent the application of intrinsic CloudFormation functions.

These will probably return a special object that exports as a YAML scalar
("string") containing the function reference. Some functions may be able to
be resolved internally.

See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
"""

from flyingcircus.core import AWS_Region
from flyingcircus.core import PseudoParameter
from .yaml import CustomYamlObject


# TODO use the rule that every time you detect a nested func, the outer has to use long form


class _Function(CustomYamlObject):
    """Base class for all intrinsic CloudFormation functions"""
    pass


class GetAZs(_Function):
    """Models the behaviour of Fn::GetAZs for Python objects.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getavailabilityzones.html
    """

    def __init__(self, region=""):
        if region == "":
            region = Ref(AWS_Region)
        self._region = region

    def as_yaml_node(self, dumper):
        if isinstance(self._region, _Function):
            return dumper.represent_dict({
                "Fn::GetAZs": self._region
            })
        else:
            return dumper.represent_scalar("!GetAZs", self._region, style="")


class Ref(_Function):
    """Models the behaviour of Ref for Python objects.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html
    """

    # TODO should we provide a version where you just give the logical name (perhaps check it at export time if we are keen)?

    def __init__(self, data):
        """Create a reference to a Resource or Parameter.

        :param data: The Python object that is being referenced.
        """
        # Explicitly reject attempts to use a string name directly, and
        # provide a helpful error message. Beware that PseudoParameters
        # are valid referents, but still look like a string!
        if isinstance(data, str) and not isinstance(data, PseudoParameter):
            raise TypeError("You can't directly create a Ref to a name. Try Ref._for_name(name).")

        _Function.__init__(self)
        self._data = data

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(self._data)  # Pass error through
        return dumper.represent_scalar("!Ref", name, style="")

    @classmethod
    def _for_name(cls, name):
        # TODO doco - you can use this, but better not to
        # TODO implement as a private subclass. Still get type safety, but shortcut the lookup process
        assert False
