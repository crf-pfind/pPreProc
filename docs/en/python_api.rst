====================
Python API reference
====================

The public package is ``ppreproc_pfb``. The supported public names are
``PFBReader``, ``PFBRecord``, and ``PFBFormatError``.

Typical use
===========

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       first = reader.get_spectrum(0)
       selected = reader.get_spectrum_by_scan("102")
       parent = reader.get_parent_ms1(selected)

       for spectrum in reader.iter_spectra(with_arrays=False):
           print(spectrum.index, spectrum.scan_number)

       xic = reader.extract_xic(
           target_mz=500.2,
           ppm=10,
           rt_start=0,
           rt_end=20,
       )

Direct retrieval uses the PFB footer index and does not decode preceding
records. Set ``with_arrays=False`` when only properties and PFC metadata are
required.

Public classes
==============

.. autoclass:: ppreproc_pfb.PFBReader
   :members:
   :special-members: __len__, __iter__
   :exclude-members: __weakref__

.. autoclass:: ppreproc_pfb.PFBRecord
   :members:

.. autoclass:: ppreproc_pfb.PFBFormatError

Errors
======

Malformed or structurally incompatible files raise ``PFBFormatError``.
Unknown record indexes raise ``IndexError`` and unknown scan identifiers raise
``KeyError``. Applications should not suppress ``PFBFormatError`` and continue
as though the pair were valid.
