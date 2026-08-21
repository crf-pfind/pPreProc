# Windows runtime dependency audit

Audit date: 2026-08-20
Source inspected: pFind 3.2.3 working installation

## Standalone boundary

The `runtime-manifest.json` whitelist includes pParse2/pParse2+, the pXtract
executables, their model/configuration files, and only the runtime libraries
needed to read supported vendor formats. The pFind search engine, GUI, report
programs, result utilities, debug symbols, object files, logs, and user guides
are excluded.

| Group | Examples | Technical status | Public redistribution status |
|---|---|---|---|
| pPreProc core | `pParse.exe`, pParse2+, model files | present | project-owner approval required |
| Thermo access | CommonCore RawFileReader libraries | present | vendor terms must be confirmed |
| Bruker access | `timsdata.dll` | present | vendor terms must be confirmed |
| SCIEX access | Clearcore libraries | present | vendor terms must be confirmed |
| Open-source runtime | SQLite, log4net, Mono.Options, Ionic.Zlib | present | license notices/source obligations must be assembled |
| Microsoft runtime | VC runtime libraries | present | redistributable-package terms must be followed |
| Embedded pParse2+ runtime | Python/native package bundle | present | bundled package notices must be preserved |

“Present” means that the file is available in the inspected pFind installation
and the release manifest resolves it. It does not constitute a legal conclusion
that the file may be redistributed in a new archive.

## Version and license-evidence findings

The inspected runtime identifies Thermo Fisher RawFileReader 5.0.0.93, Bruker
`timsdata.dll` 2.21.104.32-342-vc142, and the SCIEX Clearcore 2.0.1020.0
family. No matching vendor EULA was stored beside those files in the pFind
directory. The public Thermo project supplies a separate license document;
the matching version must be retained with a redistributed bundle. Bruker SDK
terms must be obtained for the exact TDF SDK version rather than inferred from
the presence of `timsdata.dll`.

A legacy SCIEX WIFF Reader developer license located during the audit lists
specific Clearcore files as distributable subject to conditions. Most observed
files match that historical list, but `Clearcore2.Processing.dll` does not.
That historical document is not proof that the installed version is covered;
the exact SDK/EULA and any required end-user agreement must be confirmed before
any Clearcore file is uploaded.

The frozen pParse2+ directory includes CPython 3.12, OpenSSL 3.0.11,
SQLite, NumPy/OpenBLAS, pandas, psutil, pytz, setuptools and vendored packages,
PyYAML, and Microsoft runtime files. Its distribution metadata is incomplete,
so a public archive requires a reconstructed, version-specific notice bundle
or, preferably, a reproducible rebuild from a locked environment that retains
package metadata and licenses.

The public pFind 3.2.3 release notes state an application expiration date of
20 December 2028 and refer to an existing pFind license. This does not establish
whether the extracted preprocessing components enforce the same mechanism.
Before publication, a clean-machine test must record any activation,
license-file, or expiration dependency and the standalone documentation must
state it explicitly.

## Release policy

The build script refuses to assemble a binary archive unless the project owner
passes an explicit redistribution-rights acknowledgement and supplies the
approved project `LICENSE`, final `THIRD_PARTY_NOTICES.txt`, and matching
third-party license texts. If a vendor runtime cannot be redistributed, its
manifest entry should be replaced by an official installer/bootstrap check and
the clean-machine test repeated. For Microsoft C/C++ runtimes, the preferred
deployment is the current official Redistributable prerequisite rather than
unserviced copies of individual DLLs.

The repository's original Python/C++ reader source can be licensed separately
from the Windows executable bundle. This split permits the public, inspectable
PFB/PFC interface to be maintained as online documentation and repository
source while binary-runtime terms are being resolved, but it should not be
described as the complete standalone Windows preprocessor until that runtime is
actually available.

A subsequent audit of the pFind 3.2.3 development tree located historical
pParse2, pParse2+, and pXtract application projects. They remain coupled to
platform-specific build settings and vendor SDKs and are not included in the
current cross-platform reader source. Consequently, the repository supports
online PFB/PFC documentation and reference-reader source plus a separately
authorized compiled Windows software Release; it does not claim that the
complete Windows application is open source. See `SOURCE_PROVENANCE.md`.
