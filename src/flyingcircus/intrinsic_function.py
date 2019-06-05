"""Represent the application of CloudFormation intrinsic functions.

These will probably return a special object that exports as a YAML scalar
("string") containing the function reference. Some functions may be able to
be resolved internally.

See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html
"""

from typing import Union

import yaml

from flyingcircus.core import AWS_Region
from flyingcircus.core import PseudoParameter
from .yaml import CustomYamlObject
from .yaml import represent_string


# TODO use the rule that every time you detect a nested func, the outer has to use long form


class _Function(CustomYamlObject):
    """Base class for all CloudFormation intrinsic functions"""

    def _get_string_node(
        self, dumper: yaml.Dumper, value: Union["_Function", str], tag: str
    ) -> yaml.Node:
        """Get a PyYAML node for a function that returns a string.

        Lots of the intrinsic functions take a single string as the argument,
        which we echo directly into the output. However, in CloudFormation,
        this string could be a reference to another function rather than a
        literal string, and that needs to be handled specially.
        """
        if isinstance(value, _Function):
            return dumper.represent_dict({f"Fn::{tag}": value})
        else:
            # TODO be able to control the scalar output, perhaps
            # TODO use represent_string instead, perhaps
            return dumper.represent_scalar(f"!{tag}", value, style="")


class Base64(_Function):
    """Models the behaviour of Fn::Base64 for Python objects.

    Will have the effect of turning the content string into a base64-encoded
    string when the Cloud Formation template is executed.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-base64.html
    """

    def __init__(self, data):
        self._data = data

    def as_yaml_node(self, dumper):
        # TODO If the content is a string, try to format multi-line strings nicely (eg. from EC2 UserData)
        return self._get_string_node(dumper, self._data, "Base64")


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
                raise ValueError(
                    "The attribute name cannot have a {} component".format(
                        component.__class__.__name__
                    )
                )

        self._resource = resource
        self._attribute_name = tuple(attribute_name)

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(
            self._resource, resources_only=True
        )  # Pass error through

        if self._attribute_name_has_refs:
            return dumper.represent_dict(
                {"Fn::GetAtt": [name] + list(self._attribute_name)}
            )
        else:
            return dumper.represent_scalar(
                "!GetAtt", ".".join([name] + list(self._attribute_name)), style=""
            )

    def __eq__(self, other):
        # noinspection PyProtectedMember
        if not isinstance(other, self.__class__):
            return False

        # Two GetAtt calculations are equal if they refer to *exactly* the same object...
        if self._resource is not other._resource:
            return False

        # ... and the same attribute names, calculated in the same way
        return self._attribute_name == other._attribute_name

    def __hash__(self):
        # An immutable class that implements equality should also implement hash.
        # Equal objects should have the same hash, so we derive our hash from
        # the class, the resource, and the attribute list
        return hash((self.__class__, id(self._resource), self._attribute_name))


class GetAZs(_Function):
    """Models the behaviour of Fn::GetAZs for Python objects.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getavailabilityzones.html
    """

    def __init__(self, region=""):
        if region == "":
            region = Ref(AWS_Region)
        self._region = region

    def as_yaml_node(self, dumper):
        return self._get_string_node(dumper, self._region, "GetAZs")


class ImportValue(_Function):
    """Models the behaviour of Fn::ImportValue for Python objects.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-importvalue.html
    """

    def __init__(self, export_name):
        self._export_name = export_name

    def as_yaml_node(self, dumper):
        return self._get_string_node(dumper, self._export_name, "ImportValue")

    def __eq__(self, other):
        # noinspection PyProtectedMember
        if not isinstance(other, self.__class__):
            return False

        # Two references are equal if they refer to the same name (which may
        # be another intrinsic function). We can't dereference other functions
        # to evaluate their final string form, so we do a shallow comparison
        # based on string-or-object.
        return self._export_name == other._export_name

    def __hash__(self):
        # An immutable class that implements equality should also implement hash.
        # Equal objects should have the same hash, so we derive our hash from
        # the class and the name
        return hash((self.__class__, self._export_name))


class Join(_Function):
    """Models the behaviour of Fn::Join for Python objects.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-join.html
    """

    def __init__(self, delimiter, *values):
        """Join several string-like objects together at template execution time.

        Args:
            delimiter: The string used to join the values. May be the empty
                string.
            *values: The values to join together, expressed as either
                sequential parameters, or a single list. May contain other
                intrinsic functions.
        """
        # Check delimiter
        if not isinstance(delimiter, str):
            raise TypeError("Delimiter must be a string")
        if len(delimiter) > 30:
            # CloudFormation does not specify any inherent restriction on
            # delimiter length, but any large delimiter probably represents
            # a coding error
            raise ValueError("Delimiter is very large {}".format(len(delimiter)))

        # Clean values
        if len(values) == 1 and isinstance(values[0], list):
            values = list(values[0])
        else:
            values = list(values)

        if len(values) < 2:
            raise ValueError(
                "`values` parameter must contain at least 2 values to join together"
            )

        # Save fields for YAML output
        self._delimiter = delimiter
        self._values = list(values)

    def as_yaml_node(self, dumper):
        # TODO The default block layout is ugly. Better to use a compact form if values are not too large
        return dumper.represent_sequence("!Join", [self._delimiter, self._values])


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
            raise TypeError(
                "You can't directly create a Ref to a name. Try Ref._for_name(name)."
            )

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
        # Equal objects should have the same hash, so we derive our hash from
        # the class and the referred object
        return hash((self.__class__, id(self._data)))


class Sub(_Function):
    """Models the behaviour of Ref for Python objects.

    See https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-sub.html
    """

    def __init__(self, input: str, **vars):
        """Create a string that will have values substituted in
        by the CloudFormation service

        Args:
            input: Sub-specific string containing "${Name}" -style references
                to values in this CloudFormation template.
            vars: (Optional) Mapping of {name: value} for substituted values
                referenced by the input string, that are not otherwise present
                in this template.
        """
        # Checks
        if not isinstance(input, str):
            raise TypeError("The Fn::Sub function can only accept a string.")
        if isinstance(input, PseudoParameter):
            # Beware that a PseudoParameter is actually a string, in Flying Circus
            raise TypeError(
                "Don't try to use a Pseudo Parameter as the input of Fn::Sub."
            )

        for name in vars.keys():
            if not isinstance(name, str):
                raise TypeError(
                    f"Variable names for Fn::Sub function must be a string, not `{name}`."
                )

        self._input = input
        self._variables = vars

    def as_yaml_node(self, dumper):
        if self._variables:
            # Use long form
            return dumper.represent_sequence("!Sub", [self._input, self._variables])

        # Use short form without any extra named variables.
        #
        # Strings used in Sub tend to be full of special characters, so we
        # force them to be quoted in order to improve readability.

        # TODO not sure this forced quoting makes sense. Maybe revisit with some concrete examples.
        # If we do want it, we need to apply it to the long form as well
        return represent_string(dumper, self._input, tag="!Sub", basicsep="'")
