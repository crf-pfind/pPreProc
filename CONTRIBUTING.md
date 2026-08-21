# Contributing

Contributions are welcome for the public parts of this repository:

- documentation and examples;
- the Python and C++ PFB/PFC SDKs;
- the PFB/PFC specification and compatibility tests;
- issue reproduction and packaging metadata.

The proprietary application source, internal algorithms, and vendor SDK source
are outside this repository and cannot be changed through a pull request.

## Before opening a change

Use GitHub Discussions for design proposals and feature requests. Use an Issue
for a reproducible defect. Do not upload vendor data, licensed binaries, access
tokens, or confidential logs.

## Development checks

```console
python -m pip install .
python -m pip install ruff==0.16.4
python tools/generate_fixture.py
python -m unittest discover -s sdk/python/tests -v
ruff check sdk/python/src sdk/python/tests tools examples/python
python tools/check_repository.py
cmake -S sdk/cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --config Release
ctest --test-dir build/cmake --build-config Release --output-on-failure
```

Build both documentation languages before changing navigation or shared
reference material:

```console
sphinx-build -W --keep-going -b html docs/en build/docs/en
sphinx-build -W --keep-going -b html docs/zh_CN build/docs/zh-cn
```

## Compatibility rules

- Existing PFB/PFC v1 files must remain readable by 1.x SDK releases.
- Adding optional PFC columns is compatible; changing an existing field or the
  PFB byte layout requires a new format version.
- User-visible changes belong in `CHANGELOG.md`.
- A pull request should contain one focused change and the tests needed to
  demonstrate it.
