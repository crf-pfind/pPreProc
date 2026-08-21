=========================
PFB/PFC v1 file format
=========================

Status
======

PFB/PFC v1 is a paired, indexed representation:

* ``name.pfb`` stores spectrum properties, m/z arrays, intensity arrays, and a
  footer index.
* ``name.pfc`` stores the corresponding tab-delimited metadata.

The ordinal of a PFB record, footer entry, and PFC data row refers to the same
spectrum. Public API ordinals are zero based. ``ScanNo`` is an identifier and
does not need to equal the ordinal.

Primitive types
===============

All numeric fields are little-endian.

=================  ====================================  ========
Name               Encoding                              Size
=================  ====================================  ========
``int32``          signed two's-complement integer       4 bytes
``uint32``         unsigned integer                      4 bytes
``uint64``         unsigned integer                      8 bytes
``binary64``       IEEE 754 double-precision float       8 bytes
=================  ====================================  ========

The m/z and intensity arrays use ``binary64``. PFB itself performs no decimal
rounding, quantization, or lossy recompression.

PFB layout
==========

Header
------

The fixed header occupies 24 bytes.

======  ==========  ==================  ===================================
Offset  Type        Field               v1 meaning
======  ==========  ==================  ===================================
0       ``int32``   ``reserved_1``      reserved
4       ``int32``   ``reserved_2``      reserved
8       ``int32``   ``reserved_3``      reserved
12      ``uint64``  ``index_address``   absolute footer-index offset
20      ``int32``   ``spectrum_count``  number of records and PFC data rows
======  ==========  ==================  ===================================

Spectrum record
---------------

Each record contains, in order:

#. ``uint32 property_byte_count``;
#. that many UTF-8 property bytes;
#. ``uint32 peak_count``;
#. ``peak_count`` m/z values as ``binary64``;
#. ``peak_count`` intensity values as ``binary64``.

No alignment padding is defined between records.

Footer index
------------

At ``index_address`` the file contains exactly ``spectrum_count`` ``uint64``
offsets. Entry *i* points directly to record *i*. Offsets must be strictly
increasing, the first must be 24, and the last record must end exactly at
``index_address``. This is what allows a reader to retrieve a spectrum without
decoding the records before it.

PFC metadata
============

PFC is UTF-8 tab-delimited text with one header and one data row per spectrum.
Readers select fields by name and tolerate extra columns. The v1 core fields
are:

* identity and linkage: ``ScanNo``, ``PrecursorScan``;
* acquisition context: ``RetTime``, ``SpectrumType``, ``InstrumentType``,
  ``IonInjectionTime``;
* activation and precursor data: ``activationType``, ``activationCenter``,
  ``NCE``, ``monoIsotopicMz``, ``upperCharge``, ``lowerCharge``, and
  ``activationWindow``;
* cross-file integrity: ``NumberofPeaks``, ``StartPos``, and ``EndPos``.

``ScanNo`` must be present and unique. The three integrity fields must agree
with the matching PFB record and footer.

Fidelity boundary
=================

PFB preserves the m/z and intensity values supplied to the writer as
double-precision values. PFC intentionally retains the metadata required by
the validated preprocessing and fast-access workflows; it is not a complete
serialization of every vendor-specific attribute. A workflow that requires an
unlisted native identifier, ion-mobility coordinate, or other vendor field
must retain and consult the source data.

Compatibility and validation
============================

A conforming reader rejects invalid header/index bounds, inconsistent record
sizes, missing core PFC columns, duplicate scan identifiers, row-count
mismatches, and inconsistent peak counts or byte boundaries. Older PFB files
without a valid v1 footer index are not silently guessed as v1.

The complete normative wording is maintained in the repository's
`PFB/PFC v1 specification <https://github.com/crf-pfind/pPreProc/blob/main/docs/PFB_PFC_SPECIFICATION_V1.md>`_.
