# Interface validation record

Validation date: 2026-08-21
Release: 1.0.0

## Synthetic fixture

Both Python and C++ readers were tested against `tests/fixtures/minimal.pfb`
and its PFC companion. Tests cover direct index access, scan-number access,
parent-MS1 resolution, numeric binary64 arrays, XIC extraction, full decode,
CLI output, missing PFC handling, and rejection of truncation and inconsistent
PFC peak-count metadata.

Python result: 7/7 unit tests passed independently on CPython 3.9.13, 3.10.0,
and 3.14.3.
C++ result: the C++17 example compiled with MinGW-w64 g++ 8.1.0 using
`-Wall -Wextra -pedantic` and returned the expected scan, peak count, and
parent scan. The repository CI repeats the C++ test through CMake/CTest.

## Current indexed output

A full decode was run on the existing current indexed output
`HEK293_FAIMS_60_70_80_Fr6_CV80.pfb` and its PFC companion:

| Check | Result |
|---|---:|
| PFB spectra/PFC rows | 14,455 |
| Decoded spectra | 14,455 |
| Decoded peaks | 3,498,412 |
| Resolved parent links | 11,477 |
| PFC peak-count/byte-boundary mismatches | 0 |
| Structural/index errors | 0 |

The test data are not distributed in this repository. This record does not
replace per-platform release qualification or checksums for public benchmark
data.

## Historical-layout check

A historical TIMS PFB in the project was identified as a legacy unindexed
layout and was rejected by the v1 reader as intended. It is not counted as a
failed v1 file; it lies outside the stated v1 compatibility contract.

## Windows launcher status

The PowerShell launcher passed version reporting and dry-run resolution against
the inspected pFind 3.2.3 runtime: it located `pParse2Plus.exe`, preserved a
literal input/configuration path, and selected the executable directory as its
working directory. An end-to-end preprocessing run from the final standalone
archive on a clean Windows machine remains a release-blocker check; a dry run
is not presented as equivalent to that qualification.
