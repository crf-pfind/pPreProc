========
快速开始
========

请根据任务选择入口：

* 使用 pPreProc 应用处理厂商数据：参见 :doc:`windows_application`；
* 在 Python 中读取已有 PFB/PFC 文件：安装下述参考读取器；
* 在 C++17 程序中集成 PFB/PFC：参见 :doc:`cpp_api`。

环境要求
========

Python 读取器支持 Windows、Linux 和 macOS 上的 Python 3.9 及以上版本，
运行时不依赖第三方 Python 包。

从仓库安装
==========

读取器作为在线接口文档和仓库源码的一部分持续维护，不作为单独的
GitHub Release 附件发布。

.. code-block:: console

   git clone https://github.com/crf-pfind/pPreProc.git
   cd pPreProc
   python -m pip install .

使用仓库内置的合成测试数据检查安装：

.. code-block:: console

   ppreproc-pfb info tests/fixtures/minimal.pfb
   ppreproc-pfb validate tests/fixtures/minimal.pfb --full
   ppreproc-pfb spectrum tests/fixtures/minimal.pfb --scan 102

读取一张谱图
============

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       ms2 = reader.get_spectrum_by_scan(102)
       print(ms2.scan_number, ms2.peak_count)
       parent = reader.get_parent_ms1(ms2)

默认自动查找同名的 ``run.pfc``。只有 PFB 和 PFC 文件名主体不一致时，
才需要向 ``PFBReader`` 显式传入 ``pfc_path``。

继续阅读
========

* 实现新的读取器前，请先阅读 :doc:`pfb_pfc_format`；
* 随机访问、父谱查找、遍历和 XIC 提取见 :doc:`python_api`；
* 不编写代码时，可使用 :doc:`cli` 完成检查和验证。
