# C++17 PFB/PFC SDK

The C++ reference SDK is a header-only implementation of the indexed PFB/PFC
v1 interface. It depends only on the C++17 standard library.

```console
cmake -S sdk/cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --config Release
ctest --test-dir build/cmake --build-config Release --output-on-failure
```

The public header is `include/ppreproc/pfb_reader.hpp`. See the
[C++ SDK documentation](https://ppreproc.readthedocs.io/en/latest/reference/cpp-api.html).
