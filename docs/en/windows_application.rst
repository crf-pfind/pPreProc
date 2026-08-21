Windows pPreProc application
============================

The standalone application is the user-facing preprocessing software. It is
distinct from the reference reader documented elsewhere on this site.

Current availability
====================

pPreProc was originally distributed inside pFind 3.2.3. The project is being
separated into its own repository and runnable Windows package. A public ZIP
must not be assumed available until the corresponding GitHub Release contains
the executable package, dependency notices, checksum manifest, and a passed
clean-machine validation record.

Planned package entry points
============================

The Windows package is designed to expose one pPreProc entry point around the
required pParse2+ runtime:

.. code-block:: powershell

   .\ppreproc.ps1 -Input D:\data\sample.raw
   .\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml

The package is assembled from an authorized runtime using an explicit
whitelist. It must not copy unrelated pFind search, GUI, or reporting tools.

Workflow scope
==============

The currently validated end-to-end application workflow targets DDA data.
The PFB/PFC representation itself stores spectrum arrays and selected metadata
without assuming DDA or DIA. DIA support therefore has two separate aspects:

* PFB/PFC readers can access spectra from either acquisition scheme when the
  required records and metadata are present.
* Integration and validation of DIA-specific precursor-processing behavior in
  pParse/pParse2+ are ongoing application work.

Publication boundary
====================

GitHub Releases are for the runnable application. Format specifications and
API reference material remain on this versioned documentation site; they are
not duplicated as Release attachments. See :doc:`release_scope`.
