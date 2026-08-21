============
命令行接口
============

安装 Python 读取器后会提供 ``ppreproc-pfb`` 命令。输出为 UTF-8 JSON，
既便于直接检查，也可由其他程序继续处理。

查看文件信息
============

.. code-block:: console

   ppreproc-pfb info run.pfb

输出 PFB/PFC 路径、PFB 字节大小、谱图数量、尾部索引地址和 PFC 字段名。

验证文件
========

.. code-block:: console

   ppreproc-pfb validate run.pfb
   ppreproc-pfb validate run.pfb --full

默认在打开文件时检查结构约束。``--full`` 还会解码全部记录，核对 PFB/PFC
谱峰数与字节边界，解析保留时间并验证已声明的父谱关联。

读取单张谱图
============

可按从 0 开始的记录序号或 PFC ``ScanNo`` 选择：

.. code-block:: console

   ppreproc-pfb spectrum run.pfb --index 0
   ppreproc-pfb spectrum run.pfb --scan 102

输出包含记录和元数据信息，但有意不把峰数组写入 JSON。

退出行为
========

成功时退出码为 0。无效参数由 ``argparse`` 处理；格式错误或文件缺失会返回
非零退出码并输出异常信息，因此可直接用于持续集成中的验证步骤。
