====================
Windows application
====================

pPreProc separates vendor-data extraction, indexed spectrum storage, and
precursor processing from downstream database search. The standalone package
is intended to run this preprocessing workflow without presenting the rest of
the pFind suite as part of pPreProc.

Availability
============

The application was previously distributed with pFind 3.2.3. The standalone
``2.5.2-rc.1`` Windows x64 release candidate is now available from `GitHub
Releases <https://github.com/crf-pfind/pPreProc/releases/tag/v2.5.2-rc.1>`_. It
is intended to qualify installation and vendor-format workflows before the
stable ``2.5.2`` release. Application source is proprietary and is not
included in this repository.

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

The current end-to-end validation covers DDA workflows, including conventional
DDA, FAIMS-DDA, and dda-PASEF. PFB/PFC itself can represent spectra without
assuming DDA or DIA. DIA-specific precursor-processing integration in
pParse/pParse2+ remains under development.
