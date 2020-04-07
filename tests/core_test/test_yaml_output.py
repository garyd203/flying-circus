"""Tests for YAML output from the AWSObject base class."""

import pytest
from attr import attrib
from attr import attrs

from flyingcircus.core import AWSObject, ATTRSCONFIG
from flyingcircus.core import EMPTY_DICT
from flyingcircus.core import EMPTY_LIST
from flyingcircus.core import dedent
from .common import DualAttributeObject
from .common import MixedAttributeObject
from .common import SingleAttributeObject
from .common import ZeroAttributeObject


# TODO space between sections/attributes at the top-level Stack template


class TestYamlAttributeExport:
    """Verify all relevant attributes are exported to YAML"""

    def test_aws_attributes_are_exported_when_set(self):
        data = SingleAttributeObject(one=42)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_aws_attributes_are_not_exported_when_uninitialised(self):
        data = DualAttributeObject(one=42)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_aws_attributes_are_not_exported_when_set_to_none(self):
        data = DualAttributeObject(one=42, two=15)
        data.two = None

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_internal_attributes_are_not_exported(self):
        data = MixedAttributeObject(one=42, a=6)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_empty_export_when_no_aws_attributes_configured(self):
        data = ZeroAttributeObject()

        output = data.export("yaml")

        assert output == dedent(
            """
            --- {}
            """
        )

    def test_empty_export_when_no_aws_attributes_set(self):
        data = MixedAttributeObject(a=6)

        output = data.export("yaml")

        assert output == dedent(
            """
            --- {}
            """
        )


class TestYamlBasicFormatting:
    """Verify basic formatting of YAML output"""

    def test_yaml_document_explicitly_indicates_document_start(self):
        data = ZeroAttributeObject()

        output = data.export("yaml")

        assert output.startswith("---")

    def test_yaml_tags_are_not_printed(self):
        @attrs(**ATTRSCONFIG)
        class TestObject(AWSObject):
            dict_value = attrib()
            list_value = attrib()
            number_value = attrib()
            string_value = attrib()

        data = TestObject(
            string_value="some string",
            number_value=42,
            list_value=[1, 2, "abc"],
            dict_value={"a": "b"},
        )

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            dict_value:
              a: b
            list_value:
            - 1
            - 2
            - abc
            number_value: 42
            string_value: some string
            """
        )

    def test_yaml_aliases_are_not_used(self):
        shared_data = {"a": "b"}
        data = DualAttributeObject(one=shared_data, two=shared_data)

        output = data.export("yaml")

        assert (
            "&" not in output
        ), "We don't want anchors, which are marked with an ampersand"
        assert (
            "*" not in output
        ), "We don't want aliases to anchors, which are indicated by an asterisk"

    def test_single_entry_object_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=1)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 1
            """
        )

    def test_multi_entry_object_is_exported_in_block_style(self):
        data = DualAttributeObject(one=1, two=2)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 1
            two: 2
            """
        )

    @pytest.mark.skip(
        "#107: Need to think about why we need null's in output. Currently we treat them as 'no value'"
    )
    def test_none_values_are_exported_as_null(self):
        data = SingleAttributeObject()
        data.one = None

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: null
            """
        )

    def test_false_values_are_exported(self):
        data = SingleAttributeObject(one=False)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: false
            """
        )

    def test_complex_attributes_that_dont_extend_the_base_class_should_raise_an_error(
        self
    ):
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

    def test_object_entries_are_sorted_in_order_of_declaration(self):
        @attrs(**ATTRSCONFIG)
        class OrderedObject(AWSObject):
            b = attrib()
            a = attrib()

        data = OrderedObject(a=1, b=2)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            b: 2
            a: 1
            """
        )

    def test_dictionary_entries_are_sorted_alphabetically(self):
        data = SingleAttributeObject(
            one=dict(
                [
                    (x, "foo")
                    for x in [
                        "a",
                        "b",
                        "c",
                        "A",
                        "Bad",
                        "bad",
                        "badness",
                        "baddie",
                        "42",
                        "4",
                        "1",
                        "z",
                        "ZoologicalSpecimen",
                    ]
                ]
            )
        )

        output = data.export("yaml")

        # TODO I don't really like this sort order - capitalized items before lowercase items is a bit deceptive
        assert output == dedent(
            """
            ---
            one:
              '1': foo
              '4': foo
              '42': foo
              A: foo
              Bad: foo
              ZoologicalSpecimen: foo
              a: foo
              b: foo
              bad: foo
              baddie: foo
              badness: foo
              c: foo
              z: foo
            """
        )

    # List Export Style
    # -----------------

    def test_list_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=[2, 3, 4])

        output = data.export("yaml")

        assert output == dedent(
            """
                ---
                one:
                - 2
                - 3
                - 4
                """
        )

    def test_single_entry_list_is_exported_in_block_style(self):
        data = SingleAttributeObject(one=[2])

        output = data.export("yaml")

        assert output == dedent(
            """
                ---
                one:
                - 2
                """
        )

    def test_empty_list_is_exported_in_flow_style(self):
        data = SingleAttributeObject(one=EMPTY_LIST)

        output = data.export("yaml")

        assert output == dedent(
            """
                ---
                one: []
                """
        )

    def test_nested_lists_are_readable(self):
        data = SingleAttributeObject(one=[[2, 3, 4], [5], [6, 7], 8])

        output = data.export("yaml")

        # TODO #41: This is not actually very readable
        assert output == dedent(
            """
                ---
                one:
                - - 2
                  - 3
                  - 4
                - - 5
                - - 6
                  - 7
                - 8
                """
        )


class TestYamlStringFormatting:
    """Verify formatting of strings in YAML output"""

    def test_string_quotes_are_not_used_when_unnecessary(self):
        data = SingleAttributeObject(
            one="Hello world. Here is a namespace AWS::service::Resource"
        )

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: Hello world. Here is a namespace AWS::service::Resource
            """
        )

    def test_empty_string_has_simple_representation(self):
        data = SingleAttributeObject(one="")

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: ''
            """
        )

    def test_leading_and_trailing_whitespace_is_not_stripped(self):
        data = SingleAttributeObject(one="    hello world   ")

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: '    hello world   '
            """
        )

    def test_long_strings_dont_get_broken(self):
        long_text = (
            "This is a really long string and it just goes on and on "
            "and on. I hope there's a good reason for it. Of "
            "course, this means that my IDE is complaining about "
            "the length of the line too, but it got over that."
        )
        data = SingleAttributeObject(one=long_text)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: |-
              {}
            """.format(
                long_text
            )
        )

    def test_multiline_strings_retain_formatting(self):
        data = SingleAttributeObject(
            one="hello\nworld\n\n  We should retain indenting too"
        )

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: |-
              hello
              world
              
                We should retain indenting too
            """
        )


class TestYamlEmptyAttributeFormatting:
    """Verify formatting of empty attributes in YAML output"""

    def test_empty_top_level_object_is_exported_as_empty_dict(self):
        data = ZeroAttributeObject()

        output = data.export("yaml")

        assert output == dedent(
            """
            --- {}
            """
        )

    def test_attribute_set_to_emptyish_list_is_not_exported(self):
        data = DualAttributeObject(one=42, two=[{}])

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_attribute_set_to_list_has_empty_entries_removed_in_export(self):
        data = DualAttributeObject(one=42, two=["a", {}])

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            two:
            - a
            """
        )

    def test_attribute_set_to_emptyish_dictionary_is_not_exported(self):
        data = DualAttributeObject(one=42, two={"a": []})

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_attribute_set_to_dictionary_has_empty_values_removed_in_export(self):
        data = DualAttributeObject(one=42, two={"a": [], "b": 13})

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            two:
              b: 13
            """
        )

    def test_attribute_set_to_emptyish_object_is_not_exported(self):
        data = DualAttributeObject(one=42, two=SingleAttributeObject(one=[]))

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            """
        )

    def test_attribute_can_export_an_empty_list_by_using_signal_value(self):
        data = DualAttributeObject(one=42, two=EMPTY_LIST)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            two: []
            """
        )

    def test_attribute_can_export_an_empty_dictionary_by_using_signal_value(self):
        data = DualAttributeObject(one=42, two=EMPTY_DICT)

        output = data.export("yaml")

        assert output == dedent(
            """
            ---
            one: 42
            two: {}
            """
        )

    test_attribute_set_to_empty_string_is_exported_normally = (
        TestYamlStringFormatting.test_empty_string_has_simple_representation
    )
    test_attribute_set_to_none_is_exported_normally = (
        TestYamlBasicFormatting.test_none_values_are_exported_as_null
    )
    test_attribute_set_to_false_is_exported_normally = (
        TestYamlBasicFormatting.test_false_values_are_exported
    )
