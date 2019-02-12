# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
* Update AWS Resource specification to v2.22.0

## [v0.6.0] - 2019-02-12
### Changed
* Added changelog
* Refactor AWSObject to use `attrs` for attribute access. The way you define
  an AWSObject subclass has changed (especially Resource classes).
* Remove install dependency on `boto3`
