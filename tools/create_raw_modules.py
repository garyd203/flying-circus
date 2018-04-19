#!/usr/bin/env python

"""
Create the basic Python modules in the `_raw` package.

These are automatically generated from a JSON specification provided by Amazon.
"""

# TODO reference the AWS documentation at https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification-format.html
# TODO generate the modules and commit them

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
    # FIXME remove this temporary hack when we are satisfied wth the output
    "AutoScaling",
}

#: Lookup table of documentation URL's for AWS services. This information does
#: not appear to be in the specification, and is not always in a predictable
#: place
SERVICE_DOCUMENTATION_URLS = {
    # FIXME add more to here.
    # FIXME log warning if a module is missing
    "AutoScaling": "http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html",
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
def generate_raw_package(packagedir, specification):
    """Create the basic Python modules in the `_raw` package.

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
            "friendly_name": inflection.titleize(service_name),
            "name": service_name,
            "resources": {},
        })

        # Augment the resource data and add it to the service
        assert resource_name not in service["resources"], "resource type is defined twice"
        service["resources"][resource_name] = resource_data

        resource_data.update({
            "extra_aws_attributes": RESOURCES_WITH_EXTRA_ATTRIBUTES.get(resource_type, []),
            "friendly_name": inflection.titleize(resource_name),
            "type": {
                "fullname": resource_type,
            },
        })

        assert not set(resource_data["extra_aws_attributes"]).difference({"CreationPolicy", "UpdatePolicy"}), \
            "We have defined extra AWS attributes that are not handled by the class constructor in the Jinja template"

    # TODO collect property types in the same way

    # Create a Python module for each AWS service, with a Python class for
    # each AWS resource type
    env = Environment(
        loader=FileSystemLoader(SCRIPTDIR),
    )
    template = env.get_template('raw_module.py.jinja2')

    for service_name, service in sorted(services.items()):
        module_name = os.path.join(raw_dirname, service_name.lower() + ".py")
        with open(module_name, "w") as fp:
            LOGGER.debug("Generating module %s.py", service_name.lower())
            fp.write(template.render(service=service))

        # TODO check that there is a module in the `service` package with basic imports


if __name__ == '__main__':
    logging.basicConfig()
    LOGGER.setLevel(logging.DEBUG)

    generate_raw_package()
