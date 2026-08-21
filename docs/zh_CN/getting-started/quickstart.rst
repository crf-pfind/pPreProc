========
快速开始
========

验证配套的 PFB/PFC 文件
=======================

仓库提供了一个小型合成测试样例：

.. code-block:: console

   ppreproc-pfb info sdk/python/tests/fixtures/minimal.pfb
   ppreproc-pfb validate sdk/python/tests/fixtures/minimal.pfb --full

``validate --full`` 会解码全部记录，检查 PFB/PFC 字节边界和谱峰数，并验证
已声明的一级谱关联关系。

读取一张谱图
============

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       spectrum = reader.get_spectrum_by_scan(102)
       print(spectrum.scan_number, spectrum.peak_count)
       parent_ms1 = reader.get_parent_ms1(spectrum)

读取器会自动选择同名的配套文件 ``run.pfc``。记录定位直接使用 PFB 尾部索引，
无需解码排在前面的谱图。

后续阅读
========

* :doc:`../user-guide/reading-pfb-pfc`：遍历、仅元数据读取、对应一级谱定位和
  提取离子流色谱图（XIC）。
* :doc:`../reference/python-api`：完整 Python 接口。
* :doc:`../reference/pfb-pfc-format`：实现其他读取器前应遵循的格式约定。
