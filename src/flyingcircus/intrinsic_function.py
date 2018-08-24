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


class Base64(_Function):
    """Models the behaviour of Fn::Base64 for Python objects.

    Will have the effect of turning the content string into a base64-encoded
    string when the Cloud Formation template is executed.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-base64.html
    """

    def __init__(self, data):
        self._data = data

    def as_yaml_node(self, dumper):
        # TODO wrap up helper function for this code to detect a nested function. pass in tag and content
        if isinstance(self._data, _Function):
            return dumper.represent_dict({
                "Fn::Base64": self._data
            })
        else:
            # TODO If the content is a string, try to format multi-line strings nicely (eg. from EC2 UserData)
            return dumper.represent_scalar("!Base64", self._data, style="")


class GetAtt(_Function):
    """Models the behaviour of Fn::GetAtt for Python objects.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getavailabilityzones.html
    """

    # TODO Verify that attribute name is valid by comparing it against known
    #  attributes for the resource type in question. This is obviously only
    #  possible if the resource is concrete Resource subclass, and the
    #  attribute name is composed solely of strings.

    # TODO Have AWS attribute access as a special function on the resource
    #  and/or be actual attribute lookup (the latter is perhaps too confusing)

    def __init__(self, resource, *attribute_name):
        """Get a resource attribute from another resource in this stack.

        :param resource: The Python object that contains the resource attribute.
        :param attribute_name: One or more components for the name of the attribute.
            The components may be supplied as a list, or as a single dotted
            string. They may contain Ref objects.
        """
        if isinstance(resource, str):
            raise TypeError("You can't directly create a GetAtt on a logical name.")

        if len(attribute_name) < 1:
            raise ValueError("At least one part of the AWS attribute name is required")

        self._attribute_name_has_refs = False
        for component in attribute_name:
            if isinstance(component, Ref):
                self._attribute_name_has_refs = True
            elif not isinstance(component, str):
                raise ValueError("The attribute name cannot have a {} component".format(component.__class__.__name__))

        self._resource = resource
        self._attribute_name = list(attribute_name)

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(self._resource, resources_only=True)  # Pass error through

        if self._attribute_name_has_refs:
            return dumper.represent_dict({
                "Fn::GetAtt": [name] + self._attribute_name
            })
        else:
            return dumper.represent_scalar("!GetAtt", ".".join([name] + self._attribute_name), style="")


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

    def __init__(self, data):
        """Create a reference to a Resource or Parameter.

        :param data: The Python object that is being referenced.
        """
        # Explicitly reject attempts to use a string name directly, and
        # provide a helpful error message. Beware that PseudoParameters
        # are valid referents, but still look like a string!
        if isinstance(data, str) and not isinstance(data, PseudoParameter):
            raise TypeError("You can't directly create a Ref to a name. Try Ref._for_name(name).")

        self._data = data

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(self._data)  # Pass error through
        return dumper.represent_scalar("!Ref", name, style="")

    @classmethod
    def _for_name(cls, name):
        # TODO doco - you can use this, but better not to
        # TODO implement as a private subclass. Still get type safety, but shortcut the lookup process
        assert False

    def __eq__(self, other):
        # noinspection PyProtectedMember
        if not isinstance(other, self.__class__):
            return False

        # Two references are equal if they refer to *exactly* the same object
        return self._data is other._data

    def __hash__(self):
        # An immutable class that implements equality should also implement hash.
        # Equal objects should have the same hash, so we derive our has from
        # the class and the referred object
        return hash((self.__class__, id(self._data)))
