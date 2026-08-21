# Windows distribution

This directory contains the public packaging metadata for the proprietary
pPreProc Windows application. Application binaries and vendor runtimes are not
stored in Git.

The package builder reads `runtime-manifest.json`, copies only the listed
runtime files from the project-approved pFind 3.2.3 runtime and the licensed
Microsoft x64 Redistributable directory, adds the launchers and notices, and
generates SHA-256 checksums. It deliberately excludes pFind search, reporting,
and graphical applications.

A public archive must include:

- `ppreproc.cmd` and `ppreproc.ps1`;
- the selected application runtime;
- an application `VERSION` file;
- application terms, the public-component license, and third-party notices;
- `runtime-manifest.json`;
- `runtime-provenance.json` and `RUNTIME_INVENTORY.json`; and
- `SHA256SUMS.txt`.

The approved application terms, component inventory, and third-party notices
are maintained in this directory. When a runtime changes, update
`runtime-manifest.json`, `third-party/third-party-components.json`, and the
affected notices or license texts before rebuilding. Release maintainers must
follow `.github/RELEASING.md`.
