# PFB/PFC compatibility

## Indexed PFB/PFC v1

The public readers target the current indexed layout defined in
`PFB_PFC_SPECIFICATION_V1.md`. The footer contains one absolute record offset
per spectrum, enabling direct retrieval without scanning prior records.

Validated current output:

- source component: the pXtract runtime bundled with the working pFind 3.2.3
  installation;
- spectra: 14,455;
- peaks decoded: 3,498,412;
- parent links resolved: 11,477;
- result: full structural, record, and parent-link validation passed.

## Legacy unindexed PFB

Some historical project files use an earlier streaming layout without the v1
footer index. They can be distinguished because the header does not provide a
valid `index_address` and the file tail is not an array of record offsets.

The v1 readers intentionally reject these files instead of scanning them and
calling the result random access. This protects the documented performance and
prevents a corrupt current file from being silently misinterpreted. A legacy
file should be regenerated with the indexed pXtract release from the retained
vendor source data. If a migration utility is later published, it will be
documented separately and will not change the v1 contract.

## Platform and acquisition scope

The PFB/PFC representation stores extracted spectra and does not itself impose
a DDA precursor-selection model. The currently validated end-to-end pParse
workflow is DDA. DIA-specific pParse integration is ongoing and is not claimed
as a v1.0.0 validation result.
