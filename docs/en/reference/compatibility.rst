=============
Compatibility
=============

Versioning
==========

The Windows application, PFB/PFC SDKs, and PFB/PFC format are versioned
independently. Use the combinations listed below. ``latest`` documentation
follows the main branch; select versioned documentation when it is available
for an installed release.

Version matrix
==============

=======================  ==========  =======  =======  =========================
Application              Python SDK  C++ SDK  PFB/PFC  Status
=======================  ==========  =======  =======  =========================
2.5.2                    1.0.x       1.0.x    v1       Stable Windows release
=======================  ==========  =======  =======  =========================

SDK 1.x reads indexed files satisfying the v1 specification. Readers accept
additional PFC columns, while existing v1 field meanings and units remain
stable. An incompatible byte layout or field-semantics change requires a new
format version.

Legacy PFB files
================

Historical streaming PFB files may not contain the v1 footer index. The SDKs
reject them instead of scanning the file and presenting the result as indexed
v1 access. Regenerate those files from retained source data with a compatible
writer.
