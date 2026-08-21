# Release model

pPreProc uses one repository and two explicitly distinguished deliverables.
This keeps the PFB/PFC interface inspectable while preventing an unreviewed
binary dependency from being mistaken for open-source application code.

## 1. Source tag

The Git tag contains:

- the normative indexed PFB/PFC v1 specification;
- the original Python and header-only C++17 reader source;
- the validator, synthetic fixture, unit tests, and CI configuration;
- the standalone command wrappers, runtime manifest, and release builder; and
- documentation, citation metadata, and release records.

It does not contain pFind search/reporting programs, vendor binaries, or the
compiled pParse/pParse2+/pXtract runtime. The source tag can be published once
the repository license, permanent URL, authorship metadata, and source checks
are approved.

## 2. Windows runtime asset

The optional Windows ZIP is built from an authorized pFind runtime by the
explicit whitelist in `runtime-manifest.json`. It contains the user-facing
pPreProc entry point and the compiled components required by the validated
workflow, but excludes the pFind search engine, GUI, reporting tools, logs,
debug artifacts, and unrelated utilities.

The ZIP is a release asset, not a claim that the application implementation is
open source. Publication additionally requires project-owner authorization,
exact third-party notices and license texts, checksums, and validation on a
clean Windows machine. If a vendor library may not be redistributed, the asset
must use that vendor's official installer or bootstrap procedure instead.

## 3. Versioning and citation

The source tag and a matching Windows asset use the same pPreProc version. A
release must identify which asset was used, and analyses should record the tag,
platform, input format, command/configuration, and checksum. After archival,
the version DOI should be cited together with the associated article.

## 4. Wording used in documentation and the manuscript

- **Open/source-visible:** the PFB/PFC specification, Python/C++ readers,
  fixtures, tests, and release tooling in the repository.
- **Standalone distribution:** the repository plus an authorized Windows
  runtime asset that runs independently of the pFind search engine and GUI.
- **Not claimed:** that the compiled Windows application is fully open source,
  that every vendor-native metadata attribute is preserved, or that every
  third-party search engine reads PFB/PFC without an adapter.
