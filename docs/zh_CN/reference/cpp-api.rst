================
C++17 SDK 参考
================

仅含头文件的 SDK 位于 ``sdk/cpp/include/ppreproc/pfb_reader.hpp``，只依赖
C++17 标准库。

构建示例
========

.. code-block:: console

   cmake -S sdk/cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
   cmake --build build/cmake --config Release
   ctest --test-dir build/cmake --build-config Release --output-on-failure

最小用法
========

.. code-block:: cpp

   #include <ppreproc/pfb_reader.hpp>
   #include <iostream>

   int main() {
     ppreproc::pfb_reader reader("run.pfb");
     auto record = reader.spectrum_by_scan("102");
     std::cout << record.mz.size() << "\n";
   }

公开类型
========

``ppreproc::pfb_format_error``
   表示输入损坏或不兼容。

``ppreproc::spectrum_record``
   包含记录序号、PFB 字节边界、属性文本、m/z 与强度数组以及 PFC 元数据。

``ppreproc::pfb_reader``
   打开配套的 PFB/PFC 文件，并提供 ``size()``、``index_address()``、
   ``spectrum()``、``spectrum_by_scan()`` 和 ``parent_ms1()``。

构造函数会验证尾部索引和 PFC 必需列。C++ SDK 要求配套 PFC 文件存在。
