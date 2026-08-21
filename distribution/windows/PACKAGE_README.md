# pPreProc for Windows

This archive contains the pPreProc preprocessing application and the runtime
files required by this release.

## Run

```powershell
.\ppreproc.ps1 -Input D:\data\sample.raw
.\ppreproc.ps1 -Config D:\work\pParse2Plus.yaml
.\ppreproc.ps1 -Version
```

Specify exactly one of `-Input` and `-Config`. See the version-matched online
documentation at https://ppreproc.readthedocs.io/.

## Verify the archive

`SHA256SUMS.txt` records the checksum of every packaged file. Verify the ZIP
checksum against the value published with the GitHub Release before use.

## Terms and support

`APPLICATION_LICENSE.txt` governs the proprietary application. Public launcher
components and third-party files are covered by the accompanying notices and
license texts.

Report reproducible defects at https://github.com/crf-pfind/pPreProc/issues.
Do not attach restricted vendor data or confidential logs.
