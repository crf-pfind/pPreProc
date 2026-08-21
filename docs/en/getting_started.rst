===============
Getting started
===============

Choose the path that matches your task:

* To preprocess vendor data with the pPreProc application, see
  :doc:`windows_application`.
* To read an existing PFB/PFC pair from Python, install the reference reader
  below.
* To integrate PFB/PFC in C++17, see :doc:`cpp_api`.

Requirements
============

The Python reader supports Python 3.9 or newer on Windows, Linux, and macOS.
It has no third-party runtime dependencies.

Install from the repository
===========================

The reader is maintained as part of the online interface documentation and
repository source. It is not delivered as a separate GitHub Release asset.

.. code-block:: console

   git clone https://github.com/crf-pfind/pPreProc.git
   cd pPreProc
   python -m pip install .

Validate the bundled synthetic fixture:

.. code-block:: console

   ppreproc-pfb info tests/fixtures/minimal.pfb
   ppreproc-pfb validate tests/fixtures/minimal.pfb --full
   ppreproc-pfb spectrum tests/fixtures/minimal.pfb --scan 102

Read a spectrum
===============

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       ms2 = reader.get_spectrum_by_scan(102)
       print(ms2.scan_number, ms2.peak_count)
       parent = reader.get_parent_ms1(ms2)

The companion ``run.pfc`` is selected automatically. Pass ``pfc_path`` to
``PFBReader`` only when the two files do not share a stem.

Next steps
==========

* Read :doc:`pfb_pfc_format` before implementing another reader.
* Use :doc:`python_api` for random access, parent lookup, iteration, and XIC
  extraction.
* Use :doc:`cli` for validation and inspection without writing code.
