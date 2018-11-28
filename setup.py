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
        # We use the `kw_only` only for attribute classes, which was
        # introduced in v18.2.0
        'attrs>=18.2.0',
        'PyYAML',
    ],

    # metadata for upload to PyPI
    author="Gary Donovan",
    author_email="gazza@gazza.id.au",
    description="A tool for managing AWS infrastructure.",
    license="LGPL v3",
    keywords="AWS cloudformation infrastructure-as-code",
    url="https://github.com/garyd203/flying-circus",
    project_urls={
        'Documentation': "https://flying-circus.readthedocs.io/en/latest/",
        'Source': "https://github.com/garyd203/flying-circus",
        'Tracker': "https://github.com/garyd203/flying-circus/issues",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
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
