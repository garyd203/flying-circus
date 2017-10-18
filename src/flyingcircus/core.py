"""Core classes for composing AWS Cloud Formation Stacks."""
import textwrap
import yaml
import yaml.resolver

from . import function


class NonAliasedDumper(yaml.Dumper):
    """We don't usually want the serializer to use node references/aliasing, because that makes the YAML difficult to read for a human.
    For lack of an option to disable it in pyYAML, we hack this up by clobbering the functionality with a superclass
    """

    def generate_anchor(self, node):
        return None

    def serialize_node(self, node, parent, index):
        self.serialized_nodes = {}
        super(NonAliasedDumper, self).serialize_node(node, parent, index)


class AWSObject(object):
    """Base class to represent any dictionary-like object from AWS Cloud Formation.

    In general, Cloud Formation attributes are stored directly as Python
    attributes on the object. Any public Python instance attribute is
    considered to be a Cloud Formation attribute. By contrast, a private
    Python attribute (ie. named with a leading underscore) is considered to
    be an internal attribute and is not exported to Cloud Formation.

    Concrete subclasses are expected to implement a constructor that
    explicitly lists all the known AWS attributes. This is intended to help
    with API discovery and IDE auto-completion.

    Default values for attributes are implemented by having a non-None
    default value in the constructor.
    """

    #: Set of valid AWS attribute names for this class
    AWS_ATTRIBUTES = set()  # TODO make a function instead

    def __init__(self, **kwargs):
        # Set default values
        for key, value in kwargs.items():
            if value is not None:
                try:
                    setattr(self, key, value)
                except AttributeError as ex:
                    raise TypeError(str(ex)) from ex

    def __setattr__(self, key, value):
        if hasattr(self, key):
            # Allow modification of existing attributes. This avoids madness,
            # whilst also neatly covering some corner cases with our
            # attribute filtering
            super(AWSObject, self).__setattr__(key, value)
            return
        if key.startswith("_"):
            # Internal attribute
            super(AWSObject, self).__setattr__(key, value)
            return
        if key in self.AWS_ATTRIBUTES:
            # Known AWS attribute
            super(AWSObject, self).__setattr__(key, value)
            return
        raise AttributeError("'{}' is not a recognised AWS attribute for {}".format(key, self.__class__.__name__))

    def export(self, format="yaml"):
        if format == "yaml":
            return ""
        else:
            raise ValueError("Export format '{}' is unknown".format(format))

    def set_unknown_aws_attribute(self, key, value):
        """Override the normal checking and set an AWS attribute that we don't know about.

        This is intended as a bridging mechanism for when older versions of
        the library do not explicitly know about a newly introduced AWS
        attribute.

        Note that normal, known, AWS attributes cannot be set by this method.

        Ideally, users would issue a pull request to fix the problem in our
        type mapping, but this method exists for when you need a workaround.
        """
        # TODO store this attrib somewhere so we know to export it? Or does that all work out in the wash. Write a test...
        if key in self.AWS_ATTRIBUTES:
            # TODO throwing an error here stuffs up the code migration when users move to a version that knows about this attribute. At least it's thrown at set-time, not at export time.
            raise AttributeError(
                "'{}' is a recognised AWS attribute should be set as a normal Python attribute".format(key))

        # Bypass the filtering in our __setattr__ implementation
        object.__setattr__(self, key, value)


class FlattenedObject(AWSObject):
    # TODO an object that collapses a second-level object into attributes on the main object, where the main object would otherwise be trivial (eg. Resource.Properties)
    pass


class _AWSObjectOld(object):
    """Base class to represent any dictionary-like object in AWS Cloud Formation.

    In general, CloudFormation attributes are stored directly as Python
    attributes on the object.
    """

    # TODO filter/validate fields as we set them
    # TODO tests for core class

    CFN_FIELDS = []

    #: See list of supported attributes per resource at http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html
    AWS_ATTRIBUTES = []

    #: These keys, if present, are output first. All other keys are output afterwards, in alphabetical order.
    KEY_ORDER = []

    def __init__(self, *args, **kwargs):
        # args are interpreted according to their type
        # kwargs are added as fields using their type and Name

        #: Map of fields that are exported
        self._data = {}

        # Add fields from constructor
        for key, value in kwargs.items():
            self.add(key, value)

    # TODO Name. distinguish betwen logical name (for the stack) and physical name (for the created resource). store logical name on the object.
    # TODO add?
    # TODO canonicalise
    # TODO dict-like interface to set/get fields
    # TODO getattr override to emulate the !GetAtt function for special attributes
    # TODO __empty__ or false or whatever it is - are my fields all empty. will work recursively to trim trees

    def export(self, format="yaml"):
        # TODO have the option to use aliases in dump (eg. set by export context), but default to no aliases.
        return yaml.dump_all([self], stream=None, Dumper=NonAliasedDumper, line_break=True, default_flow_style=False,
                             explicit_start=True)

    def as_yaml_node(self, dumper):
        """Convert this instance to a PyYAML node."""
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
            return function.GetAtt(getattr(self, "logical_name", self.__class__.__name__),
                                   item)  # TODO THis is obviously wrong for the logical nmae
        if item in self._data:
            return self._data[item]
        raise AttributeError(item)
        # TODO handle core Resource attributes: CreationPolicy, DeletionPOlicy, DependsON, Name, Metadata, Properties, UpdatePolicy

    def get_logical_name(self):
        # TODO figure out based on the object type (eg. Resource, Parameter) and subtype (eg. RoleName vs. Name), where an answer is possible
        raise NotImplementedError()


yaml.add_multi_representer(AWSObject, lambda dumper, data: data.as_yaml_node(dumper))


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


class Resource(AWSObject):
    """Base class to represent a single resource in AWS Cloud Formation."""

    AWS_RESOURCE_TYPE = None

    def __init__(self, *args, **kwargs):
        properties = kwargs.get("Properties", None)
        if properties is not None:
            del kwargs["Properties"]

        AWSObject.__init__(self, *args, **kwargs)

        for key, value in properties.items():
            self.add(key, value)

        assert self.AWS_RESOURCE_TYPE is not None

    def _get_ordered_output(self):
        properties = dict(self._data)
        result = [
            ("Type", self.AWS_RESOURCE_TYPE),
            ("Properties", properties),
        ]

        # Remove Resource-level attributes that are not part of Properties
        # TODO make this cover all attributes, not just DeletionPolicy
        if "DeletionPolicy" in self._data:
            result.append(("DeletionPolicy", self._data["DeletionPolicy"]))
            del properties["DeletionPolicy"]

        return result


class Parameter(AWSObject):
    """Base class to represent a single parameter in an AWS Cloud Formation stack."""
    # TODO explicitly list attributes
    pass


class Output(AWSObject):
    """Base class to represent a single output in an AWS Cloud Formation stack."""

    def __init__(self, Name=None, Value=None, Description=None):
        AWSObject.__init__(self, Name == Name, Value=Value, Description=Description)


class Stack(AWSObject):
    """Base class to represent a single stack in AWS Cloud Formation."""

    def __init__(self, *args, **kwargs):
        AWSObject.__init__(self, *args, **kwargs)
        self._data.setdefault('AWSTemplateFormatVersion', '2010-09-09')  # TODO better done in a factory function.?

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

        return [(k, self._data[k]) for k in ordered_keys if k in self._data]

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
