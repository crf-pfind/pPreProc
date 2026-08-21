============================
Compatibility and validation
============================

Version matrix
==============

=======================  ==========  =======  =======  ========================
Application              Python SDK  C++ SDK  PFB/PFC  Status
=======================  ==========  =======  =======  ========================
No public release yet    1.0.x       1.0.x    v1       Current public interface
=======================  ==========  =======  =======  ========================

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

Validation record
=================

The synthetic fixture exercises direct access, scan lookup, parent-MS1
resolution, binary64 arrays, XIC extraction, full validation, CLI output, and
corruption handling in both SDK implementations.

A full decode of a current indexed output also validated 14,455 spectra,
3,498,412 peaks, and 11,477 parent links with no structural, boundary, or peak
count mismatch. That dataset is not distributed in the repository and does not
replace qualification of a future application archive.
