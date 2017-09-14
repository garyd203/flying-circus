from flyingcircus.core import Stack
from flyingcircus.services import s3

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
}'''  # FIXME this is JSON, not YAML


class TestCoreServices:
    def test_s3_as_naive_python(self):
        """As a developer, I can use a naive python representation of YAML to create objects representing a basic S3 bucket."""
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
            "!GetAtt S3Bucket.WebsiteURL",
            Description="URL for website hosted on S3",
        )
        stack.Outputs["S3BucketSecureURL"] = Output(
            '''!Join ["", ["https://", !GetAtt S3Bucket.DomainName]]''',
            Description="Name of S3 bucket to hold website content",
        )

        # Verify
        assert stack.export() == SIMPLE_S3_YAML

    def test_s3_as_simple_python(self):
        """As a developer, I can use a simplified Python interface to create Python objects representing a basic S3 bucket."""
        # Exercise
        stack = Stack(
            Description="vcvxcv",
        )
        bucket = s3.Bucket(
            Name="S3Bucket",
            Properties={
                "AccessControl": "PublicRead",
                "WebsiteConfiguration": {
                    "IndexDocument": "index.html",
                    "ErrorDocument": "error.html",
                }
            },
            DeletionPolicy="Retain",
        )
        stack.add(bucket)
        stack.add(Output(
            Name="WebsiteURL",
            Value=bucket.WebsiteURL,
            Description="URL for website hosted on S3",
        ))
        stack.add(Output(
            Name="S3BucketSecureURL",
            Value=YamlJoin("https://", bucket.DomainName),
            Description="Name of S3 bucket to hold website content",
        ))

        # Verify
        assert stack.export() == SIMPLE_S3_YAML
