"""Core classes for composing AWS Cloud Formation Stacks."""

import yaml


class BaseAWSObject(object):
    """Base class to represent an object in AWS Cloud Formation."""

    AWS_YAML_FIELDS = []
    RESOURCE_ATTRIBUTES = []

    def __init__(self, *args, **kwargs):
        # args are interpreted according to their type
        # kwargs are added as fields using their type and Name
        pass

    # TODO Name
    # TODO add?
    # TODO canonicalise
    # TODO dict-like interface to set/get fields
    # TODO getattr override to emulate the !GetAtt function for special attributes

    def export(self, format="yaml"):
        # import yaml
        return yaml.dump(self, line_break=True, default_flow_style=False)

    def as_yaml_node(self, dumper, data):
        """Convert this class to a PyYAML node."""
        return dumper.represent_mapping("!" + self.__class__.__name__, {'c': 'd'})

    def __str__(self):
        # TODO support ExportContext state on thread local
        # TODO if no current state, then instantiate a default one (YAML, stdout)
        return self.export()


def representation_redirecter(dumper, data):
    return data.as_yaml_node(dumper, data)


yaml.add_multi_representer(BaseAWSObject, representation_redirecter)


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
