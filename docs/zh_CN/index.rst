=============
pPreProc 文档
=============

pPreProc 是用于质谱数据预处理的 Windows 应用程序，并通过带索引的
PFB/PFC 接口支持下游软件快速访问数据。本文档介绍应用程序工作流程、公开
SDK 和文件格式规范。

.. note::

   pPreProc 应用程序以专有二进制软件包发布，核心源码未在本仓库公开。
   Python 和 C++ PFB/PFC SDK、示例及接口规范以 BSD-3-Clause 许可证公开。

.. toctree::
   :caption: 快速开始
   :maxdepth: 2

   getting-started/installation
   getting-started/quickstart

.. toctree::
   :caption: 操作指南
   :maxdepth: 2

   user-guide/application
   user-guide/reading-pfb-pfc

.. toctree::
   :caption: 原理与边界
   :maxdepth: 2

   concepts/architecture
   concepts/data-fidelity

.. toctree::
   :caption: 参考
   :maxdepth: 2

   reference/cli
   reference/python-api
   reference/cpp-api
   reference/pfb-pfc-format
   reference/compatibility

.. toctree::
   :caption: 项目
   :maxdepth: 2

   project/releases
   project/support

中文术语约定
============

本中文版统一使用以下质谱术语：

============================  ============================
英文                          中文
============================  ============================
MS1 spectrum / MS2 spectrum   一级谱 / 二级谱
precursor ion / product ion   母离子 / 子离子
fragment ion                  碎片离子
spectrum / peak               谱图 / 谱峰
scan number                   扫描号
retention time                保留时间
ion mobility                  离子淌度
isolation window              隔离窗口
FAIMS compensation voltage    FAIMS 补偿电压
============================  ============================

相关链接
========

* `GitHub 仓库 <https://github.com/crf-pfind/pPreProc>`_
* `应用程序发布页 <https://github.com/crf-pfind/pPreProc/releases>`_
* `问题跟踪 <https://github.com/crf-pfind/pPreProc/issues>`_
* `讨论区 <https://github.com/crf-pfind/pPreProc/discussions>`_
