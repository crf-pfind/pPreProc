# Compatibility

pPreProc uses separate versions for the application, public SDKs, and PFB/PFC
file format.

| Application | Python SDK | C++ SDK | PFB/PFC | Status |
|---|---|---|---|---|
| Not yet released | 1.0.x | 1.0.x | v1 | Current public interface |

## Guarantees for PFB/PFC v1

- SDK 1.x reads indexed files that satisfy the v1 specification.
- Readers select PFC fields by name and accept additional columns.
- Existing field meanings and units do not change within v1.
- An incompatible PFB layout or PFC field change requires a new format
  specification.
- Historical unindexed PFB files are rejected rather than guessed as v1.

## Platform scope

The Python SDK supports Python 3.9 or newer on Windows, Linux, and macOS. The
C++ SDK requires a C++17 compiler and the standard library. The standalone
preprocessing application targets Windows.

The validated end-to-end application workflow currently covers DDA. PFB/PFC
stores spectra without imposing a DDA precursor model; DIA-specific precursor
processing in the application remains under development.
