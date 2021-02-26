
# Change Log
All notable changes to this project will be documented in this file.
 
## [0.6.3] - 2021-02-25
HTML5 datetime picker, README.
 
### Added
- CHANGELOG.md
- [DateTimeInput](https://github.com/adammbaker/ristra/commit/a92a4181414df0e1bccb63d5c0b352d6d9109cd7#diff-13377425408f910e06076c111c2b3a4e9dc1e3e8d107713a6fd7434f674ff5a9)
  DateTimeInput - The old DateTimePickerInput was defunct. The new picker uses the built-in HTML5 Date/Time input types.
- [intake/models.py](https://github.com/adammbaker/ristra/commit/bac44c3f0f5799ad0ce100901a21c097c1c9f994)
  Added user capability flags
 
### Changed
- [README](https://github.com/adammbaker/ristra/commit/716e34f8615a7e588fb308f5fe47a372210a960a)
  Updated README.md to reflect changes to Ristra.
- [intake/migrations/000\[12\]*.py](https://github.com/adammbaker/ristra/commit/65f8f5e95f35b7257f42b512c95f6f42c39368ea)
  Changed the migration files to hopefully be future-proof.

### Fixed
- [intake/models.py](https://github.com/adammbaker/ristra/commit/6afc1bb408a4662d096a72350b154382d3089da3)
  Fixed breadcrumbs for Medical; missing @property
  
## [0.6.2] - 2021-02-24
  
Updated last few forms, getting ready for presentation to the Thursday group.
 
### Changed
Updated Medical model to include new encrypted fields. Updated TravelForm models as well.