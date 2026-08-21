===================
Processing workflow
===================

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

Components
==========

The Windows application contains the preprocessing workflow. The public
PFB/PFC interface supports downstream integration:

* the application is distributed as a proprietary Windows binary;
* PFB/PFC is a public, versioned storage format; and
* the Python and C++ SDKs are public reference readers.

The repository does not contain the application's core source or vendor SDK
source.
