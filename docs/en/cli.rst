======================
Command-line interface
======================

Installing the Python reader provides the ``ppreproc-pfb`` command. Output is
UTF-8 JSON so it can be inspected directly or consumed by another program.

File information
================

.. code-block:: console

   ppreproc-pfb info run.pfb

Reports file paths, PFB byte size, spectrum count, footer-index address, and
the available PFC columns.

Validation
==========

.. code-block:: console

   ppreproc-pfb validate run.pfb
   ppreproc-pfb validate run.pfb --full

The default command checks structural invariants while opening the pair.
``--full`` additionally decodes every record, checks PFB/PFC peak counts and
byte boundaries, parses retention times, and follows declared parent links.

Retrieve one spectrum
=====================

Select by zero-based record index or PFC ``ScanNo``:

.. code-block:: console

   ppreproc-pfb spectrum run.pfb --index 0
   ppreproc-pfb spectrum run.pfb --scan 102

The command reports record and metadata information but deliberately omits
the peak arrays from JSON output.

Exit behavior
=============

Successful commands return exit status zero. Invalid arguments are handled by
``argparse``. Format violations and missing files produce a non-zero exit and
an exception message, which is suitable for CI validation gates.
