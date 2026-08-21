# PFB/PFC v1 format specification

- Status: normative specification
- Format version: 1
- Byte order: little-endian
- Text encoding: UTF-8

Normative terms **MUST**, **SHOULD**, and **MAY** are used as in RFC 2119.

## 1. Pairing and record identity

A dataset consists of `name.pfb` and `name.pfc`. The PFB footer ordinal,
the PFB record ordinal, and the corresponding PFC data-row ordinal MUST refer
to the same spectrum. Ordinals are zero based in the public API. `ScanNo` is a
metadata value and need not equal the ordinal.

PFB contains peak arrays and a footer index. PFC is a UTF-8, tab-delimited
metadata table whose first row contains column names.

## 2. Primitive types

| Name | Encoding | Size |
|---|---|---:|
| `int32` | signed two's-complement integer | 4 bytes |
| `uint32` | unsigned integer | 4 bytes |
| `uint64` | unsigned integer | 8 bytes |
| `binary64` | IEEE 754 double-precision floating point | 8 bytes |

All numeric values MUST be stored in little-endian order. The m/z and intensity
arrays use `binary64`; they are not 32-bit floats.

## 3. PFB header

The fixed header is 24 bytes:

| Offset | Type | Field | v1 meaning |
|---:|---|---|---|
| 0 | `int32` | `reserved_1` | reserved; reader MUST NOT interpret |
| 4 | `int32` | `reserved_2` | reserved; reader MUST NOT interpret |
| 8 | `int32` | `reserved_3` | reserved; reader MUST NOT interpret |
| 12 | `uint64` | `index_address` | absolute byte offset of footer index |
| 20 | `int32` | `spectrum_count` | number of records and PFC data rows |

For an empty file, `index_address` is 24 and `spectrum_count` is zero.

The historical header does not contain a magic string or an explicit version
field. “v1” therefore denotes files that satisfy this complete structural
contract, including the valid footer index. The API reports version 1 only
after those checks succeed.

## 4. Spectrum record

Records occupy the byte range from offset 24 to `index_address`. For each
record, in order:

1. `uint32 property_byte_count`;
2. exactly `property_byte_count` bytes of UTF-8 property text;
3. `uint32 peak_count`;
4. `peak_count` little-endian `binary64` m/z values;
5. `peak_count` little-endian `binary64` intensity values.

The record ends immediately after the intensity array; no alignment padding is
defined in v1. Readers SHOULD preserve the property text but MUST use PFC as
the versioned tabular metadata interface.

## 5. Footer index and random access

At `index_address`, PFB contains exactly `spectrum_count` `uint64` values.
Entry `i` is the absolute byte offset of record `i`. The first entry MUST be
24, entries MUST be strictly increasing, and the final record MUST end at
`index_address`.

A compliant random-access reader retrieves record `i` by reading footer entry
`i` and footer entry `i+1` (or `index_address` for the final record). It MUST
NOT be necessary to parse records `0..i-1`.

## 6. PFC metadata

PFC MUST have one header row and exactly `spectrum_count` data rows. It MAY
begin with a UTF-8 byte-order mark. Rows are terminated by LF or CRLF and
fields are separated by one tab. v1 defines no quoting or escaping mechanism;
a field value therefore MUST NOT contain a literal tab, CR, or LF. Empty fields
are allowed where noted.

The v1 columns are:

| Field | Representation | Meaning/unit |
|---|---|---|
| `ScanNo` | non-empty identifier | unique scan number |
| `PrecursorScan` | identifier or empty | parent scan number; empty if none is declared |
| `RetTime` | decimal number | retention time in seconds |
| `SpectrumType` | text | `MS1`, `MS2`, or `MS3` |
| `InstrumentType` | text | source instrument category |
| `IonInjectionTime` | decimal or empty | ion injection time in milliseconds |
| `activationType` | text or empty | fragmentation/activation type |
| `activationCenter` | decimal or empty | isolation center in m/z |
| `NCE` | decimal or empty | normalized collision energy |
| `monoIsotopicMz` | decimal or empty | monoisotopic precursor m/z |
| `upperCharge` | integer or empty | upper charge bound |
| `lowerCharge` | integer or empty | lower charge bound |
| `activationWindow` | decimal or empty | isolation-window width in m/z |
| `NumberofPeaks` | non-negative integer | PFB `peak_count` for the same ordinal |
| `StartPos` | non-negative integer | absolute PFB byte offset of the record |
| `EndPos` | non-negative integer | absolute byte offset immediately after the record |

Readers MUST select fields by header name rather than fixed column number and
SHOULD tolerate additional columns. The listed columns MUST be present, though
values explicitly marked “or empty” may be empty. `ScanNo` MUST be non-empty
and unique. `NumberofPeaks`, `StartPos`, and `EndPos` MUST agree with the
corresponding PFB record and footer index.

## 7. Fidelity boundary

PFB preserves the numeric m/z and intensity values supplied to the writer as
binary64 values. The format itself performs no decimal rounding, quantization,
or lossy compression.

PFC intentionally exposes the metadata required by the validated preprocessing
and indexed-access workflows. It is not a complete serialization of all fields
available through every vendor API. In the tested v1 files, no dedicated field
guarantees preservation of the original vendor native-ID string. Tested legacy
TIMS PFC files also do not expose explicit frame, mobility-coordinate, or
mobility-scan-interval fields. Consumers requiring such fields MUST retain and
consult the vendor source data and MUST NOT infer their preservation merely
from spectrum order.

## 8. Validation requirements

A conforming reader MUST reject:

- files shorter than 24 bytes;
- negative `spectrum_count` values;
- an `index_address` outside `[24, file_size]`;
- a footer whose byte length is not `8 * spectrum_count`;
- non-increasing or out-of-range record offsets;
- records whose decoded length differs from their indexed boundary; and
- a PFC row count different from `spectrum_count`, when PFC is required;
- a missing v1 PFC column or duplicate/empty `ScanNo`; and
- PFC `NumberofPeaks`, `StartPos`, or `EndPos` values inconsistent with PFB.

Full validation SHOULD decode all records and verify all declared parent links.

## 9. Versioning

This document describes PFB/PFC v1 as emitted by the validated pPreProc/pXtract
runtime. Any incompatible byte-layout change requires a new format version and
a separate specification with an explicit discriminator. Readers MUST NOT
silently guess the layout of an unrecognized or structurally inconsistent
file.
