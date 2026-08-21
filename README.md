# pPreProc

[![CI](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml/badge.svg)](https://github.com/crf-pfind/pPreProc/actions/workflows/ci.yml)
[![CITATION.cff](https://img.shields.io/badge/citation-CFF-4B8BBE.svg)](CITATION.cff)
[![License: BSD-3-Clause](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)

pPreProc is a mass-spectrometry data-preprocessing framework that separates
vendor-data extraction, precursor processing, and indexed downstream access.
The current validated release targets data-dependent acquisition (DDA)
workflows on Windows. Its PFB/PFC representation is acquisition-scheme
agnostic; integration of DIA precursor-processing workflows is ongoing.

This repository is the canonical home of pPreProc, which was originally
distributed inside pFind 3.2.3. It separates two release surfaces:

1. an inspectable source release containing the versioned PFB/PFC v1 contract,
   dependency-free reference readers, tests, and release tooling; and
2. a separately assembled Windows runtime asset containing the compiled
   preprocessing application and only its required data-access dependencies.

This source release does not include the application source projects for the
compiled pParse/pParse2+/pXtract components. The repository must therefore not
be described as a complete open-source release of the Windows application.
See the [release model](docs/RELEASE_MODEL.md) and
[source-provenance record](docs/SOURCE_PROVENANCE.md).

## Repository contents

- `src/ppreproc_pfb/`: Python 3 reference reader and validation CLI.
- `cpp/`: header-only C++17 reader and a minimal example.
- `docs/PFB_PFC_SPECIFICATION_V1.md`: normative v1 format description.
- `docs/ARCHITECTURE.md`: separation of the Windows application and the
  cross-platform storage interface.
- `docs/RELEASE_MODEL.md`: source-tag and Windows-asset publication model.
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

The release archive will provide a single `ppreproc.ps1`/`ppreproc.cmd` entry
point around the existing pParse2+ runtime. Typical calls are:

```powershell
.\ppreproc.ps1 -Input D:\data\sample.raw
.\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
```

The source package deliberately does not copy the whole pFind `bin` directory.
The release builder uses an explicit runtime manifest so that pFind search and
reporting programs are not presented as pPreProc components.

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

Version 1.0.0 of the reader/specification source was released on 2026-08-21
and is useful independently of the Windows runtime. Every source tag is
validated against the synthetic fixture and the repository release checks.

The Windows runtime is a separate release asset. It must not be uploaded until
the team confirms redistribution rights for the pPreProc executables and every
bundled runtime, completes the version-specific notice bundle, and passes a
clean-machine test. See `RELEASE_BLOCKERS.md` and `third_party/README.md`.

## Citation

Use the metadata in `CITATION.cff`. After the public repository is connected
to Zenodo, the archived release DOI should be preferred for the exact software
version used in an analysis.

## License

The original source code in this repository is available under the
[BSD 3-Clause License](LICENSE). Third-party software and any future Windows
runtime asset remain subject to their own terms and the independent release
gate described above.
