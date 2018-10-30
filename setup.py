import os

from setuptools import find_packages
from setuptools import setup


def get_version_data():
    data = {}
    with open(os.path.join("src", "flyingcircus", "_about.py")) as fp:
        exec(fp.read(), data)
    return data


setup(
    name="flying-circus",
    version=get_version_data()['__version__'],
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    install_requires=[
        'boto3',
        'PyYAML',
    ],

    # metadata for upload to PyPI
    author="Gary Donovan",
    author_email="gazza@gazza.id.au",
    description="A tool for managing AWS infrastructure.",
    license="LGPL",  # TODO is this correct? v3?
    keywords="cloud formation",
    url="https://github.com/garyd203/flying-circus",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: System :: Systems Administration',
    ],
)
