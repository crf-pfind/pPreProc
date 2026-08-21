====================
Windows application
====================

pPreProc extracts spectra from supported instrument data, writes indexed
PFB/PFC files, and runs pParse2+ precursor processing for downstream analysis.
Install the application as described in :doc:`../getting-started/installation`.

Command entry point
===================

The Windows package exposes one launcher:

.. code-block:: powershell

   .\ppreproc.ps1 -Input D:\data\sample.raw
   .\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
   .\ppreproc.ps1 -Version

Use exactly one of ``-Input`` and ``-Config``. The launcher resolves the input
path, selects the bundled pParse2+ runtime, and runs from the executable
directory required by the application.

Validated scope
===============

The current application workflow is validated for conventional DDA, FAIMS-DDA,
and dda-PASEF data. The PFB/PFC format and its readers do not assume an
acquisition mode; the current pParse2+ workflow does not provide DIA-specific
precursor processing.
