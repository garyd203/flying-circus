#!/usr/bin/env python

"""
Create the basic Python modules in the `_raw` package.

These are automatically generated from a JSON specification provided by Amazon,
which is documented at https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification-format.html
"""

import json
import logging
import os.path

import click
import inflection
from jinja2 import FileSystemLoader, Environment

LOGGER = logging.getLogger(
    os.path.splitext(os.path.basename(__file__))[0]
)

#: Set of AWS service names that we create Flying Circus modules for.
#: At the moment we only include some modules because we are still building
#: up our script
SUPPORTED_AWS_SERVICES = {
    # FIXME remove this temporary hack when we are satisfied with the output
    "AutoScaling",
    "CloudFront",
    "CloudTrail",
    "CloudWatch",
    "Cognito",
    "EC2",
    "ECR",
    "ECS",
    "KMS",
    "RDS",
    "S3",
    "SecretsManager",
    "SNS",
}

#: Lookup table of documentation URL's for AWS services. This information does
#: not appear to be in the specification, and does not have a deterministic URL.
SERVICE_DOCUMENTATION_URLS = {
    "AutoScaling": "http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html",
    "CloudFront": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html",
    "CloudTrail": "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html",
    "CloudWatch": "http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html",
    "Cognito": "https://docs.aws.amazon.com/cognito/latest/developerguide/index.html",
    "EC2": "http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/",
    "ECR": "https://docs.aws.amazon.com/AmazonECR/latest/userguide/index.html",
    "ECS": "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/index.html",
    "KMS": "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html",
    "RDS": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/index.html",
    "S3": "https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html",
    "SecretsManager": "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html",
    "SNS": "https://docs.aws.amazon.com/sns/latest/dg/welcome.html",
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
    "AWS::Lambda::Alias": ["UpdatePolicy"],
}

#: The directory where this script lives
SCRIPTDIR = os.path.dirname(__file__)


@click.command()
@click.argument("packagedir",
                metavar="FCPACKAGE",
                type=click.Path(exists=True, file_okay=False),
                required=True,
                )
@click.option("--specification", "-s",
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
    assert os.path.isdir(service_dirname), "The 'flyingcircus.service' package does not exist"

    # Load data as a python dictionary
    with open(specification, "r") as fp:
        all_data = json.load(fp)

    assert set(all_data.keys()) == {"PropertyTypes", "ResourceSpecificationVersion", "ResourceTypes"}, \
        "Found an unknown top-level key"

    # Group the data by AWS service and calculate additional data
    services = {}

    for resource_type, resource_data in all_data["ResourceTypes"].items():
        # Break down the resource type
        assert resource_type.count("::") == 2, "Fully qualified resource type should have 3 components"
        provider_name, service_name, resource_name = resource_type.split("::")
        assert provider_name == "AWS", "Resource provider is expected to be AWS"

        if service_name not in SUPPORTED_AWS_SERVICES:
            LOGGER.info("Skipping '%s' because we don't yet support that service", resource_type)
            continue

        # Ensure the service data exists
        service = services.setdefault(service_name, {
            "documentation": {
                "url": SERVICE_DOCUMENTATION_URLS.get(service_name)
            },
            "module_name": service_name.lower(),
            "name": service_name,
            "resources": {},
            "typing_imports": set(),
        })

        # Augment the resource data and add it to the service
        assert resource_name not in service["resources"], "resource type is defined twice"
        service["resources"][resource_name] = resource_data

        resource_extra_attributes = RESOURCES_WITH_EXTRA_ATTRIBUTES.get(resource_type, [])
        assert not (set(resource_extra_attributes) - {"CreationPolicy", "UpdatePolicy"}), \
            "We have defined extra AWS attributes that we don't know what to do with yet"

        resource_data.update({
            "friendly_name": inflection.titleize(resource_name),
            "has_create_policy": "CreatePolicy" in resource_extra_attributes,
            "has_update_policy": "UpdatePolicy" in resource_extra_attributes,
            "type": {
                "fullname": resource_type,
            },
        })

        if resource_data["has_create_policy"]:
            service["typing_imports"].update(["Any", "Dict"])
        if resource_data["has_update_policy"]:
            service["typing_imports"].update(["Any", "Dict"])

    # TODO collect property types in the same way
    # TODO verify that a property doesn't have the same name as a resource (nor an existing property)

    # Create a Python module for each AWS service, with a Python class for
    # each AWS resource type
    env = Environment(
        loader=FileSystemLoader(SCRIPTDIR),  # TODO put our template into a "standard" location for Jinja
    )
    raw_template = env.get_template('raw_module.py.jinja2')
    service_template = env.get_template('service_module.py.jinja2')

    for service_name, service in sorted(services.items()):
        if not service["documentation"]["url"]:
            LOGGER.warning("Service %s does not have a documentation URL configured", service_name)

        # Create or update the "raw" python module
        raw_module_name = os.path.join(raw_dirname, service["module_name"] + ".py")
        with open(raw_module_name, "w") as fp:
            LOGGER.debug("Generating raw module %s.py", service_name.lower())
            fp.write(raw_template.render(service=service))

        # Ensure that the "service" module exists, and pre-populate it with
        # the boilerplate if it doesn't
        service_module_name = os.path.join(service_dirname, service["module_name"] + ".py")
        if not os.path.exists(service_module_name):
            with open(service_module_name, "w") as fp:
                LOGGER.debug("Generating service module %s.py", service_name.lower())
                fp.write(service_template.render(service=service))


if __name__ == '__main__':
    logging.basicConfig()
    LOGGER.setLevel(logging.DEBUG)

    generate_modules()
