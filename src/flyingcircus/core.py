"""Core classes for composing AWS Cloud Formation Stacks."""
import textwrap
import yaml
import yaml.resolver

from .yaml import AmazonCFNDumper
from .yaml import CustomYamlObject


# TODO rename "AWS attribute" to "CloudFormation attribute" everywhere ?
# TODO rename "unknown" AWS attributes to something less confusing.

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

    #: Order in which we write attributes out, when exporting them to a file.
    #: If an attribute is not set, it will not be exported, even if it is
    #: listed here.
    #:
    #: Any attributes not specified here will be listed alphabetically after
    #: these attributes (ie. the default ordering is to list every attribute
    #: in alphabetical order)
    EXPORT_ORDER = []

    # Constructor
    # -----------

    def __init__(self, **kwargs):
        # Set of unknown AWS attribute names that we have seen in this
        # object. These may or may not still be present.
        self._known_unknown_aws_attributes = set()

        # Set initial values passed to constructor
        self._set_constructor_attributes(kwargs)

    def _set_constructor_attributes(self, params):
        """Set any attributes that were passed to the object constructor.

        This requires some special handling to handle constructor-specific
        semantics, in contrast to normal attribute setting.
        """
        for name, value in params.items():
            if value is not None:
                try:
                    setattr(self, name, value)
                except AttributeError as ex:
                    # Unrecognised keyword parameters in a constructor
                    # normally get treated as TypeError's, interestingly.
                    raise TypeError(str(ex)) from ex

    @classmethod
    def _split_current_attributes(cls, params):
        """Filter attribute values to separate those that are defined by the current class."""
        parent_names = super(cls, cls).AWS_ATTRIBUTES
        current_names = cls.AWS_ATTRIBUTES.difference(parent_names)

        current_attribs = {}
        other_params = dict(params)

        for name in current_names:
            try:
                current_attribs[name] = other_params.pop(name)
            except KeyError:
                pass

        return current_attribs, other_params

    # Attribute Access
    # ----------------

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
        # TODO use a better name than "unknown attribute". How about "new attribute"???
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
                Dumper=AmazonCFNDumper,
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
        # TODO use the class iterator, to handle ordering and missing attributes transparently
        attributes = [
            (key, getattr(self, key))
            for key in self._get_export_order()
            if hasattr(self, key)
        ]

        # Represent this object as a mapping of it's AWS attributes
        return dumper.represent_mapping(tag, attributes)

    def _get_export_order(self):
        """Get ordered list of all attribute names that might exist on this object."""
        result = []

        # All valid AWS attributes
        trailing_attribs = self.AWS_ATTRIBUTES.union(self._known_unknown_aws_attributes)

        # Some attributes need to b explicitly listed in a particular order
        # at the beginning of the map output
        for name in self.EXPORT_ORDER:
            try:
                trailing_attribs.remove(name)
            except KeyError:
                # The explicit attribute ordering refers to a attribute that
                # is not valid. This could indicate a configuration problem,
                # but failures here are stylistic rather than critical, so
                # we choose to silently ignore any problems.
                # TODO log warning message
                continue
            result.append(name)

        # Include all remaining attributes in standard sort order
        result.extend(sorted(trailing_attribs, key=self._get_export_sort_key))
        return result

    @classmethod
    def _get_export_sort_key(cls, st):
        """Sort method for sorting dictionary keys when exporting."""
        # We want to order alphabetically in a case-insensitive fashion, but
        # we also want to ensure consistency in the event of two keys that
        # differ only in case (crazy as that may be). The best way to achieve
        # this is to use a compound key that falls back to the original value.
        return st.lower(), st


class Stack(AWSObject):
    """Represents a CloudFormation Stack, the top-level template object.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html
    """

    # This is in the order recommended in the documentation
    EXPORT_ORDER = [
        "AWSTemplateFormatVersion", "Description", "Metadata", "Parameters",
        "Mappings", "Conditions", "Transform", "Resources", "Outputs",
    ]

    AWS_ATTRIBUTES = {
        "AWSTemplateFormatVersion", "Conditions", "Description", "Mappings",
        "Metadata", "Outputs", "Parameters", "Resources", "Transform",
    }

    def __init__(self, AWSTemplateFormatVersion=None, Conditions=None,
                 Description=None, Mappings=None, Metadata=None, Outputs=None,
                 Parameters=None, Resources=None, Transform=None):
        # We default to the most recent format version
        # TODO #55 consider functionality to set defaults in a generic way. Not sure how much it would be needed, so maybe not worth the fuss
        if AWSTemplateFormatVersion is None:
            AWSTemplateFormatVersion = "2010-09-09"

        AWSObject.__init__(**locals())

        # TODO We really want issue #45 to auto-initialise all the sets
        if not hasattr(self, "Conditions"):
            self.Conditions = {}
        if not hasattr(self, "Mappings"):
            self.Mappings = {}
        if not hasattr(self, "Metadata"):
            self.Metadata = {}
        if not hasattr(self, "Outputs"):
            self.Outputs = {}
        if not hasattr(self, "Parameters"):
            self.Parameters = {}
        if not hasattr(self, "Resources"):
            self.Resources = {}
        if not hasattr(self, "Transform"):
            self.Transform = {}

    def get_logical_name(self, resource):
        """Get the logical name used for this object in this stack.

        Raises ValueError if the object is not in this stack.
        """
        # Pseudo Parameters are a special case. They can be thought of as
        # implicitly part of the current stack, so we support finding them
        # through this function
        if isinstance(resource, PseudoParameter):
            return str(resource)

        # The lazy and non-performant approach is to iterate through all
        # the objects in this stack until we find the supplied object.
        # That should do for now, really.
        for object_type in ["Resources", "Parameters"]:
            objects = getattr(self, object_type, {})
            matches = [name for name, data in objects.items() if data is resource]
            if len(matches) > 1:
                raise ValueError("Object has multiple names in this stack: {}".format(resource))
            elif len(matches) == 1:
                return matches[0]
        raise ValueError("Object is not part of this stack: {}".format(resource))

    def as_yaml_node(self, dumper):
        dumper.cfn_stack = self
        return super().as_yaml_node(dumper)


class PseudoParameter(str):
    """Represents an AWS-provided pseudo parameter.

    This is simply a string with extra mixin behaviour.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html
    """

    #: Set of all AWS pseudo-parameters
    ALL = set()

    # TODO if we try to use it as a YAML scalar, then implicitly make it be a Ref? Do with as_yaml_node()

    @classmethod
    def _create_standard_parameter(cls, name):
        obj = cls(name)
        cls.ALL.add(obj)
        return obj


# TODO not convinced about the names of the constants, or about putting them in this namespace
AWS_AccountId = PseudoParameter._create_standard_parameter("AWS::AccountId")
AWS_NotificationARNs = PseudoParameter._create_standard_parameter("AWS::NotificationARNs")
AWS_NoValue = PseudoParameter._create_standard_parameter("AWS::NoValue")
AWS_Partition = PseudoParameter._create_standard_parameter("AWS::Partition")
AWS_Region = PseudoParameter._create_standard_parameter("AWS::Region")
AWS_StackId = PseudoParameter._create_standard_parameter("AWS::StackId")
AWS_StackName = PseudoParameter._create_standard_parameter("AWS::StackName")
AWS_URLSuffix = PseudoParameter._create_standard_parameter("AWS::URLSuffix")


class Resource(AWSObject):
    """Represents a CloudFormation Resource in a Stack.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resources-section-structure.html
    and http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html
    """

    # This list includes the attributes that are defined at this level by
    # CloudFormation, but only listed in AWS_ATTRIBUTES in some subclasses.
    EXPORT_ORDER = ["Type", "DependsOn", "Metadata", "CreationPolicy", "UpdatePolicy", "DeletionPolicy", "Properties"]

    AWS_ATTRIBUTES = {
        # NB: CreationPolicy is defined as a Resource-level attribute, but is
        # currently only valid for AutoScalingGroup, EC2::Instance and
        # CloudFormation::WaitCondition.
        #
        # See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html
        #
        # "CreationPolicy",
        "DeletionPolicy",
        "DependsOn",
        #: Note that Metadata is not expected to be used by Flying Circus
        #: users, so it can't be set in the constructor. However, you can
        #: still modify it and set it as an attribute if you must.
        "Metadata",
        "Properties",
        #: Note that Type is coupled to the Flying Circus Python type, and
        #: can't be directly set
        "Type",
        # NB: UpdatePolicy is defined as a Resource-level attribute, but is
        # currently only valid for AutoScalingGroup.
        #
        # See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html
        #
        # "UpdatePolicy",
    }

    #: The AWS CloudFormation string for this resource's Type
    RESOURCE_TYPE = None

    #: Set of valid property names for this Resource class
    RESOURCE_PROPERTIES = set()

    # TODO classmethod to instantiate a Properties object for this resource type. Or better, have a hard-wired Properties initialised in __init__
    # TODO implement a shortcut function for get_ref(), instead of having to bring in the fn.Ref function?

    def __init__(self, DeletionPolicy=None, DependsOn=None, Properties=None):
        if Properties is None:
            # TODO better to use the (not yet existing) generic hook to pre-initialise all complex objects. See issue #45
            Properties = ResourceProperties(self.RESOURCE_PROPERTIES)

        AWSObject.__init__(**locals())

        if not self.RESOURCE_TYPE:
            raise TypeError(
                "Concrete Resource class {} needs to define the "
                "CloudFormation Type as a class variable called "
                "RESOURCE_TYPE".format(
                    self.__class__.__name__
                )
            )

    @property
    def Type(self):
        # The Type attribute is read-only because it is coupled to the
        # underlying class via this class constant. The easiest way to
        # achieve this is through a property
        return self.RESOURCE_TYPE


class ResourceProperties(AWSObject):
    def __init__(self, property_names, **properties):
        self.AWS_ATTRIBUTES = property_names
        AWSObject.__init__(self, **properties)


# TODO new `reflow` function that cleans a long (multi-) line string from IDE padding, and marks it as as suitable for PyYAML flow style

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
