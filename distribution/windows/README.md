# Windows distribution

This directory contains the public packaging metadata for the proprietary
pPreProc Windows application. Application binaries and vendor runtimes are not
stored in Git.

The package builder reads `runtime-manifest.json`, copies only the listed
runtime files from an authorized installation, adds the launchers and required
notices, and generates SHA-256 checksums. It deliberately excludes pFind search,
reporting, and graphical applications.

A public archive must include:

- `ppreproc.cmd` and `ppreproc.ps1`;
- the selected application runtime;
- an application `VERSION` file;
- approved application terms, the public-component license, `NOTICE`, and all
  applicable third-party notices;
- `runtime-manifest.json`; and
- `SHA256SUMS.txt`.

The source repository's BSD-3-Clause license does not by itself authorize
redistribution of the separately supplied application or third-party binaries.
Release maintainers must follow `.github/RELEASING.md`.
