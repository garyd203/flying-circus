"""Core classes for composing AWS Cloud Formation Stacks."""

import copy
import re
import textwrap
from itertools import chain
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional

import attr
import yaml
import yaml.resolver
from attr import Attribute
from attr import attrib
from attr import attrs

from . import _about
from .exceptions import StackMergeError
from .yaml import AmazonCFNDumper
from .yaml import CustomYamlObject

# TODO rename "AWS attribute" to "CloudFormation attribute" (or YAML attribute) everywhere ?

#: Arguments to `attrs` decorator for creating a CloudFormation object,
#: as a subclass of CustomYamlObject.
#:
#: Some type checkers (eg PyCharm) implement attrs-based type-checking by
#: detecting the use of the @attrs decorator and then examining the decorated
#: class. These type checkers break when we wrap attrs() in our own extensions,
#: so we instead provide our standard configuration as a set of arguments
ATTRSCONFIG = dict(
    # TODO Consider whether we should have comparison. It's not normally needed, but it wouldnt hurt either
    cmp=False,
    # Only allow known attributes. This requires all parent classes to also
    # have __slots__ defined.
    slots=True,
    # Create a constructor with only keyword parameters
    init=True,
    kw_only=True,
)


def create_object_converter(ObjectClass):
    """Create a converter for attributes using this AWSObject class"""

    def convert_to_object(value):
        """Convert a possible dictionary argument into it's object type"""
        # Convert a dictionary
        if isinstance(value, dict):
            return ObjectClass(**value)

        # Leave all other objects untouched. If they have an invalid type,
        # that will be picked up by a validator later.
        return value

    return convert_to_object


# TODO create some prototypes or helper functions for creating attribs().
# prototype_aws_attribute: int = attrib(default=None)
# _prototype_internal_attribute: int = attrib(default=None, init=False)


@attrs(**ATTRSCONFIG)
class AWSObject(CustomYamlObject):
    """Base class to represent any dictionary-like object from AWS Cloud Formation.

    Cloud Formation attributes are stored as Python attributes on the object,
    using the `attrs` library.

    Any public Python instance attribute is considered to be a Cloud
    Formation attribute. By contrast, a private Python attribute (ie. named
    with a leading underscore) is considered to be an internal attribute and
    is not exported to Cloud Formation.

    If an attribute is set to None it is considered to not be set for cloud
    formation. It is still returned when accessed in code, but won't be
    exported.

    Attributes are exported in the order they are declared.
    """

    # TODO rename to BaseObject and make this an AWS-specific module for context

    # TODO use attrs metadata to mark non-exported attributes

    # TODO beware we have changed the semantics of hasattr with our `attrs` reimplementation. Nowadays the attr is always there, but has a signal value to say it is absent

    # FIXME validate behaviour when we have subclassed objects with attribs defined at multiple levels (all should be included)
    #   - can't set invalid attributes => slots should be set all the way up

    # FIXME convert existing "safe" getattr code to simple attribute lookup

    # Attribute Access
    # ----------------

    def __setattr__(self, key: str, value: Any):
        # attrs only applies converters and validators at initialisation, so
        # we use the existing attribute declaration to also execute them when
        # attributes are set
        # TODO push this upstream to the attrs library, controlled by a flag on @attrs ?

        # Convert value first, if necessary
        try:
            data: Attribute = attr.fields_dict(self.__class__)[key]
        except KeyError:
            # This attribute is not actually an attrs attribute. Let the
            # superclass deal with that...
            pass
        else:
            if data.converter:
                value = data.converter(value)

        # Set the value normally
        super(AWSObject, self).__setattr__(key, value)

        # Run per-attribute and per-class validation
        attr.validate(self)

    def _is_internal_attribute(self, name: str) -> bool:
        """Whether this attribute name corresponds to an internal attribute for this object.

        This is effectively the inverse of _is_cfn_attribute().
        """
        # TODO use attribs metadata
        # Internal attributes all start with an underscore
        return name.startswith("_")

    def _is_cfn_attribute(self, name: str) -> bool:
        """Whether this attribute name corresponds to a known CloudFormation attribute for this object."""
        # TODO use attribs metadata
        # A CloudFormation attribute is an attribute that's not internal.
        return not self._is_internal_attribute(name)

    def is_attribute_set(self, name: str) -> bool:
        """Whether this attribute has a valid value."""
        # Currently we use None as a signal value (and default value in
        # attrib() definitions) to indicate that the attribute is not set.

        # TODO If we ever encounter a need to use None as a real value,
        # have some attrib() metadata that is used to indicate the
        # alternate signal value for not-set (eg. "fc-notset-signal-value")

        return getattr(self, name, None) is not None

    # Container-Like Access For CloudFormation Attributes
    # ---------------------------------------------------
    # TODO implement other container functions: __reversed__, __contains__
    # TODO probably need __reversed__ otherwise an attempt to reverse the object will break like crazy (int item lookups)

    def __getitem__(self, item: str) -> Any:
        """Get CloudFormation attributes in a dictionary-like manner."""
        if self._is_cfn_attribute(item):
            try:
                return getattr(self, item)
            except AttributeError as ex:
                raise KeyError(str(ex)) from ex
        else:
            raise KeyError(
                "'{}' is not a CloudFormation attribute, and cannot be retrieved with the dictionary interface".format(
                    item
                )
            )

    def __setitem__(self, key: str, value: Any):
        """Set CloudFormation attributes in a dictionary-like manner."""
        if self._is_cfn_attribute(key):
            setattr(self, key, value)
        else:
            raise KeyError(
                "'{}' is not a CloudFormation attribute, and cannot be set with the dictionary interface".format(
                    key
                )
            )

    def __iter__(self) -> Iterator[str]:
        # We treat the object like a dictionary for iteration. This means
        # we return a sorted list of CloudFormation attribute names.

        # Sorting by declaration order does not work with subclassing. For
        # now, we achieve this by having the sorted subclass override the
        # behaviour of this function.
        #
        # If there turns out to be a real need for more control, we can
        # re-introduce partial sort-order declaration like we used to
        # have, controlled by a class constant.

        # noinspection PyUnresolvedReferences
        for attrib in self.__attrs_attrs__:
            if self._is_cfn_attribute(attrib.name):
                yield attrib.name

    def __len__(self) -> int:
        # The length of the object is the number of attributes currently set,
        # in order to match the result from __iter__
        return len(list(iter(self)))

    # Export Data
    # -----------

    # TODO change param name to prevent namespace clash
    def export(self, format: str = "yaml") -> str:
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

    def as_yaml_node(self, dumper: yaml.Dumper) -> yaml.Node:
        # Ideally, we would create a tag that contains the object name
        # (eg. "!Bucket") for completeness. Unfortunately, there is no way
        # to then prevent the YAML dumper from printing tags unless it
        # determines that the tag is implicit (ie. the default tag for a
        # mapping node is the tag being used), so we end up just using the
        # default tag.
        # TODO investigate hacking a Dumper subclass like we did for aliasing
        tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

        # Get all cloud formation attributes that are set, in sorted order
        attributes = [(key, self[key]) for key in self if self.is_attribute_set(key)]

        # Create neater YAML by filtering out empty blocks at this level
        attributes = [
            (key, value) for key, value in attributes if is_non_empty_attribute(value)
        ]

        # Create neater YAML by filtering out empty entries in sub-lists
        attributes = [
            (key, remove_empty_values_from_attribute(value))
            for key, value in attributes
        ]

        # Represent this object as a mapping of it's AWS attributes.
        # Note that `represent_mapping` works on a list of 2-tuples, not a map!
        return dumper.represent_mapping(tag, attributes)


def remove_empty_values_from_attribute(data):
    """If this attribute is a list or dictionary, return a copy with empty entries recursively removed."""
    if isinstance(data, list):
        cleaned = map(remove_empty_values_from_attribute, data)
        cleaned = filter(is_non_empty_attribute, cleaned)
        return list(cleaned)
    elif isinstance(data, dict):
        cleaned = {
            key: remove_empty_values_from_attribute(value)
            for key, value in data.items()
        }
        cleaned = {
            key: value
            for key, value in cleaned.items()
            if is_non_empty_attribute(value)
        }
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
            if data.is_attribute_set(key) and is_non_empty_attribute(data[key]):
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


@attrs(**ATTRSCONFIG)
class Stack(AWSObject):
    """Represents a CloudFormation Stack, the top-level template object.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html
    """

    # These are declared in the order recommended in the documentation
    # TODO can probably nail down the value types for these dicts - Resource, Output, etc.
    AWSTemplateFormatVersion: str = attrib(default="2010-09-09")
    Description: Optional[str] = attrib(default=None)
    Metadata: Dict[str, Any] = attrib(factory=dict)
    Parameters: Dict[str, Any] = attrib(factory=dict)
    Mappings: Dict[str, Any] = attrib(factory=dict)
    Conditions: Dict[str, Any] = attrib(factory=dict)
    Transform: Optional[str] = attrib(default=None)
    Resources: Dict[str, Any] = attrib(factory=dict)
    Outputs: Dict[str, Any] = attrib(factory=dict)

    def __attrs_post_init__(self):
        # Set standard Metadata
        self.Metadata["FlyingCircus"] = {"version": _about.__version__}

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
            matches.extend(
                [name for name, data in self.Parameters.items() if data is resource]
            )

        if len(matches) > 1:
            raise ValueError(
                "Object has multiple names in this stack: {}".format(resource)
            )
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
        if (
            self.Transform is not None
            and other.Transform is not None
            and self.Transform != other.Transform
        ):
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
        existing_exports = {
            getattr(output, "Export", {}).get("Name", "")
            for output in self.Outputs.values()
        }
        new_exports = {
            getattr(output, "Export", {}).get("Name", "")
            for output in other.Outputs.values()
        }
        shared_exports = existing_exports.intersection(new_exports)
        shared_exports.discard("")
        if shared_exports:
            raise StackMergeError(
                "The target stack already has exports named {}".format(
                    ", ".join(sorted(shared_exports))
                )
            )

        # Copy the name and reference for the relevant item types
        for item_type in ["Resources", "Parameters", "Outputs"]:
            existing_items = self[item_type]
            new_items = other[item_type]
            for name, value in new_items.items():
                if name in existing_items:
                    raise StackMergeError(
                        "{} in this stack already has an item with the logical name {}".format(
                            item_type, name
                        )
                    )
                existing_items[name] = value

        # Copy across metadata from other sources.
        for name, value in other.Metadata.items():
            if name == "FlyingCircus":
                continue
            if name in self.Metadata:
                raise StackMergeError(
                    "Metadata in this stack already has an item with the logical name {}".format(
                        name
                    )
                )
            self.Metadata[name] = value

        return self

    def with_prefixed_names(self, prefix):
        """Create a new stack which has the same objects as the current stack,
        but with the supplied prefix added to the logical and external names
        of all appropriate objects.

        Return the new stack.
        """
        # TODO Add checks for logical name format when we set items, as well as here
        # FIXME #43 Copy across Metadata. i don't think we should prefix it.

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
            AWSTemplateFormatVersion=self.AWSTemplateFormatVersion,
            Transform=self.Transform,
        )

        # Modify the description to refer to the prefix. This is a bit hacky,
        # but for our use cases we don't expect the description to be
        # retained in final output, so it's good enough for now
        if self.Description:
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
        # TODO force the type for Resources to always be a resource, then can simplify this checking
        for resource in self.Resources.values():
            if hasattr(resource, "tag") and callable(resource.tag):
                # Assume this is a Resource-like object
                resource.tag(tags=tags, tag_derived_resources=tag_derived_resources)


@attrs(**ATTRSCONFIG)
class Parameter(AWSObject):
    """Represents a CloudFormation Parameter.

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html
    """

    Type: Optional[str] = attrib(default=None)
    AllowedPattern: Optional[str] = attrib(default=None)
    AllowedValues: List[Any] = attrib(factory=list)
    ConstraintDescription: Optional[str] = attrib(default=None)
    Default: Optional[Any] = attrib(default=None)
    Description: Optional[str] = attrib(default=None)
    MaxLength: Optional[int] = attrib(default=None)
    MaxValue: Optional[int] = attrib(default=None)  # TODO this could also ]be a float
    MinLength: Optional[int] = attrib(default=None)
    MinValue: Optional[int] = attrib(default=None)  # TODO this could also be float
    NoEcho: Optional[bool] = attrib(default=None)

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
AWS_NotificationARNs = PseudoParameter._create_standard_parameter(
    "AWS::NotificationARNs"
)
AWS_NoValue = PseudoParameter._create_standard_parameter("AWS::NoValue")
AWS_Partition = PseudoParameter._create_standard_parameter("AWS::Partition")
AWS_Region = PseudoParameter._create_standard_parameter("AWS::Region")
AWS_StackId = PseudoParameter._create_standard_parameter("AWS::StackId")
AWS_StackName = PseudoParameter._create_standard_parameter("AWS::StackName")
AWS_URLSuffix = PseudoParameter._create_standard_parameter("AWS::URLSuffix")


@attrs(**ATTRSCONFIG)
class Resource(AWSObject):
    """Represents a CloudFormation Resource in a Stack.

    See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resources-section-structure.html
    and http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html

    Subclasses need to:
     * Use the @attrs decorator
     * Define RESOURCE_TYPE
     * Define a ResourceProperties subclass and the Properties attribute
       using fields specific to that resource type
     * Define attributes for CreationPolicy and UpdatePolicy, if relevant.
    """

    # `CreationPolicy` is defined as a Resource-level attribute in
    # CloudFormation, but is currently only valid for a few resource types.
    # Therefore we leave it to concrete subclasses to defined the attribute
    # when it exists.
    #
    # See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html
    #
    # CreationPolicy: Dict[str, Any] = attrib(factory=dict)

    DeletionPolicy: str = attrib(default=None)
    DependsOn: List[str] = attrib(factory=list)

    #: Note that Resource-level Metadata is not expected to be used by Flying
    #: Circus users, so it can't be set in the constructor. However, they can
    #: still modify it and set it as an attribute.
    Metadata: Dict[str, Any] = attrib(factory=dict, init=False)

    # `Properties` has a resource-type-specific Python type, so we leave it to
    # each concrete subtype to define the attribute appropriately.
    #
    # Properties: ResourceProperties = attrib(factory=ResourceProperties, converter=create_object_converter(ResourceProperties))

    # `Type` is defined as a Python property - see below
    #
    # Type: str = attrib(init=False)

    # `UpdatePolicy` is defined as a Resource-level attribute in
    # CloudFormation, but is currently only valid for a few resource types.
    # Therefore we leave it to concrete subclasses to define the attribute
    # when it exists.
    #
    # See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html
    #
    # UpdatePolicy: Dict[str, Any] = attrib(factory=dict)

    UpdateReplacePolicy: str = attrib(default=None)

    #: Customised sort order for a Resource class. We need to implement
    #: special functionality to sort the attributes on a Resource, because
    #: they are defined in several different (non-standard) places.
    #:
    #: This list includes all the attributes that are defined on a
    #: CloudFormation Resource, even if they may not exist on every concrete
    #: Resource subclass
    _SORT_ORDER = [
        "Type",
        "DependsOn",
        "Metadata",
        "CreationPolicy",
        "UpdatePolicy",
        "UpdateReplacePolicy",
        "DeletionPolicy",
        "Properties",
    ]

    #: The AWS CloudFormation string for this resource's Type
    RESOURCE_TYPE = None

    #: The name of the property that tags are stored in (if any)
    TAG_PROPERTY = "Tags"

    # TODO implement a shortcut function for get_ref(), instead of having to bring in the fn.Ref function?

    def __attrs_post_init__(self):
        # Check that the resource type is specified
        try:
            _ = self.Type
        except AttributeError as ex:
            raise TypeError(ex)

        # Check that the Properties attribute has been defined correctly
        if not (
            hasattr(self, "Properties")
            and isinstance(self.Properties, (dict, ResourceProperties))
        ):
            raise TypeError(
                "Concrete Resource class {} needs to define an attribute "
                "called `Properties`".format(self.__class__.__name__)
            )

    @property
    def Type(self) -> str:
        # The `Type` attribute is a class-specific fixed-value attribute.
        # It is coupled to the underlying concrete subclass via this class
        # constant.
        #
        # We can't achieve this functionality by declaring it as a normal
        # `attrs`-style attribute, so we implement it as a property and
        # override all the base-class functionality that is aware of
        # CloudFormation attributes.
        if not self.RESOURCE_TYPE:
            raise AttributeError(
                "Concrete Resource class {} needs to define the "
                "CloudFormation Type as a class variable called "
                "RESOURCE_TYPE".format(self.__class__.__name__)
            )
        return self.RESOURCE_TYPE

    def __iter__(self) -> Iterator[str]:
        # Get the attributes for this Resource type
        attribs = set(super().__iter__())

        # Type is a class-specific fixed-value attribute, which means we
        # define it specially. We need to explicitly add it to the list
        # of attributes here
        attribs.add("Type")

        # Filter our custom sort order based on which fields actually exist
        # for this Resource class
        for name in self._SORT_ORDER:
            if name in attribs:
                yield name

    @property
    def is_retained(self) -> bool:
        """Whether the underlying physical resource will always be retained,
        regardless of any changes in the stack.

        This reflects whether *both* the underlying policies (`DeletionPolicy`
        and `UpdateReplacePolicy`) are set to "Retain". It is an effective way
        to ensure that irreplacable resources cannot be accidentally removed
        by the CloudFormation.

        Ensure you understand the cost implications of setting this flag.
        """
        return self.DeletionPolicy == "Retain" and self.UpdateReplacePolicy == "Retain"

    @is_retained.setter
    def is_retained(self, value: bool):
        if value:
            self.DeletionPolicy = "Retain"
            self.UpdateReplacePolicy = "Retain"
        else:
            self.DeletionPolicy = None
            self.UpdateReplacePolicy = None

    @property
    def is_taggable(self):
        """Is this resource taggable."""
        return hasattr(self.Properties, self.TAG_PROPERTY)

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
                self._get_tag_list().append({"Key": key, "Value": value})

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
        if not self.is_taggable:
            raise AttributeError("Tags are not supported by {}".format(self.Type))

        # Get or create the Tags property
        #
        # Note that Properties might be a `ResourceProperties` object, which
        # doesn't support `setdefault`
        taglist = self.Properties[self.TAG_PROPERTY]
        if taglist is not None:
            return taglist

        self.Properties[self.TAG_PROPERTY] = []
        return self.Properties[self.TAG_PROPERTY]

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
    """Base class for a Properties object on a Resource."""

    __slots__ = []

    # TODO put default tagging functionality in here, instead of on the resource?

    pass


class LogicalName(CustomYamlObject):
    """Represents the logical name of a resource in an exported stack.

    The logical name of a resource in a CloudFormation template is the
    internal variable name for that resource, which is unique within
    that template.

    Sometimes, when describing infrastructure with Flying Circus, you have a
    reference to the Flying Circus object but CloudFormation requires the
    template's logical name for the resource. This allows you to dereference
    the object, rather than carrying around hard-coded names (yay!)

    The name is exported to CloudFormation as a string, but internally it's an
    object that is dynamically resolved to the correct logical name on export.
    """

    # TODO Find a better module for this to live in
    # TODO consider subclassing from _Function
    # TODO also (primarily) be able to create these Name's from a method on the referenced object

    def __init__(self, resource: Resource):
        """Create a reference to the logical name of a Resource

        :param data: The Python object that is being referenced.
        """
        self._resource = resource

    def as_yaml_node(self, dumper):
        name = dumper.cfn_stack.get_logical_name(
            self._resource, resources_only=True
        )  # Pass error through
        return dumper.represent_str(name)


@attrs(**ATTRSCONFIG)
class Output(AWSObject):
    """Represents a CloudFormation Output.

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html
    """

    # TODO Export is a single-entry dictionary. Should we flatten it or do something nicer?

    Description: str = attrib(default=None)
    Export: Dict[str, Any] = attrib(factory=dict)
    Value: Any = attrib(default=None)


# TODO new `reflow` function that cleans a long (multi-) line string from IDE padding, and marks it as as suitable for PyYAML flow style


def dedent(st):
    """Remove unwanted whitespace from a multi-line string intended for output.

    This is perfect for text embedded inside indented Python code.
    """
    # TODO needs test cases
    # TODO different python module

    lines = st.split("\n")

    # Remove a leading line that contains only a newline character
    if lines and not lines[0]:
        lines = lines[1:]

    # Remove python-style leading indentation on each line
    cleaned_lines = textwrap.dedent("\n".join(lines))

    return cleaned_lines
