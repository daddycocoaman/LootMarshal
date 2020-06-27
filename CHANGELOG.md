# Changelog
All notable changes to this project will be documented in this file.


## [0.2.0] - 2020-06-28
### Added
- Implemented Azure Files Storage class. 
- Added ability to add tag metadata to secrets.
- Added `cred binparse` to CLI. This module will parse binary files for a preset list of filters held in [CredParser.py](./lootmarshal/server/misc/credparser.py).

### Added - Server
- Self-signed certificate for SSL.

### Changed - Server
- Standardize parameter for endpoints that accept files to be `upload_file`.  