# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
* Officially support Python 3.8
* Update libraries: [attrs](https://pypi.org/project/attrs/19.3.0/)

## [v0.7.3] - 2020-01-13
### Changed
* Update AWS Resource specification to v10.2.0

## [v0.7.2] - 2019-11-05
### Changed
* Update AWS Resource specification to v7.1.0
* Use [poetry](https://poetry.eustace.io/) for package management

## [v0.7.1] - 2019-10-01
### Changed
* Update AWS Resource specification to v6.2.0

## [v0.7.0] - 2019-08-06
### Changed
* Update AWS Resource specification to v4.3.0
* Build and release with [Azure Pipelines](https://dev.azure.com/garyd203/flying-circus/_build/)

### Security
* Upgrade to PyYAML v5.1 from v3.13. This addresses
  [CVE-2017-18342](https://security-tracker.debian.org/tracker/CVE-2017-18342),
  which was documented in [PyYAML bug 207](https://github.com/yaml/pyyaml/issues/207).
  Note that this bug **did not** affect Flying Circus, because YAML is only
  dump'ed, and hence there was no unsafe use of `yaml.load` with an untrusted
  source)
* Upgrade to Jinja2 v2.10.1 from v2.10. This addresses
  [CVE-2019-10906](https://nvd.nist.gov/vuln/detail/CVE-2019-10906). Note that
  this bug **did not** affect Flying Circus users, because Jinja2 was only
  used in an internal tool.

## [v0.6.6] - 2019-07-11
### Changed
* Update AWS Resource specification to v4.1.0

## [v0.6.5] - 2019-06-05
### Changed
* Support equals for ImportValue

## [v0.6.4] - 2019-06-04
### Changed
* Update AWS Resource specification to v3.3.0
* Utilities to create inline AWS Lambda functions
* Support equals for GetAtt

## [v0.6.3] - 2019-03-14
### Changed
* Python packaging changes only.

## [v0.6.2] - 2019-03-14
### Changed
* Create some introductory documentation
* Update AWS Resource specification to v2.25.0
* Create classes for all AWS services
* [#171](https://github.com/garyd203/flying-circus/issues/171): Support
  `UpdateReplacePolicy` and introduce `is_retained` property for a resource.

## [v0.6.1] - 2019-02-12
### Changed
* Update AWS Resource specification to v2.22.0

## [v0.6.0] - 2019-02-12
### Changed
* Added changelog
* Refactor AWSObject to use `attrs` for attribute access. The way you define
  an AWSObject subclass has changed (especially Resource classes).
* Remove installation dependency on `boto3`
* Hide code from original proof-of-concept implementation (`fcspike`) so that
  it is not part of a standard installation.