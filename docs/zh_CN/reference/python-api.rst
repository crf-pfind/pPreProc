================
Python SDK 参考
================

公开包名为 ``ppreproc_pfb``，受支持的公开名称为 ``PFBReader``、
``PFBRecord`` 和 ``PFBFormatError``。

示例
====

.. code-block:: python

   from ppreproc_pfb import PFBReader

   with PFBReader("run.pfb") as reader:
       first = reader.get_spectrum(0)
       selected = reader.get_spectrum_by_scan("102")
       parent = reader.get_parent_ms1(selected)
       metadata = list(reader.iter_spectra(with_arrays=False))

API
===

.. autoclass:: ppreproc_pfb.PFBReader
   :members:
   :special-members: __len__, __iter__
   :exclude-members: __weakref__

.. autoclass:: ppreproc_pfb.PFBRecord
   :members:

.. autoclass:: ppreproc_pfb.PFBFormatError

异常
====

数据损坏或结构不兼容时抛出 ``PFBFormatError``；序号越界时抛出
``IndexError``；扫描号不存在时抛出 ``KeyError``；文件缺失等情况使用 Python
标准库对应异常。
