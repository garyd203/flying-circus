"""Tests for YAML output from the AWSObject base class."""

from flyingcircus.core import AWSObject


class TestYAMLOutput:
    """Verify YAML output."""
    '''fixme

    # data types/formatting
    empty object
    text value
    int value
    list with no items
    normal list
    list with nested list
    list with nested dictionary
    dictionary with no items
    dictionary with 1 item
    dictionary with nested dictionary
    dictionary with nested list

    # configuration
    no python attributes set
    no known aws attributes, only internal attributes set
    has known aws attributes, only internal attributes set
    has known aws attributes, some aws attributes set
    no known aws attributes, some unknown attributes set
    has known aws attributes, some known and unknown and internal attributes set


    '''
    pass


class TestYAMLBasicFormatting:
    """Verify basic formatting of YAML output"""

    '''fixme
    no tag
    alphabetical ordering or explicit-then-alphabetical ordering
    aliases not used
    string wrapping and block flow style
    '''

    def test_yaml_document_explicitly_indicates_document_start(self):
        class YamlOutputTest(AWSObject):
            pass

        data = YamlOutputTest()

        output = data.export("yaml")

        print(output)  # FIXME remove
        assert output.startswith("---")
