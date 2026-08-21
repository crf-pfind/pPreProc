# Third-party release evidence

This directory contains the reviewed component inventory, consolidated
notices, and license texts used by the Windows package builder. Application
and vendor binaries are not committed here.

When a runtime component changes, update all three of:

1. `../runtime-manifest.json`;
2. `third-party-components.json`; and
3. `THIRD_PARTY_NOTICES.txt` and any affected file in `licenses/`.

The package builder stops when this evidence is absent. Each built archive
also contains `RUNTIME_INVENTORY.json` with file-level versions and SHA-256
digests.
