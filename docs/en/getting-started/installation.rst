============
Installation
============

Windows application
===================

Open the GitHub `Releases page
<https://github.com/crf-pfind/pPreProc/releases>`_ and download
``pPreProc-<version>-windows-x64.zip`` together with its ``.sha256`` file.
The automatically generated ``Source code`` archives are not application
packages.

Compare the published checksum with:

.. code-block:: powershell

   (Get-FileHash .\pPreProc-<version>-windows-x64.zip -Algorithm SHA256).Hash

Extract the ZIP, open PowerShell in the extracted directory, and run:

.. code-block:: powershell

   .\pPreProc.cmd --help
   .\pPreProc.cmd "D:\data\sample.raw"

The application requires 64-bit Windows and .NET Framework 4.8.

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
