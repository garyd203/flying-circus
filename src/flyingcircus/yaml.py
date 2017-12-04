"""Helper methods for configuring PyYAML."""

import yaml


def register_yaml_representers():
    """Configure YAML output from PyYAML."""
    # TODO better to add these to a custom Dumper than pollute the global object?

    # Add marshalling/representers for custom types
    yaml.add_representer(str, _represent_string)
    yaml.add_multi_representer(CustomYamlObject, CustomYamlObject.represent_object)

    # Don't silently fail if we try to export something weird
    def unknown_type(dumper, data):
        raise TypeError(
            "{} object cannot be dumped to YAML because it does not "
            "extend CustomYamlObject".format(
                data.__class__.__name__
            )
        )

    yaml.add_multi_representer(object, unknown_type)


class CustomYamlObject(object):
    """Mixin class for objects that have a custom YAML export."""

    def as_yaml_node(self, dumper):
        """Get a representation of this object as a PyYAML node."""
        raise NotImplementedError("as_yaml_node")

    @classmethod
    def represent_object(cls, dumper, data):
        assert isinstance(data, cls)
        return data.as_yaml_node(dumper)


def _represent_string(dumper, data):
    # Override the normal string emission rules to produce the most readable text output
    # TODO test cases
    if '\n' in data:
        # '|' style means literal block style, so line breaks and formatting are retained.
        # This will be especially handy for inline code.
        return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG, data, "|")
    elif len(data) > 65:
        # Longer lines will be automatically folded (ie. have line breaks
        # inserted) by PyYAML, which is likely to cause confusion. We
        # compromise by using the literal block style ('|'), which doesn't
        # fold, but does require some special block indicators.
        # TODO need some way to allow folding. Having a helper function probably isn't really good enough. perhaps have the reflow function return a special subclass of string which we can detect here
        return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG, data, '|')
    else:
        return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG, data, "")


class NonAliasingDumper(yaml.Dumper):
    """A YAML dumper that doesn't use aliases or print anchors.

    The use of aliasing in PyYAML is a little bit arbitrary since it depends
    on object identity, rather than equality. Additionally, the use of node
    aliasing usually makes the output more difficult to understand for a
    human. Finally, AWS CloudFormation doesn't support aliases anyway :-)
    Hence we prefer to not use aliases in our CloudFormation YAML output.

    There is no method to disable aliasing in PyYAML, so we work around this
    by using a subclassed Dumper implementation that clobbers the relevant
    functionality.
    """

    # TODO what about overriding ignore_aliases() instead ?

    def generate_anchor(self, node):
        # Don't generate anchors at all
        return None

    def serialize_node(self, node, parent, index):
        # Don't keep track of previously serialised nodes, so any node will appear to be new.
        self.serialized_nodes = {}
        super(NonAliasingDumper, self).serialize_node(node, parent, index)


class AmazonCFNDumper(NonAliasingDumper, yaml.Dumper):
    """A YAML dumper with output customised for AWS CloudFormation."""

    def __init__(self, *args, **kwargs):
        yaml.Dumper.__init__(self, *args, **kwargs)

        self.__cloud_formation_stack = None

    @property
    def cfn_stack(self):
        """The Cloud Formation stack being exported.

        This should be set by the stack object when it is first represented.
        """
        return self.__cloud_formation_stack

    @cfn_stack.setter
    def cfn_stack(self, value):
        # Checks
        if value is not None:
            from .core import Stack
            if not isinstance(value, Stack):
                raise TypeError(
                    "The current CloudFormation stack must be a Stack object, "
                    "in order to prevent surprise to users."
                )

            if self.__cloud_formation_stack is not None:
                raise RuntimeError("The current CloudFormation stack is already set!")

        # Set value
        self.__cloud_formation_stack = value

    def choose_scalar_style(self):
        if self.analysis is None:
            self.analysis = self.analyze_scalar(self.event.value)

        # If an explicit tag is present on a scalar (eg. because it is a Cloud
        # Formation intrinsic function), try to honour a request for plain
        # scalar style. The default behaviour will always clobber this,
        # which is strange.
        if self.event.style == "" and self.event.tag.startswith("!"):
            if not (self.analysis.empty or self.analysis.multiline):
                return ""

        return super().choose_scalar_style()
