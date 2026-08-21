======================
pPreProc documentation
======================

pPreProc is a mass-spectrometry data-preprocessing framework that separates
vendor-data extraction, precursor processing, and indexed downstream access.
The currently validated application workflow targets data-dependent
acquisition (DDA). The PFB/PFC storage interface is acquisition-scheme
agnostic, while DIA precursor-processing integration remains ongoing.

This site is the maintained home of the PFB/PFC contract and its public
interfaces. GitHub Releases have a different purpose: they are reserved for
runnable, versioned pPreProc software packages after the Windows runtime and
redistribution checks are complete.

.. important::

   The Python and C++ readers are source-visible reference implementations.
   The compiled pParse, pParse2+, and pXtract application components are not
   represented as open-source implementations in this repository.

Getting started
===============

.. toctree::
   :maxdepth: 2

   getting_started
   windows_application

PFB/PFC interface
=================

.. toctree::
   :maxdepth: 2

   pfb_pfc_format
   python_api
   cpp_api
   cli

Project and publication
=======================

.. toctree::
   :maxdepth: 2

   release_scope

Useful links
============

* `GitHub repository <https://github.com/crf-pfind/pPreProc>`_
* `Issue tracker <https://github.com/crf-pfind/pPreProc/issues>`_
* `Normative PFB/PFC v1 source document <https://github.com/crf-pfind/pPreProc/blob/main/docs/PFB_PFC_SPECIFICATION_V1.md>`_
