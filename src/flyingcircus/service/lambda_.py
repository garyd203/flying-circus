"""General-use classes to interact with the Lambda service through CloudFormation.

See Also:
    `AWS developer guide for Lambda
    <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_
"""

import inspect
import sys
import warnings
from typing import Callable

import inflection

# noinspection PyUnresolvedReferences
from .._raw import lambda_ as _raw

# noinspection PyUnresolvedReferences
from .._raw.lambda_ import *


class Function(_raw.Function):
    __slots__ = []

    @classmethod
    def create_from_python_function(
        cls, handler: Callable, Role, Description=None, Runtime=None
    ) -> "Function":
        """Factory function to create a Function with inlined code from a Python function."""
        # Extract and format source code
        handler_sig = inspect.signature(handler)
        if len(handler_sig.parameters) > 2:
            raise ValueError("Lambda handler takes too many parameters")

        param_names = list(handler_sig.parameters.keys())
        if len(param_names) >= 1 and param_names[0] not in ("e", "event"):
            warnings.warn(
                UserWarning(
                    "First handler parameter has an unusual name: '{}'".format(
                        param_names[0]
                    )
                )
            )
        if len(param_names) >= 2 and param_names[1] not in ("c", "context"):
            warnings.warn(
                UserWarning(
                    "Second handler parameter has an unusual name: '{}'".format(
                        param_names[1]
                    )
                )
            )

        source = inspect.getsource(handler)

        # Automatically generate description. We pluck out just the first
        # paragraph of the docstring, formatted into a single line
        desc = Description
        if not desc:
            if handler.__doc__:
                docstring_lines = []
                for line in handler.__doc__.split("\n"):
                    line = line.strip()

                    # Use empty lines to detect paragraph breaks, and drop
                    # everything after the first paragraph
                    if not line:
                        if not docstring_lines:
                            # ...but just ignoire leading empty lines
                            continue
                        break

                    docstring_lines.append(line.strip())
                desc = " ".join(docstring_lines)
            else:
                desc = inflection.humanize(handler.__name__) + "."

        # Create a basic Function resource with only the compulsory properties
        return cls(
            Properties=FunctionProperties(
                Code=dict(ZipFile=source),
                Description=desc,
                Handler="index.{}".format(handler.__name__),
                Role=Role,
                Runtime=Runtime or get_lambda_runtime_for_this_process(),
            )
        )


#: Lambda Runtimes for Python that we know about.
#: See `the definitive list in the AWS documentation
#: <https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html>`_
_KNOWN_LAMBDA_RUNTIMES = {(2, 7): "python2.7", (3, 6): "python3.6", (3, 7): "python3.7"}


def get_lambda_runtime_for_this_process() -> str:
    """Determine the best Lambda runtime for the current Python process."""
    # The basic premise is to use exact matching if possible, upgrade if
    # necessary, and don't downgrade

    (major, minor, _, _, _) = sys.version_info

    try:
        return _KNOWN_LAMBDA_RUNTIMES[(major, minor)]
    except KeyError:
        pass

    # Maybe this is an old Python v3
    if major == 3 and minor < 6:
        return _KNOWN_LAMBDA_RUNTIMES[(3, 6)]

    # Maybe this is an old Python v2
    if major == 2 and minor < 7:
        return _KNOWN_LAMBDA_RUNTIMES[(2, 7)]

    raise ValueError(
        "Python version '{}' cannot be supported by AWS Lambda".format(sys.version)
    )
