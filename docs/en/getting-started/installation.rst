============
Installation
============

Windows application
===================

Runnable pPreProc packages are published on the GitHub
`Releases page <https://github.com/crf-pfind/pPreProc/releases>`_. A valid
application release contains a Windows ZIP archive, checksums, release notes,
and the applicable license and third-party notices.

No standalone application Release is currently published. The ``Source code``
archives generated automatically by GitHub contain the public repository, not
the Windows application. Until the standalone package is released, the
application remains available through pFind 3.2.3.

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
