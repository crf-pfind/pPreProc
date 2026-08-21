=======================
Releases and versioning
=======================

Version domains
===============

pPreProc maintains separate versions for:

* the Windows application distributed through GitHub Releases;
* the Python and C++ SDKs, declared by their package and build metadata; and
* the PFB/PFC contract, represented by its versioned specification directory.

Compatibility between these surfaces is published in the compatibility
matrix. Equal version numbers do not imply that the surfaces share a release
cycle.

Application releases
====================

A public application Release contains a runnable ZIP, checksum, user-facing
release notes, application terms, and third-party notices. Source archives
generated automatically from a Git tag are not application packages.

Release notes use the following order: highlights, installation or upgrade,
compatibility, improvements, fixes, breaking changes, known issues, and
checksums. The historical ``v1.0.0`` tag establishes the initial public SDK and
format baseline; it is not a standalone application Release.

The first standalone package is ``2.5.2-rc.1`` for Windows x64. It is a
pre-release intended to validate installation and vendor-format workflows
before the stable ``2.5.2`` release.

Documentation versions
======================

``latest`` follows the main branch. Stable software tags may be activated in
Read the Docs after their builds pass. Readers should select documentation
matching the installed application or SDK version whenever that version is
available.

Support lifecycle
=================

Release candidates do not carry a long-term-support commitment. Support dates
and end-of-life status will be published with the first stable standalone
release.
