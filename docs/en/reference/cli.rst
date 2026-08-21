======================
Command-line reference
======================

Installing the Python SDK provides the ``ppreproc-pfb`` command. Commands emit
UTF-8 JSON on standard output.

File information
================

.. code-block:: console

   ppreproc-pfb info run.pfb

Reports the PFB and PFC paths, file size, spectrum count, footer-index address,
and PFC columns.

Validation
==========

.. code-block:: console

   ppreproc-pfb validate run.pfb
   ppreproc-pfb validate run.pfb --full

Opening the pair always validates its structure. ``--full`` also decodes every
record, verifies PFB/PFC peak counts and byte boundaries, parses retention
times, and follows declared parent links.

Spectrum lookup
===============

.. code-block:: console

   ppreproc-pfb spectrum run.pfb --index 0
   ppreproc-pfb spectrum run.pfb --scan 102

The response contains record properties and metadata but omits peak arrays.
Use the Python or C++ SDK when the arrays are required.

Exit status
===========

Successful commands return zero. Invalid arguments, missing files, and format
violations return non-zero.
