# Contributing

This repository accepts changes to the public SDKs, PFB/PFC specification,
documentation, examples, tests, and packaging metadata. The proprietary
application and vendor SDK source are outside its scope.

Use GitHub Discussions for proposals and GitHub Issues for reproducible
defects. Do not upload vendor data, licensed binaries, credentials, or
confidential logs.

## Checks

```console
python -m pip install .
python -m pip install ruff==0.16.4
python tools/generate_fixture.py
python -m unittest discover -s sdk/python/tests -v
ruff check sdk/python/src sdk/python/tests sdk/python/examples tools
python tools/check_repository.py
cmake -S sdk/cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --config Release
ctest --test-dir build/cmake --build-config Release --output-on-failure
```

For documentation changes, build both languages:

```console
python -m pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs/en build/docs/en
sphinx-build -W --keep-going -b html docs/zh_CN build/docs/zh-cn
```

PFB/PFC v1 compatibility must be preserved within SDK 1.x. Changing the PFB
byte layout or an existing PFC field requires a new format version.
