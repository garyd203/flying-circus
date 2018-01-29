"""Tests for the emptiness helper functions."""

from flyingcircus.core import is_non_empty_attribute, remove_empty_values_from_attribute
from .common import DualAttributeObject
from .common import ZeroAttributeObject


class TestEmptyAttribute:
    """Tests for is_non_empty_attribute()"""

    def test_none_is_not_empty(self):
        assert is_non_empty_attribute(None) is True

    def test_empty_string_is_not_empty(self):
        assert is_non_empty_attribute("") is True

    def test_non_empty_string_is_not_empty(self):
        assert is_non_empty_attribute("hello") is True

    def test_empty_list_is_empty(self):
        assert is_non_empty_attribute([]) is False

    def test_non_empty_list_is_not_empty(self):
        assert is_non_empty_attribute([1]) is True

    def test_non_empty_list_with_only_empty_values_is_empty(self):
        assert is_non_empty_attribute([[], [], [[]]]) is False

    def test_non_empty_list_with_some_empty_values_is_not_empty(self):
        assert is_non_empty_attribute([[], [], 1, [[]]]) is True

    def test_empty_dictionary_is_empty(self):
        assert is_non_empty_attribute({}) is False

    def test_non_empty_dictionary_is_not_empty(self):
        assert is_non_empty_attribute({'a': 1}) is True

    def test_non_empty_dictionary_with_only_empty_values_is_empty(self):
        assert is_non_empty_attribute({'a': {}, 'b': [[]]}) is False

    def test_non_empty_dictionary_with_some_empty_values_is_not_empty(self):
        assert is_non_empty_attribute({'a': {}, 'b': 1}) is True

    def test_awsobject_with_no_attributes_is_empty(self):
        assert is_non_empty_attribute(ZeroAttributeObject()) is False

    def test_awsobject_with_some_attributes_is_empty(self):
        assert is_non_empty_attribute(DualAttributeObject(one=42)) is True

    def test_awsobject_with_no_attributes_set_is_empty(self):
        assert is_non_empty_attribute(DualAttributeObject()) is False

    def test_awsobject_with_only_empty_attributes_is_empty(self):
        assert is_non_empty_attribute(DualAttributeObject(one=[], two={})) is False


class TestRemoveEmptyAttributes:
    """Tests for remove_empty_values_from_attribute()"""

    def test_none_is_not_modified(self):
        data = None
        cleaned = remove_empty_values_from_attribute(data)
        assert cleaned is data

    def test_strings_are_not_modified(self):
        data = "yolo"
        cleaned = remove_empty_values_from_attribute(data)
        assert cleaned is data

    def test_awsobjects_are_not_modified(self):
        data = DualAttributeObject(one='hello', two=[1, []])
        cleaned = remove_empty_values_from_attribute(data)
        assert cleaned is data

    def test_empty_list_entries_are_removed(self):
        data = [1, []]
        cleaned = remove_empty_values_from_attribute(data)
        assert cleaned == [1]

    def test_empty_dictionary_values_are_removed(self):
        data = {'a': 1, 'b': []}
        cleaned = remove_empty_values_from_attribute(data)
        assert cleaned == {'a': 1}
