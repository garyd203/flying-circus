"""Tests for YAML output from the AWSObject base class."""

from flyingcircus.core import AWSObject
from flyingcircus.core import reflow


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

    # TODO alphabetical ordering or explicit-then-alphabetical ordering
    # TODO string wrapping and block flow style

    def test_yaml_document_explicitly_indicates_document_start(self):
        data = AWSObject()

        output = data.export("yaml")

        assert output.startswith("---")

    def test_yaml_tags_are_not_printed(self):
        class TestObject(AWSObject):
            AWS_ATTRIBUTES = {"string_value", "number_value", "list_value", "dict_value"}

            def __init__(self):
                AWSObject.__init__(self, string_value="some string", number_value=42, list_value=[1, 2, 'abc'],
                                   dict_value={'a': 'b'})

        data = TestObject()

        output = data.export("yaml")

        assert output == reflow("""
            ---
            dict_value: {a: b}
            list_value: [1, 2, abc]
            number_value: 42
            string_value: some string
            """) + "\n"

    def test_yaml_aliases_are_not_used(self):
        class TestObject(AWSObject):
            AWS_ATTRIBUTES = {"foo", "bar"}

            def __init__(self, foo=None, bar=None):
                AWSObject.__init__(self, foo=foo, bar=bar)

        shared_data = {'a': 'b'}
        data = TestObject(foo=shared_data, bar=shared_data)

        output = data.export("yaml")

        assert "&" not in output, "We don't want anchors, which are marked with an ampersand"
        assert "*" not in output, "We don't want aliases to anchors, which are indicated by an asterisk"
