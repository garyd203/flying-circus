"""Tests for Parameters and PseudoParameters"""

import pytest

from flyingcircus.core import AWSObject
from flyingcircus.core import Parameter
from flyingcircus.core import PseudoParameter
from flyingcircus.core import dedent
from flyingcircus.yaml import CustomYamlObject
from .common import SingleAttributeObject


class TestBasicParameterBehaviour:
    """Verify basic behaviour of the Parameter class"""

    def test_export_basic_parameter(self):
        """Should be able to create and export a simple parameter."""
        param = Parameter(Type="String", Default="Hello world")
        output = param.export("yaml")

        assert output == dedent("""
        ---
        Type: String
        Default: Hello world
        """)


class TestPseudoParameter:
    """Verify behaviour and values of the PseudoParameter class"""

    def test_can_be_used_as_string_value_in_scalar_node(self):
        class _ValueWithPseudoParameter(CustomYamlObject):
            def as_yaml_node(self, dumper):
                param = PseudoParameter("AWS::FakeTestValue")
                return dumper.represent_str(param)

        value = _ValueWithPseudoParameter()
        data = SingleAttributeObject(one=value)

        # Exercise
        output = data.export("yaml")

        # Verify
        assert output == dedent("""
            ---
            one: AWS::FakeTestValue
            """)

    def test_cannot_be_exported_as_yaml_directly(self):
        value = PseudoParameter("AWS::FakeTestValue")
        data = SingleAttributeObject(one=value)

        # Exercise
        with pytest.raises(TypeError) as excinfo:
            _ = data.export("yaml")

        # Verify
        assert "does not extend CustomYamlObject" in str(excinfo.value)

    def test_is_not_an_awsobject(self):
        """A PseudoParameter does not represent a user-defined construct in a
        CloudFormation stack, hence it is inappropriate for it to be an
        AWSObject.
        """
        value = PseudoParameter("AWS::FakeTestValue")

        assert not isinstance(value, AWSObject)

    def test_all_pseudo_parameters_are_listed_in_a_constant(self):
        # Verify constant exists
        assert hasattr(PseudoParameter, "ALL")

        # Verify constant has a number of entries
        assert len(PseudoParameter.ALL) > 2

        # Verify each entry looks superficially valid
        for param in PseudoParameter.ALL:
            assert isinstance(param, PseudoParameter)
            assert param.startswith("AWS::")
