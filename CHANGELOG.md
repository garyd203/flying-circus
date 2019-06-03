# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
* Update AWS Resource specification to v3.3.0
* Utilities to create inline AWS Lambda functions

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