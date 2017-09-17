"""Core classes for composing AWS Cloud Formation Stacks."""

import yaml


class BaseAWSObject(yaml.YAMLObject):
# class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""

    yaml_tag = "!sometag"

    AWS_YAML_FIELDS = []
    RESOURCE_ATTRIBUTES = []

    def __init__(self, *args, **kwargs):
        # args are interpreted according to their type
        # kwargs are added as fields using their type and Name
        # yaml.YAMLObject.__init__(self)
        pass

    # TODO Name
    # TODO add?
    # TODO canonicalise
    # TODO dict-like interface to set/get fields
    # TODO getattr override to emulate the !GetAtt function for special attributes

    def export(self, format="yaml"):
        # import yaml
        return yaml.dump(self, Dumper=self.yaml_dumper, line_break=True, default_flow_style=False)

    @classmethod
    def to_yaml(cls, dumper, data):
        # Convert this class to a PyYAML node.\
        #
        # Should not be confused with a public method to export an object as a YAML string.
        return dumper.represent_mapping("!FIXME", {'c': 'd'})

    def __str__(self):
        # TODO support ExportContext state on thread local
        # TODO if no current state, then instantiate a default one (YAML, stdout)
        return self.export()


def _base_representer(dumper, data):
    return dumper.represent_mapping("!TODO", {'a': 'b'})
# yaml.add_multi_representer(BaseAWSObject, _base_representer)


class Function(object):
    """Base class to represent an AWS Cloud Formation function."""
    pass


class Resource(BaseAWSObject):
    """Base class to represent a single resource in AWS Cloud Formation."""

    pass


class Output(BaseAWSObject):
    """Base class to represent a single output in an AWS Cloud Formation stack."""

    def __init__(self, Name=None, Value=None, Description=None):
        BaseAWSObject.__init__(self, Name == Name, Value=Value, Description=Description)


class Stack(BaseAWSObject):
    """Base class to represent a single stack in AWS Cloud Formation."""

    def __init__(self, *args, **kwargs):
        BaseAWSObject.__init__(self, *args, **kwargs)
        self.Resources = {}
        self.Outputs = {}
