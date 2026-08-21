============
Installation
============

Windows application
===================

Runnable pPreProc packages are published on the GitHub
`Releases page <https://github.com/crf-pfind/pPreProc/releases>`_. A valid
application release contains a Windows ZIP archive, checksums, release notes,
and the applicable license and third-party notices.

The current standalone package is the ``2.5.2-rc.1`` Windows x64 release
candidate. Download the asset named ``pPreProc-2.5.2-rc.1-windows-x64.zip``;
the automatically generated ``Source code`` archives are not application
packages. Verify the adjacent ``.sha256`` file, extract the ZIP, and run:

.. code-block:: powershell

   .\ppreproc.ps1 -Version
   .\ppreproc.ps1 -Input D:\data\sample.raw

The application targets 64-bit Windows and requires .NET Framework 4.8.

Python SDK
==========

The Python reference SDK supports Python 3.9 or newer on Windows, Linux, and
macOS and has no third-party runtime dependencies.

.. code-block:: console

   git clone https://github.com/crf-pfind/pPreProc.git
   cd pPreProc
   python -m pip install .

Confirm the installation:

.. code-block:: console

   ppreproc-pfb --help

C++ SDK setup
=============

The C++ reference SDK is header-only and requires a C++17 compiler. Add
``sdk/cpp/include`` to the include path or install the CMake target from
``sdk/cpp``. See :doc:`../reference/cpp-api` for build commands.
