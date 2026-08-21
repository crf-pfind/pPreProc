===================
C++17 SDK reference
===================

The header-only SDK is located at
``sdk/cpp/include/ppreproc/pfb_reader.hpp`` and depends only on the C++17
standard library.

Build the example
=================

.. code-block:: console

   cmake -S sdk/cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
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
   Reports malformed or incompatible input.

``ppreproc::spectrum_record``
   Contains the ordinal, PFB byte boundaries, property text, m/z and intensity
   vectors, and PFC metadata.

``ppreproc::pfb_reader``
   Opens a PFB/PFC pair and provides ``size()``, ``index_address()``,
   ``spectrum()``, ``spectrum_by_scan()``, and ``parent_ms1()``.

The constructor validates the footer index and required PFC columns. The C++
SDK requires the PFC companion.
