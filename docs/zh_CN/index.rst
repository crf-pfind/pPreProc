=================
pPreProc 文档
=================

pPreProc 是一个质谱数据预处理框架，将厂商数据提取、前体处理和下游
索引访问相互分离。目前完成端到端验证的软件工作流面向数据依赖采集
（data-dependent acquisition，DDA）。PFB/PFC 存储接口本身不限定采集
模式；DIA 前体处理流程的集成仍在推进。

本站是 PFB/PFC 格式约定和公共接口的持续维护入口。GitHub Release 的
用途不同：只有在 Windows 运行时、再分发许可和干净环境测试均通过后，
才用于发布可直接运行且带版本号的 pPreProc 软件包。

.. important::

   Python 和 C++ 读取器是可检查的参考实现。仓库不把已编译的 pParse、
   pParse2+ 和 pXtract 应用组件表述为开源实现。

快速开始
========

.. toctree::
   :maxdepth: 2

   getting_started
   windows_application

PFB/PFC 接口
============

.. toctree::
   :maxdepth: 2

   pfb_pfc_format
   python_api
   cpp_api
   cli

项目与发布
==========

.. toctree::
   :maxdepth: 2

   release_scope

常用链接
========

* `GitHub 仓库 <https://github.com/crf-pfind/pPreProc>`_
* `问题反馈 <https://github.com/crf-pfind/pPreProc/issues>`_
* `PFB/PFC v1 英文规范原文 <https://github.com/crf-pfind/pPreProc/blob/main/docs/PFB_PFC_SPECIFICATION_V1.md>`_
