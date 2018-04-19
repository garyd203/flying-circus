#!/usr/bin/env python

"""
Create the basic Python modules in the `_raw` package.

These are automatically generated from a JSON specification provided by Amazon.
"""
# TODO reference the AWS documentation at https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-resource-specification-format.html

import json
import logging
import os.path
import sys

import inflection
from jinja2 import FileSystemLoader, Environment

LOGGER = logging.getLogger(
    os.path.splitext(os.path.basename(__file__))[0]
)

#: Set of AWS service names that we create Flying Circus modules for.
#: At the moment we only include some modules because we are still building
#: up our script
SUPPORTED_SERVICES = {
    "AutoScaling",
}

#: Lookup table of documentation URL's for AWS services. This information does
#: not appear to be in the specification, and is not always in a predictable
#: place
SERVICE_DOCUMENTATION_URL = {
    "AutoScaling": "http://docs.aws.amazon.com/autoscaling/latest/userguide/WhatIsAutoScaling.html",
}


def parse_specification(specfile, outputdir):
    # Check inputs
    os.makedirs(outputdir, exist_ok=True)

    # TODO Ensure the directory is a Python package

    # Load data as a python dictionary
    with open(specfile, "r") as fp:
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

        if service_name not in SUPPORTED_SERVICES:
            LOGGER.info("Skipping '%s' because we don't yet support that service", resource_type)
            continue

        # Ensure the service data exists
        service = services.setdefault(service_name, {
            "documentation": {
                "url": SERVICE_DOCUMENTATION_URL.get(service_name)
            },
            "friendly_name": inflection.titleize(service_name),
            "name": service_name,
            "resources": {},
        })

        # Augment the resource data and add it to the service
        assert resource_name not in service["resources"], "resource type is defined twice"
        service["resources"][resource_name] = resource_data

        resource_data.update({
            # TODO set a field for the few resoruces that have specal AWS attributes
            "friendly_name": inflection.titleize(resource_name),
            "type": {
                "fullname": resource_type,
            },
        })

    # TODO collect property types in the same way

    # Create a Python module for each AWS service, with a Python class for
    # each AWS resource type
    env = Environment(
        loader=FileSystemLoader("."),
    )
    template = env.get_template('raw_module.py.jinja2')

    for service_name, service in sorted(services.items()):
        module_name = os.path.join(outputdir, service_name.lower() + ".py")
        with open(module_name, "w") as fp:
            fp.write(template.render(service=service))


if __name__ == '__main__':
    # TODO use a real arg parser
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)

    specfile = sys.argv[1]
    outputdir = sys.argv[2]

    parse_specification(specfile, outputdir)
