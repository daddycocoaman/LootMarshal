# Changelog
All notable changes to this project will be documented in this file.


## [0.3.0] - 2020-07-12
### Added
- Added logging with loguru library.
- Added search ability for secret tags metadata.
- Added ability to upload `creds binparse` and `creds lsass` to Azure fileclient.
- Added setting to specify number of workers for uvicorn. More than one worker is not currently possible on Windows. [Github Issue](https://github.com/encode/uvicorn/issues/514)
- Self-signed certs will be generated on startup if they don't exist in locations configured in settings.

### Changed
- Renamed `lootmarshal.py` to `lm.py` to avoid unintentional import clashes.
- Changed `secret` endpoint to `secrets` for consistency.

### Removed
- `/tags` endpoint removed.


## [0.2.0] - 2020-06-28
### Added
- Implemented Azure Files Storage class. 
- Added ability to add tag metadata to secrets.
- Added `cred binparse` to CLI. This module will parse binary files for a preset list of filters held in [CredParser.py](./lootmarshal/server/misc/credparser.py).

### Added - Server
- Self-signed certificate for SSL.

### Changed - Server
- Standardize parameter for endpoints that accept files to be `upload_file`.  