# pPreProc

[![CI](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml/badge.svg)](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/ppreproc/badge/?version=latest)](https://ppreproc.readthedocs.io/en/latest/)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
[![Citation](https://img.shields.io/badge/citation-CFF-4B8BBE.svg)](CITATION.cff)

pPreProc is a mass-spectrometry preprocessing application with an indexed
PFB/PFC interface for fast downstream access. The validated application
workflow currently covers data-dependent acquisition (DDA); the PFB/PFC
storage interface is acquisition-scheme agnostic.

[Documentation](https://ppreproc.readthedocs.io/en/latest/) ·
[中文文档](https://ppreproc.readthedocs.io/zh-cn/latest/) ·
[Releases](https://github.com/crf-pfind/pPreProc/releases) ·
[SDK reference](https://ppreproc.readthedocs.io/en/latest/reference/python-api.html) ·
[Support](SUPPORT.md)

## Repository scope

This repository is the public developer and distribution entry point for
pPreProc. It does not contain the proprietary source code of the Windows
application.

| Component | Availability | Location |
|---|---|---|
| pPreProc Windows application | Proprietary binary distribution | GitHub Releases |
| Python PFB/PFC SDK | Public source, BSD-3-Clause | `sdk/python/` |
| C++17 PFB/PFC SDK | Public source, BSD-3-Clause | `sdk/cpp/` |
| PFB/PFC specification | Public | `interfaces/pfb-pfc/` |
| Examples and documentation | Public | `examples/`, `docs/` |
| Core application source | Not included | — |

The application was previously distributed with pFind 3.2.3. The first
standalone Windows package is available as a release candidate on the Releases
page. GitHub's automatically generated source archives are not application
installers; use the asset named `pPreProc-*-windows-x64.zip`.

## Quick start

Install the Python reference SDK from a clone of this repository:

```console
git clone https://github.com/crf-pfind/pPreProc.git
cd pPreProc
python -m pip install .
ppreproc-pfb validate sdk/python/tests/fixtures/minimal.pfb --full
```

Read an indexed PFB/PFC pair:

```python
from ppreproc_pfb import PFBReader

with PFBReader("run.pfb") as reader:
    spectrum = reader.get_spectrum_by_scan(102)
    parent_ms1 = reader.get_parent_ms1(spectrum)
```

The companion `run.pfc` file is selected automatically. Direct record access
uses the PFB footer index and does not decode preceding spectra.

## Repository layout

```text
docs/                  Versioned English and Chinese documentation
distribution/windows/ Windows packaging metadata and launchers
examples/              Minimal SDK examples
interfaces/pfb-pfc/    Public format contract
sdk/python/            Python reference SDK and tests
sdk/cpp/               Header-only C++17 reference SDK
tools/                 Repository and packaging utilities
```

## Versions and compatibility

The application, SDK, and file format are versioned independently.

| Surface | Current public version |
|---|---:|
| Python SDK | 1.0.0 |
| C++ SDK | 1.0.0 |
| PFB/PFC format | v1 |
| Standalone application | 2.5.2-rc.1 |

See [COMPATIBILITY.md](COMPATIBILITY.md) before integrating a reader or
upgrading a deployed workflow.

## Support and contributions

- Reproducible defects: [GitHub Issues](https://github.com/crf-pfind/pPreProc/issues)
- Usage questions and proposals: [GitHub Discussions](https://github.com/crf-pfind/pPreProc/discussions)
- Security reports: follow [SECURITY.md](SECURITY.md)
- Documentation, examples, SDKs, and interface contributions: see
  [CONTRIBUTING.md](CONTRIBUTING.md)

Do not upload vendor data or other restricted files unless you are authorized
to share them.

## Citation

Citation metadata are provided in [CITATION.cff](CITATION.cff). Record the
pPreProc application version, SDK version, PFB/PFC format version, platform,
and configuration used for a reproducible analysis.

## License

Unless a subdirectory states otherwise, the public source and documentation in
this repository are licensed under the [BSD 3-Clause License](LICENSE). The
separately distributed pPreProc application and third-party runtime components
are governed by the terms supplied with their release. See [NOTICE](NOTICE).
