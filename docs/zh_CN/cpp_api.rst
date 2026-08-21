===============
C++17 接口
===============

仅头文件的参考读取器位于 ``cpp/include/ppreproc/pfb_reader.hpp``，运行时
只依赖 C++17 标准库。

构建示例
========

.. code-block:: console

   cmake -S cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
   cmake --build build/cmake --config Release
   ctest --test-dir build/cmake --build-config Release --output-on-failure

最小示例
========

.. code-block:: cpp

   #include <ppreproc/pfb_reader.hpp>
   #include <iostream>

   int main() {
     ppreproc::pfb_reader reader("run.pfb");
     auto record = reader.spectrum_by_scan("102");
     std::cout << record.mz.size() << "\n";
   }

公共类型
========

``ppreproc::pfb_format_error``
   输入 PFB/PFC 格式错误或不兼容时抛出的异常。

``ppreproc::spectrum_record``
   包含记录序号、PFB 字节边界、属性文本、m/z 与强度向量，以及 PFC
   元数据映射。

``ppreproc::pfb_reader``
   打开 PFB 及其同名 PFC，主要操作包括：

   * ``size()`` 和 ``index_address()``：读取文件级信息；
   * ``spectrum(index, with_arrays)``：按尾部索引访问；
   * ``spectrum_by_scan(scan, with_arrays)``：按 PFC 扫描标识访问；
   * ``parent_ms1(child, with_arrays)``：沿父谱关联查找 MS1。

构造函数会验证 PFB 索引结构及 PFC 必需字段。当前 C++ 接口要求存在 PFC
配套文件。
