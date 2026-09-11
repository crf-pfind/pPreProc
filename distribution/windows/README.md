# Windows distribution

This directory contains the Windows package definition. Application binaries
and vendor runtimes are not stored in Git.

The package builder copies the required runtime files into `bin`, alongside a
single launcher, a short readme, and one consolidated license file. pFind
search, reporting, and graphical applications are not included.

A public archive contains only:

- `pPreProc.cmd`;
- the selected application runtime in `bin/`;
- `README.txt`;
- `LICENSE.txt` containing the application terms and required third-party
  notices.

Runtime manifests and component records remain in this repository for release
maintenance; they are not included in the user archive. Release maintainers
must follow `.github/RELEASING.md`.
