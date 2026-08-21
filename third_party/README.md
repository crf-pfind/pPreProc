# Third-party runtime boundary

This directory contains notices only. Third-party binaries are not committed
to the source repository.

`THIRD_PARTY_NOTICES.template.md` records the evidence that must be completed.
The binary builder requires a project-approved `THIRD_PARTY_NOTICES.txt` and
matching files under `third_party/licenses/`; neither placeholder satisfies a
public release.

The Windows preprocessing runtime may require components supplied by Thermo
Fisher Scientific, Bruker, SCIEX, Microsoft, and open-source projects including
SQLite, log4net, Mono.Options, and Ionic.Zlib. Their inclusion in an existing
pFind installation does not by itself establish permission to redistribute
them in a new standalone archive.

The release builder therefore uses an explicit manifest and requires the
project owner to acknowledge that redistribution rights have been reviewed.
Where redistribution is not authorized, the public release must instead
provide installation instructions for obtaining the dependency from its
official source.
