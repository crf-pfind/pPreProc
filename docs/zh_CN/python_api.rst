================
Python API 参考
================

公共包名为 ``ppreproc_pfb``，稳定的公共名称为 ``PFBReader``、
``PFBRecord`` 和 ``PFBFormatError``。

典型用法
========

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       first = reader.get_spectrum(0)
       selected = reader.get_spectrum_by_scan("102")
       parent = reader.get_parent_ms1(selected)

       for spectrum in reader.iter_spectra(with_arrays=False):
           print(spectrum.index, spectrum.scan_number)

       xic = reader.extract_xic(
           target_mz=500.2,
           ppm=10,
           rt_start=0,
           rt_end=20,
       )

直接读取通过 PFB 尾部索引定位，不会解码目标记录之前的谱图。只需要属性
和 PFC 元数据时，可设置 ``with_arrays=False`` 以跳过峰数组解码。

PFBReader
=========

构造函数：

.. code-block:: python

   PFBReader(pfb_path, pfc_path=None, *, require_pfc=True)

``pfb_path`` 是 PFB 路径；默认使用同名 PFC。将 ``require_pfc`` 设为
``False`` 只适用于底层 PFB 检查，此时扫描号、父谱和 XIC 操作不可用。

主要方法：

``get_spectrum(index, *, with_arrays=True)``
   按从 0 开始的记录序号随机读取谱图；支持 Python 风格的负序号。

``get_spectrum_by_scan(scan_number, *, with_arrays=True)``
   按 PFC 的 ``ScanNo`` 字段读取谱图。

``get_parent_ms1(spectrum, *, with_arrays=True)``
   沿 ``PrecursorScan`` 关联向上查找对应 MS1，并检测循环关联。

``iter_spectra(*, with_arrays=True)``
   按文件顺序遍历全部谱图；``len(reader)`` 返回谱图数。

``validate(*, full=False)``
   检查结构。``full=True`` 时解码所有记录，并核对谱峰数、字节边界、
   保留时间和父谱关联。

``extract_xic(target_mz, ppm, rt_start, rt_end, *, faims_cv=None)``
   在给定 m/z 容差和保留时间范围内提取简单的 MS1 色谱曲线；可按
   FAIMS CV 进一步筛选。

``close()``
   关闭内存映射和文件句柄。推荐使用 ``with`` 上下文管理器。

PFBRecord
=========

不可变记录对象包含 ``index``、``start_pos``、``end_pos``、
``property_text``、``peak_count``、``mz``、``intensity`` 和 ``metadata``。
``scan_number`` 属性返回清理后的 ``ScanNo``，不存在时返回 ``None``。

异常
====

格式错误或结构不兼容时抛出 ``PFBFormatError``；记录序号越界抛出
``IndexError``；扫描号不存在抛出 ``KeyError``。程序不应忽略
``PFBFormatError`` 后继续把文件当作有效数据使用。
