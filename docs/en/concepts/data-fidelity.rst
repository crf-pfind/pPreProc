========================
Data fidelity and scope
========================

Peak arrays
===========

PFB stores each exported m/z and intensity value as little-endian IEEE 754
binary64. The format does not apply decimal rounding, quantization, or lossy
recompression to those values.

Metadata
========

PFC retains the metadata required by the validated preprocessing and indexed
access workflows. Its named fields cover spectrum identity and linkage,
retention time, instrument context, activation and precursor attributes, peak
count, and PFB byte boundaries.

PFC does not serialize every attribute exposed by every vendor API.

==============================  ============================================
Data                            v1 guarantee
==============================  ============================================
Exported m/z and intensity      Stored as binary64 without format-level loss
Core named PFC fields           Preserved according to the v1 specification
Additional PFC columns          Accepted by compatible readers
All vendor-native metadata      Not guaranteed
Native identifier strings       Not guaranteed by a dedicated v1 field
Ion-mobility coordinates        Not guaranteed by the core v1 fields
==============================  ============================================

Retain the original vendor data when a workflow needs a field outside the
declared PFB/PFC contract. Readers must not infer an unrepresented value from
spectrum order or another field.
