# Changelog

Notable changes to the public repository are recorded here. The application,
SDKs, and PFB/PFC format use independent versions.

## [Unreleased]

### Changed

- Reorganize the repository around distribution, SDK, interface, example, and
  documentation surfaces.
- Separate SDK and format version identifiers.
- Restructure the English and Chinese documentation by task and reference type.

### Added

- Define public repository scope, support channels, component licensing, and a
  release process for future application binaries.

## [2.5.2-rc.1] - 2026-08-21

### Added

- Package pPreProc as a standalone Windows x64 release candidate.
- Add an explicit application license, third-party component inventory,
  runtime provenance, file-level SHA-256 inventory, and archive checksum.
- Bundle only the pParse2+, pParse, pXtract, model, vendor-reader, and Microsoft
  runtime files required by the preprocessing workflow.

## [1.0.0] - 2026-08-21

### Added

- Publish the PFB/PFC v1 specification.
- Add dependency-free Python and C++17 reference readers.
- Add a validation CLI, synthetic fixture, tests, and bilingual documentation.

The `v1.0.0` tag establishes the first public SDK and format-interface
baseline. It is not a standalone Windows application release.
