"""Tests for YAML output from the AWSObject base class."""

import pytest

from flyingcircus.core import AWSObject
from flyingcircus.core import dedent
from .common import DualAttributeObject
from .common import SingleAttributeObject
from .common import ZeroAttributeObject


# TODO space between sections/attributes at the top-level Stack template

class TestYamlAttributeExport:
    """Verify all relevant attributes are exported to YAML"""

    def test_aws_attributes_are_only_exported_when_set(self):
        data = DualAttributeObject(one=42)
        data._internal_value = 7
        data.set_unknown_aws_attribute("special", 8)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: 42
            special: 8
            """)

    def test_empty_export_when_no_aws_attributes_configured_and_internal_attributes_set(self):
        data = ZeroAttributeObject()
        data._internal_value = 7

        output = data.export("yaml")

        assert output == dedent("""
            --- {}
            """)

    def test_empty_export_when_no_aws_attributes_set_and_internal_attributes_set(self):
        data = DualAttributeObject()
        data._internal_value = 7

        output = data.export("yaml")

        assert output == dedent("""
            --- {}
            """)

    def test_unknown_attributes_are_exported_when_no_known_attributes(self):
        data = ZeroAttributeObject()
        data.set_unknown_aws_attribute("special", 8)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            special: 8
            """)


class TestYamlBasicFormatting:
    """Verify basic formatting of YAML output"""

    def test_yaml_document_explicitly_indicates_document_start(self):
        data = ZeroAttributeObject()

        output = data.export("yaml")

        assert output.startswith("---")

    def test_yaml_tags_are_not_printed(self):
        class TestObject(AWSObject):
            AWS_ATTRIBUTES = {"string_value", "number_value", "list_value", "dict_value"}

        data = TestObject(string_value="some string", number_value=42, list_value=[1, 2, 'abc'], dict_value={'a': 'b'})

        output = data.export("yaml")

        assert output == dedent("""
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
        shared_data = {'a': 'b'}
        data = DualAttributeObject(one=shared_data, two=shared_data)

        output = data.export("yaml")

        assert "&" not in output, "We don't want anchors, which are marked with an ampersand"
        assert "*" not in output, "We don't want aliases to anchors, which are indicated by an asterisk"

    def test_single_entry_object_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=1)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: 1
            """)

    def test_multi_entry_object_is_exported_in_block_style(self):
        data = DualAttributeObject(one=1, two=2)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: 1
            two: 2
            """)

    def test_none_values_are_exported_as_null(self):
        data = SingleAttributeObject()
        data.one = None

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: null
            """)

    def test_false_values_are_exported(self):
        data = SingleAttributeObject(one=False)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: false
            """)

    def test_complex_attributes_that_dont_extend_the_base_class_should_raise_an_error(self):
        class CustomObjectThatIsntYamlisable(object):
            pass

        attrib = CustomObjectThatIsntYamlisable()
        attrib.foo = 42
        data = SingleAttributeObject(one=attrib)

        with pytest.raises(TypeError) as excinfo:
            _ = data.export("yaml")

        assert "CustomObjectThatIsntYamlisable" in str(excinfo.value)
        assert "does not extend" in str(excinfo.value)

    # Object/Dictionary Export Order
    # ------------------------------

    def test_map_entries_are_sorted(self):
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b"}
            EXPORT_ORDER = ["b", "a"]

        data = OrderedObject(a=1, b=2)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            b: 2
            a: 1
            """)

    # List Export Style
    # -----------------

    def test_list_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=[2, 3, 4])

        output = data.export("yaml")

        assert output == dedent("""
                ---
                one:
                - 2
                - 3
                - 4
                """)

    def test_single_entry_list_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=[2])

        output = data.export("yaml")

        assert output == dedent("""
                ---
                one:
                - 2
                """)

    def test_nested_lists_are_readable(self):
        data = SingleAttributeObject(one=[[2, 3, 4], [5], [6, 7], 8])

        output = data.export("yaml")

        # TODO This is not actually very readable - see issue #41
        assert output == dedent("""
                ---
                one:
                - - 2
                  - 3
                  - 4
                - - 5
                - - 6
                  - 7
                - 8
                """)


class TestYamlStringFormatting:
    """Verify formatting of strings in YAML output"""

    def test_string_quotes_are_not_used_when_unnecessary(self):
        data = SingleAttributeObject(one="Hello world. Here is a namespace AWS::service::Resource")

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: Hello world. Here is a namespace AWS::service::Resource
            """)

    def test_empty_string_has_simple_representation(self):
        data = SingleAttributeObject(one="")

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: ''
            """)

    def test_leading_and_trailing_whitespace_is_not_stripped(self):
        data = SingleAttributeObject(one="    hello world   ")

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: '    hello world   '
            """)

    def test_long_strings_dont_get_broken(self):
        long_text = "This is a really long string and it just goes on and on " \
                    "and on. I hope there's a good reason for it. Of " \
                    "course, this means that my IDE is complaining about " \
                    "the length of the line too, but it got over that."
        data = SingleAttributeObject(one=long_text)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: |-
              {}
            """.format(long_text))

    def test_multiline_strings_retain_formatting(self):
        data = SingleAttributeObject(one="hello\nworld\n\n  We should retain indenting too")

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: |-
              hello
              world
              
                We should retain indenting too
            """)


class TestYamlEmptyAttributeFormatting:
    """Verify formatting of empty attributes in YAML output"""

    # TODO test scenarios.
    #   empty dict
    #   empty object
    #   empty list
    #   can force output of an empty dict by supplying signal value
    #   can force output of an empty list by supplying signal value
    #   X empty string still gets exported
    #   X None still gets exported
    #   X False still gets exported

    @pytest.mark.skip("#55: We dont currently support filtering out empty attributes")
    def test_empty_attributes_are_not_exported(self):
        empty_attribute = ZeroAttributeObject()
        data = DualAttributeObject(one=1, two=empty_attribute)

        output = data.export("yaml")

        assert output == dedent("""
            ---
            one: 1
            """)

    def test_empty_top_level_object_is_exported_as_empty_dict(self):
        data = ZeroAttributeObject()

        output = data.export("yaml")

        assert output == dedent("""
            --- {}
            """)

    def test_empty_list_is_exported_in_flow_style(self):
        data = SingleAttributeObject(one=[])

        output = data.export("yaml")

        assert output == dedent("""
                ---
                one: []
                """)
