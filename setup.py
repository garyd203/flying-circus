import os

from setuptools import find_packages
from setuptools import setup

THIS_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def get_version_data():
    data = {}
    with open(os.path.join(THIS_DIRECTORY, "src", "flyingcircus", "_about.py")) as fp:
        exec(fp.read(), data)
    return data


def get_readme():
    with open(os.path.join(THIS_DIRECTORY, "README.md")) as fp:
        desc = fp.read()
    return desc


setup(
    # Basic Project Description
    name="flying-circus",
    version=get_version_data()["__version__"],
    description="A tool for describing AWS infrastructure as code",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    # Project Packaging
    # FIXME I think we are still packaging fcspike???
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # FIXME do we need this?
    install_requires=[
        # We use the `kw_only` only for attribute classes, which was
        # introduced in v18.2.0
        "attrs>=18.2.0",
        "inflection>=0.3.1,<0.4",
        "PyYAML==5.1.1",
    ],
    # Contact Details
    author="Gary Donovan",
    author_email="gazza@gazza.id.au",
    url="https://github.com/garyd203/flying-circus",
    project_urls={
        "Documentation": "https://flying-circus.readthedocs.io/en/latest/",
        "Source": "https://github.com/garyd203/flying-circus",
        "Tracker": "https://github.com/garyd203/flying-circus/issues",
    },
    # Other metadata for PyPI
    license="LGPL v3",
    keywords="AWS cloudformation infrastructure-as-code",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: System :: Systems Administration",
    ],
    metadata_version="2.1",
)
