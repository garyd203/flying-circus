Doing a Release
===============

This is a manual process at the moment. See the
`python packaging guide <https://packaging.python.org/tutorials/distributing-packages/#packaging-your-project>`_
for some background and guidance. Or just do the following steps
(hand wavy description) on your local workstation (Linux works best)

#. Ensure the trove classifiers in ``setup.py`` are up to date
#. Ensure ``install_requires`` in setup_py is up to date with
   ``requirements.txt``. However, we shouldn't include test dependencies
   here.
#. Ensure ``__version__`` in ``_about.py`` reflects what you want to release.
   Pay attention to major/minor/patch numbers, and ensure
   this is not a version that has already been released to PyPI
#. Update ``CHANGELOG.md``
#. Commit any changes you may have made and merge into master on Github.
#. Make sure there are no uncommitted changes in your local workspace
#. Checkout ``master`` branch and get the latest:

   .. code-block:: bash

      git checkout master
      git pull
#. Create a fresh venv and run all tests (including integration tests)

   .. code-block:: bash

      rm -rf venv
      virtualenv -p python3.6 venv
      source ./venv/bin/activate
      pip install -r requirements.txt
      pip install -e . # Install the local working copy of flying circus in "edit" mode
      export AWS_PROFILE=your-aws-test-profile
      pytest tests --run-aws-integration-tests
#. Do a clean build and upload to PyPI:

   .. code-block:: bash

      deactivate # Don't do a release from a virtual environment
      rm -rf dist
      python3.6 setup.py sdist
      python3.6 setup.py bdist_wheel # this will be --universal in the future
      # TODO test upload with twine
      twine upload dist/*
#. Check the correct build appears in PyPI
#. Tag the release in git. Make sure you push the tag to upstream:

   .. code-block:: bash

      git tag -a release-0.4.0 -m "#63: Release version 0.4.0"
      git push origin release-0.4.0
#. Bump version in ``_about.py`` in order to avoid unfortunate mistakes :-)
#. Close any relevant github issue and milestone
#. Make a github release. This seems to magically work from our tag name
   format.
#. Announce the exciting new release:

   * Python announcement lists
   * Twitter
   * Gary's personal mailing list
#. Sit back for a moment and revel in your excellent-ness
