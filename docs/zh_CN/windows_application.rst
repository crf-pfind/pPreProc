=====================
Windows pPreProc 软件
=====================

独立应用是面向最终用户的数据预处理软件，与本站介绍的参考读取器是两个
边界清楚的组成部分。

当前可用状态
============

pPreProc 最初包含在 pFind 3.2.3 中，目前正在整理为独立仓库和可运行的
Windows 软件包。只有 GitHub Release 中实际提供了可执行包、依赖许可
声明、校验和清单以及干净环境测试记录时，才能认为该独立软件包已经公开
发布。

计划提供的入口
==============

Windows 软件包计划围绕所需的 pParse2+ 运行时提供统一的 pPreProc 入口：

.. code-block:: powershell

   .\ppreproc.ps1 -Input D:\data\sample.raw
   .\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml

软件包使用明确的白名单从已获授权的运行时中组装，不应包含与 pPreProc
无关的 pFind 搜索、图形界面或结果报告程序。

工作流范围
==========

目前完成端到端验证的应用流程面向 DDA 数据。PFB/PFC 表示保存谱峰数组和
选定元数据，本身不假定 DDA 或 DIA。因此 DIA 支持需要区分两个层面：

* 只要文件中具有所需谱图记录和元数据，PFB/PFC 读取器即可访问不同采集
  模式的数据；
* pParse/pParse2+ 中 DIA 特定前体处理行为的集成和系统验证仍是后续应用
  开发工作。

发布边界
========

GitHub Release 用于可运行的软件包；格式规范和 API 参考在这个可版本化的
文档站持续更新，不再作为 Release 附件重复打包。详见
:doc:`release_scope`。
