# PFB/PFC interface

PFB/PFC is the versioned storage interface used by pPreProc for indexed
spectrum access.

- `v1/specification.md` is the normative v1 contract.
- PFB contains spectrum records and a footer index.
- PFC contains the corresponding named metadata rows.
- The Python and C++ reference SDKs are maintained under `sdk/`.

An incompatible byte-layout or field-semantics change requires a new versioned
specification. Additional optional PFC columns may be introduced without
changing v1 readers.
