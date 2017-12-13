"""Helper functions to validate output."""

import boto3
import pytest
from botocore.exceptions import ClientError


class AwsTemplateValidation:
    """Base class to validate the content of a CloudFormation stack template."""

    def get_stacks_under_test(self):
        """Return a list of concrete stack objects that need to be validated."""
        return []

    @pytest.mark.aws_integration
    def test_validate_stacks(self):
        # Setup
        cfclient = boto3.client("cloudformation")

        # Verify
        for stack in self.get_stacks_under_test():
            template = stack.export("yaml")
            try:
                cfclient.validate_template(TemplateBody=template)
            except ClientError as ex:
                print("Error validating template for `{}`".format(stack.Description.replace('\n', ' ')))
                error_data = getattr(ex, "response", {}).get("Error", None)
                if error_data and error_data["Code"] == "ValidationError":
                    pytest.fail("{} template is invalid: {}".format(stack.__class__.__name__, error_data["Message"], ))
                else:
                    raise
