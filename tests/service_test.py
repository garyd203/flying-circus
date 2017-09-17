from flyingcircus.config import ExportYamlContext
from flyingcircus.core import Stack
from flyingcircus.core import Output
from flyingcircus.service import s3

SIMPLE_S3_YAML = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",

  "Description" : "AWS CloudFormation Sample Template S3_Website_Bucket_With_Retain_On_Delete: Sample template showing how to create a publicly accessible S3 bucket configured for website access with a deletion policy of retail on delete. **WARNING** This template creates an S3 bucket that will NOT be deleted when the stack is deleted. You will be billed for the AWS resources used if you create a stack from this template.",

  "Resources" : {
    "S3Bucket" : {
      "Type" : "AWS::S3::Bucket",
      "Properties" : {
        "AccessControl" : "PublicRead",
        "WebsiteConfiguration" : {
          "IndexDocument" : "index.html",
          "ErrorDocument" : "error.html"      
         }
      },
      "DeletionPolicy" : "Retain"
    }
  },

  "Outputs" : {
    "WebsiteURL" : {
      "Value" : { "Fn::GetAtt" : [ "S3Bucket", "WebsiteURL" ] },
      "Description" : "URL for website hosted on S3"
    },
    "S3BucketSecureURL" : {
      "Value" : { "Fn::Join" : [ "", [ "https://", { "Fn::GetAtt" : [ "S3Bucket", "DomainName" ] } ] ] },
      "Description" : "Name of S3 bucket to hold website content"
    }
  } 
}'''  # FIXME this is JSON, not YAML. also should be canonicalised (for some value of canonicalisation that macthes what we do)


class TestCoreServices:
    def test_s3_as_naive_python(self):
        """As a developer, I can use a straightforward python representation of YAML to create objects representing a basic S3 bucket."""
        # Exercise
        stack = Stack(
            AWSTemplateFormatVersion="2010-09-09",
            Description="vcvxcv",
        )
        stack.Resources["S3Bucket"] = s3.Bucket(
            Properties={
                "AccessControl": "PublicRead",
                "WebsiteConfiguration": {
                    "IndexDocument": "index.html",
                    "ErrorDocument": "error.html",
                }
            },
            DeletionPolicy="Retain",
        )
        stack.Outputs["WebsiteURL"] = Output(
            Value="!GetAtt S3Bucket.WebsiteURL",
            Description="URL for website hosted on S3",
        )
        stack.Outputs["S3BucketSecureURL"] = Output(
            Value='''!Join ["", ["https://", !GetAtt S3Bucket.DomainName]]''',
            Description="Name of S3 bucket to hold website content",
        )

        # Verify
        # TODO print(yaml.dump({'a': 42, 'b': 55, 'c': {"tag": "AWS::xyz", "foo":"HELLoworld"}}, line_break=True, default_flow_style=False))
        with ExportYamlContext():  # this context manager simply makes explicit the defualt behavious of stringifying as YAML
            assert str(stack) == SIMPLE_S3_YAML

    def test_s3_as_magic_python(self):
        """As a developer, I can use a magic Python interface to create Python objects representing a basic S3 bucket."""
        # Exercise
        bucket = s3.Bucket(
            Name="S3Bucket",
            Properties={
                # TODO needs to be abstracted so we can export in a variable format
                "AccessControl": "PublicRead",
                "WebsiteConfiguration": {
                    "IndexDocument": "index.html",
                    "ErrorDocument": "error.html",
                }
            },
            DeletionPolicy="Retain",
        )
        stack = Stack(
            Description="vcvxcv",
            WebsiteURL=Output(
                Value=bucket.WebsiteURL,
                Description="URL for website hosted on S3",
            ),
            S3BucketSecureURL=Output(
                Value=Join("https://", bucket.DomainName),
                Description="Name of S3 bucket to hold website content",
            ),
        ).add(bucket)

        # Verify
        with ExportYamlContext():
            assert str(stack) == SIMPLE_S3_YAML
