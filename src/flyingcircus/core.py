"""Core classes for composing AWS Cloud Formation Stacks."""

import yaml
import yaml.resolver

class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""

    AWS_CFN_FIELDS = []

    def __init__(self, *args, **kwargs):
        # args are interpreted according to their type
        # kwargs are added as fields using their type and Name

        #: Map of fields that are exported
        self._data = {}

        # Add fields from constructor
        for key, value in kwargs.items():
            self.add(key, value)

    # TODO Name
    # TODO add?
    # TODO canonicalise
    # TODO dict-like interface to set/get fields
    # TODO getattr override to emulate the !GetAtt function for special attributes
    # TODO __empty__ or false or whatever it is - are my fields all empty. will work recursively to trim trees

    def export(self, format="yaml"):
        return yaml.dump(self, line_break=True, default_flow_style=False, explicit_start=True)

    def as_yaml_node(self, dumper):
        """Convert this instance to a PyYAML node."""
        import yaml.serializer
        # see yaml.serializer line 102. If you use the "default" tag, then it will be conisdered implicit and the tag name isnt printed out (which is what we desire). Just need to figure out how to best trigger this behaviour.

        data = {k: v for k, v in self._data.items() if v}
        # TODO handle ordering (is it builtin?)

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


yaml.add_multi_representer(BaseAWSObject, lambda dumper, data: data.as_yaml_node(dumper))


class Function(object):
    """Base class to represent an AWS Cloud Formation function."""
    pass


class Resource(BaseAWSObject):
    """Base class to represent a single resource in AWS Cloud Formation."""

    AWS_RESOURCE_TYPE = None

    def __init__(self, *args, **kwargs):
        BaseAWSObject.__init__(self, *args, **kwargs)
        assert self.AWS_RESOURCE_TYPE is not None
        self._data['Type'] = self.AWS_RESOURCE_TYPE


class Output(BaseAWSObject):
    """Base class to represent a single output in an AWS Cloud Formation stack."""

    def __init__(self, Name=None, Value=None, Description=None):
        BaseAWSObject.__init__(self, Name == Name, Value=Value, Description=Description)


class Stack(BaseAWSObject):
    """Base class to represent a single stack in AWS Cloud Formation."""

    def __init__(self, *args, **kwargs):
        BaseAWSObject.__init__(self, *args, **kwargs)
        self._data['Resources'] = {}
        self._data['Outputs'] = {}

    @property
    def Outputs(self):
        return self._data['Outputs']

    @property
    def Resources(self):
        return self._data['Resources']
