==================
PFB/PFC v1 参考
==================

PFB/PFC v1 由两个配套文件组成，并支持索引访问。``name.pfb`` 保存谱图记录和
尾部索引，``name.pfc`` 保存对应的制表符分隔元数据。记录序号、尾部索引序号和
PFC 数据行序号均指向同一张谱图。

基本类型
========

所有数值字段均采用小端字节序。

=================  ====================================  ========
名称               编码                                  大小
=================  ====================================  ========
``int32``          有符号二进制补码整数                  4 字节
``uint32``         无符号整数                            4 字节
``uint64``         无符号整数                            8 字节
``binary64``       IEEE 754 双精度浮点数                 8 字节
=================  ====================================  ========

PFB 布局
========

固定头部为 24 字节：

======  ==========  ==================  =============================
偏移    类型        字段                v1 含义
======  ==========  ==================  =============================
0       ``int32``   ``reserved_1``      保留
4       ``int32``   ``reserved_2``      保留
8       ``int32``   ``reserved_3``      保留
12      ``uint64``  ``index_address``   尾部索引的绝对偏移
20      ``int32``   ``spectrum_count``  记录数及 PFC 数据行数
======  ==========  ==================  =============================

每条谱图记录依次包含 ``uint32`` 属性字节数、UTF-8 属性字节、``uint32`` 谱峰数、
``peak_count`` 个 binary64 m/z 值和同样数量的 binary64 强度值。记录间不定义
对齐填充。

从 ``index_address`` 开始，尾部恰好包含 ``spectrum_count`` 个 ``uint64``
绝对记录偏移。第一个偏移为 24，所有偏移严格递增，最后一条记录恰好结束于
``index_address``。

PFC 核心字段
============

PFC 是 UTF-8 制表符分隔文本，包含一个表头和每张谱图一行数据。读取器按字段名
选择列，并接受额外列。v1 要求：

* 标识与关联：``ScanNo``、``PrecursorScan``；
* 采集上下文：``RetTime``、``SpectrumType``、``InstrumentType``、
  ``IonInjectionTime``；
* 活化与母离子信息：``activationType``、``activationCenter``、``NCE``、
  ``monoIsotopicMz``、``upperCharge``、``lowerCharge``、
  ``activationWindow``；
* 完整性字段：``NumberofPeaks``、``StartPos``、``EndPos``。

``ScanNo`` 必须非空且唯一；完整性字段必须与对应 PFB 记录及尾部索引一致。

规范文本
========

包含验证要求和字段单位的完整规范位于
`interfaces/pfb-pfc/v1/specification.md <https://github.com/crf-pfind/pPreProc/blob/main/interfaces/pfb-pfc/v1/specification.md>`_。
