"""Tests for the package itself"""

import importlib
import importlib.util
import inspect

import importlib_resources
import pytest
import semver

import flyingcircus
import flyingcircus.service
from flyingcircus.core import AWSObject


def test_has_version_attribute():
    assert hasattr(flyingcircus, "__version__")
    assert isinstance(flyingcircus.__version__, str)
    _ = semver.parse(flyingcircus.__version__)  # Should not raise ValueError


def test_all_exported_classes_have_slots():
    """All "public" classes that form part of the library's interface should have `__slots__`.

    When defining a subclass of AWSObject, it is possible to accidentally
    forget to add an empty __slots__ class variable. This means that
    unknown variables can accidentally be set on that class - violating
    the well-defined behaviour of our types.
    """
    # Modules to inspect
    public_modules = [
        flyingcircus.core,
        flyingcircus.intrinsic_function,
    ]

    # Packages to inspect
    public_packages = [
        flyingcircus.service,
    ]

    # Get public module from public packages
    for package in public_packages:
        for filename in importlib_resources.contents(package):
            # Ignore special filenames/modules
            if filename.startswith("__"):
                continue

            modulename = package.__name__ + "." + filename.split(".")[0]
            module = importlib.import_module(modulename)
            public_modules.append(module)

    # Verify that every AWSObject-like class in a public module has
    # a well-defined attribute list
    for module in public_modules:
        for name, obj in module.__dict__.items():

            if not inspect.isclass(obj):
                continue
            if not issubclass(obj, AWSObject):
                continue
            if obj is flyingcircus.core.Resource:
                # Resource is abstract, so we can't check it directly
                continue

            full_class_name = f"{module.__name__}.{name}"

            try:
                instance = obj()
            except Exception as ex:
                assert False, f"Unable to instantiate {full_class_name}: " + str(ex)

            nonexistent_attrib_name = "ThisAttributeDoesNotExist"
            with pytest.raises(
                    AttributeError,
                    message=f"{full_class_name} hasn't defined __slots__",
                    match=f"{obj.__name__}.*{nonexistent_attrib_name}"
            ):
                setattr(instance, nonexistent_attrib_name, 42)
