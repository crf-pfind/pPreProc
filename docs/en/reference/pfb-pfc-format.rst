=====================
PFB/PFC v1 reference
=====================

PFB/PFC v1 is a paired, indexed representation. ``name.pfb`` stores spectrum
records and a footer index; ``name.pfc`` stores the corresponding
tab-delimited metadata. Record, footer, and PFC row ordinals refer to the same
spectrum.

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

PFB layout
==========

The fixed header occupies 24 bytes:

======  ==========  ==================  ===================================
Offset  Type        Field               v1 meaning
======  ==========  ==================  ===================================
0       ``int32``   ``reserved_1``      reserved
4       ``int32``   ``reserved_2``      reserved
8       ``int32``   ``reserved_3``      reserved
12      ``uint64``  ``index_address``   absolute footer-index offset
20      ``int32``   ``spectrum_count``  record and PFC-row count
======  ==========  ==================  ===================================

Each spectrum record contains a ``uint32`` property-byte count, UTF-8 property
bytes, a ``uint32`` peak count, ``peak_count`` binary64 m/z values, and the same
number of binary64 intensity values. No alignment padding is defined.

At ``index_address``, the footer contains exactly ``spectrum_count`` ``uint64``
absolute record offsets. The first offset is 24, offsets are strictly
increasing, and the final record ends at ``index_address``.

PFC core fields
===============

PFC is UTF-8 tab-delimited text with one header and one row per spectrum.
Readers select fields by name and accept additional columns. v1 requires:

* identity and linkage: ``ScanNo``, ``PrecursorScan``;
* acquisition context: ``RetTime``, ``SpectrumType``, ``InstrumentType``,
  ``IonInjectionTime``;
* activation and precursor data: ``activationType``, ``activationCenter``,
  ``NCE``, ``monoIsotopicMz``, ``upperCharge``, ``lowerCharge``, and
  ``activationWindow``; and
* integrity fields: ``NumberofPeaks``, ``StartPos``, and ``EndPos``.

``ScanNo`` is non-empty and unique. The integrity fields agree with the PFB
record and footer.

Normative specification
=======================

The complete normative contract, including validation requirements and field
units, is maintained in
`interfaces/pfb-pfc/v1/specification.md <https://github.com/crf-pfind/pPreProc/blob/main/interfaces/pfb-pfc/v1/specification.md>`_.
