================
使用 PFB/PFC
================

打开配套文件
============

``PFBReader("run.pfb")`` 会打开 ``run.pfb`` 及同名的 ``run.pfc``。仅当两个
文件路径不同才需要传入 ``pfc_path``。创建读取器时会检查头部、尾部索引、
PFC 必需列、记录数和扫描号。

随机访问
========

.. code-block:: python

   with PFBReader("run.pfb") as reader:
       by_ordinal = reader.get_spectrum(0)
       by_scan = reader.get_spectrum_by_scan("102")

序号从零开始。``ScanNo`` 是 PFC 中的标识符，不要求与序号相同。

仅读取元数据
============

不需要谱峰数组时可设置 ``with_arrays=False``：

.. code-block:: python

   for spectrum in reader.iter_spectra(with_arrays=False):
       print(spectrum.scan_number, spectrum.metadata["RetTime"])

定位对应的一级谱
================

``get_parent_ms1()`` 沿 ``PrecursorScan`` 记录的谱图关联关系查找对应一级谱
（MS1）。关联缺失、扫描号不存在或出现循环关联时会明确报错，不会静默忽略。

提取离子流色谱图（XIC）
=======================

.. code-block:: python

   points = reader.extract_xic(
       target_mz=500.2,
       ppm=10,
       rt_start=0,
       rt_end=20,
       faims_cv=None,
   )

返回结果为指定窗口内一级谱的 ``(保留时间, 强度总和)`` 列表。
