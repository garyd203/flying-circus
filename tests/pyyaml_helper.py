"""Helper functions for testing with PyYAML objects."""

from flyingcircus.yaml import AmazonCFNDumper


def get_mapping_node_key(node, i=0):
    """Get a dictionary key from a PyYAML node.

    :param int i: Get the key for the i'th entry in the mapping. Entries
        are sorted deterministically by the node export (usually
        alphabetically)
    :param node: A PyYAML node representing a mapping.
    """
    return node.value[i][0].value


def create_refsafe_dumper(stack):
    # TODO make this a pytest fixture `dumper`
    dumper = AmazonCFNDumper(None)
    dumper.cfn_stack = stack
    return dumper
