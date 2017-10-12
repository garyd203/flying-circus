"""Core classes for composing AWS Cloud Formation Stacks."""
import textwrap

import yaml
import yaml.resolver

from . import function


class NonAliasedDumper(yaml.Dumper):
    """We don't usually want the serializer to use node referneces, because that makes the YAML difficult to read for a human.
    For lack of an option to disable it in pyYAML, we hack this up by clobbering the functionality with a superclass
    """

    def generate_anchor(self, node):
        return None

    def serialize_node(self, node, parent, index):
        self.serialized_nodes = {}
        super(NonAliasedDumper, self).serialize_node(node, parent, index)


class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""

    AWS_CFN_FIELDS = []

    #: See list of supported attributes per resource at http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html
    AWS_ATTRIBUTES = []

    def __init__(self, *args, **kwargs):
        # args are interpreted according to their type
        # kwargs are added as fields using their type and Name

        #: Map of fields that are exported
        self._data = {}

        # Add fields from constructor
        for key, value in kwargs.items():
            self.add(key, value)

        # Create logical name based on supplied physical name. This is pretty dodgy and I am not very happy with it.
        if 'Name' in self._data:
            self.logical_name = self._data['Name']

    # TODO Name. distinguish betwen logical name (for the stack) and physical name (for the created resource). store logical name on the object.
    # TODO add?
    # TODO canonicalise
    # TODO dict-like interface to set/get fields
    # TODO getattr override to emulate the !GetAtt function for special attributes
    # TODO __empty__ or false or whatever it is - are my fields all empty. will work recursively to trim trees

    def export(self, format="yaml"):
        return yaml.dump_all([self], stream=None, Dumper=NonAliasedDumper, line_break=True, default_flow_style=False, explicit_start=True)

    def as_yaml_node(self, dumper):
        """Convert this instance to a PyYAML node."""
        # see yaml.serializer line 102. If you use the "default" tag, then it will be conisdered implicit and the tag name isnt printed out (which is what we desire). Just need to figure out how to best trigger this behaviour.

        data = self._get_ordered_output()

        return dumper.represent_mapping(self._get_yaml_tag(), data)

    def _get_yaml_tag(self):
        """The tag to use when representing this class as a mapping node in YAML."""
        # Ideally, we would create a tag that contains the object name
        # (eg. "!Bucket"). Unfortunately, there is no way to prevent the
        # YAML dumper from printing tags unless it determines that the tag
        # is implicit (ie. the default tag for a mapping node is the tag
        # being used), so we end up just using the default tag.
        #
        # return "!" + self.__class__.__name__
        return yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def __str__(self):
        # TODO support ExportContext state on thread local
        # TODO if no current state, then instantiate a default one (YAML, stdout)
        return self.export()

    def add(self, key, value):
        self._data[key] = value
        return self

    def _get_ordered_output(self):
        """Extract the items that represent this AWS object.

        The default implementation uses everything in self._data, sorted alphabetically.

        :return: An ordered, filtered list of (key, value) pairs.
        """
        return sorted([(k, v) for k, v in self._data.items() if v])

    def __getattr__(self, item):
        if item in self.AWS_ATTRIBUTES:
            return function.GetAtt(getattr(self, "logical_name", self.__class__.__name__), item)  # TODO THis is obviously wrong for the logical nmae
        if item in self._data:
            return self._data[item]
        raise AttributeError(item)
        # TODO handle core Resource attributes: CreationPolicy, DeletionPOlicy, DependsON, Name, Metadata, Properties, UpdatePolicy


yaml.add_multi_representer(BaseAWSObject, lambda dumper, data: data.as_yaml_node(dumper))


def represent_string(dumper, data):
    # Override the normal string emission rules to handle long and short lines differently (for readability)
    if len(data) > 80 or '\n' in data:
        # '|' style means literal block style. So line breaks and formatting are retained.
        return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG, data, "|")
    return dumper.represent_scalar(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG, data, "")


yaml.add_representer(str, represent_string)


class Function(object):
    """Base class to represent an AWS Cloud Formation function."""

    def as_yaml_node(self, dumper):
        """Convert this instance to a PyYAML node."""
        raise NotImplementedError("as_yaml_node() not implemented in abstract class")


yaml.add_multi_representer(Function, lambda dumper, data: data.as_yaml_node(dumper))


class Resource(BaseAWSObject):
    """Base class to represent a single resource in AWS Cloud Formation."""

    AWS_RESOURCE_TYPE = None

    def __init__(self, *args, **kwargs):
        BaseAWSObject.__init__(self, *args, **kwargs)
        assert self.AWS_RESOURCE_TYPE is not None

    def _get_ordered_output(self):
        return [
            ("Type", self.AWS_RESOURCE_TYPE),
            ("Properties", self._data),
        ]


class Parameter(BaseAWSObject):
    """Base class to represent a single parameter in an AWS Cloud Formation stack."""
    pass


class Output(BaseAWSObject):
    """Base class to represent a single output in an AWS Cloud Formation stack."""

    def __init__(self, Name=None, Value=None, Description=None):
        BaseAWSObject.__init__(self, Name == Name, Value=Value, Description=Description)


class Stack(BaseAWSObject):
    """Base class to represent a single stack in AWS Cloud Formation."""

    def __init__(self, *args, **kwargs):
        BaseAWSObject.__init__(self, *args, **kwargs)
        self._data.setdefault('AWSTemplateFormatVersion', '2010-09-09')

    @property
    def Outputs(self):
        return self._data.setdefault('Outputs', {})

    @property
    def Parameters(self):
        return self._data.setdefault('Parameters', {})

    @property
    def Resources(self):
        return self._data.setdefault('Resources', {})

    def _get_ordered_output(self):
        ordered_keys = [
            'AWSTemplateFormatVersion',
            'Description',
            'Parameters',
            'Resources',
            'Outputs',
        ]

        # TODO what if there's stuff that's in _data but not in ordered_keys

        return [(k, self._data[k]) for k in ordered_keys]

    def add(self, key, value):
        if isinstance(value, Output):
            self.Outputs[key] = value
        if isinstance(value, Parameter):
            self.Parameters[key] = value
        elif isinstance(value, Resource):
            self.Resources[key] = value
        else:
            self._data[key] = value
        return self  # Allow call chaining


def reflow(st):
    """Remove unwanted whitespace from a multiline string intended for output.

    This is perfect for text embedded inside indented Python code.
    """
    # Remove leading and trailing blank lines because they confuse the de-denter.
    lines = st.split('\n')
    while lines:
        if not lines[0] or lines[0].isspace():
            lines = lines[1:]
            continue
        if not lines[-1] or lines[-1].isspace():
            lines = lines[:-1]
            continue
        break

    # Remove python-style leading indentation on each line
    cleaned_lines = textwrap.dedent('\n'.join(lines))

    return cleaned_lines
