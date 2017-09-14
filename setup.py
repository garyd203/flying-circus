from setuptools import setup, find_packages

setup(
    name="flying-circus",
    version="0.0.2",
    packages=find_packages(),

    # metadata for upload to PyPI
    author="Gary Donovan",
    author_email="gazza@gazza.id.au",
    description="A tool for managing AWS infrastructure.",
    license="LGPL", #TODO is this correct? v3?
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
