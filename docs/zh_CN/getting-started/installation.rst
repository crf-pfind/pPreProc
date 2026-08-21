========
安装
========

Windows 应用程序
================

打开 GitHub `Releases 页面 <https://github.com/crf-pfind/pPreProc/releases>`_，
下载 ``pPreProc-<版本号>-windows-x64.zip`` 及对应的 ``.sha256`` 文件。
GitHub 自动生成的 ``Source code`` 压缩包不是可运行的软件包。

在 PowerShell 中计算压缩包校验和，并与发布页提供的值比较：

.. code-block:: powershell

   (Get-FileHash .\pPreProc-<版本号>-windows-x64.zip -Algorithm SHA256).Hash

解压后，在软件包目录中运行：

.. code-block:: powershell

   .\ppreproc.ps1 -Version
   .\ppreproc.ps1 -Input D:\data\sample.raw

应用程序需要 64 位 Windows 和 .NET Framework 4.8。

Python SDK
==========

Python 参考 SDK 支持 Windows、Linux 和 macOS 上的 Python 3.9 及以上版本，
且没有第三方运行时依赖。

.. code-block:: console

   git clone https://github.com/crf-pfind/pPreProc.git
   cd pPreProc
   python -m pip install .

确认安装：

.. code-block:: console

   ppreproc-pfb --help

C++ SDK 安装
============

C++ 参考 SDK 仅包含头文件，需要 C++17 编译器。可将 ``sdk/cpp/include``
加入包含路径，也可从 ``sdk/cpp`` 安装 CMake 目标。构建命令见
:doc:`../reference/cpp-api`。
