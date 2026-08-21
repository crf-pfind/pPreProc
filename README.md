# pPreProc

[![CI](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml/badge.svg)](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/ppreproc/badge/?version=latest)](https://ppreproc.readthedocs.io/en/latest/)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)

pPreProc is a Windows application for mass-spectrometry data preprocessing.
Its indexed PFB/PFC interface supports fast downstream spectrum access.

[Download](https://github.com/crf-pfind/pPreProc/releases) ·
[Documentation](https://ppreproc.readthedocs.io/en/latest/) ·
[中文文档](https://ppreproc.readthedocs.io/zh-cn/latest/) ·
[Issues](https://github.com/crf-pfind/pPreProc/issues) ·
[Discussions](https://github.com/crf-pfind/pPreProc/discussions)

## Windows application

Download `pPreProc-*-windows-x64.zip` from GitHub Releases. The automatically
generated source archives do not contain the application. Each application
release includes its checksum, license, runtime inventory, and third-party
notices.

The validated end-to-end workflow currently covers data-dependent acquisition
(DDA). PFB/PFC stores spectra independently of acquisition scheme; DIA-specific
precursor processing is under development.

## Public interfaces

The proprietary application source is not included in this repository. The
public developer components are:

| Component | Location | Version |
|---|---|---:|
| Python PFB/PFC SDK and CLI | `sdk/python/` | 1.0.0 |
| Header-only C++17 SDK | `sdk/cpp/` | 1.0.0 |
| PFB/PFC specification | `interfaces/pfb-pfc/v1/` | v1 |
| Windows packaging metadata | `distribution/windows/` | 2.5.2-rc.1 |
| English and Chinese documentation | `docs/` | latest |

Compatibility details are maintained in the
[documentation](https://ppreproc.readthedocs.io/en/latest/reference/compatibility.html).

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

## Support and licensing

- Report reproducible defects through [GitHub Issues](https://github.com/crf-pfind/pPreProc/issues).
- Use [GitHub Discussions](https://github.com/crf-pfind/pPreProc/discussions) for questions and proposals.
- Report vulnerabilities according to the [security policy](.github/SECURITY.md).
- Public contributions follow the [contribution guide](.github/CONTRIBUTING.md).

Public source files are licensed under [BSD-3-Clause](LICENSE). The Windows
application and bundled third-party runtimes are governed by the terms included
with each release. Citation metadata are available in [CITATION.cff](CITATION.cff).
