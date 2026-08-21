# pPreProc

[![CI](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml/badge.svg)](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/ppreproc/badge/?version=latest)](https://ppreproc.readthedocs.io/en/latest/)

pPreProc is a Windows application for mass-spectrometry data preprocessing.
Its indexed PFB/PFC interface supports fast downstream spectrum access.

[Download](https://github.com/crf-pfind/pPreProc/releases) ·
[Documentation](https://ppreproc.readthedocs.io/en/latest/) ·
[中文文档](https://ppreproc.readthedocs.io/zh-cn/latest/) ·
[Issues](https://github.com/crf-pfind/pPreProc/issues) ·
[Discussions](https://github.com/crf-pfind/pPreProc/discussions)

## Download

Download `pPreProc-<version>-windows-x64.zip` and its checksum from
[GitHub Releases](https://github.com/crf-pfind/pPreProc/releases). The
automatically generated source archives are not runnable application packages.
Installation and command examples are in the
[documentation](https://ppreproc.readthedocs.io/en/latest/getting-started/installation.html).

## Repository contents

This repository contains the public components that accompany the Windows
application:

- [Python PFB/PFC SDK and CLI](sdk/python/)
- [C++17 PFB/PFC SDK](sdk/cpp/)
- [PFB/PFC format specification](interfaces/pfb-pfc/)
- [English and Chinese documentation](docs/)

The proprietary application source and vendor SDK source are not included.
The supported application, SDK, and format combinations are listed in the
[compatibility reference](https://ppreproc.readthedocs.io/en/latest/reference/compatibility.html).

## Python SDK

```console
git clone https://github.com/crf-pfind/pPreProc.git
cd pPreProc
python -m pip install .
ppreproc-pfb validate sdk/python/tests/fixtures/minimal.pfb --full
```

```python
from ppreproc_pfb import PFBReader

with PFBReader("run.pfb") as reader:
    spectrum = reader.get_spectrum_by_scan(102)
```

See the [Python](https://ppreproc.readthedocs.io/en/latest/reference/python-api.html)
and [C++](https://ppreproc.readthedocs.io/en/latest/reference/cpp-api.html)
references for the complete public API.

## Support and license

- Report reproducible defects through [GitHub Issues](https://github.com/crf-pfind/pPreProc/issues).
- Use [GitHub Discussions](https://github.com/crf-pfind/pPreProc/discussions) for questions and proposals.
- Report vulnerabilities according to the [security policy](.github/SECURITY.md).
- Public contributions follow the [contribution guide](.github/CONTRIBUTING.md).

The public SDKs, specification, examples, and documentation are licensed under
[BSD-3-Clause](LICENSE). The Windows application and bundled runtimes are
governed by the terms included with each application release. Citation metadata
for the public PFB/PFC SDK are available in [CITATION.cff](CITATION.cff).
