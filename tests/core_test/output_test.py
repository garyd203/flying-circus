"""Tests for Parameters and PseudoParameters"""

from flyingcircus.core import Output
from flyingcircus.core import dedent


class TestBasicOutputBehaviour:
    """Verify basic behaviour of the Output class"""

    def test_export_basic_output(self):
        """Should be able to create and export a simple CloudFormation Output object."""
        output = Output(Description="Stuff we need", Value=6644, Export={"Name": "ImportantThingy"})
        exported = output.export("yaml")

        assert exported == dedent("""
        ---
        Description: Stuff we need
        Export:
          Name: ImportantThingy
        Value: 6644
        """)
