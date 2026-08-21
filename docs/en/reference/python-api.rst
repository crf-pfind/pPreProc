====================
Python SDK reference
====================

The public package is ``ppreproc_pfb``. Its supported public names are
``PFBReader``, ``PFBRecord``, and ``PFBFormatError``.

Usage example
=============

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       first = reader.get_spectrum(0)
       selected = reader.get_spectrum_by_scan("102")
       parent = reader.get_parent_ms1(selected)
       metadata = list(reader.iter_spectra(with_arrays=False))

API
===

.. autoclass:: ppreproc_pfb.PFBReader
   :members:
   :special-members: __len__, __iter__
   :exclude-members: __weakref__

.. autoclass:: ppreproc_pfb.PFBRecord
   :members:

.. autoclass:: ppreproc_pfb.PFBFormatError

Exceptions
==========

Malformed or incompatible data raise ``PFBFormatError``. An invalid ordinal
raises ``IndexError``; an unknown scan identifier raises ``KeyError``. Missing
files raise the corresponding standard library exception.
