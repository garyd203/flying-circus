"""Tests for the AWSObject base class.

This functionality forms the core of Flying Circus.
"""

import inspect

import hypothesis.strategies as st
import pytest
from hypothesis import given

from flyingcircus.core import AWSObject
from .common import DualAttributeObject
from .common import SingleAttributeObject
from .common import ZeroAttributeObject
from .common import aws_attribute_strategy


class TestInitMethod:
    """Verify behaviour of the base AWSObject's constructor"""

    def test_init_should_not_accept_positional_parameters(self):
        # noinspection PyPep8Naming
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                # NB: Make sure we exercise the __init__ in the base class!
                # noinspection PyArgumentList
                AWSObject.__init__(self, Foo)

        with pytest.raises(TypeError) as excinfo:
            _ = InitTestObject()

        assert "positional" in str(excinfo.value)

    def test_init_should_only_accept_kwargs(self):
        sig = inspect.signature(AWSObject.__init__)
        for param in sig.parameters.values():
            if param.name == 'self':
                continue
            assert param.kind == param.VAR_KEYWORD

    @given(aws_attribute_strategy(), aws_attribute_strategy(), aws_attribute_strategy())
    def test_init_should_map_keyword_args_to_attributes(self, foo_value, default_value, bar_value):
        # noinspection PyPep8Naming
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo", "ValueWithDefault", "Bar"}

            def __init__(self, Foo=None, ValueWithDefault=default_value, Bar=None):
                AWSObject.__init__(self, Foo=Foo, ValueWithDefault=ValueWithDefault, Bar=Bar)

        data = InitTestObject(foo_value, Bar=bar_value)

        assert data.Foo is foo_value
        assert data.ValueWithDefault is default_value
        assert data.Bar is bar_value

    @given(aws_attribute_strategy())
    def test_init_should_only_accept_keyword_args_that_are_known_aws_attributes(self, value):
        # noinspection PyPep8Naming
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                # NB: Make sure we exercise the __init__ in the base class!
                AWSObject.__init__(self, Foo=Foo, SomeUnknownAttribute=value)

        with pytest.raises(TypeError) as excinfo:
            _ = InitTestObject()

        assert "SomeUnknownAttribute" in str(excinfo.value)

    def test_init_should_ignore_keyword_parameters_that_are_none(self):
        # noinspection PyPep8Naming
        class InitTestObject(AWSObject):
            AWS_ATTRIBUTES = {"Foo"}

            def __init__(self, Foo=None):
                AWSObject.__init__(self, Foo=Foo)

        data = InitTestObject()

        assert not hasattr(data, "Foo")


class TestExport:
    """Verify behaviour of the export method"""

    VALID_EXPORT_FORMATS = {"yaml"}

    @pytest.mark.parametrize('format', VALID_EXPORT_FORMATS)
    def test_valid_export_methods_produce_a_result(self, format):
        data = ZeroAttributeObject()

        output = data.export(format)

        assert output is not None

    @given(st.text().filter(lambda x: x not in TestExport.VALID_EXPORT_FORMATS))
    def test_invalid_export_methods_cause_an_error(self, format):
        data = ZeroAttributeObject()

        with pytest.raises(ValueError) as excinfo:
            data.export(format)

        assert format in str(excinfo.value)


class TestAttributeAccess:
    """Verify behaviour of attributes on a Flying Circus AWS object"""

    # noinspection PyPep8Naming
    class SimpleObject(AWSObject):
        """Simple AWS object for testing attribute access"""
        AWS_ATTRIBUTES = {"Foo", "bar"}

        def __init__(self, Foo=None, bar=None):
            AWSObject.__init__(self, Foo=Foo, bar=bar)

    # Set and Read
    # ------------

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_valid_aws_attributes_can_be_set_and_read(self, foo_value, bar_value):
        data = self.SimpleObject()

        data.Foo = foo_value
        data.bar = bar_value

        assert hasattr(data, "Foo")
        assert data.Foo is foo_value
        assert hasattr(data, "bar")
        assert data.bar is bar_value

    @given(st.text())
    def test_internal_attributes_can_be_set_and_read(self, value):
        data = self.SimpleObject()

        data._internal_value = value

        assert hasattr(data, "_internal_value")
        assert data._internal_value is value

    def test_unknown_attributes_cannot_be_set_directly(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            data.WeirdValue = "hello"
        assert "WeirdValue" in str(excinfo.value)
        assert not hasattr(data, "WeirdValue")

    @given(aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_explicitly_set_and_read_normally(self, value):
        data = self.SimpleObject()

        data.set_unknown_aws_attribute("WeirdValue", value)

        assert hasattr(data, "WeirdValue")
        assert data.WeirdValue is value

    def test_valid_aws_attributes_cannot_be_explicitly_set(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("bar", "hello")

        assert "bar" in str(excinfo.value)
        assert not hasattr(data, "bar")

    def test_internal_attributes_cannot_be_explicitly_set(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            data.set_unknown_aws_attribute("_internal_value", "hello")

        assert "_internal_value" in str(excinfo.value)
        assert not hasattr(data, "_internal_value")

    # Set Special Cases
    # -----------------

    def test_attribute_can_be_set_to_none(self):
        """An attribute can be set to None, although
        it can't be initialised to None in the constructor.
        """
        # Setup
        data = self.SimpleObject()
        assert not hasattr(data, "Foo")

        # Exercise
        data.Foo = None

        # Verify
        assert hasattr(data, "Foo")
        assert data.Foo is None

    # Read Special Cases
    # ------------------

    def test_aws_attributes_cannot_be_read_before_they_are_set(self):
        data = self.SimpleObject()

        assert not hasattr(data, "Foo")

    # Update
    # ------

    @given(aws_attribute_strategy(), aws_attribute_strategy(), aws_attribute_strategy())
    def test_aws_attributes_can_be_updated(self, foo_value_old, foo_value_new, bar_value):
        data = self.SimpleObject()

        # Setup: set initial values
        data.Foo = foo_value_old
        data.bar = bar_value

        # Exercise
        data.Foo = foo_value_new

        # Verify
        assert data.Foo is foo_value_new
        assert data.bar is bar_value

    @given(st.text(), st.text())
    def test_internal_attributes_can_be_updated(self, old_value, new_value):
        data = self.SimpleObject()
        data._internal_value = old_value

        data._internal_value = new_value

        assert data._internal_value is new_value

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_updated_directly(self, old_value, new_value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data.WeirdValue = new_value

        assert data.WeirdValue is new_value

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_updated_via_explicit_setter(self, old_value, new_value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data.set_unknown_aws_attribute("WeirdValue", new_value)

        assert data.WeirdValue is new_value

    # Delete
    # ------

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_aws_attributes_can_be_deleted(self, foo_value, bar_value):
        data = self.SimpleObject()

        # Setup: set initial values
        data.Foo = foo_value
        data.bar = bar_value

        # Exercise
        del data.Foo
        del data.bar

        # Verify
        assert not hasattr(data, "Foo")
        assert not hasattr(data, "bar")

    @given(st.text())
    def test_internal_attributes_can_be_deleted(self, value):
        data = self.SimpleObject()
        data._internal_value = value

        del data._internal_value

        assert not hasattr(data, "_internal_value")

    @given(aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_deleted(self, value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        del data.WeirdValue

        assert not hasattr(data, "WeirdValue")

    def test_delete_nonexistent_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data.DoesNotExist

        assert "DoesNotExist" in str(excinfo.value)

    def test_delete_unset_aws_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data.Foo

        assert "Foo" in str(excinfo.value)

    def test_delete_nonexistent_internal_attribute_raises_error(self):
        data = self.SimpleObject()

        with pytest.raises(AttributeError) as excinfo:
            del data._internal_value

        assert "_internal_value" in str(excinfo.value)

    @given(aws_attribute_strategy())
    def test_delete_already_deleted_unknown_aws_attribute_raises_error(self, value):
        data = self.SimpleObject()
        data.set_unknown_aws_attribute("WeirdValue", value)
        del data.WeirdValue

        with pytest.raises(AttributeError) as excinfo:
            del data.WeirdValue

        assert "WeirdValue" in str(excinfo.value)


class TestDictionaryAccess:
    """Verify behaviour of dictionary access to attributes on a Flying Circus AWS object"""

    # CRUD Access for AWS Attributes
    # ------------------------------

    @given(aws_attribute_strategy())
    def test_aws_attributes_can_be_set(self, value):
        data = SingleAttributeObject()

        data["one"] = value

        assert hasattr(data, "one")
        assert data.one is value

    @given(aws_attribute_strategy())
    def test_aws_attributes_can_be_read(self, value):
        data = SingleAttributeObject(one=value)

        assert data["one"] is value

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_aws_attributes_can_be_updated(self, old_value, new_value):
        data = SingleAttributeObject(one=old_value)

        data["one"] = new_value

        assert data["one"] is new_value
        assert data.one is new_value

    @given(aws_attribute_strategy())
    def test_aws_attributes_can_be_deleted(self, value):
        data = SingleAttributeObject(one=value)

        del data["one"]

        assert not hasattr(data, "one")

    def test_unset_aws_attributes_cannot_be_read(self):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            _ = data["one"]

        assert "one" in str(excinfo.value)

    def test_unset_aws_attributes_cannot_be_deleted(self):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            del data["one"]

        assert "one" in str(excinfo.value)

    # CRUD Access For Internal Attributes
    # -----------------------------------

    @given(st.text())
    def test_internal_attributes_cannot_be_set(self, value):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            data["_internal_value"] = value

        assert "_internal_value" in str(excinfo.value)

    @given(st.text())
    def test_internal_attributes_cannot_be_read(self, value):
        data = SingleAttributeObject()
        data._internal_value = value

        with pytest.raises(KeyError) as excinfo:
            _ = data["_internal_value"]

        assert "_internal_value" in str(excinfo.value)

    @given(st.text(), st.text())
    def test_internal_attributes_cannot_be_updated(self, old_value, new_value):
        data = SingleAttributeObject()
        data._internal_value = old_value

        with pytest.raises(KeyError) as excinfo:
            data["_internal_value"] = new_value

        assert "_internal_value" in str(excinfo.value)
        assert data._internal_value is old_value

    @given(st.text())
    def test_internal_attributes_cannot_be_deleted(self, value):
        data = SingleAttributeObject()
        data._internal_value = value

        with pytest.raises(KeyError) as excinfo:
            del data["_internal_value"]

        assert "_internal_value" in str(excinfo.value)
        assert data._internal_value is value

    # CRUD Access For Unknown AWS Attributes
    # --------------------------------------

    @given(aws_attribute_strategy())
    def test_unknown_aws_attributes_cannot_be_set_directly(self, value):
        data = SingleAttributeObject()

        with pytest.raises(KeyError) as excinfo:
            data["WeirdValue"] = value

        assert "WeirdValue" in str(excinfo.value)

    @given(aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_read(self, value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        assert data["WeirdValue"] is value

    @given(aws_attribute_strategy(), aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_updated(self, old_value, new_value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", old_value)

        data["WeirdValue"] = new_value

        assert data["WeirdValue"] is new_value
        assert data.WeirdValue is new_value

    @given(aws_attribute_strategy())
    def test_unknown_aws_attributes_can_be_deleted(self, value):
        data = SingleAttributeObject()
        data.set_unknown_aws_attribute("WeirdValue", value)

        del data["WeirdValue"]

        assert not hasattr(data, "WeirdValue")


class TestIteratorAccess:
    """Verify behaviour of attribute iteration on a Flying Circus AWS object.

    Note that attribute length is highly coupled functionality, so we verify
    the behaviour of both `__iter__` and `__len__` together.
    """

    # TODO Test cases for empty tests on an object (ie. object has length 0)
    #   object with no attributes
    #   object with no attributes set (ie. empty)
    #   non-empty object with some/all attributes that are empty

    def test_object_iteration_returns_attribute_names(self):
        # Setup
        data = DualAttributeObject(one=42, two='hello world')

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_includes_unknown_attributes(self):
        # Setup
        data = DualAttributeObject(one=42, two='hello world')
        data.set_unknown_aws_attribute("special", 8)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'special', 'two']
        assert len(data) == 3

    def test_object_iteration_includes_attributes_set_to_none(self):
        # Setup
        data = DualAttributeObject(one=42)
        data.two = None

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_excludes_unset_attributes(self):
        # Setup
        data = DualAttributeObject(one=42)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one']
        assert len(data) == 1

    def test_object_iteration_excludes_internal_attributes(self):
        # Setup
        data = DualAttributeObject(one=42, two='hello world')
        data._internal_value = 7

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['one', 'two']
        assert len(data) == 2

    def test_object_iteration_uses_export_sorting(self):
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"one", "two"}
            EXPORT_ORDER = ["two", "one"]

        # Setup
        data = OrderedObject(one=42, two='hello world')

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['two', 'one']
        assert len(data) == 2


class TestIteratorSortOrder:
    """Verify that the attribute iteration follows complex attribute sorting rules."""

    def test_attributes_are_ordered_alphabetically_by_default(self):
        # Setup
        class MegaObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b", "c", "A", "Bad", "bad", "42", "4", "1", "z", "ZoologicalSpecimen"}

        data = MegaObject(
            a=1,
            b=2,
            c=3,
            A=4,
            Bad=5,
            bad=6,
            # NB: You can't set numeric string keys in the constructor
            # 42=7,
            # 4=8,
            # 1=9,
            z=10,
            ZoologicalSpecimen=11,
        )

        setattr(data, "42", 7)
        setattr(data, "4", 8)
        setattr(data, "1", 9)

        data.set_unknown_aws_attribute("badness", 12)
        data.set_unknown_aws_attribute("baddie", 13)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == [
            '1',
            '4',
            '42',
            'A',
            'a',
            'b',
            'Bad',
            'bad',
            'baddie',
            'badness',
            'c',
            'z',
            'ZoologicalSpecimen',
        ]

    def test_some_attributes_can_have_an_explicit_order(self):
        # Setup
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b"}
            EXPORT_ORDER = ["b", "a"]

        data = OrderedObject(a=1, b=2)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b', 'a']

    def test_explicit_attribute_ordering_should_ignore_unset_attributes(self):
        # Setup
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b"}
            EXPORT_ORDER = ["b", "a"]

        data = OrderedObject(b=2)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b']

    def test_explicit_attribute_ordering_should_silently_ignore_attributes_that_dont_exist(self):
        # Setup
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b"}
            EXPORT_ORDER = ["b", "c", "a"]

        data = OrderedObject(a=1, b=2)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b', 'a']

    def test_explicit_attribute_ordering_can_use_unknown_aws_attributes(self):
        # Setup
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b"}
            EXPORT_ORDER = ["b", "c", "a"]

        data = OrderedObject(a=1, b=2)
        data.set_unknown_aws_attribute("c", 3)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b', 'c', 'a']

    def test_explicit_attribute_ordering_may_list_only_some_attributes(self):
        # Setup
        class OrderedObject(AWSObject):
            AWS_ATTRIBUTES = {"a", "b", "c", "d"}
            EXPORT_ORDER = ["b", "a"]

        data = OrderedObject(a=1, b=2, c=3, d=4)

        # Exercise
        attribs = iter(data)

        # Verify
        assert list(attribs) == ['b', 'a', 'c', 'd']


class _NestedObject(DualAttributeObject):
    """Test object that is a grandchild of AWSObject."""
    AWS_ATTRIBUTES = {"one", "two", "three", "four"}

    def __init__(self, one=None, two=None, three=None, four=None):
        DualAttributeObject.__init__(self, one=one, two=two)
        self._set_constructor_attributes(dict(three=three, four=four))


class TestSplitCurrentAttributes:
    """Verify behaviour of the _split_current_attributes() internal helper method."""

    # Happy Case :-)
    # --------------
    def test_current_class_attributes_are_separated_from_other_parameters(self):
        current, other = _NestedObject._split_current_attributes(dict(one=1, two=2, three=3, four=4))

        assert current == {"three": 3, "four": 4}
        assert other == {"one": 1, "two": 2}

    # Params Dict Corner Cases
    # ------------------------
    def test_results_are_empty_when_no_parameters_supplied(self):
        current, other = _NestedObject._split_current_attributes({})

        assert current == {}
        assert other == {}

    def test_only_supplied_parameters_are_used_when_some_parent_attributes_missing(self):
        current, other = _NestedObject._split_current_attributes(dict(two=2, three=3, four=4))

        assert current == {"three": 3, "four": 4}
        assert other == {"two": 2}

    def test_only_supplied_parameters_are_used_when_some_child_attributes_missing(self):
        current, other = _NestedObject._split_current_attributes(dict(one=1, two=2, four=4))

        assert current == {"four": 4}
        assert other == {"one": 1, "two": 2}

    def test_invalid_parameters_are_passed_to_parent(self):
        current, other = _NestedObject._split_current_attributes(dict(one=1, two=2, three=3, four=4, five=5))

        assert current == {"three": 3, "four": 4}
        assert other == {"one": 1, "two": 2, "five": 5}

    def test_original_parameters_dictionary_is_not_altered(self):
        params = dict(one=1, two=2, three=3, four=4)
        current, other = _NestedObject._split_current_attributes(params)

        assert params == {"one": 1, "two": 2, "three": 3, "four": 4}

    # AWS_ATTRIBUTES Corner Cases
    # ---------------------------

    def test_should_work_when_child_class_has_no_defined_aws_attributes(self):
        class ExtendedObject(DualAttributeObject):
            pass

        current, other = ExtendedObject._split_current_attributes(dict(one=1))

        assert current == {}
        assert other == {"one": 1}

    def test_should_work_when_parent_class_has_no_defined_aws_attributes(self):
        current, other = DualAttributeObject._split_current_attributes(dict(one=1))

        assert current == {"one": 1}
        assert other == {}

    def test_should_work_when_parent_class_has_no_defined_aws_attributes_but_grandparent_does(self):
        class BoringObject(DualAttributeObject):
            pass

        class ObjectWithMoreAttributes(BoringObject):
            AWS_ATTRIBUTES = {"one", "two", "three", "four"}

            def __init__(self, one=None, two=None, three=None, four=None):
                BoringObject.__init__(self, one=one, two=two)
                self._set_constructor_attributes(dict(three=three, four=four))

        current, other = ObjectWithMoreAttributes._split_current_attributes(dict(one=1, two=2, three=3, four=4))

        assert current == {"three": 3, "four": 4}
        assert other == {"one": 1, "two": 2}
