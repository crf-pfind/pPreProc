========
安装
========

Windows 应用程序
================

可运行的 pPreProc 软件包通过 GitHub
`Releases 页面 <https://github.com/crf-pfind/pPreProc/releases>`_ 发布。
有效的应用程序 Release 应包含 Windows ZIP 包、校验和、发行说明以及适用的
许可证和第三方声明。

目前尚未发布独立应用程序 Release。GitHub 自动生成的 ``Source code`` 压缩包
只包含本公共仓库，并不是 Windows 应用程序安装包。在独立版本发布前，应用程序
仍通过 pFind 3.2.3 提供。

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
