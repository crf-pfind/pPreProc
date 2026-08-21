======================
Working with PFB/PFC
======================

Open a pair
===========

``PFBReader("run.pfb")`` opens ``run.pfb`` and the same-stem ``run.pfc``. Pass
``pfc_path`` only when the companion uses a different path. The reader
validates the header, footer index, required PFC columns, record count, and scan
identifiers during construction.

Random access
=============

.. code-block:: python

   with PFBReader("run.pfb") as reader:
       by_ordinal = reader.get_spectrum(0)
       by_scan = reader.get_spectrum_by_scan("102")

Ordinals are zero based. ``ScanNo`` is a PFC identifier and does not need to
equal the ordinal.

Metadata-only access
====================

Set ``with_arrays=False`` when peak arrays are not needed:

.. code-block:: python

   for spectrum in reader.iter_spectra(with_arrays=False):
       print(spectrum.scan_number, spectrum.metadata["RetTime"])

Parent lookup
=============

``get_parent_ms1()`` follows ``PrecursorScan`` links until it reaches an MS1
record. Missing links, unknown scans, and cycles are reported as errors rather
than silently ignored.

Extract an XIC
==============

.. code-block:: python

   points = reader.extract_xic(
       target_mz=500.2,
       ppm=10,
       rt_start=0,
       rt_end=20,
       faims_cv=None,
   )

The result is a list of ``(retention_time, summed_intensity)`` pairs from MS1
records in the requested window.
