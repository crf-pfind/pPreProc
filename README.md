# pPreProc

[![CI](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml/badge.svg)](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml)
[![CITATION.cff](https://img.shields.io/badge/citation-CFF-4B8BBE.svg)](CITATION.cff)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)

pPreProc is a mass-spectrometry data-preprocessing framework that separates
vendor-data extraction, precursor processing, and indexed downstream access.
The currently validated workflow targets data-dependent acquisition (DDA)
workflows on Windows. Its PFB/PFC representation is acquisition-scheme
agnostic; integration of DIA precursor-processing workflows is ongoing.

This repository is the canonical home of pPreProc, which was originally
distributed inside pFind 3.2.3. It separates two publication channels:

1. bilingual, versioned online documentation for the PFB/PFC contract,
   reference readers, command-line interface, and integration guidance; and
2. GitHub Releases reserved for a separately assembled, runnable Windows
   application containing the compiled preprocessing components and only their
   required runtime dependencies.

This repository does not include the application source projects for the
compiled pParse/pParse2+/pXtract components. The repository must therefore not
be described as a complete open-source release of the Windows application.
See the [release model](docs/RELEASE_MODEL.md) and
[source-provenance record](docs/SOURCE_PROVENANCE.md).

## Repository contents

- `src/ppreproc_pfb/`: Python 3 reference reader and validation CLI.
- `cpp/`: header-only C++17 reader and a minimal example.
- `docs/en/` and `docs/zh_CN/`: parallel English and Simplified Chinese
  documentation sources for Read the Docs.
- `docs/PFB_PFC_SPECIFICATION_V1.md`: normative v1 format description.
- `docs/ARCHITECTURE.md`: separation of the Windows application and the
  cross-platform storage interface.
- `docs/RELEASE_MODEL.md`: online-documentation and software-release model.
- `docs/SOURCE_PROVENANCE.md`: audited boundary of source and compiled inputs.
- `runtime/`: created by the release builder from an authorized pFind runtime.
- `tests/fixtures/`: small synthetic data for testing the public interface.
- `third_party/`: dependency notices; third-party binaries are not committed.

The PFB/PFC reader is independent of the Windows preprocessing runtime and can
be used on Linux, macOS, and Windows.

See the [architecture and public boundaries](docs/ARCHITECTURE.md) for the
precise distinction between the standalone application, PFB/PFC readers, and
the pFind search suite.

The current technical status and the independent publication gate for the
Windows runtime are recorded in the
[release-readiness record](docs/RELEASE_READINESS_2026-08-20.md).

## Documentation

The public interface is documented as a Read the Docs site rather than a
GitHub Release artifact:

- [English documentation](https://ppreproc.readthedocs.io/en/latest/)
- [简体中文文档](https://ppreproc.readthedocs.io/zh-cn/latest/)

The site configuration is already in this repository. Until the two Read the
Docs projects are imported, the same content can be read from
[`docs/en/`](docs/en/index.rst) and [`docs/zh_CN/`](docs/zh_CN/index.rst).
Maintainer setup and local build commands are in
[`docs/README.md`](docs/README.md).

## Read PFB/PFC in Python

```powershell
python -m pip install .
ppreproc-pfb info tests/fixtures/minimal.pfb
ppreproc-pfb validate tests/fixtures/minimal.pfb --full
ppreproc-pfb spectrum tests/fixtures/minimal.pfb --scan 102
```

```python
from ppreproc_pfb import PFBReader

with PFBReader("run.pfb") as spectra:
    ms2 = spectra.get_spectrum_by_scan(102)
    parent_ms1 = spectra.get_parent_ms1(ms2)
    xic = spectra.extract_xic(500.2, ppm=10, rt_start=0, rt_end=20)
```

`get_spectrum()` performs direct footer-indexed retrieval; it does not decode
the preceding records. See the [v1 specification](docs/PFB_PFC_SPECIFICATION_V1.md)
for exact types and compatibility guarantees, and see
[`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for the explicit distinction
between indexed v1 files and older unindexed PFB files.

## Run the Windows preprocessor

A future application Release will provide a single
`ppreproc.ps1`/`ppreproc.cmd` entry point around the existing pParse2+ runtime.
Typical calls are:

```powershell
.\ppreproc.ps1 -Input D:\data\sample.raw
.\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
```

The future software package deliberately does not copy the whole pFind `bin`
directory. The release builder uses an explicit runtime manifest so that pFind
search and reporting programs are not presented as pPreProc components.

## Data fidelity and scope

PFB stores each exported m/z and intensity value as little-endian IEEE 754
binary64. The reader performs no numeric rounding or lossy recompression.
PFC retains the metadata fields required by the validated preprocessing and
downstream-access workflows. It is not a lossless serialization of every
vendor-specific metadata attribute; applications that require an unlisted
vendor field should retain and consult the source data.

The tested v1 PFC schema does not expose every platform-specific native
identifier or ion-mobility coordinate. These boundaries are stated explicitly
in the specification rather than being inferred by downstream readers.

## Reproducibility

```powershell
python tools\generate_fixture.py
python -m unittest discover -s tests -v
python tools\validate_release.py
```

Release maintainers use separate gates:

```powershell
python tools\validate_release.py --artifact source
python tools\validate_release.py --artifact binary --source-bin D:\path\to\authorized\bin
```

The fixture is synthetic and contains no vendor data. A release archive is
also accompanied by a SHA-256 manifest.

The C++ reader can be configured and tested through CMake:

```powershell
cmake -S cpp -B build/cmake -DCMAKE_BUILD_TYPE=Release
cmake --build build/cmake --config Release
ctest --test-dir build/cmake --build-config Release --output-on-failure
```

The reference reader has additionally completed a full decode of a current
14,455-spectrum indexed output; see [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Release status

The historical `v1.0.0` tag established the initial public PFB/PFC interface
baseline. On the current main branch, that interface is maintained through the
versioned bilingual documentation site and repository source, not as a
separate Release download.

Future GitHub Releases are reserved for runnable pPreProc software. A Windows
package must not be uploaded until the team confirms redistribution rights for
the pPreProc executables and every bundled runtime, completes the
version-specific notice bundle, and passes a clean-machine test. See
`RELEASE_BLOCKERS.md` and `third_party/README.md`.

## Citation

Use the metadata in `CITATION.cff`. After the public repository is connected
to Zenodo, the archived release DOI should be preferred for the exact software
version used in an analysis.

## License

The original source code in this repository is available under the
[BSD 3-Clause License](LICENSE). Third-party software and any future Windows
runtime asset remain subject to their own terms and the independent release
gate described above.
