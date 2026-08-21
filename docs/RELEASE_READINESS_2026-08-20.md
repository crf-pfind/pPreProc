# Release-readiness record — updated 2026-08-21

## Current recommended sequence

1. Publish the English and Simplified Chinese interface documentation through
   two linked Read the Docs projects.
2. Keep the historical `v1.0.0` interface-baseline tag unchanged and archive
   it separately for provenance if required.
3. Complete binary authorization, notices, checksums, and clean-machine tests.
4. Create a new GitHub software Release for the runnable Windows package, then
   enable the same tag as a stable Read the Docs version.

This sequence keeps the PFB/PFC interface inspectable online without treating
API files as software Release assets or representing an unreviewed vendor
runtime as open source.

## Checks completed

- Python reader: all 7 tests passed on Python 3.9.13, 3.10.0, and 3.14.3.
- Python package: isolated PEP 517 source-distribution and wheel builds passed;
  installation into a clean virtual environment followed by CLI validation of
  the synthetic fixture also passed.
- C++ reader: C++17 compilation passed with MinGW g++ 8.1.0 using
  `-Wall -Wextra -pedantic`; the synthetic reader/parent-link example passed.
- Real indexed output: full decode passed for 14,455 spectra, 3,498,412 peaks,
  and 11,477 parent links without an indexed-layout or PFC-boundary mismatch.
- Runtime manifest: every required entry resolved in the inspected pFind 3.2.3
  installation; unrelated pFind search/reporting programs are not whitelisted.
- Windows wrapper: version reporting and a manifest-backed dry run passed.
- Repository validation: zero errors. The Windows binary gate
  remains independent and stops at the unresolved items listed below.

Local CMake execution was not available on the audit machine. The CMake/CTest
configuration is included in CI, while the same C++ source was compiled and run
directly during the local audit.

## Historical interface-baseline decisions

- The original reader, specification, tests, and release-tool source is
  approved under BSD-3-Clause.
- The canonical repository is `https://github.com/crf-pfind/pPreProc`.
- `CITATION.cff` follows the manuscript author order; no unconfirmed ORCID
  identifiers are included.
- Version 1.0.0 uses the public release date 2026-08-21.

The remaining historical follow-up is to archive the exact public tag with
Zenodo and add its version DOI. Current API and format material is maintained
through the bilingual online documentation.

## Decisions required for the Windows runtime asset

- Review and, where appropriate, extract the historical pParse2, pParse2+, and
  pXtract application projects now available in the pFind 3.2.3 development
  tree. Their presence supersedes the earlier source-location finding but does
  not resolve third-party SDK or redistribution requirements.
- Confirm authority to redistribute the pFind-owned compiled pParse,
  pParse2+, pXtract, model, and configuration files independently of pFind.
- Confirm whether the extracted components retain a pFind activation,
  license-file, or expiration dependency and document the observed behavior.
- Supply or approve the exact vendor/runtime terms and notices enumerated in
  `RUNTIME_DEPENDENCY_AUDIT.md` and `third_party/`.
- Choose an official installer/bootstrap dependency when direct vendor-library
  redistribution is not explicitly permitted.
- Run the final ZIP on a clean Windows machine and retain the test record.

## Standards used

- Read the Docs for bilingual, versioned API and format documentation.
- GitHub Releases for runnable, tagged software packages and checksums.
- Citation File Format 1.2.0 for machine-readable software citation metadata.
- Semantic Versioning for the software version.
- SPDX/PEP 639 license expressions in Python package metadata after approval.
- A repository-level license plus component-specific third-party notices and
  exact license texts for any redistributed binary asset.
