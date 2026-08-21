============
命令行参考
============

安装 Python SDK 后可使用 ``ppreproc-pfb`` 命令。所有命令在标准输出中返回
UTF-8 JSON。

文件信息
========

.. code-block:: console

   ppreproc-pfb info run.pfb

输出 PFB/PFC 路径、PFB 文件大小、谱图数、尾部索引位置和 PFC 列名。

验证
====

.. code-block:: console

   ppreproc-pfb validate run.pfb
   ppreproc-pfb validate run.pfb --full

打开配套的 PFB/PFC 文件时始终进行结构检查。``--full`` 还会解码每条记录，
核对 PFB/PFC 谱峰数和字节边界，解析保留时间，并验证已声明的一级谱关联关系。

按序号或扫描号读取谱图
======================

.. code-block:: console

   ppreproc-pfb spectrum run.pfb --index 0
   ppreproc-pfb spectrum run.pfb --scan 102

输出包含记录属性和元数据，但不包含谱峰数组。需要谱峰数组时请使用 Python 或
C++ SDK。

退出状态
========

成功返回零；参数无效、文件缺失或格式不合法时返回非零。
