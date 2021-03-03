
# Change Log
All notable changes to this project will be documented in this file.

## [0.7.1] - 2021-03-02

### Added
- Reports - Added more reports
  - Active Households
  - Active Asylees
  - At-A-Glance
  - Households in Motion

### Changed
- IntakeBus -
  Now takes you to IntakeBus overview instead of detail

## [0.7.0] - 2021-03-01

### Added
- Reports - 
  Reports are dynamically-generated updates of critical information. It is intended to be used be used by Site Coordinators to keep an eye on their organization.
 
### Changed
- [Templates] (https://github.com/adammbaker/ristra/commit/d7b60dacd77658ba493924a75075e785195f5c8f)
  Rearranged the Update and Delete model buttons to avoid them being accidentally invoked.
- [User profile] (https://github.com/adammbaker/ristra/commit/6d012608a762107e7ce54364187228654b561463)
  Changed the user's capacities selection to checkboxes.

### Fixed
- [Models] (https://github.com/adammbaker/ristra/commit/345dc9ae92cfc38ab39a0978b3f1186848dfefef#diff-2b8788fe07dd603a3b6ee130f6ab32e676ee82c24c3a63497e2ea41664d127e1)
  Removed requirement for Lodging to be specified during Head of Household intake.
 
## [0.6.4] - 2021-02-28

### Added
- [Card test](https://github.com/adammbaker/ristra/commit/dbccee7c0458975a595281be29b4122963b3cde7#diff-100f5cc8a43b048b6d0b681a121803f37e4db8910d96e2704cb5dbe97d19a25f)
  Added a card test view for debug/design purposes
- Models - 
  Models now have Update and Delete views as well as descriptive detail and curt overview views.
- Itinerary - 
  Heads of Household that have TravelPlans associated with them have a printable itinerary.
 
### Changed
- Templates - 
  Templates are a lot more reusable and flexible. I've switched from one view to several views with templates that you can plug-and-play. This reduces complexity of generic views and also more closely aligns with how generic views should be integrated.

### Fixed
- [intake/models.py](https://github.com/adammbaker/ristra/commit/f007565b8b23e471c853834eb2690e6aae929518)
  A field in Medical was fixed to accurately reflect its field name; copy-and-paste issue
- [Typo](https://github.com/adammbaker/ristra/commit/dbccee7c0458975a595281be29b4122963b3cde7#diff-f216c3e9acfe834e1af705b9fae4e7fd9e1fd4a3d9710d952dd9596214379806)
  There was a typo in the footer. How embarassing.
- [intake/models.py](https://github.com/adammbaker/ristra/commit/dbccee7c0458975a595281be29b4122963b3cde7#diff-2b8788fe07dd603a3b6ee130f6ab32e676ee82c24c3a63497e2ea41664d127e1)
  Fixed the breadcrumbs to allow for Overview views instead of DetailViews
 
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