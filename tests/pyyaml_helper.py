"""Helper functions for testing with PyYAML objects."""


def get_mapping_node_key(node, i=0):
    """Get a dictionary key from a PyYAML node.

    :param int i: Get the key for the i'th entry in the mapping. Entries
        are sorted deterministically by the node export (usually
        alphabetically)
    :param node: A PyYAML node representing a mapping.
    """
    return node.value[i][0].value
