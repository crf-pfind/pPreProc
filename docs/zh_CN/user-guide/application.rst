===================
Windows 应用程序
===================

pPreProc 将仪器厂商数据提取、带索引的谱图存储和母离子处理与下游数据库检索
分离。独立软件包用于运行这一预处理流程，不会将 pFind 的其他组件作为
pPreProc 的一部分发布。

当前可用方式
============

pPreProc 先前随 pFind 3.2.3 提供。当前 Windows x64 独立候选发布版
``2.5.2-rc.1`` 已在 `GitHub Releases
<https://github.com/crf-pfind/pPreProc/releases/tag/v2.5.2-rc.1>`_ 发布，用于在
稳定版 ``2.5.2`` 发布前验证安装过程和各仪器厂商数据格式的工作流程。应用程序
核心源码属于专有内容，未在本仓库公开。

命令入口
========

Windows 软件包提供统一启动脚本：

.. code-block:: powershell

   .\ppreproc.ps1 -Input D:\data\sample.raw
   .\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
   .\ppreproc.ps1 -Version

``-Input`` 和 ``-Config`` 必须且只能指定一个。启动脚本会解析输入路径、选择
软件包内的 pParse2+ 运行组件，并在应用程序所需的工作目录中执行。

已验证范围
==========

当前端到端验证覆盖数据依赖型采集（DDA），包括常规 DDA、FAIMS-DDA 和
dda-PASEF。PFB/PFC 本身并不限定 DDA 或数据非依赖型采集（DIA）；
pParse/pParse2+ 中面向 DIA 的母离子处理整合仍在推进。
