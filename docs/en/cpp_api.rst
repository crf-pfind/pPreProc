=================
C++17 interface
=================

The header-only reference reader is located at
``cpp/include/ppreproc/pfb_reader.hpp``. It depends only on the C++17 standard
library.

Build the example
=================

.. code-block:: console

   cmake -S cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
   cmake --build build/cmake --config Release
   ctest --test-dir build/cmake --build-config Release --output-on-failure

Minimal use
===========

.. code-block:: cpp

   #include <ppreproc/pfb_reader.hpp>
   #include <iostream>

   int main() {
     ppreproc::pfb_reader reader("run.pfb");
     auto record = reader.spectrum_by_scan("102");
     std::cout << record.mz.size() << "\n";
   }

Public types
============

``ppreproc::pfb_format_error``
   Raised for malformed or incompatible PFB/PFC input.

``ppreproc::spectrum_record``
   Contains ``index``, PFB byte boundaries, property text, m/z and intensity
   vectors, and the PFC metadata map.

``ppreproc::pfb_reader``
   Opens a PFB file and its same-stem PFC companion. Its principal operations
   are:

   * ``size()`` and ``index_address()`` for file-level information;
   * ``spectrum(index, with_arrays)`` for footer-indexed access;
   * ``spectrum_by_scan(scan, with_arrays)`` for PFC identifier lookup; and
   * ``parent_ms1(child, with_arrays)`` for parent-chain resolution.

The constructor validates the structural index and the required PFC columns.
The C++ interface currently requires the PFC companion.
