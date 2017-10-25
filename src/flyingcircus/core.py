"""Core classes for composing AWS Cloud Formation Stacks."""
import textwrap
import yaml
import yaml.resolver

from . import function


class NonAliasingDumper(yaml.Dumper):
    """A YAML dumper that doesn't use aliases or print anchors.

    The use of aliasing in PyYAML is a little bit arbitrary since it depends
    on object identity, rather than equality. Additionally, the use of node
    aliasing usually makes the output more difficult to understand for a
    human. Hence we prefer to not use aliases in our CloudFormation YAML
    output.

    There is no method to disable aliasing in PyYAML, so we work around this
    by using a subclassed Dumper implementation that clobbers the relevant
    functionality.
    """

    def generate_anchor(self, node):
        # Don't generate anchors at all
        return None

    def serialize_node(self, node, parent, index):
        # Don't keep track of previously serialised nodes, so any node will appear to be new.
        self.serialized_nodes = {}
        super(NonAliasingDumper, self).serialize_node(node, parent, index)


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

    # TODO implement __str__ and/or __repr__

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

        if key.startswith("_"):
            # Internal attribute
            raise AttributeError("'{}' is an internal attribute and should not be set as a AWS attribute".format(key))
        if key in self.AWS_ATTRIBUTES:
            # Known AWS attribute
            # TODO throwing an error here stuffs up the code migration when users move to a version that knows about this attribute. At least it's thrown at set-time, not at export time.
            raise AttributeError(
                "'{}' is a recognised AWS attribute and should be set as a normal Python attribute".format(key))

        # Bypass the filtering in our __setattr__ implementation
        object.__setattr__(self, key, value)

    def export(self, format="yaml"):
        """Export this AWS object as CloudFormation in the specified format."""
        # TODO document the formats. 'json' or 'yaml'
        if format == "yaml":
            return yaml.dump_all(
                [self],
                Dumper=NonAliasingDumper,
                default_flow_style=False,
                explicit_start=True,
            )
        else:
            raise ValueError("Export format '{}' is unknown".format(format))

    def as_yaml_node(self, dumper):
        """Get a representation of this object as a PyYAML node."""
        # Ideally, we would create a tag that contains the object name
        # (eg. "!Bucket") for completeness. Unfortunately, there is no way
        # to then prevent the YAML dumper from printing tags unless it
        # determines that the tag is implicit (ie. the default tag for a
        # mapping node is the tag being used), so we end up just using the
        # default tag.
        # TODO investigate hacking a Dumper subclass like we did for aliasing
        tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

        # Get all attributes for export
        # TODO ordering
        # TODO include unknown aws attributes
        attributes = {
            key: getattr(self, key)
            for key in self.AWS_ATTRIBUTES
            if hasattr(self, key)
        }

        # Represent this object as a mapping of it's AWS attributes
        return dumper.represent_mapping(tag, attributes)


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
        return yaml.dump_all([self], stream=None, Dumper=NonAliasingDumper, line_break=True, default_flow_style=False,
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


yaml.add_multi_representer(AWSObject, lambda dumper, data: data.as_yaml_node(
    dumper))  # TODO find a neater way to set this up, that is more tied to the class itself


def represent_string(dumper, data):
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
    """Remove unwanted whitespace from a multi-line string intended for output.

    This is perfect for text embedded inside indented Python code.
    """
    # TODO better name. reflow sounds like it does forced line breaks
    # TODO have functionality variations by providing extra args. eg include_trailing_newlines
    # TODO needs test cases
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


def reflow_trailing(st):  # TODO poor name
    """Reflow a block of text, but add a final trailing newline.

    This is helpful for creating inline block of YAML that need to be compared to generated YAML, which has a final empty line
    """
    return reflow(st) + "\n"
