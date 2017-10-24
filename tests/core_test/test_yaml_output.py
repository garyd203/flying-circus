"""Tests for YAML output from the AWSObject base class."""

import pytest

from flyingcircus.core import AWSObject
from flyingcircus.core import reflow_trailing


class TestYAMLOutput:
    """Verify YAML output."""
    '''fixme

    # data types/formatting
    empty object. prints properly, but can optionally be left out?
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
    # TODO block flow style
    # TODO list values are indented

    def test_yaml_document_explicitly_indicates_document_start(self):
        data = AWSObject()

        output = data.export("yaml")

        assert output.startswith("---")

    def test_yaml_tags_are_not_printed(self):
        class TestObject(AWSObject):
            AWS_ATTRIBUTES = {"string_value", "number_value", "list_value", "dict_value"}

        data = TestObject(string_value="some string", number_value=42, list_value=[1, 2, 'abc'], dict_value={'a': 'b'})

        output = data.export("yaml")

        assert output == reflow_trailing("""
            ---
            dict_value:
              a: b
            list_value:
            - 1
            - 2
            - abc
            number_value: 42
            string_value: some string
            """)

    def test_yaml_aliases_are_not_used(self):
        class TestObject(AWSObject):
            AWS_ATTRIBUTES = {"foo", "bar"}

        shared_data = {'a': 'b'}
        data = TestObject(foo=shared_data, bar=shared_data)

        output = data.export("yaml")

        assert "&" not in output, "We don't want anchors, which are marked with an ampersand"
        assert "*" not in output, "We don't want aliases to anchors, which are indicated by an asterisk"

    @pytest.mark.skip
    def test_empty_objects_are_not_exported(self):
        """If an object has no non-empty attributes, then it is not exported"""
        # TODO further variations with attributes that are set to None, or attributes that are themselves empty
        data = AWSObject()

        output = data.export("yaml")

        assert output == reflow_trailing("""
            ---
            """)

    def test_single_entry_object_is_exported_in_block_style(self):
        class SingleEntryObject(AWSObject):
            AWS_ATTRIBUTES = {"foo"}

        data = SingleEntryObject(foo=1)

        output = data.export("yaml")

        assert output == reflow_trailing("""
            ---
            foo: 1
            """)

    def test_multi_entry_object_is_exported_in_block_style(self):
        class MultiEntryObject(AWSObject):
            AWS_ATTRIBUTES = {"bar", "foo"}

        data = MultiEntryObject(bar=1, foo=2)

        output = data.export("yaml")

        assert output == reflow_trailing("""
            ---
            bar: 1
            foo: 2
            """)
