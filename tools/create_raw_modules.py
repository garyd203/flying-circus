#!/usr/bin/env python

"""
Create the basic Python modules in the `_raw` package.

These are automatically generated from a JSON specification provided by Amazon,
which is documented at https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification-format.html
"""

import json
import logging
import os.path

import black
import click
import inflection
from jinja2 import FileSystemLoader, Environment

LOGGER = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

BLACK_SETTINGS = black.FileMode(
    target_versions={black.TargetVersion.PY36, black.TargetVersion.PY37}
)

#: Lookup table of documentation URL's for AWS services. This information does
#: not appear to be in the specification, and does not have a deterministic URL.
AWS_SERVICE_DOCUMENTATION_URLS = {
    "AmazonMQ": "https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html",
    "Amplify": "https://docs.aws.amazon.com/amplify/latest/userguide/getting-started.html",
    "ApiGateway": "https://docs.aws.amazon.com/apigateway/latest/developerguide/index.html",
    "ApiGatewayV2": "https://docs.aws.amazon.com/apigateway/latest/developerguide/index.html",
    "ApplicationAutoScaling": "https://docs.aws.amazon.com/autoscaling/application/APIReference/Welcome.html",
    "AppMesh": "https://docs.aws.amazon.com/app-mesh/?id=docs_gateway",
    "AppStream": "https://docs.aws.amazon.com/appstream2/latest/developerguide/index.html",
    "AppSync": "https://docs.aws.amazon.com/appsync/latest/devguide/welcome.html",
    "Athena": "https://docs.aws.amazon.com/athena/latest/ug/what-is.html",
    "AutoScaling": "http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html",
    "AutoScalingPlans": "https://docs.aws.amazon.com/autoscaling/plans/userguide/",
    "Backup": "https://docs.aws.amazon.com/aws-backup/latest/devguide/index.html",
    "Batch": "https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html",
    "Budgets": "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/",
    "CertificateManager": "https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html",
    "Cloud9": "https://docs.aws.amazon.com/cloud9/latest/user-guide/index.html",
    "CloudFormation": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/index.html",
    "CloudFront": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html",
    "CloudTrail": "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html",
    "CloudWatch": "http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html",
    "CodeBuild": "https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html",
    "CodeCommit": "https://docs.aws.amazon.com/codecommit/latest/userguide/index.html",
    "CodeDeploy": "https://docs.aws.amazon.com/codedeploy/latest/userguide/index.html",
    "CodePipeline": "https://docs.aws.amazon.com/codepipeline/latest/userguide/index.html",
    "CodeStar": "https://docs.aws.amazon.com/codestar/latest/userguide/welcome.html",
    "Cognito": "https://docs.aws.amazon.com/cognito/latest/developerguide/index.html",
    "Config": "https://docs.aws.amazon.com/config/latest/developerguide/index.html",
    "DataPipeline": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
    "DAX": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html",
    "DirectoryService": "https://docs.aws.amazon.com/directoryservice/latest/admin-guide/index.html",
    "DLM": "https://docs.aws.amazon.com/dlm/latest/APIReference/Welcome.html",
    "DMS": "https://docs.aws.amazon.com/dms/latest/userguide/index.html",
    "DocDB": "https://docs.aws.amazon.com/documentdb/latest/developerguide/index.html",
    "DynamoDB": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/index.html",
    "EC2": "http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/",
    "ECR": "https://docs.aws.amazon.com/AmazonECR/latest/userguide/index.html",
    "ECS": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/index.html",
    "EFS": "https://docs.aws.amazon.com/efs/latest/ug/index.html",
    "EKS": "https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html",
    "ElastiCache": "https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/index.html",
    "ElasticBeanstalk": "https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/index.html",
    "ElasticLoadBalancing": "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/index.html",
    "ElasticLoadBalancingV2": "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/index.html",
    "Elasticsearch": "https://docs.aws.amazon.com/workspaces/latest/adminguide/index.html",
    "EMR": "https://docs.aws.amazon.com/dms/latest/userguide/index.html",
    "Events": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html",
    "FSx": "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/index.html",
    "GameLift": "https://docs.aws.amazon.com/gamelift/latest/developerguide/index.html",
    "Glue": "https://docs.aws.amazon.com/glue/latest/dg/index.html",
    "Greengrass": "https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html",
    "GuardDuty": "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html",
    "IAM": "https://docs.aws.amazon.com/IAM/latest/UserGuide/index.html",
    "Inspector": "https://docs.aws.amazon.com/inspector/latest/userguide/index.html",
    "IoT": "https://docs.aws.amazon.com/iot/latest/developerguide/index.html",
    "IoT1Click": "https://docs.aws.amazon.com/iot-1-click/latest/developerguide/index.html",
    "IoTAnalytics": "https://docs.aws.amazon.com/appsync/latest/devguide/welcome.html",
    "IoTThingsGraph": "https://docs.aws.amazon.com/thingsgraph/latest/ug/index.html",
    "IoTEvents": "https://docs.aws.amazon.com/iotevents/latest/developerguide/index.html",
    "Kinesis": "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html",
    "KinesisAnalytics": "https://docs.aws.amazon.com/kinesisanalytics/latest/dev/what-is.html",
    "KinesisAnalyticsV2": "https://docs.aws.amazon.com/kinesisanalytics/latest/java/what-is.html",
    "KinesisFirehose": "https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html",
    "KMS": "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html",
    "LakeFormation": "https://docs.aws.amazon.com/lake-formation/latest/dg/index.html",
    "Lambda": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    "Logs": "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/index.html",
    "ManagedBlockchain": "https://docs.aws.amazon.com/managed-blockchain/latest/managementguide",
    "MediaLive": "https://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html",
    "MediaStore": "https://docs.aws.amazon.com/mediastore/latest/ug/what-is.html",
    "MSK": "https://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html",
    "Neptune": "https://docs.aws.amazon.com/neptune/latest/userguide/index.html",
    "OpsWorks": "https://docs.aws.amazon.com/opsworks/latest/userguide/index.html",
    "OpsWorksCM": "https://docs.aws.amazon.com/opsworks/latest/userguide/index.html",
    "Pinpoint": "https://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html",
    "PinpointEmail": "http://docs.aws.amazon.com/pinpoint/latest/userguide/welcome.html",
    "QLDB": "https://docs.aws.amazon.com/qldb/latest/developerguide/index.html",
    "RAM": "https://docs.aws.amazon.com/ram/latest/userguide/index.html",
    "RDS": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/index.html",
    "Redshift": "https://docs.aws.amazon.com/redshift/latest/gsg/index.html",
    "RoboMaker": "https://docs.aws.amazon.com/robomaker/latest/dg/index.html",
    "Route53": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/index.html",
    "Route53Resolver": "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/index.html",
    "S3": "https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html",
    "SageMaker": "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html",
    "SDB": "https://docs.aws.amazon.com/AmazonSimpleDB/latest/DeveloperGuide/index.html",
    "SecretsManager": "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html",
    "SecurityHub": "https://docs.aws.amazon.com/securityhub/latest/userguide/index.html",
    "ServiceCatalog": "https://docs.aws.amazon.com/servicecatalog/latest/dg/index.html",
    "ServiceDiscovery": "https://docs.aws.amazon.com/cloud-map/latest/dg/index.html",
    "SES": "https://docs.aws.amazon.com/servicecatalog/latest/dg/index.html",
    "SNS": "https://docs.aws.amazon.com/sns/latest/dg/welcome.html",
    "SQS": "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html",
    "SSM": "https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html",
    "StepFunctions": "https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html",
    "Transfer": "https://docs.aws.amazon.com/transfer/latest/userguide/index.html",
    "WAF": "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html",
    "WAFRegional": "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html",
    "WorkSpaces": "https://docs.aws.amazon.com/workspaces/latest/adminguide/index.html",
}

#: Lookup table of documentation URL's for non-AWS services.
OTHER_SERVICE_DOCUMENTATION_URLS = {
    "Alexa": {
        "ASK": "https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html"
    }
}

#: AWS CFN resources that have non-standard attributes.
#:
#: Some of the CloudFormation resource attributes are only valid for a few AWS
#: resources. This is a list of which attributes exist on which resources
#:
#: See http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-creationpolicy.html
#: and http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html
RESOURCES_WITH_EXTRA_ATTRIBUTES = {
    # {resource_type_fullname: [attribute_name]}
    "AWS::AutoScaling::AutoScalingGroup": ["CreationPolicy", "UpdatePolicy"],
    "AWS::CloudFormation::WaitCondition": ["CreationPolicy"],
    "AWS::EC2::Instance": ["CreationPolicy"],
    "AWS::ElastiCache::ReplicationGroup": ["UpdatePolicy"],
    "AWS::Lambda::Alias": ["UpdatePolicy"],
}

#: The directory where this script lives
SCRIPTDIR = os.path.dirname(__file__)


@click.command()
@click.argument(
    "packagedir",
    metavar="FCPACKAGE",
    type=click.Path(exists=True, file_okay=False),
    required=True,
)
@click.option(
    "--specification",
    "-s",
    type=click.Path(exists=True, dir_okay=False),
    default=os.path.join(
        SCRIPTDIR, "..", "contrib", "CloudFormationResourceSpecification.json"
    ),
    help="JSON resource specification from Amazon Web Services.",
    show_default=True,
)
def generate_modules(packagedir, specification):
    """Create the basic Python modules in the `_raw` package,
    and ensure the accompanying modules in the `service` package exist.

    The output directory argument should be the location of the existing
    'src/flyingcircus/' directory, where generated files will be placed.
    Existing files will be replaced.
    """
    # Check inputs
    raw_dirname = os.path.join(packagedir, "_raw")
    assert os.path.isdir(raw_dirname), "The 'flyingcircus._raw' package does not exist"

    service_dirname = os.path.join(packagedir, "service")
    assert os.path.isdir(
        service_dirname
    ), "The 'flyingcircus.service' package does not exist"

    # Load data as a python dictionary
    with open(specification, "r") as fp:
        all_data = json.load(fp)

    assert set(all_data.keys()) == {
        "PropertyTypes",
        "ResourceSpecificationVersion",
        "ResourceTypes",
    }, "Found an unknown top-level key"

    # Group the data by AWS service and calculate additional data
    services = {}

    for resource_type, resource_data in all_data["ResourceTypes"].items():
        # Break down the resource type
        assert (
            resource_type.count("::") == 2
        ), "Fully qualified resource type should have 3 components"
        provider_name, service_name, resource_name = resource_type.split("::")

        if provider_name == "AWS":
            doc_url = AWS_SERVICE_DOCUMENTATION_URLS.get(service_name)
        else:
            # TODO #165: need a new module naming scheme to differentiate top-level providers
            doc_url = OTHER_SERVICE_DOCUMENTATION_URLS.get(provider_name, {}).get(
                service_name
            )
            LOGGER.warning(
                "Skipping '%s' because we don't handle non-AWS providers yet",
                resource_type,
            )
            continue

        if not doc_url:
            LOGGER.error(
                "Skipping '%s' because we don't know how to document that service",
                resource_type,
            )
            continue

        # Ensure the service data exists
        service = services.setdefault(
            service_name,
            {
                "documentation": {"url": doc_url},
                "module_name": service_name.lower(),
                "name": service_name,
                "resources": {},
                "typing_imports": set(),
            },
        )

        # Avoid namespace clashes
        if service["module_name"] in ["lambda"]:
            service["module_name"] += "_"

        # Augment the resource data and add it to the service
        assert (
            resource_name not in service["resources"]
        ), "resource type is defined twice"
        service["resources"][resource_name] = resource_data

        resource_extra_attributes = RESOURCES_WITH_EXTRA_ATTRIBUTES.get(
            resource_type, []
        )
        assert not (
            set(resource_extra_attributes) - {"CreationPolicy", "UpdatePolicy"}
        ), "We have defined extra AWS attributes that we don't know what to do with yet"

        resource_data.update(
            {
                "friendly_name": inflection.titleize(resource_name),
                "has_creation_policy": "CreationPolicy" in resource_extra_attributes,
                "has_update_policy": "UpdatePolicy" in resource_extra_attributes,
                "type": {"fullname": resource_type},
            }
        )

        if resource_data["has_creation_policy"]:
            service["typing_imports"].update(["Any", "Dict"])
        if resource_data["has_update_policy"]:
            service["typing_imports"].update(["Any", "Dict"])

    # TODO collect property types in the same way
    # TODO verify that a property doesn't have the same name as a resource (nor an existing property)

    # Create a Python module for each AWS service, with a Python class for
    # each AWS resource type
    env = Environment(
        loader=FileSystemLoader(
            SCRIPTDIR
        )  # TODO put our template into a "standard" location for Jinja
    )
    raw_template = env.get_template("raw_module.py.jinja2")
    service_template = env.get_template("service_module.py.jinja2")

    for service_name, service in sorted(services.items()):
        if not service["documentation"]["url"]:
            LOGGER.warning(
                "Service %s does not have a documentation URL configured", service_name
            )

        # Create or update the "raw" python module
        raw_module_name = os.path.join(raw_dirname, service["module_name"] + ".py")
        with open(raw_module_name, "w") as fp:
            LOGGER.debug("Generating raw module %s.py", service["module_name"])

            rendered = raw_template.render(service=service)
            formatted = black.format_str(rendered, mode=BLACK_SETTINGS)
            fp.write(formatted)

        # Ensure that the "service" module exists, and pre-populate it with
        # the boilerplate if it doesn't
        service_module_name = os.path.join(
            service_dirname, service["module_name"] + ".py"
        )
        if not os.path.exists(service_module_name):
            with open(service_module_name, "w") as fp:
                LOGGER.debug("Generating service module %s.py", service["module_name"])
                rendered = service_template.render(service=service)
                formatted = black.format_str(rendered, mode=BLACK_SETTINGS)
                fp.write(formatted)


if __name__ == "__main__":
    logging.basicConfig()
    LOGGER.setLevel(logging.INFO)

    generate_modules()
