"""Top-level py.test configuration"""

import pytest


def pytest_addoption(parser):
    # Allow users to skip integration tests that use AWS services
    # This is on by default, so that test work out of the box. Hopefully the
    # skipped tests will be a red flag for people to investigate further.
    parser.addoption(
        "--run-aws-integration-tests",
        action="store_true",
        default=False,
        help="Run integration tests that connect to AWS",
    )


def pytest_collection_modifyitems(config, items):
    # Skip AWS integration tests. This relies on a pytest marker
    if not config.getoption("--run-aws-integration-tests"):
        skip_aws_integration = pytest.mark.skip(
            reason="Don't attempt to run tests that need AWS authentication and network access"
        )
        for item in items:
            if "aws_integration" in item.keywords:
                item.add_marker(skip_aws_integration)
