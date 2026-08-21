# pPreProc 1.0.0

Released 2026-08-21 under the BSD-3-Clause license.

This is the first versioned pPreProc release separated from the pFind suite.
The source tag publishes the supported PFB/PFC interface and release tooling.
An independently runnable Windows preprocessing ZIP may be attached as a
separately qualified asset after redistribution and clean-machine checks.

## Highlights

- Unified Windows command entry point for a vendor input file or pParse2+ YAML
  configuration.
- Versioned specification for indexed PFB/PFC v1.
- Dependency-free Python reader with direct spectrum, scan, parent-MS1, XIC,
  and validation operations.
- Header-only C++17 reader with direct spectrum, scan, and parent-MS1 access.
- Synthetic test fixture, Python unit tests, C++ example, and CI workflow.
- Explicit compatibility boundary for historical unindexed PFB files.
- SHA-256 file manifest, `CITATION.cff`, changelog, security policy, and release
  checklist.

## Validated scope

The current pParse2+ analytical workflow is validated for DDA, including
conventional DDA, FAIMS-DDA, and dda-PASEF. Indexed PFB/PFC storage is not tied
to a DDA precursor model, but DIA-specific pParse processing is not claimed as
validated in this release.

The reference reader completed a full decode of a current 14,455-spectrum
indexed PFB/PFC pair (3,498,412 peaks and 11,477 parent links) without a format
or linkage error. See `VALIDATION.md`.

## Known limits

- PFC contains the metadata declared by the validated workflow, not every
  vendor-native attribute.
- Historical unindexed PFB files must be regenerated or migrated; the v1 reader
  rejects them.
- Peak arrays use uncompressed binary64 values in v1.
- DIA-specific pParse support and broader real-time validation remain future
  work.

## Release assets and archival

This release publishes the source tag only. The Zenodo version DOI will be
added after archival. A Windows ZIP and its SHA-256 digest may be attached only
after all runtime redistribution rights and clean-machine checks are complete.
