===========
Quick start
===========

Validate a PFB/PFC pair
=======================

The repository includes a small synthetic fixture:

.. code-block:: console

   ppreproc-pfb info sdk/python/tests/fixtures/minimal.pfb
   ppreproc-pfb validate sdk/python/tests/fixtures/minimal.pfb --full

``validate --full`` decodes every record, checks PFB/PFC byte boundaries and
peak counts, and follows declared parent links.

Read a spectrum
===============

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       spectrum = reader.get_spectrum_by_scan(102)
       print(spectrum.scan_number, spectrum.peak_count)
       parent_ms1 = reader.get_parent_ms1(spectrum)

The reader selects the same-stem ``run.pfc`` companion automatically. Record
lookup uses the PFB footer index and does not decode earlier spectra.

Next steps
==========

* Follow :doc:`../user-guide/reading-pfb-pfc` for iteration, metadata-only
  access, parent lookup, and XIC extraction.
* Use :doc:`../reference/python-api` for the complete Python interface.
* Read :doc:`../reference/pfb-pfc-format` before implementing another reader.
