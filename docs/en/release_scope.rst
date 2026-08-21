Documentation and release scope
===============================

The project publishes two different surfaces, and they should not be
conflated.

Online documentation
====================

This Read the Docs site is the canonical, continuously maintained location for:

* the PFB/PFC format contract and compatibility boundary;
* Python and C++ interface reference;
* CLI and integration examples; and
* architecture, validation, and application guidance.

The documentation is built from the repository and versioned with future
software tags. API pages and specification files are not attached to a GitHub
Release as a second product.

GitHub software releases
========================

A GitHub Release is reserved for a runnable pPreProc application package. A
public Windows package must include the intended pPreProc entry point, only the
required runtime components, applicable third-party notices and license texts,
checksums, and a clean-machine validation record.

The package must not imply that compiled pParse/pParse2+/pXtract application
implementations are open source. It also must not bundle unrelated pFind
search, GUI, and reporting programs.

Versioning
==========

``latest`` tracks the documentation on the main branch. Beginning with the
next software tag that contains this Sphinx configuration, Read the Docs can
also expose stable, version-specific documentation. The historical
``v1.0.0`` tag predates the documentation site and should remain inactive in
Read the Docs rather than being rewritten.

Citation
========

Analyses should record the pPreProc software version, platform, input format,
command/configuration, and artifact checksum. Once a release is archived, use
the version DOI in addition to the associated article.
