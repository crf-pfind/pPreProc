===================
Python SDK 接口参考
===================

公开包名为 ``ppreproc_pfb``，稳定公开对象包括 ``PFBReader``、``PFBRecord``
和 ``PFBFormatError``。

示例
====

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       first = reader.get_spectrum(0)
       selected = reader.get_spectrum_by_scan("102")
       parent = reader.get_parent_ms1(selected)
       metadata = list(reader.iter_spectra(with_arrays=False))

``PFBReader``
=============

.. py:class:: PFBReader(pfb_path, pfc_path=None, *, require_pfc=True)

   打开并随机访问 PFB/PFC v1 配套文件。

   ``pfb_path`` 为 PFB 文件路径；``pfc_path`` 用于显式指定 PFC 路径，省略时
   自动使用同名的 ``.pfc`` 文件。``require_pfc=False`` 仅适用于底层 PFB
   检查，此时无法按扫描号读取谱图或定位对应一级谱。

   建议通过 ``with`` 语句使用读取器，以便及时关闭内存映射和文件句柄。

   .. py:method:: get_spectrum(index, *, with_arrays=True)

      按从零开始的记录序号直接读取一张谱图。负数序号遵循 Python 索引规则。
      ``with_arrays=False`` 时不解码 m/z 和强度数组，仅返回记录信息和元数据。

   .. py:method:: get_spectrum_by_scan(scan_number, *, with_arrays=True)

      按 PFC 的 ``ScanNo`` 扫描号读取一张谱图。扫描号不存在时抛出
      ``KeyError``。

   .. py:method:: get_parent_ms1(spectrum, *, with_arrays=True)

      根据 ``PrecursorScan`` 记录的谱图关联关系，返回指定记录对应的一级谱。
      ``spectrum`` 可以是记录序号或现有 ``PFBRecord``。关联缺失或循环关联时
      抛出 ``PFBFormatError``。

   .. py:method:: iter_spectra(*, with_arrays=True)

      按记录序号顺序遍历谱图。``with_arrays=False`` 可用于仅元数据读取。

   .. py:method:: validate(*, full=False)

      验证配套文件并返回可供程序读取的汇总字典。``full=True`` 时解码全部
      记录，核对谱峰数和字节边界，解析保留时间，并验证一级谱关联关系。

   .. py:method:: extract_xic(target_mz, ppm, rt_start, rt_end, *, faims_cv=None)

      从一级谱中提取离子流色谱图（XIC）。``target_mz`` 为中心 m/z，``ppm``
      为对称质量容差，``rt_start`` 和 ``rt_end`` 为闭区间保留时间边界。
      ``faims_cv`` 可用于按 FAIMS 补偿电压筛选；此时 PFC 必须包含
      ``FAIMS_Voltage`` 列。返回 ``(保留时间, 强度总和)`` 列表。

   .. py:method:: close()

      关闭内存映射和 PFB 文件句柄。

   ``len(reader)`` 返回谱图数；直接遍历 ``reader`` 等价于调用
   ``iter_spectra()``。

``PFBRecord``
=============

.. py:class:: PFBRecord

   一张已解码谱图及其配套 PFC 元数据。主要属性如下：

   ``index``
      从零开始的记录序号。

   ``start_pos`` / ``end_pos``
      该记录在 PFB 中的绝对字节边界。

   ``property_text``
      PFB 记录中保存的 UTF-8 属性文本。

   ``peak_count``
      成对 m/z 和强度值的数量，即谱峰数。

   ``mz`` / ``intensity``
      双精度谱峰数组。使用 ``with_arrays=False`` 读取时为空数组。

   ``metadata``
      以 PFC 列名为键的元数据字典。

   ``scan_number``
      非空的 PFC ``ScanNo`` 扫描号；没有可用值时为 ``None``。

``PFBFormatError``
==================

.. py:exception:: PFBFormatError

   PFB/PFC 配套文件违反 v1 格式规范时抛出的异常。

异常
====

数据损坏或结构不兼容时抛出 ``PFBFormatError``；记录序号越界时抛出
``IndexError``；扫描号不存在时抛出 ``KeyError``；文件缺失等情况使用 Python
标准库的对应异常。
