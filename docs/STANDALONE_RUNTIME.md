# Standalone Windows runtime

## Components

The standalone pPreProc runtime has three functional layers:

1. **pXtract** reads supported vendor data and emits MS text or PFB/PFC.
2. **pParse2** performs precursor-related preprocessing for the validated DDA
   workflow.
3. **pParse2+** provides the unified command/configuration entry point and the
   enhanced isotope-envelope logic evaluated in the accompanying article.

The pFind database search engine, GUI, report tools, and unrelated utilities
are outside the standalone pPreProc boundary.

## Supported entry points

The wrapper accepts either a single vendor input or an existing pParse2+ YAML
configuration. It resolves the bundled runtime relative to its own location so
that users do not need to add pFind directories to `PATH`.

```powershell
.\ppreproc.ps1 -Input D:\data\sample.raw
.\ppreproc.ps1 -Config D:\work\pParse2Plus_cfg.yaml
.\ppreproc.ps1 -Input D:\data\sample.raw -DryRun
```

The current validated workflow is Windows-based and DDA-based. PFB/PFC itself
can represent spectra from DDA or DIA extraction, but DIA-specific precursor
processing through pParse is not claimed as validated in v1.0.0.

## Provenance

For reproducibility, record the pPreProc release tag, input platform, command
or configuration file, PFB/PFC checksum, and downstream software version.
