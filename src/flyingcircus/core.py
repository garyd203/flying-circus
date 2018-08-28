"""Core classes for composing AWS Cloud Formation Stacks."""

import copy
import re
import textwrap
from itertools import chain

import yaml
import yaml.resolver

from flyingcircus.exceptions import StackMergeError
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

    # TODO implement other container functions: __reversed__, __contains__

    # TODO probably need __reversed__ otherwise an attempt to reverse the object will break like crazy (int item lookups)

    def __iter__(self):
        # We treat the object like a dictionary for iteration. This means
        # we return a sorted list of AWS attribute names that are currently set
        for key in self._get_export_order():
            if hasattr(self, key):
                yield key

    def __len__(self):
        # The length of the object is the number of attributes currently set
        return len(
            [key for key in self.AWS_ATTRIBUTES if hasattr(self, key)] +
            [key for key in self._known_unknown_aws_attributes if hasattr(self, key)]
        )

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

        # Get all attributes for export in our customised sort order
        attributes = [(key, self[key]) for key in self]

        # Create neater YAML by filtering out empty blocks at this level
        attributes = [(key, value) for key, value in attributes if is_non_empty_attribute(value)]

        # Create neater YAML by filtering out empty entries in sub-lists
        attributes = [(key, remove_empty_values_from_attribute(value)) for key, value in attributes]

        # Represent this object as a mapping of it's AWS attributes.
        # Note that `represent_mapping` works on a list of 2-tuples, not a map!
        return dumper.represent_mapping(tag, attributes)

    def _get_export_order(self):
        """Get ordered list of all attribute names that might exist on this object."""
        # TODO Rename - not just export order, but iteration order
        result = []

        # All valid AWS attributes
        trailing_attribs = self.AWS_ATTRIBUTES.union(self._known_unknown_aws_attributes)

        # Some attributes need to be explicitly listed in a particular order
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


def remove_empty_values_from_attribute(data):
    """If this attribute is a list or dictionary, return a copy with empty entries recursively removed."""
    if isinstance(data, list):
        cleaned = map(remove_empty_values_from_attribute, data)
        cleaned = filter(is_non_empty_attribute, cleaned)
        return list(cleaned)
    elif isinstance(data, dict):
        cleaned = {key: remove_empty_values_from_attribute(value) for key, value in data.items()}
        cleaned = {key: value for key, value in cleaned.items() if is_non_empty_attribute(value)}
        return dict(cleaned)

    # Don't modify other types
    return data


def is_non_empty_attribute(data):
    """Is this attribute of an AWS object non-empty?

    The purpose of this function is to provide clean output by not exporting
    data that has no semantic meaning. It is worth noting that empty-ish
    values like None and "" do actually have a meaning.

    A non-empty object is defined recursively as:
      - not a block-like object
      - a block-like object that contains at least one non-empty attribute.
    """
    if isinstance(data, (tuple, list)):
        for value in data:
            if is_non_empty_attribute(value):
                return True
        return False
    elif isinstance(data, dict):
        for value in data.values():
            if is_non_empty_attribute(value):
                return True
        return False
    elif isinstance(data, AWSObject):
        for key in data:
            if is_non_empty_attribute(data[key]):
                return True
        return False

    # Other types of object are never empty
    return True


class _EmptyList(CustomYamlObject):
    """Represents an immutable YAML-isable list with no entries."""

    def as_yaml_node(self, dumper):
        return dumper.represent_list([])


#: Signal value for an empty list.
#:
#: Normally empty lists are trimmed from the AWSObject's export, in
#: order to produce cleaner YAML. This special object will allow you to
#: force the export of an empty list.
EMPTY_LIST = _EmptyList()


class _EmptyDict(CustomYamlObject):
    """Represents an immutable YAML-isable dictionary with no items."""

    def as_yaml_node(self, dumper):
        return dumper.represent_dict({})


#: Signal value for an empty dictionary.
#:
#: Normally empty dictionaries are trimmed from the AWSObject's export, in
#: order to produce cleaner YAML. This special object will allow you to
#: force the export of an empty dictionary.
EMPTY_DICT = _EmptyDict()


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
        # TODO #56 consider functionality to set defaults in a generic way. Not sure how much it would be needed, so maybe not worth the fuss
        if AWSTemplateFormatVersion is None:
            AWSTemplateFormatVersion = "2010-09-09"

        AWSObject.__init__(**locals())

        # TODO We really want issue #45 to auto-initialise all the sets
        if not hasattr(self, "Parameters"):
            self.Parameters = {}
        if not hasattr(self, "Resources"):
            self.Resources = {}
        if not hasattr(self, "Outputs"):
            self.Outputs = {}

    def as_yaml_node(self, dumper):
        dumper.cfn_stack = self
        return super().as_yaml_node(dumper)

    def get_logical_name(self, resource, resources_only=False):
        """Get the logical name used for this object in this stack.

        Raises ValueError if the object is not in this stack.
        """
        # Pseudo Parameters are a special case. They can be thought of as
        # implicitly part of the current stack, so we support finding them
        # through this function
        if not resources_only and isinstance(resource, PseudoParameter):
            return str(resource)

        # The lazy and non-performant approach is to iterate through all
        # the objects in this stack until we find the supplied object.
        # That should do for now, really.
        matches = [name for name, data in self.Resources.items() if data is resource]
        if not resources_only:
            matches.extend([name for name, data in self.Parameters.items() if data is resource])

        if len(matches) > 1:
            raise ValueError("Object has multiple names in this stack: {}".format(resource))
        elif len(matches) == 1:
            return matches[0]
        raise ValueError("Object is not part of this stack: {}".format(resource))

    def merge_stack(self, other):
        """Add a reference in this stack to all objects from the supplied stack.

        Return the current stack for call-chaining purposes.
        """
        # Check that we aren't using incompatible versions. Note that the
        # 'Transform' attribute is currently used to store the version of
        # the Serverless Application Model we are using (if any), so it
        # counts as a version too.
        if self.AWSTemplateFormatVersion != other.AWSTemplateFormatVersion:
            raise StackMergeError(
                "This template has a different template version ({}) to the "
                "other template ({})".format(
                    self.AWSTemplateFormatVersion, other.AWSTemplateFormatVersion
                )
            )
        if getattr(self, "Transform", None) is not None and \
                getattr(other, "Transform", None) is not None and \
                self.Transform != other.Transform:
            raise StackMergeError(
                "This template has a different Serverless Application Model "
                "Transform version ({}) to the other template ({})".format(
                    self.Transform, other.Transform
                )
            )

        # Check for output's with a repeated name. The export name can be
        # different from the logical name of the Output in the stack, so it
        # wouldn't otherwise be checked.
        #
        # Duplicated export names are picked up by cloud formation when we
        # import the template, but when merging stacks it is a lot more
        # helpful to catch these errors early
        # TODO what if Export is not a simple dict?
        existing_exports = {getattr(output, "Export", {}).get("Name", "") for output in self.Outputs.values()}
        new_exports = {getattr(output, "Export", {}).get("Name", "") for output in other.Outputs.values()}
        shared_exports = existing_exports.intersection(new_exports)
        shared_exports.discard("")
        if shared_exports:
            raise StackMergeError(
                "The target stack already has exports named {}".format(", ".join(sorted(shared_exports)))
            )

        # Copy the name and reference for the relevant item types
        for item_type in ["Resources", "Parameters", "Outputs"]:
            existing_items = self[item_type]
            new_items = other[item_type]
            for name, value in new_items.items():
                if name in existing_items:
                    raise StackMergeError(
                        "{} in this stack already has an item with the logical name {}".format(item_type, name)
                    )
                existing_items[name] = value

        return self

    def with_prefixed_names(self, prefix):
        """Create a new stack which has the same objects as the current stack,
        but with the supplied prefix added to the logical and external names
        of all appropriate objects.

        Return the new stack.
        """
        # TODO Add checks for logical name format when we set items, as well as here

        # Filter out ridiculous prefixes before they cause subtle damage
        if not isinstance(prefix, str):
            raise TypeError("Prefix should be a string")
        if not prefix:
            raise ValueError("Prefix should not be empty")
        if not re.fullmatch(r"[A-Z]\w*", prefix):
            raise ValueError(
                "Prefix should have alphanumeric or underscore characters, "
                "beginning with an uppercase character: '{}'".format(prefix)
            )

        # Create a new stack with copies of the static text fields
        new_stack = Stack(
            AWSTemplateFormatVersion=getattr(self, "AWSTemplateFormatVersion", None),
            Transform=getattr(self, "Transform", None),
        )

        # Modify the description to refer to the prefix. This is a bit hacky,
        # but for our use cases we don't expect the description to be
        # retained in final output, so it's good enough for now
        if hasattr(self, "Description"):
            new_stack.Description = prefix + ": " + self.Description
        else:
            new_stack.Description = prefix

        # Insert all references to standard existing objects into new stack, with modified names
        # Copy the name and reference for the relevant item types
        for item_type in ["Resources", "Parameters"]:
            new_stack[item_type] = new_items = {}
            for name, value in self[item_type].items():
                new_items[prefix + name] = value

        # Create copies of all Outputs, with modified Export name where appropriate
        if hasattr(self, "Outputs"):
            new_stack.Outputs = {}
            for name, output in self.Outputs.items():
                # Beware that a deep copy may wreck any intrinsic functions
                # we have attached (a common use case), which is undesirable.
                #
                # OTOH, a shallow copy means that any modifications to the
                # attribute's values (like Export) will affect the original,
                # which is also undesirable. We just need to remember to
                # allow for this
                output = copy.copy(output)
                if getattr(output, "Export", {}).get("Name", ""):
                    output.Export = {"Name": prefix + output.Export["Name"]}

                new_stack.Outputs[prefix + name] = output

        return new_stack

    def tag(self, tags=None, tag_derived_resources=True, **more_tags):
        """Apply tags to all resources in this stack, where they are supported.

        Parameters:
            tags (dict): Key-value pairs representing tags to apply to the
             resource.
            more_tags: Additional key-value pairs representing tags
             to apply to the resource, specified as keyword arguments.
             It is not defined which tag is actually applied in the event
             of duplicates.
            tag_derived_resources (bool): Whether to attempt to apply the
             same tags to derived resources, using Cloud Formation
             (eg. EC2 instances started by an auto-scaling group).

        See Also:
            `AWS documentation on resource tagging
            <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_
        """
        # TODO naming ambiguity - `tag` sounds like it could just mean "tag this single object"

        # Handle multiple ways of passing tags
        if tags is None:
            tags = more_tags
        else:
            tags = dict(tags)
            tags.update(more_tags)

        # Simply apply the tags to each resource
        for resource in self.Resources.values():
            if hasattr(resource, "tag") and callable(resource.tag):
                # Assume this is a Resource-like object
                resource.tag(tags=tags, tag_derived_resources=tag_derived_resources)


class Parameter(AWSObject):
    """Represents a CloudFormation Parameter.

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html
    """

    EXPORT_ORDER = ["Type"]

    AWS_ATTRIBUTES = {
        "AllowedPattern", "AllowedValues", "ConstraintDescription", "Default",
        "Description", "MaxLength", "MaxValue", "MinLength", "MinValue",
        "NoEcho", "Type",
    }

    def __init__(self, AllowedPattern=None, AllowedValues=None,
                 ConstraintDescription=None, Default=None, Description=None,
                 MaxLength=None, MaxValue=None, MinLength=None, MinValue=None,
                 NoEcho=None, Type=None,
                 ):
        AWSObject.__init__(**locals())
        # TODO check Type is set to a valid value?
        # TODO check MinLength/MaxLength are set to a valid integer value?


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
        # currently only valid for a few resource types.
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
        # currently only valid for a few resource types.
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

    @property
    def is_taggable(self):
        """Is this resource taggable."""
        return "Tags" in self.RESOURCE_PROPERTIES

    def tag(self, tags=None, tag_derived_resources=True, **more_tags):
        """Apply tags to this resource, if they are supported.

        Existing tags with the same key will be overwritten.

        Parameters:
            tags (dict): Key-value pairs representing tags to apply to the
             resource.
            more_tags: Additional key-value pairs representing tags
             to apply to the resource, specified as keyword arguments.
             It is not defined which tag is actually applied in the event
             of duplicates.
            tag_derived_resources (bool): Whether to attempt to apply the
             same tags to resources which are derived from this one, using
             Cloud Formation (eg. EC2 instances started by an auto-scaling
             group).

        Returns:
            Whether tags are actually supported by this resource type.

        See Also:
            `AWS documentation on resource tagging
            <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_
        """
        if not self.is_taggable:
            return False

        if tags is None:
            tags = {}

        # Add Tags to our horribly structured list
        for key, value in chain(tags.items(), more_tags.items()):
            # Ensure a tag with key and value exists, overwriting any existing
            # value with that key
            for tag_object in self._get_tag_list():
                if tag_object["Key"] == key:
                    # Overwrite the existing value
                    tag_object["Value"] = value
                    break
            else:
                # Key was not found, so append a new tag object
                self._get_tag_list().append({
                    "Key": key,
                    "Value": value,
                })

        return True

    def get_tag(self, key: str):
        """Get one of the tags currently set on this resource.

        Raises:
             AttributeError: If this resource doesn't support tags

        Returns:
            The tag's value, or else `None` if it is not set
        """
        # TODO tests
        if not self.is_taggable:
            raise AttributeError("Tags are not supported by {}".format(self.Type))

        # Search through existing tags looking for the tag
        for tag_object in self._get_tag_list():
            if tag_object["Key"] == key:
                return tag_object["Value"]

        # Tag was not found
        return None

    def _get_tag_list(self):
        """Get the internal list of all the tag objects on this resource,
        creating it if necessary
        """
        # Try to get the property as quickly as possible
        #
        # Note that Properties might be a `ResourceProperties` object, which
        # doesn't support `setdefault`
        try:
            return self.Properties["Tags"]
        except KeyError:
            pass

        # Create the Tags list, if allowed
        if not self.is_taggable:
            raise AttributeError("Tags are not supported by {}".format(self.Type))

        self.Properties["Tags"] = []
        return self.Properties["Tags"]

    @property
    def name(self):
        """The context-dependent name of this resource, if it is set.
        Usually a resource's name appears as the 'Name' tag.

        Raises:
             AttributeError: If this resource doesn't support name's

        Returns:
            The resource's name, or else `None` if it is not set
        """
        # The default implementation looks for the 'Name' tag
        return self.get_tag("Name")

    @name.setter
    def name(self, value: str):
        # The default implementation looks for the 'Name' tag
        if not self.is_taggable:
            raise AttributeError("Tags are not supported by {}".format(self.Type))

        self.tag(Name=value)


class ResourceProperties(AWSObject):
    def __init__(self, property_names, **properties):
        self.AWS_ATTRIBUTES = property_names
        AWSObject.__init__(self, **properties)


class Output(AWSObject):
    """Represents a CloudFormation Output.

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html
    """

    AWS_ATTRIBUTES = {
        "Description", "Export", "Value"
    }

    def __init__(self, Description=None, Export=None, Value=None):
        AWSObject.__init__(**locals())
        # TODO Export is a single-entry dictionary. Should we flatten it?


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
