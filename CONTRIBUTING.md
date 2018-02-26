# Contributing to Flying Circus
We are still finding our way in the early days of this project.
If you have any feedback, bugs or suggestions, please [open an
issue](https://github.com/garyd203/flying-circus/issues/new)
in GitHub.

# Process Notes

## Creating A Release

This is a manual process at the moment. See the
[python packaging guide](https://packaging.python.org/tutorials/distributing-packages/#packaging-your-project)
for soem background and guidance. Or just do the following steps
(hand wavy description) on your local workstation

1. Make sure there are no uncommitted changes in your local workspace
2. Checkout `master` branch and get the latest:
   ```bash
   git checkout master
   git pull
   ```
3. Create a fresh venv and run all tests (including integration tests)
   ```bash
   rm -rf venv
   virtualenv venv
   ./venv/bin/activate
   pip install -r requirements.txt
   pip install -e . # Install the local working copy of flying circus in "edit" mode
   export AWS_PROFILE=your-aws-test-profile
   pytest tests --run-aws-integration-tests
   ```
4. Ensure the trove classifiers in setup.py are up to date
5. Ensure `install_requires` in setup_py is up to date with
   `requirements.txt`. However, we shouldn't include test dependencies
   here 
6. Ensure `__version__` in `_about.py` reflects what you want to release.
   Pay attention to major/minor/patch numbers, and ensure
   this is not a version that has already been released to PyPI
7. Commit any changes you may have made :-) If you did make changes,
   then go around the merry go round of branch-commit-pr-merge-pull
   once more, and re-run tests.
8. Do a clean build and upload to PyPI
   ```bash
   deactivate # Don't do a release from a virtual environment
   rm -rf dist
   python setup.py sdist
   python setup.py bdist_wheel # this will be --universal in the future)
   twine upload dist/*
   ```
9. Check the correct build appears in PyPI
10. Tag the release in git. Make sure you push the tag to upstream
    ```bash
    git tag -a release-0.4.0 -m "#63: Release version 0.4.0"
    git push origin release-0.4.0
    ```
11. Bump version in _about.py in order to avoid unfortunate mistakes :-)
12. Close any relevant github issue and milestone
13. Make a github release. This seems to magically work from our tag name
    format
14. Announce the exciting new release:
    * Python announcement lists
    * Twitter
    * Gary's personal mailing list
15. Sit back for a moment and revel in your excellent-ness
