============
Architecture
============

pPreProc has three functional stages:

.. code-block:: text

   vendor data -> pXtract extraction -> PFB/PFC -> pParse2+ -> downstream search
                                         |
                                         +------> Python/C++ SDKs

``pXtract`` performs instrument-aware spectrum extraction. PFB/PFC stores the
extracted spectra and selected metadata with a footer index. ``pParse2+``
combines the established pParse2 precursor results with complementary evidence
from pXtract output and targeted enumeration, then consolidates the results for
downstream use.

Public surfaces
===============

The Windows application and the PFB/PFC developer interface are related but
separate products:

* the application is a proprietary Windows binary distribution;
* PFB/PFC is a public, versioned storage contract;
* the Python and C++ SDKs are public reference implementations; and
* MGF remains an interchange path for software that does not implement
  PFB/PFC.

The public repository does not contain the application's core source or vendor
SDK implementations. It contains the materials needed to download, document,
integrate, test, and report problems with the product.
