"""Core classes for composing AWS Cloud Formation Stacks."""
import textwrap
import yaml
import yaml.resolver

from .yaml import NonAliasingDumper
from .yaml import CustomYamlObject


class AWSObject(CustomYamlObject):
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
    # TODO implement equals functionality

    #: Set of valid AWS attribute names for this class
    AWS_ATTRIBUTES = set()  # TODO make a function instead?

    # Attribute Access
    # ----------------

    def __init__(self, **kwargs):
        # Set of unknown AWS attribute names that we have seen in this
        # object. These may or may not still be present.
        self._known_unknown_aws_attributes = set()

        # Set default values
        for key, value in kwargs.items():
            if value is not None:
                try:
                    setattr(self, key, value)
                except AttributeError as ex:
                    # Unrecognised keyword parameters normally get treated as
                    # TypeError's, interestingly.
                    raise TypeError(str(ex)) from ex

    def __setattr__(self, key, value):
        if hasattr(self, key):
            # Allow modification of existing attributes. This avoids madness,
            # whilst also neatly covering some corner cases with our
            # attribute filtering
            super(AWSObject, self).__setattr__(key, value)
            return
        if self._is_internal_attribute(key):
            # Internal attribute
            super(AWSObject, self).__setattr__(key, value)
            return
        if self._is_normal_aws_attribute(key):
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
        if self._is_internal_attribute(key):
            raise AttributeError("'{}' is an internal attribute and should not be set as a AWS attribute".format(key))
        if self._is_normal_aws_attribute(key):
            # TODO throwing an error here stuffs up the code migration when users move to a version that knows about this attribute. At least it's thrown at set-time, not at export time.
            raise AttributeError(
                "'{}' is a recognised AWS attribute and should be set as a normal Python attribute".format(key))

        # Bypass the filtering in our __setattr__ implementation
        object.__setattr__(self, key, value)

        # If we managed to store the attribute successfully, then keep track of it
        self._known_unknown_aws_attributes.add(key)

    def _is_internal_attribute(self, name):
        """Whether this attribute name corresponds to an internal attribute for this object."""
        # Internal attributes all start with an underscore
        return name.startswith("_")

    def _is_normal_aws_attribute(self, name):
        """Whether this attribute name corresponds to a known AWS attribute for this object."""
        # Known AWS attributes are explicitly listed in a class-specific constant
        return name in self.AWS_ATTRIBUTES

    def _is_unknown_aws_attribute(self, name):
        """Whether this attribute name corresponds to an explicitly set but unknown AWS attribute for this object."""
        return name in self._known_unknown_aws_attributes and hasattr(self, name)

    # Container-Like Access
    # ---------------------

    def __getitem__(self, item):
        """Get AWS attributes in a dictionary-like manner."""
        if self._is_normal_aws_attribute(item) or self._is_unknown_aws_attribute(item):
            try:
                return getattr(self, item)
            except AttributeError as ex:
                raise KeyError(str(ex)) from ex
        else:
            raise KeyError(
                "'{}' is not an AWS attribute, and cannot be retrieved with the dictionary interface".format(item))

    def __setitem__(self, key, value):
        """Set AWS attributes in a dictionary-like manner."""
        if self._is_normal_aws_attribute(key) or self._is_unknown_aws_attribute(key):
            setattr(self, key, value)
        else:
            raise KeyError(
                "'{}' is not an AWS attribute, and cannot be set with the dictionary interface".format(key))

    def __delitem__(self, key):
        """Delete AWS attributes in a dictionary-like manner."""
        if self._is_normal_aws_attribute(key) or self._is_unknown_aws_attribute(key):
            try:
                delattr(self, key)
            except AttributeError as ex:
                raise KeyError(str(ex)) from ex
        else:
            raise KeyError(
                "'{}' is not an AWS attribute, and cannot be deleted with the dictionary interface".format(key))

    # TODO implement other container functions: __len__, __iter__, __reversed__, __contains__

    # Export Data
    # -----------

    # TODO change param name to prevent namespace clash
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
        # TODO use the class iterator, which should hadnle the previous two problems for you
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


# TODO new `reflow` function that cleans a long (multi-) line string and marks it as as suitable for PyYAML flow style

def dedent(st):
    """Remove unwanted whitespace from a multi-line string intended for output.

    This is perfect for text embedded inside indented Python code.
    """
    # TODO needs test cases

    lines = st.split('\n')

    # Remove a leading line that contains only a newline character
    if lines and not lines[0]:
        lines = lines[1:]

    # Remove python-style leading indentation on each line
    cleaned_lines = textwrap.dedent('\n'.join(lines))

    return cleaned_lines
