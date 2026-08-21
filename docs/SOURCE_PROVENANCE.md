# Source and binary provenance

Audit date: 2026-08-20

## Original source in this repository

The Python PFB/PFC reader, header-only C++17 reader, validator, tests,
synthetic fixture generator, command wrappers, runtime manifest, and release
engineering documents were prepared for this standalone repository.

## Compiled application input

The audited pFind 3.2.3 development tree contains the historical pParse2,
pParse2+, and pXtract application projects in addition to the compiled
runtime. Those projects remain coupled to platform-specific build settings and
vendor data-access SDKs, and are not part of the initial cross-platform
reader/specification source package. The independently runnable Windows asset
is therefore assembled through the explicit runtime manifest and remains
subject to its separate redistribution and clean-machine validation gate.

This finding does not determine ownership or redistribution rights. The
project owner must confirm the right to distribute the pFind-owned compiled
components separately, and the applicable terms for every third-party runtime
must be documented before the Windows ZIP is published.

## Reproducibility boundary

The public reader source and synthetic tests reproduce and verify the declared
PFB/PFC byte-level access behavior. Rebuilding the complete Windows
preprocessing application is outside the initial source-package boundary until
the historical application projects and their SDK dependencies complete a
separate build, licensing, and redistribution review.
