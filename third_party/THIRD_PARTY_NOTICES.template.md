# Third-party notices completion template

This template is an audit checklist, not a license grant. Before producing a
public Windows archive, replace it with `THIRD_PARTY_NOTICES.txt`, attach the
license text that applies to each exact bundled version under
`third_party/licenses/`, and have the project owner confirm the completed
record.

## pPreProc-owned runtime

- Components: `pParse.exe`, pParse2+, pXtract executables, models, and
  configuration files.
- Required record: copyright owner, approved redistribution terms, and the
  relationship between the standalone release and pFind 3.2.3.

## Vendor data-access runtimes

| Runtime observed in pFind 3.2.3 | Version observed | Required release action |
|---|---|---|
| Thermo Fisher RawFileReader | 5.0.0.93 | Obtain and include the matching official license; verify the permitted distribution form. |
| Bruker `timsdata.dll` | 2.21.104.32-342-vc142 | Obtain the matching TDF SDK terms. If public redistribution is not explicit, require users to install/download the SDK from Bruker. |
| SCIEX Clearcore | 2.0.1020.0 family | Obtain the matching WIFF Reader SDK/EULA and distribute only components expressly listed as redistributable. Review `Clearcore2.Processing.dll` separately because it is not present in the legacy Appendix-A list located during this audit. |

For every vendor runtime, record its official download page, exact license
file, version, required end-user terms, and any attribution/indemnification or
non-commercial-use conditions. A copy already present in pFind is not by
itself evidence of permission to repackage it.

## Embedded pParse2+ runtime

The inspected PyInstaller-style bundle contains CPython 3.12, OpenSSL 3.0.11,
SQLite, NumPy/OpenBLAS, pandas, psutil, pytz, setuptools and vendored packages,
PyYAML, and Microsoft runtime files. The final notice must preserve the
license and attribution text for the exact embedded versions. If exact package
metadata is unavailable from the frozen directory, rebuild pParse2+ from a
locked environment that emits a dependency inventory and license bundle.

## Other libraries in the runtime manifest

Verify and include the exact applicable terms for SQLite, Apache log4net,
Mono.Options, Ionic.Zlib/DotNetZip, and every remaining copied binary. For
Microsoft C/C++ runtimes, prefer the current official Redistributable
installer as a documented prerequisite; copying individual DLLs is permitted
only when the project is entitled to do so under the applicable Microsoft
license.

## Completion declaration

The final `THIRD_PARTY_NOTICES.txt` should state:

1. the release version and archive name;
2. every third-party component actually included;
3. the exact component version and copyright holder;
4. the governing license and location of its full text;
5. any required installation, attribution, non-endorsement, or end-user terms;
6. the name/date of the project-owner review.
