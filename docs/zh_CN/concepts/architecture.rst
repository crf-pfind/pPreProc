========
处理流程
========

pPreProc 包含三个功能阶段：

.. code-block:: text

   仪器厂商原始数据 -> pXtract 提取 -> PFB/PFC -> pParse2+ -> 下游检索
                                         |
                                         +------> Python/C++ SDK

``pXtract`` 针对不同仪器数据格式提取谱图；PFB/PFC 通过尾部索引保存谱图及
选定的元数据；``pParse2+`` 在既有 pParse2 母离子识别结果基础上，补充来自
pXtract 输出和针对性枚举的证据，并将多路结果统一整理后提供给下游流程。

组件
====

Windows 应用程序提供完整预处理流程；公开的 PFB/PFC 接口用于下游软件集成：

* 应用程序以专有 Windows 二进制软件包发布；
* PFB/PFC 是公开且版本化的存储格式规范；
* Python 和 C++ SDK 是公开的参考实现；

本仓库不包含应用程序核心源码或仪器厂商 SDK 源码。
