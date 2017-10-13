from setuptools import find_packages
from setuptools import setup

setup(
    name="flying-circus",
    version="0.4",
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    install_requires=[
        'pyyaml',
    ],

    # metadata for upload to PyPI
    author="Gary Donovan",
    author_email="gazza@gazza.id.au",
    description="A tool for managing AWS infrastructure.",
    license="LGPL",  # TODO is this correct? v3?
    keywords="cloud formation",
    url="https://github.com/garyd203/flying-circus",
    classifiers=[
        # TODO add more classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
