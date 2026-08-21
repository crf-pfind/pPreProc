===================
Windows 应用程序
===================

pPreProc 将厂商数据提取、带索引的谱图存储和前体处理与下游数据库检索分离。
独立软件包用于运行这一预处理流程，不把 pFind 的其他组件作为 pPreProc 的一部分。

当前可用方式
============

pPreProc 先前随 pFind 3.2.3 提供。待运行时再分发审查和干净系统验证完成后，
独立软件包将发布到 GitHub Releases。应用程序核心源码为闭源内容，不包含在
本仓库中。

命令入口
========

Windows 软件包提供统一启动脚本：

.. code-block:: powershell

   .\ppreproc.ps1 -Input D:\data\sample.raw
   .\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
   .\ppreproc.ps1 -Version

``-Input`` 和 ``-Config`` 必须且只能指定一个。启动脚本会解析输入路径、选择
软件包内的 pParse2+ 运行时，并在应用程序所需的工作目录中执行。

已验证范围
==========

当前端到端验证覆盖 DDA，包括常规 DDA、FAIMS-DDA 和 dda-PASEF。PFB/PFC
本身并不限定 DDA 或 DIA；pParse/pParse2+ 中面向 DIA 的前体处理整合仍在推进。
