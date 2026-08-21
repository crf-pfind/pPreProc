===================
Windows 应用程序
===================

pPreProc 从支持的仪器数据中提取谱图，写入带索引的 PFB/PFC 文件，并通过
pParse2+ 进行母离子处理，供下游分析使用。安装步骤见
:doc:`../getting-started/installation`。

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

当前应用程序工作流程已针对常规数据依赖型采集（DDA）、FAIMS-DDA 和
dda-PASEF 数据完成验证。PFB/PFC 格式及其读取器不限定采集模式；当前
pParse2+ 工作流程尚未提供面向数据非依赖型采集（DIA）的专用母离子处理。
