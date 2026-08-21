========
安装
========

Windows 应用程序
================

可运行的 pPreProc 软件包通过 GitHub
`Releases 页面 <https://github.com/crf-pfind/pPreProc/releases>`_ 发布。
有效的应用程序 Release 应包含 Windows ZIP 包、校验和、发行说明以及适用的
许可证和第三方声明。

当前独立应用程序为 ``2.5.2-rc.1`` Windows x64 候选版本。请下载名为
``pPreProc-2.5.2-rc.1-windows-x64.zip`` 的附件；GitHub 自动生成的
``Source code`` 压缩包不是应用程序。先用相邻的 ``.sha256`` 文件核验压缩包，
解压后运行：

.. code-block:: powershell

   .\ppreproc.ps1 -Version
   .\ppreproc.ps1 -Input D:\data\sample.raw

应用程序面向 64 位 Windows，并需要 .NET Framework 4.8。

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

C++ 参考 SDK 为仅头文件实现，需要 C++17 编译器。可将 ``sdk/cpp/include``
加入包含路径，也可从 ``sdk/cpp`` 安装 CMake target。构建命令见
:doc:`../reference/cpp-api`。
