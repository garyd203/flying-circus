"""Represent the application of YAML functions.

These will probably return a special object that resolves into a YAML string containing the function reference. Some functions may be able to be resolved internally (hah!).
"""
from .core import *


class GetAtt(Function):
    """Models the behaviour of Fn:GetAtt for Python objects"""
    pass
